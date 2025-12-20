import math
import timeit
from integrate import integrate

print(integrate(math.cos, 0, math.pi / 2, n_iter=1_000_000))

if __name__ == "__main__":
  print(timeit.repeat(stmt="integrate(math.sin, 0, math.pi)", setup="from integrate import integrate; import math", repeat=1, number=5))