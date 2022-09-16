import datetime

from ms.db import db_api
from ms.db.models import Product, Station, Unit, db


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
    assert station.name == "Station Superstar"
    first_update_time = station.updated
    members_full = station.members_full

    # make changes
    station.name = "Superstation Megagood NEW"
    station.members_full = 35
    db.session.commit()

    # expect changes
    station_new = Station.query.get(1)
    assert station_new.name != "Station Superstar"
    assert station_new.members_full != members_full

    # expect updated time to be changed
    assert station_new.updated != first_update_time
