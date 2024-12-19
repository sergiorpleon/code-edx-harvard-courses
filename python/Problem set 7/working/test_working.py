import pytest
from working import convert

def test_correct_not_minute():
    assert convert("9 AM to 5 PM") == "09:00 to 17:00"
    assert convert("12 AM to 12 PM") == "00:00 to 12:00"

def test_correct_with_minute():
    assert convert("9:00 AM to 5:00 PM") == "09:00 to 17:00"
    assert convert("12:00 AM to 12:00 PM") == "00:00 to 12:00"

def test_correct_mix():
    assert convert("10 AM to 8:50 PM") == "10:00 to 20:50"
    assert convert("10:30 PM to 8 AM") == "22:30 to 08:00"




def test_incorrect_minutes_etc():
     with pytest.raises(ValueError):
        convert("9:60 AM to 5:60 PM")
        convert("9:60 AM 5:60 PM")
        convert("20:80 AM to 5:80 PM")

def test_incorrect_separator_etc():
     with pytest.raises(ValueError):
        convert("9 AM - 5 PM")
        convert("09:00 AM - 17:00 PM")



def test_wrong_format():
    with pytest.raises(ValueError):
        convert("9 AM - 9 PM")


def test_wrong_minute():
    with pytest.raises(ValueError):
         convert("9:60 AM to 9:60 PM")


def test_wrong_hour():
    with pytest.raises(ValueError):
        convert("13 PM to 17 PM")
