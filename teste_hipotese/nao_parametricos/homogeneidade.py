from scipy.stats import t as t_student
from scipy.stats import norm, chi2
from sympy import symbols, Eq, sqrt, solve
import pandas as pd
import numpy as np
from helpers import get_confianca

class Homogeneidade:
    def __init__(self, serie):
        self.serie = pd.Series(serie)

        N1 = int(np.floor(self.serie.values.size/2))
        N2 = int(np.ceil(self.serie.values.size/2))

        self.N1 = N1
        self.N2 = N2

        serie1 = self.serie.values[:N1]
        serie2 = self.serie.values[N1:N1+N2]

        self.serie1 = serie1
        self.serie2 = serie2

        x_1 = serie1.mean()
        self.x_1 = x_1
        x_2 = serie2.mean()
        self.x_2 = x_2

        s_1 = serie1.std()
        self.s_1 = s_1
        s_2 = serie2.std()
        self.s_2 = s_2

        # Ordenando a série
        df_serie = pd.DataFrame({"dados": self.serie})

        df_serie["pertence1"] = self.serie.isin(serie1)
        df_serie["pertence2"] = self.serie.isin(serie2)

        df_serie = df_serie.sort_values(by="dados", ignore_index=True)
        df_serie["m"] = [i for i in range(1, self.serie.size + 1)]

        self.df_serie = df_serie

        m_1_amostra = df_serie[df_serie["pertence1"]]["m"].values
        R1 = np.sum(m_1_amostra)
        
        self.V1 = N1*N2 + ((N1*(N1+1))/2)-R1
        self.V2 = N1*N2 - self.V1

        self.V = min(self.V1, self.V2)

        self.E_V = N1*N2/2
        self.Var_V = (N1*N2*(N1+N2+1))/12


    def teste_homogeneidade(self, alfa:float=0.05):
        """H0: `a amostra é homogênea`\n
        - Se False rejeito H0"""

        alfa = get_confianca(alfa)

        T = (self.V - self.E_V)/np.sqrt(self.Var_V)
        t = norm.ppf(1-(alfa/2))

        if abs(T) > t:
            return False
        return True

