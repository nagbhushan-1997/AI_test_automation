# tests.py

import pytest
from scr.my_testing_code import divide, power

def test_divide_happy_path():
    assert divide(10, 2) == 5

def test_divide_invalid_input():
    with pytest.raises(ValueError):
        divide(0, 2)

def test_power_happy_path():
    assert power(2, 3) == 8

def test_power_invalid_input():
    with pytest.raises(ValueError):
        power(0, 3)