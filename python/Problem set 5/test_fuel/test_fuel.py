import pytest
from fuel import convert, gauge

def test_covert():
    assert convert("3/4") == 75
    assert convert("1/4") == 25
    assert convert("4/4") == 100
    assert convert("0/4") == 0

def test_zero():
    with pytest.raises(ZeroDivisionError):
        convert("4/0") == False

def test_value_error():
    with pytest.raises(ValueError):
        convert("three/four")
        convert("1.5/3")


def test_percent():
    assert gauge(75) == "75%"
    assert gauge(25) == "25%"

def test_full():
    assert gauge(100) == "F"
    assert gauge(99) == "F"

def test_empty():
    assert gauge(0) == "E"
    assert gauge(1) == "E"
