import pytest
from jar import Jar


def test_init():
    jar1 = Jar()
    assert jar1.size == 0
    assert jar1.capacity == 12
    jar2 = Jar(10)
    assert jar2.capacity == 10

def test_init_negative():
    with pytest.raises(ValueError):
        assert Jar(-5)

def test_str():
    jar = Jar()
    assert str(jar) == ""
    jar.deposit(1)
    assert str(jar) == "🍪"
    jar.deposit(11)
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"

def test_deposit():
    jar = Jar(5)
    jar.deposit(2)
    assert jar.size == 2
    jar.deposit(2)
    assert jar.size == 4

def test_deposit_error():
    with pytest.raises(ValueError):
        jar = Jar(5)
        assert jar.deposit(10)

def test_withdraw():
    jar = Jar(5)
    jar.deposit(4)
    jar.withdraw(2)
    assert jar.size == 2
    jar.withdraw(2)
    assert jar.size == 0

def test_withdraw_error():
    with pytest.raises(ValueError):
        jar = Jar(5)
        assert jar.withdraw(10)
