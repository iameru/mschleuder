import datetime


def datetime_now():

    # remove seconds and  microseconds
    return datetime.datetime.utcnow().replace(microsecond=0, second=0)
