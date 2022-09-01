import json

from flask import Blueprint, flash, render_template
from testmark import parse

settings = Blueprint("settings", __name__)


@settings.route("/")
def settings_view():

    site = {"title": "Einstellungen"}
    return render_template("settings/settings.html", site=site)
