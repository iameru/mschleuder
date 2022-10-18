import os

from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment

from ms.config import Config
from ms.db.models import db

migrate = Migrate()
moment = Moment()


def create_app(test_config=None):

    if test_config:
        app = Flask(__name__, instance_path=test_config.get("INSTANCE_PATH"))
    else:
        app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)
    app.jinja_env.add_extension("jinja2.ext.loopcontrols")

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
    from ms.db.models import db
    from ms.distribution.views import distribution
    from ms.first_run import first_run
    from ms.history.views import history
    from ms.products.views import products
    from ms.settings.views import settings
    from ms.stations.views import stations
    from ms.utils import page_not_found

    app.register_blueprint(stations, url_prefix="/stations", options=_tmplt)
    app.register_blueprint(products, url_prefix="/products", options=_tmplt)
    app.register_blueprint(history, url_prefix="/", options=_tmplt)
    app.register_blueprint(settings, url_prefix="/settings", options=_tmplt)
    app.register_blueprint(distribution, url_prefix="/distribute", options=_tmplt)

    moment.init_app(app)
    db.init_app(app)

    migrate.init_app(app, db, render_as_batch=True)

    with app.app_context():
        first_run()

    app.context_processor(context_processor.inject)

    app.register_error_handler(404, page_not_found)

    return app
