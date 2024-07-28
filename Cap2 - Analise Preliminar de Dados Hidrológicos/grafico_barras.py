import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes._axes import Axes

def bar_chart(
    ax:Axes,
    valores:dict[str, list[float]],
    categorias:list,
    title_x='Número de Cheias Anuais',
    title_y='Número de Ocorrências',
    title='Gráfico de Barras',
    largura_barra = 0.3,
    show_legenda=True,
):
    x = np.arange(len(categorias))
    start_eixo=len(valores)/2

    for n, (key, val) in enumerate(valores.items()):
        deslocamento = largura_barra*(n - start_eixo + 0.5)
        ax.bar(x+deslocamento, val, largura_barra, label=key)

    ax.set_xlabel(title_x)
    ax.set_ylabel(title_y)
    ax.set_title(title)

    #Categorias no eixo X
    ax.set_xticks(x, categorias)

    if show_legenda:
        ax.legend()

if __name__ == "__main__":
    fig, ax = plt.subplots(1, 1, figsize=(12, 4))

    categorias = range(1, 9)
    valores = {
        "Série 1": [2, 6, 7, 9, 4, 1, 4, 1],
        "Série 2": [2, 6, 7, 9, 4, 1, 4, 1],
    }

    bar_chart(ax, valores=valores, categorias=categorias)

    plt.show()