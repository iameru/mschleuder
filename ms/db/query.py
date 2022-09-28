from sqlalchemy import func

from ms.db.models import Distribution, Product, Share, Station, StationHistory, Unit, db


def distribution_overview(distribution: Distribution):
    fields = db.session.query(
        func.sum(Share.sum_total).label("total_sum"),
        Product.name,
        Product.id,
        func.avg(Share.single_full).label("single_full_average"),
        func.avg(Share.single_half).label("single_half_average"),
        Unit.longname.label("unit_name"),
        Unit.id.label("unit_id"),
    )
    joins = fields.join(Product).join(Unit)
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
