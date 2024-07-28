import numpy as np
import pandas as pd
from scipy.stats import t as t_student
from scipy.stats import norm, chi2
from sympy import symbols, Eq, sqrt, solve
from helpers import get_confianca

class PearsonLinear:
    def __init__(self, dados:pd.DataFrame, dados1:str, dados2:str, coef_corr_lin:float=None):
        self.dados = dados
        self.N = len(dados.index)

        self.coef_corr_lin_pop = coef_corr_lin

        self.cov_amostral = self.covariancia_amostral(self.dados[dados1], self.dados[dados2])
        self.r = self.cov_amostral/(self.dados[dados1].std()*self.dados[dados2].std())

    def covariancia_amostral(self, serie1: list|tuple|set|pd.Series|np.ndarray, serie2: list|tuple|set|pd.Series|np.ndarray):
        serie1 = np.array(serie1)
        serie2 = np.array(serie2)

        if serie1.size != serie2.size:
            raise ValueError("As séries 1 e 2 devem conter a mesma quantidade de elementos")
        
        med1 = serie1.mean()
        med2 = serie2.mean()

        p1 = (serie1-med1)
        p2 = (serie2-med2)
        p3 = p1*p2

        sxy = np.sum(p3)/(serie1.size-1)

        return sxy
    
    def Z(self, alfa:0.05):
        """Retorna Z[alfa/2]"""
        alfa = get_confianca(alfa)

        N = self.N
        r = self.r

        if self.coef_corr_lin_pop is not None:
            aTanh_ro = np.arctanh(self.coef_corr_lin_pop)
            print("ρ populacional")
        else:
            aTanh_ro = np.arctanh(r)
            print("ρ amostral (r)")

        mi_z = aTanh_ro
        sigma2 = (N-3)**(-1)
        Z = norm.ppf(alfa/2, loc=mi_z, scale=sigma2) # TODO: Aqui é isto mesmo?

        return Z

    # Testes de Hipótese
    def H0_0_H1_NOT_0(self, alfa=0.05):
        """Teste de hipótese sobre o Coeficiente de Correlação
        - Se `False` rejeito H0 então Coef. de Correlção Linear != 0
        - Se `True` não rejeito H0 então Coef. de Correlção Linear = 0"""

        alfa = get_confianca(alfa)
        alfa = alfa/2

        N = self.N
        r = self.r

        t0 = r*np.sqrt(N-2)/np.sqrt(1-(r**2))
        T = t_student.ppf((alfa/2), N-2)

        if abs(t0) > abs(T):
            return False
        return True
    
    def H0_ro_H1_NOT_ro(self, ro0:float, alfa=0.05):
        """Teste de hipótese sobre o Coeficiente de Correlação
        - Se `False` rejeito H0 então Coef. de Correlção Linear != ro0
        - Se `True` não rejeito H0 então Coef. de Correlção Linear = ro0"""

        N = self.N
        r = self.r

        aTanh_r = np.arctanh(r)

        Z = self.Z(alfa)

        z0 = (aTanh_r-np.arctanh(ro0))*np.sqrt(N-3)

        if abs(z0) > abs(Z):
            return False
        return True
    
    # Intervalo de confiança para RÔ
    def interval_ro(self, alfa=0.05)-> tuple[float, float]:
        """Retorna o intervalo de confiança para ρ
        - `tuple` -> (min ρ, max ρ)"""

        N = self.N
        r = self.r
        Z_alfa_2 = abs(self.Z(alfa))

        aTanh_r = np.arctanh(r)
        sqrt_n_3 = np.sqrt(N-3)

        i1 = np.tanh(aTanh_r - (Z_alfa_2/sqrt_n_3))
        i2 = np.tanh(aTanh_r + (Z_alfa_2/sqrt_n_3))

        return i1, i2




