import numpy as np
import pandas as pd
from sympy import symbols, log as ln, sqrt, pi

from helpers.z_normal import X as Xz

#Contas
class GumbelMax:
    def __init__(self, xs:np.ndarray, mean:float=None, var:float=None):
        self.mean = mean if mean is not None else xs.mean()
        self.var = var if var is not None else xs.var()
        self.xs = xs

        self.alfa = np.round(np.sqrt((6*self.var)/(np.pi**2)), decimals=4)
        self.beta = np.round(self.mean-0.5772*self.alfa, decimals=4)

    def parametros(self):
        return self.alfa, self.beta

    def interval(self, confianca:float, prob:float):
        """Retorna os valores superiores e inferiores para a probabilidade especificada"""

        #Verificando o intervalo da confiança
        if confianca <= 0 or confianca >= 100:
            raise ValueError("O nível do intervalo de confiaça deve ser um valor no intervalo (0 e 100)%")
        if confianca > 1:
            confianca=confianca/100

        # Verificando a probabilidade
        if prob <= 0 or prob >= 100:
            raise ValueError("Os valores de probabilidade devem estar contidos no intervalo (0, 100)")

        if prob > 1:
            prob/=100
        if prob >= 1:
            raise ValueError("Os valores de probabilidade devem estar contidos no intervalo (0, 100)")

        # Tamanho da amostra
        N = self.xs.size

        # Função Kt
        α,β,p,μ_1,μ2 = symbols("α,β,p,μ_1,μ2")
        
        α = sqrt(6*μ2/(pi**2))
        β = μ_1-0.5772*α
        gama1 = 1.1396
        gama2 = 5.4

        # Função Kt
        X_t = β-α*ln(-ln(1-p))
        K_t = (X_t - μ_1)/sqrt(μ2)

        # Valor Kt
        Kt = float(K_t.subs({p:prob}).evalf())

        # valor de St
        mi_2 = (np.pi**2)*(self.alfa**2)/6
        St_2 = (mi_2/N)*(1 + Kt*gama1 + ((Kt**2)/4)*(gama2-1))
        St = np.sqrt(St_2)

        # Criando o intervalo
        xt = X_t.subs({
            p:prob,
            α:self.alfa,
            β:self.beta,
        }).evalf()

        intervalo = (1-confianca)/2
        if intervalo < 0.5:
            intervalo = 1-intervalo
        z = Xz(intervalo)

        minimo = xt-z*St
        maximo = xt+z*St

        return minimo, maximo

    def interval_Tr(self, confianca:float, Tr:float):
        """Retorna os valores superiores e inferiores no intervalo de confiaça especificados para o tempo de retorno T"""

        if Tr<0:
            raise ValueError("O valor de `Tr` deve ser maior que 0")
        
        return self.interval(confianca, 1/Tr)



if __name__ == "__main__":
    #Entradas
    E_X=534.175439
    Var_X=176.013811**2
    T = 100

    serie = [
        576, 414,  472, 458, 684, 408, 371, 333, 570, 502, 810, 366, 690, 570,
        288, 295,  498, 470, 774, 388, 408, 448, 822, 414, 515, 748, 570, 726,
        580, 450,  478, 340, 246, 568, 520, 449, 357, 276, 736, 822, 550, 698,
        585, 1017, 437, 549, 601, 288, 481, 927, 827, 424, 603, 633, 695, 296, 427
    ]

    xs = np.array(serie)
    gum_max = GumbelMax(
        xs   = xs,
        mean = xs.mean(),
        var  = xs.var(),
    )

    alfa, beta = gum_max.parametros()
    vazao = beta-alfa*(np.log(-np.log(1-(1/T))))

    print(f"α: {alfa:.3f}, β: {beta:.3f}, Vazão T({T}): {vazao:.3f}")
    
