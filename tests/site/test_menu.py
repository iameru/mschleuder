from bs4 import BeautifulSoup as bs

from ms.dev import dev_data


def parse_menu(test_client, url: str, link_name: str, recursive=True):

    """
    Find the existing menu and check for active hint
    """
    html = test_client.get(url)
    assert html.status_code == 200

    menu = bs(html.data, "html.parser").find("aside", {"class": "menu"})
    assert menu

    menu_list = menu.find("ul", {"class": "menu-list"})

    active_hint = menu_list.find_all("a", {"class": "is-active"})

    assert 1 == len(active_hint)

    assert link_name in active_hint[0]

    """
    If this is the first trip
    Find other links and try them
    """
    if not recursive:
        return True

    a_tags = [a_tag for a_tag in menu_list.find_all("a") if not a_tag.get("class")]
    for tag in a_tags:

        link_name = tag.text
        href = tag.get("href")
        assert link_name
        assert href

        parse_menu(test_client, href, link_name, recursive=False)

    return True


def test_menu_links(test_client):

    """
    given an entry point ("stations")
        I'll find a menu bar linking to other routes
    when I click them
    i'll find myself on the right page
        and with a menu again
    """

    parse_menu(test_client, "/stations/", "Stationen")
    parse_menu(test_client, "/products/", "Gemüse")
    parse_menu(test_client, "/", "History")


def test_products_in_distribution(test_client):

    html = test_client.get("/settings/")
    menu = bs(html.data, "html.parser").find("aside", {"class": "menu"})
    in_distribution = dev_data("in-distribution")

    product_list = menu.find("ul", {"id": "products-in-distribution"})
    assert product_list

    for item in in_distribution:

        menu_entry = product_list.find("a", {"id": f"distributed-product-{item['id']}"})

        assert item["name"] in menu_entry.text
        assert str(item["amount"]) in menu_entry.text
        assert item["unit"] in menu_entry.text

        url = menu_entry["href"]

        assert str(item["id"]) in url


def test_distribution_overview_link(test_client):

    html = test_client.get("/")
    menu = bs(html.data, "html.parser").find("aside", {"class": "menu"})

    link = menu.find("a", string="Aktuelle Verteilung")
    assert link
    assert "/distribute/overview" in link["href"]

    res = test_client.get(link["href"])
    assert res.status_code == 200
