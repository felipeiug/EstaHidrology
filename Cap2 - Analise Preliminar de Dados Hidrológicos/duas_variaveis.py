import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes._axes import Axes

def dispersao(ax:Axes, serie:pd.DataFrame, col_y1, col_y2, col_x):
    ax.scatter(serie[col_y1], serie[col_y2])
    ax.set_ylabel(col_y2)
    ax.set_xlabel(col_y1)
    ax.set_title("Diagrama de Dispersão")
    
    correlacao = serie[col_y1].corr(serie[col_y2])
    print(f"Grau de associação linear (Correlação): {correlacao}")

def quantis(ax:Axes, serie:pd.DataFrame, col_y1, col_y2, col_x):
    serie.sort_values(by=col_y1, inplace=True, ignore_index=True)
    col1 = serie[col_y1]

    serie.sort_values(by=col_y2, inplace=True, ignore_index=True)
    col2 = serie[col_y2]

    ax.scatter(col1, col2)
    ax.set_ylabel(col_y2)
    ax.set_xlabel(col_y1)
    ax.set_title("Diagrama de Q-Q")

if __name__ == "__main__":
    anos = [
        "1941/42",
        "1942/43",
        "1943/44",
        "1944/45",
        "1945/46",
        "1946/47",
        "1947/48",
        "1948/49",
        "1949/50",
        "1950/51",
        "1951/52",
        "1952/53",
        "1953/54",
        "1954/55",
        "1955/56",
        "1956/57",
        "1957/58",
        "1958/59",
        "1959/60",
        "1960/61",
        "1961/62",
        "1962/63",
        "1963/64",
        "1964/65",
        "1965/66",
        "1966/67",
        "1967/68",
        "1968/69",
        "1969/70",
        "1970/71",
        "1971/72",
        "1972/73",
        "1973/74",
        "1974/75",
        "1975/76",
        "1976/77",
        "1977/78",
        "1978/79",
        "1979/80",
        "1980/81",
        "1981/82",
        "1982/83",
        "1983/84",
        "1984/85",
        "1985/86",
        "1986/87",
        "1987/88",
        "1988/89",
        "1989/90",
        "1990/91",
        "1991/92",
        "1992/93",
        "1993/94",
        "1994/95",
        "1995/96",
        "1996/97",
        "1997/98",
        "1998/99",
    ]

    precip = [
        1249,
        1319,
        1191,
        1440,
        1251,
        1507,
        1363,
        1814,
        1322,
        1338,
        1327,
        1301,
        1138,
        1121,
        1454,
        1648,
        1294,
        883,
        1601,
        1487,
        1347,
        1250,
        1298,
        1673,
        1452,
        1169,
        1189,
        1220,
        1306,
        1013,
        1531,
        1487,
        1395,
        1090,
        1311,
        1291,
        1273,
        2027,
        1697,
        1341,
        1764,
        1786,
        1728,
        1880,
        1429,
        1412,
        1606,
        1290,
        1451,
        1447,
        1581,
        1642,
        1341,
        1359,
        1503,
        1927,
        1236,
        1163,
    ]

    vazao = [
        91.9,
        145,
        90.6,
        89.9,
        79.0,
        90.0,
        72.6,
        135,
        82.7,
        112,
        95.3,
        59.5,
        53.0,
        52.6,
        62.3,
        85.6,
        67.8,
        52.5,
        64.6,
        122,
        64.8,
        63.5,
        54.2,
        113,
        110,
        102,
        74.2,
        56.4,
        72.6,
        34.5,
        80.0,
        97.3,
        86.8,
        67.6,
        54.6,
        88.1,
        73.6,
        134,
        104,
        80.7,
        109,
        148,
        92.9,
        134,
        88.2,
        79.4,
        79.5,
        58.3,
        64.7,
        105,
        99.5,
        95.7,
        86.1,
        71.8,
        86.2,
        127,
        66.3,
        59.0,
    ]

    serie = pd.DataFrame({
        "Ano":anos,
        "Precipitação (mm)":precip,
        "Vazao (m³/s)":vazao
    })

    fig, ax = plt.subplots(1,1)
    dispersao(ax, serie, "Precipitação (mm)", "Vazao (m³/s)", "Ano")

    plt.show()

    fig, ax = plt.subplots(1,1)
    quantis(ax, serie, "Vazao (m³/s)", "Precipitação (mm)", "Ano")

    plt.show()


