import json
from random import choice

import pytest
from flask import url_for
from sqlalchemy import func

from ms.db.models import Distribution, Product, Share, Station, StationHistory, Unit, db


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


@pytest.fixture(autouse=True, scope="module")
def distribution(test_client):

    # create dist
    # setup
    dist = Distribution(in_progress=True)
    db.session.add(dist)
    db.session.commit()
    Station.archive_all(dist.id)

    # create products
    _save_product(test_client, 1, 50, [1, 3])
    _save_product(test_client, 2, 44, [1, 2, 3])
    _save_product(test_client, 3, 33, [1, 2, 3, 4])

    yield dist

    # teardown
    stations = StationHistory.query.filter_by(distribution_id=dist.id).all()
    [db.session.delete(share) for share in dist.shares]
    [db.session.delete(station) for station in stations]
    db.session.delete(dist)
    db.session.commit()


def test_query(distribution):

    assert len(distribution.stations) != 0

    dist = Distribution.current().id
    fields = db.session.query(
        func.sum(Share.sum_total).label("total_sum"),
        Product.name,
    )
    joins = fields.join(Product)

    groups = joins.group_by(Share.product_id)

    filters = groups.filter(
        Share.distribution_id == dist,
    )

    result = filters.all()

    # query = all_relevant_shares.filter(Share.distribution_id == distribution.id)

    products = (
        Product.query.join(Share).filter(Share.distribution_id == distribution.id).all()
    )
    # breakpoint()
    # # get all products distributed
    # # products = []
    # # for share in Share.query.filter_by(distribution_id=distribution.id).all():
    # #     products.append(Product.query.get(share.product_id))
    # # products = [p for p in set(products)]

    # # query = db.session.query(
    # #         Product, Share, StationHistory, Distribution
    # #     ).filter( Share.distribution_id == distribution.id,
    # #     ).filter( Share.stationhistory_id == StationHistory.id,
    # #     ).filter( Share.distribution_id == StationHistory.distribution_id,
    # #     ).filter( Share.product_id == Product.id,
    # #     ).filter( Share.distribution_id == Distribution.id,
    # # ).all()
    # # example = query[0]
    # query = db.session.query(
    #         Product
    #     ).join( Share
    #     ).join( StationHistory
    #     ).join( Distribution
    #     ).filter( Share.distribution_id == distribution.id,
    #     ).filter( Share.stationhistory_id == StationHistory.id,
    #     ).filter( Share.distribution_id == StationHistory.distribution_id,
    #     ).filter( Share.product_id == Product.id,
    #     ).filter( Share.distribution_id == Distribution.id,
    #     ).all()
    # example = query[0]
    # breakpoint()
