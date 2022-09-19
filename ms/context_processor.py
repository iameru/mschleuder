from ms.db.models import Organisation

from .dev import dev_data


def inject():
    context = {}

    context.update({"in_distribution": dev_data("in-distribution")})

    organisation = Organisation.query.get(1)
    context.update({"csa": organisation})

    return context
