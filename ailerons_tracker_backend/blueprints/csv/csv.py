"""Upload CSV files blueprint"""

from pathlib import Path

from flask import (
    Blueprint,
    abort,
    current_app,
    render_template,
    request,
    url_for,
)
from flask_htmx import HTMX, make_response
from flask_login import login_required
from jinja2 import TemplateNotFound
from jinja_partials import render_partial
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from ailerons_tracker_backend.blueprints.csv.utils import (
    match_depths,
    open_csv,
    prepare_depths,
    prepare_locs,
)
from ailerons_tracker_backend.db import db
from ailerons_tracker_backend.errors import GeneratorError, MissingParamError
from ailerons_tracker_backend.generator import generate
from ailerons_tracker_backend.models.csv_model import Csv
from ailerons_tracker_backend.models.individual_model import Individual
from ailerons_tracker_backend.models.record_model import Record

csv = Blueprint(
    "csv", __name__, template_folder="templates", url_prefix="/csv"
)


def process_csv(
    loc_file: FileStorage,
    depth_file: FileStorage,
    csv_uuid: str,
    individual_id: int,
):
    loc_rows = open_csv(loc_file, 5)
    depth_rows = open_csv(depth_file, 0)

    loc_rows = prepare_locs(loc_rows)
    depth_rows = prepare_depths(depth_rows)

    return tuple(
        Record(
            record_timestamp=loc_row.timestamp,
            latitude=loc_row.latitude,
            longitude=loc_row.longitude,
            depth=match_depths(loc_row, depth_rows),
            csv_uuid=csv_uuid,
            individual_id=individual_id,
        )
        for loc_row in loc_rows
    )


@csv.post("/upload")
@login_required
def upload():
    """Parse a CSV file and insert data in DB"""

    try:
        individual_id = request.args.get("id", type=int)

        loc_file = request.files.get("loc_file")
        depth_file = request.files.get("depth_file")

        if any([loc_file is None, individual_id is None, depth_file is None]):
            raise MissingParamError("files or id")

        individual = db.session.get_one(Individual, individual_id)

        individual.csv = Csv(
            loc_file=secure_filename(Path(loc_file.filename).stem),
            depth_file=secure_filename(Path(depth_file.filename).stem),
        )

        db.session.commit()
        db.session.refresh(individual)

        records = process_csv(
            loc_file, depth_file, individual.csv.uuid, individual.id
        )

        db.session.add_all(records)
        db.session.commit()

        generate(individual, db)

        return make_response(
            render_partial("dashboard/dashboard.jinja"),
            push_url=url_for("portal.dashboard.show"),
        ), 200

    except GeneratorError as e:
        current_app.logger.error(e.message)
        return e.message, 500


@csv.get("/upload")
@login_required
def show():
    """Serve csv upload page"""

    try:
        htmx = HTMX(current_app)
        individual_id = request.args.get("id")

        if individual_id is None:
            raise MissingParamError("id")

        individual = db.session.get_one(Individual, individual_id)

        if htmx:
            return render_partial(
                "csv_upload/csv_upload.jinja", ind=individual
            ), 200

        return render_template(
            "base_layout.jinja",
            view=url_for("portal.csv.show", id=individual_id),
        )

    except TemplateNotFound as e:
        current_app.logger.error(e)
        abort(404)

    except MissingParamError as e:
        current_app.logger.error(e)
        return e, 400
