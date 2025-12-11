from iter1 import integrate
import unittest
import math

class TestIter1(unittest.TestCase):

    def test_iter1(self):
        self.assertEqual(round(integrate(math.cos, 0, math.pi / 2, n_iter=100), 5), 1.00783)
        self.assertEqual(round(integrate(math.cos, 0, math.pi / 2, n_iter=100), 5), 1.00783)

    
# запускаем тесты
if __name__ == "__main__":
    unittest.main()