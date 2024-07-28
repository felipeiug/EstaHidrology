from scipy.stats import t as t_student
from scipy.stats import norm, chi2
from sympy import symbols, Eq, sqrt, solve
import pandas as pd
import numpy as np

class Normal:

    def __init__(self, serie:np.ndarray|pd.Series|list|tuple|set):
        self.serie = pd.Series(serie)

        self.x_ = self.serie.mean()
        self.s = self.serie.std()
        self.N = len(self.serie.index)
    
    def get_media_desvio(self, confianca=95, mi=None, sigma=None):
        if confianca > 1:
            confianca /= 100

        if confianca >=100 or confianca <=0:
            raise ValueError("A confiaça deve ser um valor entre 0 e 100%")

        μ, σ, α = symbols("μ, σ, α")

        alfa1 = (1-confianca)/2
        alfa2 = 1-alfa1

        mi_return = None
        sigma_return = None

        # Cálculo de μ
        if sigma is None:
            v1 = t_student.ppf(alfa1, self.N-1)
            v2 = t_student.ppf(alfa2, self.N-1)

            eq1 = Eq(v1, (self.x_-μ)/(self.s/sqrt(self.N)))
            eq2 = Eq(v2, (self.x_-μ)/(self.s/sqrt(self.N)))

            mi_return_1 = solve(eq1, μ)[0].evalf()
            mi_return_2 = solve(eq2, μ)[0].evalf()

            mi_return = (min(mi_return_1, mi_return_2), max(mi_return_1, mi_return_2))
        else:
            v1 = norm.ppf(alfa1)
            v2 = norm.ppf(alfa2)

            eq1 = Eq(v1, (self.x_-μ)/(sigma/sqrt(self.N)))
            eq2 = Eq(v2, (self.x_-μ)/(sigma/sqrt(self.N)))

            mi_return_1 = solve(eq1, μ)[0].evalf()
            mi_return_2 = solve(eq2, μ)[0].evalf()

            mi_return = (min(mi_return_1, mi_return_2), max(mi_return_1, mi_return_2))

        #Cálculo de σ
        if mi is None:
            v1 = chi2.ppf(alfa1, self.N-1)
            v2 = chi2.ppf(alfa2, self.N-1)

            eq1 = Eq(v1, (self.N-1)*(self.s**2)/(σ**2))
            eq2 = Eq(v2, (self.N-1)*(self.s**2)/(σ**2))

            sigma_return_1 = abs(solve(eq1, σ)[0].evalf())
            sigma_return_2 = abs(solve(eq2, σ)[0].evalf())

            sigma_return = (min(sigma_return_1, sigma_return_2), max(sigma_return_1, sigma_return_2))
        else:
            v1 = chi2.ppf(alfa1, self.N)
            v2 = chi2.ppf(alfa2, self.N)

            x_s = self.serie.values

            somatorio = np.sum(((x_s-mi)/σ)**2)
            eq1 = Eq(v1, somatorio)
            eq2 = Eq(v2, somatorio)

            sigma_return_1 = abs(solve(eq1, σ)[0].evalf())
            sigma_return_2 = abs(solve(eq2, σ)[0].evalf())

            sigma_return = (min(sigma_return_1, sigma_return_2), max(sigma_return_1, sigma_return_2))
        
        return mi_return, sigma_return


