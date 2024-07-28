import numpy as np
import pandas as pd
from sympy import symbols, log as ln, sqrt, pi


#Contas
class LogNorm3:
    def __init__(self, xs:np.ndarray):
        self.xs = xs

        xs:pd.Series = pd.Series(xs)

        self.mean = xs.mean()
        self.var = xs.var()
        self.std = xs.std()
        self.skew = xs.skew()

    def parametros(self):
        w = (-self.skew + np.sqrt(np.power(self.skew, 2) + 4))/2

        CV = (1-np.power(np.power(w, 2), 1/3))/np.power(w, 1/3)

        a = self.mean - self.std/CV
        y:np.ndarray = np.log(self.xs-a)

        mi_y = y.mean()
        sigma_y = y.std()

        return a, mi_y, sigma_y

    def interval(self, confianca:float, prob:float):
        """Retorna os valores superiores e inferiores para a probabilidade especificada"""

        # TODO: Refazer pra log normal

        #Verificando o intervalo da confiança
        # if confianca <= 0 or confianca >= 100:
        #     raise ValueError("O nível do intervalo de confiaça deve ser um valor no intervalo (0 e 100)%")
        # if confianca > 1:
        #     confianca=confianca/100

        # # Verificando a probabilidade
        # if prob <= 0 or prob >= 100:
        #     raise ValueError("Os valores de probabilidade devem estar contidos no intervalo (0, 100)")

        # if prob > 1:
        #     prob/=100
        # if prob >= 1:
        #     raise ValueError("Os valores de probabilidade devem estar contidos no intervalo (0, 100)")

        # # Tamanho da amostra
        # N = self.xs.size

        # # Função Kt
        # α,β,p,μ_1,μ2 = symbols("α,β,p,μ_1,μ2")
        
        # α = sqrt(6*μ2/(pi**2))
        # β = μ_1-0.5772*α
        # gama1 = 1.1396
        # gama2 = 5.4

        # # Função Kt
        # X_t = β-α*ln(-ln(1-p))
        # K_t = (X_t - μ_1)/sqrt(μ2)

        # # Valor Kt
        # Kt = float(K_t.subs({p:prob}).evalf())

        # # valor de St
        # mi_2 = (np.pi**2)*(self.alfa**2)/6
        # St_2 = (mi_2/N)*(1 + Kt*gama1 + ((Kt**2)/4)*(gama2-1))
        # St = np.sqrt(St_2)

        # # Criando o intervalo
        # xt = X_t.subs({
        #     p:prob,
        #     α:self.alfa,
        #     β:self.beta,
        # }).evalf()

        # intervalo = (1-confianca)/2
        # if intervalo < 0.5:
        #     intervalo = 1-intervalo
        # z = Xz(intervalo)

        # minimo = xt-z*St
        # maximo = xt+z*St

        return 0, 0

    def interval_Tr(self, confianca:float, Tr:float):
        """Retorna os valores superiores e inferiores no intervalo de confiaça especificados para o tempo de retorno T"""

        if Tr<0:
            raise ValueError("O valor de `Tr` deve ser maior que 0")
        
        return self.interval(confianca, 1/Tr)

    
