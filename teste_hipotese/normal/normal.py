from scipy.stats import t as t_student
from scipy.stats import norm, chi2
from sympy import symbols, Eq, sqrt, solve
import numpy as np
import pandas as pd

from helpers import get_confianca

# Testes de Hipoteses
class μ:
    def __init__(self, serie:pd.Series, x_, s, N, mi:float=None, sigma:float=None):
        self.serie:pd.Series = serie

        self.x_ = x_
        self.s = s
        self.N = N

        self.mi = mi
        self.sigma = sigma

    def H0_equals_H1_different(self, μ1: float, μ2:float=None, alfa:float=5):
        """Caso sej apassado um μ1 somente:
        - Serão comparadas as hipóteses: `H0`: μ=μ1 e `H1`: μ!=μ1\n
        Se não:
        - Serão comparadas as hipóteses:`H0`: μ=μ1 e `H1`: μ=μ2
        """

        alfa = get_confianca(alfa)

        # Caso conheça σ²
        if self.sigma is not None:
            eq = (self.x_-μ1)/(self.sigma/np.sqrt(self.N))

            if μ2 is None:
                alfa = 1-(alfa/2)
                z_alfa = norm.ppf(alfa)

                if abs(eq) > z_alfa:
                    return False
                
                return True
            
            else:
                alfa = 1-alfa
                z_alfa = norm.ppf(alfa)

                if (μ1 > μ2 and eq < -z_alfa) or (μ1 < μ2 and eq > z_alfa):
                    return False
                
                return True
        
        # Caso não conheça σ²
        eq = (self.x_-μ1)/(self.s/np.sqrt(self.N))

        if μ2 is None:
            alfa = 1-(alfa/2)
            t_alfa = t_student.ppf(alfa, self.N-1)

            print(f"t: {eq}")
            print(f"T({(alfa*100):.2f}%): {t_alfa}")

            if abs(eq) > t_alfa:
                return False
            
            return True

        else:
            alfa = 1-alfa
            t_alfa = t_student.ppf(alfa, self.N-1)

            print(f"t: {eq}")
            print(f"T({(alfa*100):.2f}%): {t_alfa}")

            if (μ1 > μ2 and eq < -t_alfa) or (μ1 < μ2 and eq > t_alfa):
                return False
            
            return True
        
    def H0_equals_H1_above(self, μ1: float, alfa:float=5):
        """Serão comparadas as hipóteses:`H0`: μ=μ1 e `H1`: μ>μ1"""

        alfa = get_confianca(alfa)

        # Caso conheça σ²
        if self.sigma is not None:
            eq = (self.x_-μ1)/(self.sigma/np.sqrt(self.N))

            alfa = 1-alfa
            z_alfa = norm.ppf(alfa)

            if abs(eq) > z_alfa:
                return False
            
            return True
        
        # Caso não conheça μ²
        eq = (self.x_-μ1)/(self.s/np.sqrt(self.N))
        alfa = 1-alfa
        t_alfa = t_student.ppf(alfa, self.N-1)

        if abs(eq) > t_alfa:
            return False
        
        return True
    
    def H0_equals_H1_under(self, μ1: float, alfa:float=5):
        """Serão comparadas as hipóteses:`H0`: μ=μ1 e `H1`: μ<μ1"""
        return self.H0_equals_H1_above(μ1, alfa)

class σ:
    def __init__(self, serie:pd.Series, x_, s, N, mi:float=None, sigma:float=None):
        self.serie:pd.Series = serie

        self.x_ = x_
        self.s = s
        self.N = N

        self.mi = mi
        self.sigma = sigma
        
    def H0_equals_H1_different(self, σ1: float, alfa:float=5):
        """- Serão comparadas as hipóteses:`H0`: σ=σ1 e `H1`: σ!=σ1
        """

        alfa = get_confianca(alfa)

        # Caso conheça μ²
        if self.mi is not None:
            Q = self.N * (self.s**2)/(σ1**2)
            
            alfa1 = alfa/2
            alfa2 = 1-alfa1

            v1 = chi2.ppf(alfa1, self.N)
            v2 = chi2.ppf(alfa2, self.N)

            if Q < v1 or Q > v2:
                return False
            
            return True
        
        # Caso não conheça μ²
        K = (self.N-1) * (self.s**2)/(σ1**2)

        alfa1 = alfa/2
        alfa2 = 1-alfa1

        v1 = chi2.ppf(alfa1, self.N)
        v2 = chi2.ppf(alfa2, self.N)

        print(f"chi: {K}")
        print(f"CHI²[1]({(alfa1*100):.2f}%, {self.N}): {v1}")
        print(f"CHI²[2]({(alfa2*100):.2f}%, {self.N}): {v2}")

        if K < v1 or K > v2:
            return False
        
        return True
        
    def H0_equals_H1_above(self, σ1: float, alfa:float=5):
        """Serão comparadas as hipóteses:`H0`: σ=σ1 e `H1`: σ>σ1"""

        alfa = get_confianca(alfa)

        # Caso conheça μ²
        if self.mi is not None:
            Q = self.N * (self.s**2)/(σ1**2)
            v1 = chi2.ppf(1-alfa, self.N)

            if Q > v1:
                return False
            
            return True
        
        # Caso não conheça μ²
        K = (self.N-1) * (self.s**2)/(σ1**2)
        v1 = chi2.ppf(1-alfa, self.N-1)

        if K > v1:
            return False
        
        return True
    
    def H0_equals_H1_under(self, σ1: float, alfa:float=5):
        """Serão comparadas as hipóteses:`H0`: σ=σ1 e `H1`: σ<σ1"""

        alfa = get_confianca(alfa)

        # Caso conheça μ²
        if self.mi is not None:
            Q = self.N * (self.s**2)/(σ1**2)
            v1 = chi2.ppf(alfa, self.N)

            if Q < v1:
                return False
            
            return True
        
        # Caso não conheça μ²
        K = (self.N-1) * (self.s**2)/(σ1**2)
        v1 = chi2.ppf(alfa, self.N-1)

        if K < v1:
            return False
        
        return True

class Normal:
    def __init__(self, serie:np.ndarray|pd.Series|list|tuple|set, media_pop:float=None, desvio_pop:float=None):
        self.serie = pd.Series(serie)

        self.x_ = 5.4 #self.serie.mean()
        self.s = 1.8  #self.serie.std()
        self.N = 20 #len(self.serie.index)

        self.mi = media_pop
        self.sigma = desvio_pop

        self.μ = μ(
            serie=self.serie,
            x_ = self.x_,
            s = self.s,
            N = self.N,
            mi=self.mi,
            sigma=self.sigma,
        )
        self.σ = σ(
            serie=self.serie,
            x_ = self.x_,
            s = self.s,
            N = self.N,
            mi=self.mi,
            sigma=self.sigma,
        )


