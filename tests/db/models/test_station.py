from datetime import datetime

from pytest import mark

from ms.db import db_api
from ms.db.models import Distribution, Station, StationHistory, db


def test_adding_station(test_app):

    station_1 = dict(
        name="Station Superstar",
        delivery_order=2,
        info="Beste Station der Welt!",
        members_full=32,
        members_half=12,
    )
    station_2 = dict(
        name="Station3000",
        delivery_order=1,
        info="Megabeste Station der Superwelt!",
        members_full=12,
        members_half=13,
    )
    db_api.add(Station, station_1)
    db_api.add(Station, station_2)

    station = Station.query.filter_by(**station_1).first()
    assert station
    assert station.id == 1
    station = Station.query.filter_by(**station_2).first()
    assert station
    assert station.id == 2


def test_station_has_total_member_sum(test_app):

    for _ in range(3):
        # Check current value
        station = Station.query.get(2)
        full = station.members_full
        half = station.members_half
        total = full + half
        assert total == station.members_total
        # edit both value and check new value
        full += 5
        half += 1
        total = full + half
        station.members_full = full
        station.members_half = half
        db.session.add(station)
        db.session.commit()
        assert total == station.members_total
        # edit one value and check new value
        full += 2
        total = full + half
        station.members_full = full
        station.members_half = half
        db.session.add(station)
        db.session.commit()
        assert total == station.members_total


def test_stations_softdelete(test_app):

    # we add a station and delete it
    station = Station(
        name="to be deleted", delivery_order=123, members_full=3, members_half=2
    )
    db.session.add(station)
    db.session.commit()

    assert station.deleted_at == None

    station.delete()
    db.session.commit()

    # roughly deleted now timestamp
    assert station.deleted_at
    assert station.deleted_at.replace(microsecond=0) == datetime.now().replace(
        microsecond=0
    )


def test_unique_station_names():

    station = dict(
        name="The Low Hanging Fruits",
        delivery_order=1,
        info="fun",
        members_full=2,
        members_half=2,
    )
    db_api.add(Station, station)
    db_api.add(Station, station)
    db_api.add(Station, station)
    db_api.add(Station, station)
    station = Station.query.filter_by(name="The Low Hanging Fruits").all()
    assert len(station) == 1


def test_edit_station_change_and_timestamp(test_app):

    # get station
    station = Station.query.get(1)
    members_full = station.members_full
    assert station.name == "Station Superstar"
    assert station.created
    assert not station.updated

    # make changes
    station.name = "Superstation Megagood NEW"
    station.members_full = members_full + 5
    db.session.commit()

    # expect changes
    station_new = Station.query.get(1)
    assert station_new.name != "Station Superstar"
    assert station_new.members_full != members_full

    # expect updated time to be changed
    assert station.updated


def test_archive_of_stations(test_app, station):

    # this shall archive into a table StationHistory
    # needed is a Dist key
    dist_id = Distribution.current().id
    station.archive(dist_id)

    # Find archived Item in History
    result = StationHistory.query.filter_by(
        name=station.name, members_total=station.members_total
    ).all()
    assert result
    assert len(result) == 1

    # Do again
    station.archive(dist_id)
    station.archive(dist_id)

    # Find three Items in History
    result = StationHistory.query.filter_by(distribution_id=dist_id).all()
    assert result
    assert len(result) == 3

    # find these in station itself.
    assert station.history == result
