import json

from bs4 import BeautifulSoup as bs

from ms.db.models import Product, Unit


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


def test_add_product_modal(test_client, csrf):

    response = test_client.get("/products/new")
    doc = bs(response.data, "html.parser")
    assert doc.find("input", {"id": "name"})
    assert doc.find("input", {"id": "info"})
    assert doc.find("select", {"id": "unit_id"})
    assert csrf(response)

    units = Unit.query.all()
    for unit in units:
        assert unit.longname in response.text


def test_add_product(test_client, csrf):

    item = dict(name="Tomate", info="yummi", unit_id=2)

    # check product not in table
    response = test_client.get("/products/")
    table = bs(response.data, "html.parser").find("table", {"id": "all-products-table"})
    assert item["name"] not in table.text

    # find button
    new_product_button = bs(response.data, "html.parser").find(
        "button", {"id": "new-product-button"}
    )
    assert new_product_button
    assert new_product_button["hx-get"] == "/products/new"

    # create product
    response = test_client.get(new_product_button["hx-get"])
    item["csrf_token"] = csrf(response)
    response = test_client.post("/products/new", data=item, follow_redirects=True)
    assert response.status_code == 200

    # check if product is in table now
    product = Product.query.filter_by(name=item["name"]).first()
    assert product
    table = bs(response.data, "html.parser").find("table", {"id": "all-products-table"})
    row = table.find("tr", {"id": f"distribute-product-{product.id}"})
    unit = Unit.query.get(item["unit_id"])

    assert item["name"] in row.text
    assert item["info"] in row.text
    assert unit.shortname in row.text
