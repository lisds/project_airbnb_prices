""" Projcode tests
"""

from projtools import projcode


def test_myfunc():
    assert projcode.my_func(1, 1) == 11
    assert projcode.my_func(0, 1) == 1
    assert projcode.my_func(5, 0) == 50
