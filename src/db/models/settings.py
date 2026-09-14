"""`user_settings`"""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config import settings
from src.db.base import Base

if TYPE_CHECKING:
    from src.db.models.users import User


class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    is_enabled: Mapped[bool] = mapped_column(sa.Boolean, server_default=sa.true())
    price_per_km: Mapped[Decimal] = mapped_column(
        sa.Numeric(10, 2), default=settings.default_price_per_km
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()
    )

    user: Mapped[User] = relationship(back_populates="settings")
