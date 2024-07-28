from papeis_de_plotagem.papel_plotagem_gumbel import papel_gumbel_r, papel_gumbel_l
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def plot_series(series:list[np.ndarray], nomes_series:list[str]=None):
    _, axs = plt.subplots(nrows=3, ncols=2)

    for func in dir(stats):
        if func.startswith("_") or func.endswith("_"):
            continue
        
        func = getattr(stats, func)

        if "ppf" not in dir(func) or "pdf" not in dir(func) or "cdf" not in dir(func):
            continue
        
        print(func)

    plt.show()