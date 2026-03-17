""" Portal blueprint """

from flask import Blueprint, abort, current_app, render_template, url_for
from jinja2 import TemplateNotFound

# Local modules
from ailerons_tracker_backend.blueprints.csv import csv
from ailerons_tracker_backend.blueprints.login import login
from ailerons_tracker_backend.blueprints.dashboard import dashboard
from ailerons_tracker_backend.blueprints.individual import individual

portal = Blueprint('portal', __name__,
                   template_folder='templates',
                   static_folder='static',
                   url_prefix='/portal')

portal.register_blueprint(dashboard)
portal.register_blueprint(csv)
portal.register_blueprint(login)
portal.register_blueprint(individual)


@portal.route('/')
def show():
    """ Serve portal """

    try:
        return render_template('base_layout.jinja', view=url_for("portal.dashboard.show"))

    except TemplateNotFound as e:
        current_app.logger.error(e)
        abort(404)
