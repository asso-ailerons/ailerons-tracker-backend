"""SQLAlchemy DB interface"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate


class Base(DeclarativeBase):
    """Base class that can be customized if needed"""


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
