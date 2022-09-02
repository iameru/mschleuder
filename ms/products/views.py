import json

from flask import Blueprint, flash, render_template
from testmark import parse

products = Blueprint("products", __name__)


@products.route("/")
def products_view():

    site = {"title": "Erzeugnisse"}

    dev_data = parse("dev.md")  # DEV DATA
    products = json.loads(dev_data["products"])
    products = sorted(products.copy(), key=lambda item: item["name"])
    recent_products = sorted(products, key=lambda item: item["recent_distribution"])[
        :10
    ]

    return render_template(
        "products/products.html",
        site=site,
        products=products,
        recent_products=recent_products,
    )
