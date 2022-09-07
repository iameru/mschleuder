from random import choice

from bs4 import BeautifulSoup as bs

from ms.dev import dev_data

products = dev_data("products")


def test_distribution_site_available(test_client):

    product = choice(products)
    response = test_client.get(f"/products/distribute/{product['id']}")
    assert response.status_code == 200
    assert product["name"].encode() in response.data


def test_distribute_product_details_shown(test_client):

    product = choice(products)
    response = test_client.get("/products/")
    html = bs(response.data, "html.parser")

    product_row = html.find("tr", {"id": f"distribute-product-{product['id']}"})
    assert product_row

    url = product_row.find("td")["onclick"].split("'")[1]

    distribute_page = test_client.get(url)
    assert distribute_page.status_code == 200

    assert product["recent_distribution"] in distribute_page.text
    assert product["unit"] in distribute_page.text
    assert product["name"] in distribute_page.text
    assert product["info"] in distribute_page.text


def test_existing_distribution_data_shown(test_client):

    in_distribution = dev_data("in-distribution")
    product = choice(in_distribution)

    response = test_client.get(f"/products/distribute/{product['id']}")

    assert response.status_code == 200

    body = bs(response.data, "html.parser").find("body")

    amount_string = f"{product['amount']} {product['unit']}"

    assert amount_string in body.text


def test_stations_in_dist(test_client):

    in_distribution = dev_data("in-distribution")
    product = choice(in_distribution)
    response = test_client.get(f"/products/distribute/{product['id']}")
    body = bs(response.data, "html.parser").find("body")

    stations = dev_data("stations-current")

    stations_element = body.find("div", {"id": "dist-stations-area"})

    assert stations_element

    for station in stations:

        station_element = stations_element.find(
            "div", {"id": f"dist-station-{station['id']}"}
        )
        assert station["name"] in station_element.text
        assert str(station["members_full"]) in station_element.text
        assert str(station["members_half"]) in station_element.text
