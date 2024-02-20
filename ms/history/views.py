from typing import Dict, List
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel

from flask import Blueprint, current_app, make_response, render_template, url_for, request
from flask_weasyprint import HTML, render_pdf

from ms.db import query
from ms.db.models import (
    Distribution,
    Organisation,
    Product,
    Share,
    StationHistory,
    Unit,
    db,
)

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
    csa = Organisation.query.first()

    if pdf_station_name:

        if not station.pdf:

            # make pdf
            css = [Path("ms/static/customisation.css"), Path("ms/static/style.css")]
            html = render_template(
                "history/station_details.pdf.html",
                station=station,
                shares=shares,
                csa=csa,
                pdf=True,
            )
            pdf = HTML(string=html)

            # write to db
            distribution_time = station.distribution.date_time
            pdf_path = Path(
                current_app.instance_path,
                "files/pdf",
                distribution_time.strftime(f"%Y%m%d-%H%M-{station.name}.pdf"),
            )
            pdf.write_pdf(target=pdf_path, stylesheets=css)
            station.pdf = pdf_path.as_posix()

            db.session.commit()

        pdf_path = Path(station.pdf)
        filename = pdf_path.name
        pdf_response = make_response(pdf_path.read_bytes())
        pdf_response.headers["Content-Type"] = "application/pdf"
        pdf_response.headers["Content-Disposition"] = f"inline; filename={filename}"

        return pdf_response

    return render_template(
        "history/station_details_modal.html", station=station, shares=shares, csa=csa
    )


@history.route("/tools/show-recent-distributions/<int:product_id>/<int:unit_id>")
def show_recent_distribution(product_id, unit_id):

    product = Product.query.get_or_404(product_id)
    unit = Unit.query.get_or_404(unit_id)
    how_many_distributions = 6

    result = query.show_recent_distribution(
        product, unit, how_many_distributions=how_many_distributions
    )

    return render_template(
        "history/tools/show_recent_distribution_modal.html",
        data=result,
        product=product,
        unit=unit,
        how_many_distributions=how_many_distributions,
    )


@history.route("/chart/stations")
def station_chart():

    stations = {}
    for station_id in db.session.query(StationHistory.station_id).distinct().all():

        result = (
            db.session.query(
                StationHistory.name,
                StationHistory.time_archived,
                StationHistory.members_total,
            )
            .filter(StationHistory.station_id == station_id[0])
            .all()
        )
        name = result[-1][0]
        stations[name] = result

    return render_template("history/station_chart.html", stations=stations)


@history.route("/chart/products")
def product_chart():
    return render_template("history/product_chart.html")


@history.route("/api/products")
def api_products():
    products = Product.query.all()
    return [{"id": product.id, "name": product.name} for product in products]


class ProductData(BaseModel):
    distribution_date: str
    value: float

class UnitProductData(BaseModel):
    total: float
    unit_name: str
    data: List[ProductData]

class ProductResponse(BaseModel):
    id: int
    name: str
    data: Dict[str, UnitProductData]

@history.route("/api/product")
def api_product() -> ProductResponse:

    request_args = request.args
    product_id = request_args.get("product_id")
    product = Product.query.get_or_404(product_id)

    start_time = datetime.strptime( request_args.get("start_date"), "%Y-%m-%d")
    end_time = datetime.strptime( request_args.get("end_date"), "%Y-%m-%d")

    def time_filter(share) -> bool:
        if start_time <= share.dist.date_time and share.dist.date_time <= end_time:
            return True
        return False
    filtered_data = [share for share in filter(time_filter, product.shares)]

    # extremely inefficient as this would be lot faster in DB. will do it in
    # python as the query rewrite is off the limits for now. fetch all dist ids
    dist_ids = set([share.dist.id for share in filtered_data])

    data = {}
    for dist_id in dist_ids:
        # fetch all shares for this distribution
        shares = [share for share in filtered_data if share.dist.id == dist_id]

        share_unit_name = shares[0].unit.longname

        shares_total = sum([share.sum_total for share in shares])

        if share_unit_name not in data.keys():
            data[share_unit_name] = {
                "total": shares_total,
                "data": [
                ProductData(
                    distribution_date=shares[0].dist.date_time.strftime("%Y-%m-%d"),
                    value=shares_total,
                    )],
                "unit_name": share_unit_name,
            }
        else:
            data[share_unit_name]["total"] += shares_total
            data[share_unit_name]["data"].append(
                ProductData(
                    distribution_date=shares[0].dist.date_time.strftime("%Y-%m-%d"),
                    value=shares_total,
                )
            )

    return ProductResponse(
        id=product.id,
        name=product.name,
        data=data,
    ).dict()

