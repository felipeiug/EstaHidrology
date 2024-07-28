import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


from solvers.MOM.MOM_GEV import GEV as GEV_MOM
from distribuicoes import GEV

from distribuicoes import LogNorm3ParamHosking, LogNorm3Param
from solvers.MOM.MOM_log_norm_3 import LogNorm3

# Lendo os dados
df = pd.read_csv("prova_2\dados_formatados_antigos.csv", sep= "\t")

# Definindo os parâmetros para ambas as distribuições
data_params = {
    "N":[],
    "a":[],
    "mi_y":[],
    "sigma_y":[],
}
data_params_GEV = {
    "N":[],
    "alfa":[],
    "beta":[],
    "kapa":[],
}
for col in df.columns:
    col_data = df[col]/df[col].mean()
    col_data = col_data[~col_data.isna()]

    N = col_data.size

    col_data.sort_values(inplace=True, ascending=False, ignore_index=True)
    x = (np.arange(1, col_data.size+1)-0.4)/(col_data.size+0.2)

    log_norm = LogNorm3(col_data)
    a, mi_y, sigma_y = log_norm.parametros()

    gev_mom = GEV_MOM(col_data)
    alfa, beta, k = gev_mom.parametros()

    if np.isnan(a) or np.isnan(mi_y) or np.isnan(sigma_y):
        continue
    if not np.isfinite(a) or not np.isfinite(mi_y) or not np.isfinite(sigma_y):
        continue

    data_params["N"].append(N)
    data_params["a"].append(a)
    data_params["mi_y"].append(mi_y)
    data_params["sigma_y"].append(sigma_y)

    data_params_GEV["N"].append(N)
    data_params_GEV["alfa"].append(alfa)
    data_params_GEV["beta"].append(beta)
    data_params_GEV["kapa"].append(k)

    Tr = 1/x
    Tr = Tr[::-1]
    col_data.sort_values(inplace=True, ascending=True, ignore_index=True)

    plt.scatter(Tr, col_data, label=col)

# Definindo a média ponderada pela quantidade de dados nos anos
df_params = pd.DataFrame(data_params)

a = np.sum(df_params["N"]*df_params["a"])/np.sum(df_params["N"])
mi_y = np.sum(df_params["N"]*df_params["mi_y"])/np.sum(df_params["N"])
sigma_y = np.sum(df_params["N"]*df_params["sigma_y"])/np.sum(df_params["N"])

print(f"a: {np.round(a, 3)}, mi_y: {np.round(mi_y, 3)}, sigma_y: {np.round(sigma_y, 3)}")



df_params_gev = pd.DataFrame(data_params_GEV)

alfa = np.sum(df_params_gev["N"]*df_params_gev["alfa"])/np.sum(df_params_gev["N"])
beta = np.sum(df_params_gev["N"]*df_params_gev["beta"])/np.sum(df_params_gev["N"])
kapa = np.sum(df_params_gev["N"]*df_params_gev["kapa"])/np.sum(df_params_gev["N"])

print(f"alfa: {np.round(alfa, 3)}, beta: {np.round(beta, 3)}, kapa: {np.round(kapa, 3)}")


gev = GEV(alfa=alfa, beta=beta, kapa=kapa)
log_norm3 = LogNorm3Param(a=a, mi_y=mi_y, sigma_y=sigma_y)
log_norm3_CPRM = LogNorm3ParamHosking(qsi=0.929, alfa=0.448, kapa=-0.311)

tempos = [1.01, 2, 5, 10, 20, 25, 50, 100, 150, 200]
for n, i in enumerate(["TR", "GEV", "Log-Normal 3P (MOM)", "Log-Normal 3P (CPRM)"]):
    
    if n == 0:
        print("TR: " + " | ".join([str(i) for i in tempos]))
    elif n == 1:
        print("GEV: " + " | ".join([str(np.round(gev.quantil_TR(i), 3)) for i in tempos]))
    elif n == 2:
        print("LOGN3: " + " | ".join([str(np.round(log_norm3.quantil_TR(i), 3)) for i in tempos]))
    elif n == 3:
        print("LOGN3 (CPRM): " + " | ".join([str(np.round(log_norm3_CPRM.quantil_TR(i), 3)) for i in tempos]))

# GRáfico normalizado

Tr = np.linspace(1.01, 1000, 5000)

y_gev = gev.quantil_TR(Tr)
plt.plot(Tr, y_gev, label="GEV (MOM)")

y_ln3 = log_norm3.quantil_TR(Tr)
plt.plot(Tr, y_ln3, label="Log-Normal 3P (MOM)")

y_lncprm = log_norm3_CPRM.quantil_TR(Tr)
plt.plot(Tr, y_lncprm, label="Log-Normal 3P (CPRM)")

plt.title("Teste de Aderência Visual")

plt.xlabel("TR (anos)")
plt.ylabel("Qmax_anual/Q_med_max_anual")
plt.xscale("log")

plt.grid(True)
plt.legend()
plt.show()

# Gráfico real

def Qmed(A):
    return 0.7651*A**(0.7828)

areas = {
    "41151000": 174.6,
    "41199998": 1697.8,
    "41250000": 675.7,
    "41260000": 3727.4,
    "41300000": 626,
    "41340000": 4874.2,
    "41380000": 553.4,
    "41410000": 6557.7
}

for estacao in df.columns:

    q_med = Qmed(areas[estacao])

    y_now = q_med*y_gev
    plt.plot(Tr, y_now, label="GEV (MOM)")

    y_now = q_med*y_ln3
    plt.plot(Tr, y_now, label="Log-Normal 3P (MOM)")

    y_now = q_med*y_lncprm
    plt.plot(Tr, y_now, label="Log-Normal 3P (CPRM)")

    # Dados estação
    col_data = df[estacao]
    col_data = col_data[~col_data.isna()]

    N = col_data.size

    col_data.sort_values(inplace=True, ascending=False, ignore_index=True)
    x = (np.arange(1, col_data.size+1)-0.4)/(col_data.size+0.2)

    Tr_esta = 1/x
    Tr_esta = Tr_esta[::-1]
    col_data.sort_values(inplace=True, ascending=True, ignore_index=True)

    plt.scatter(Tr_esta, col_data, label=estacao)

    plt.title(f"Quantil Estação {estacao}")

    plt.xlabel("TR (anos)")
    plt.ylabel("Qmax_anual (m³/s)")
    plt.xscale("log")

    plt.grid(True)
    plt.legend()
    plt.show()