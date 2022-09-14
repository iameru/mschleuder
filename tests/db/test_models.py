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


def _add_product_post(
    name: str = "Kohlrabi", unit_id: int = 2, info: str = None, test_client=None
):

    item = {"name": name, "info": info, "unit_id": unit_id}
    data = json.dumps(item)
    response = test_client.post(
        "/products/new", data=data, content_type="application/json"
    )
    return response


def test_add_product(test_client, product):

    response = _add_product_post(
        name=product["name"], unit_id=2, info=None, test_client=test_client
    )

    assert product["name"] in response.text
    assert response.status_code == 201


def test_added_products_in_database(test_client, products):

    response = _add_product_post(
        name="chickpeas", unit_id=1, info=None, test_client=test_client
    )
    response = _add_product_post(
        name="oranges", unit_id=2, info=None, test_client=test_client
    )

    chickpeas = Product.query.filter_by(name="chickpeas").first()
    oranges = Product.query.filter_by(name="oranges").first()

    assert "chickpeas" == chickpeas.name
    assert "oranges" == oranges.name


def test_consistency_of_db_model():

    chickpeas = Product.query.filter_by(name="chickpeas").first()
    oranges = Product.query.filter_by(name="oranges").first()

    assert "chickpeas" == chickpeas.name
    assert "oranges" == oranges.name
