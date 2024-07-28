def get_confianca(confianca:float):
    if confianca > 1:
        confianca /= 100

    if confianca <=0 or confianca >= 100:
        raise ValueError("A confiança deve estar entre 0 e 100%")
    
    return confianca