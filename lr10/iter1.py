import math
import timeit
from typing import Callable, Union


# итерация 1
def integrate(f: Callable[[Union[int, float]], Union[int, float]], 
              a: Union[int, float], 
              b: Union[int, float], 
              *, 
              n_iter: int = 1000) -> float:
  """Функция численного интегрирования методом прямоугольников

  Args:
      f: Callable функция, которую необходимо проинтегрировать.
          Функция должна принимать один числовой аргумент и возвращать числовое значение.
      a: int, float
          Левая граница интервала
      b: int, float
          Правая граница интервала
      n_iter: int, optional
          Количество разбиений
          По умолчанию: 1000

  Returns:
      float: Приблизительное значение интеграла функции f на интервале [a, b]

  Examples:
      Пример 1: Интегрирование тригонометрической функции (косинус)
      
      >>> import math
      >>> result = round(integrate(math.cos, 0, math.pi / 2, n_iter=1000), 5)
      >>> print(f"Интеграл cos(x) от 0 до π/2: {result}")
      Интеграл cos(x) от 0 до π/2: 1.00079
      
      Пример 2: Интегрирование полиномиальной функции второго порядка (x²)
      
      >>> def quadratic(x):
      ...     return x ** 2
      >>> result = round(integrate(quadratic, 0, 3, n_iter=1000), 5)
      >>> print(f"Интеграл x² от 0 до 3: {result}")
      Интеграл x² от 0 до 3: 8.9865
      >>> # Аналитическое значение: [x³/3] от 0 до 3 = 27/3 = 9.0
  """
  acc = 0
  step = (b - a) / n_iter
  for i in range(n_iter):
    acc += f(a + i*step) * step
  return acc

if __name__ == "__main__":
  print(timeit.repeat(stmt="integrate(math.sin, 0, math.pi)", setup="from iter1 import integrate; import math", repeat=1, number=5))