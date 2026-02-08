"""GeoJSON Features Models"""

from geojson import Feature, GeoJSON, Point, LineString
from sqlalchemy import ForeignKey, Identity
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column as mc, relationship as rel
from errors import GeneratorLineError, GeneratorPointError
from models.individual_model import Individual
from models.record_model import Record
from db import db

# pylint: disable=locally-disabled, not-callable


def to_point_feature(record: Record, individual: Individual) -> GeoJSON:
    """Create a Point GeoJSON Feature."""

    properties = {
        "individual_id": individual.id,
        "individual_name": individual.individual_name,
        "timestamp": str(record.record_timestamp),
    }

    feature = Feature(
        geometry=Point((record.longitude, record.latitude)), properties=properties
    )

    if feature.is_valid:
        return feature

    raise GeneratorPointError(feature)


class LineGeojson(db.Model):
    """Model for Line."""

    id: Mapped[int] = mc(
        postgresql.BIGINT, Identity(start=1, always=True), primary_key=True, unique=True
    )

    individual_id: Mapped[int] = mc(postgresql.BIGINT, ForeignKey("individual.id"))

    individual: Mapped["Individual"] = rel(back_populates="line_feature")

    geojson: Mapped[GeoJSON] = mc(postgresql.JSON)

    @classmethod
    def to_line_feature(
        cls, individual_records: list[Record], individual: Individual
    ) -> GeoJSON:
        """Create a LineString GeoJSON Feature."""

        properties = {
            "individual_id": individual.id,
            "individual_name": individual.individual_name,
            "timestamps": list(
                map(lambda record: str(record.record_timestamp), individual_records)
            ),
        }

        coordinates = list(
            map(lambda record: (record.longitude, record.latitude), individual_records)
        )

        feature = Feature(geometry=LineString(coordinates), properties=properties)

        if feature.is_valid:
            return feature

        raise GeneratorLineError(feature)
