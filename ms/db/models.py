import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)


class Unit(db.Model):

    __tablename__ = "units"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    by_piece = db.Column(db.Boolean, nullable=False)
    shortname = db.Column(db.String(128), unique=True, nullable=False)
    longname = db.Column(db.String(128), unique=True, nullable=False)
    products = db.relationship("Product", backref="unit", lazy=True)


class Product(TimestampMixin, db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    info = db.Column(db.String(128))
    last_distribution = db.Column(db.DateTime)
    unit_id = db.Column(db.Integer, db.ForeignKey("units.id"), nullable=False)


class Station(TimestampMixin, db.Model):

    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    info = db.Column(db.String(128), nullable=False)
    delivery_order = db.Column(db.Integer)
    members_full = db.Column(db.Integer, nullable=False)
    members_half = db.Column(db.Integer, nullable=False)


class StationHistory(Station):

    __tablename__ = "stationshistory"

    saved = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)


class Organisation(db.Model):

    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    display_name = db.Column(db.String(128), unique=True, nullable=False)
    info = db.Column(db.String(128))

    header = db.Column(db.String(128), unique=True, nullable=False)
    footer = db.Column(db.String(128), unique=True, nullable=False)
