import json

from flask import Blueprint, flash, render_template
from testmark import parse

history = Blueprint("history", __name__)


@history.route("/")
def history_view():

    return render_template("history/history.html")
