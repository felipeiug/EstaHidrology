import numpy as np
from scipy.stats import lognorm, gumbel_r, gumbel_l
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.ticker import FuncFormatter

from distribuicoes.Gumbel.maximos import Gumbel_Max

def papel_gumbel_r(
    series:list[np.ndarray] | np.ndarray,
    nomes_series:list[str]= None,
    alfa: float = None,
    beta: float = None,
    ax:Axes = None
):
    dist = gumbel_r()

    if ax is None:
        ax:Axes = plt

    N = 0
    if len(series) > 0 and not isinstance(series, np.ndarray):
        for serie in series:
            if serie.size > N:
                N = serie.size

    for n, serie in enumerate(series):
        serie.sort()

        # Posição de plotagem
        x = np.arange(1, serie.size+1)
        x = (x-0.44)/(serie.size+0.12)
        x_plot:np.ndarray = dist.ppf(x)

        nome = str(n)
        if nomes_series is not None and len(nomes_series) > n:
            nome = nomes_series[n]

        ax.scatter(x_plot, serie, label=nome)


    if alfa is not None and beta is not None:
        dist_now = Gumbel_Max(alfa=alfa, beta=beta)

        # Posição de plotagem
        Tr = np.linspace(1.01, 1000, 100)
        y = dist_now.quantil_TR(Tr)["quan"]

        x_plot:np.ndarray = dist.ppf(1-1/Tr)

        ax.plot(x_plot, y, "-", label=f"α: {alfa}\nβ: {beta}")


    def formatador(y_now, _):
        p_now = dist.cdf(y_now)
        Tr_now = 1/(1-p_now)

        num_str = str(np.round(Tr_now, 3))
        if int(num_str.split(".")[1]) > 0:
            num_str = float(num_str)
        else:
            num_str = int(num_str.split(".")[0])

        return f"${num_str}$"

    try:
        ax.gca().xaxis.set_major_formatter(FuncFormatter(formatador))
        ax.xticks([
            dist.ppf(1-1/1.01),
            dist.ppf(1-1/2),
            dist.ppf(1-1/5),
            dist.ppf(1-1/10),
            dist.ppf(1-1/25),
            dist.ppf(1-1/50),
            dist.ppf(1-1/100),
            dist.ppf(1-1/1000),
        ])

        ax.ylabel("Quantil")
        ax.xlabel("Tr (Anos)")
        ax.title("Papel de Plotagem Gumbel R")

    except AttributeError as e:
        ax.xaxis.set_major_formatter(FuncFormatter(formatador))
        ax.set_xticks([
            dist.ppf(1-1/1.01),
            dist.ppf(1-1/2),
            dist.ppf(1-1/5),
            dist.ppf(1-1/10),
            dist.ppf(1-1/25),
            dist.ppf(1-1/50),
            dist.ppf(1-1/100),
            dist.ppf(1-1/1000),
        ])

        ax.set_ylabel("Quantil")
        ax.set_xlabel("Tr (Anos)")

        ax.set_title("Papel de Plotagem Gumbel R")

    ax.grid(True)
    ax.legend()

def papel_gumbel_l(series:list[np.ndarray] | np.ndarray, nomes_series:list[str]= None, ax:Axes = None):
    dist = gumbel_l()

    if ax is None:
        ax:Axes = plt

    N = 0
    if len(series) > 0 and not isinstance(series, np.ndarray):
        for serie in series:
            if serie.size > N:
                N = serie.size

    for n, serie in enumerate(series):
        serie.sort()

        # Posição de plotagem
        x = np.arange(1, serie.size+1)
        x = (x-0.44)/(serie.size+0.12)
        x_plot:np.ndarray = dist.ppf(x)

        nome = str(n)
        if nomes_series is not None and len(nomes_series) > n:
            nome = nomes_series[n]

        ax.scatter(x_plot, serie, label=nome)

    def formatador(y_now, _):
        p_now = dist.cdf(y_now)
        Tr_now = 1/(1-p_now)

        num_str = str(np.round(Tr_now, 3))
        if int(num_str.split(".")[1]) > 0:
            num_str = float(num_str)
        else:
            num_str = int(num_str.split(".")[0])

        return f"${num_str}$"

    try:
        ax.gca().xaxis.set_major_formatter(FuncFormatter(formatador))
        ax.xticks([
            dist.ppf(1-1/1.01),
            dist.ppf(1-1/2),
            dist.ppf(1-1/5),
            dist.ppf(1-1/10),
            dist.ppf(1-1/25),
            dist.ppf(1-1/50),
            dist.ppf(1-1/100),
            dist.ppf(1-1/1000),
        ])

        ax.ylabel("Quantil")
        ax.xlabel("Tr (Anos)")
        ax.title("Papel de Plotagem Gumbel L")

    except AttributeError as e:
        ax.xaxis.set_major_formatter(FuncFormatter(formatador))
        ax.set_xticks([
            dist.ppf(1-1/1.01),
            dist.ppf(1-1/2),
            dist.ppf(1-1/5),
            dist.ppf(1-1/10),
            dist.ppf(1-1/25),
            dist.ppf(1-1/50),
            dist.ppf(1-1/100),
            dist.ppf(1-1/1000),
        ])

        ax.set_ylabel("Quantil")
        ax.set_xlabel("Tr (Anos)")

        ax.set_title("Papel de Plotagem Gumbel L")

    ax.grid(True)
    ax.legend()