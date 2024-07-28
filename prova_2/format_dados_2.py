from scipy.stats import (
    norm,
    t as t_student,
    chi2,
)
import lmoments3 as lm

from numpy import sqrt
import pandas as pd
import numpy as np
import calendar
import os

files = os.listdir("prova_2/vazoes_novas")

data:dict[str, list[float]] = {}
for file in files:
    estacao = file.replace(".txt", "")
    df = pd.read_csv(f"prova_2/vazoes_novas/{file}", skiprows=15, sep=";", encoding='ISO-8859-1')

    df.rename(columns={"DataHora": "Data"}, inplace=True)
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
    df.sort_values(by="Data", ascending=False, inplace=True, ignore_index=True)

    datas_diarias = []
    vazoes_diarias = []
    vazoes_status = []
    metodos_obtencao = []
    niveis_consistencia = []

    for _, vazao_mensal in df.iterrows():
        mes = vazao_mensal["Data"].month
        ano = vazao_mensal["Data"].year

        _, numero_de_dias = calendar.monthrange(ano, mes)

        # Criando os dias no intervalo
        date_range = pd.date_range(
            start=f"{ano}-{mes}-01", periods=numero_de_dias, freq="D"
        )
        datas_diarias.extend(date_range)
        vazoes_diarias.extend(vazao_mensal.values[15 : 15 + numero_de_dias])
        vazoes_status.extend(
            vazao_mensal.values[
                15 + numero_de_dias : 15 + numero_de_dias + numero_de_dias
            ]
        )
        metodos_obtencao.extend(
            [vazao_mensal["MetodoObtencaoVazoes"]] * numero_de_dias
        )
        niveis_consistencia.extend(
            [vazao_mensal["NivelConsistencia"]] * numero_de_dias
        )

    df_vazoes = pd.DataFrame()
    df_vazoes["Data"] = datas_diarias
    df_vazoes["Vazao"] = vazoes_diarias
    df_vazoes["VazaoStatus"] = vazoes_status
    df_vazoes["Unidades"] = "m³/s"
    df_vazoes["MetodoObtencao"] = metodos_obtencao
    df_vazoes["NivelConsistencia"] = niveis_consistencia
    df_vazoes["CodigoEstacao"] = estacao
    df_vazoes["Responsavel"] = "ANA"

    df_vazoes.to_csv(f"prova_2/vazoes_novas_estacao/{estacao}.csv", index=False, sep=";")




