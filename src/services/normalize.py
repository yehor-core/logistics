"""Normalize raw city names into `_norm` keys via a lookup dictionary."""

import re

_PREFIX_PATTERN = re.compile(r"^(м\.|с\.|смт\.?)\s*", re.IGNORECASE)
_PUNCTUATION_PATTERN = re.compile(r"[^\w\s]", re.UNICODE)


def normalize_city(raw: str, city_dict: dict[str, str]) -> str | None:
    without_prefix = _PREFIX_PATTERN.sub("", raw.strip())
    cleaned = _PUNCTUATION_PATTERN.sub("", without_prefix).strip().lower()
    return city_dict.get(cleaned)
