import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes._axes import Axes

def dados_serie(
    ax_serie:Axes,
    serie:pd.DataFrame,
    col_val:str="valores",
    col_x:str="x",
    intervalos:list|int=None,
    ax_histograma:Axes=None,
    ax_frequencia:Axes=None,
    ax_freq_acum:Axes=None,
    ax_curv_perma:Axes=None,
    ax_metricas:Axes=None,
):
    #Histograma para uma série de dados com 1+3.3log10(N) intervalos

    #Plotando a série
    ax_serie.plot(serie[col_x], serie[col_val])
    ax_serie.set_xlabel(col_x)
    ax_serie.set_ylabel(col_val)
    ax_serie.set_title("Série")

    #Ordenando os valores pela colunas de valores
    serie.sort_values(by=col_val, inplace=True, ignore_index=True)

    # Intervalos em Arrendondar para cima 1+3.3log10(N)
    if intervalos is None:
        intervalos = int(np.ceil(1+3.3*np.log10(len(serie.index))))

    serie['intervalos'] = pd.cut(serie[col_val], bins=intervalos)

    # Contando a frequência de cada intervalo
    frequencia = serie['intervalos'].value_counts().sort_index()
    freq_rel = (frequencia/len(serie.index)).values

    freq_acum = [freq_rel[0]]
    for i in range(1, len(freq_rel)):
        freq_acum.append(freq_acum[i-1]+freq_rel[i])

    # Criando um novo DataFrame com os dados do histograma
    limites_superiores = np.array(list(frequencia.index.map(lambda x: x.right).values))
    limites_inferiores = np.array(list(frequencia.index.map(lambda x: x.left ).values))

    medias = (limites_superiores+limites_inferiores)/2

    histograma = pd.DataFrame({
        'Inter': frequencia.index,
        'InterMed':medias,
        'Freq': frequencia.values,
        "FreqRel":freq_rel,
        "FreqRelAcum": freq_acum,
        "Media":medias,
    })

    #Plotando o histograma
    if ax_histograma is not None:
        serie.hist(column=col_val, bins=intervalos, color='skyblue', edgecolor='black', ax=ax_histograma)
        ax_histograma.set_xlabel("Intervalos")
        ax_histograma.set_ylabel("Frequência Absoluta")
        ax_histograma.set_title("Histograma")
        def get_freq_rel(x):
            return x/len(serie.index)
        sec_ax = ax_histograma.secondary_yaxis('right', functions=(get_freq_rel, lambda x: x))
        sec_ax.set_ylabel('Frequência Relativa')

    #Plotando o Polígono de Frequêcias
    if ax_frequencia is not None:
        ax_frequencia.plot(histograma["Media"], histograma["FreqRel"])
        ax_frequencia.set_xlabel("Intervalos")
        ax_frequencia.set_ylabel("Frequência Absoluta")
        ax_frequencia.set_title("Polígono de Frequências")


    #Dados das frequencias de não superação e curva de permanência
    m = np.arange(1, len(serie.index)+1)
    p_nao_sup = [i/len(m) for i in m]
    p_curv_perm = [(1-i)*100 for i in p_nao_sup]

    freq_nao_sup = pd.DataFrame({
        col_val: serie[col_val],
        "m":m,
        "PNaoSup": p_nao_sup,
        "CurvPerm":p_curv_perm,
    })

    #Plotando as Frequências acumuladas
    if ax_freq_acum is not None:
        ax_freq_acum.plot(freq_nao_sup[col_val], freq_nao_sup["PNaoSup"])
        ax_freq_acum.set_xlabel(col_val)
        ax_freq_acum.set_ylabel("Frequência de Não Superação")
        ax_freq_acum.set_title("Diagrama de Frequências Relativas Acumuladas")

    #Plotando a curva de permanência
    if ax_curv_perma is not None:
        ax_curv_perma.plot(freq_nao_sup["CurvPerm"], freq_nao_sup[col_val])
        ax_curv_perma.set_xlabel("% tempo igual ou superior")
        ax_curv_perma.set_ylabel(f"Valor Médio ({col_val})")
        ax_curv_perma.set_title("Curva de Permanência")


    #Medidas de Tendência Central
    media = serie[col_val].mean()
    mediana = serie[col_val].median()
    moda_amostral = serie[col_val].mode()
    moda_grafico = histograma.loc[histograma["Freq"].idxmax()]["Media"]
    if len(moda_amostral) == 1:
        moda_amostral = moda_amostral.values[0]
    else:
        moda_amostral=None

    #Medidas de dispersão
    variancia = serie[col_val].var()
    desvio_padrao = serie[col_val].std() #Raiz da variância

    #Assimetria e Curtose
    coef_assimetria = serie[col_val].skew()
    coef_curtose = serie[col_val].kurtosis()

    #Quartis
    Q1,Q2,Q3 = serie[col_val].quantile([0.25, 0.5, 0.75])
    AIQ = Q3-Q1

    message = f"""*Medidas de Tendência Central*
Média:         {media:.6f}
Mediana:       {mediana:.6f}
Moda Amostral: {moda_amostral if moda_amostral is not None else "---"}
Moda Gráfica:  {moda_grafico:.6f}

*Medidas de Dispersão*
Variância:     {variancia:.6f}
Desvio Padrão: {desvio_padrao:.6f}

*Assimetria e Curtose*
Coef. de Assimetria: {coef_assimetria:.6f}
Coef. de Curtose:    {coef_curtose:.6f}
Excesso de Curtose:  {(coef_curtose-3):.6f} ({"mesocúrtica" if coef_curtose-3 < 0 else "leptocúrtica" if coef_curtose-3 > 0 else "platicúrtica"})

*Quartis*
1° Quartil: {Q1:.6f}
2° Quartil: {Q1:.6f}
3° Quartil: {Q1:.6f}
Amplitude Inter Quartis: {AIQ:.6f}
Outliers: X<{(Q1-1.5*AIQ):.6f} U X>{(Q3-1.5*AIQ):.6f}
"""
    print(message)
            
    if ax_metricas is not None:
        ax_metricas.axhline(y=media, linestyle='--', label=f'Média: {media}')
        ax_metricas.axhline(y=mediana, linestyle='--', label=f'Mediana: {mediana}')
        if moda_amostral is not None:
            ax_metricas.axhline(y=moda_amostral, linestyle='--', label=f'Moda Amostral: {moda_amostral}')
        ax_metricas.axhline(y=moda_grafico, linestyle='--', label=f'Moda Gráfico: {moda_grafico}')

        ax_metricas.axhline(y=variancia, linestyle='--', label=f'Variância: {variancia}')
        ax_metricas.axhline(y=desvio_padrao, linestyle='--', label=f'Desvio Padrão: {desvio_padrao}')
        
        ax_metricas.axhline(y=coef_assimetria, linestyle='--', label=f'Coef. De Assimetria: {coef_assimetria}')
        ax_metricas.axhline(y=coef_curtose, linestyle='--', label=f'Coef. De Curtose: {coef_curtose}')
        
        
        ax_metricas.axhline(y=Q1, linestyle='--', label=f'1° Quartil: {Q1}')
        ax_metricas.axhline(y=Q2, linestyle='--', label=f'2° Quartil: {Q2}')
        ax_metricas.axhline(y=Q3, linestyle='--', label=f'3° Quartil: {Q3}')
        ax_metricas.axhline(y=0, label=f'AI Quartis: {AIQ}')

        ax_metricas.legend()

    return histograma, freq_nao_sup

if __name__ == "__main__":
    intervalos = [30, 50, 70, 90, 110, 130, 150, 170]
    valores= [
        104.3,
        97.9,
        89.2,
        92.7,
        98,
        141.7,
        81.1,
        97.3,
        72,
        93.9,
        83.8,
        122.8,
        87.6,
        101,
        97.8,
        59.9,
        49.4,
        57,
        68.2,
        83.2,
        60.6,
        50.1,
        68.7,
        117.1,
        80.2,
        43.6,
        66.8,
        118.4,
        110.4,
        99.1,
        71.6,
        62.6,
        61.2,
        46.8,
        79,
        96.3,
        77.6,
        69.3,
        67.2,
        72.4,
        78,
        141.8,
        100.7,
        87.4,
        100.2,
        166.9,
        74.8,
        133.4,
        85.1,
        78.9,
        76.4,
        64.2,
        53.1,
        112.2,
        110.8,
        82.2,
        88.1,
        80.9,
        89.8,
        114.9,
        63.6,
        57.3,
    ]
    anos = [i+1950 for i in range(len(valores))]
    serie = pd.DataFrame({
        "Vazão":valores,
        "Anos":anos,
    })

    fig, axs = plt.subplots(3, 2, figsize=(12, 4))
    df_histograma, df_frequ_nao_sup = dados_serie(axs[0,0], serie, "Vazão", "Anos",
        intervalos=intervalos,
        ax_histograma=axs[0,1],
        ax_frequencia=axs[1,0],
        ax_freq_acum=axs[1,1],
        ax_curv_perma=axs[2,0],
        ax_metricas=axs[2,1],
    )

    plt.show()