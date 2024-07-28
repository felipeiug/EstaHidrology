from scipy.stats import (
    norm,
    t as t_student,
    chi2,
)
import lmoments3 as lm

from numpy import sqrt
import numpy as np
import pandas as pd
import os

data = pd.read_csv("prova_2\dados_formatados_novos.csv", sep="\t")

for estacao in data.columns:
    
    dados_estacao = data[estacao].values
    dados_estacao = [str(i) for i in dados_estacao]
    with open("prova_2/dados_alea_novos/" + str(estacao) + ".txt", mode="w+") as arq:
        arq.write("\n".join(dados_estacao))

str_data = ""
for i in range(-1, 1000):
    all_null = True

    data_now = []
    for estacao in data.keys():
        if i < 0:
            data_now.append(estacao)
            all_null = False
            continue
        
        if i >= len(data[estacao]):
            vazao = ""
        else:
            vazao = str(data[estacao][i])
            all_null = False
        data_now.append(vazao)
    
    if all_null:
        break

    str_add = "\t".join(data_now)

    str_data += str_add + "\n"

with open("Prova 2/dados_formatados_antigos.csv", mode="w+") as arq:
    arq.writelines(str_data)

lmoments = lm.lmom_ratios(data)




