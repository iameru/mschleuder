import datetime

from flask import session
from flask_sqlalchemy import SQLAlchemy
from wtforms.csrf.session import SessionCSRF
from wtforms_alchemy import ModelForm

from ms.config import Config

db = SQLAlchemy()


class BaseForm(ModelForm):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = Config.CSRF_SECRET_KEY

        @property
        def csrf_context(self):
            return session


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


class ProductForm(BaseForm):
    class Meta:
        model = Product
