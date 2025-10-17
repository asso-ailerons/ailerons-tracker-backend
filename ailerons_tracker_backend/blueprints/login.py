"""Login blueprint"""

import flask_login
from flask_htmx import HTMX, make_response
from jinja2 import TemplateNotFound
from jinja_partials import render_partial
from flask import current_app, Blueprint, abort, render_template, url_for

# Local modules
from ailerons_tracker_backend.errors import EnvVarError
from ailerons_tracker_backend.models.user_model import User
from ailerons_tracker_backend.forms.login_form import LoginForm


login = Blueprint("login", __name__, template_folder="templates", url_prefix="/login")


@login.post("/")
def connect():
    """Connect to the app"""

    try:
        form = LoginForm()
        form.validate()

        if User.check_pwd(form.password.data):
            flask_login.login_user(User())

            return make_response(
                render_partial("dashboard/dashboard.jinja"),
                push_url=url_for("portal.dashboard.show"),
            ), 200

        return render_partial(
            "login/login_section.jinja", form=form, error_message=True
        ), 401

    except TemplateNotFound as e:
        current_app.logger.error(e)
        abort(404)

    except EnvVarError as e:
        current_app.logger.error(e)
        return e, 500


@login.get("/")
def show():
    """Retrieve the login section HTML template"""

    htmx = HTMX(current_app)
    form = LoginForm()

    try:
        if htmx:
            return render_partial("login/login_section.jinja", form=form), 200

        return render_template(
            "base_layout.jinja", view=url_for("portal.login.show"), form=form
        ), 200

    except TemplateNotFound as e:
        current_app.logger.error(e)
        abort(404)
