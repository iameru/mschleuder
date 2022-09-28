from sqlalchemy import desc

from ms.db import query
from ms.db.models import Distribution, Organisation


def inject():
    context = {}

    dist = Distribution.current()
    context.update(dict(distribution_in_progress=dist.in_progress))

    organisation = Organisation.query.get(1)
    context.update({"csa": organisation})

    if context["distribution_in_progress"]:
        context.update({"in_distribution": query.distribution_overview(dist)})

    return context
