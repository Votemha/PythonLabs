# cython: language_level=3
from typing import Callable

def integrate(
    f,
    double a,
    double b,
    *,
    int n_iter=1000
) -> double:
    cdef int i
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef double x

    for i in range(n_iter):
        x = a + i * step
        acc += f(x) * step

    return acc