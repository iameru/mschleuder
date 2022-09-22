from bs4 import BeautifulSoup as bs

from ms.db.models import Product, Unit


def test_product_on_site(test_client, product):

    response = test_client.get("/products/")

    assert product.name in response.text


def test_all_products_on_site(test_client, products):

    response = test_client.get("/products/")

    for product in products:
        assert product.name in response.text


def test_htmx_detail_product(test_client, product):

    response = test_client.get("/products/")
    html = bs(response.data, "html.parser")

    product_html = html.find("td", {"id": f"product-edit-view-{product.id}"})

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
    assert doc.find("select", {"id": "units"})
    assert csrf(response)

    units = Unit.query.all()
    for unit in units:
        assert unit.longname in response.text


def test_add_product_with_two_units(test_client, csrf):

    units = [Unit.query.get(1), Unit.query.get(2)]
    item = dict(name="Tomate", info="yummi", units=[unit.id for unit in units])

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
    row = table.find("tr", {"id": f"product-row-{product.id}"})

    assert item["name"] in row.text
    assert item["info"] in row.text
    for unit in units:
        assert unit.shortname in row.text


def test_edit_product(test_client, csrf, product):

    # product to edit
    data = product.__dict__
    old_info = data["info"]
    data = data.copy()

    # go on overview site and click edit button
    response = test_client.get("/products/")
    edit_box = bs(response.data, "html.parser").find(
        "td", {"id": f"product-edit-view-{product.id}"}
    )
    assert edit_box
    response = test_client.get(edit_box["hx-get"])

    # find form, fill details and send
    form = bs(response.data, "html.parser").find("form", {"id": "product-edit-form"})
    assert form
    data["csrf_token"] = csrf(response)
    data["info"] = "Now even more tasty"
    response = test_client.post(form["action"], data=data, follow_redirects=True)
    assert response.status_code == 200

    # find new values on site
    response = test_client.get("/products/")
    product_row = bs(response.data, "html.parser").find(
        "tr", {"id": f"product-row-{product.id}"}
    )
    assert product_row
    assert data["name"] in product_row.text
    assert data["info"] in product_row.text
    assert old_info not in product_row.text
