"""`user_subscriptions`"""

from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, pg_enum
from src.enums import SubscriptionStatus

if TYPE_CHECKING:
    from src.db.models.features import Feature
    from src.db.models.payments import Payment
    from src.db.models.users import User


class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, sa.ForeignKey("users.id", ondelete="RESTRICT"), index=True
    )
    feature_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("features.id", ondelete="RESTRICT"), index=True
    )
    payment_id: Mapped[int | None] = mapped_column(
        sa.BigInteger, sa.ForeignKey("payments.id", ondelete="RESTRICT")
    )
    status: Mapped[SubscriptionStatus] = mapped_column(
        pg_enum(SubscriptionStatus, "subscription_status"), index=True
    )
    starts_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), index=True)
    expiry_notified_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True))

    user: Mapped[User] = relationship(back_populates="subscriptions")
    feature: Mapped[Feature] = relationship(back_populates="subscriptions")
    payment: Mapped[Payment | None] = relationship(back_populates="subscriptions")
