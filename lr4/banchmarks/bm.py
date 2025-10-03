import timeit
import matplotlib.pyplot as plt
import random
from functools import *

def fact_recursive(n: int) -> int:
    """Рекурсивный факториал"""
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)


def fact_iterative(n: int) -> int:
    """Нерекурсивный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

@lru_cache(None)
def fact_recursive_lc(n: int) -> int:
    """Рекурсивный факториал c lru_cache"""
    if n == 0:
        return 1
    return n * fact_recursive_lc(n - 1)

@lru_cache(None)
def fact_iterative_lc(n: int) -> int:
    """Нерекурсивный факториал c lru_cache"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


def benchmark(func, data, number=1, repeat=5):
    """Возвращает среднее время выполнения func на наборе data"""
    total = 0
    for n in data:
        # несколько повторов для усреднения
        times = timeit.repeat(lambda: func(n), number=number, repeat=repeat)
        total += min(times)  # берём минимальное время из серии
    return total / len(data)

@lru_cache(None)
def main():
    # фиксированный набор данных
    random.seed(42)
    test_data = list(range(60, 300, 14))

    res_recursive = []
    res_iterative = []
    res_recursiveLc = []
    res_iterativeLc = []

    for n in test_data:
        res_recursive.append(benchmark(fact_recursive, [n], number=10000, repeat=5))
        res_iterative.append(benchmark(fact_iterative, [n], number=10000, repeat=5))
        res_recursiveLc.append(benchmark(fact_recursive_lc, [n], number=10000, repeat=5))
        res_iterativeLc.append(benchmark(fact_iterative_lc, [n], number=10000, repeat=5))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Первый график: итеративный с кешированием
    ax1.plot(test_data, res_iterative, label="Нерекурсивный факториал")
    ax1.plot(test_data, res_iterativeLc, label="Нерекурсивный факториал c lru_cache")
    ax1.set_xlabel("n")
    ax1.set_ylabel("Время (сек)")
    ax1.set_title("Сравнение итеративных реализаций")
    ax1.legend()
    ax1.grid(True)

    # Второй график: рекурсивный с кешированием
    ax2.plot(test_data, res_recursive, label="Рекурсивный факториал")
    ax2.plot(test_data, res_recursiveLc, label="Рекурсивный факториал c lru_cache")
    ax2.set_xlabel("n")
    ax2.set_ylabel("Время (сек)")
    ax2.set_title("Сравнение рекурсивных реализаций")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
