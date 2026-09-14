"""`routes`"""

from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class Route(Base):
    """Looked up by value from `Posts.(from_norm, to_norm)` — no foreign key on either side"""

    __tablename__ = "routes"

    from_norm: Mapped[str] = mapped_column(sa.Text, primary_key=True)
    to_norm: Mapped[str] = mapped_column(sa.Text, primary_key=True)
    distance_km: Mapped[Decimal] = mapped_column(sa.Numeric(10, 2))
    from_location: Mapped[str] = mapped_column(sa.Text)
    to_location: Mapped[str] = mapped_column(sa.Text)
