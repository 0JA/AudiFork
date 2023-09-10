# tests/a_test.py

import sys
sys.path.append("../src")

import a
import pytest

def test_addition():
    result = a.add(1, 2)
    assert result == 3

def test_addition_negative():
    result = a.add(-1, -2)
    assert result == -9

@pytest.mark.parametrize("input_a, input_b, expected", [(1, 2, 3), (-1, -2, -3), (0, 0, 0)])
def test_addition_parametrized(input_a, input_b, expected):
    result = a.add(input_a, input_b)
    assert result == expected
