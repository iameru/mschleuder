from flask import session
from wtforms.csrf.session import SessionCSRF
from wtforms.fields import SelectField
from wtforms_alchemy import ModelForm

from ms.config import Config
from ms.db.models import Organisation, Product, Station, Unit


class BaseForm(ModelForm):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = Config.CSRF_SECRET_KEY

        @property
        def csrf_context(self):
            return session


class ProductForm(BaseForm):
    class Meta:
        model = Product

    unit_id = SelectField("Einheit", coerce=int)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.unit_id.choices = [(unit.id, unit.longname) for unit in Unit.query.all()]


class StationForm(BaseForm):
    class Meta:
        model = Station


class UnitForm(BaseForm):
    class Meta:
        model = Unit

    # coerce by "True" as html doesnt return boolean
    by_piece = SelectField(
        "Einheit?",
        choices=[("True", "In Stück"), ("False", "In Gewicht")],
        coerce=lambda x: x == "True",
    )


class OrganisationForm(BaseForm):
    class Meta:
        model = Organisation
