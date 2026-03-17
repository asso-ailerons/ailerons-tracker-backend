"""Record Model"""

from uuid import UUID

from geojson import GeoJSON
from sqlalchemy import ForeignKey, Identity, Integer, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as mc
from sqlalchemy.orm import relationship as rel
from sqlalchemy.types import Uuid

from ailerons_tracker_backend.db import Base

# pylint: disable=locally-disabled, not-callable


class Record(Base):
    """Model for a GPS data record."""

    __tablename__ = "record"

    id: Mapped[int] = mc(
        postgresql.BIGINT,
        Identity(start=1, always=True),
        primary_key=True,
        unique=True,
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
    individual_id: Mapped[int] = mc(
        postgresql.BIGINT, ForeignKey("individual.id")
    )
    record_timestamp: Mapped[str] = mc(postgresql.TIMESTAMP(timezone=False))
