from scipy.stats import t as t_student, f as f_snedecor
from scipy.stats import norm, chi2
from sympy import symbols, Eq, sqrt, solve
import numpy as np
import pandas as pd

from helpers import get_confianca

# Testes de Hipoteses
class μ:
    def __init__(
        self,
        serie1:pd.Series, x_1, s1, N1,
        serie2:pd.Series, x_2, s2, N2,
        mi1:float=None, sigma1:float=None,
        mi2:float=None, sigma2:float=None,
    ):
        # Série 1
        self.serie1:pd.Series = serie1

        self.x_1 = x_1
        self.s1 = s1
        self.N1 = N1

        self.mi1 = mi1
        self.sigma1 = sigma1
        
        # Série 2
        self.serie2:pd.Series = serie2

        self.x_2 = x_2
        self.s2 = s2
        self.N2 = N2

        self.mi2 = mi2
        self.sigma2 = sigma2

    def H0_equals_H1_different(self, δ:float, sigma_x_sigma_y:bool = True, alfa:float=5):
        """`sigma_x_sigma_y` refere-se a se o valore de σx é supostamente igual a σy\n
        Verifica se μx - μy = δ contra μx - μy != δ
        Retorna:
        - True: se não rejeito H0\n
        - False: se rejeito H0"""

        alfa = get_confianca(alfa)

        # Caso conheça σ1 e σ2
        if self.sigma1 is not None and self.sigma2 is not None:
            numerador = (self.x_1 - self.x_2) - δ

            par1 = (self.sigma1**2)/self.N1
            par2 = (self.sigma2**2)/self.N2

            denominador = np.sqrt(par1+par2)

            Z = numerador/denominador

            z = norm.ppf(1-(alfa/2))

            if abs(Z) > z:
                return False
            return True

        # Caso não conheça σ1 e σ2 mas supostamente eles são iguais
        elif sigma_x_sigma_y:
            numerador = (self.x_1 - self.x_2) - δ

            par1 = (self.N1-1)*self.s1**2
            par2 = (self.N2-1)*self.s2**2

            denominador = np.sqrt(par1 + par2)
            
            numerador_raiz = self.N1*self.N2*(self.N1+self.N2-2)
            denominador_raiz = self.N1 + self.N2
            raiz= np.sqrt(numerador_raiz/denominador_raiz)

            T = (numerador/denominador)*raiz

            t = t_student.ppf(1-(alfa/2), self.N1 + self.N2 - 2)

            if abs(T) > t:
                return False
            return True

        # Caso não conheça σ1 e σ2 mas supostamente eles são diferentes
        else:

            sN1 = (self.s1**2)/self.N1
            sN2 = (self.s2**2)/self.N2

            numerador = (self.x_1 - self.x_2) - δ

            denominador = np.sqrt(sN1 + sN2)

            T = (numerador/denominador)

            numerador = (sN1 + sN2)**2

            par1 = (sN1**2)/(self.N1-1)
            par2 = (sN2**2)/(self.N2-1)

            denominador = par1 + par2

            v = numerador/denominador

            t = t_student.ppf(1-(alfa/2), v)

            if abs(T) > t:
                return False
            return True
        
    def H0_equals_H1_above(self, δ:float, sigma_x_sigma_y:bool = True, alfa:float=5):
        """`sigma_x_sigma_y` refere-se a se o valore de σx é supostamente igual a σy\n
        Verifica se μx - μy = δ contra μx - μy > δ
        Retorna:
        - True: se não rejeito H0\n
        - False: se rejeito H0"""

        alfa = get_confianca(alfa)

        # Caso conheça σ1 e σ2
        if self.sigma1 is not None and self.sigma2 is not None:
            numerador = (self.x_1 - self.x_2) - δ

            par1 = (self.sigma1**2)/self.N1
            par2 = (self.sigma2**2)/self.N2

            denominador = np.sqrt(par1+par2)

            Z = numerador/denominador
            z = norm.ppf(1-alfa)

            if abs(Z) > z:
                return False
            return True

        # Caso não conheça σ1 e σ2 mas supostamente eles são iguais
        elif sigma_x_sigma_y:
            numerador = (self.x_1 - self.x_2) - δ

            par1 = (self.N1-1)*self.s1**2
            par2 = (self.N2-1)*self.s2**2

            denominador = np.sqrt(par1 + par2)
            
            numerador_raiz = self.N1*self.N2*(self.N1+self.N2-2)
            denominador_raiz = self.N1 + self.N2
            raiz= np.sqrt(numerador_raiz/denominador_raiz)

            T = (numerador/denominador)*raiz
            t = t_student.ppf(1-alfa, self.N1 + self.N2 - 2)

            if abs(T) > t:
                return False
            return True

        # Caso não conheça σ1 e σ2 mas supostamente eles são diferentes
        else:
            numerador = (self.x_1 - self.x_2) - δ

            par1 = (self.N1)*self.s1**2
            par2 = (self.N2)*self.s2**2

            denominador = np.sqrt(par1 + par2)

            T = (numerador/denominador)

            sN1 = (self.s1**2)/self.N1
            sN2 = (self.s2**2)/self.N2

            numerador = (sN1 + sN2)**2

            par1 = (sN1**2)/(self.N1-1)
            par2 = (sN2**2)/(self.N2-1)

            denominador = par1 + par2

            v = numerador/denominador

            t = t_student.ppf(1-alfa, v)

            if abs(T) > t:
                return False
            return True
    
    def H0_equals_H1_under(self, δ:float, sigma_x_sigma_y:bool = True, alfa:float=5):
        """`sigma_x_sigma_y` refere-se a se o valore de σx é supostamente igual a σy\n
        Verifica se μx - μy = δ contra μx - μy < δ
        Retorna:
        - True: se não rejeito H0\n
        - False: se rejeito H0"""

        return self.H0_equals_H1_above(δ, sigma_x_sigma_y, alfa)

class σ:
    def __init__(
        self,
        serie1:pd.Series, x_1, s1, N1,
        serie2:pd.Series, x_2, s2, N2,
        mi1:float=None, sigma1:float=None,
        mi2:float=None, sigma2:float=None,
    ):
        # Série 1
        self.serie1:pd.Series = serie1

        self.x_1 = x_1
        self.s1 = s1
        self.N1 = N1

        self.mi1 = mi1
        self.sigma1 = sigma1
        
        # Série 2
        self.serie2:pd.Series = serie2

        self.x_2 = x_2
        self.s2 = s2
        self.N2 = N2

        self.mi2 = mi2
        self.sigma2 = sigma2
        
    def H0_equals_H1_different(self, σ1: float, σ2: float, alfa:float=5):
        """- Serão comparadas as hipóteses:`H0`: σ1²/σ2² = 1 e `H1`: σ1²/σ2² != 1
        """

        alfa = get_confianca(alfa)
            
        alfa1 = alfa/2
        alfa2 = 1-alfa1

        # Caso conheça μ²
        if self.mi1 is not None and self.mi2 is not None:
            num = (self.s1**2)/(σ1**2)
            den = (self.s2**2)/(σ2**2)

            Q = num/den

            q1 = f_snedecor.ppf(alfa1, self.N1, self.N2)
            q2 = f_snedecor.ppf(alfa2, self.N1, self.N2)

            if Q < q1 or Q > q2:
                return False
            return True
        
        # Caso não conheça μ²
        num = (self.s1**2)/(σ1**2)
        den = (self.s2**2)/(σ2**2)
        F = num/den

        f1 = f_snedecor.ppf(alfa1, self.N1-1, self.N2-1)
        f2 = f_snedecor.ppf(alfa2, self.N1-1, self.N2-1)

        if F < f1 or F > f2:
            return False
        return True
        
    def H0_equals_H1_above(self, σ1: float, σ2: float, alfa:float=5):
        """- Serão comparadas as hipóteses:`H0`: σ1²/σ2² = 1 e `H1`: σ1²/σ2² > 1"""

        alfa = get_confianca(alfa)
        alfa = 1-alfa

        # Caso conheça μ
        if self.mi1 is not None and self.mi2 is not None:
            num = (self.s1**2)/(σ1**2)
            den = (self.s2**2)/(σ2**2)

            Q = num/den
            q = f_snedecor.ppf(alfa, self.N1, self.N2)

            if Q > q:
                return False
            return True
        
        # Caso não conheça μ
        num = (self.s1**2)/(σ1**2)
        den = (self.s2**2)/(σ2**2)
        F = num/den
        f = f_snedecor.ppf(alfa, self.N1-1, self.N2-1)

        if  F > f:
            return False
        return True
    
    def H0_equals_H1_under(self, σ1: float, σ2: float, alfa:float=5):
        """- Serão comparadas as hipóteses:`H0`: σ1²/σ2² = 1 e `H1`: σ1²/σ2² < 1"""

        alfa = get_confianca(alfa)

        # Caso conheça μ1 e μ2
        if self.mi1 is not None and self.mi2 is not None:
            num = (self.s1**2)/(σ1**2)
            den = (self.s2**2)/(σ2**2)

            Q = num/den
            q = f_snedecor.ppf(alfa, self.N1, self.N2)

            if Q < q:
                return False
            return True
        
        # Caso não conheça μ²
        num = (self.s1**2)/(σ1**2)
        den = (self.s2**2)/(σ2**2)
        F = num/den
        f = f_snedecor.ppf(alfa, self.N1-1, self.N2-1)

        if  F < f:
            return False
        return True



class Normal2Series:
    def __init__(
        self,
        serie1:np.ndarray|pd.Series|list|tuple|set,
        serie2:np.ndarray|pd.Series|list|tuple|set,
        media_pop1:float=None,
        desvio_pop1:float=None,
        media_pop2:float=None,
        desvio_pop2:float=None,
    ):
        # Serie 1
        self.serie1 = pd.Series(serie1)

        self.x_1 = self.serie1.mean()
        self.s1 = self.serie1.std()
        self.N1 = len(self.serie1.index)

        self.mi1 = media_pop1
        self.sigma1 = desvio_pop1

        # Serie 2
        self.serie2 = pd.Series(serie2)

        self.x_2 = self.serie2.mean()
        self.s2 = self.serie2.std()
        self.N2 = len(self.serie2.index)

        self.mi2 = media_pop2
        self.sigma2 = desvio_pop2

        self.μ = μ(
            serie1=self.serie1,
            x_1 = self.x_1,
            s1 = self.s1,
            N1 = self.N1,
            mi1=self.mi1,
            sigma1=self.sigma1,
            
            serie2=self.serie2,
            x_2 = self.x_2,
            s2 = self.s2,
            N2 = self.N2,
            mi2=self.mi2,
            sigma2=self.sigma2,
        )
        self.σ = σ(
            serie1=self.serie1,
            x_1 = self.x_1,
            s1 = self.s1,
            N1 = self.N1,
            mi1=self.mi1,
            sigma1=self.sigma1,
            
            serie2=self.serie2,
            x_2 = self.x_2,
            s2 = self.s2,
            N2 = self.N2,
            mi2=self.mi2,
            sigma2=self.sigma2,
        )