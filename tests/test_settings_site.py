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
    html = bs(response.data, "html.parser")

    body = html.find("body")
    assert settings["csa_name"] in body.text

    units_element = html.find("div", {"id": "settings-unit"})
    assert units_element

    for unit in settings["units"]:
        assert unit["name"] in units_element.text
        assert str(unit["id"]) in units_element.text
        assert str(unit["unit_id"]) in units_element.text

    for base_unit in settings["base-units"]:
        assert base_unit["description"] in html.text

    logo = html.find("image", {"src": settings["logo"]})
    assert logo

    assert settings["packinglist_footer"] in response.text


def test_settings_being_applied_to_other_sites(test_client):

    settings = dev_data("test-settings")
    response = test_client.get("/products/")
    html = bs(response.data, "html.parser")

    title = html.find("title")
    assert settings["csa_name"] in title.text
