from scipy.stats import lognorm, norm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from distribuicoes import LogNorm3ParamHosking, LogNorm3Param

mi_y = 0.8556 #qsi
sigma_y  = 0.2306 #alfa
a   = -1.7912 #k

log_norm3 = LogNorm3Param(a=a, mi_y=mi_y, sigma_y=sigma_y)
log_norm3_CPRM = LogNorm3ParamHosking(qsi=0.929, alfa=0.448, kapa=-0.311)

dados = pd.read_csv(r"prova_2\dados_formatados_antigos.csv", sep="\t")

dados_norm = dados.copy()

for col in dados_norm:
    ys = dados_norm[col]/dados_norm[col].mean()
    ys = ys[~ys.isna()]
    ys = ys.sort_values(ascending=True)

    N = ys.size

    xs = x = np.arange(1, N+1)
    xs = (xs/(N+1))[::-1]

    Tr=1/xs

    plt.scatter(Tr, ys, label = col)

for Tr in [1.01, 2, 5, 10, 20, 25, 50, 100, 150, 200]:
    y_now = log_norm3.quantil_TR(Tr)
    print(f"Tr: {Tr} | {y_now}")

# Posição de plotagem
Tr = np.linspace(1.01, 100, 1000)

y_now = log_norm3.quantil_TR(Tr)
plt.plot(Tr, y_now, label="Log-Normal 3P")

y_now = log_norm3_CPRM.quantil_TR(Tr)
plt.plot(Tr, y_now, label="Log-Normal 3P (CPRM)")

plt.xscale("log")

plt.grid(True)
plt.legend()
plt.show()

