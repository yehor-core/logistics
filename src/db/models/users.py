"""`users`"""

from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.db.models.deliveries import PostDelivery
    from src.db.models.payments import Payment
    from src.db.models.settings import UserSettings
    from src.db.models.subscriptions import UserSubscription
    from src.db.models.user_sources import UserSource


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    tg_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now()
    )
    card_token: Mapped[str | None] = mapped_column(sa.Text)
    wallet_id: Mapped[str | None] = mapped_column(sa.Text)

    settings: Mapped[UserSettings] = relationship(back_populates="user")
    sources: Mapped[list[UserSource]] = relationship(back_populates="user")
    payments: Mapped[list[Payment]] = relationship(back_populates="user")
    subscriptions: Mapped[list[UserSubscription]] = relationship(back_populates="user")
    deliveries: Mapped[list[PostDelivery]] = relationship(back_populates="user")
