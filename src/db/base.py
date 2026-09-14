"""Declarative base shared by every model"""

from enum import StrEnum

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Every model inherits from this; `Base.metadata` is what Alembic autogenerates against"""

    metadata = sa.MetaData(naming_convention=NAMING_CONVENTION)


def pg_enum(enum_cls: type[StrEnum], name: str) -> sa.Enum:
    """Native Postgres enum storing member values, not member names"""
    return sa.Enum(
        enum_cls,
        name=name,
        native_enum=True,
        values_callable=lambda enum: [member.value for member in enum],
    )
