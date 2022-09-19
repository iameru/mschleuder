from bs4 import BeautifulSoup as bs

from ms.db.models import Organisation, Unit


def test_settings_on_page(test_client):

    response = test_client.get("/settings/")
    assert response.status_code == 200
    body = bs(response.data, "html.parser").find("body")

    # find entries

    assert body.find("div", {"id": "units-div"})
    assert body.find("input", {"id": "name"})
    assert body.find("input", {"id": "display_name"})
    assert body.find("input", {"id": "info"})
    assert body.find("input", {"id": "header"})
    assert body.find("input", {"id": "footer"})


def test_settings_visible_in_form(test_client):

    organisation = Organisation.query.get(1)
    assert organisation

    response = test_client.get("/settings/")
    body = bs(response.data, "html.parser").find("body")

    name = body.find("input", {"id": "name"})
    assert organisation.name == name["value"]
    display_name = body.find("input", {"id": "display_name"})
    assert organisation.display_name == display_name["value"]
    info = body.find("input", {"id": "info"})
    assert organisation.info == info["value"]
    header = body.find("input", {"id": "header"})
    assert organisation.header == header["value"]
    footer = body.find("input", {"id": "footer"})
    assert organisation.footer == footer["value"]


def test_settings_being_applied_to_other_sites(test_client):

    organisation = Organisation.query.get(1)

    response = test_client.get("/")
    html = bs(response.data, "html.parser")
    title = html.find("title")
    assert organisation.name in title.text


def test_add_product_modal(test_client, csrf):

    response = test_client.get("/settings/units/new")
    doc = bs(response.data, "html.parser")
    assert doc.find("input", {"id": "longname"})
    assert doc.find("input", {"id": "shortname"})
    assert doc.find("select", {"id": "by_piece"})
    assert csrf(response)


def test_add_unit(test_client, csrf):

    item = dict(shortname="kSt", longname="Kiste", by_piece=True)
    # check unit not in table
    response = test_client.get("/settings/")
    table = bs(response.data, "html.parser").find("table", {"id": "all-units-table"})
    assert item["longname"] not in table.text

    # find button
    new_unit_button = bs(response.data, "html.parser").find(
        "button", {"id": "new-unit-button"}
    )
    assert new_unit_button
    assert new_unit_button["hx-get"] == "/settings/units/new"

    # open modal and create product
    response = test_client.get(new_unit_button["hx-get"])
    item["csrf_token"] = csrf(response)
    response = test_client.post("/settings/units/new", data=item, follow_redirects=True)
    del item["csrf_token"]
    assert response.status_code == 200

    # check if unit is in table now
    unit = Unit.query.filter_by(**item).first()
    assert unit
    table = bs(response.data, "html.parser").find("table", {"id": "all-units-table"})
    row = table.find("tr", {"id": f"unit-{unit.id}"})
    assert item["longname"] in row.text  # by_piece=True

    #  the same stuff for the item for weight
    item = dict(shortname="mg", longname="Miligramm", by_piece=False)
    # open modal and create product
    response = test_client.get(new_unit_button["hx-get"])
    item["csrf_token"] = csrf(response)
    response = test_client.post("/settings/units/new", data=item, follow_redirects=True)
    del item["csrf_token"]
    assert response.status_code == 200

    # check if unit is in table now
    unit = Unit.query.filter_by(**item).first()
    assert unit
    table = bs(response.data, "html.parser").find("table", {"id": "all-units-table"})
    row = table.find("tr", {"id": f"unit-{unit.id}"})
    assert item["longname"] in row.text  # by_piece=False
