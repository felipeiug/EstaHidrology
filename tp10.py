import numpy as np
from scipy.stats import lognorm, gumbel_r, gumbel_l, weibull_min
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from solvers.MOM.MOM_gumbel_max import GumbelMax

N = 100

#########################################
# 1)

# Log-Norm

Tr = np.linspace(1.01, 1000, N)
series = []

for i in [(169.08, 402.41), (130, 350), (15, 40)]:
    dist = lognorm(s=1, loc=i[0], scale=i[1])

    p = 1-(1/Tr)
    y = dist.ppf(p)

    x_plot:np.ndarray = y

    series.append((y, i[0], i[1]))

for serie in series:
    plt.plot(x_plot, serie[0], "-", label=f"s: 1\nμy: {serie[1]}\nσy: {serie[2]}")

def formatador(y_now, _):
    p_now = dist.cdf(y_now)
    Tr_now = 1/(1-p_now)

    num_str = str(np.round(Tr_now, 3))
    if int(num_str.split(".")[1]) > 0:
        num_str = float(num_str)
    else:
        num_str = int(num_str.split(".")[0])

    return f"${num_str}$"

plt.gca().xaxis.set_major_formatter(FuncFormatter(formatador))

plt.xticks([
    dist.ppf(1-1/1.01),
    dist.ppf(1-1/10),
    dist.ppf(1-1/30),
    dist.ppf(1-1/50),
    dist.ppf(1-1/100),
    dist.ppf(1-1/1000),
])

plt.ylabel("Quantil")
plt.xlabel("Tr (Anos)")
plt.title("Papel de Plotagem Log-Normal")

plt.grid(True)
plt.legend()

plt.savefig('log-norm.png', format='png')

plt.show()

# 1) Gumbel

Tr = np.linspace(1.01, 1000, N)
series = []

for i in [(169.08, 402.41), (130, 350), (15, 40)]:
    dist = gumbel_r(loc=i[0], scale=i[1])

    p = 1-(1/Tr)
    y = dist.ppf(p)

    x_plot:np.ndarray = y

    series.append((y, i[0], i[1]))

for serie in series:
    plt.plot(x_plot, serie[0], "-", label=f"α: {serie[1]}\nβ: {serie[2]}")

def formatador(y_now, _):
    p_now = dist.cdf(y_now)
    Tr_now = 1/(1-p_now)

    num_str = str(np.round(Tr_now, 3))
    if int(num_str.split(".")[1]) > 0:
        num_str = float(num_str)
    else:
        num_str = int(num_str.split(".")[0])

    return f"${num_str}$"

plt.gca().xaxis.set_major_formatter(FuncFormatter(formatador))

plt.xticks([
    dist.ppf(1-1/1.01),
    dist.ppf(1-1/10),
    dist.ppf(1-1/30),
    dist.ppf(1-1/50),
    dist.ppf(1-1/100),
    dist.ppf(1-1/1000),
])

plt.ylabel("Quantil")
plt.xlabel("Tr (Anos)")
plt.title("Papel de Plotagem Gumbel")

plt.grid(True)
plt.legend()

plt.savefig('gumbel.png', format='png')

plt.show()

####################################################################
# 4)
####################################################################

Tr = np.linspace(1.01, 1000, N)
series = []

serie_data = np.array([
    1342, 625, 619,  797,  1250, 271, 263,  566,  649, 236,
    474,  763, 592,  981,  438,  281, 556,  393,  726, 897,
    969,  566, 1300, 526,  520,  487, 897,  582,  510, 708,
    998,  477, 298,  872,  483, 1040, 1010, 1240, 697, 1406,
    801,  741, 1002, 1090, 589, 490,  2475, 2125,
])

gum_max = GumbelMax(serie_data)

for i in [gum_max.parametros()]:
    dist = gumbel_r(loc=i[0], scale=i[1])

    p = 1-(1/Tr)
    y = dist.ppf(p)

    x_plot:np.ndarray = y

    series.append((y, i[0], i[1]))

for serie in series:
    plt.plot(x_plot, serie[0], "-", label=f"α: {serie[1]}\nβ: {serie[2]}")


# Serie
p = np.arange(len(serie_data))+1
p = (p-0.44)/(len(serie_data)+0.12)
x_plot = dist.ppf(p)

serie_data.sort()
plt.scatter(x_plot, serie_data, marker="x", label="Descargas médias máxmas")

def formatador(y_now, _):
    p_now = dist.cdf(y_now)
    Tr_now = 1/(1-p_now)

    num_str = str(np.round(Tr_now, 3))
    if int(num_str.split(".")[1]) > 0:
        num_str = float(num_str)
    else:
        num_str = int(num_str.split(".")[0])

    return f"${num_str}$"

plt.gca().xaxis.set_major_formatter(FuncFormatter(formatador))

plt.xticks([
    dist.ppf(1-1/1.01),
    dist.ppf(1-1/10),
    dist.ppf(1-1/30),
    dist.ppf(1-1/50),
    dist.ppf(1-1/100),
    dist.ppf(1-1/1000),
])

plt.ylabel("Quantil")
plt.xlabel("Tr (Anos)")
plt.title("Papel de Plotagem Gumbel")

plt.grid(True)
plt.legend()

plt.savefig('gumbel_ex4.png', format='png')

plt.show()


########################################################
#12
########################################################

Tr = np.linspace(1.01, 1000, N)

alfa=6.482
beta=32.266
dist = gumbel_r(loc=alfa, scale=beta)
p = 1-(1/Tr)
y = dist.ppf(p)
x_plot:np.ndarray = y
plt.plot(x_plot, y, "-", label=f"Gumbel:\nα: {alfa}\nβ: {beta}")

k=4.23
alfa=31.403
dist = gumbel_r(loc=k, scale=alfa)
p = 1-(1/Tr)
y = dist.ppf(p)
x_plot:np.ndarray = y
plt.plot(x_plot, y, "-", label=f"Weibull:\nk: {k}\nα: {alfa}")

def formatador(y_now, _):
    p_now = dist.cdf(y_now)
    Tr_now = 1/(1-p_now)

    num_str = str(np.round(Tr_now, 3))
    if int(num_str.split(".")[1]) > 0:
        num_str = float(num_str)
    else:
        num_str = int(num_str.split(".")[0])

    return f"${num_str}$"

plt.gca().xaxis.set_major_formatter(FuncFormatter(formatador))

plt.xticks([
    dist.ppf(1-1/1.01),
    dist.ppf(1-1/10),
    dist.ppf(1-1/30),
    dist.ppf(1-1/50),
    dist.ppf(1-1/100),
    dist.ppf(1-1/1000),
])

plt.ylabel("Quantil")
plt.xlabel("Tr (Anos)")
plt.title("Papel de Plotagem Gumbel")

plt.grid(True)
plt.legend()

plt.savefig('gumbel_ex12.png', format='png')

plt.show()

