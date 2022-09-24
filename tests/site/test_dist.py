from random import choice

import pytest
from flask import url_for

from ms.db.models import Distribution, Product, Station, StationHistory, db


@pytest.fixture(autouse=True, scope="module")
def distribute():
    # setup
    dist = Distribution(**dict(in_progress=True))
    db.session.add(dist)
    db.session.commit()
    Station.archive_all(dist.id)

    yield dist.in_progress

    # teardown
    stations = StationHistory.query.filter_by(distribution_id=dist.id).all()
    [db.session.delete(station) for station in stations]
    db.session.delete(dist)
    db.session.commit()


def test_post_nonvalid_data_to_save_distribution(test_client):

    response = test_client.post(url_for("distribution.save"), data={"stuff": "wrong"})
    assert response.status_code == 404
