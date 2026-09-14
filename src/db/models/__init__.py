"""Importing this package registers every model on `Base.metadata`"""

from src.db.models.deliveries import PostDelivery
from src.db.models.features import Feature
from src.db.models.methods import Method
from src.db.models.payments import Payment
from src.db.models.posts import Post
from src.db.models.routes import Route
from src.db.models.settings import UserSettings
from src.db.models.sources import Source
from src.db.models.subscriptions import UserSubscription
from src.db.models.user_sources import UserSource
from src.db.models.users import User

__all__ = [
    "Feature",
    "Method",
    "Payment",
    "Post",
    "PostDelivery",
    "Route",
    "Source",
    "User",
    "UserSettings",
    "UserSource",
    "UserSubscription",
]
