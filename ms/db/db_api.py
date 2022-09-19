from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import class_mapper

from ms.db.models import Organisation, db


def add(Model, item: dict):

    data = {}
    # throw away fields not used in Model
    fields = class_mapper(Model).attrs.keys()
    for key, value in item.items():

        if key in fields:
            data[key] = value

    stmt = insert(Model).values(**data).on_conflict_do_nothing()
    db.session.execute(stmt)
    db.session.commit()

    return True


def add_org(item: dict):

    # currently one org per app
    if len(Organisation.query.all()) >= 1:
        return False

    stmt = insert(Organisation).values(**item).on_conflict_do_nothing()
    db.session.execute(stmt)
    db.session.commit()

    return True


def update(Model, query_item: dict, update: dict):

    if len(Model.query.filter_by(**query_item).all()) == 1:

        Model.query.filter_by(**query_item).update(update)
        db.session.commit()
        return True

    return False
