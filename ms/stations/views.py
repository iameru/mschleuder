import json

from flask import Blueprint, flash, render_template
from testmark import parse

stations = Blueprint("stations", __name__)


@stations.route("/")
def stations_view():

    dev_data = parse("ms/dev.md")  # DEV DATA
    stations = {
        "current": json.loads(dev_data["stations-current"]),
        "historical": json.loads(dev_data["stations-historical"]),
    }
    flash("asd Dies ist ein fehler omg. hast du vllt etwas vergessen? Sicher?")
    return render_template("stations/stations.html", stations=stations)
