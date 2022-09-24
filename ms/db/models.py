import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Computed, desc

from ms.utils import datetime_now

db = SQLAlchemy()


class TimestampMixin(object):

    # This Mixin generates TimeStamps
    created = db.Column(db.DateTime, nullable=False, default=datetime_now)
    updated = db.Column(db.DateTime, nullable=True, onupdate=datetime_now)


class Unit(db.Model):

    __tablename__ = "units"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    by_piece = db.Column(db.Boolean, nullable=False)
    shortname = db.Column(db.String(128), unique=True, nullable=False)
    longname = db.Column(db.String(128), unique=True, nullable=False)


product_units = db.Table(
    "product_units",
    db.Column("unit_id", db.Integer, db.ForeignKey("units.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True),
)


class Product(TimestampMixin, db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    info = db.Column(db.String(128))
    last_distribution = db.Column(db.DateTime)
    units = db.relationship(
        "Unit",
        secondary=product_units,
        lazy="subquery",
        backref=db.backref("products", lazy="subquery"),
    )


class StationHistory(db.Model):

    __tablename__ = "stationshistory"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    info = db.Column(db.String(128), nullable=True)
    delivery_order = db.Column(db.Integer, nullable=False)
    members_full = db.Column(db.Integer, nullable=False)
    members_half = db.Column(db.Integer, nullable=False)
    members_total = db.Column(db.Integer, nullable=False)

    time_archived = db.Column(db.DateTime, default=datetime_now)
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=True)

    distribution_id = db.Column(
        db.Integer, db.ForeignKey("distribution.id"), nullable=False
    )


class Station(TimestampMixin, db.Model):

    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    info = db.Column(db.String(128), nullable=True)
    delivery_order = db.Column(db.Integer, nullable=False)
    members_full = db.Column(db.Integer, nullable=False)
    members_half = db.Column(db.Integer, nullable=False)
    members_total = db.Column(db.Integer, Computed("members_full + members_half"))

    def archive(self, dist_id):

        # get non PK data into a dict and commit to History
        table = self.__table__
        non_pk_columns = [k for k in table.columns.keys() if k not in table.primary_key]
        data = {c: getattr(self, c) for c in non_pk_columns}

        # add corresponding DIST ID
        data["distribution_id"] = dist_id

        archive_obj = StationHistory(**data)
        db.session.add(archive_obj)
        db.session.commit()


class Organisation(db.Model):

    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    display_name = db.Column(db.String(128), unique=True, nullable=False)
    info = db.Column(db.String(128))

    header = db.Column(db.String(128), unique=True, nullable=True)
    footer = db.Column(db.String(128), unique=True, nullable=True)


class Distribution(TimestampMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    in_progress = db.Column(db.Boolean, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime_now)
    stations = db.relationship("StationHistory", backref="distribution", lazy=True)

    def current():

        return Distribution.query.order_by(desc(Distribution.id)).first()
