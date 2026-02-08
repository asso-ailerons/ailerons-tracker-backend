"""Dashboard blueprint"""

from jinja_partials import render_partial
from jinja2 import TemplateNotFound
from flask import Blueprint, abort, current_app, render_template, url_for
from flask_htmx import HTMX
from flask_login import login_required
from db import db
from models.individual_model import Individual
# Local modules

dashboard = Blueprint(
    "dashboard", __name__, template_folder="templates", url_prefix="/dashboard"
)


@dashboard.get("/")
@login_required
def show():
    """Serve dashboard"""

    htmx = HTMX(current_app)

    try:
        if htmx:
            return render_partial("dashboard/dashboard.jinja")

        return render_template(
            "base_layout.jinja", view=url_for("portal.dashboard.show")
        )

    except TemplateNotFound as e:
        current_app.logger.error(e)
        abort(404)


@dashboard.get("/individuals")
@login_required
def show_table():
    try:
        htmx = HTMX(current_app)
        individuals = db.session.execute(db.select(Individual)).scalars().all()

        if htmx:
            return render_template(
                "dashboard/partials/individual_table.jinja", inds=individuals
            ), 200
        return render_template(
            "base_layout.jinja", view=url_for("portal.dashboard.show")
        )

    except TemplateNotFound as e:
        current_app.logger.error(e)
        abort(404)
