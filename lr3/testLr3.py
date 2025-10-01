from lr3 import genBinTree
import unittest

class TestGenBinTree(unittest.TestCase):

    def testGenBinTree(self):
        # Тесты на успешное создание бинарного дерева
        self.assertEqual(genBinTree(2, 1), {1: 1,'left 2': {2: 2, 'left 4': None, 'right 5': None},'right 4': {4: 4, 'left 8': None, 'right 7': None}})
        self.assertEqual(genBinTree(1, 3), {3: 3, 'left 6': None, 'right 6': None})

        # Тесты на нецелочисленные значения
        self.assertEqual(genBinTree("s", 1), "Значение height не целочисленно")
        self.assertEqual(genBinTree(3, "s"), "Значение root не целочисленно")
        self.assertEqual(genBinTree(3.5, 1), "Значение height не целочисленно")
        self.assertEqual(genBinTree(3, 1.5), "Значение root не целочисленно")
        self.assertEqual(genBinTree(-1, 1), "Значение height не целочисленно")
        self.assertEqual(genBinTree(1, -1), "Значение root не целочисленно")
        
    
# проверка, что тесты запускаются только при прямом вызове файла
if __name__ == "__main__":
    unittest.main()