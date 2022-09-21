from flask import session
from wtforms.csrf.session import SessionCSRF
from wtforms.fields import FieldList, FormField, SelectField, SelectMultipleField
from wtforms_alchemy import ModelForm
from wtforms_alchemy.fields import QuerySelectMultipleField

from ms.config import Config
from ms.db.models import Organisation, Product, Station, Unit, db


class BaseForm(ModelForm):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = Config.CSRF_SECRET_KEY

        @property
        def csrf_context(self):
            return session


class UnitForm(BaseForm):
    class Meta:
        model = Unit

    # coerce by "True" as html doesnt return boolean
    by_piece = SelectField(
        "Einheit?",
        choices=[("True", "In Stück"), ("False", "In Gewicht")],
        coerce=lambda x: x == "True",
    )


class ProductForm(BaseForm):
    class Meta:
        model = Product

    units = QuerySelectMultipleField(
        "Units",
        query_factory=lambda: db.session.query(Unit),
        get_pk=lambda unit: unit.id,
        get_label=lambda unit: unit.longname,
    )


class StationForm(BaseForm):
    class Meta:
        model = Station

    exclude = ["members_total"]


class OrganisationForm(BaseForm):
    class Meta:
        model = Organisation
