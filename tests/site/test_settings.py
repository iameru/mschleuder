from bs4 import BeautifulSoup as bs

from ms.db.models import Unit
from ms.dev import dev_data


def test_settings_on_page(test_client):

    response = test_client.get("/settings/")
    assert response
    assert "Einheit" in response.text
    assert "Logo" in response.text
    assert "SoLaWi Name" in response.text


def test_settings_set_on_page(test_client):

    settings = dev_data("test-settings")
    assert settings

    response = test_client.get("/settings/")
    body = bs(response.data, "html.parser").find("body")

    name_field = body.find("input", {"id": "input-csa-name"})
    assert settings["csa_name"] == name_field["value"]

    units_element = body.find("div", {"id": "settings-unit"})
    assert units_element

    for unit in settings["units"]:
        assert unit["name"] in units_element.text
        assert str(unit["id"]) in units_element.text
        assert str(unit["unit_id"]) in units_element.text

    for base_unit in settings["base_units"]:
        assert base_unit["description"] in body.text

    logo = body.find("img", {"alt": "CSA logo"})
    assert settings["logo"] == logo["src"]

    assert settings["packinglist_footer"] in body.text


def test_settings_being_applied_to_other_sites(test_client):

    settings = dev_data("test-settings")
    response = test_client.get("/products/")
    html = bs(response.data, "html.parser")

    title = html.find("title")
    assert settings["csa_name"] in title.text


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
