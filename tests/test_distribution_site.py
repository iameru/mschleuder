import json
from random import choice

from bs4 import BeautifulSoup as bs
from testmark import parse

products = json.loads(parse("dev.md")["products"])


def test_distribution_site_available(test_client):

    product = choice(products)
    response = test_client.get(f"/products/distribute/{product['id']}")
    assert response.status_code == 200
    assert product["name"].encode() in response.data


def test_distribute_product_link_working(test_client):

    product = choice(products)
    response = test_client.get("/products/")
    html = bs(response.data, "html.parser")

    product_row = html.find("tr", {"id": f"distribute-product-{product['id']}"})
    assert product_row

    url = product_row.find("td")["onclick"].split("'")[1]

    distribute_page = test_client.get(url)
    assert distribute_page.status_code == 200

    for item in product.values():
        assert str(item) in distribute_page.text
