from random import choice

from ms.db.models import Distribution, Product, Share, Station, StationHistory, db


def test_creation_and_linkage_of_Share_model(in_distribution):

    # a model for each station, product, distribution and unit

    # We are in a distribution
    dist = Distribution.current()
    assert dist.in_progress == True

    # We want to distribute a product
    product = choice(Product.query.all())
    unit = choice(product.units)
    # To a station
    station = choice(dist.stations)

    keys = dict(
        product_id=product.id,
        stationhistory_id=station.id,
        distribution_id=dist.id,
        unit_id=unit.id,
    )

    # we have values for what a single member gets
    # and values for the total sum of the station
    sum_full = 8 * station.members_full
    sum_half = 4 * station.members_half
    sum_total = sum_full + sum_half
    data = dict(
        single_full=8,
        single_half=4,
        single_total=12,
        sum_full=sum_full,
        sum_half=sum_half,
        sum_total=sum_total,
    )

    data.update(keys)

    share = Share(**data)
    db.session.add(share)
    db.session.commit()

    # now it should have been saved
    share = Share.query.filter_by(**data).first()
    assert share
    assert share.id
    assert share.created
    assert share.product_id == product.id
    assert share.stationhistory_id == station.id
    assert share.distribution_id == dist.id
    assert share.unit_id == unit.id
    assert share.single_full == 8
    assert share.single_half == 4
    assert share.single_total == 12
    assert share.sum_full == sum_full
    assert share.sum_half == sum_half
    assert share.sum_total == sum_total

    # also the other models should have references
    assert share.product == product
    assert share.unit == unit
    assert share.stationhistory == station
    assert share.dist == dist

    # also the distribution should have stations referenced
    assert station in dist.stations
