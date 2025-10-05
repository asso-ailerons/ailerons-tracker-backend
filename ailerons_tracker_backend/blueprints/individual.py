""" Individual data upload blueprint """

import flask_login
from wtforms.validators import ValidationError
from jinja_partials import render_partial
from flask import Blueprint, abort, flash, render_template, request, current_app, url_for
from jinja2 import TemplateNotFound
from werkzeug.datastructures import ImmutableMultiDict, iter_multi_items
from flask_htmx import HTMX, make_response

# Local modules
from ailerons_tracker_backend.db import db
from ailerons_tracker_backend.errors import MissingParamError
from ailerons_tracker_backend import cloudinary_client
from ailerons_tracker_backend.models.context_model import Context
from ailerons_tracker_backend.models.individual_model import Individual
from ailerons_tracker_backend.forms.individual_forms import ContextForm, IndividualForm
from ailerons_tracker_backend.models.picture_model import Picture


individual = Blueprint('individual', __name__,
                       template_folder='templates', url_prefix='/individual')


def upload_images(files: ImmutableMultiDict) -> list[str]:
    """ Parse and upload image files.

    Args:
        files (ImmutableMultiDict(str)): request files. """

    image_urls = []

    for k, v in iter_multi_items(files):
        image_url: str = cloudinary_client.upload(v.filename, v)
        image_urls.append(image_url)

    return image_urls


@individual.post('/edit')
@flask_login.login_required
def edit():
    """ Update specific rows in tables individual and context """

    try:
        individual_id = request.args.get("id", type=int)

        if individual_id is None:
            raise MissingParamError('id')

        ind = db.session.get_one(Individual, individual_id)

        ind_form = IndividualForm(obj=ind)
        context_form = ContextForm(obj=ind.context)

        ind_form.validate()
        context_form.validate()

        ind_form.populate_obj(ind)
        context_form.populate_obj(ind.context)

        if request.files:
            image_urls: list[str] = upload_images(request.files)
            for url in image_urls:
                ind.pictures.append(Picture(url=url))

        db.session.add(ind)
        db.session.commit()

        content = {
            'message': f'Successfully updated individual {ind.id}',
            'individual_data': ind,
            'context_data': ind.context}

        current_app.logger.info(content)

        flash(content['message'])

        return make_response(
            render_partial('dashboard/dashboard.jinja'),
            push_url=url_for('portal.dashboard.show')), 200

    except ValidationError as e:
        current_app.logger.error(e)
        return e, 400

    except postgrest.exceptions.APIError as e:
        current_app.logger.error(e.message)
        return e.message, 304

    except MissingParamError as e:
        current_app.logger.error(e)
        return e, 304


@individual.post('/create')
@flask_login.login_required
def create():
    """ Create new rows in tables individual and context """

    try:
        ind_form = IndividualForm()
        context_form = ContextForm()

        ind_form.validate()
        context_form.validate()

        individual = Individual(
            individual_name=ind_form.individual_name.data,
            sex=ind_form.sex.data,
            description=ind_form.description.data,
            context=Context(
                size=context_form.size.data,
                behavior=context_form.behavior.data,
                situation=context_form.situation.data,
                date=context_form.tag_date.data)
        )

        if request.files:
            image_urls: list[str] = upload_images(request.files)
            for url in image_urls:
                individual.pictures.append(Picture(url=url))

        db.session.add(individual)
        db.session.commit()

        content = {'message': f'Successfully created new individual {individual.id}',
                   'individual_data': individual,
                   'context_data': individual.context}

        current_app.logger.info(content)

        flash(content['message'])

        return make_response(
            render_partial(
                'dashboard/dashboard.jinja'),
            push_url=url_for('portal.dashboard.show')), 200

    except ValidationError as e:
        current_app.logger.error(e)
        return e, 400

    except postgrest.exceptions.APIError as e:
        current_app.logger.error(e.message)
        return e.message, 304


@individual.get('/create')
@flask_login.login_required
def show_create():
    """ Serve the view to create a new individual """

    htmx = HTMX(current_app)
    form = IndividualForm()

    try:
        if htmx:
            return render_partial('individual_infos/individual_infos.jinja', form=form)

        return render_template(
            'base_layout.jinja', view=url_for("portal.individual.show_create"))

    except TemplateNotFound as e:
        current_app.logger.error(e)
        abort(404)


@individual.get('/edit')
@flask_login.login_required
def show_edit():
    """ Serve the view to edit an individual """

    htmx = HTMX(current_app)
    form = IndividualForm()

    try:
        individual_id = request.args.get("id")

        if individual_id is None:
            raise MissingParamError('id')

        ind = db.session.get_one(Individual, individual_id)

        if htmx:
            return render_partial(
                'individual_infos/individual_infos_edit.jinja', ind=ind, form=form)

        current_app.logger.debug("YOOOO")
        return render_template(
            'base_layout.jinja',
            view=url_for("portal.individual.show_edit", id=individual_id))

    except TemplateNotFound as e:
        current_app.logger.error(e)
        abort(404)

    except MissingParamError as e:
        current_app.logger.error(e)
        return e, 400
