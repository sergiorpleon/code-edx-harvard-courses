import pytest
from numb3rs import validate

def test_zero():
    assert validate("0.0.0.1") == True

def test_localhost():
    assert validate("127.0.0.1") == True

def test_255():
    assert validate("255.255.255.255") == True


def test_512():
    assert validate("512.512.512.512") == False

def test_big():
    assert validate("10.450.50.50") == False
    assert validate("1.260.300.1000") == False
    assert validate("1.2.3.1000") == False
    assert validate("1.2.1000.4") == False
    assert validate("1.1000.3.4") == False
    assert validate("1000.2.3.4") == False

def test_only_3():
    assert validate("2.3.4") == False

def test_text():
    assert validate("cat") == False

def test_text_4():
    assert validate("cat.cat.cat.cat") == False

