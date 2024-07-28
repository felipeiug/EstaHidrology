import numpy as np
from numpy import log as ln, sqrt

from helpers import val_to_np
from helpers.z_normal import X as Xz

#Solver
class GumbelMax:
    def __init__(self, xs, l1, l2):
        self.serie = val_to_np(xs)
        self.l1 = l1
        self.l2 = l2

    # Valores de gumbel
    def parametros(self):
        alfa = np.round(self.l2/np.log(2), decimals=4)
        beta = np.round(self.l1 - 0.5772*alfa, decimals=4)
        return alfa, beta
    
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
        N = self.serie.size

        # Parâmetros para esta amostra
        alfa, beta = self.parametros()

        # St
        W = -ln(-ln(1-prob))
        St_2 = ((alfa**2)/N)*(1.1128 + 0.4574*W + 0.8046*(W**2))
        St = sqrt(St_2)
        
        # Valores do intervalo
        xt = beta-alfa*ln(-ln(1-prob))

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

    serie = [
        576, 414,  472, 458, 684, 408, 371, 333, 570, 502, 810, 366, 690, 570,
        288, 295,  498, 470, 774, 388, 408, 448, 822, 414, 515, 748, 570, 726,
        580, 450,  478, 340, 246, 568, 520, 449, 357, 276, 736, 822, 550, 698,
        585, 1017, 437, 549, 601, 288, 481, 927, 827, 424, 603, 633, 695, 296, 427
    ]

    g_max = GumbelMax(serie)
    alfa, beta = g_max.parametros(serie)
    print(f"α: {alfa}, β: {beta}")




    
    