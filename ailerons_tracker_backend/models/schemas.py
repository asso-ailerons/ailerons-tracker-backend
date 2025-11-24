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


class ArticleSchema(CamelCaseAutoSchema):
    class Meta:
        model = Article

    published = ma.auto_field(load_only=True)
    archived = ma.auto_field(load_only=True)


class PictureSchema(CamelCaseAutoSchema):
    class Meta:
        model = Picture


class ContextSchema(CamelCaseAutoSchema):
    class Meta:
        model = Context

    id = ma.auto_field(load_only=True)
    date = ma.auto_field(load_only=True)


class RecordSchema(CamelCaseSchema):
    class Meta:
        model = Record


class LineGeojsonSchema(CamelCaseSchema):
    class Meta:
        model = LineGeojson


class CsvSchema(CamelCaseSchema):
    class Meta:
        model = Csv


class IndividualSchema(CamelCaseSchema):
    def rename_context():
        def on_bind_field(self, field_name, field_obj):
            if field_name == "context":
                field_obj.data_key = "observationContext"

    class Meta:
        model = Individual
        include_relationships = True

    id = ma.auto_field()
    created_at = ma.auto_field()
    individual_name = ma.auto_field()
    sex = ma.auto_field()
    common_name = ma.auto_field()
    binomial_name = ma.auto_field()
    description = ma.auto_field()
    context = ma.Nested(ContextSchema)
