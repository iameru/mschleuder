import pytest

from ms import create_app

test_config = {
    "SECRET_KEY": "TEST_CONFIG",
    "TESTING": True,
}


@pytest.fixture(scope="session")
def test_app():

    test_app = create_app(test_config=test_config)
    with test_app.app_context():
        # dbcreate
        yield test_app
        # dbdrop


@pytest.fixture(scope="module")
def test_client(test_app):

    with test_app.test_client() as test_client:
        yield test_client
