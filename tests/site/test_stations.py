import json

from bs4 import BeautifulSoup as bs

from ms.db.models import Station


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
