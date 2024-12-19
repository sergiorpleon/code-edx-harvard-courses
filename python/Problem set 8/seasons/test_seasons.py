import pytest
from datetime import date
from seasons import minutes

def test_1_day():
    today = date.today()
    if today.day == 1:
        assert minutes(f"{today.year}-{today.month:02}-{(today.day+1):02}") == "One thousand, four hundred forty minutes"
    else:
        assert minutes(f"{today.year}-{today.month:02}-{(today.day-1):02}") == "One thousand, four hundred forty minutes"

def test_1_month():
    today = date.today()
    if today.month == 1:
        assert minutes(f"{today.year}-{(today.month+1):02}-{today.day:02}") == "Forty-four thousand, six hundred forty minutes"
    else:
        assert minutes(f"{today.year}-{(today.month-1):02}-{today.day:02}") == "Forty-four thousand, six hundred forty minutes"

def test_one_year():
    today = date.today()
    assert minutes(f"{today.year-1}-{today.month:02}-{today.day:02}") == "Five hundred twenty-seven thousand forty minutes"

def test_two_year():
    today = date.today()
    assert minutes(f"{today.year-2}-{today.month:02}-{today.day:02}") == "One million, fifty-two thousand, six hundred forty minutes"

def test_text():
    with pytest.raises(ValueError):
        assert minutes("today")

def test_date_invalid():
    with pytest.raises(ValueError):
        assert minutes("2020-12-50")
