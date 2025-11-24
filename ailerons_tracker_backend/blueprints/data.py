from flask import Blueprint
from sqlalchemy.orm import defer, noload, selectinload

from ailerons_tracker_backend.db import db
from ailerons_tracker_backend.models.article_model import Article
from ailerons_tracker_backend.models.individual_model import Individual
from ailerons_tracker_backend.models.schemas import ArticleSchema, IndividualSchema

data = Blueprint("data", __name__, template_folder="templates", url_prefix="/data")


@data.get("/individuals")
def get_individuals():
    individuals = (
        db.session.execute(
            db.select(Individual).options(
                selectinload(Individual.context),
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
