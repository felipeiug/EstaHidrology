import pandas as pd
import numpy as np

from helpers.math_functions import C
from solvers.MML.MML_gumbel_max import GumbelMax

class MML:
    def __init__(self, xs:list|tuple|set|np.ndarray|pd.Series):
        # Dados
        if isinstance(xs, pd.Series):
            xs = xs.sort_values(ignore_index=True)
            xs = xs.values
        elif not isinstance(xs, np.ndarray):
            xs = np.array(xs)
            xs.sort()

        self.xs = np.round(xs, decimals=6)

        # Variáveis iniciais
        self.alfa_0 = np.round(self.alfa_s(0), decimals=6)
        self.alfa_1 = np.round(self.alfa_s(1), decimals=6)
        self.alfa_2 = np.round(self.alfa_s(2), decimals=6)
        self.alfa_3 = np.round(self.alfa_s(3), decimals=6)

        self.beta_0 = np.round(self.beta_r(0), decimals=6)
        self.beta_1 = np.round(self.beta_r(1), decimals=6)
        self.beta_2 = np.round(self.beta_r(2), decimals=6)
        self.beta_3 = np.round(self.beta_r(3), decimals=6)

        self.l1=np.round(self.alfa_0, decimals=6)
        self.l2=np.round(self.alfa_0-2*self.alfa_1, decimals=6)
        self.l3=np.round(self.alfa_0-6*self.alfa_1+6*self.alfa_2, decimals=6)
        self.l4=np.round(self.alfa_0-12*self.alfa_1+30*self.alfa_2-20*self.alfa_3, decimals=6)
        
        self.tau=    np.round(self.l2/self.l1, decimals=6)
        self.tau_3 = np.round(self.l3/self.l2, decimals=6)
        self.tau_4 = np.round(self.l4/self.l2, decimals=6)

        self.gumbel_max = GumbelMax(xs, self.l1, self.l2)

    # Alfa do MML
    def alfa_s(self, s:int):
        N = len(self.xs)
        i = np.array([i for i in range(1, N+1)])

        num = C(N-i, s)
        num_xs = self.xs * num

        if isinstance(num_xs, (np.ndarray, pd.Series)):
            num_xs[np.isnan(num_xs)|np.isinf(num_xs)] = 0
        
        sum1 = np.sum(num_xs)

        den = C(N-1, s)

        divisao = sum1/den

        val = (1/N)*divisao
        return val

    # Beta do MML
    def beta_r(self, r:int):
        N = len(self.xs)
        i = np.array([i for i in range(1, N+1)])

        num = C(i-1, r)
        vals_sum = self.xs*num

        if isinstance(vals_sum, (np.ndarray, pd.Series)):
            vals_sum[np.isnan(vals_sum)|np.isinf(vals_sum)] = 0

        sum1 = np.sum(vals_sum)

        den = C(N-1, r)

        divisao = sum1/den

        val = (1/N)*divisao

        return val

    # Valores da normal
    def normal(self):
        mi = np.round(self.l1, decimals=4)
        sigma = np.round(self.l2*np.sqrt(np.pi), decimals=4)

        return mi, sigma
    
    # Valores da exponencial
    def exponencial(self):
        teta = np.round(self.l1, decimals=4)
        return teta
    
    # Valores da exponencial
    def uniforme(self):
        b = np.round(3*self.l2 + self.l1, decimals=4)
        a = np.round(2*self.l1-b, decimals=4)
        return a, b

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

    mml = MML(serie)

    print(mml)