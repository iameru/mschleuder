import datetime

from . import db


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    last_update = db.Column(db.DateTime, nullable=False)

    def __init__(self, name):

        self.name = name
        self.last_update = datetime.datetime.now()
