# использование зависимостей
from lr1 import two_sums
import unittest

# тесты
class TestTwoSums(unittest.TestCase):
    
    def test_simple(self):
        # стандартные тесты
        self.assertEqual(two_sums([2,7,11,15], 9), [0, 1], "Ошибка в Example 1")
        self.assertEqual(two_sums([3,2,4], 6), [1, 2], "Ошибка в Example 2")
        self.assertEqual(two_sums([3,3], 6), [0, 1], "Ошибка в Example 3")

        # мои тесты
        self.assertEqual(two_sums([-1,-1,-1], -2), [0, 1], "Ошибка при использовании отрицательных чисел")
        self.assertEqual(two_sums([1,4,5,6,1], 2), [0,4], "Ошибка при проверке значений в разных частях массива")
        self.assertEqual(two_sums([1,1,-1], -2), "Нет решения", "Ошибка при не нахождении решения")
        self.assertEqual(two_sums(["q",1,-1], -2), "Один или несколько элементов не являются целыми числами", "Ошибка при использовании строчных значений")
        self.assertEqual(two_sums([1.1,1.3,3.1], 2.4), "Один или несколько элементов не являются целыми числами", "Ошибка при использовании дробных значений")
        self.assertEqual(two_sums([1], 1), "Недостаточно элементов в массиве", "Ошибка при проверке количества элементов в массиве")



# проверка, что тесты запускаются только при прямом вызове файла
if __name__ == "__main__":
    unittest.main()