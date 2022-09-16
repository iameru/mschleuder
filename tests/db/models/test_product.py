import datetime

from ms.db import db_api
from ms.db.models import Product, Station, Unit, db


def test_adding_unit_product(test_app):

    # add units as they are needed
    kg = dict(shortname="kg", by_piece=False, longname="Kilogramm")
    st = dict(shortname="st", by_piece=True, longname="Stück")
    db_api.add(Unit, kg)
    db_api.add(Unit, st)

    # add products
    product_1 = dict(name="Kartoffel", unit_id=1, info="Lecker Kartoffel")
    db_api.add(Product, product_1)
    product_2 = dict(name="Kohlrabi", unit_id=2, info="Super Kohlrabi")
    db_api.add(Product, product_2)
    product_3 = dict(name="Mangold", unit_id=1, info="Mega Mangold")
    db_api.add(Product, product_3)

    # get products and check unit name
    products = Product.query.all()
    assert len(products) == 3
    for product in products:
        assert product.unit.longname

    # get one unit and check its products
    unit = Unit.query.filter_by(shortname="kg").first()
    p = Product.query.get(1)
    assert p in unit.products
    p = Product.query.get(2)
    assert p not in unit.products
    p = Product.query.get(3)
    assert p in unit.products


def test_unique_product_names():

    product = dict(name="Kartoffel", unit_id=1, info="Lecker Kartoffel")
    db_api.add(Product, product)
    db_api.add(Product, product)
    db_api.add(Product, product)
    db_api.add(Product, product)
    potatoes = Product.query.filter_by(name="Kartoffel").all()
    assert len(potatoes) == 1


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
