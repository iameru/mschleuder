import json
from random import choice

from bs4 import BeautifulSoup as bs
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


def test_recently_used_products(test_client):

    response = test_client.get("/products/")

    sorted_products = sorted(products, key=lambda item: item["recent_distribution"])
    top_ten = sorted_products[:10]

    html = bs(response.data, "html.parser")

    recent_distribution = html.find("div", {"id": "recent-distribution"})
    assert recent_distribution

    for product in top_ten:

        assert product["name"] in recent_distribution.string
