import datetime

from ms.db import db_api
from ms.db.models import Product, Station, Unit, db


def test_adding_station(test_app):

    station_1 = Station(
        name="Station Superstar",
        delivery_order=2,
        info="Beste Station der Welt!",
        members_full=32,
        members_half=12,
    )
    station_2 = Station(
        name="Station3000",
        delivery_order=1,
        info="Megabeste Station der Superwelt!",
        members_full=12,
        members_half=13,
    )

    db.session.add(station_1)
    db.session.add(station_2)

    db.session.commit()

    station = Station.query.get(1)
    assert station == station_1
    station = Station.query.get(2)
    assert station == station_2


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
