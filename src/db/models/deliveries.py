"""`post_deliveries`"""

from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, pg_enum
from src.enums import DeliveryStatus

if TYPE_CHECKING:
    from src.db.models.posts import Post
    from src.db.models.users import User


class PostDelivery(Base):
    __tablename__ = "post_deliveries"

    post_id: Mapped[int] = mapped_column(
        sa.BigInteger, sa.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    tg_message_id: Mapped[int | None] = mapped_column(sa.BigInteger)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now()
    )
    sent_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True))
    status: Mapped[DeliveryStatus] = mapped_column(
        pg_enum(DeliveryStatus, "delivery_status"), index=True
    )

    post: Mapped[Post] = relationship(back_populates="deliveries")
    user: Mapped[User] = relationship(back_populates="deliveries")
