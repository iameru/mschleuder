import json

from flask import Blueprint, render_template, request

from ms.db.models import Product, ProductForm, db
from ms.dev import dev_data

products = Blueprint("products", __name__)


@products.route("/")
def products_view():

    products = dev_data("products")
    all_products = sorted(products.copy(), key=lambda item: item["name"])
    distributed_products = [
        product for product in products if product["recent_distribution"]
    ]
    recent_products = sorted(
        distributed_products, key=lambda item: item["recent_distribution"]
    )
    recent_products.reverse()
    recent_products = recent_products[:10]

    return render_template(
        "products/products.html",
        products=all_products,
        recent_products=recent_products,
    )


@products.route("/productdetail/<int:productid>")
def detail_view(productid):

    products = dev_data("products")
    product = next((item for item in products if item["id"] == productid), None)

    return render_template("products/detail_view.html", product=product)


@products.route("/distribute")
def distribute_view():

    return render_template("products/distribute/overview.html")


@products.route("/distribute/<int:productid>")
def distribute_by_id(productid):

    products = dev_data("products")
    in_distribution = dev_data("in-distribution")

    product = next((item for item in products if item["id"] == productid), None)
    # already distributed product:
    d_product = next(
        (item for item in in_distribution if item["id"] == productid), None
    )
    if d_product:
        product.update(d_product)

    stations = dev_data("stations-current")

    station_sums = {
        "full": sum(station["members_full"] for station in stations),
        "half": sum(station["members_half"] for station in stations),
    }
    station_sums["total"] = station_sums["full"] + station_sums["half"]

    return render_template(
        "products/distribute/distribute.html",
        product=product,
        stations=stations,
        station_sums=station_sums,
    )


@products.route("/new")
def new_product():

    form = ProductForm()

    return render_template("products/new.html", form=form)


@products.route("/new", methods=["POST"])
def post_new_product():

    product = Product(**request.json)
    db.session.add(product)
    db.session.commit()

    return f"{product.name}", 201
