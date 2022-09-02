import json

from flask import Blueprint, flash, render_template
from testmark import parse

stations = Blueprint("stations", __name__)


@stations.route("/")
def stations_view():

    site = {"title": "Stationen"}
    dev_data = parse("dev.md")  # DEV DATA
    stations = {
        "current": json.loads(dev_data["stations-current"]),
        "historical": json.loads(dev_data["stations-historical"]),
    }

    labels = []
    data = []
    data = [[None for _ in range(len(stations["historical"]))] for x in range(123)]

    chart_data = json.loads(dev_data["stations-chart"])

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
        "stations/stations.html", stations=stations, chart_data=chart_data, site=site
    )
