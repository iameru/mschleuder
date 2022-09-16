from flask import Blueprint, redirect, render_template, request, url_for

from ms.db import db_api
from ms.db.forms import UnitForm
from ms.db.models import Unit

settings = Blueprint("settings", __name__)


@settings.route("/")
def settings_view():

    units = Unit.query.all()

    return render_template("settings/settings.html", units=units)


@settings.route("/units/new", methods=["GET", "POST"])
def add_unit():

    form = UnitForm(request.form)

    if request.method == "POST" and form.validate():

        data = form.data
        del data["csrf_token"]
        db_api.add(Unit, data)

        return redirect(url_for("settings.settings_view"), 302)

    return render_template("settings/add_unit.html", form=form)
