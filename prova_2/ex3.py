import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from helpers.hipotesis_to_str import hipotesis_to_str

from teste_hipotese.normal.normal import Normal

mi = 5.4
std= 1.8
N = [i for i in range(20)]

normal = Normal(N)

print(f"a)") 
hipo = normal.μ.H0_equals_H1_different(4, alfa=5)
print(f"H0: μ=4 e H1: μ!=4 -> {hipotesis_to_str(hipo)}")

print(f"\nb)") 
hipo = normal.μ.H0_equals_H1_different(4, 3, alfa=5)
print(f"H0: μ=4 e H1: μ=3 -> {hipotesis_to_str(hipo)}")

print(f"\nc)") 
hipo = normal.σ.H0_equals_H1_different(2, alfa=5)
print(f"H0: σ²=4 e H1: σ²!=4 -> {hipotesis_to_str(hipo)}")

print("_____________________________________________________\n")

