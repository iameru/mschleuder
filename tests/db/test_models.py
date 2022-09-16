import datetime

from pytest import mark

from ms.db import db_api
from ms.db.models import Product, Station, Unit, db


def test_add_unit(test_app):

    assert True


def test_adding_unit_product(test_app):

    kg = Unit(shortname="kg", by_piece=False, longname="Kilogramm")
    st = Unit(shortname="st", by_piece=True, longname="Stück")
    db.session.add(kg)
    db.session.add(st)
    product_1 = Product(name="Kartoffel", unit_id=1, info="Lecker Kartoffel")
    db.session.add(product_1)
    product_2 = Product(name="Kohlrabi", unit_id=2, info="Super Kohlrabi")
    db.session.add(product_2)
    product_3 = Product(name="Mangold", unit_id=1, info="Mega Mangold")
    db.session.add(product_3)

    db.session.commit()

    products = Product.query.all()

    for product in products:
        assert product.unit.longname

    unit = Unit.query.filter_by(shortname="kg").first()

    assert product_1 in unit.products
    assert product_2 not in unit.products
    assert product_3 in unit.products


def test_unique_product_names():

    product = dict(name="Kartoffel", unit_id=1, info="Lecker Kartoffel")
    db_api.add(Product, product)
    db_api.add(Product, product)
    db_api.add(Product, product)
    db_api.add(Product, product)
    potatoes = Product.query.filter_by(name="Kartoffel").all()
    assert len(potatoes) == 1


def test_consistency_of_db_model():

    potatoe = Product.query.filter_by(name="Kartoffel").first()
    mangold = Product.query.filter_by(name="Mangold").first()

    assert "Kartoffel" == potatoe.name
    assert "Mangold" == mangold.name


def test_edit_products_change_and_timestamp(test_app):

    # get product
    product = Product.query.get(1)
    info = product.info
    assert product.name == "Kartoffel"
    assert product.created
    assert not product.updated

    # make changes
    product.name = "Krombeere"
    product.info = "Schmackhaft"
    db.session.commit()

    # expect changes
    product = Product.query.get(1)
    assert product.name != "Kartoffel"
    assert product.info != info

    # expect updated time to be changed
    assert product.updated


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
