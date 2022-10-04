import json
from random import choice

import pytest
from flask import url_for
from sqlalchemy import func

from ms.db.models import Distribution, Product, Share, Station, StationHistory, Unit, db

## These are/were explorative tests to get a hang and insights on how queries are formed.
# might be deleted, dont take this too seriously


def _save_product(test_client, product_id, single_full, stations):

    product = Product.query.get(product_id)
    unit = choice(product.units)
    dist = Distribution.current()

    post_data = []
    for station_id in stations:
        station = StationHistory.query.get(station_id)

        single_half = int(single_full / 2)
        single_total = single_full + single_half
        sum_full = single_full * station.members_full
        sum_half = single_half * station.members_half
        sum_total = sum_full + sum_half
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


@pytest.fixture(autouse=True, scope="module")
def distribution(test_client):

    # create dist
    # setup
    dist = Distribution(in_progress=True)
    db.session.add(dist)
    db.session.commit()
    Station.archive_all(dist.id)

    # create products
    _save_product(test_client, 1, 50, [4, 6])
    _save_product(test_client, 2, 44, [4, 5, 6])
    _save_product(test_client, 3, 33, [4, 5])

    yield dist

    # teardown
    stations = StationHistory.query.filter_by(distribution_id=dist.id).all()
    [db.session.delete(share) for share in dist.shares]
    [db.session.delete(station) for station in stations]
    db.session.delete(dist)
    db.session.commit()


def test_query_current_distribution_sum_and_averages_for_products(distribution):

    # build a query by choosing the fields we want
    fields = db.session.query(
        Product.name.label("product_name"),
        Product.id.label("product_id"),
        func.sum(Share.sum_total).label("total_sum"),
        func.avg(Share.single_full).label("single_full_average"),
        func.avg(Share.single_half).label("single_half_average"),
        Share.single_full.label("single_full"),
    )
    # the tables to join for it
    joins = fields.join(Product)
    # the grouping
    groups = joins.group_by(Share.product_id)
    # and some filters
    filters = groups.filter(
        Share.distribution_id == distribution.id,
    )
    data = [dict(item) for item in filters.all()]

    # assert some of the data from _save_product call above inside
    for idx, entry in enumerate(data):
        assert entry.get("product_id") == idx + 1
        assert entry.get("single_full") in [50, 44, 33]


def test_query_for_a_distribution_product_details(distribution):

    # variables
    product_id = 1
    distribution_id = distribution.id

    # test for all stations
    fields = db.session.query(
        Product.name.label("product_name"),
        func.sum(Share.sum_total).label("total_sum"),
        Share,
    )

    joins = fields.join(Product).join(StationHistory)
    groups = joins.group_by(Share.stationhistory_id, StationHistory.id)
    filters = groups.filter(
        Share.distribution_id == distribution_id,
        Share.product_id == product_id,
    )

    result = filters.all()

    data = [dict(item) for item in result]
    from pprint import pprint
