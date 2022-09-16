import datetime

from ms.db import db_api
from ms.db.models import Product, Station, Unit, db


def test_adding_unique_unit_product(test_app):

    # add units
    unit = dict(shortname="g", by_piece=False, longname="Gramm")
    db_api.add(Unit, unit)
    unit = dict(shortname="bnd", by_piece=True, longname="Bund")
    db_api.add(Unit, unit)
    db_api.add(Unit, unit)
    db_api.add(Unit, unit)
    db_api.add(Unit, unit)
    db_api.add(Unit, unit)
    db_api.add(Unit, unit)

    # from test_product, as there is relationship testing
    kg = dict(shortname="kg", by_piece=False, longname="Kilogramm")
    st = dict(shortname="st", by_piece=True, longname="Stück")
    db_api.add(Unit, kg)
    db_api.add(Unit, st)

    units = Unit.query.all()
    assert len(units) == 4
