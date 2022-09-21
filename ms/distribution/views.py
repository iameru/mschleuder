from flask import Blueprint, render_template

distribution = Blueprint("distribution", __name__)


@distribution.route("/overview")
def overview():

    return render_template("distribution/overview.html")


@distribution.route("/gateway", methods=["POST"])
def distribute_gateway():

    return ""


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
