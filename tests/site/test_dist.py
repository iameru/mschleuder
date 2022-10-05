import json
from random import choice, randint

import pytest
from bs4 import BeautifulSoup as bs
from flask import url_for

from ms.db.models import Distribution, Product, Share, Station, StationHistory, Unit, db


@pytest.fixture(autouse=True, scope="module")
def distribute():
    # setup
    dist = Distribution(in_progress=True)
    db.session.add(dist)
    db.session.commit()
    Station.archive_all(dist.id)

    yield dist.in_progress

    # teardown
    stations = StationHistory.query.filter_by(distribution_id=dist.id).all()
    [db.session.delete(share) for share in dist.shares]
    [db.session.delete(station) for station in stations]
    db.session.delete(dist)
    db.session.commit()


def test_post_nonvalid_data_to_save_distribution(test_client):

    response = test_client.post(url_for("distribution.save"), data={"stuff": "wrong"})
    assert response.status_code == 404


def _save_product(test_client, product: Product):

    # we have a product we want to share for this distribution, in a unit, with infos of a station at that time.
    # we would have to do this for each station
    # dist.id gets added in view
    unit = choice(product.units)
    dist = Distribution.current()
    post_data = []
    # we generate the data to post
    for station in dist.stations:

        # we have values we want to be saved (given from frontend)
        # single members each get
        single_full = randint(2, 100)
        single_half = int(single_full / 2)

        # the whole station gets
        sum_full = single_full * station.members_full
        sum_half = single_half * station.members_half

        # we build the keys
        keys = dict(
            product_id=product.id,
            stationhistory_id=station.id,
            unit_id=unit.id,
        )
        # we build the data
        data = dict(
            single_full=single_full,
            single_half=single_half,
            sum_full=sum_full,
            sum_half=sum_half,
        )
        data.update(keys)

        post_data.append(data)

    data = json.dumps(post_data)

    # we send the request
    response = test_client.post(
        url_for("distribution.save"),
        data=data,
        content_type="application/json",
        follow_redirects=True,
    )

    # we return the response for tests
    return dict(response=response, post_data=post_data)


def test_saving_of_a_distribution(test_client):

    # have to pretend a bit as the generation is in javascript
    # see test in function _save_product

    product = Product.query.get(1)
    result = _save_product(test_client, product)
    response = result.get("response")
    post_data = result.get("post_data")
    assert response.status_code == 200
    assert response.request.path == url_for("distribution.overview")

    # we expect all entries to be saved to database
    for data in post_data:

        share = Share.query.filter_by(**data).first()
        assert share


def test_saving_no_duplicates(test_client, product):

    # save a product 5 times
    product = Product.query.get(2)
    for _ in range(5):
        result = _save_product(test_client, product)
        post_data = result.get("post_data")

    # expect only one, not 5, entries for this
    query = dict(
        product_id=product.id,
        distribution_id=Distribution.current().id,
        stationhistory_id=post_data[0].get("stationhistory_id"),
        unit_id=post_data[0].get("unit_id"),
    )
    share = Share.query.filter_by(**query).all()
    assert len(share) != 5
    assert len(share) == 1

    # expect the last post request to be in database
    share = share[0]
    for key, value in post_data[0].items():
        assert share.__dict__[key] == value


def test_delete_a_distribution_from_overview(test_client):

    # get a product which was distributed
    dist = Distribution.current()
    query = (
        db.session.query(
            Share.product_id.label("product_id"), Share.unit_id.label("unit_id")
        )
        .filter(Share.distribution_id == dist.id)
        .first()
    )
    product_id = query.product_id
    unit_id = query.unit_id
    assert product_id
    assert unit_id
    product = Product.query.get(product_id)
    unit = Unit.query.get(unit_id)

    all_shares_of_product = Share.query.filter(
        Share.product_id == product.id, Share.unit_id == unit.id
    ).all()
    assert all_shares_of_product

    # get site
    response = test_client.get(url_for("distribution.overview"))
    html = bs(response.data, "html.parser")
    row = html.find("tr", {"id": f"overview-{product.id}-{unit.longname}"})
    delete_button = row.find(
        "button", {"id": f"delete-from-distribution-{product.id}-{unit.longname}"}
    )
    assert delete_button
    link = delete_button["hx-get"]
    assert link == url_for(
        "distribution.delete_from_distribution",
        product_id=product.id,
        unit_shortname=unit.shortname,
    )

    # follow modal link
    response = test_client.get(link)
    assert response.status_code == 200
    deletion_button = bs(response.data, "html.parser").find(
        "button", {"id": "confirm-deletion-button"}
    )
    assert deletion_button
    form = bs(response.data, "html.parser").find(
        "form", {"id": "confirm-deletion-form"}
    )
    assert form

    for key, value in {
        "delete": "1",
        "product_id": str(product.id),
        "unit_id": str(unit.id),
    }.items():
        input = form.find("input", {"name": key})
        assert value == input["value"]
    link = form["action"]
    assert link

    # follow confirmation link
    response = test_client.post(
        link,
        data={"delete": True, "product_id": product.id, "unit_id": unit.id},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert response.request.path == url_for("distribution.overview")

    # expect message for user that deletion was successfull
    messages = bs(response.data, "html.parser").find("div", class_="message")
    assert messages
    assert product.name in messages.text
    assert "gelöscht" in messages.text

    # deletion was successfull
    all_shares_of_product = Share.query.filter(
        Share.product_id == product.id, Share.unit_id == unit.id
    ).all()
    assert not all_shares_of_product