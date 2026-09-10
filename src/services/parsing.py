"""Extract price and route from raw post text."""

import re
from decimal import Decimal, InvalidOperation

_CITY_PATTERN = r"[A-Za-zА-ЯІЇЄҐа-яіїєґ'’]+(?:\s[A-Za-zА-ЯІЇЄҐа-яіїєґ'’]+)*"

_PRICE_PATTERN = re.compile(
    r"(?:(\d[\d\s]*(?:[.,]\d+)?)\s*(?:грн|₴|uah)"
    r"|(?:грн|₴|uah)\s*(\d[\d\s]*(?:[.,]\d+)?))",
    re.IGNORECASE,
)
_ROUTE_PATTERN = re.compile(rf"({_CITY_PATTERN})\s*(?:-|–|—|->|=>)\s*({_CITY_PATTERN})")


def extract_price(raw_text: str) -> Decimal | None:
    match = _PRICE_PATTERN.search(raw_text)
    if match is None:
        return None
    raw_number = match.group(1) or match.group(2)
    normalized = raw_number.replace(" ", "").replace(",", ".")
    try:
        return Decimal(normalized)
    except InvalidOperation:
        return None


def extract_route(raw_text: str) -> tuple[str, str] | None:
    # Naive dash-separated match; doesn't handle hyphenated city names
    # (e.g. "Кам'янець-Подільський") — needs revisiting against real
    # channel samples.
    match = _ROUTE_PATTERN.search(raw_text)
    if match is None:
        return None
    return match.group(1).strip(), match.group(2).strip()
