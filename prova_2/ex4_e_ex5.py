from scipy.stats import norm,t as t_student,chi2
from numpy import sqrt
import numpy as np

#######################################
# Exercício 4 Teste de Chi2

serie = np.array([0, 3, 1, 2, 0, 1, 1, 1, 2, 0, 1, 4, 3, 1, 1, 0, 0, 1, 0, 2])

print(f"Série: {serie}")

v_chapeu = serie.mean()
print(f"v^: {v_chapeu}")

c = chi2.ppf(1-0.05, 3)

print("Exercício 4")
print(f"chi2: {c}\n\n")

# Exercício 5

N = 30
x_ = 2.52
s = 2.05
t = abs(t_student.ppf(0.975, N-1))

print("Exercício 5")
print(f"t(97,5%%, {N-1}) = {t}")

mi_x_ = (t*s/sqrt(N))

print(f"mi-x_ <= {mi_x_}")

print(norm(loc=2.05, scale=2.52).cdf(0.68))



