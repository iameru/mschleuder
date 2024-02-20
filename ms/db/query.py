import datetime
from typing_extensions import NamedTuple
from typing import List

from sqlalchemy import func

from ms.db.models import Distribution, Product, Share, Station, StationHistory, Unit, db


# hotfix rotten code
class DistQueryResult(NamedTuple):
    total_sum: int
    name: str
    product_id: int
    dist_id: int
    unit_name: str
    unit_shortname: str
    unit_id: int
    info: str
def distribution_overview(distribution: Distribution) -> List[DistQueryResult]:
    ## hotfix

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
    result = filters.all()
    data = [
        DistQueryResult(
            total_sum=item[0],
            name=item[1],
            product_id=item[2],
            dist_id=item[3],
            unit_name=item[4],
            unit_shortname=item[5],
            unit_id=item[6],
            info=item[7],
        )
        for item in result
    ]
    return data
    # return [dict(item) for item in filters.all()]


# hotfix rotten code
class ProductDetailsQueryResult(NamedTuple):
    name: str
    total_sum: int
    Share: Share
    unit_name: str
def product_details(distribution_id, product_id, unit_id) -> List[ProductDetailsQueryResult]:

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

    result = filters.all()
    data = [
        ProductDetailsQueryResult(
            name=item[0],
            total_sum=item[1],
            Share=item[2],
            unit_name=item[3],
        )
        for item in result
    ]
    return data
    # return [dict(item) for item in filters.all()]


def show_recent_distribution(product, unit, how_many_distributions=6):

    time_limit = datetime.datetime.utcnow() - datetime.timedelta(weeks=8)

    # Dist query
    query = (
        db.session.query(Distribution.id)
        .filter(
            Distribution.in_progress == False,
            Distribution.finalized == True,
            Distribution.date_time > time_limit,
        )
        .order_by(Distribution.id.desc())
    )
    distribution_ids = [dist[0] for dist in query.all()[:how_many_distributions]]

    result = {}
    for station in Station.query.all():

        station_history_ids = [station.id for station in station.history]

        query = (
            db.session.query(
                Share.single_full.label("single_full"),
                Share.single_half.label("single_half"),
                Distribution.date_time.label("share_date"),
            )
            .join(Distribution)
            .filter(
                Share.product_id == product.id,
                Share.unit_id == unit.id,
                Share.distribution_id.in_(distribution_ids),
                Share.stationhistory_id.in_(station_history_ids),
            )
            .order_by(Distribution.date_time.desc())
        )
        result[station] = query.all()

    return result


def product_history(product_id, station_id=None, how_many_distributions=1):
    ### WIP!!! unused.

    product = Product.query.get_or_404(product_id)
    if station_id:
        station = Station.query.get_or_404(station_id)
        station_history_ids = [station.id for station in station.history]
    else:
        stations = Station.query.all()
        station_history_ids = []
        for station in stations:
            [station_history_ids.append(history.id) for history in station.history]

    query = (
        db.session.query(Distribution.id)
        .filter(Distribution.in_progress == False, Distribution.finalized == True)
        .order_by(Distribution.id.desc())
    )
    distribution_ids = [dist[0] for dist in query.all()[:how_many_distributions]]

    query = db.session.query(
        func.sum(Share.single_full).label("single_full"),
        func.sum(Share.single_half).label("single_half"),
    ).filter(
        Share.product_id == product.id,
        Share.distribution_id.in_(distribution_ids),
        Share.stationhistory_id.in_(station_history_ids),
    )

    query_result = query.one()
    # this would calculate the AVERAGE
    result = [value / len(distribution_ids) for value in query_result if value]
