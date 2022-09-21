from random import choice

from bs4 import BeautifulSoup as bs
from flask import request, url_for
from pytest import mark

from ms.db.models import Product, Unit


@mark.skip
def test_distribution_site_available(test_client, product):

    response = test_client.get(f"/products/distribute/{product.id}")
    assert response.status_code == 200
    assert product.name in response.text


@mark.skip
def test_distribution_site_throws_404_if_no_product(test_client):

    response = test_client.get("/products/distribute/999999999")
    assert response.status_code == 404


@mark.skip
def test_distribute_product_details_shown(test_client, product):

    # check  link and follow
    response = test_client.get("/products/")
    html = bs(response.data, "html.parser")
    product_row = html.find("tr", {"id": f"product-row-{product.id}"})
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
    for unit in product.units:
        assert unit.longname in label.text


@mark.skip
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


@mark.skip
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


def test_redirect_for_products_without_multiple_units(test_app, test_client):

    product = Product.query.filter_by(name="Mangold").first()
    assert len(product.units) == 1

    # go to distribution
    response = test_client.get(
        url_for("distribution.product", p_id=product.id), follow_redirects=True
    )

    # target Url we are supposed to be redirected to
    target_url = url_for(
        "distribution.distribute",
        p_unit_shortname=product.units[0].shortname,
        p_id=product.id,
    )

    assert response.status_code == 200
    assert response.request.path == target_url


def test_redirect_for_products_with_multiple_units(test_client):

    product = Product.query.filter_by(name="Rote Beete").first()
    assert len(product.units) == 2

    # go to distribution
    response = test_client.get(
        url_for("distribution.product", p_id=product.id), follow_redirects=True
    )

    # not be redirected
    assert response.status_code == 200
    assert response.request.path == url_for("distribution.product", p_id=product.id)

    # but be asked to choose a unit for the product
    html = bs(response.data, "html.parser")
    for unit in product.units:
        button = html.find("button", {"id": f"distribute-unit-{unit.id}"})
        assert button

    # choose unit and check url for correct redirect
    unit = choice(product.units)
    button = html.find("button", {"id": f"distribute-unit-{unit.id}"})
    target_url = url_for(
        "distribution.distribute",
        p_unit_shortname=unit.shortname,
        p_id=product.id,
    )

    assert button.parent["href"] == target_url
