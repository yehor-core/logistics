"""Status and type enums shared by the ORM models"""

from enum import StrEnum


class SourceType(StrEnum):
    TELEGRAM = "telegram"


class PostStatus(StrEnum):
    NEW = "new"
    READY = "ready"
    DISTRIBUTED = "distributed"
    SKIPPED = "skipped"
    FAILED = "failed"
    DUPLICATE = "duplicate"
