from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import class_mapper

from ms.db.models import Organisation, db


def add(Model, item: dict):

    stmt = insert(Model).values(**item).on_conflict_do_nothing()
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


def update(modelinstance, update: dict):

    _class = modelinstance.__class__
    fields = class_mapper(_class).attrs.keys()

    for key, value in update.items():

        if key in fields:

            setattr(modelinstance, key, value)


# def _update(Model, query_item: dict, update: dict):
#
#    if len(Model.query.filter_by(**query_item).all()) == 1:
#
#        Model.query.filter_by(**query_item).update(update)
#        db.session.commit()
#        return True
#
#    return False
