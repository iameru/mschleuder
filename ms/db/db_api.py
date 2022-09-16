from sqlalchemy.dialects.sqlite import insert

from ms.db.models import db


def add(Model, item: dict):

    stmt = insert(Model).values(**item).on_conflict_do_nothing()
    db.session.execute(stmt)

    return True
