"""`sources`"""

from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, pg_enum
from src.enums import SourceType

if TYPE_CHECKING:
    from src.db.models.posts import Post
    from src.db.models.user_sources import UserSource


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    type: Mapped[SourceType] = mapped_column(pg_enum(SourceType, "source_type"))
    is_enabled: Mapped[bool] = mapped_column(sa.Boolean, server_default=sa.true())
    last_fetched_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True))
    chat_id: Mapped[int | None] = mapped_column(sa.BigInteger)

    users: Mapped[list[UserSource]] = relationship(back_populates="source")
    posts: Mapped[list[Post]] = relationship(back_populates="source")
