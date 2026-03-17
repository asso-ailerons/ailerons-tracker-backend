"""Context model"""

from sqlalchemy import ForeignKey, Identity, Text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as mc
from sqlalchemy.orm import relationship as rel

from ailerons_tracker_backend.db import Base

# be careful not to cause circular imports when importing models that share a rel in the same file
# access with getitem directly rather than use imports


# pylint: disable=locally-disabled, not-callable


class Context(Base):
    """Context model."""

    __tablename__ = "context"

    id: Mapped[int] = mc(
        postgresql.BIGINT,
        Identity(start=1, always=True),
        primary_key=True,
        unique=True,
    )
    date: Mapped[str] = mc(postgresql.TIMESTAMP(timezone=True))
    individual: Mapped["Individual"] = rel(back_populates="context")
    individual_id: Mapped[int] = mc(
        postgresql.BIGINT, ForeignKey("individual.id")
    )
    situation: Mapped[str] = mc(Text)
    size: Mapped[int] = mc(postgresql.BIGINT)
    behavior: Mapped[str] = mc(Text)
