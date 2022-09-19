from flask import Blueprint, flash, redirect, render_template, request, url_for

from ms.db import db_api
from ms.db.forms import StationForm
from ms.db.models import Station, db

stations = Blueprint("stations", __name__)


@stations.route("/")
def stations_view():

    stations = Station.query.all()
    return render_template("stations/stations.html", stations=stations)


@stations.route("/edit/<int:stationid>", methods=["POST"])
def edit(stationid):

    station = Station.query.get(stationid)
    form = StationForm(request.form, obj=station)

    form.populate_obj(station)

    if form.validate():
        db.session.add(station)
        db.session.commit()

        return redirect(url_for("stations.stations_view"), 302)

    flash("something went wrong...")
    return redirect(url_for("stations.stations_view"), 302)


@stations.route("/stationsdetail/<int:stationid>")
def detail_view(stationid):

    station = Station.query.get(stationid)
    form = StationForm(request.form, station)

    return render_template("stations/detail_view.html", station=station, form=form)


@stations.route("/new", methods=["GET", "POST"])
def new_station():

    station = Station()
    form = StationForm(request.form)
    form.populate_obj(station)

    if request.method == "POST" and form.validate():

        db.session.add(station)
        db.session.commit()

        return redirect(url_for("stations.stations_view"), 302)

    return render_template("stations/new.html", form=form)
