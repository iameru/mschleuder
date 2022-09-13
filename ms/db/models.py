import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    by_piece = db.Column(db.Boolean, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, by_piece):

        self.name = name
        self.by_piece = by_piece
        self.last_update = datetime.datetime.now()
