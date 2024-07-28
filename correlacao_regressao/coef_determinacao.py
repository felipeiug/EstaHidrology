import numpy as np
import pandas as pd
from scipy.stats import t as t_student
from scipy.stats import norm, chi2
from sympy import symbols, Eq, sqrt, solve
from helpers import get_confianca
from typing import Iterable
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

class CoefienteDeterminacao:
    def __init__(self, xs:Iterable, ys: Iterable, a:float, b:float):
        self.xs = np.array(xs)
        self.ys = np.array(ys)

        if self.xs.size != self.ys.size:
            raise ValueError("As séries 1 e 2 devem ter exatamento o mesmo tamanho.")

        self.N = self.xs.size
        self.a = a
        self.b = b

        self.x_ = self.xs.mean()
        self.y_ = self.ys.mean()
        self.sx2 = self.xs.var()
        self.sy2 = self.ys.var()

        # Mesmo que y^
        self.y__= self.f(self.xs)

        # Determinando o r²
        s_1 = np.sum(np.power((self.y__- self.y_), 2))
        s_2 = np.sum(np.power((self.ys - self.y_), 2))
        self.r2 = s_1/s_2

        #TODO: Somente para testes
        self.r2 = (self.b**2)*self.sx2/self.sy2

        self.r = (-1 if b<0 else 1) * np.sqrt(self.r2)

    

