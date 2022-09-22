from ms.db.models import Distribution, Organisation


def inject():
    context = {}

    context.update(dict(distribution_in_progress=Distribution.query.get(1).in_progress))

    organisation = Organisation.query.get(1)

    context.update({"csa": organisation})

    return context
