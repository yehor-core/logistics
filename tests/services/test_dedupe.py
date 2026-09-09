"""Tests for src.services.dedupe."""

from decimal import Decimal

from src.services.dedupe import compute_fingerprint


def test_compute_fingerprint_is_deterministic():
    first = compute_fingerprint("kyiv", "odesa", Decimal(5000))
    second = compute_fingerprint("kyiv", "odesa", Decimal(5000))
    assert first == second


def test_compute_fingerprint_ignores_decimal_precision():
    assert compute_fingerprint("kyiv", "odesa", Decimal(5000)) == compute_fingerprint(
        "kyiv", "odesa", Decimal("5000.00")
    )


def test_compute_fingerprint_differs_on_price():
    assert compute_fingerprint("kyiv", "odesa", Decimal(5000)) != compute_fingerprint(
        "kyiv", "odesa", Decimal(5001)
    )


def test_compute_fingerprint_differs_on_route():
    assert compute_fingerprint("kyiv", "odesa", Decimal(5000)) != compute_fingerprint(
        "odesa", "kyiv", Decimal(5000)
    )
