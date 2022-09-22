from sqlalchemy.exc import IntegrityError

from ms.db import db_api
from ms.db.models import Product, Unit, db


def test_adding_unit_product(test_app):

    # add units as they are needed
    kg = dict(shortname="kg", by_piece=False, longname="Kilogramm")
    st = dict(shortname="st", by_piece=True, longname="Stück")
    db_api.add(Unit, kg)
    db_api.add(Unit, st)
    kg = Unit.query.filter_by(**kg).first()
    st = Unit.query.filter_by(**st).first()

    # add products
    product_1 = dict(name="Kartoffel", units=[kg], info="Lecker Kartoffel")
    product_2 = dict(name="Kohlrabi", units=[st], info="Super Kohlrabi")
    product_3 = dict(name="Mangold", units=[kg], info="Mega Mangold")
    for product in [product_1, product_2, product_3]:
        pr = Product(**product)
        db.session.add(pr)

    db.session.commit()

    # get products and check unit name
    products = Product.query.all()
    assert len(products) == 3
    for product in products:
        assert len(product.units) == 1

    # get one unit and check its products
    unit = Unit.query.filter_by(shortname="kg").first()
    p = Product.query.get(1)
    assert p in unit.products
    p = Product.query.get(2)
    assert p not in unit.products
    p = Product.query.get(3)
    assert p in unit.products


def test_unique_product_names():

    kg = Unit.query.filter_by(shortname="kg").first()
    product = dict(name="Kartoffel", units=[kg], info="Lecker Kartoffel")
    try:
        db.session.add(Product(**product))
        db.session.add(Product(**product))
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

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


def test_product_multiple_units():

    unit_1 = Unit.query.get(1)
    unit_2 = Unit.query.get(2)
    product_data = dict(name="Rote Beete", units=[unit_1, unit_2], info="choose wisely")
    product = Product(**product_data)
    db.session.add(product)

    product = Product.query.filter_by(name="Rote Beete").first()
    assert product
    assert unit_1 in product.units
    assert unit_2 in product.units
