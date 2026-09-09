"""Tests for src.services.normalize."""

from src.services.normalize import normalize_city

_CITY_DICT = {
    "київ": "kyiv",
    "одеса": "odesa",
    "кривий ріг": "kryvyi_rih",
}


def test_normalize_city_lowercases():
    assert normalize_city("Київ", _CITY_DICT) == "kyiv"


def test_normalize_city_strips_prefix():
    assert normalize_city("м. Одеса", _CITY_DICT) == "odesa"


def test_normalize_city_strips_punctuation_and_emoji():
    assert normalize_city("Одеса!🚚", _CITY_DICT) == "odesa"


def test_normalize_city_multi_word():
    assert normalize_city("Кривий Ріг", _CITY_DICT) == "kryvyi_rih"


def test_normalize_city_unknown_returns_none():
    assert normalize_city("Атлантида", _CITY_DICT) is None
