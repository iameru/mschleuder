import datetime

from ms.db import db_api
from ms.db.models import Organisation, db

organisation = dict(
    name="CSA-Runkelrübe",
    display_name="RuRü",
    info="Some Information",
    header="Here is your stuff for this week",
    footer="Feel free to participate: https://runkerlrüberli.de.vu.xyz.com.ru.de/members",
)


def test_adding_organisation(test_app):

    # add orga
    db_api.add(Organisation, organisation)

    assert Organisation.query.filter_by(**organisation).first()

    # add more does not add more..
    organisation.copy().update(name="Runkelrüberli SoLaWi")
    db_api.add(Organisation, organisation)
    organisation.copy().update(info="Epic")
    db_api.add(Organisation, organisation)

    assert len(Organisation.query.all()) == 1

    # organisation is same as first entry
    orga = Organisation.query.get(1).__dict__
    del orga["_sa_instance_state"]
    del orga["id"]
    assert orga == organisation


def test_changing_organisation_changes_id_1(test_app):

    # For the moment I want to only use ID1 as organisations are per instance
    # later on this might be changed to multiple orgas per instance f.e. on a single server

    org = Organisation.query.filter_by(**organisation).first()
    assert org

    updates = dict(name="RuRübe SoLaWi", info="More Infos soon")

    query = dict(id=org.id)
    db_api.update(Organisation, query, updates)

    # updates should be in query
    organisation.update(updates)
    assert Organisation.query.filter_by(**organisation).first()
