# from regionalizacao.index_flood.index_floox import index_flood
# from papeis_de_plotagem.plot_data_and_distribuitions import plot_series

# from solvers.MOM.MOM_log_norm_3 import LogNorm3
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# import os

from tp10 import *

# df = pd.read_csv("prova_2\dados_formatados_antigos.csv", sep= "\t")

# for col in df.columns:
#     col_data = df[col]/df[col].mean()
#     col_data = col_data[~col_data.isna()]

#     col_data.sort_values(inplace=True, ascending=False, ignore_index=True)
#     x = (np.arange(1, col_data.size+1)-0.4)/(col_data.size+0.2)

#     log_norm = LogNorm3(col_data)
#     print(f"{col}: {log_norm.parametros()}")

#     Tr = 1/x
#     Tr = Tr[::-1]
#     col_data.sort_values(inplace=True, ascending=True, ignore_index=True)

#     plt.scatter(Tr, col_data, label=col)

# plt.xlabel("TR (anos)")
# plt.ylabel("Qmax_anual/Q_med_max_anual")
# plt.xscale("log")

# plt.grid(True)
# plt.legend()
# plt.show()



# # Regionalização das vazões médias
# dados_estacoes = {
#     "codigo": [40549998, 40573000, 40577000, 40579995, 40665000, 40710000, 40740000],
#     "area": [461.4, 291.1, 244, 578.5, 293.3, 2760.1, 3939.2],
#     "P": [1.400, 1.462, 1.466, 1.464, 1.373, 1.408, 1.422],
#     "I": [2.69, 3.94, 7.2, 3.18, 2.44, 1.59, 1.21],
#     "L": [52, 32.7, 18.3, 41.6, 45.7, 118.9, 187.4],
#     "Juncoes": [0.098, 0.079, 0.119, 0.102, 0.123, 0.137, 0.134],
# }



# vazoes_maximas_anuais = {
#     "40549998":np.array([97.2, 42.2, 44.1, 51.7, 80.3, 56.6, 44, 81, 77.8, 58, 56.9, 91.7, 53.3, 48, 33.1, 65.6, 112, 132, 68.6, 48.5, 50.4, 38.3, 36.4, 77, 37.2, 44.6, 57.9, 33, 63.2, 42.4, 85.7, 39]),
#     "40573000":np.array([33, 28.8, 39.3, 34.9, 20, 22, 49.3, 20.5, 23.5, 21, 50.7, 40.6, 18.5, 36.1, 33.7]),
#     "40577000":np.array([43, 22.2, 34.4, 19.9, 26.5, 30.9, 44.8, 21.8, 34.1, 28.2, 12.9, 39.3, 16.5, 22.5, 26.6, 40.4, 39.3, 23.8, 39.3, 27.4]),
#     "40579995":np.array([93.6, 85.6, 112, 48.4, 103, 62.9, 76.7, 41.2, 54.1, 62.3, 104, 46, 206, 110, 89, 41.2, 112, 44.1, 75.6, 52.8, 72.9, 68.2, 112, 77, 111, 45.5, 30.8, 55.8, 148, 128, 59.4, 50.9, 94.6, 132, 88.2, 132, 54.7, 22.1, 63.4, 19.8, 74.6, 57.2, 55.1, 60.3, 66.5, 84.2, 90.2]),
#     "40665000":np.array([22.6, 19.3, 24.5, 31.5, 23.5, 24.2, 22.1, 30.7, 19.7, 26.2, 25.7, 19.5, 24.4, 25.7, 24.9, 27, 21, 18.9, 14.7, 44.4, 41, 29.1, 33.1, 50.7, 44.7, 39, 46.6, 42.4, 29.5, 52]),
#     "40710000":np.array([457, 350, 220, 268, 190, 147, 378, 330, 295, 207, 150, 350, 670, 403, 336, 385, 460, 451, 374, 785, 287, 322, 418, 161, 397]),
#     "40740000":np.array([315, 356, 255, 182, 474, 410, 351, 456, 723, 457, 460, 432, 519, 443, 387, 816, 345, 423, 455, 222, 715, 300, 336, 461, 372, 1133, 205, 235]),
# }

# vazoes_normalizadas = {
#     k: v/v.mean() for k, v in vazoes_maximas_anuais.items()
# }
# plot_series(
#     series=list(vazoes_normalizadas.values()),
#     nomes_series=list(vazoes_normalizadas.keys())
# )

# loc, scale, form = index_flood(dados=vazoes_maximas_anuais)
# print(f"loc: {loc} | scale: {scale} | form: {form}")


