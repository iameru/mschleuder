from pathlib import Path

from flask import current_app

from ms.db.models import Distribution, db


def first_run():

    # check and create folder for files
    pdfs = Path(Path(current_app.instance_path), Path("files/pdf"))
    pdfs.mkdir(parents=True, exist_ok=True)


def dev_run():

    # check if necessary and set up distribution entry
    if not Distribution.query.first():

        db.session.add(Distribution(**dict(in_progress=False)))
        db.session.commit()
