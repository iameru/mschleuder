from bs4 import BeautifulSoup as bs


def url(test_client, url, string, longmode=True):

    if longmode:
        response = test_client.get(url)
        assert response.status_code == 308

        response = test_client.get(url + "/")
        assert response.status_code == 200
    else:
        response = test_client.get(url)
        assert response.status_code == 200

    assert "<title>404 Not Found</title>" not in response.text

    html = bs(response.data, "html.parser")
    title = html.find("h2", {"class": "title is-2", "id": "site-title"})
    assert string in title.text


def test_template_and_url_for_stations(test_client):
    url(test_client, "/stations", "Stationen")


def test_template_and_url_for_products(test_client):
    url(test_client, "/products", "Erzeugnisse")


def test_template_and_url_for_history(test_client):
    url(test_client, "", "History")


def test_template_and_url_for_distribute_overview(test_client):
    url(test_client, "/products/distribute", "Verteilung", longmode=False)
