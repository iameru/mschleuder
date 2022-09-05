import json

from flask import Blueprint, flash, render_template

from ms.dev import dev_data

products = Blueprint("products", __name__)


@products.route("/")
def products_view():

    products = dev_data("products")
    all_products = sorted(products.copy(), key=lambda item: item["name"])
    recent_products = sorted(products, key=lambda item: item["recent_distribution"])
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
    all_products = sorted(products.copy(), key=lambda item: item["name"])
    product = next((item for item in products if item["id"] == productid), None)

    return render_template("products/detail_view.html", product=product)


@products.route("/distribute/<int:productid>")
def distribute_by_id(productid):

    products = dev_data("products")
    in_distribution = dev_data("in-distribution")

    product = next((item for item in products if item["id"] == productid), None)
    d_product = next(
        (item for item in in_distribution if item["id"] == productid), None
    )
    if d_product:
        product.update(d_product)

    return render_template("products/distribute/distribute.html", product=product)


@products.route("/new")
def new_product():
    return render_template("products/new.html")
