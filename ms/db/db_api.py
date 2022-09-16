from sqlalchemy.dialects.sqlite import insert

from ms.db.models import db


def add(Model, item: dict):

    stmt = insert(Model).values(**item).on_conflict_do_nothing()
    db.session.execute(stmt)

    return True


def _add(Model):

    val = dict(**Model.__dict__)
    del val["_sa_instance_state"]
    s = insert(Model.__class__).values(val).on_conflict_do_nothing()

    db.session.execute(s)
