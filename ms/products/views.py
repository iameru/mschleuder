import json

from flask import Blueprint, flash, render_template
from testmark import parse

products = Blueprint("products", __name__)


@products.route("/")
def products_view():

    site = {"title": "Erzeugnisse"}

    dev_data = parse("dev.md")  # DEV DATA
    products = json.loads(dev_data["products"])
    all_products = sorted(products.copy(), key=lambda item: item["name"])

    recent_products = sorted(products, key=lambda item: item["recent_distribution"])
    recent_products.reverse()
    recent_products = recent_products[:10]

    return render_template(
        "products/products.html",
        site=site,
        products=all_products,
        recent_products=recent_products,
    )


@products.route("/productdetail/<int:productid>")
def detail_view(productid):

    dev_data = parse("dev.md")  # DEV DATA
    products = json.loads(dev_data["products"])

    product = next((item for item in products if item["id"] == productid), None)

    return render_template("products/detail_view.html", product=product)


@products.route("/distribute/<int:productid>")
def distribute_by_id(productid):

    dev_data = parse("dev.md")  # DEV DATA
    products = json.loads(dev_data["products"])

    product = next((item for item in products if item["id"] == productid), None)
    return ""


@products.route("/new")
def new_product():
    return ""
