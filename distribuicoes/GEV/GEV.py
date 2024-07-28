from numpy import log as ln
import pandas as pd
import numpy as np

from distribuicoes.Gumbel.maximos import Gumbel_Max
from helpers.val_to_np import val_to_np

class P_GEV:
    def __init__(self, alfa:np.ndarray, beta:np.ndarray):
        self.alfa = alfa
        self.beta = beta

    # == (igual a): Método especial
    def __eq__(self, _):
        return 0

    # != (diferente de): Método especial
    def __ne__(self, _):
        return 1

    # > (maior que): Método especial
    def __gt__(self, other):
        return 1 - self._p_menor(other)

    # >= (maior ou igual a): Método especial
    def __ge__(self, other):
        return 1 - self._p_menor(other)

    # < (menor que): Método especial
    def __lt__(self, other):
        return self._p_menor(other)

    # <= (menor ou igual a): Método especial
    def __le__(self, other):
        return self._p_menor(other)
    
    def _p_menor(self, value:float|int|pd.Series|np.ndarray|list|set|tuple):
        value = val_to_np(value)

        val_beta = value-self.beta
        div = val_beta/self.alfa
        p_menor = np.exp(-np.exp(-div))

        return p_menor

class GEV:
    def __init__(self, alfa:float, beta:float, kapa:float):
        self.alfa = alfa
        self.beta = beta
        self.kapa = kapa
        
        # Objeto de probailidade
        # self.p = P_GEV(self.alfa, self.beta, self.kapa)

    def pdf(self, x):
        """Função densidade de probabilidade"""

        div = (x-self.beta)/self.alfa
        c2 = np.power((1-self.kapa*div), 1/(self.kapa-1))

        f_y = (1/self.alfa)*c2
        
        if self.kapa != 0:
            f_y = f_y * self.cdf(x)

        return f_y


    def cdf(self, x):
        """Cumulative density probability"""

        div = (x-self.beta)/self.alfa
        c1 = np.power((1-self.kapa*div), 1/self.kapa)

        return np.exp(-c1)

    def quantil(self, p:float):
        c1 = 1-(np.power(-np.log(p), self.kapa))
        div = (self.alfa/self.kapa)
        return self.beta + (div * c1)

    def quantil_TR(self, Tr:float):
        return self.quantil(1-(1/Tr))
    
