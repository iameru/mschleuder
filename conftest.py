from random import choice

import pytest

from ms import create_app
from ms.db.models import db
from ms.dev import dev_data

test_config = {
    "SECRET_KEY": "TEST_CONFIG",
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
}


@pytest.fixture(scope="session")
def test_app():

    test_app = create_app(test_config=test_config)

    with test_app.app_context():

        db.create_all()
        yield test_app
        db.drop_all()


@pytest.fixture(scope="session")
def test_client(test_app):

    with test_app.test_client() as test_client:

        yield test_client


@pytest.fixture(scope="session")
def products():
    return dev_data("products")


@pytest.fixture(scope="module")
def product(products):
    return choice(products)
