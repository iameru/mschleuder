import json
from random import choice
from typing import NamedTuple

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
    ## BROKEN HOTFIX
    ## BROKEN HOTFIX
    class QueryResult(NamedTuple):
        product_name: str
        product_id: int
        total_sum: int
        single_full_average: int
        single_half_average: int
        single_full: int

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
    result = filters.all()
    data = []
    for item in result:
        data.append(QueryResult(product_name=item[0], product_id=item[1],
                    total_sum=item[2], single_full_average=item[3],
                    single_half_average=item[4], single_full=item[5]))
    # data = [dict(item) for item in filters.all()]

    # assert some of the data from _save_product call above inside
    for idx, entry in enumerate(data):
        assert entry.product_id == idx + 1
        assert entry.single_full in [50, 44, 33]


def test_query_for_a_distribution_product_details(distribution):
    ## BROKEN HOTFIX
    class QueryResult(NamedTuple):
        product_name: str
        total_sum: int
        share: Share

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

    result = [QueryResult(product_name=item[0], total_sum=item[1], share=item[2])
              for item
              in filters.all()]

    # data = [dict(item) for item in result]
    from pprint import pprint


def test_query_for_recent_distributions_of_product(distribution):

    distribution.in_progress = False
    # CHOSE PRODUCT (variable)
    product = Product.query.get(1)

    # CHOSE HOW MANY DISTS IN THE PAST (variable)
    how_many_distributions = 2
    FAKE_VALUE = False  # in production this should be True was too much refactoring of tests for me now
    distributions = (
        db.session.query(Distribution.id)
        .filter(Distribution.in_progress == False, Distribution.finalized == FAKE_VALUE)
        .order_by(Distribution.id.desc())
    ).all()[:how_many_distributions]
    distribution_ids = [dist[0] for dist in distributions]

    # CHOSE STATION (variable)
    station = Station.query.get(1)
    station_history_ids = [station.id for station in station.history]

    # DO QUERY DATA
    fields = db.session.query(
        func.sum(Share.single_full).label("single_full"),
        func.sum(Share.single_half).label("single_half"),
    )
    joins = fields
    groups = joins
    filters = groups.filter(
        Share.distribution_id.in_(distribution_ids),
        Share.product_id == product.id,
        Share.stationhistory_id.in_(station_history_ids),
    )
    query_result = filters.one()

    # this would calculate the AVERAGE
    result = [value / len(distributions) for value in query_result if value]

    # teardown
    distribution.in_progress = True

    ### STATIONS ALL
    stations = Station.query.all()
