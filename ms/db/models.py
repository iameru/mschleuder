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
    shortname = db.Column(db.String(128), nullable=False)
    longname = db.Column(db.String(128), nullable=False)
    products = db.relationship("Product", backref="unit", lazy=True)


class Product(TimestampMixin, db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    info = db.Column(db.String(128))
    last_distribution = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime, nullable=False)

    unit_id = db.Column(db.Integer, db.ForeignKey("units.id"), nullable=False)

    def __init__(self, name, unit_id, info=None):

        self.name = name
        self.unit_id = unit_id
        self.info = info
        self.last_update = datetime.datetime.now()


class Station(TimestampMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    info = db.Column(db.String(128), nullable=False)
    delivery_order = db.Column(db.Integer)
    members_full = db.Column(db.Integer, nullable=False)
    members_half = db.Column(db.Integer, nullable=False)

    def __init__(self, **k):

        self.name = k["name"]
        self.info = k["info"]
        self.delivery_order = k["delivery_order"]
        self.members_full = k["members_full"]
        self.members_half = k["members_half"]
