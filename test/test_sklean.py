import unittest

from sklearn import datasets
from sklearn.datasets.base import Bunch


class TestDate(unittest.TestCase):
  def test_iris(self):
    iris = datasets.load_iris()
    self.assertEqual(Bunch, type(iris))


if __name__ == '__main__':
  unittest.main()
