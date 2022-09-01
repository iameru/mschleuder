import json

from flask import Blueprint, flash, render_template
from testmark import parse

history = Blueprint("history", __name__)


@history.route("/")
def history_view():

    site = {"title": "History"}
    return render_template("history/history.html", site=site)
