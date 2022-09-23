from conftest import BrowserTest, test_config


def test_test_app(test_app):

    assert test_app


def test_test_config(test_app):

    for key, value in test_config.items():
        assert test_app.config[key] == value


def test_test_client(test_client):

    assert test_client


def test_client_generated_from_app(test_app, test_client):

    with test_app.test_client() as test_app_client:

        assert test_app_client.application == test_client.application


class TestSeleniumBaseClass(BrowserTest):
    def test_driver_in_class(self):

        assert self.driver
