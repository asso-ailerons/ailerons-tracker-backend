from flask import Blueprint
from sqlalchemy.orm import defer, noload

from ailerons_tracker_backend.db import db
from ailerons_tracker_backend.models.article_model import Article
from ailerons_tracker_backend.models.feature_models import LineGeojson
from ailerons_tracker_backend.models.individual_model import Individual
from ailerons_tracker_backend.models.record_model import Record
from ailerons_tracker_backend.models.schemas import (
    ArticleSchema,
    IndividualSchema,
    LineGeojsonSchema,
    RecordSchema,
)

data = Blueprint("data", __name__, template_folder="templates", url_prefix="/data")


@data.get("/individuals")
def get_individuals():
    individuals = (
        db.session.execute(
            db.select(Individual).options(
                noload(Individual.records),
                noload(Individual.line_feature),
                noload(Individual.csv),
                defer(Individual.feature_collection),
            )
        )
        .scalars()
        .all()
    )

    individual_schema = IndividualSchema()
    results = [individual_schema.dump(individual) for individual in individuals]

    return results


@data.get("/articles")
def get_articles():
    articles = db.session.execute(db.select(Article)).scalars().all()

    article_schema = ArticleSchema()
    results = [article_schema.dump(article) for article in articles]

    return results


@data.get("/records/point")
def get_points():
    records = db.session.execute(db.select(Record)).scalars().all()
    record_schema = RecordSchema()
    results = [record_schema.dump(record) for record in records]

    return results


@data.get("/records/geojson")
def get_geojson():
    features = db.session.execute(db.select(LineGeojson)).scalars().all()
    feature_schema = LineGeojsonSchema()
    results = [feature_schema.dump(feature) for feature in features]

    return results
