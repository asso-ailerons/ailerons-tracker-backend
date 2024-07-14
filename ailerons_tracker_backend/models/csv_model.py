from typing import List
from uuid import uuid4
from sqlalchemy import UUID, ForeignKey, Text, func
from sqlalchemy.dialects import postgresql
from ailerons_tracker_backend.db import db
from sqlalchemy.orm import Mapped, mapped_column as mc, relationship as rel


class Csv(db.Model):
    uuid: Mapped[UUID] = mc(UUID(as_uuid=True),
                            primary_key=True,
                            default=uuid4(),
                            unique=True)

    created_at: Mapped[str] = mc(postgresql.TIMESTAMP(timezone=True),
                                 default=func.now())

    loc_file: Mapped[str] = mc(Text)

    depth_file: Mapped[str] = mc(Text)

    records: Mapped[List['Record']] = rel(back_populates='csv',
                                          cascade="all, delete-orphan")

    individual_id: Mapped[int] = mc(postgresql.BIGINT,
                                    ForeignKey('individual.id'))

    individual: Mapped['Individual'] = rel(back_populates='csv')
