from math import gamma
from numpy import sqrt, log as ln

#Entradas
E_X=694.6
Var_X=26186.62
gama=1.1

T=25

alfa = 10

min_erro = 0.000005

#Solver

def f(a):
    gam_1_a = gamma(1+1/a)
    gam_1_3_a = gamma(1+3/a)
    gam_1_2_a = gamma(1+2/a)

    num=-1*gam_1_3_a+3*gam_1_2_a*gam_1_a+2*(gam_1_a**3)
    den = gam_1_2_a-(gam_1_a**2)**(3/2)

    return num/den

beta=0

erro_ans = None
aumetar=True

n_iter = 0
while True:
    n_iter+=1

    gama_now = f(alfa)

    erro = abs(gama-gama_now)
    if erro < min_erro:
        break
    
    if erro_ans != None and erro > erro_ans:
        aumetar = not aumetar

    if aumetar:
        alfa += 0.000001
    else:
        alfa -= 0.000001
    
    erro_ans = erro
    
    if n_iter > 100:
        n_iter=0
        print(erro, alfa)

#Alfa
beta=E_X/gamma(1+1/alfa)

vazao = beta*((-ln(1-(1/T)))**(1/alfa))

print(f"α: {alfa}, β: {beta}, Vazão T({T}): {vazao}")

    
    