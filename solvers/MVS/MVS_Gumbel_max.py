import numpy as np
from numpy import log as ln, sqrt

from helpers import val_to_np
from helpers.z_normal import X as Xz

#Solver
class GumbelMax:
    def __init__(self, xs):
        self.serie = val_to_np(xs)
        self.alfa = None
        self.beta = None
        self.alfa_init = None
        self.min_erro = None
        self.max_iterations = None

    def parametros(self, alfa_init:float|None=100, min_erro:float|None=1E-5, max_iterations:float|None = 1E200):
        if alfa_init is None:
            alfa_init = self.alfa_init
        if min_erro is None:
            min_erro = self.min_erro
        if max_iterations is None:
            max_iterations = self.max_iterations

        check1 = (self.alfa_init!=alfa_init) or (self.min_erro != min_erro) or (self.max_iterations!=max_iterations)

        if not check1 and self.alfa is not None and self.beta is not None:
            return self.alfa, self.beta
        
        self.alfa_init=alfa_init
        self.min_erro=min_erro
        self.max_iterations=max_iterations
        
        def f(dados, alfa):
            sum1=np.sum(dados*np.exp(-dados / alfa))
            
            t1 = 1/len(dados)
            sum2=np.sum(dados - alfa)

            sum3=np.sum(np.exp(-dados / alfa))

            return sum1-t1*sum2*sum3

        def diff_f(dados, alfa):
            t1 = 1/(alfa**2)
            sum1=np.sum(np.power(dados, 2)*np.exp(-dados / alfa))

            sum2 = np.sum(np.exp(-dados / alfa))
            
            t3 = 1/alfa
            sum3=np.sum(dados*np.exp(-dados / alfa))

            return t1*sum1 + sum2 + t3*sum3

        # Alfa
        alfa = alfa_init

        print("Iterações MVS Gumbel MAX")
        for n_iter in range(int(max_iterations)):

            # Valor de alfa, deve se aproximar o máximo possível de 0.
            val = f(self.serie, alfa)

            erro = abs(0-val)
            if erro < min_erro:
                break

            # Derivada de f.
            diff_val = diff_f(self.serie, alfa)
            
            alfa = alfa - (val/diff_val)
            
            if n_iter % 100 == 0:
                print(erro, alfa)

        #Beta
        beta = alfa*ln(len(self.serie)/np.sum(np.exp(-self.serie/alfa)))

        self.alfa = alfa
        self.beta = beta

        return np.round(alfa, decimals=4), np.round(beta, decimals=4)

    def interval(self, confianca:float, prob:float, alfa_init=None, min_erro=None, max_iterations = None):
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

        alfa, beta = self.parametros(alfa_init, min_erro, max_iterations)

        # St
        W = -ln(-ln(1-prob))
        St_2 = ((alfa**2)/N)*(1.1087 + 0.514*W + 0.6079*(W**2))
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

    def interval_Tr(self, confianca:float, Tr:float, alfa_init=None, min_erro=None, max_iterations = None):
        """Retorna os valores superiores e inferiores no intervalo de confiaça especificados para o tempo de retorno T"""

        if Tr<0:
            raise ValueError("O valor de `Tr` deve ser maior que 0")
        
        return self.interval(confianca, 1/Tr, alfa_init, min_erro, max_iterations)



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




    
    