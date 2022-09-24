from bs4 import BeautifulSoup as bs
from flask import url_for

from ms.db.models import Distribution, Station, db


def test_station_on_site(test_client, station):

    station = Station.query.get(1)
    response = test_client.get("/stations/")

    assert station.name in response.text


def test_all_stations_on_site(test_client):

    response = test_client.get("/stations/")

    for station in Station.query.all():
        assert station.name in response.text


def test_htmx_edit_station(test_client):

    station = Station.query.get(1)
    response = test_client.get("/stations/")
    html = bs(response.data, "html.parser")

    edit_button = html.find("a", {"id": f"station-edit-view-{station.id}"})

    url = edit_button["hx-get"]
    assert str(station.id) == url.split("/")[-1]

    modal = test_client.get(url)
    assert station.name in modal.text


def test_new_station_modal_shown(test_client):

    response = test_client.get("/stations/")
    html = bs(response.data, "html.parser")
    link = html.find("button", {"hx-get": "/stations/new"})
    assert link

    modal = test_client.get(link["hx-get"])
    assert modal.status_code == 200
    assert "Neue Station" in modal.text


def test_add_station(test_client, csrf):

    station = dict(
        name="Station One",
        info="01234 Infotown - 123 Superstreet",
        delivery_order=4,
        members_full=2,
        members_half=1,
    )

    # check station not in table
    response = test_client.get("/stations")
    assert station["name"] not in response.text

    # create station
    response = test_client.get("/stations/new")
    station["csrf_token"] = csrf(response)
    response = test_client.post("/stations/new", data=station, follow_redirects=True)
    assert response.status_code == 200

    # check if station got saved in the view
    station = Station.query.filter_by(name="Station One").first()
    box = bs(response.data, "html.parser").find(
        "div", {"id": f"box-station-{station.id}"}
    )
    assert box
    assert str(station.members_half) in box.text
    assert station.info in box.text
    assert "Station One" in box.text


def test_edit_station(test_client, csrf, station):

    # choose station to edit
    station_data = station.__dict__
    station_data = station_data.copy()

    # go to site and click on edit button
    response = test_client.get("/stations/")
    edit_box = bs(response.data, "html.parser").find(
        "a", {"id": f"station-edit-view-{station.id}"}
    )
    assert edit_box
    response = test_client.get(edit_box["hx-get"])

    # find form, fill details and send
    form = bs(response.data, "html.parser").find("form", {"id": "station-edit-form"})
    assert form

    station_data["csrf_token"] = csrf(response)
    del station_data["_sa_instance_state"]
    del station_data["id"]
    del station_data["updated"]
    del station_data["created"]
    station_data["members_full"] += 12
    station_data["members_half"] += 1
    station_data["name"] = "Station Site Edit Testname"
    response = test_client.post(
        form["action"], data=station_data, follow_redirects=True
    )
    assert response.status_code == 200

    # find new values in stations site
    response = test_client.get("/stations/")
    station_box = bs(response.data, "html.parser").find(
        "div", {"id": f"box-station-{station.id}"}
    )
    assert station_data["name"] in station_box.text
    assert station_data["info"] in station_box.text
    assert str(station_data["members_full"]) in station_box.text
    assert str(station_data["members_half"]) in station_box.text


def test_edit_station_members(test_client, csrf):

    response = test_client.get("/stations/stationsdetail/1")

    form = bs(response.data, "html.parser").find("form")

    name = form.find("input", {"id": "name"})
    info = form.find("input", {"id": "info"})
    delivery_order = form.find("input", {"id": "delivery_order"})
    members_full = form.find("input", {"id": "members_full"})
    members_half = form.find("input", {"id": "members_half"})

    data = dict(
        name=name["value"],
        info=info["value"],
        delivery_order=delivery_order["value"],
        members_full=int(members_full["value"]) + 5,
        members_half=int(members_half["value"]) + 3,
    )

    data.update(csrf=csrf(response))

    response = test_client.post(form["action"], data=data, follow_redirects=True)
    # find new values in stations site
    response = test_client.get("/stations/")
    station_box = bs(response.data, "html.parser").find("div", {"id": "box-station-1"})
    assert data["name"] in station_box.text
    assert data["info"] in station_box.text
    assert str(data["members_full"]) in station_box.text
    assert str(data["members_half"]) in station_box.text


def test_values_in_edit_station(test_client, station):

    response = test_client.get("/stations/")
    edit_box = bs(response.data, "html.parser").find(
        "a", {"id": f"station-edit-view-{station.id}"}
    )
    response = test_client.get(edit_box["hx-get"])
    form = bs(response.data, "html.parser").find("form")

    name = form.find("input", {"id": "name"})
    info = form.find("input", {"id": "info"})
    delivery_order = form.find("input", {"id": "delivery_order"})
    members_full = form.find("input", {"id": "members_full"})
    members_half = form.find("input", {"id": "members_half"})

    # Values in Fields?
    assert station.name == name["value"]
    assert station.info == info["value"]
    assert station.delivery_order == int(delivery_order["value"])
    assert str(station.members_full) == members_full["value"]
    assert str(station.members_half) == members_half["value"]


def test_stations_not_editable_in_distribution(test_client, in_distribution):

    assert in_distribution

    response = test_client.get(url_for("stations.stations_view"))
    html = bs(response.data, "html.parser")

    for station in Station.query.all():
        # dont find edit box
        edit_box = html.find("a", {"id": f"station-edit-view-{station.id}"})
        assert not edit_box
        # dont find create station link
        assert not html.find("button", {"hx-get": url_for("stations.new_station")})

    # but find reminder that its an ongoing distribution
    info = html.find("p", {"id": "text-station-in-distribution"})
    assert info
    assert "Aktuell in Verteilung - Stationen nicht editierbar" == info.text


def test_create_update_stations_routes_without_distribution(
    test_client, not_in_distribution
):

    # to new -> csrf token -> creation
    response = test_client.get(url_for("stations.new_station"))
    assert response.status_code == 200

    # to update -> csrf -> update
    response = test_client.get(url_for("stations.detail_view", stationid=1))
    assert response.status_code == 200


def test_create_update_stations_not_possible_in_distribution(
    test_client, in_distribution
):

    # no route to new -> no csrf token -> no creation
    response = test_client.get(url_for("stations.new_station"))
    assert response.status_code == 404

    # no route to update -> no csrf -> no update
    response = test_client.get(url_for("stations.detail_view", stationid=1))
    assert response.status_code == 404
