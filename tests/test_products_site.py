import json
from random import choice

from testmark import parse

products = json.loads(parse("dev.md")["products"])


def test_product_on_site(test_client):

    product = choice(products)
    response = test_client.get("/products/")

    assert product["name"].encode() in response.data


def test_all_products_on_site(test_client):

    response = test_client.get("/products/")

    for product in products:
        assert product["name"].encode() in response.data
