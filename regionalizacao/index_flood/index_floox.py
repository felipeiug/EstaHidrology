from scipy.stats import (
    norm,
    t as t_student,
    chi2,
    gumbel_r
)
import lmoments3 as lm

from numpy import sqrt
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

from papeis_de_plotagem.papel_plotagem_gumbel import papel_gumbel_r, papel_gumbel_l
from solvers.MOM.MOM_gumbel_max import GumbelMax
from distribuicoes.Gumbel.maximos import Gumbel_Max

def index_flood(dados: dict[str, np.ndarray])->tuple[float]:
    """Retorna os parâmetros de localizacao, escala e forma admensionalizados pela média"""

    loc, scale, form = None, None, None

    _, ax = plt.subplots(nrows=1, ncols=2)
    
    ################
    # A) Ánalise de consistência dos dados

    series = []
    nomes = []
    medias = []
    normalizados:list[np.ndarray] = []
    for estacao in dados.keys():
        media = dados[estacao].mean()

        medias.append(media)

        nomes.append(estacao)
        series.append(dados[estacao])
        normalizados.append(dados[estacao]/media)


    papel_gumbel_r(normalizados, nomes, ax=ax[0])


    # B) Organização e admensionalização da série



    # C) Definição das curvas empíricas de frquência de cada estação hidrometeorológica
    
    medias = []
    desvios = []
    alfas = []
    betas = []
    N_s = []
    for n, estacao in enumerate(dados.keys()):
        media = normalizados[n].mean()
        desvio = normalizados[n].std()
        variancia = normalizados[n].var()

        N_s.append(len(normalizados[n]))

        medias.append(media)
        desvios.append(desvio)

        gum_max = GumbelMax(normalizados, media, variancia)
        alfa, beta = gum_max.parametros()

        alfas.append(alfa)
        betas.append(beta)

    alfas = np.array(alfas)
    betas = np.array(betas)
    N_s = np.array(N_s)

    alfa_final = np.round(np.sum(N_s*alfas)/np.sum(N_s), 3)
    beta_final = np.round(np.sum(N_s*betas)/np.sum(N_s), 3)

    loc = alfa_final
    scale = beta_final

    # D) Definição das regiões homogêneas e das curvas de frequência regional

    # E) Análise de regressão

    gumbel_distribuicao = Gumbel_Max(alfa_final, beta_final)

    for i in (1.01, 2, 5, 10, 20, 25, 50, 75, 100, 1000):
        q = gumbel_distribuicao.quantil_TR(i)
        print(i, q)
    
    papel_gumbel_r(normalizados, nomes, ax=ax[1], alfa=alfa_final, beta=beta_final)
    plt.show()

    # F) Estimação de um evento associado a um período de retorno qualquer


    return (loc, scale, form)
