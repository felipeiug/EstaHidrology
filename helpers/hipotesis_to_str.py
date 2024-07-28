def hipotesis_to_str(hipotesis:bool):
    message = ""
    if hipotesis:
        message +="não "
    
    message += "deve-se rejeitar H0, em favor de H1"

    if hipotesis:
        message += ". Com base na amostra disponível, não há evidências que comprovem o checado entre H0 e H1. A diferença deve-se unicamente a flutuações aleatórias nas observações."
    else:
        message += ". Com base na amostra disponível, há evidências suficientes que comprovem o checado entre H0 e H1. A diferença é significativa e não justificavél por flutuações aleatórias nas observações."

    return message