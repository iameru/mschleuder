import os

from flask import Flask

from ms.config import Config


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    if test_config:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except FileExistsError:
        pass

    if app.debug:

        from .dev import add_development_help

        add_development_help(app)

    _tmplt = {"template_folder": "templates"}

    from ms import context_processor
    from ms.db.models import Product, db
    from ms.history.views import history
    from ms.products.views import products
    from ms.settings.views import settings
    from ms.stations.views import stations

    app.register_blueprint(stations, url_prefix="/stations", options=_tmplt)
    app.register_blueprint(products, url_prefix="/products", options=_tmplt)
    app.register_blueprint(history, url_prefix="/", options=_tmplt)
    app.register_blueprint(settings, url_prefix="/settings", options=_tmplt)

    db.init_app(app)
    if not test_config:
        with app.app_context():
            db.create_all()

    app.context_processor(context_processor.inject)

    return app
