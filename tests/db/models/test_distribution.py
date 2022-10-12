from datetime import datetime

from sqlalchemy import desc

from ms.db.models import Distribution, StationHistory, db


def test_entry_got_generated_via_test_setup(test_app):

    dist = Distribution.query.all()
    assert len(dist) == 1
    dist = dist[0]
    assert dist.in_progress is False
    assert dist.date_time == datetime.utcnow().replace(microsecond=0, second=0)

    # cleanup
    db.session.delete(dist)
    db.session.commit()


def test_distribution_model(test_app):

    data = dict(in_progress=False)
    dist = Distribution(**data)

    db.session.add(dist)
    db.session.commit()

    dist = Distribution.query.first()
    assert dist.in_progress is False
    assert dist.created
    assert not dist.updated

    dist.in_progress = True
    db.session.commit()

    dist = Distribution.query.first()
    assert dist.in_progress is True
    assert dist.created
    assert dist.updated

    # cleanup
    dist.in_progress = False
    db.session.commit()
    assert db.session.query(Distribution.in_progress is False).first()
    assert len(Distribution.query.all()) == 1


def test_query_for_latest_dist(test_app):

    dist = Distribution.query.order_by(Distribution.id).first()
    assert dist
    assert dist.in_progress is False

    # add some dists
    db.session.add(Distribution(**dict(in_progress=False)))
    db.session.commit()
    db.session.add(Distribution(**dict(in_progress=True)))
    db.session.commit()

    dist = Distribution.query.order_by(desc(Distribution.id)).first()
    assert dist
    assert dist.in_progress is True


def test_Model_function_to_get_latest_dist(test_app):

    dist = Distribution(**dict(in_progress=False))
    db.session.add(dist)
    db.session.commit()

    saved_dist = Distribution.current()

    assert dist == saved_dist


def test_adding_information_field():

    dist = Distribution.current()
    assert not dist.information
    dist.information = "Nächste Woche ist großes Kino"
    db.session.commit()

    dist = Distribution.current()
    assert dist.information
    assert dist.information == "Nächste Woche ist großes Kino"
