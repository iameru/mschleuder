from flask import Blueprint, render_template, url_for

from ms.db import query
from ms.db.models import Distribution, Product

history = Blueprint("history", __name__)


@history.route("/")
def overview():

    return render_template("history/history.html")


@history.route("/detail/<int:distribution_id>/<int:product_id>/<int:unit_id>")
def product_detail_view(distribution_id, product_id, unit_id):

    product = Product.query.get(product_id)
    distribution = Distribution.query.get(distribution_id)
    data = query.product_details(distribution_id, product_id, unit_id)

    return render_template(
        "history/product_detail_modal.html",
        data=data,
        product=product,
        distribution=distribution,
    )


from ms.db.models import Share, StationHistory


@history.route("/stationdetails/<int:station_id>")
def station_distribution_details(station_id):

    station = StationHistory.query.get_or_404(station_id)
    shares = Share.query.filter(Share.stationhistory_id == station.id).all()

    return render_template(
        "history/station_details_modal.html", station=station, shares=shares
    )
