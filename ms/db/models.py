from decimal import Decimal
from typing import Union

from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel
from sqlalchemy import Computed, MetaData, desc
from sqlalchemy.orm.exc import DetachedInstanceError
from sqlalchemy.types import Float

from ms.utils import datetime_now

db = SQLAlchemy()


class ReprMixin(object):
    def __repr__(self):
        return self._repr(id=self.id)

    def _repr(self, **fields):

        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f"{key}={field!r}")
            except DetachedInstanceError:
                field_string.append(f"{key}=DetachedInstanceError")
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"


class TimestampMixin(object):

    # This Mixin generates TimeStamps
    created = db.Column(db.DateTime, nullable=False, default=datetime_now)
    updated = db.Column(db.DateTime, nullable=True, onupdate=datetime_now)


class Unit(db.Model, ReprMixin):

    __tablename__ = "units"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    by_piece = db.Column(db.Boolean, nullable=False)
    shortname = db.Column(db.String(128), unique=True, nullable=False)
    longname = db.Column(db.String(128), unique=True, nullable=False)
    shares = db.relationship("Share", backref="unit", lazy=True)

    def __repr__(self):
        return self._repr(id=self.id, shortname=self.shortname, by_piece=self.by_piece)


product_units = db.Table(
    "product_units",
    db.Column("unit_id", db.Integer, db.ForeignKey("units.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True),
)


class Product(TimestampMixin, db.Model, ReprMixin):

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
    shares = db.relationship("Share", backref="product", lazy=True)

    def __repr__(self):
        return self._repr(id=self.id, name=self.name)


class StationHistory(db.Model, ReprMixin):

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
    shares = db.relationship("Share", backref="stationhistory", lazy=True)

    distribution_id = db.Column(
        db.Integer, db.ForeignKey("distribution.id"), nullable=False
    )
    station_id = db.Column(db.Integer, db.ForeignKey("stations.id"), nullable=False)

    def __repr__(self):
        return self._repr(id=self.id, name=self.name, members_total=self.members_total)


class Station(TimestampMixin, db.Model, ReprMixin):

    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    info = db.Column(db.String(128), nullable=True)
    delivery_order = db.Column(db.Integer, nullable=False)
    members_full = db.Column(db.Integer, nullable=False)
    members_half = db.Column(db.Integer, nullable=False)
    members_total = db.Column(db.Integer, Computed("members_full + members_half"))
    history = db.relationship("StationHistory", backref="current", lazy=True)

    def archive_all(dist_id):

        archive_time = datetime_now()

        for station in Station.query.all():
            station.archive(dist_id, archive_time)

    def archive(self, dist_id, archive_time=None):

        # get non PK data into a dict and commit to History
        table = self.__table__
        non_pk_columns = [k for k in table.columns.keys() if k not in table.primary_key]
        data = {c: getattr(self, c) for c in non_pk_columns}

        # add corresponding DIST ID
        data["distribution_id"] = dist_id
        data["station_id"] = self.id

        if archive_time:
            data["time_archived"] = archive_time

        archive_obj = StationHistory(**data)

        db.session.add(archive_obj)
        db.session.commit()

    def __repr__(self):
        return self._repr(id=self.id, name=self.name, members_total=self.members_total)


class Organisation(db.Model, ReprMixin):

    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    display_name = db.Column(db.String(128), unique=True, nullable=False)
    info = db.Column(db.String(128))

    header = db.Column(db.String(128), unique=True, nullable=True)
    footer = db.Column(db.String(128), unique=True, nullable=True)

    def __repr__(self):
        return self._repr(id=self.id, name=self.name)


class Distribution(TimestampMixin, db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    in_progress = db.Column(db.Boolean, nullable=False)
    finalized = db.Column(db.Boolean, default=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime_now)
    stations = db.relationship("StationHistory", backref="distribution", lazy=True)
    shares = db.relationship("Share", backref="dist", lazy=True)

    def current():

        return Distribution.query.order_by(desc(Distribution.id)).first()

    def __repr__(self):
        return self._repr(id=self.id, in_progress=self.in_progress)


class Share(TimestampMixin, db.Model, ReprMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    stationhistory_id = db.Column(
        db.Integer, db.ForeignKey("stationshistory.id"), nullable=False
    )
    distribution_id = db.Column(
        db.Integer, db.ForeignKey("distribution.id"), nullable=False
    )
    unit_id = db.Column(db.Integer, db.ForeignKey("units.id"), nullable=False)
    single_full = db.Column(
        Float(asdecimal=True, precision=8, decimal_return_scale=None)
    )
    single_half = db.Column(
        Float(asdecimal=True, precision=8, decimal_return_scale=None)
    )
    single_total = db.Column(db.Float, Computed("single_full + single_half"))
    sum_full = db.Column(Float(asdecimal=True, precision=8, decimal_return_scale=None))
    sum_half = db.Column(Float(asdecimal=True, precision=8, decimal_return_scale=None))
    sum_total = db.Column(db.Float, Computed("sum_full + sum_half"))

    def __repr__(self):
        return self._repr(
            id=self.id,
            distribution_id=self.distribution_id,
            sum_total=self.sum_total,
            product_id=self.product_id,
            unit_id=self.unit_id,
            stationhistory_id=self.stationhistory_id,
        )


class ShareModel(BaseModel):

    single_full: Decimal
    single_half: Decimal
    sum_full: Decimal
    sum_half: Decimal
