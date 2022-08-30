import os

from flask import Flask

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

    if app.env == "development":

        from .dev import add_development_help

        add_development_help(app)

        app.config["SECRET_KEY"] = "DEVELOPMENT"

    _tmplt = {"template_folder": "templates"}

    from .stations.views import stations

    app.register_blueprint(stations, url_prefix="/stations", options=_tmplt)

    return app
