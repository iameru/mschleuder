from datetime import datetime

from ms.db.models import Distribution, db


def test_entry_got_generated(test_app):

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
