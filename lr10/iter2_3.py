# итерация 2
# оптимизация с помощью потоков и процессов

import math
import timeit
from typing import Callable, Union
from iter1 import integrate

import concurrent.futures as ftres
from functools import partial


def integrate_async_threads(f: Callable[[Union[int, float]], Union[int, float]], 
                           a: Union[int, float], 
                           b: Union[int, float], 
                           *, 
                           n_jobs: int = 2, 
                           n_iter: int = 1000) -> float:
    """Численное интегрирование с использованием потоков (ThreadPoolExecutor)
    
    Функция разбивает интервал интегрирования на n_jobs подынтервалов и вычисляет
    интегралы параллельно в отдельных потоках, затем суммирует результаты.
    
    Args:
        f: Callable функция для интегрирования, принимает число и возвращает число
        a: Union[int, float] левая граница интервала интегрирования
        b: Union[int, float] правая граница интервала интегрирования
        n_jobs: int количество параллельных потоков (по умолчанию 2)
        n_iter: int общее количество итераций (распределяется между потоками)
    
    Returns:
        float приблизительное значение интеграла
        
    Notes:
        - Каждый поток получает n_iter // n_jobs итераций
        - Использует ThreadPoolExecutor для управления потоками
        - Эффективнее всего при 2-4 потоках из-за GIL в Python
    """
    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)
    
    step = (b - a) / n_jobs
    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
    
    return sum(f.result() for f in ftres.as_completed(fs))


def integrate_async_processes(f: Callable[[Union[int, float]], Union[int, float]], 
                             a: Union[int, float], 
                             b: Union[int, float], 
                             *, 
                             n_jobs: int = 2, 
                             n_iter: int = 1000) -> float:
    """Численное интегрирование с использованием процессов (ProcessPoolExecutor)
    
    Функция разбивает интервал интегрирования на n_jobs подынтервалов и вычисляет
    интегралы параллельно в отдельных процессах, затем суммирует результаты.
    
    Args:
        f: Callable функция для интегрирования, принимает число и возвращает число
        a: Union[int, float] левая граница интервала интегрирования
        b: Union[int, float] правая граница интервала интегрирования
        n_jobs: int количество параллельных процессов (по умолчанию 2)
        n_iter: int общее количество итераций (распределяется между процессами)
    
    Returns:
        float приблизительное значение интеграла
        
    Notes:
        - Каждый процесс получает n_iter // n_jobs итераций
        - Использует ProcessPoolExecutor для управления процессами
        - Имеет overhead инициализации, эффективнее для больших объёмов вычислений
    """
    executor = ftres.ProcessPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)
    
    step = (b - a) / n_jobs
    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
    
    return sum(f.result() for f in ftres.as_completed(fs))


if __name__ == "__main__":
    # Базовая проверка
    print("Потоки (n_iter=1000):", integrate_async_threads(math.sin, 0, math.pi, n_jobs=2, n_iter=1000))
    print("Процессы (n_iter=1000):", integrate_async_processes(math.sin, 0, math.pi, n_jobs=2, n_iter=1000))
    
    print("\nПотоки (n_iter=100000):")
    print(timeit.repeat(stmt="integrate_async_threads(math.sin, 0, math.pi, n_jobs=2, n_iter=100000)", setup="from iter2_3 import integrate_async_threads; import math; from iter1 import integrate", repeat=1, number=5))
    
    print("\nПроцессы (n_iter=100000):")
    print(timeit.repeat(stmt="integrate_async_processes(math.sin, 0, math.pi, n_jobs=2, n_iter=100000)", setup="from iter2_3 import integrate_async_processes; import math; from iter1 import integrate", repeat=1, number=5))