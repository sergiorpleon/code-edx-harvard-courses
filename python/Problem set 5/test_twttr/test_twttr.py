from twttr import shorten

def test_empty():
    assert shorten("") == ""
    assert shorten("aeiou") == ""
    assert shorten("AEIOU") == ""

def test_word():
    assert shorten("Twitter") == "Twttr"
    assert shorten("What's your name?") == "Wht's yr nm?"
    assert shorten("HOME") == "HM"

def test_not_vocal():
    assert shorten("CS50") == "CS50"
