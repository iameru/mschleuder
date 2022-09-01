import pytest

from ms import create_app

test_config = {
    "SECRET_KEY": "TEST_CONFIG",
    "TESTING": True,
}


@pytest.fixture(scope="module")
def test_client():

    test_app = create_app(test_config=test_config)

    with test_app.test_client() as test_client:
        yield test_client
