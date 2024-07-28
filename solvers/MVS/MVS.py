import pandas as pd
import numpy as np

from helpers.val_to_np import val_to_np

#Distribuições
from solvers.MVS.MVS_Gumbel_max import *

class MVS:
    def __init__(self, xs:list|tuple|set|np.ndarray|pd.Series):

        # Dados
        xs = val_to_np(xs)
        xs.sort()

        self.xs = np.round(xs, decimals=6)

        self.gumbel_max = GumbelMax(xs)

if __name__ == "__main__":
    # Dados de entrada
    serie = [
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

    mom = MVS(serie)

    print(mom)