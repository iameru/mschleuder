import json
from random import choice

from testmark import parse

stations = json.loads(parse("dev.md")["stations-current"])


def test_station_on_site(test_client):

    station = choice(stations)
    response = test_client.get("/stations/")

    assert station["name"].encode() in response.data


def test_all_stations_on_site(test_client):

    response = test_client.get("/stations/")

    for station in stations:
        assert station["name"].encode() in response.data


from bs4 import BeautifulSoup as bs


def test_htmx_edit_station(test_client):

    station = choice(stations)
    response = test_client.get("/stations/")
    html = bs(response.data, "html.parser")

    edit_button = html.find("a", {"id": f"station-edit-view-{station['id']}"})

    url = edit_button["hx-get"]
    assert str(station["id"]) == url.split("/")[-1]

    modal = test_client.get(url)
    assert station["name"] in modal.text


def test_new_station_modal_shown(test_client):

    response = test_client.get("/stations/")
    html = bs(response.data, "html.parser")
    link = html.find("button", {"hx-get": "/stations/new"})
    assert link

    modal = test_client.get(link["hx-get"])
    assert modal.status_code == 200
    assert "Neue Station" in modal.text
