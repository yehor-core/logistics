"""All statuses in one place"""

from enum import StrEnum


class PaymentStatus(StrEnum):
    """`Payments.status`"""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    EXPIRED = "expired"


class SubscriptionStatus(StrEnum):
    """`User subscriptions.status`"""

    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class SourceType(StrEnum):
    """`Sources.type`"""

    TELEGRAM = "telegram"


class PostStatus(StrEnum):
    """`Posts.status`"""

    NEW = "new"
    READY = "ready"
    DISTRIBUTED = "distributed"
    SKIPPED = "skipped"
    FAILED = "failed"
    DUPLICATE = "duplicate"


class DeliveryStatus(StrEnum):
    """`Post deliveries.status`"""

    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    BLOCKED = "blocked"
