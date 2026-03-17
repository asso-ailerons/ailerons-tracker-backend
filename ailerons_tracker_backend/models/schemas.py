from marshmallow.fields import Float, Integer, String
from ailerons_tracker_backend.ma import ma

from ailerons_tracker_backend.models.article_model import Article
from ailerons_tracker_backend.models.context_model import Context
from ailerons_tracker_backend.models.csv_model import Csv
from ailerons_tracker_backend.models.feature_models import LineGeojson
from ailerons_tracker_backend.models.individual_model import Individual
from ailerons_tracker_backend.models.picture_model import Picture
from ailerons_tracker_backend.models.record_model import Record


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(ma.SQLAlchemySchema):
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)
        if field_name == "context":
            field_obj.data_key = "observationContext"


class CamelCaseAutoSchema(ma.SQLAlchemyAutoSchema):
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


class ArticleSchema(CamelCaseSchema):
    class Meta:
        model = Article

    title = String(required=True)
    content = String(required=True)
    publication_date = String(required=True)
    image_url = String(required=True)


class PictureSchema(CamelCaseAutoSchema):
    class Meta:
        model = Picture


class ContextSchema(CamelCaseSchema):
    class Meta:
        model = Context

    situation = String(required=True)
    size = Float(required=True)
    behavior = String(required=True)


class RecordSchema(CamelCaseSchema):
    class Meta:
        model = Record
        include_relationships = True

    longitude = Float(required=True)
    latitude = Float(required=True)
    individual_id = ma.auto_field(data_key="idIndividual", required=True)
    record_timestamp = String(required=True)
    depth = Integer()


class LineGeojsonSchema(CamelCaseSchema):
    class Meta:
        model = LineGeojson

    geojson = String(data_key="json")
    individual_id = ma.auto_field(data_key="idIndividual")


class CsvSchema(CamelCaseSchema):
    class Meta:
        model = Csv


class IndividualSchema(CamelCaseSchema):
    class Meta:
        model = Individual
        include_relationships = True

    id = ma.auto_field()
    created_at = String(required=True)
    individual_name = String(required=True)
    sex = String(required=True)
    common_name = String(required=True)
    binomial_name = String(required=True)
    description = String(required=True)
    context = ma.Nested(ContextSchema)
