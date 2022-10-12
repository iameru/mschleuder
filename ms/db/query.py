from sqlalchemy import func

from ms.db.models import Distribution, Product, Share, Station, StationHistory, Unit, db


def distribution_overview(distribution: Distribution):
    fields = db.session.query(
        func.sum(Share.sum_total).label("total_sum"),
        Product.name,
        Product.id.label("product_id"),
        Distribution.id.label("dist_id"),
        Unit.longname.label("unit_name"),
        Unit.shortname.label("unit_shortname"),
        Unit.id.label("unit_id"),
        Share.information.label("info"),
    )
    joins = fields.join(Product).join(Unit).join(Distribution)
    groups = joins.group_by(Share.product_id, Share.unit_id)
    filters = groups.filter(
        Share.distribution_id == distribution.id,
        Share.unit_id == Unit.id,
    )
    return [dict(item) for item in filters.all()]


def product_details(distribution_id, product_id, unit_id):

    fields = db.session.query(
        Product.name.label("product_name"),
        func.sum(Share.sum_total).label("total_sum"),
        Share,
        Unit.longname.label("unit_name"),
    )
    joins = fields.join(Product).join(StationHistory).join(Unit)
    groups = joins.group_by(Share.stationhistory_id, StationHistory.id)
    filters = groups.filter(
        Share.distribution_id == distribution_id,
        Share.product_id == product_id,
        Share.unit_id == unit_id,
    )

    return [dict(item) for item in filters.all()]
