"""`features`"""

from datetime import timedelta
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.db.models.subscriptions import UserSubscription


class Feature(Base):
    __tablename__ = "features"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.Text)
    is_enabled: Mapped[bool] = mapped_column(sa.Boolean, server_default=sa.true())
    price: Mapped[int] = mapped_column(sa.BigInteger)
    duration: Mapped[timedelta] = mapped_column(sa.Interval)

    subscriptions: Mapped[list[UserSubscription]] = relationship(back_populates="feature")
