import json
from pathlib import Path
from random import choice, randint

import pytest
from bs4 import BeautifulSoup as bs
from flask import url_for

from ms.db.models import Distribution, Product, Share, Station, StationHistory, Unit, db


@pytest.fixture(autouse=True, scope="module")
def distribute():
    # setup
    dist = Distribution(in_progress=True)
    db.session.add(dist)
    db.session.commit()
    Station.archive_all(dist.id)

    yield dist.in_progress


def test_post_nonvalid_data_to_save_distribution(test_client):

    response = test_client.post(url_for("distribution.save"), data={"stuff": "wrong"})
    assert response.status_code == 404


def _save_product(test_client, product: Product):

    # we have a product we want to share for this distribution, in a unit, with infos of a station at that time.
    # we would have to do this for each station
    # dist.id gets added in view
    unit = choice(product.units)
    dist = Distribution.current()
    post_data = []
    # we generate the data to post
    for station in dist.stations:

        # we have values we want to be saved (given from frontend)
        # single members each get
        single_full = randint(2, 100)
        single_half = int(single_full / 2)

        # the whole station gets
        sum_full = single_full * station.members_full
        sum_half = single_half * station.members_half

        # we build the keys
        keys = dict(
            product_id=product.id,
            stationhistory_id=station.id,
            unit_id=unit.id,
        )
        # we build the data
        data = dict(
            single_full=single_full,
            single_half=single_half,
            sum_full=sum_full,
            sum_half=sum_half,
        )
        data.update(keys)

        post_data.append(data)

    data = json.dumps(post_data)

    # we send the request
    response = test_client.post(
        url_for("distribution.save"),
        data=data,
        content_type="application/json",
        follow_redirects=True,
    )

    # we return the response for tests
    return dict(response=response, post_data=post_data)


def test_saving_of_a_distribution(test_client):

    # have to pretend a bit as the generation is in javascript
    # see test in function _save_product

    product = Product.query.get(1)
    result = _save_product(test_client, product)
    response = result.get("response")
    post_data = result.get("post_data")
    assert response.status_code == 200
    assert response.text == ""

    # we expect all entries to be saved to database
    for data in post_data:

        share = Share.query.filter_by(**data).first()
        assert share


def test_saving_no_duplicates(test_client, product):

    # save a product 5 times
    product = Product.query.get(2)
    for _ in range(5):
        result = _save_product(test_client, product)
        post_data = result.get("post_data")

    # expect only one, not 5, entries for this
    query = dict(
        product_id=product.id,
        distribution_id=Distribution.current().id,
        stationhistory_id=post_data[0].get("stationhistory_id"),
        unit_id=post_data[0].get("unit_id"),
    )
    share = Share.query.filter_by(**query).all()
    assert len(share) != 5
    assert len(share) == 1

    # expect the last post request to be in database
    share = share[0]
    for key, value in post_data[0].items():
        assert share.__dict__[key] == value


def test_info_can_be_given_for_distribution_in_overview(test_client):

    # we want to add a comment to a distribution in progress
    response = test_client.get(url_for("distribution.overview"))
    html = bs(response.data, "html.parser")

    # there should be a containre and a button for it
    container = html.find("div", {"id": "add-distribution-info"})
    assert container
    assert "Die allerbeste Info der Welt!" not in container.text
    button = container.find("button", {"id": "add-distribution-info-button"})
    assert button
    assert button["hx-get"] == url_for("distribution.add_distribution_info")
    assert button["hx-target"] == "#add-distribution-info"
    assert button["hx-swap"] == "innerHTML"

    # we "push" the button and expect a form to edit the commentary
    response = test_client.get(button["hx-get"])
    html = bs(response.data, "html.parser")

    form = html.find("form", {"id": "add-distribution-info-form"})
    assert form
    assert form["method"] == "POST"
    assert form["action"] == url_for("distribution.add_distribution_info")

    input_field = form.find("input", {"id": "add-distribution-info-input"})
    assert input_field
    assert input_field["name"] == "info"

    submit_button = form.find("button", {"id": "add-distribution-info-submit-button"})
    assert submit_button

    assert html.find("a", {"id": "add-distribution-info-abort-button"})

    # we submit the form
    response = test_client.post(
        form["action"], data={input_field["name"]: "Die allerbeste Info der Welt!"}
    )
    assert response.status_code == 200

    # we expect the info now be displayed in the page
    response = test_client.get(url_for("distribution.overview"))
    html = bs(response.data, "html.parser")
    container = html.find("div", {"id": "add-distribution-info"})
    assert "Die allerbeste Info der Welt!" in container.text


def test_info_can_be_given_for_a_product_in_overview(test_client):

    # we want to add a comment to a product in distribution
    response = test_client.get(url_for("distribution.overview"))
    html = bs(response.data, "html.parser")
    # so we look for the product
    # we know this from earlier when we inserted
    row = html.find("tr", class_="product-row")
    assert row
    _string_magic = row["id"].split("-")
    product = Product.query.get(int(_string_magic[-2]))
    unit = Unit.query.filter(Unit.longname == _string_magic[-1]).first()

    # we find a button with a link
    add_info_button = row.find("button", {"id": "add-info"})
    assert add_info_button
    assert add_info_button["hx-get"] == url_for(
        "distribution.add_product_info", product_id=product.id, unit_id=unit.id
    )
    assert add_info_button.text == "Info bearbeiten"

    # we follow the link
    response = test_client.get(add_info_button["hx-get"])
    assert response.status_code == 200

    # and find a text and an input field and a button to save
    # the information for this distribution
    hx_html = bs(response.data, "html.parser")

    form = hx_html.find("form", {"id": "add-info-form"})
    assert form
    assert form["method"] == "POST"
    form_action = form["action"]
    assert form_action == url_for(
        "distribution.add_product_info", product_id=product.id, unit_id=unit.id
    )

    save_info_button = form.find("button", {"id": "save-info"})
    assert save_info_button
    assert save_info_button.text == "info speichern"

    input_field = form.find("input", {"id": "input-add-info"})
    assert input_field
    submit_name = input_field["name"]
    assert submit_name == "product-info"

    # we submit the form
    response = test_client.post(
        form_action, data={submit_name: "Sehr gute Informationen"}
    )
    assert response.status_code == 200

    # we expect the info now be displayed in the page
    response = test_client.get(url_for("distribution.overview"))
    info_field = bs(response.data, "html.parser").find(
        "div", {"id": f"info-div-{product.id}-{unit.id}"}
    )
    assert info_field
    assert "Sehr gute Informationen" in info_field.text


def test_delete_a_distribution_from_overview(test_client):

    # get a product which was distributed
    dist = Distribution.current()
    query = (
        db.session.query(
            Share.product_id.label("product_id"), Share.unit_id.label("unit_id")
        )
        .filter(Share.distribution_id == dist.id)
        .first()
    )
    product_id = query.product_id
    unit_id = query.unit_id
    assert product_id
    assert unit_id
    product = Product.query.get(product_id)
    unit = Unit.query.get(unit_id)

    all_shares_of_product = Share.query.filter(
        Share.product_id == product.id, Share.unit_id == unit.id
    ).all()
    assert all_shares_of_product

    # get site
    response = test_client.get(url_for("distribution.overview"))
    html = bs(response.data, "html.parser")
    row = html.find("tr", {"id": f"overview-{product.id}-{unit.longname}"})
    delete_button = row.find(
        "button", {"id": f"delete-from-distribution-{product.id}-{unit.longname}"}
    )
    assert delete_button
    link = delete_button["hx-get"]
    assert link == url_for(
        "distribution.delete_from_distribution",
        product_id=product.id,
        unit_shortname=unit.shortname,
    )

    # follow modal link
    response = test_client.get(link)
    assert response.status_code == 200
    deletion_button = bs(response.data, "html.parser").find(
        "button", {"id": "confirm-deletion-button"}
    )
    assert deletion_button
    form = bs(response.data, "html.parser").find(
        "form", {"id": "confirm-deletion-form"}
    )
    assert form

    for key, value in {
        "delete": "1",
        "product_id": str(product.id),
        "unit_id": str(unit.id),
    }.items():
        input = form.find("input", {"name": key})
        assert value == input["value"]
    link = form["action"]
    assert link

    # follow confirmation link
    response = test_client.post(
        link,
        data={"delete": True, "product_id": product.id, "unit_id": unit.id},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert response.request.path == url_for("distribution.overview")

    # expect message for user that deletion was successfull
    messages = bs(response.data, "html.parser").find("div", class_="message")
    assert messages
    assert product.name in messages.text
    assert "gelöscht" in messages.text

    # deletion was successfull
    all_shares_of_product = Share.query.filter(
        Share.product_id == product.id, Share.unit_id == unit.id
    ).all()
    assert not all_shares_of_product


def test_no_pdf_field_before_finalization():

    dist: Distribution = Distribution.current()

    for station in dist.stations:

        assert not station.pdf


def test_finalization_of_distribution_in_db_and_interface(test_client):

    dist: Distribution = Distribution.current()
    assert dist.in_progress
    assert dist.finalized == False

    # find finalize button on overview site
    response = test_client.get(url_for("distribution.overview"))
    html = bs(response.data, "html.parser")

    button = html.find("button", {"id": "finalize-distribution-modal"})
    assert button
    href = button.parent["href"]
    link = button.parent["hx-get"]
    assert href
    assert link
    assert href == link == url_for("distribution.finalize")

    # open modal
    response = test_client.get(link)
    assert response
    assert response.status_code == 200
    html = bs(response.data, "html.parser")
    confirmation_button = html.find("button", {"id": "confirm-finalization-button"})
    assert confirmation_button
    form = html.find("form", {"id": "confirm-finalization-form"})
    assert form
    input = form.find("input", {"name": "finalization"})
    assert input["value"] == str(dist.id)
    link = form["action"]
    assert link
    assert link == url_for("distribution.finalize")
    assert form["method"] == "POST"

    # send this data
    response = test_client.post(
        link, data={input["name"]: input["value"]}, follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == "/"

    # expect message for user that finalization was successfull
    messages = bs(response.data, "html.parser").find("div", class_="message")
    assert messages
    assert "Verteilung abgeschlossen!" in messages.text

    assert not dist.in_progress
    assert dist.finalized == True


def test_expect_values_changed_after_finalisation(test_client):

    dist: Distribution = Distribution.current()
    assert not dist.in_progress
    assert dist.finalized == True

    # get products in this distribution
    shares = Share.query.filter(Share.distribution_id == dist.id).all()
    products_ids = []
    for share in shares:
        products_ids.append(share.product_id)
    products = [Product.query.get(_id) for _id in products_ids]

    for product in products:
        assert product.last_distribution.replace(microsecond=0) == dist.updated.replace(
            microsecond=0
        )


@pytest.mark.skip(reason="takes some time")
def test_generation_of_station_pdfs(test_client):

    dist: Distribution = Distribution.current()

    for station in dist.stations:

        response = test_client.get(
            url_for(
                "history.station_distribution_details",
                station_id=station.id,
                pdf_station_name=station.name,
            )
        )
        assert response.status_code == 200
        assert response.content_type == response.mimetype == "application/pdf"


@pytest.mark.skip(reason="takes some time")
def test_pdf_field_in_stationhistory_after_dist():

    dist: Distribution = Distribution.current()

    for station in dist.stations:

        assert station.pdf

        pdf = Path(station.pdf)
        assert pdf.exists()

        # teardown
        pdf.unlink()
