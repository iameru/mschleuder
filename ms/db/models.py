import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Computed

db = SQLAlchemy()


class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.utcnow)


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


class Station(TimestampMixin, db.Model):

    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    info = db.Column(db.String(128), nullable=True)
    delivery_order = db.Column(db.Integer, nullable=False)
    members_full = db.Column(db.Integer, nullable=False)
    members_half = db.Column(db.Integer, nullable=False)
    members_total = db.Column(db.Integer, Computed("members_full + members_half"))


class StationHistory(Station):

    __tablename__ = "stationshistory"

    saved = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)


class Organisation(db.Model):

    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    display_name = db.Column(db.String(128), unique=True, nullable=False)
    info = db.Column(db.String(128))

    header = db.Column(db.String(128), unique=True, nullable=True)
    footer = db.Column(db.String(128), unique=True, nullable=True)
