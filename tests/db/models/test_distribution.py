from ms.db.models import Distribution, db


def test_entry_got_generated(test_app):

    dist = Distribution.query.all()
    assert len(dist) == 1
    assert dist[0].in_progress == False

    # cleanup
    db.session.delete(dist[0])
    db.session.commit()


def test_distribution_model(test_app):

    data = dict(in_progress=False)
    dist = Distribution(**data)

    db.session.add(dist)
    db.session.commit()

    dist = Distribution.query.first()
    assert dist.in_progress == False
    assert dist.created
    assert not dist.updated

    dist.in_progress = True
    db.session.commit()

    dist = Distribution.query.first()
    assert dist.in_progress == True
    assert dist.created
    assert dist.updated

    # cleanup
    dist.in_progress = False
    db.session.commit()
    assert db.session.query(Distribution.in_progress == False).first()
    assert len(Distribution.query.all()) == 1
