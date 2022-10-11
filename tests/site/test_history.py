from random import choice

from flask import url_for

from ms.db.models import Distribution, Share, StationHistory


def test_history_overview(test_client):

    distributions = Distribution.query.filter(
        Distribution.in_progress == False, Distribution.finalized == True
    ).all()

    response = test_client.get(url_for("history.overview"))
    assert response.status_code == 200

    txt = response.data.decode()

    for dist in distributions:

        assert str(dist.date_time) in txt

        for station in dist.stations:

            assert station.name in txt


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
