from scipy.stats import t as t_student
from scipy.stats import norm, chi2
from sympy import symbols, Eq, sqrt, solve
import pandas as pd
import numpy as np
from helpers import get_confianca

class Independencia:
    def __init__(self, serie):
        self.serie = pd.Series(serie)

        x_ = self.serie.mean()
        self.x_ = x_

        s = self.serie.std()
        self.s = s

        N = len(self.serie.index)
        self.N = N

        self.X_linha = self.serie.values - self.x_

        #Calculando o R
        self.R = self.X_linha[0]*self.X_linha[-1]
        for i in range(self.X_linha.size - 1):
            self.R += self.X_linha[i]*self.X_linha[i+1]

        s2 = self.sr(2)
        s4 = self.sr(4)

        self.E_R = -s2/(self.N-1)

        s2_2 = s2**2
        t1 = (s2_2-s4)/(N-1)
        t2 = (s2_2-2*s4)/((N-1)*(N-2))
        t3 = s2_2/((N-1)**2)
        self.Var_R = t1+t2-t3
    
    def sr(self, r:float):
        return self.N*self.m(r)
    
    def m(self, r:float):
        xs = self.X_linha**r
        mr = np.sum(xs)/self.N

        return mr

    def teste_independencia(self, alfa:float=0.05):
        """- Se `verdadeiro` é independente (não rejeito H0), se `falso` não é independente (rejeito H0)"""

        alfa = get_confianca(alfa)

        T = (self.R - self.E_R)/np.sqrt(self.Var_R)
        t = norm.ppf(1-(alfa/2))

        if abs(T) > t:
            return False
        return True

