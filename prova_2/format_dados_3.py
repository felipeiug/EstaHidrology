import pandas as pd
import os

ano_hidrologico1 = [10, 11, 12]
ano_hidrologico2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]

files = os.listdir("prova_2/vazoes_novas_estacao")

dados_save = {}

for file in files:
    df = pd.read_csv(f"prova_2/vazoes_novas_estacao/{file}", sep=";")
    df["Data"] = pd.to_datetime(df["Data"])
    df["Vazao"] = pd.to_numeric(df["Vazao"].str.replace(",", "."), errors="coerce")
    df.fillna(-1)

    codigo = df["CodigoEstacao"].values[0]

    df.sort_values(by="Data", ascending=True, inplace=True, ignore_index=True)

    ano_inicial = df["Data"].min().year
    ano_final = df["Data"].max().year

    if codigo not in dados_save:
        dados_save[codigo] = []

    for ano in range(ano_inicial, ano_final+1):
        ano_init = ano-1

        mask1 = (df["Data"].dt.year == ano_init) & (df["Data"].dt.month.isin(ano_hidrologico1))
        mask2 = (df["Data"].dt.year == ano) & (df["Data"].dt.month.isin(ano_hidrologico2))
        df_ano1 = df[mask1 | mask2]

        if df_ano1.empty:
            continue

        max_vazao = df_ano1["Vazao"].max()

        dados_save[codigo].append(max_vazao)

str_data = ""
for i in range(-1, 1000):
    all_null = True

    data_now = []
    for estacao in dados_save.keys():
        if i < 0:
            data_now.append(str(estacao))
            all_null = False
            continue
        
        if i >= len(dados_save[estacao]):
            vazao = ""
        else:
            vazao = str(dados_save[estacao][i])
            all_null = False
        data_now.append(vazao)
    
    if all_null:
        break

    str_add = "\t".join(data_now)

    str_data += str_add + "\n"

with open("prova_2/dados_formatados_novos.csv", mode="w+") as arq:
    arq.writelines(str_data)

print(dados_save)

