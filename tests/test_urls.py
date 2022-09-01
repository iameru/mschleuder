from pytest import mark


@mark.skip(reason="tba")
def test_history_url(test_app):

    response = test_app.get("/history/")
    assert response.status_code == 200
    response = test_app.get("/history")
    assert response.status_code == 308


@mark.skip(reason="tba")
def test_history_using_template(test_app):

    response = test_app.get("/history/")
    assert b"<title>404 Not Found</title>" not in response.data
    assert b"<!doctype html>" in response.data


def test_products_url(test_app):

    response = test_app.get("/products/")
    assert response.status_code == 200
    response = test_app.get("/products")
    assert response.status_code == 308


def test_products_using_template(test_app):

    response = test_app.get("/products/")
    assert b"<title>404 Not Found</title>" not in response.data
    assert b"<!doctype html>" in response.data


def test_stations_url(test_app):

    response = test_app.get("/stations/")
    assert response.status_code == 200
    response = test_app.get("/stations")
    assert response.status_code == 308


def test_stations_using_template(test_app):

    response = test_app.get("/stations/")
    assert b"<title>404 Not Found</title>" not in response.data
    assert b"<!doctype html>" in response.data
