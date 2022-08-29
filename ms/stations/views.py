import json

from flask import Blueprint, render_template
from testmark import parse

stations = Blueprint("stations", __name__)


@stations.route("/")
def stations_view():

    dev_data = parse("ms/dev.md")  # DEV DATA
    stations = {
        "current": json.loads(dev_data["stations-current"]),
        "historical": json.loads(dev_data["stations-historical"]),
    }
    return render_template("stations/stations.html", stations=stations)
