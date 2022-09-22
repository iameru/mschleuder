from ms.db.models import Distribution, db


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

    dist.in_progress = False
    db.session.commit()
    assert db.session.query(Distribution.in_progress == False).first()

    assert len(Distribution.query.all()) == 1
