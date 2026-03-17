"""Upload CSV files blueprint"""

from pathlib import Path
from werkzeug.utils import secure_filename
from flask_login import login_required
from flask import Blueprint, abort, render_template, request, current_app, url_for
from flask_htmx import HTMX, make_response
from jinja2 import TemplateNotFound
from jinja_partials import render_partial
from pandas import Timedelta, pandas as pd

# Local modules
from ailerons_tracker_backend.models.individual_model import Individual
from ailerons_tracker_backend.models.csv_model import Csv
from ailerons_tracker_backend.db import db
from ailerons_tracker_backend.generator import generate
from ailerons_tracker_backend.errors import GeneratorError, MissingParamError


csv = Blueprint("csv", __name__, template_folder="templates", url_prefix="/csv")


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

        loc_df = pd.read_csv(
            loc_file, header=4, sep=",", decimal=".", on_bad_lines="error"
        )

        loc_df["record_timestamp"] = loc_df["Date"].apply(pd.to_datetime)

        loc_df = loc_df.filter(
            [
                "Most Likely Latitude",
                "Most Likely Longitude",
                "record_timestamp",
            ]
        )

        loc_df = loc_df.rename(
            columns={
                "Most Likely Latitude": "latitude",
                "Most Likely Longitude": "longitude",
            }
        )

        loc_df = loc_df.sort_values(by="record_timestamp")

        depth_df = pd.read_csv(depth_file, sep=",", decimal=".", on_bad_lines="error")

        depth_df["record_timestamp"] = depth_df["Day"] + " " + depth_df["Time"]

        depth_df["record_timestamp"] = depth_df["record_timestamp"].apply(
            pd.to_datetime
        )

        depth_df = depth_df.filter(["record_timestamp", "Depth"])
        depth_df = depth_df.rename(columns={"Depth": "depth"})

        depth_df = depth_df.sort_values(by="record_timestamp")

        df = pd.merge_asof(
            loc_df, depth_df, on="record_timestamp", tolerance=Timedelta(30, unit="min")
        )

        df = df.assign(csv_uuid=individual.csv.uuid, individual_id=individual.id)

        df.to_sql(name="record", con=db.engine, if_exists="append", index=False)

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
            return render_partial("csv_upload/csv_upload.jinja", ind=individual), 200

        return render_template(
            "base_layout.jinja", view=url_for("portal.csv.show", id=individual_id)
        )

    except TemplateNotFound as e:
        current_app.logger.error(e)
        abort(404)

    except MissingParamError as e:
        current_app.logger.error(e)
        return e, 400
