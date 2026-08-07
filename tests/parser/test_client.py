from dataclasses import dataclass

import pytest

from app.parser.client import extract_text


@dataclass
class _FakeEvent:
    """Minimal stand-in for a Telethon events.NewMessage.Event -- only the
    attribute extract_text actually reads."""

    raw_text: str | None


class _NoTextEvent:
    """Stand-in for an event that doesn't even have a raw_text attribute
    (defensive case, e.g. some non-message update types)."""


@pytest.mark.parametrize(
    ("raw_text", "expected"),
    [
        ("Kyiv -> Lviv, 15000 grn", "Kyiv -> Lviv, 15000 grn"),
        ("  padded text  ", "padded text"),
        ("", None),
        ("   ", None),
        (None, None),
    ],
)
def test_extract_text(raw_text: str | None, expected: str | None) -> None:
    assert extract_text(_FakeEvent(raw_text=raw_text)) == expected


def test_extract_text_missing_attribute() -> None:
    assert extract_text(_NoTextEvent()) is None
