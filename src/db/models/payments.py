"""`payments`"""

from datetime import datetime
from typing import TYPE_CHECKING, Any

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, pg_enum
from src.enums import PaymentStatus

if TYPE_CHECKING:
    from src.db.models.methods import Method
    from src.db.models.subscriptions import UserSubscription
    from src.db.models.users import User


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, sa.ForeignKey("users.id", ondelete="RESTRICT"), index=True
    )
    method_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("methods.id", ondelete="RESTRICT")
    )
    amount: Mapped[int] = mapped_column(sa.BigInteger)
    status: Mapped[PaymentStatus] = mapped_column(pg_enum(PaymentStatus, "payment_status"))
    external_id: Mapped[str] = mapped_column(sa.Text, unique=True)
    payload: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now()
    )
    confirmed_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True))

    user: Mapped[User] = relationship(back_populates="payments")
    method: Mapped[Method] = relationship(back_populates="payments")
    subscriptions: Mapped[list[UserSubscription]] = relationship(back_populates="payment")
