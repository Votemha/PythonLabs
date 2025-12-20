import unittest
import math
from iter1 import integrate


class TestIntegrate(unittest.TestCase):
    """Юнит-тесты для функции integrate()"""

    def test_cosine_integration(self):
        """Тест 1: Проверка правильного расчёта интеграла косинуса
        
        Аналитическое значение: ∫cos(x)dx от 0 до π/2 = sin(π/2) - sin(0) = 1.0
        """
        result = integrate(math.cos, 0, math.pi / 2, n_iter=10000)
        expected = 1.0
        self.assertAlmostEqual(result, expected, places=3,
                             msg="Интеграл косинуса должен быть близок к 1.0")

    def test_quadratic_integration(self):
        """Тест 2: Проверка правильного расчёта интеграла полинома второго порядка
        
        Аналитическое значение: ∫x²dx от 0 до 3 = [x³/3] от 0 до 3 = 27/3 = 9.0
        """
        def quadratic(x):
            return x ** 2
        
        result = integrate(quadratic, 0, 3, n_iter=10000)
        expected = 9.0
        self.assertAlmostEqual(result, expected, places=2,
                             msg="Интеграл x² от 0 до 3 должен быть близок к 9.0")

    def test_linear_integration(self):
        """Тест 3: Проверка расчёта интеграла линейной функции
        
        Аналитическое значение: ∫x dx от 0 до 4 = [x²/2] от 0 до 4 = 8.0
        """
        def linear(x):
            return x
        
        result = integrate(linear, 0, 4, n_iter=5000)
        expected = 8.0
        self.assertAlmostEqual(result, expected, places=2,
                             msg="Интеграл x от 0 до 4 должен быть близок к 8.0")

    def test_constant_function(self):
        """Тест 4: Проверка расчёта интеграла константной функции
        
        Аналитическое значение: ∫5 dx от 1 до 4 = 5 * (4 - 1) = 15.0
        """
        def constant(x):
            return 5
        
        result = integrate(constant, 1, 4, n_iter=1000)
        expected = 15.0
        self.assertAlmostEqual(result, expected, places=3,
                             msg="Интеграл константы 5 от 1 до 4 должен быть 15.0")

    def test_convergence_with_iterations(self):
        """Тест 5: Проверка устойчивости к изменению числа итераций
        
        Точность должна улучшаться с увеличением числа итераций.
        Сравниваем результаты с разным количеством итераций.
        """
        def quadratic(x):
            return x ** 2
        
        expected = 9.0
        
        # Расчёты с разным количеством итераций
        result_100 = integrate(quadratic, 0, 3, n_iter=100)
        result_1000 = integrate(quadratic, 0, 3, n_iter=1000)
        result_10000 = integrate(quadratic, 0, 3, n_iter=10000)
        
        # Проверяем, что результаты улучшаются
        error_100 = abs(result_100 - expected)
        error_1000 = abs(result_1000 - expected)
        error_10000 = abs(result_10000 - expected)
        
        self.assertGreater(error_100, error_1000,
                          msg="Ошибка с 100 итерациями должна быть больше, чем с 1000")
        self.assertGreater(error_1000, error_10000,
                          msg="Ошибка с 1000 итерациями должна быть больше, чем с 10000")
        
        # Проверяем абсолютную точность
        self.assertAlmostEqual(result_10000, expected, places=2,
                             msg="С 10000 итерациями результат должен быть близок к 9.0")

    def test_convergence_with_different_functions(self):
        """Тест 6: Проверка сходимости для разных функций с увеличением итераций
        
        Косинус интегрируется на интервале [0, π/2]
        """
        expected = 1.0
        
        result_100 = integrate(math.cos, 0, math.pi / 2, n_iter=100)
        result_1000 = integrate(math.cos, 0, math.pi / 2, n_iter=1000)
        
        error_100 = abs(result_100 - expected)
        error_1000 = abs(result_1000 - expected)
        
        # Ошибка должна уменьшаться с увеличением итераций
        self.assertGreater(error_100, error_1000,
                          msg="Увеличение итераций должно уменьшить ошибку")

    def test_negative_bounds(self):
        """Тест 7: Проверка работы с отрицательными границами интервала
        
        Аналитическое значение: ∫x dx от -2 до 2 = [x²/2] от -2 до 2 = 2 - 2 = 0.0
        Метод левых прямоугольников может иметь небольшую ошибку.
        """
        def linear(x):
            return x
        
        result = integrate(linear, -2, 2, n_iter=1000)
        expected = 0.0
        self.assertAlmostEqual(result, expected, places=1,
                             msg="Интеграл нечётной функции на симметричном интервале близок к 0")

    def test_sine_integration(self):
        """Тест 8: Проверка расчёта интеграла синуса
        
        Аналитическое значение: ∫sin(x)dx от 0 до π = [-cos(x)] от 0 до π = 2.0
        """
        result = integrate(math.sin, 0, math.pi, n_iter=10000)
        expected = 2.0
        self.assertAlmostEqual(result, expected, places=2,
                             msg="Интеграл синуса от 0 до π должен быть близок к 2.0")


class TestIntegrateEdgeCases(unittest.TestCase):
    """Тесты граничных случаев для функции integrate()"""

    def test_zero_width_interval(self):
        """Тест: Интегрирование на интервале нулевой ширины [a, a]
        
        Результат должен быть близок к нулю
        """
        result = integrate(math.sin, 2.0, 2.0, n_iter=1000)
        self.assertAlmostEqual(result, 0.0, places=5,
                             msg="Интеграл на нулевом интервале должен быть 0")

    def test_small_interval(self):
        """Тест: Интегрирование на очень малом интервале
        
        Аналитическое значение: ∫x² dx от 0 до 0.1 ≈ 0.000333...
        """
        def quadratic(x):
            return x ** 2
        
        result = integrate(quadratic, 0, 0.1, n_iter=1000)
        expected = (0.1 ** 3) / 3  # x³/3 at x=0.1
        self.assertAlmostEqual(result, expected, places=6,
                             msg="Интеграл на малом интервале должен быть точным")

    def test_reversed_bounds(self):
        """Тест: Интегрирование с обратным порядком границ (b < a)
        
        Результат должен быть отрицательным (противоположным нормальному интегралу)
        """
        result_normal = integrate(math.sin, 0, math.pi, n_iter=5000)
        result_reversed = integrate(math.sin, math.pi, 0, n_iter=5000)
        
        # Результаты должны быть противоположны по знаку
        self.assertAlmostEqual(result_normal, -result_reversed, places=3,
                             msg="Интеграл с обратными границами должен быть противоположен")


if __name__ == '__main__':
    unittest.main(verbosity=2)
