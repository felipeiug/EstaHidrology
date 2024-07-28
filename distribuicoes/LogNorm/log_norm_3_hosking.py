from numpy import log as ln
import pandas as pd
import numpy as np
from sympy import exp, symbols, log as ln, sqrt, pi
from scipy.stats import norm
from scipy.optimize import root

from helpers.val_to_np import val_to_np

# class P_Gumbel_Max:
#     def __init__(self, alfa:np.ndarray, beta:np.ndarray):
#         self.alfa = alfa
#         self.beta = beta

#     # == (igual a): Método especial
#     def __eq__(self, _):
#         return 0

#     # != (diferente de): Método especial
#     def __ne__(self, _):
#         return 1

#     # > (maior que): Método especial
#     def __gt__(self, other):
#         """Retorna o valor da probabilidade caso alfa e beta sejam escalares 
#         ou um `pd.DataFrame` com os valores para cada α e β
#         """
#         if self.alfa.size > 1 or self.beta.size > 1:
#             if self.alfa.size == 1:
#                 self.alfa = [self.alfa]
#             elif self.beta.size == 1:
#                 self.beta = [self.beta]

#             data = {
#                 "alfa":[],
#                 "beta":[],
#                 "prob":[],
#             }

#             for alfa in self.alfa:
#                 for beta in self.beta:
#                     val = 1 - self._p_menor(other, alfa, beta)
#                     data["alfa"].append(alfa)
#                     data["beta"].append(beta)
#                     data["prob"].append(val)
            
#             return pd.DataFrame(data)

#         return 1 - self._p_menor(other, self.alfa, self.beta)

#     # >= (maior ou igual a): Método especial
#     def __ge__(self, other):
#         """Retorna o valor da probabilidade caso alfa e beta sejam escalares 
#         ou um `pd.DataFrame` com os valores para cada α e β
#         """
#         if self.alfa.size > 1 or self.beta.size > 1:
#             if self.alfa.size == 1:
#                 self.alfa = [self.alfa]
#             elif self.beta.size == 1:
#                 self.beta = [self.beta]

#             data = {
#                 "alfa":[],
#                 "beta":[],
#                 "prob":[],
#             }

#             for alfa in self.alfa:
#                 for beta in self.beta:
#                     val = 1 - self._p_menor(other, alfa, beta)
#                     data["alfa"].append(alfa)
#                     data["beta"].append(beta)
#                     data["prob"].append(val)
            
#             return pd.DataFrame(data)

#         return 1 - self._p_menor(other, self.alfa, self.beta)

#     # < (menor que): Método especial
#     def __lt__(self, other):
#         """Retorna o valor da probabilidade caso alfa e beta sejam escalares 
#         ou um `pd.DataFrame` com os valores para cada α e β
#         """
#         if self.alfa.size > 1 or self.beta.size > 1:
#             if self.alfa.size == 1:
#                 self.alfa = [self.alfa]
#             elif self.beta.size == 1:
#                 self.beta = [self.beta]

#             data = {
#                 "alfa":[],
#                 "beta":[],
#                 "prob":[],
#             }

#             for alfa in self.alfa:
#                 for beta in self.beta:
#                     val = self._p_menor(other, alfa, beta)
#                     data["alfa"].append(alfa)
#                     data["beta"].append(beta)
#                     data["prob"].append(val)
            
#             return pd.DataFrame(data)

#         return self._p_menor(other, self.alfa, self.beta)

#     # <= (menor ou igual a): Método especial
#     def __le__(self, other):
#         """Retorna o valor da probabilidade caso alfa e beta sejam escalares 
#         ou um `pd.DataFrame` com os valores para cada α e β
#         """
#         if self.alfa.size > 1 or self.beta.size > 1:
#             if self.alfa.size == 1:
#                 self.alfa = [self.alfa]
#             elif self.beta.size == 1:
#                 self.beta = [self.beta]

#             data = {
#                 "alfa":[],
#                 "beta":[],
#                 "prob":[],
#             }

#             for alfa in self.alfa:
#                 for beta in self.beta:
#                     val = self._p_menor(other, alfa, beta)
#                     data["alfa"].append(alfa)
#                     data["beta"].append(beta)
#                     data["prob"].append(val)
            
#             return pd.DataFrame(data)

#         return self._p_menor(other, self.alfa, self.beta)
    
#     def _p_menor(self, value:float|int|pd.Series|np.ndarray|list|set|tuple, alfa:float, beta:float):
#         value = val_to_np(value)

#         val_beta = value-beta
#         div = val_beta/alfa
#         p_menor = np.exp(-np.exp(-div))

#         return p_menor

class LogNorm3ParamHosking:
    def __init__(self, qsi:float, alfa:float, kapa:float):
        self.qsi = qsi
        self.alfa = alfa
        self.kapa = kapa
        
        # Objeto de probailidade
        # self.p = P_Gumbel_Max(self.alfa, self.beta)

    # Quantil para α e β
    def quantil(self, prob:float|int|pd.Series|np.ndarray|list|set|tuple):
        """Retorno o valor do quantil para a probabilidade `prob`
        
        O resultado pode ser um `pd.DataFrame` caso existam mais de 1 α ou β,
        ou várias probabilidades.
        """
        prob = val_to_np(prob)

        quan = self._pdf(prob)
        return quan

    def quantil_TR(self, Tr:float|int|pd.Series|np.ndarray|list|set|tuple):
        """Retorno o valor do quantil para o tempo de retorno `Tr`"""
        
        Tr = val_to_np(Tr)

        if (Tr<0).any():
            raise ValueError("O valor de `Tr` deve ser maior que 0")
        
        data = self.quantil(1-1/Tr)

        return data

    def fdp(self, x:float|int|pd.Series|np.ndarray|list|set|tuple):
        y_ = self._y(x)
    
        elev = (self.kapa*y_) - (np.power(y_, 2)/2)
        num = np.exp(elev)

        den = self.alfa*np.sqrt(2*np.pi)

        return num/den

    def cdf(self, x):
        y_ = self._y(x)
        return norm.cdf(y_)

    def _y(self, x):
        qsi=self.qsi
        alfa=self.alfa
        kapa=self.kapa

        param_1 = (x-qsi)/alfa

        if kapa == 0:
            return param_1
        
        kapa_param_1 = kapa*param_1
        y_ = -(1/kapa)*np.log(1-kapa_param_1)
        return y_
    
    def _pdf(self, p:float|int|pd.Series|np.ndarray|list|set|tuple):
        def equation(x, p):
            return (self.cdf(x)*1000) - (p*1000)
        
        def solve(p):
            for method in ['hybr', 'lm', 'broyden1', 'broyden2', 'anderson', 'linearmixing', 'diagbroyden', 'excitingmixing', 'krylov', 'df-sane']:
                sol = root(lambda x: equation(x, p), x0=0.5, method=method)

                if sol.success:
                    try:
                        return sol.x[0]
                    except:
                        return sol.x
                    
            return np.nan
            
        
        if p.size == 1:
            return solve(p)

        res = [] 
        for p_ in p:
            sol = solve(p_)
            res.append(sol)

        return np.array(res)


