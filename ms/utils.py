import datetime

from flask import render_template


def datetime_now():

    # remove seconds and  microseconds
    return datetime.datetime.utcnow().replace(microsecond=0, second=0)


def page_not_found(e):
    return render_template("404.html"), 404
