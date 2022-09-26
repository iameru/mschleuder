import json
from random import choice, randint

import pytest
from flask import url_for

from ms.db.models import Distribution, Product, Share, Station, StationHistory, db


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
        single_total = single_full + single_half

        # the whole station gets
        sum_full = single_full * station.members_full
        sum_half = single_half * station.members_half
        sum_total = sum_full + sum_half

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
            single_total=single_total,
            sum_full=sum_full,
            sum_half=sum_half,
            sum_total=sum_total,
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
