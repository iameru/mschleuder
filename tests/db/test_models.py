def test_add_product(test_client, product):

    data = {"name": product["name"]}
    response = test_client.post(
        "/products/new", data=data, content_type="application/json"
    )

    assert response.status_code == 201
