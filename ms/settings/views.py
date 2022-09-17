from flask import Blueprint, redirect, render_template, request, url_for

from ms.db import db_api
from ms.db.forms import OrganisationForm, UnitForm
from ms.db.models import Organisation, Unit, db

settings = Blueprint("settings", __name__)


@settings.route("/")
def settings_view():

    organisation = Organisation.query.get(1)
    form = OrganisationForm(request.form, organisation)

    # if request.method == "POST" and form.validate():

    # Suggestion for now
    # data = form.data
    # del data["csrf_token"]

    # Organisation.query.get(1).update(data)
    # db.session.commit()
    #
    # return redirect(url_for("settings.settings_view"), 302)

    units = Unit.query.all()

    return render_template("settings/settings.html", units=units, form=form)


@settings.route("/units/new", methods=["GET", "POST"])
def add_unit():

    form = UnitForm(request.form)

    if request.method == "POST" and form.validate():

        data = form.data
        del data["csrf_token"]
        db_api.add(Unit, data)

        return redirect(url_for("settings.settings_view"), 302)

    return render_template("settings/add_unit.html", form=form)
