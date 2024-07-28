from scipy.stats import t as t_student
from scipy.stats import norm, chi2
from sympy import symbols, Eq, sqrt, solve
import pandas as pd
import numpy as np
from helpers import get_confianca

class Estacionariedade:
    def __init__(self, serie, tempos):
        self.serie = pd.Series(serie)

        N = self.serie.values.size
        self.N = N

        x_ = self.serie.mean()
        self.x_ = x_
        s = self.serie.std()
        self.s = s

        # Ordenando a série
        df_serie = pd.DataFrame({
            "dados": self.serie,
            "tempo":tempos,
        })

        df_serie = df_serie.sort_values(by="dados", ignore_index=True)
        df_serie["m"] = [i for i in range(1, self.serie.size+1)]

        df_serie = df_serie.sort_values(by="tempo", ignore_index=True)
        df_serie["T"] = [i for i in range(1, self.serie.size+1)]

        m_T = np.sum((df_serie["m"] - df_serie["T"])**2)
        self.rs = 1 - (6*m_T)/((N**3)-N)

        self.E_rs = 0
        self.Var_rs = 1/(N-1)


    def teste_estacionariedade(self, alfa:float=0.05):
        """H0: `a amostra não apresenta tendência temporal`\n
        - Se False rejeito H0"""

        alfa = get_confianca(alfa)

        T = self.rs/np.sqrt(self.Var_rs)
        t = norm.ppf(1-(alfa/2))

        if abs(T) > t:
            return False
        return True

