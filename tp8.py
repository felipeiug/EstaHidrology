from solvers import *
from teste_hipotese import Normal as HipNormal
from teste_hipotese import Normal2Series as HipNormal2
from teste_hipotese import Aleatoriedade, Independencia, Homogeneidade, Estacionariedade
import pandas as pd
from helpers import hipotesis_to_str

serie = """1938 1 104.3 51 1 18.20 43.6
1939 2 97.9 45 1 11.80 46.8
1940 3 89.2 38 1 3.10 49.4
1941 4 92.7 40 1 6.60 50.1
1942 5 98 4 6 1 11.90 53.1
1943 6 141.7 60 1 55.60 57
1944 7 81.1 30 1 -5.00 57.3
1945 8 97.3 43 1 11.20 59.9
1946 9 72 2 0 1 -14.10 60.6
1947 10 93.9 41 1 7.80 61.2
1948 11 83.8 33 1 -2.30 62.6
1949 12 122.8 58 1 36.70 63.6
1950 13 87.6 36 1 1.50 64.2
1951 14 101 5 0 1 14.90 66.8
1952 15 97.8 44 1 11.70 67.2
1953 16 59.9 8 1 -26.20 68.2
1954 17 49.4 3 1 -36.70 68.7
1955 18 57 6 1 -29.10 69.3
1956 19 68.2 16 1 -17.90 71.6
1957 20 83.2 32 1 -2.90 72
1958 21 60.6 9 1 -25.50 72.4
1959 22 50.1 4 1 -36.00 74.8
1960 23 68.7 17 1 -17.40 76.4
1961 24 117.1 56 1 31.00 77.6
1962 25 80.2 28 1 -5.90 78
1963 26 43.6 1 1 -42.50 78.9
1964 27 66.8 14 1 -19.30 7 9
1965 28 118.4 57 1 32.30 80.2
1966 29 110.4 52 1 24.30 80.9
1967 30 99.1 47 1 13.00 81.1
1968 31 71.6 19 1 -14.50 82.2
1969 32 62.6 11 2 -23.50 83.2
1970 33 61.2 10 2 -24.90 83.8
1971 34 46.8 2 2 -39.30 85.1
1972 35 79 2 7 2 -7.10 87.4
1973 36 96.3 42 2 10.20 87.6
1974 37 77.6 24 2 -8.50 88.1
1975 38 69.3 18 2 -16.80 89.2
1976 39 67.2 15 2 -18.90 89.8
1977 40 72.4 21 2 -13.70 92.7
1978 41 78 2 5 2 -8.10 93.9
1979 42 141.8 61 2 55.70 96.3
1980 43 100.7 49 2 14.60 97.3
1981 44 87.4 35 2 1.30 97.8
1982 45 100.2 48 2 14.10 97.9
1983 46 166.9 62 2 80.80 9 8
1984 47 74.8 22 2 -11.30 99.1
1985 48 133.4 59 2 47.30 100.2
1986 49 85.1 34 2 -1.00 100.7
1987 50 78.9 26 2 -7.10 101
1988 51 76.4 23 2 -9.70 104.3
1989 52 64.2 13 2 -21.90 110.4
1990 53 53.1 5 2 -33.00 110.8
1991 54 112.2 54 2 26.10 112.2
1992 55 110.8 53 2 24.70 114.9
1993 56 82.2 31 2 -3.90 117.1
1994 57 88.1 37 2 2.00 118.4
1995 58 80.9 29 2 -5.20 122.8
1996 59 89.8 39 2 3.70 133.4
1997 60 114.9 55 2 28.80 141.7
1998 61 63.6 12 2 -22.50 141.8
1999 62 57.3 7 2 -28.80 166.9"""

dados = {
    "ano": [],
    "T": [],
    "X": [],
    "m": [],
    "sub_amostra": [],
    "X_X_":[],
    "X_class":[],
}
for i in serie.split("\n"):
    for col, dado in zip(dados.keys(), i.split(" ")):
        dados[col].append(float(dado))

serie = pd.DataFrame(dados)

print(serie)

# Intervalo de confiança
intervalo = Normal(serie["X"])

print(f"\nIntervalo de confiança:")
for confianca in [80, 90, 95]:
    mi, sigma = intervalo.get_media_desvio(confianca=confianca, mi=86.105)
    print(f"{confianca}%: μ e σ desconhecidos: μ = ({mi[0]:.6f} a {mi[1]:.6f}), σ² = ({(sigma[0]**2):.12f} a {(sigma[1]**2):.12f}) | Δμ={mi[1]-mi[0]}, Δσ²={(sigma[1]**2)-(sigma[0]**2)}")

# Teste de hipótese
testeHipotese = HipNormal(serie["X"])
print("\nTeste de Hipótese")

print("Ex: 9")
hipo = testeHipotese.σ.H0_equals_H1_under(25, alfa=5)
print(hipotesis_to_str(hipo))


serie1 = serie[serie["ano"] < 1969]["X"]
serie2 = serie[serie["ano"] >= 1969]["X"]

testeHipose2 = HipNormal2(serie1, serie2)
print("Ex 10")
hipo = not testeHipose2.σ.H0_equals_H1_different(1, 1, alfa=5)
print(hipotesis_to_str(hipo))

print("Ex 11")
hipo = testeHipose2.σ.H0_equals_H1_above(1.1, 1, alfa=5)
print(hipotesis_to_str(hipo))


print("Ex 13")

dados_serie = """41/42
42/43
43/44
44/45
45/46
46/47
47/48
48/49
49/50
50/51
51/52
52/53
53/54
54/55
55/56
68,8
-
-
67,3
-
70,2
113,2
79,2
61,2
66,4
65,1
115
67,3
102,2
54,4
56/57
57/58
58/59
59/60
60/61
61/62
62/63
63/64
64/65
65/66
66/67
67/68
68/69
69/70
70/71
69,3
54,3
36
64,2
83,4
64,2
76,4
159,4
62,1
78,3
74,3
41
101,6
85,6
51,4
71/72
72/73
73/74
74/75
75/76
76/77
77/78
78/79
79/80
80/81
81/82
82/83
83/84
84/85
85/86
70,3
81,3
85,3
58,4
66,3
91,3
72,8
100
78,4
61,8
83,4
93,4
99
133
101
86/87
87/88
88/89
89/90
90/91
91/92
92/93
93/94
94/95
95/96
96/97
97/98
98/99
99/00
109
88
99,6
74
94
99,2
101,6
76,6
84,8
114,4
-
95,8
65,4
114,8"""

anos_de = []
anos_ate = []

values = []

get_anos = True
for value in dados_serie.split("\n"):
    if "/" in value:
        anos_de.append(int(value.split("/")[0]))
        anos_ate.append(int(value.split("/")[1]))

    else:
        if "-" in value:
            val = None
        else:
            val = float(value.replace(",", "."))

        values.append(val)
    
df_dados:pd.DataFrame = pd.DataFrame({
    "anos_de":anos_de,
    "anos_ate":anos_ate,
    "dados":values,
})

df_dados.dropna(inplace=True)

# aleatorio = Aleatoriedade(df_dados["dados"])
# hipo = aleatorio.aleatorio(34)
# print("É aleatório" if hipo else "Não é aleatório")

independencia = Independencia(df_dados["dados"])
hipo = independencia.teste_independencia(5)
print("As amostras são independentes" if hipo else "As amostras não são independentes")

homogeneidade = Homogeneidade(df_dados["dados"])
hipo = homogeneidade.teste_homogeneidade(5)
print("A amostra é homogênea" if hipo else "A amostra não é homogênea")

estacionariedade = Estacionariedade(df_dados["dados"], df_dados["anos_de"])
hipo = estacionariedade.teste_estacionariedade(5)
print("As amostra é estacionária" if hipo else "As amostra não é estacionária")


