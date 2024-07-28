from scipy.stats import norm
import pandas as pd
import numpy as np
from helpers import get_confianca

class Aleatoriedade:
    def __init__(self, serie):
        self.serie = pd.Series(serie)

        self.N = len(self.serie.index)
        
        if self.N <= 30:
            print("\nN da série é menor ou igual a 30. O ideal é que N seja maior que 30!\n")


        self.E_p = 2*(self.N-2)/3
        self.Var_p = (16*self.N - 29)/90

    def aleatorio(self, p:int, alfa:float=0.05):
        """H0: `a amostra é aleatória`\n
        -`p` é a quantidade de picos e vales da amostra ao longo do tempo\n
        Se `verdadeiro` é aleatório,, se `falso` não é aleatório"""
        
        alfa = get_confianca(alfa)

        T = (p-self.E_p)/np.sqrt(self.Var_p)
        t = norm.ppf(1-(alfa/2))

        if abs(T) > t:
            return False
        return True