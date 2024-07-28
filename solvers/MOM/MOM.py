import pandas as pd
import numpy as np
from sympy import symbols, log as ln, sqrt, pi

from helpers.val_to_np import val_to_np
from solvers.MOM.MOM_gumbel_max import *
from solvers.MOM.MOM_gumbel_min import *

#Distribuições
from solvers.MOM.MOM_frechet import frechet

class MOM:
    def __init__(self, xs:list|tuple|set|np.ndarray|pd.Series):

        # Dados
        xs = val_to_np(xs)
        xs.sort()

        self.xs = np.round(xs, decimals=6)

        data_pd = pd.Series(self.xs)

        # Variáveis iniciais
        self.mean = data_pd.mean()
        self.median = data_pd.median()
        self.mode = data_pd.mode()

        #Medidas de dispersão
        self.var = data_pd.var()
        self.std = data_pd.std() #Raiz da variância

        #Assimetria e Curtose
        self.assimetria = data_pd.skew()
        self.curtose = data_pd.kurtosis()

        #Quartis
        self.Q1, self.Q2, self.Q3 = data_pd.quantile([0.25, 0.5, 0.75])
        self.AIQ = self.Q3-self.Q1

        #Gumbel max e min
        self.gumbel_max = GumbelMax(self.xs, self.mean, self.var)
        self.gumbel_min = gum_min(self.mean, self.var) 
    
    #Para a Frechet
    def frechet_max(self):
        return frechet(self.mean, self.std/self.mean)


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

    mom = MOM(serie)

    print(mom)