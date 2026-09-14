"""`user_sources`"""

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.db.models.sources import Source
    from src.db.models.users import User


class UserSource(Base):
    __tablename__ = "user_sources"

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    source_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("sources.id", ondelete="CASCADE"), primary_key=True
    )
    is_enabled: Mapped[bool] = mapped_column(sa.Boolean, server_default=sa.true())

    user: Mapped[User] = relationship(back_populates="sources")
    source: Mapped[Source] = relationship(back_populates="users")
