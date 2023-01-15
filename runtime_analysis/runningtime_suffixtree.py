from numpy.random import choice
from numpy import mean
import pandas as pd
import time
from suffixtree import *

alphabet = ["A", "C", "G", "T"]


def get_random_string(alphabet, n):
    return "".join(choice(alphabet, n))


lengths = range(1, 10000000, 500000)

t_naive = []
t_mccreight = []
i = 1

for n in lengths:
    tn = []
    tm = []
    for _ in range(3):
        x = get_random_string(alphabet, n)
        start = time.perf_counter()
        naive_st_construction(x)
        end = time.perf_counter()
        tn.append(end - start)

        start = time.perf_counter()
        mccreights_st_construction(x)
        end = time.perf_counter()
        tm.append(end - start)

    t_naive.append(mean(tn))
    t_mccreight.append(mean(tm))
    print("Completed iteration", i, ", average run time per iteration:", sum(tn))
    i += 1

df = pd.DataFrame(
    list(zip(lengths, t_naive, t_mccreight)), columns=["n", "naive", "mccreight"]
)

df.to_csv("plots/suffixtree_runtime_10m.csv", index=False)
