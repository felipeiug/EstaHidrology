from numpy import log as ln
import pandas as pd
import numpy as np
from sympy import exp, symbols, log as ln, sqrt, pi

from helpers.val_to_np import val_to_np

class P_Gumbel_Max:
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
        """Retorna o valor da probabilidade caso alfa e beta sejam escalares 
        ou um `pd.DataFrame` com os valores para cada α e β
        """
        if self.alfa.size > 1 or self.beta.size > 1:
            if self.alfa.size == 1:
                self.alfa = [self.alfa]
            elif self.beta.size == 1:
                self.beta = [self.beta]

            data = {
                "alfa":[],
                "beta":[],
                "prob":[],
            }

            for alfa in self.alfa:
                for beta in self.beta:
                    val = 1 - self._p_menor(other, alfa, beta)
                    data["alfa"].append(alfa)
                    data["beta"].append(beta)
                    data["prob"].append(val)
            
            return pd.DataFrame(data)

        return 1 - self._p_menor(other, self.alfa, self.beta)

    # >= (maior ou igual a): Método especial
    def __ge__(self, other):
        """Retorna o valor da probabilidade caso alfa e beta sejam escalares 
        ou um `pd.DataFrame` com os valores para cada α e β
        """
        if self.alfa.size > 1 or self.beta.size > 1:
            if self.alfa.size == 1:
                self.alfa = [self.alfa]
            elif self.beta.size == 1:
                self.beta = [self.beta]

            data = {
                "alfa":[],
                "beta":[],
                "prob":[],
            }

            for alfa in self.alfa:
                for beta in self.beta:
                    val = 1 - self._p_menor(other, alfa, beta)
                    data["alfa"].append(alfa)
                    data["beta"].append(beta)
                    data["prob"].append(val)
            
            return pd.DataFrame(data)

        return 1 - self._p_menor(other, self.alfa, self.beta)

    # < (menor que): Método especial
    def __lt__(self, other):
        """Retorna o valor da probabilidade caso alfa e beta sejam escalares 
        ou um `pd.DataFrame` com os valores para cada α e β
        """
        if self.alfa.size > 1 or self.beta.size > 1:
            if self.alfa.size == 1:
                self.alfa = [self.alfa]
            elif self.beta.size == 1:
                self.beta = [self.beta]

            data = {
                "alfa":[],
                "beta":[],
                "prob":[],
            }

            for alfa in self.alfa:
                for beta in self.beta:
                    val = self._p_menor(other, alfa, beta)
                    data["alfa"].append(alfa)
                    data["beta"].append(beta)
                    data["prob"].append(val)
            
            return pd.DataFrame(data)

        return self._p_menor(other, self.alfa, self.beta)

    # <= (menor ou igual a): Método especial
    def __le__(self, other):
        """Retorna o valor da probabilidade caso alfa e beta sejam escalares 
        ou um `pd.DataFrame` com os valores para cada α e β
        """
        if self.alfa.size > 1 or self.beta.size > 1:
            if self.alfa.size == 1:
                self.alfa = [self.alfa]
            elif self.beta.size == 1:
                self.beta = [self.beta]

            data = {
                "alfa":[],
                "beta":[],
                "prob":[],
            }

            for alfa in self.alfa:
                for beta in self.beta:
                    val = self._p_menor(other, alfa, beta)
                    data["alfa"].append(alfa)
                    data["beta"].append(beta)
                    data["prob"].append(val)
            
            return pd.DataFrame(data)

        return self._p_menor(other, self.alfa, self.beta)
    
    def _p_menor(self, value:float|int|pd.Series|np.ndarray|list|set|tuple, alfa:float, beta:float):
        value = val_to_np(value)

        val_beta = value-beta
        div = val_beta/alfa
        p_menor = np.exp(-np.exp(-div))

        return p_menor

class Gumbel_Max:
    def __init__(self,
        alfa:float|int|pd.Series|np.ndarray|list|set|tuple,
        beta:float|int|pd.Series|np.ndarray|list|set|tuple
    ):
        self.alfa = val_to_np(alfa)
        self.beta = val_to_np(beta)

        if (self.alfa <= 0).any():
            raise ValueError("α deve sempre ser maior que 0")
        
        self.gama = val_to_np(1.1396)
        
        # Objeto de probailidade
        self.p = P_Gumbel_Max(self.alfa, self.beta)

    # Quantil para α e β
    def quantil(self, prob:float|int|pd.Series|np.ndarray|list|set|tuple):
        """Retorno o valor do quantil para a probabilidade `prob`
        
        O resultado pode ser um `pd.DataFrame` caso existam mais de 1 α ou β,
        ou várias probabilidades.
        """

        prob = val_to_np(prob)

        if (prob > 100).any() or (prob < 0).any():
            raise ValueError("O valor da probabilidade do quantil deve estar compreendido entre 0 e 100%")
        
        mask = prob > 1
        prob[mask] = prob[mask] / 100
        
        if self.alfa.size > 1 or self.beta.size > 1 or prob.size > 1:
            if self.alfa.size == 1:
                self.alfa = val_to_np([self.alfa])
            if self.beta.size == 1:
                self.beta = val_to_np([self.beta])
            if prob.size == 1:
                prob = val_to_np([prob])

            data = {
                "alfa":[],
                "beta":[],
                "prob":[],
                "quan":[],
            }
            for alfa in self.alfa:
                for beta in self.beta:
                    for pro in prob:
                        data["alfa"].append(alfa)
                        data["beta"].append(beta)
                        data["prob"].append(pro)
                        data["quan"].append(beta-alfa*(ln(-ln(1-pro))))
            return pd.DataFrame(data)
        
        return self.beta-self.alfa*(ln(-ln(1-prob)))

    def quantil_TR(self, Tr:float|int|pd.Series|np.ndarray|list|set|tuple):
        """Retorno o valor do quantil para o tempo de retorno `Tr`"""
        
        Tr = val_to_np(Tr)

        if (Tr<0).any():
            raise ValueError("O valor de `Tr` deve ser maior que 0")
        
        data = self.quantil(1-1/Tr)

        if isinstance(data, pd.DataFrame):
            data = data.rename(columns={'prob': 'TR'})
            data["TR"] = 1/data["TR"]

        return data
    
    def fdp(self, x:float|int|pd.Series|np.ndarray|list|set|tuple):
        """Função densidade de probabilidade, retorna o valor da probabilidade de superação de `x` para os valores
        de alfa e beta especificados"""

        x = val_to_np(x)

        if self.alfa.size > 1 or self.beta.size > 1:
            if self.alfa.size == 1:
                self.alfa = val_to_np([self.alfa])
            if self.beta.size == 1:
                self.beta = val_to_np([self.beta])
            
            data = {
                "alfa":[],
                "beta":[],
                "fx":[],
            }
            for alfa in self.alfa:
                for beta in self.beta:
                    t1 = 1/alfa

                    x_beta = x-beta
                    x_beta_alfa = x_beta/alfa

                    fx:np.ndarray = (t1 * np.exp(-x_beta_alfa - np.exp(-x_beta_alfa)))[0]

                    data["alfa"].append(alfa)
                    data["beta"].append(beta)
                    data["fx"].append(fx)

            return pd.DataFrame(data)

        t1 = 1/self.alfa

        x_beta = x-self.beta
        x_beta_alfa = x_beta/self.alfa

        fx = t1 * np.exp(-x_beta_alfa - np.exp(-x_beta_alfa))

        return fx
