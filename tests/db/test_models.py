import json
from random import choice

from ms.db.models import Product


def test_add_product(test_client, product):

    item = {"name": product["name"], "by_piece": product["by_piece"]}
    data = json.dumps(item)
    response = test_client.post(
        "/products/new", data=data, content_type="application/json"
    )

    assert item["name"] in response.text
    assert response.status_code == 201


def test_added_products_in_database(test_client, products):

    item = {"name": "chickpeas", "by_piece": True}
    data = json.dumps(item)
    test_client.post("/products/new", data=data, content_type="application/json")
    item = {"name": "oranges", "by_piece": False}
    data = json.dumps(item)
    test_client.post("/products/new", data=data, content_type="application/json")

    chickpeas = Product.query.filter_by(name="chickpeas").first()
    oranges = Product.query.filter_by(name="oranges").first()

    assert "chickpeas" == chickpeas.name
    assert "oranges" == oranges.name


def test_consistency_of_db_model():

    chickpeas = Product.query.filter_by(name="chickpeas").first()
    oranges = Product.query.filter_by(name="oranges").first()

    assert "chickpeas" == chickpeas.name
    assert "oranges" == oranges.name
