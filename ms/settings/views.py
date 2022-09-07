from flask import Blueprint, render_template

settings = Blueprint("settings", __name__)


@settings.route("/")
def settings_view():

    return render_template("settings/settings.html")
