from lr5 import gen_bin_tree
import unittest

class TestGenBinTree(unittest.TestCase):

    def test_gen_bin_tree(self):
        self.assertEqual(gen_bin_tree(0, 2, lambda x: x*3, lambda y: y+2), "Высота дерева должна быть больше 0")
        self.assertEqual(gen_bin_tree(-1, 2, lambda x: x*3, lambda y: y+2), "Значения height и root должны быть целочисленными")
        self.assertEqual(gen_bin_tree("ss", 2, lambda x: x*3, lambda y: y+2), "Значения height и root должны быть целочисленными")
        self.assertEqual(gen_bin_tree(4, 2, 12, lambda y: y+2), "Функции должны быть callable")
        self.assertEqual(gen_bin_tree(4, 2, lambda x: x*3, 12), "Функции должны быть callable")


# проверка, что тесты запускаются только при прямом вызове файла
if __name__ == "__main__":
    unittest.main()