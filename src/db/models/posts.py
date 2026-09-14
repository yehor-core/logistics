"""`posts`"""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, pg_enum
from src.enums import PostStatus

if TYPE_CHECKING:
    from src.db.models.deliveries import PostDelivery
    from src.db.models.sources import Source


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        sa.UniqueConstraint("source_id", "external_id"),
        sa.Index("ix_posts_fingerprint_published_at", "fingerprint", "published_at"),
    )

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    source_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("sources.id", ondelete="CASCADE")
    )
    external_id: Mapped[int] = mapped_column(sa.BigInteger)
    fingerprint: Mapped[str | None] = mapped_column(sa.String(64))
    raw_text: Mapped[str] = mapped_column(sa.Text)
    from_location: Mapped[str | None] = mapped_column(sa.Text)
    to_location: Mapped[str | None] = mapped_column(sa.Text)
    price: Mapped[Decimal | None] = mapped_column(sa.Numeric(12, 2))
    price_per_km: Mapped[Decimal | None] = mapped_column(sa.Numeric(10, 2))
    published_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    parsed_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True))
    status: Mapped[PostStatus] = mapped_column(pg_enum(PostStatus, "post_status"), index=True)
    from_norm: Mapped[str | None] = mapped_column(sa.Text)
    to_norm: Mapped[str | None] = mapped_column(sa.Text)
    duplicate_of_id: Mapped[int | None] = mapped_column(
        sa.BigInteger, sa.ForeignKey("posts.id", ondelete="SET NULL")
    )

    source: Mapped[Source] = relationship(back_populates="posts")
    deliveries: Mapped[list[PostDelivery]] = relationship(back_populates="post")
