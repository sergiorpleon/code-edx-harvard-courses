from plates import is_valid

def test_true_case():
    assert is_valid("CS50") == True
    assert is_valid("ABC123") == True

def test_zero():
    assert is_valid("CS05") == False

def test_end_letter():
    assert is_valid("CS50P") == False

def test_size():
    assert is_valid("CS123456") == False

def test_number():
    assert is_valid("1234") == False

def test_point_number():
    assert is_valid("PI3.14") == False

def test_small():
    assert is_valid("H") == False

def test_reverse():
    assert is_valid("50CS") == False


