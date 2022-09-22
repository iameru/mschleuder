from flask import (
    Blueprint,
    Response,
    abort,
    redirect,
    render_template,
    request,
    url_for,
)

from ms.db.models import Distribution, Product, Station, Unit, db

distribution = Blueprint("distribution", __name__)


@distribution.before_request
def check_distribution_in_progress():

    # check if dist is in progress, else redirect to start it
    if not Distribution.query.get(1).in_progress:

        if not request.endpoint == "distribution.trigger":

            return redirect(url_for("distribution.trigger"))


@distribution.route("/stop")
def confirm_stop_modal():
    return render_template("distribution/confirm_stop_modal.html")


@distribution.route("/start", methods=["GET", "POST"])
def trigger():

    if request.method == "POST":

        distribute = request.form["distribution"]
        if distribute == "start":

            dist = Distribution.query.get(1)
            dist.in_progress = True
            db.session.add(dist)
            db.session.commit()

        elif distribute == "stop":

            dist = Distribution.query.get(1)
            dist.in_progress = False
            db.session.add(dist)
            db.session.commit()

        return redirect(url_for("distribution.overview"), 302)

    return render_template("distribution/start_distribution.html")


@distribution.route("/overview")
def overview():

    return render_template("distribution/overview.html")


@distribution.route("/p_<int:p_id>", methods=["GET"])
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

    stations = Station.query.order_by(Station.delivery_order).all()
    station_sums = {
        "full": sum(station.members_full for station in stations),
        "half": sum(station.members_half for station in stations),
        "total": sum(station.members_total for station in stations),
    }

    return render_template(
        "distribution/distribute.html",
        product=product,
        unit=unit,
        stations=stations,
        station_sums=station_sums,
    )


@distribution.route("/<int:productid>")
def distribute_by_id(productid):

    product = Product.query.get(productid)
    if not product:
        abort(404)

    stations = Station.query.all()
    station_sums = {
        "full": sum(station.members_full for station in stations),
        "half": sum(station.members_half for station in stations),
    }
    station_sums["total"] = station_sums["full"] + station_sums["half"]

    return render_template(
        "distribution/distribute.html",
        product=product,
        stations=stations,
        station_sums=station_sums,
    )
