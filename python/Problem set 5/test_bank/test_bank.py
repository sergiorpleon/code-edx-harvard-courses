from bank import value

def test_hello():
    assert value("Hello") == 0
    assert value("Hello, Newman") == 0

def test_h():
    assert value("Hey") == 20
    assert value("How you doing?") == 20

def test_not_h():
    assert value("What's happening?") == 100
    assert value("123") == 100
