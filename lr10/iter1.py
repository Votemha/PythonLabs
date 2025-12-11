import math
import timeit


# итерация 1
def integrate(f, a = int, b = int, *, n_iter=1000):
  """
  - написать документацию для функции
  - аннотировать переменные
  - написать тесты для функции (2 штуки тут)
  - + тесты с помощью Unittest
  >>> round(integrate(math.cos, 0, math.pi / 2, n_iter=100), 5)
  1.00783
  - замерить время вычисления функции (timeit), записать время
  вычисления
  """
  """
  функция вычисляет интеграл для заданной функции
  на вход принимает:
  f - математическая ф-ия
  a, b - границы вычисления интеграла
  n_iter - количество делений функции на части интегрирования
  """
  acc = 0
  step = (b - a) / n_iter
  for i in range(n_iter):
    acc += f(a + i*step) * step
  return acc

# integrate(math.cos, 0, math.pi / 2, n_iter=100)
print(timeit.repeat(stmt="integrate", setup="from iter1 import integrate", repeat=2, number=10000))

print(integrate(math.sin, 0, math.pi))