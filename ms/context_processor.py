from .dev import dev_data


def inject_now():
    return {"now": datetime.utcnow()}


def inject():
    context = {}

    context.update({"in_distribution": dev_data("in-distribution")})
    context.update({"csa": dev_data("test-settings")})

    return context
