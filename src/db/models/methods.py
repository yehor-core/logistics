"""`methods`"""

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.db.models.payments import Payment


class Method(Base):
    __tablename__ = "methods"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.Text, unique=True)

    payments: Mapped[list[Payment]] = relationship(back_populates="method")
