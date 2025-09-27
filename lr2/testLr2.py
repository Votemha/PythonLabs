from lr2 import game
import unittest

class TestGuessGame(unittest.TestCase):

    def test_game(self):
        # Тест на успешное нахождение числа
        self.assertEqual(game(5, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), "Загаданное число: 5, найдено за 1 попыток")
        # Тест, когда число не найдено
        self.assertEqual(game(15, [1, 10, 20, 30, 40]), None)
        # Тест, когда число вне диапазона
        self.assertEqual(game(50, [1, 10, 20, 30, 40]), None)
        # Тест, когда число вне диапазона
        self.assertEqual(game(1, [10, 20, 30, 40]), None)
        # Тесты на нецелочисленные значения
        self.assertEqual(game(3.5, [10, 20, 30, 40]), "Значение загаданного числа не целочисленно")
        self.assertEqual(game(-1, [10, 20, 30, 40]), None)
        self.assertEqual(game("sss", [10, 20, 30, 40]), "Значение загаданного числа не целочисленно")

# проверка, что тесты запускаются только при прямом вызове файла
if __name__ == "__main__":
    unittest.main()