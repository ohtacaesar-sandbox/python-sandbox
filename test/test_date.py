import unittest
from datetime import date


class TestDate(unittest.TestCase):
  def test_str(self):
    self.assertEqual('2015-01-01', str(date(2015, 1, 1)))

  def test_min(self):
    self.assertEqual('0001-01-01', str(date.min))


if __name__ == '__main__':
  unittest.main()
