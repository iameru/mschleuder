import json

from flask import Blueprint, flash, render_template

from ms.dev import dev_data

stations = Blueprint("stations", __name__)


@stations.route("/")
def stations_view():

    stations = {
        "current": dev_data("stations-current"),
        "historical": dev_data("stations-historical"),
    }

    labels = []
    data = []
    data = [[None for _ in range(len(stations["historical"]))] for x in range(123)]

    chart_data = dev_data("stations-chart")

    for idx, event in enumerate(stations["historical"]):
        labels.append(event["date"])

        for station in event["stations"]:

            members = station["members_full"] + (station["members_half"] / 2)
            data[station["id"]][idx] = members

    labels.reverse()
    for item in data:
        item.reverse()
    chart_data = {"labels": labels, "data": data}

    return render_template(
        "stations/stations.html", stations=stations, chart_data=chart_data
    )


@stations.route("/stationsdetail/<int:stationid>")
def detail_view(stationid):

    stations = dev_data("stations-current")

    station = next((item for item in stations if item["id"] == stationid), None)

    return render_template("stations/detail_view.html", station=station)


@stations.route("/new")
def new_station():
    return render_template("stations/new.html")
