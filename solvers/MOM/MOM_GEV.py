import numpy as np
import pandas as pd
from math import gamma
from scipy.optimize import root


#Contas
class GEV:
    def __init__(self, xs:np.ndarray):
        self.xs = xs

        xs:pd.Series = pd.Series(xs)

        self.mean = xs.mean()
        self.var  = xs.var()
        self.std  = xs.std()
        self.skew = xs.skew()

    def parametros(self):
        k = self._solve_k()

        #Alfa
        gama_1_k = gamma(1+k)
        gama_1_2k = gamma(1+2*k)
        num= (k**2)*self.var
        den=gama_1_2k-gama_1_k**2
        alfa = np.sqrt(num/den)

        #Beta
        beta = self.mean-(alfa/k)*(1-gama_1_k)

        return alfa, beta, k

    def interval(self, confianca:float, prob:float):
        """Retorna os valores superiores e inferiores para a probabilidade especificada"""
        raise NotImplementedError("Não implementado")

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
        
        # α = np.sqrt(6*μ2/(pi**2))
        # β = μ_1-0.5772*α
        # gama1 = 1.1396
        # gama2 = 5.4

        # # Função Kt
        # X_t = β-α*ln(-ln(1-p))
        # K_t = (X_t - μ_1)/np.sqrt(μ2)

        # # Valor Kt
        # Kt = float(K_t.subs({p:prob}).evalf())

        # # valor de St
        # mi_2 = (np.pi**2)*(self.alfa**2)/6
        # St_2 = (mi_2/N)*(1 + Kt*gama1 + ((Kt**2)/4)*(gama2-1))
        # St = np.np.sqrt(St_2)

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

        raise NotImplementedError("Não implementado")

    def _solve_k(self):
        def equation(x, gama):
            return (self._f(x)*1000) - (gama*1000)
        
        def solve(gama):
            for method in ['hybr', 'lm', 'broyden1', 'broyden2', 'anderson', 'linearmixing', 'diagbroyden', 'excitingmixing', 'krylov', 'df-sane']:
                sol = root(lambda x: equation(x, gama), x0=0.5, method=method)

                if sol.success:
                    try:
                        return sol.x[0]
                    except:
                        return sol.x
                    
            return np.nan

        return solve(self.skew)
    
    def _f(self, k):
        posi = k>0

        gam_1_3k = gamma(1+3*k)
        gam_1_k = gamma(1+k)
        gam_1_2k = gamma(1+2*k)

        num=-1*gam_1_3k+3*gam_1_k*gam_1_2k-2*(gam_1_k**3)
        den = abs(gam_1_2k-(gam_1_k**2))**(3/2)

        return (1 if posi else -1)*(num/den)