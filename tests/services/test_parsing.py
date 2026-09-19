"""Tests for src.services.parsing."""

from decimal import Decimal

from src.services.parsing import extract_price, extract_route


def test_extract_price_with_suffix_currency():
    assert extract_price("Київ - Одеса, 5000 грн, вантаж 20т") == Decimal(5000)


def test_extract_price_with_symbol():
    assert extract_price("Ціна 12500₴") == Decimal(12500)


def test_extract_price_with_comma_decimal():
    assert extract_price("7500,50 грн терміново") == Decimal("7500.50")


def test_extract_price_with_thousands_space():
    assert extract_price("15 000 грн") == Decimal(15000)


def test_extract_price_ignores_weight_marker():
    assert extract_price("Вага 20т, без ціни") is None


def test_extract_price_finds_price_next_to_weight():
    assert extract_price("Вага 20т, ціна 5000грн") == Decimal(5000)


def test_extract_price_returns_none_when_missing():
    assert extract_price("Терміново потрібна машина") is None


def test_extract_route_with_dash():
    assert extract_route("Київ - Одеса, 5000 грн") == ("Київ", "Одеса")


def test_extract_route_with_em_dash():
    assert extract_route("Харків — Дніпро") == ("Харків", "Дніпро")


def test_extract_route_without_spaces():
    assert extract_route("Київ-Одеса 5000грн") == ("Київ", "Одеса")


def test_extract_route_with_two_word_city():
    assert extract_route("Кривий Ріг - Одеса, 3000грн") == ("Кривий Ріг", "Одеса")


def test_extract_route_returns_none_when_missing():
    assert extract_route("5000 грн, дзвонити 0501234567") is None
