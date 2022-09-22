from ms.db.models import Organisation


def inject():
    context = {}

    context.update({"in_distribution": None})

    organisation = Organisation.query.get(1)

    context.update({"csa": organisation})

    return context
