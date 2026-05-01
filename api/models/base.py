"""SQLAlchemy declarative base shared by all ORM models."""
from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base — import and subclass in every model."""
