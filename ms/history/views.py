from flask import Blueprint, render_template

history = Blueprint("history", __name__)


@history.route("/")
def history_view():

    return render_template("history/history.html")
