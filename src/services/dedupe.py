"""Compute the fingerprint used to detect duplicate posts across sources."""

import hashlib
from decimal import Decimal


def compute_fingerprint(from_norm: str, to_norm: str, price: Decimal) -> str:
    # Quantize first so 5000 and 5000.00 hash identically.
    normalized_price = price.quantize(Decimal("0.01"))
    raw = f"{from_norm}{to_norm}{normalized_price}"
    return hashlib.sha256(raw.encode()).hexdigest()
