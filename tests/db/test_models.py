import json
from random import choice

from pytest import mark

from ms.db.models import Product, Unit, db


def test_add_unit(test_app):

    assert True


def test_unit_product(test_app):

    kg = Unit(shortname="kg", by_piece=False, longname="Kilogramm")
    st = Unit(shortname="st", by_piece=True, longname="Stück")
    db.session.add(kg)
    db.session.add(st)
    product = Product(name="Kartoffel", unit_id=1)
    db.session.add(product)
    product = Product(name="Kohlrabi", unit_id=2)
    db.session.add(product)
    product = Product(name="Mangold", unit_id=1)
    db.session.add(product)

    db.session.commit()

    products = Product.query.all()
    units = Unit.query.all()

    for product in products:
        assert product.unit.longname


def test_consistency_of_db_model():

    potatoe = Product.query.filter_by(name="Kartoffel").first()
    mangold = Product.query.filter_by(name="Mangold").first()

    assert "Kartoffel" == potatoe.name
    assert "Mangold" == mangold.name
