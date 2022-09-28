from flask import Blueprint, render_template

from ms.db import query
from ms.db.models import Distribution, Product

history = Blueprint("history", __name__)


@history.route("/")
def history_view():

    return render_template("history/history.html")


@history.route("/detail/<int:distribution_id>/<int:product_id>")
def product_detail_view(distribution_id, product_id):

    product = Product.query.get(product_id)
    distribution = Distribution.query.get(distribution_id)
    data = query.product_details(distribution_id, product_id)

    return render_template(
        "history/product_detail_modal.html",
        data=data,
        product=product,
        distribution=distribution,
    )
