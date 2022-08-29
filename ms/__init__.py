import json
import os

from flask import Flask
from testmark import parse

from ms.config import Config


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if not test_config:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except FileExistsError:
        pass

    @app.route("/")
    def try_testmark():

        dev_data = parse("ms/dev.md")
        stations_current = dev_data["products-historical"]
        data = json.loads(stations_current)
        return data

    if app.env == "development":

        from .dev import add_development_help

        add_development_help(app)

    return app
