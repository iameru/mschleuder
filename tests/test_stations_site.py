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
