from pathlib import Path

from flask import Blueprint, render_template, url_for
from flask_weasyprint import HTML, render_pdf

from ms.db import query
from ms.db.models import Distribution, Product, Share, StationHistory

history = Blueprint("history", __name__)


@history.route("/")
def overview():

    distributions = Distribution.query.filter(
        Distribution.in_progress == False, Distribution.finalized == True
    ).all()

    return render_template("history/history.html", distributions=distributions)


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


@history.route("/stationdetails/<int:station_id>")
@history.route("/stationdetails/<int:station_id>/<pdf_station_name>.pdf")
def station_distribution_details(station_id, pdf_station_name=None):

    station = StationHistory.query.get_or_404(station_id)
    shares = Share.query.filter(Share.stationhistory_id == station.id).all()

    if pdf_station_name:

        css = [Path("ms/static/customisation.css"), Path("ms/static/style.css")]
        html = render_template(
            "history/station_details.pdf.html", station=station, shares=shares
        )

        return render_pdf(HTML(string=html), stylesheets=css)

    return render_template(
        "history/station_details_modal.html", station=station, shares=shares
    )
