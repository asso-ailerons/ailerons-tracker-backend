"""Record Model"""

from uuid import UUID
from geojson import GeoJSON
from sqlalchemy import ForeignKey, Identity, Integer, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.types import Uuid
from sqlalchemy.orm import Mapped, mapped_column as mc, relationship as rel
from db import db

# pylint: disable=locally-disabled, not-callable


class Record(db.Model):
    """Model for a GPS data record."""

    id: Mapped[int] = mc(
        postgresql.BIGINT, Identity(start=1, always=True), primary_key=True, unique=True
    )

    created_at: Mapped[str] = mc(
        postgresql.TIMESTAMP(timezone=True), default=func.now()
    )

    latitude: Mapped[int] = mc(postgresql.FLOAT)

    longitude: Mapped[int] = mc(postgresql.FLOAT)

    point_feature: Mapped["GeoJSON"] = mc(postgresql.JSON, nullable=True)

    depth: Mapped[int] = mc(Integer, nullable=True)

    csv: Mapped["Csv"] = rel(back_populates="records")

    csv_uuid: Mapped[UUID] = mc(Uuid, ForeignKey("csv.uuid"))

    individual: Mapped["Individual"] = rel(back_populates="records")

    individual_id: Mapped[int] = mc(postgresql.BIGINT, ForeignKey("individual.id"))

    record_timestamp: Mapped[str] = mc(postgresql.TIMESTAMP(timezone=False))
