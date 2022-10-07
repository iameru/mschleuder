from ms.db.models import Distribution, db


def first_run():

    # check if necessary and set up distribution entry
    if not Distribution.query.first():

        db.session.add(Distribution(**dict(in_progress=False)))
        db.session.commit()
