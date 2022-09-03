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

    recent_products = sorted(products, key=lambda item: item["recent_distribution"])
    recent_products.reverse()
    top_ten = recent_products[:10]

    html = bs(response.data, "html.parser")

    recent_distribution = html.find("div", {"id": "recent-distribution"})
    assert recent_distribution

    for product in top_ten:

        html_product = recent_distribution.find(
            "div", {"id": f"product{product['id']}"}
        )

        assert product["name"] in html_product.string


def test_htmx_detail_product(test_client):

    product = choice(products)
    response = test_client.get("/products/")

    html = bs(response.data, "html.parser")
    product_html = html.find("tr", {"id": f"tr-product-{product['id']}"})

    url = product_html["hx-get"]

    assert str(product["id"]) == url.split("/")[-1]

    url_res = test_client.get(url)

    assert product["name"] in url_res.text
