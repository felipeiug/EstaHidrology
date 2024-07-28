import numpy as np
import matplotlib.pyplot as plt


# Exibindo o novo DataFrame
print('Dados do Histograma')
print(histograma)

print("Dados de estatística")
moda = histograma

plt.figure(figsize=(10, 5))

# Criando o histograma
plt.subplot(2, 4, 1)  # Duas linhas, 4 subplots, 1° subplot
df['valores'].hist(bins=intervalos)

plt.plot(histograma["Freq"], histograma["Inter"])

# Adicionando rótulos e título
plt.xlabel('Valores')
plt.ylabel('Frequência')
plt.title(f'Histograma de Valores ({len(frequencia.index)} intervalos)')

# Exibindo o histograma
plt.show()