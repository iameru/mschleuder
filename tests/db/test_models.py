import json


def test_add_product(test_client, product):

    item = {"name": product["name"], "by_piece": product["by_piece"]}
    data = json.dumps(item)
    response = test_client.post(
        "/products/new", data=data, content_type="application/json"
    )

    assert item["name"] in response.text
    assert response.status_code == 201
