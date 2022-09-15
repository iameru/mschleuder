from flask import Blueprint, abort, redirect, render_template, request, session, url_for

from ms.db.forms import ProductForm
from ms.db.models import Product, Unit, db
from ms.dev import dev_data

products = Blueprint("products", __name__)


@products.route("/")
def products_view():

    products = Product.query.all()

    all_products = sorted(products.copy(), key=lambda item: item.name)
    distributed_products = [
        product for product in products if product.last_distribution
    ]
    recent_products = sorted(
        distributed_products, key=lambda item: item.last_distribution
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

    product = Product.query.get(productid)

    return render_template("products/detail_view.html", product=product)


@products.route("/distribute")
def distribute_view():

    return render_template("products/distribute/overview.html")


@products.route("/distribute/<int:productid>")
def distribute_by_id(productid):

    product = Product.query.get(productid)
    if not product:
        abort(404)

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


@products.route("/new", methods=["GET", "POST"])
def new_product():

    form = ProductForm(request.form)

    if request.method == "POST" and form.validate():

        product = Product(
            name=form.data["name"], unit_id=form.data["unit_id"], info=form.data["info"]
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("products.products_view"), 302)

    return render_template("products/new.html", form=form)
