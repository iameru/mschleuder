import datetime
from random import choice

import pytest
from bs4 import BeautifulSoup as bs
from flask import url_for

from ms.db.models import Distribution, Product, Share, Station, StationHistory, Unit, db
from tests.site.test_dist import _save_product


@pytest.fixture(autouse=True, scope="module")
def distribution(test_client):

    # create dist
    # setup
    dist = Distribution(in_progress=True)
    db.session.add(dist)
    db.session.commit()
    Station.archive_all(dist.id)

    # create products
    for product in Product.query.all():
        _save_product(test_client, product)

    yield dist

    # teardown
    stations = StationHistory.query.filter_by(distribution_id=dist.id).all()
    [db.session.delete(share) for share in dist.shares]
    [db.session.delete(station) for station in stations]
    db.session.delete(dist)
    db.session.commit()


def test_shares_in_db(distribution):

    assert len(distribution.shares) != 0


def test_shares_in_overview(test_client, distribution):

    response = test_client.get(url_for("distribution.overview"))
    html = bs(response.data, "html.parser")

    products = (
        db.session.query(
            Share.id,
            Product.name,
            Product.id.label("product_id"),
            Unit.longname.label("unit_longname"),
            Unit.id.label("unit_id"),
        )
        .join(Product)
        .join(Unit)
        .join(Distribution)
        .group_by(
            Share.product_id,
            Share.unit_id,
        )
        .filter(
            Share.distribution_id == distribution.id,
            Share.product_id == Product.id,
            Share.unit_id == Unit.id,
        )
        .all()
    )

    # We will find all the information about the distribution
    started = html.find("p", {"id": "info-dist-started"})
    assert distribution.created.replace(microsecond=0).isoformat() == started.text[:-1]

    for product in products:

        # find rows
        row = html.find(
            "tr", {"id": f"overview-{product.product_id}-{product.unit_longname}"}
        )
        assert row
        assert product.name in row.text
        assert product.unit_longname in row.text


def test_detail_view(test_client, distribution):

    share = choice(distribution.shares)
    product_id = share.product_id
    unit = Unit.query.get(share.unit_id)
    product = Product.query.get(product_id)

    response = test_client.get(url_for("distribution.overview"))
    html = bs(response.data, "html.parser")

    row = html.find("tr", {"id": f"overview-{product_id}-{unit.longname}"})

    detail_view_button = row.find("button", {"id": "detail_view"})
    assert detail_view_button

    detail_view_url = detail_view_button.get("hx-get")
    assert detail_view_url

    # get detail view
    response = test_client.get(detail_view_url)
    assert response.status_code == 200

    assert response.request.path == url_for(
        "history.product_detail_view",
        product_id=product_id,
        distribution_id=distribution.id,
        unit_id=share.unit_id,
    )
    html = bs(response.data, "html.parser")

    assert product.name in html.text
