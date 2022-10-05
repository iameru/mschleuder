from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from ms.db import query
from ms.db.models import (
    Distribution,
    Product,
    Share,
    ShareModel,
    Station,
    StationHistory,
    Unit,
    db,
)

distribution = Blueprint("distribution", __name__)


@distribution.before_request
def check_distribution_in_progress():
    # check if dist is in progress, else redirect to start it
    if not Distribution.current().in_progress:
        if not request.endpoint == "distribution.trigger":
            return redirect(url_for("distribution.trigger"))


@distribution.route("/overview")
def overview():

    dist = Distribution.current()
    data = query.distribution_overview(dist)

    return render_template("distribution/overview.html", data=data, dist=dist)


@distribution.route("/start", methods=["GET", "POST"])
def trigger():

    if request.method == "POST":

        dist = Distribution.current()
        distribute = request.form["distribution"]

        if distribute == "start" and not dist.in_progress:

            dist = Distribution(**dict(in_progress=True))
            db.session.add(dist)
            db.session.commit()
            Station.archive_all(dist.id)

            return redirect(url_for("distribution.overview"), 302)

        elif distribute == "stop" and dist.in_progress:

            dist = Distribution.current()
            stations = StationHistory.query.filter_by(distribution_id=dist.id).all()
            dist.in_progress = False
            db.session.add(dist)
            [db.session.delete(share) for share in dist.shares]
            [db.session.delete(station) for station in stations]
            db.session.commit()

            return redirect(url_for("stations.stations_view"), 302)

        return abort(404)

    return render_template("distribution/start_distribution.html")


@distribution.route("/stop")
def confirm_stop_modal():
    return render_template("distribution/confirm_stop_modal.html")


@distribution.route("/<int:p_id>", methods=["GET"])
def product(p_id):

    product = Product.query.get_or_404(p_id)

    if not product.units:
        abort(404)

    if len(product.units) == 1:
        return redirect(
            url_for(
                "distribution.distribute",
                p_id=product.id,
                p_unit_shortname=product.units[0].shortname,
            ),
            302,
        )

    return render_template("distribution/choose_unit.html", product=product)


@distribution.route("/<int:p_id>/<p_unit_shortname>")
def distribute(p_id: int, p_unit_shortname: str):

    product = Product.query.get_or_404(p_id)
    unit = Unit.query.filter_by(shortname=p_unit_shortname).first()

    if not product or not unit:
        abort(404)

    dist = Distribution.current()

    # query if existing -> ask how to proceed
    already_distributed = False
    if (
        db.session.query(Share)
        .filter(
            Share.distribution_id == dist.id,
            Share.product_id == product.id,
            Share.unit_id == unit.id,
        )
        .first()
    ):
        already_distributed = True
        flash(
            "Schon verteilt! Hier kannst du nun neu verteilen oder zusätzlich verteilen",
            category="info",
        )

    stations = Station.query.order_by(Station.delivery_order).all()

    return render_template(
        "distribution/distribute.html",
        product=product,
        unit=unit,
        stations=stations,
        already_distributed=already_distributed,
    )


@distribution.route("/save", methods=["POST"])
def save():

    if request.content_type == "application/json":

        request_data: list = request.json
        dist = Distribution.current()
        product_id = request_data[0].get("product_id")
        unit_id = request_data[0].get("unit_id")

        poll_shares = Share.query.filter(
            Share.product_id == product_id,
            Share.distribution_id == dist.id,
            Share.unit_id == unit_id,
        )

        exclude_from_deletion = []

        for json_data in request_data:

            additional_distribution = json_data.pop("additional_distribution", None)

            data = dict(distribution_id=dist.id)
            data.update(json_data)

            _stationhistory_id = data.get("stationhistory_id")
            exclude_from_deletion.append(_stationhistory_id)
            result = poll_shares.filter(Share.stationhistory_id == _stationhistory_id)

            update_data = ShareModel(**data)

            if result.one_or_none():

                if additional_distribution:

                    entry = result.one()
                    entry.sum_full += update_data.sum_full
                    entry.sum_half += update_data.sum_half
                    entry.single_full += update_data.single_full
                    entry.single_half += update_data.single_half

                else:

                    result.update(update_data.dict())

            else:
                share = Share(**data)
                db.session.add(share)

        if not additional_distribution:
            poll_shares.filter(
                Share.stationhistory_id.notin_(exclude_from_deletion)
            ).delete()

        db.session.commit()

        return redirect(url_for("distribution.overview"), 302)

    return abort(404)


@distribution.route(
    "/delete/<int:product_id>/<unit_shortname>", methods=["GET", "POST"]
)
def delete_from_distribution(product_id, unit_shortname):

    product = Product.query.get_or_404(product_id)
    unit = Unit.query.filter(Unit.shortname == unit_shortname).one_or_none()
    dist = Distribution.current()

    if request.method == "POST":

        delete_product = request.form.get("delete")
        form_product = int(request.form.get("product_id", 0))
        form_unit = int(request.form.get("unit_id", 0))

        if delete_product and (form_product == product.id) and (form_unit == unit.id):

            product_shares = Share.query.filter(
                Share.product_id == product.id,
                Share.unit_id == unit.id,
                Share.distribution_id == dist.id,
            )
            product_shares.delete()
            db.session.commit()

            flash(f"{product.name} gelöscht", category="info")
            return redirect(url_for("distribution.overview"))

        return abort(404)

    return render_template(
        "distribution/confirm_delete_modal.html", product=product, unit=unit
    )
