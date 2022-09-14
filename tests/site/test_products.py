import json

from bs4 import BeautifulSoup as bs


def test_product_on_site(test_client, product):

    response = test_client.get("/products/")

    assert product.name in response.text


def test_all_products_on_site(test_client, products):

    response = test_client.get("/products/")

    for product in products:
        assert product.name in response.text


def test_recently_used_products(test_client, products):

    response = test_client.get("/products/")

    distributed_products = [
        product for product in products if product.last_distribution
    ]
    recent_products = sorted(
        distributed_products, key=lambda item: item.last_distribution
    )
    recent_products.reverse()
    top_ten = recent_products[:10]

    html = bs(response.data, "html.parser")

    recent_distribution = html.find("div", {"id": "recent-distribution"})
    assert recent_distribution

    for product in top_ten:

        html_product = recent_distribution.find(
            "div", {"id": f"product{product['id']}"}
        )

        assert product.name in html_product.string


def test_htmx_detail_product(test_client, product):

    response = test_client.get("/products/")
    html = bs(response.data, "html.parser")

    product_html = html.find("td", {"id": f"product-detail-view-{product.id}"})

    url = product_html["hx-get"]
    assert str(product.id) == url.split("/")[-1]

    modal = test_client.get(url)
    assert product.name in modal.text


def test_new_product_modal_shown(test_client):

    response = test_client.get("/products/")

    html = bs(response.data, "html.parser")
    link = html.find("button", {"hx-get": "/products/new"})
    assert link

    modal = test_client.get(link["hx-get"])
    assert modal.status_code == 200
    assert "Neues Produkt" in modal.text


def test_add_product(test_client, product):

    item = dict(name=product.name, unit_id=2, info=None)

    data = json.dumps(item)
    response = test_client.post(
        "/products/new", data=data, content_type="application/json"
    )

    assert product.name in response.text
    assert response.status_code == 201
