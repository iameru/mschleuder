from ms.db.models import Distribution, db


def first_run():

    # create all them tables
    db.create_all()

    # check if necessary and set up distribution entry
    dist = Distribution.query.first()

    if not dist:

        db.session.add(Distribution(**dict(in_progress=False)))
        db.session.commit()
