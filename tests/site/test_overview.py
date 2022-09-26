import datetime

import pytest
from bs4 import BeautifulSoup as bs
from flask import url_for

from ms.db.models import Distribution, Product, Share, Station, StationHistory, db
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
        x = _save_product(test_client, product)

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

    # get all products distributed
    products = []
    for share in Share.query.filter_by(distribution_id=distribution.id).all():
        products.append(Product.query.get(share.product_id))
    products = [p for p in set(products)]

    # We will find all the information about the distribution
    started = html.find("p", {"id": "info-dist-started"})
    assert distribution.created == datetime.datetime.fromisoformat(started.text)

    for product in products:

        # find rows
        row = html.find("tr", {"id": f"overview-{product.id}"})
        assert row
        assert product.name in row.text

        # to be continued
