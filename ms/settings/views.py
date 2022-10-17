from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from ms.db import db_api
from ms.db.forms import OrganisationForm, UnitForm
from ms.db.models import Organisation, Unit, db

settings = Blueprint("settings", __name__)


@settings.route("setup", methods=["POST"])
def add_organisation():

    form = OrganisationForm(request.form)

    if form.validate():

        # this method is only allowed if no entry is there
        if Organisation.query.get(1):
            flash("setup already made", category="warning")
            abort(404)

        data = form.data
        del data["csrf_token"]
        db_api.add_org(data)

        flash("done!", category="primary")
        return redirect(url_for("settings.settings_view"), 302)

    flash("setup already made", category="warning")
    return redirect(url_for("settings.settings_view"), 302)


@settings.route("/")
def settings_view():

    organisation = Organisation.query.get(1)
    if not organisation:
        # HERE!
        form = OrganisationForm()
        return render_template("settings/setup.html", form=form)

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


@settings.route("/unit/<int:unit_id>/edit", methods=["GET", "POST"])
def edit_unit(unit_id):

    unit = Unit.query.get_or_404(unit_id)
    unit.by_piece = str(unit.by_piece)  # dirty workaround #12
    form = UnitForm(request.form, obj=unit)
    form.populate_obj(unit)

    if request.method == "POST" and form.validate():

        db.session.commit()

        return redirect(url_for("settings.settings_view"), 302)

    return render_template("settings/edit_unit.hx.html", unit=unit, form=form)
