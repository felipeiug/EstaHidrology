import matplotlib.pyplot as plt
from matplotlib.axes._axes import Axes

def diagrama_uniaxial(
    ax:Axes,
    valores:list,
    title_x='Eixo X',
    title_y='Eixo Y',
    title='Diagrama Uniaxial de Pontos',
    show_legenda=False,
):
    y = [0 for _ in valores]

    # Criando o diagrama de dispersão
    ax.scatter(valores, y, color="black")
    ax.plot(valores, y, color='black', linestyle='-', linewidth=1, label='Linha')

    # Adicionando rótulos e título
    ax.set_xlabel(title_x)
    ax.set_ylabel(title_y)
    ax.set_title(title)

    if show_legenda:
        ax.legend()

if __name__ == "__main__":
    # Dados para o diagrama de dispersão
    x = [
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
    ]

    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    diagrama_uniaxial(axs[0], x)
    diagrama_uniaxial(axs[1], x)

    # Exibindo a figura com os subplots
    plt.show()