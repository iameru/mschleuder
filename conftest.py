from random import choice

import pytest

from ms import create_app
from ms.db.models import Product, Unit, db

test_config = {
    "SECRET_KEY": "TEST_CONFIG",
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    "CSRF_SECRET_KEY": "CSRF_TEST_KEY",
}


@pytest.fixture(scope="session")
def test_app():

    test_app = create_app(test_config=test_config)

    with test_app.app_context():

        db.create_all()
        # dirty for migrate to SQL
        kg = Unit(shortname="kg", by_piece=False, longname="Kilogramm")
        st = Unit(shortname="st", by_piece=True, longname="Stück")
        db.session.add(kg)
        db.session.add(st)
        db.session.commit()
        yield test_app
        db.drop_all()


@pytest.fixture(scope="session")
def test_client(test_app):

    with test_app.test_client() as test_client:

        yield test_client


@pytest.fixture(scope="session")
def products():
    return Product.query.all()


@pytest.fixture(scope="function")
def product(products):
    return choice(products)
