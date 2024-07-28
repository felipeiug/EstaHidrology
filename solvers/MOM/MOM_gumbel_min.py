import numpy as np
#Contas
def gum_min(mean, var):
    alfa = np.round(np.sqrt((6*var)/(np.pi**2)), decimals=4)
    beta=np.round(mean+0.5772*alfa, decimals=4)
    return alfa, beta

if __name__ == "__main__":
    #Entradas
    E_X=534.175439
    Var_X=176.013811**2
    T = 100

    alfa, beta = gum_min(E_X, Var_X)
    vazao = beta-alfa*(np.log(-np.log(1-(1/T))))

    print(f"α: {alfa:.3f}, β: {beta:.3f}, Vazão T({T}): {vazao:.3f}")
    
    