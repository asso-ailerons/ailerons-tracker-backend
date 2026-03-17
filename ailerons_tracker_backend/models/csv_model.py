"""CSV model"""

from typing import List
from uuid import uuid4

from sqlalchemy import UUID, ForeignKey, Text, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as mc
from sqlalchemy.orm import relationship as rel

from ailerons_tracker_backend.db import Base

# pylint: disable=locally-disabled, not-callable


class Csv(Base):
    """CSV model."""

    __tablename__ = "csv"

    uuid: Mapped[UUID] = mc(
        UUID(as_uuid=True), primary_key=True, default=uuid4(), unique=True
    )
    created_at: Mapped[str] = mc(
        postgresql.TIMESTAMP(timezone=True), default=func.now()
    )
    loc_file: Mapped[str] = mc(Text)
    depth_file: Mapped[str] = mc(Text)
    records: Mapped[List["Record"]] = rel(
        back_populates="csv", cascade="all, delete-orphan"
    )
    individual_id: Mapped[int] = mc(
        postgresql.BIGINT, ForeignKey("individual.id")
    )
    individual: Mapped["Individual"] = rel(back_populates="csv")
