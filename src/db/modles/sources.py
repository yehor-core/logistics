"""Source ORM model"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from src.enums import SourceType

if TYPE_CHECKING:
    from src.db.models.posts import Post


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[SourceType] = mapped_column(
        Enum(
            SourceType,
            native_enum=True,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        )
    )
    is_enabled: Mapped[bool] = mapped_column(server_default="true")
    last_fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    chat_id: Mapped[int | None] = mapped_column(BigInteger)

    posts: Mapped[list["Post"]] = relationship(back_populates="source")
