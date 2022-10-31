import datetime
from random import choice

from bs4 import BeautifulSoup as bs
from flask import url_for
from pytest import mark

from conftest import in_distribution
from ms.db.models import Distribution, Product, Share, Station, StationHistory, Unit, db


def test_invitation_to_start_distribution(test_client, product_distribution):

    assert Distribution.current().in_progress is False
    response = test_client.get("/")
    button = bs(response.data, "html.parser").find(
        "li", {"id": "distribution-overview-button"}
    )
    assert button
    assert button.text == "Verteilung starten"


def test_redirect_if_distribution_not_started(test_client):

    # check a link of distribution blueprint
    response = test_client.get("/distribute/999999999")
    # it is redirected to start distribution
    assert response.request.path != url_for("distribution.trigger")
    assert response.status_code == 302

    response = test_client.get("/distribute/999999999", follow_redirects=True)
    # it is redirected to start distribution
    assert response.request.path == url_for("distribution.trigger")
    assert response.status_code == 200


def test_start_distribution_view(test_client):

    response = test_client.get(url_for("distribution.trigger"))

    form = bs(response.data, "html.parser").find(
        "form", {"id": "form-start-distribution"}
    )
    start_button = form.find("button", {"id": "start-distribution"})
    continue_button = bs(response.data, "html.parser").find(
        "button", {"id": "continue"}
    )

    assert start_button
    assert start_button.text == "Starten"
    assert start_button["name"] == "distribution"
    assert start_button["type"] == "submit"
    assert start_button["value"] == "start"

    assert continue_button
    assert continue_button.parent["href"] == url_for("stations.stations_view")
    assert continue_button.text == "Zurück"


def test_starting_a_distribution(test_client):

    # when starting a distribution
    # a trigger shall fire and all stations shall be
    # locked in use for the distribution

    # trigger distribution
    assert Distribution.current().in_progress is False

    data = {"distribution": "start"}

    response = test_client.post(
        url_for("distribution.trigger"), data=data, follow_redirects=True
    )

    # find the trigger successfull
    assert response.status_code == 200
    dist = Distribution.current()
    assert dist.in_progress is True
    assert response.request.path == url_for("products.products_view")

    # find the stations archived
    stations = Station.query.all()
    stations_archived = StationHistory.query.filter_by(distribution_id=dist.id).all()

    assert dist.stations
    assert dist.stations == stations_archived
    assert len(stations) == len(stations_archived)

    for s, sa in zip(stations, stations_archived):
        assert s.name == sa.name
        assert s.members_full == sa.members_full
        assert s.members_half == sa.members_half
        assert s.members_total == sa.members_total


def test_404_start_when_dist_already_started(test_client, in_distribution):

    assert Distribution.current().in_progress
    data = {"distribution": "start"}

    response = test_client.post(
        url_for("distribution.trigger"), data=data, follow_redirects=True
    )

    assert response.status_code == 404


def test_404_stop_when_dist_already_stopped(test_client, not_in_distribution):

    assert not Distribution.current().in_progress
    data = {"distribution": "stop"}

    response = test_client.post(
        url_for("distribution.trigger"), data=data, follow_redirects=True
    )

    assert response.status_code == 404


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
    assert input_field
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
    add_piece_field = body.find("button", class_="button")
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
    add_piece_field = body.find("button", class_="level-item button is-link")
    # assert fields for the product in Weight
    assert accuracy_field
    assert not rest_field
    assert not add_piece_field


def test_stations_in_dist(test_client, product):

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

    dist = Distribution.current()
    stations = StationHistory.query.filter(
        StationHistory.distribution_id == dist.id
    ).all()

    for station in stations:

        station_element = stations_element.find(
            "div", {"id": f"dist-station-{station.id}"}
        )
        assert station.name in station_element.text
        if unit.by_piece:
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

    dist = Distribution.current()
    ordered_stations = (
        StationHistory.query.filter(StationHistory.distribution_id == dist.id)
        .order_by(StationHistory.delivery_order)
        .all()
    )
    response = product_distribution
    html = bs(response.data, "html.parser")
    station_boxes = html.find_all("div", class_="station-box")
    assert station_boxes

    # loop through both lists and check correct order
    for station, ordered_station in zip(station_boxes, ordered_stations):

        # get station id from ID string
        station_box_id = int(station["id"].split("-")[-1])

        assert station_box_id == ordered_station.id


def test_stations_can_be_opt_out_visually(test_client, product_distribution):

    # not well tested - JS
    response = product_distribution
    html = bs(response.data, "html.parser")

    station_boxes = html.find_all("div", class_="station-box")
    for box in station_boxes:

        opt_out_field = box.find("div", class_="station-box-opt-out")
        assert opt_out_field
        assert opt_out_field["onclick"]
        assert opt_out_field["onclick"] == "trigger_station_opt_out(this);"


@mark.skip
def test_recent_distributions_view_in_distribution(test_client, product):

    # TEST NOT DONE but feature included..

    # setup
    # in a distribution view
    unit = choice(product.units)
    url = url_for(
        "distribution.distribute",
        p_unit_shortname=unit.shortname,
        p_id=product.id,
    )
    response = test_client.get(url, follow_redirects=True)
    html = bs(response.data, "html.parser")

    # we will find a button inviting us for details on recent dists of this product
    # this will be shown in a modal for now
    recent_dist_button = html.find("a", {"id": "recent-distributions"})
    assert recent_dist_button
    url = recent_dist_button["hx-get"]
    assert url
    assert url == url_for(
        "history.show_recent_distribution", product_id=product.id, unit_id=unit.id
    )

    # get the modal
    response = test_client.get(url)
    assert response.status_code == 200
    modal = bs(response.data, "html.parser")

    assert False


def test_stop_distribution(test_client):

    # setup
    dist = Distribution.current()
    stations_archived = dist.stations
    assert dist.in_progress is True

    # there shall be a button
    response = test_client.get(url_for("distribution.overview"))
    stop_modal_button = bs(response.data, "html.parser").find(
        "button", {"id": "stop-distribution-modal"}
    )
    assert stop_modal_button
    link = stop_modal_button.parent["href"]
    assert stop_modal_button.text == "Verteilung stoppen"
    assert link == url_for("distribution.confirm_stop_modal")

    # opening up a modal with a form and button
    response = test_client.get(link)
    form = bs(response.data, "html.parser").find(
        "form", {"id": "form-stop-distribution"}
    )
    stop_button = form.find("button", {"id": "stop-distribution"})

    assert stop_button
    assert stop_button.text == "Verteilung stoppen"
    assert stop_button["type"] == "submit"
    key = stop_button["name"]
    assert key == "distribution"
    value = stop_button["value"]
    assert value == "stop"
    url = form["action"]
    assert url == url_for("distribution.trigger")

    # if pushed the distribution shall be stopped
    test_client.post(url, data={key: value})
    dist = Distribution.current()
    assert dist.in_progress is False

    # and the stations deleted again
    assert stations_archived != dist.stations
    assert not dist.stations

    # cleanup
    dist.in_progress = True
    db.session.commit()
