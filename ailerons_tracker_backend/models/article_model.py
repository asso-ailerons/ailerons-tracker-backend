"""Article Model"""

from sqlalchemy import Boolean, Identity, Text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped
from ailerons_tracker_backend.db import db
from sqlalchemy.orm import mapped_column as mc


class Article(db.Model):
    """Model for a news article."""

    id: Mapped[int] = mc(
        postgresql.BIGINT, Identity(start=1, always=True), primary_key=True, unique=True
    )
    title: Mapped[str] = mc(Text)
    content: Mapped[str] = mc(Text)
    image_url: Mapped[str] = mc(Text)
    published: Mapped[bool] = mc(Boolean)
    archived: Mapped[bool] = mc(Boolean)
    publication_date: Mapped[str] = mc(postgresql.TIMESTAMP(timezone=True))
