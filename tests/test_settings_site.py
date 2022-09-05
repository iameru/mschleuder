from bs4 import BeautifulSoup as bs

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
