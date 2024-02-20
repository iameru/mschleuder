from random import choice

import pytest
from bs4 import BeautifulSoup as bs
from flask import url_for

from ms import create_app
from ms.db.models import Distribution, Product, Station, StationHistory, Unit, db
from ms.first_run import dev_run

test_config = {
    "SECRET_KEY": "TEST_CONFIG",
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    "CSRF_SECRET_KEY": "CSRF_TEST_KEY",
    "INSTANCE_PATH": "/dev/shm/ms-testing",
    "SERVER_NAME": "localhost",
}


@pytest.fixture(scope="session")
def test_app():

    test_app = create_app(test_config=test_config)

    with test_app.app_context():

        db.create_all()
        dev_run()

        yield test_app
        db.drop_all()


@pytest.fixture(scope="session")
def test_client(test_app):

    with test_app.test_client() as test_client:

        yield test_client


@pytest.fixture(scope="session")
def csrf():
    # This is a helper function grabbing CSRF Token for testing
    def _func(response):
        doc = bs(response.data, "html.parser")
        csrf_field = doc.find("input", {"id": "csrf_token", "name": "csrf_token"})
        return csrf_field["value"]

    return _func


@pytest.fixture(scope="function")
def products():
    return Product.query.all()


@pytest.fixture(scope="function")
def product(products):
    return choice(products)


@pytest.fixture(scope="function")
def units():
    return Unit.query.all()


@pytest.fixture(scope="function")
def unit(units):
    return choice(units)


@pytest.fixture(scope="function")
def stations():
    return Station.query.all()


@pytest.fixture(scope="function")
def station(stations):
    return choice(stations)


@pytest.fixture(scope="function")
def product_distribution(product, test_client, test_app):

    unit = choice(product.units)

    url = url_for(
        "distribution.distribute",
        p_unit_shortname=unit.shortname,
        p_id=product.id,
    )
    # go to distribution
    return test_client.get(url, follow_redirects=True)


@pytest.fixture(scope="function")
def not_in_distribution():

    # setup
    dist = Distribution(in_progress=False)
    db.session.add(dist)
    db.session.commit()
    Station.archive_all(dist.id)

    yield not dist.in_progress

    # teardown
    stations = StationHistory.query.filter_by(distribution_id=dist.id).all()
    [db.session.delete(station) for station in stations]
    db.session.delete(dist)
    db.session.commit()


@pytest.fixture(scope="function")
def in_distribution():

    # setup
    dist = Distribution(in_progress=True)
    db.session.add(dist)
    db.session.commit()
    Station.archive_all(dist.id)

    yield dist.in_progress

    # teardown
    stations = StationHistory.query.filter_by(distribution_id=dist.id).all()
    [db.session.delete(share) for share in dist.shares]
    [db.session.delete(station) for station in stations]
    db.session.delete(dist)
    db.session.commit()
