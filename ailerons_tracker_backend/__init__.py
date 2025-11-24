"""Configuration and factory for the app"""

__version__ = "0.7"

import os
import flask_login
from flask import Flask, current_app, render_template, url_for
from flask_cors import CORS
from flask_htmx import HTMX, make_response
from flask_login import FlaskLoginClient
from flask_wtf import CSRFProtect
from jinja_partials import register_extensions, render_partial

from ailerons_tracker_backend.blueprints.data import data
from ailerons_tracker_backend.blueprints.portal import portal
from ailerons_tracker_backend.db import db, migrate
from ailerons_tracker_backend.forms.login_form import LoginForm
from ailerons_tracker_backend.models.user_model import User
from ailerons_tracker_backend.ma import ma


def create_app(test_config=None):
    """Create an instance of the app"""

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.getenv("APP_SECRET_KEY"),
        # URI can be found in Supabase dashboard, pwd can be reset there as well
        SQLALCHEMY_DATABASE_URI=f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PWD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}",
        SERVER_NAME="127.0.0.1:5000",
        APPLICATION_ROOT="/",
    )
    db.init_app(app)
    migrate.init_app(app, db)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)

    except OSError:
        pass

    # Enable CORS because HTMX requests are sent as "OPTIONS"
    # by modern browsers which causes CORS errors
    CORS(app)

    # Enable Cross Site Request Forgery protection in forms
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Enable Jinja Partials, which allows us to render HTML fragments instead of pages
    register_extensions(app)

    # Initialize logging manager
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user):
        app.logger.info(f"Logged: {user}")
        return User()

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        form = LoginForm()
        htmx = HTMX(current_app)

        if htmx:
            return make_response(
                render_partial("login/login_section.jinja", form=form),
                push_url=url_for("portal.login.show"),
            ), 302

        return render_template(
            "base_layout.jinja", view=url_for("portal.login.show")
        ), 302

    app.test_client_class = FlaskLoginClient
    ma.init_app(app)

    # Register a blueprint => blueprint routes are now active
    app.register_blueprint(portal)

    app.logger.info(app.url_map)

    return app
