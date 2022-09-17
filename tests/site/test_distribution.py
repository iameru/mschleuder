from bs4 import BeautifulSoup as bs

from ms.db.models import Unit


def test_distribution_site_available(test_client, product):

    response = test_client.get(f"/products/distribute/{product.id}")
    assert response.status_code == 200
    assert product.name in response.text


def test_distribution_site_throws_404_if_no_product(test_client):

    response = test_client.get("/products/distribute/999999999")
    assert response.status_code == 404


def test_distribute_product_details_shown(test_client, product):

    # check  link and follow
    response = test_client.get("/products/")
    html = bs(response.data, "html.parser")
    product_row = html.find("tr", {"id": f"distribute-product-{product.id}"})
    url = product_row.find("td")["onclick"].split("'")[1]
    distribute_page = test_client.get(url)

    assert product_row
    assert distribute_page.status_code == 200

    # check distribute page for details
    body = bs(distribute_page.data, "html.parser").find("body")
    label = body.find("label", {"for": "dist-input-field"})
    input_field = body.find("input", {"id": "dist-input-field"})
    title = body.find("h2", {"id": "site-title"})

    assert product.name in title.text
    assert product.info in distribute_page.text
    assert product.unit.longname in label.text


from pytest import mark


@mark.skip
def test_existing_distribution_data_shown(test_client, product):

    assert False


def test_distribution_page_change_by_units(test_client):

    product = Unit.query.filter_by(by_piece=True).first()
    body = bs(
        test_client.get(f"/products/distribute/{product.id}").data, "html.parser"
    ).find("body")
    accuracy_field = body.find("p", {"id": "dist-accuracy-field"})
    rest_field = body.find("p", {"id": "dist-rest-field"})
    add_piece_field = body.find("button", {"class": "level-item button is-link"})
    assert not accuracy_field
    assert rest_field
    assert add_piece_field

    product = Unit.query.filter_by(by_piece=False).first()
    body = bs(
        test_client.get(f"/products/distribute/{product.id}").data, "html.parser"
    ).find("body")
    accuracy_field = body.find("p", {"id": "dist-accuracy-field"})
    rest_field = body.find("p", {"id": "dist-rest-field"})
    add_piece_field = body.find("button", {"class": "level-item button is-link"})
    assert accuracy_field
    assert not rest_field
    assert not add_piece_field


def test_stations_in_dist(test_client, product, stations):

    response = test_client.get(f"/products/distribute/{product.id}")
    body = bs(response.data, "html.parser").find("body")

    stations_element = body.find("div", {"id": "dist-stations-area"})

    assert stations_element

    for station in stations:

        station_element = stations_element.find(
            "div", {"id": f"dist-station-{station.id}"}
        )
        assert station.name in station_element.text
        assert str(station.members_full) in station_element.text
        assert str(station.members_half) in station_element.text
