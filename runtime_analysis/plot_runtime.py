import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("plots/repeats_runtime.csv")

df.plot(x="n", y=["ts"], kind="line", figsize=(9, 8), ylabel="Time (s)", legend=None)

plt.savefig("plots/runtime_find_repeats")
plt.show()
