import pytest

from table_top_loop.degree import Degree


def test_correct_degree():
  val = 300
  deg = Degree(val)
  assert deg.degree_celsius == val - 273.15
  assert deg.kelvin == 300

def test_exception_degree():
  val = -1
  with pytest.raises(Exception):
    deg = Degree(val)
