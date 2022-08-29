import json

from flask import Blueprint
from testmark import parse

stations = Blueprint("stations", __name__)


@stations.route("/")
def view_index():

    dev_data = parse("ms/dev.md")  # DEV DATA
    stations = {
        "current": json.loads(dev_data["stations-current"]),
        "historical": json.loads(dev_data["stations-historical"]),
    }
    return stations
