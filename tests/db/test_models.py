from ms.db.models import Product, Unit, db


def test_add_unit(test_app):

    assert True


def test_unit_product(test_app):

    kg = Unit(shortname="kg", by_piece=False, longname="Kilogramm")
    st = Unit(shortname="st", by_piece=True, longname="Stück")
    db.session.add(kg)
    db.session.add(st)
    product_1 = Product(name="Kartoffel", unit_id=1, info="Lecker Kartoffel")
    db.session.add(product_1)
    product_2 = Product(name="Kohlrabi", unit_id=2, info="Super Kohlrabi")
    db.session.add(product_2)
    product_3 = Product(name="Mangold", unit_id=1, info="Mega Mangold")
    db.session.add(product_3)

    db.session.commit()

    products = Product.query.all()

    for product in products:
        assert product.unit.longname

    unit = Unit.query.filter_by(shortname="kg").first()

    assert product_1 in unit.products
    assert product_2 not in unit.products
    assert product_3 in unit.products


def test_consistency_of_db_model():

    potatoe = Product.query.filter_by(name="Kartoffel").first()
    mangold = Product.query.filter_by(name="Mangold").first()

    assert "Kartoffel" == potatoe.name
    assert "Mangold" == mangold.name
