from pytest import mark


def url(test_client, url: str, title):
    response = test_client.get(url + "/")
    assert response.status_code == 200
    response = test_client.get(url)
    assert response.status_code == 308

    response = test_client.get(url + "/")
    assert b"<title>404 Not Found</title>" not in response.data
    assert b"<!doctype html>" in response.data
    title_element = f">{title}</h2>"
    assert title_element.encode() in response.data


def test_template_and_url_for_settings(test_client):
    url(test_client, "/settings", "Einstellungen")


def test_template_and_url_for_stations(test_client):
    url(test_client, "/stations", "Stationen")


def test_template_and_url_for_products(test_client):
    url(test_client, "/products", "Erzeugnisse")


def test_template_and_url_for_history(test_client):
    url(test_client, "/history", "History")
