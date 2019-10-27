import cv2
import numpy as np
import unittest
from os import path


class TestOpenCV3(unittest.TestCase):
  def test_image(self):
    img_path = path.join(path.dirname(__file__), '../test_data/github_boys.jpg')
    img = cv2.imread(img_path)
    self.assertEqual(type(np.array([])), type(img))


if __name__ == '__main__':
  unittest.main()
