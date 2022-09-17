from bs4 import BeautifulSoup as bs


# for now each app has one entry here. might change to multi later
def test_settings_on_site(test_client):

    response = test_client.get("/settings/")

    body = bs(response.data, "html.parser").find("body")

    # find input fields
    name = body.find("input", {"id": "name"})
    display_name = body.find("input", {"id": "display_name"})
    header = body.find("input", {"id": "header"})
    footer = body.find("input", {"id": "footer"})
    assert name
    assert display_name
    assert header
    assert footer
