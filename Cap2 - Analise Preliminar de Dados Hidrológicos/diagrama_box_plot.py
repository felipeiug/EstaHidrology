import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes._axes import Axes

def box_plot(ax:Axes, serie:pd.DataFrame, col_val="value"):
    serie.boxplot(column=col_val, ax=ax, grid=False)

if __name__ == "__main__":
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

    fig, axs = plt.subplots(1, 1)
    box_plot(axs, serie, "Vazão")

    plt.show()