from math import gamma
from numpy import sqrt
import numpy as np

def frechet(mean, CV, teta_init = 10, min_erro = 5E-6, max_iterations = 1E200):

    def f(x):
        den=gamma(1-2/x)
        num=gamma(1-1/x)**2
        return sqrt((den/num)-1)
    
    def diff_f(x):
        h = 1E-15
        val = (gamma(x+h)-gamma(x))/h
        return val

    teta = teta_init

    for n_iter in range(int(max_iterations)):
        CV2 = f(teta)
        diff_CV2 = diff_f(teta)

        erro = abs(CV-CV2)
        if erro < min_erro:
            break
        
        teta -= CV2/diff_CV2

        if teta < 2:
            teta=2
            break

        if n_iter % 100 == 0:
            print(f"Teta: {teta}")
        
    y0 = mean/gamma(1-(1/teta))

    return teta, y0

if __name__ == "__main__":
    #Dados
    E_X=500
    CV=0.434

    teta, y0 = frechet(E_X, CV)

    print(f"θ: {teta}, y0: {y0}")


    
    