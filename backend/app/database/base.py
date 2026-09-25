"""Declarative base for all ORM models (Database Integration task).

Usage in `app/models/` once the task is done:

    from app.database.base import Base

    class Prediction(Base):
        __tablename__ = "predictions"
        ...
"""
from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class every ORM model inherits from."""