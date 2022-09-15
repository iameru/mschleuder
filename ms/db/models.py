import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Unit(db.Model):

    __tablename__ = "units"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    by_piece = db.Column(db.Boolean, nullable=False)
    shortname = db.Column(db.String(128), nullable=False)
    longname = db.Column(db.String(128), nullable=False)
    products = db.relationship("Product", backref="unit", lazy=True)


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    last_distribution = db.Column(db.DateTime, nullable=True)
    last_update = db.Column(db.DateTime, nullable=False)
    info = db.Column(db.String(128), nullable=True)

    unit_id = db.Column(db.Integer, db.ForeignKey("units.id"), nullable=False)

    def __init__(self, name, unit_id, info=None):

        self.name = name
        self.unit_id = unit_id
        self.info = info
        self.last_update = datetime.datetime.now()
