"""Every table from docs/03-data-model.md is mapped, with the keys the pipeline relies on"""

import src.db.models  # noqa: F401
from src.db.base import Base

EXPECTED_TABLES = {
    "features",
    "methods",
    "payments",
    "post_deliveries",
    "posts",
    "routes",
    "sources",
    "user_settings",
    "user_sources",
    "user_subscriptions",
    "users",
}

EXPECTED_PRIMARY_KEYS = {
    "post_deliveries": ["post_id", "user_id"],
    "routes": ["from_norm", "to_norm"],
    "user_settings": ["user_id"],
    "user_sources": ["user_id", "source_id"],
}


def test_every_table_is_mapped() -> None:
    assert set(Base.metadata.tables) == EXPECTED_TABLES


def test_primary_keys() -> None:
    for table_name, columns in EXPECTED_PRIMARY_KEYS.items():
        table = Base.metadata.tables[table_name]
        assert [column.name for column in table.primary_key] == columns


def test_posts_are_unique_per_source() -> None:
    constraints = {
        tuple(column.name for column in constraint.columns)
        for constraint in Base.metadata.tables["posts"].constraints
    }
    assert ("source_id", "external_id") in constraints


def test_enum_columns_store_lowercase_values() -> None:
    status = Base.metadata.tables["posts"].columns["status"].type
    assert status.enums == ["new", "ready", "distributed", "skipped", "failed", "duplicate"]
