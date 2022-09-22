from flask import Blueprint, redirect, render_template, request, url_for

from ms.db.forms import ProductForm
from ms.db.models import Product, db

products = Blueprint("products", __name__)


@products.route("/")
def products_view():

    products = Product.query.all()

    return render_template("products/products.html", products=products)


@products.route("/productdetail/<int:productid>", methods=["POST", "GET"])
def edit_view(productid):

    product = Product.query.get(productid)
    form = ProductForm(request.form, obj=product)
    form.populate_obj(product)

    if request.method == "POST" and form.validate():

        db.session.add(product)
        db.session.commit()

        return redirect(url_for("products.products_view"), 302)

    return render_template("products/detail_view.html", product=product, form=form)


@products.route("/new", methods=["GET", "POST"])
def new_product():

    product = Product()
    form = ProductForm(request.form, obj=product)

    form.populate_obj(product)

    if request.method == "POST" and form.validate():

        db.session.add(product)
        db.session.commit()

        return redirect(url_for("products.products_view"), 302)

    return render_template("products/new.html", form=form)
