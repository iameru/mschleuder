import datetime

from flask import render_template


def datetime_now():

    return datetime.datetime.utcnow()


def page_not_found(e):

    return render_template("404.html"), 404
