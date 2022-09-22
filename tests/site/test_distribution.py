from random import choice

from bs4 import BeautifulSoup as bs
from flask import request, url_for
from pytest import mark

from ms.db.models import Product, Station, Unit


def test_distribution_site_throws_404_if_no_product(test_client):

    response = test_client.get("/distribute/999999999")
    assert response.status_code == 404


def test_distribute_product_details_shown(test_client, product):

    # check  link and follow
    response = test_client.get("/products/")
    html = bs(response.data, "html.parser")
    product_row = html.find("tr", {"id": f"product-row-{product.id}"})
    url = product_row.find("td")["onclick"].split("'")[1]

    if len(product.units) > 1:
        unit = choice(product.units)
        url = url_for(
            "distribution.distribute",
            p_unit_shortname=unit.shortname,
            p_id=product.id,
        )

    distribute_page = test_client.get(url, follow_redirects=True)

    assert product_row

    # check distribute page for details
    body = bs(distribute_page.data, "html.parser").find("body")
    label = body.find("label", {"for": "dist-input-field"})
    input_field = body.find("input", {"id": "dist-input-field"})
    title = body.find("h2", {"id": "site-title"})

    assert product.name in title.text
    assert product.info in distribute_page.text
    if len(product.units) > 1:
        assert unit.longname in label.text
    else:
        for unit in product.units:
            assert unit.longname in label.text


def test_distribution_page_change_by_units(test_client):

    # get a product in Piece
    unit = Unit.query.filter_by(by_piece=True).first()
    product = choice(unit.products)
    url = url_for(
        "distribution.distribute",
        p_unit_shortname=unit.shortname,
        p_id=product.id,
    )
    # get dist_site for it
    body = bs(test_client.get(url).data, "html.parser").find("body")
    accuracy_field = body.find("p", {"id": "dist-accuracy-field"})
    rest_field = body.find("p", {"id": "dist-rest-field"})
    add_piece_field = body.find("button", {"class": "level-item button is-link"})
    # assert fields for the product in Pieces
    assert not accuracy_field
    assert rest_field
    assert add_piece_field

    # get a product in Weight
    unit = Unit.query.filter_by(by_piece=False).first()
    product = choice(unit.products)
    url = url_for(
        "distribution.distribute",
        p_unit_shortname=unit.shortname,
        p_id=product.id,
    )
    # get dist_site for it
    body = bs(test_client.get(url).data, "html.parser").find("body")
    accuracy_field = body.find("p", {"id": "dist-accuracy-field"})
    rest_field = body.find("p", {"id": "dist-rest-field"})
    add_piece_field = body.find("button", {"class": "level-item button is-link"})
    # assert fields for the product in Weight
    assert accuracy_field
    assert not rest_field
    assert not add_piece_field


def test_stations_in_dist(test_client, product, stations):

    unit = choice(product.units)
    url = url_for(
        "distribution.distribute",
        p_unit_shortname=unit.shortname,
        p_id=product.id,
    )
    response = test_client.get(url)
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


def test_stations_in_correct_order(test_client, product_distribution):

    ordered_stations = Station.query.order_by(Station.delivery_order).all()
    response = product_distribution
    html = bs(response.data, "html.parser")
    station_boxes = html.find_all("div", {"class": "station-box"})
    assert station_boxes

    # loop through both lists and check correct order
    for station, ordered_station in zip(station_boxes, ordered_stations):

        # get station id from ID string
        station_box_id = int(station["id"].split("-")[-1])

        assert station_box_id == ordered_station.id
