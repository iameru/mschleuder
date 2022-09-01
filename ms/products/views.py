import json

from flask import Blueprint, flash, render_template
from testmark import parse

products = Blueprint("products", __name__)


@products.route("/")
def products_view():

    site = {"title": "Erzeugnisse"}
    return render_template("products/products.html", site=site)
