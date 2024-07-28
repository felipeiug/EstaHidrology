from math import gamma
from numpy import sqrt, log as ln
import pandas as pd

#Entradas
E_X=694.6
Var_X=26186.62

T=25

#Tabela

CV = sqrt(Var_X)/E_X

val = """0.000 1.0000 1.0000 0.0000 0.105 0.9493 0.9155 0.1259 0.2100 0.9155 0.8863 0.2394
0.005 0.9971 0.9943 0.0063 0.110 0.9474 0.9131 0.1316 0.2150 0.9143 0.8860 0.2446
0.010 0.9943 0.9888 0.0127 0.115 0.9454 0.9107 0.1372 0.2200 0.9131 0.8858 0.2498
0.015 0.9915 0.9835 0.0190 0.120 0.9435 0.9085 0.1428 0.2250 0.9119 0.8856 0.2549
0.020 0.9888 0.9784 0.0252 0.125 0.9417 0.9064 0.1483 0.2300 0.9107 0.8856 0.2601
0.025 0.9861 0.9735 0.0315 0.130 0.9399 0.9044 0.1539 0.2310 0.9105 0.8856 0.2611
0.030 0.9835 0.9687 0.0376 0.135 0.9381 0.9025 0.1594 0.2320 0.9103 0.8856 0.2621
0.035 0.9809 0.9641 0.0438 0.140 0.9364 0.9007 0.1649 0.2340 0.9098 0.8856 0.2642
0.040 0.9784 0.9597 0.0499 0.145 0.9347 0.8990 0.1703 0.2350 0.9096 0.8856 0.2652
0.045 0.9759 0.9554 0.0559 0.150 0.9330 0.8974 0.1758 0.2355 0.9095 0.8856 0.2657
0.050 0.9735 0.9513 0.0619 0.155 0.9314 0.8960 0.1812 0.2360 0.9094 0.8856 0.2662
0.055 0.9711 0.9474 0.0679 0.160 0.9298 0.8946 0.1866 0.2361 0.9093 0.8856 0.2663
0.060 0.9687 0.9435 0.0739 0.165 0.9282 0.8933 0.1919 0.2362 0.9093 0.8856 0.2664
0.065 0.9664 0.9399 0.0798 0.170 0.9267 0.8922 0.1973 0.2363 0.9093 0.8856 0.2665
0.070 0.9641 0.9364 0.0857 0.175 0.9252 0.8911 0.2026 0.2364 0.9093 0.8856 0.2666
0.075 0.9619 0.9330 0.0915 0.180 0.9237 0.8901 0.2079 0.2364 0.9093 0.8856 0.2667
0.080 0.9597 0.9298 0.0973 0.185 0.9222 0.8893 0.2132
0.085 0.9575 0.9267 0.1031 0.190 0.9208 0.8885 0.2185
0.090 0.9554 0.9237 0.1088 0.195 0.9195 0.8878 0.2238
0.095 0.9533 0.9208 0.1146 0.200 0.9181 0.8872 0.2290
0.100 0.9513 0.9181 0.1203 0.205 0.9168 0.8867 0.2342"""

val = val.replace("\n", " ")

CVs = []
_1_alfa=[]
A_alfa=[]
B_alfa=[]

identificador = 0
for n, valor in enumerate(val.split(" ")):
    
    if identificador == 0:
        _1_alfa.append(float(valor))
    elif identificador == 1:
        A_alfa.append(float(valor))
    elif identificador == 2:
        B_alfa.append(float(valor))
    elif identificador == 3:
        CVs.append(float(valor))

    identificador +=1

    if (n+1)%4==0:
        identificador=0


tabela = pd.DataFrame({
    "CV":CVs,
    "1_alfa":_1_alfa,
    "A_alfa":A_alfa,
    "B_alfa":B_alfa,
})

tabela.sort_values(by="CV", inplace=True, ignore_index=True)

if CV > tabela['CV'].max():
    maior = tabela.loc[tabela['CV'].idxmax()]
else:
    maior = tabela.loc[tabela[tabela['CV'] >= CV]['CV'].idxmin()]

if CV < tabela['CV'].min():
    menor = tabela.loc[tabela['CV'].idxmin()]
else:
    menor = tabela.loc[tabela[tabela['CV'] <= CV]['CV'].idxmax()]

if (maior == menor).all():
    a_alfa = menor["A_alfa"]
    b_alfa = menor["B_alfa"]
    sobre_alfa = menor["1_alfa"]
else:
    a_alfa = menor["A_alfa"] + ((maior["A_alfa"]-menor["A_alfa"])*(CV - menor["CV"]))/(maior["CV"] - menor["CV"])
    b_alfa = menor["B_alfa"] + ((maior["B_alfa"]-menor["B_alfa"])*(CV - menor["CV"]))/(maior["CV"] - menor["CV"])
    sobre_alfa = menor["1_alfa"] + ((maior["1_alfa"]-menor["1_alfa"])*(CV - menor["CV"]))/(maior["CV"] - menor["CV"])



#Alfa
alfa = 1/sobre_alfa
beta=E_X/a_alfa

vazao = beta*((-ln(1-(1/T)))**(1/alfa))

print(f"α: {alfa}, β: {beta}, Vazão T({T}): {vazao}")

    
    