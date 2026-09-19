"""Post ORM model"""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from src.enums import PostStatus

if TYPE_CHECKING:
    from src.db.models.sources import Source


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        UniqueConstraint("source_id", "external_id"),
        Index(None, "fingerprint", "published_at"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    external_id: Mapped[int] = mapped_column(BigInteger)
    fingerprint: Mapped[str | None] = mapped_column(String(64))
    raw_text: Mapped[str] = mapped_column(Text)
    from_location: Mapped[str | None] = mapped_column(Text)
    to_location: Mapped[str | None] = mapped_column(Text)
    price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    price_per_km: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    parsed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[PostStatus] = mapped_column(
        Enum(
            PostStatus,
            native_enum=True,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        index=True,
    )
    from_norm: Mapped[str | None] = mapped_column(Text)
    to_norm: Mapped[str | None] = mapped_column(Text)
    duplicate_of_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("posts.id"))

    source: Mapped[Source] = relationship(back_populates="posts")
