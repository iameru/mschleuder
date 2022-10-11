from random import choice

from bs4 import BeautifulSoup as bs
from flask import url_for

from ms.db.models import Distribution, Share, StationHistory


def test_history_overview(test_client):

    distributions = Distribution.query.filter(
        Distribution.in_progress == False, Distribution.finalized == True
    ).all()

    response = test_client.get(url_for("history.overview"))
    assert response.status_code == 200

    table = bs(response.data, "html.parser").find(
        "table", {"id": "history-overview-table"}
    )

    for dist in distributions:

        year = dist.date_time.strftime("%Y")
        date_and_day = dist.date_time.strftime("%d.%B %-H:%M")

        row = table.find("tr", {"id": f"distribution-{dist.id}"})
        assert row

        assert year in row.text
        assert date_and_day in row.text

        for station in dist.stations:

            link = row.find("a", string=station.name)
            assert link
            assert link["hx-get"] == url_for(
                "history.station_distribution_details", station_id=station.id
            )


def test_details_of_distribution_for_stations(test_client):

    dist = Distribution.query.filter(
        Distribution.in_progress == False, Distribution.finalized == True
    ).first()
    assert dist
    station = choice(dist.stations)
    assert station
    shares = Share.query.filter(Share.stationhistory_id == station.id).all()

    # get the overview and assert the shares details for it inside
    # station id is enough as every station is unique for a distribution
    response = test_client.get(
        url_for("history.station_distribution_details", station_id=station.id)
    )
    assert response.status_code == 200

    txt = response.data.decode()

    # basic check for now
    for share in shares:

        assert share.product.name in txt
        assert share.unit.shortname in txt
        assert str(share.single_full) in txt
        assert str(share.single_half) in txt
