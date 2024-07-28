import numpy as np
import pandas as pd
from scipy.stats import t as t_student
from scipy.stats import norm, chi2
from sympy import symbols, Eq, sqrt, solve, Symbol
from helpers import get_confianca
from typing import Iterable
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

class RegressaoLin:
    def __init__(self, xs:Iterable, ys:Iterable):
        """- `xs` e `ys` são as variáveis dependes.
        - `transformada` é a função para transformar em linear, deve ser do tipo Equality do sympy e deve estar sempre em função de x.
        """

        self.xs = np.array(xs)
        self.ys = np.array(ys)

        if self.xs.size != self.ys.size:
            raise ValueError("As séries 1 e 2 devem ter exatamento o mesmo tamanho.")

        self.N = self.xs.size

        self.x_ = self.xs.mean()
        self.y_ = self.ys.mean()

        self.sx2 = self.xs.var()
        self.sy2 = self.ys.var()

        # Definindo a e b para a amostra.
        self.a, self.b = self.min_quad()

        # Mesmo que y^
        self.y__= self.f(self.xs)

        # e[i]
        self.e = self._ei()
        self.E_e = np.zeros((self.e.size,)) # Esperança de e[i] qualquer
        
        # Variância e desvio padrão amostral de e
        self.var_e = np.sum(np.power(self.e, 2))/(self.N-2)
        self.se    = np.sqrt(self.var_e)

        # Determinando o r²
        self.r2 = (self.b**2)*self.sx2/self.sy2
        self.r = (-1 if self.b<0 else 1) * np.sqrt(self.r2)

        # sa e sb
        x_2 = (self.x_**2)
        sum1 = np.sum(np.power(self.xs-self.x_, 2))
        div2 = x_2/sum1
        div1 = 1/self.N
        self.sa = np.sqrt((self.se**2)*(div1+div2))

        self.sb = np.sqrt((self.se**2)/sum1)

    def _ei(self)-> np.ndarray:
        """`i` é o index no qual se deseja obter e[i]"""

        yi = self.ys
        xi = self.xs
        a = self.a
        b = self.b

        y__i = (a + b*xi)

        return yi - y__i

    def f(self, x):
        """Retorna y^=a+b*x"""

        return self.a + self.b*x

    def plot_series(
        self,
        ax_serie:Axes=None,
        ax_ei:Axes=None,
        alfa:float = 0.05,
        show_plt:bool=True,
        just_series = False
    ):
        y_line = self.a + self.b * self.xs


        if not just_series:
            if ax_serie is None or ax_ei is None:
                _, axs = plt.subplots(nrows=1, ncols=2)
            else:
                axs = [ax_serie, ax_ei]
        else:
            _, axs = plt.subplots(nrows=1, ncols=1)
            axs = [axs]

        # Serie original
        axs[0].scatter(self.xs, self.ys)

        if not just_series:
            # Série calculada
            axs[0].scatter(self.xs, (self.a + self.b*self.xs), color='red')

            # Adição da linha ao gráfico
            axs[0].plot(self.xs, y_line, color='black')

            # Gráfico dos erros
            axs[1].scatter(range(1, self.e.size+1), self.e)
            axs[1].plot(range(1, self.e.size+1), np.zeros(self.e.size), color='black')

        if show_plt:
            plt.show()

    def min_quad(self):
        """Retorna o valor de `a` e `b` em `a+b*x`"""

        xs = self.xs
        ys = self.ys

        x_ = self.xs.mean()
        y_ = self.ys.mean()

        N = self.N

        # Calculando "b"
        xy = xs*ys
        x2 = np.power(xs, 2)

        sum_x = np.sum(xs)
        sum_y = np.sum(ys)
        sum_xy = np.sum(xy)
        sum_x2 = np.sum(x2)

        num = (N*sum_xy) - (sum_y*sum_x)
        den = (N * sum_x2) - (sum_x**2)

        b = num/den

        # Calculando "a"
        a = y_ - b*x_

        return a, b
    
    # Intervalos de confiança de alfa e beta

    def intervalo_alfa(self, alfa:float = 0.05):
        """Retorna o intervalo de confiança do coeficiente α de y^ = α + β * x"""

        alfa = get_confianca(alfa)

        t = t_student.ppf(1-(alfa/2), self.N-2)

        i1 = self.a - t*self.sa
        i2 = self.a + t*self.sa

        return i1, i2
    
    def intervalo_beta(self, alfa:float = 0.05):
        """Retorna o intervalo de confiança do coeficiente β de y^ = α + β * x"""

        alfa = get_confianca(alfa)

        t = t_student.ppf(1-(alfa/2), self.N-2)

        i1 = self.b - t*self.sb
        i2 = self.b + t*self.sb

        return i1, i2

    # Intervalo de confiança para a linha de regressão linear simples
    def intervalo_reta(self, x_linha:float, alfa:float = 0.05):
        """Retorna o intervalo de confiança das retas formadas por `y^'` em que y^' = α + β * `x'`"""

        alfa = get_confianca(alfa)
        t = t_student.ppf(1-(alfa/2), self.N-2)

        y__linha = self.a + self.b*x_linha

        div1 = 1/self.N

        num2 = (x_linha - self.x_)**2
        den2 = np.sum(np.power(self.xs-self.x_, 2))
        div2 = num2/den2

        t1 = np.sqrt(div1 + div2)

        t2 = t * self.se * t1

        i1 = y__linha - t2
        i2 = y__linha + t2

        return i1, i2
    
    # Intervalo do valor previsto
    def intervalo_y_chapeu(self, x_linha:float, alfa:float = 0.05):
        """Retorna o intervalo de confiança do `y^'` em que y^' = α + β * `x'`
        - y^' é o valor previsto pela equação formada por `a + b*x`"""

        alfa = get_confianca(alfa)
        t = t_student.ppf(1-(alfa/2), self.N-2)

        y__linha = self.a + self.b*x_linha

        div1 = 1/self.N

        num2 = (x_linha - self.x_)**2
        den2 = np.sum(np.power(self.xs-self.x_, 2))
        div2 = num2/den2

        t1 = np.sqrt(1 + div1 + div2)

        t2 = t * self.se * t1

        i1 = y__linha - t2
        i2 = y__linha + t2

        return i1, i2
    
    # Testes de hipótese
    def H0_beta0_H1_beta(self, alfa:float = 0.05):
        """- True caso não rejeite H0, β=0
        - False caso rejeite H0, β != 0
        - Se β for igual a 0, não existe relação linear simples, caso β for diferente de 0, existe relação linear"""

        alfa = get_confianca(alfa)
        t = self.b/self.sb
        T = t_student.ppf(1-(alfa/2), self.N-2)

        if abs(t) > abs(T):
            return False
        return True



