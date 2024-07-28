from solvers import *
from correlacao_regressao.regressao_lin import RegressaoLin
import pandas as pd
from helpers import hipotesis_to_str
import matplotlib.pyplot as plt
from sympy import Eq, log as ln, lambdify

h = [
    0, 0.8, 1.19, 1.56, 1.91, 2.36, 2.7, 4.07,
    4.73, 4.87, 5.84, 7.19, 8.21, 8.84, 9.64,
]

q = [
    20, 40, 90, 120, 170, 240, 300, 680, 990,
    990, 1260, 1920, 2540, 2840, 3320,    
]

df = pd.DataFrame({
    "H": h,
    "Q": q,
})

x_eixo = "H"
y_eixo = "Q"

print("Ex 8")
print("Letra a")
regressao = RegressaoLin(df[x_eixo], df[y_eixo])
regressao.plot_series(just_series=True)

print("Letra b")
df.sort_values(by="Q", ignore_index=True, inplace=True)

print("Q = a + bH + cH²")

x0 = df[x_eixo].values[0]
y0 = df[y_eixo].values[0]
x_x0 = df[x_eixo] - x0
y_y0 = df[y_eixo] - y0

xs = x_x0
ys = y_y0/x_x0
regressao = RegressaoLin(xs[1:-2], ys[1:-2])
regressao.plot_series(just_series=True)

a1 = regressao.a
a2 = regressao.b

def f(x):
    y = symbols("y")
    eq = Eq((y-y0)/(x-x0), a1 + 2*a1*x0 + a2*(x-x0))
    eq = solve(eq, y)
    return eq[0]

x = symbols("x")

print(f"a1 = {regressao.a}")
print(f"a2 = {regressao.b}")
print(f"r² = {regressao.r2}")
print(f"se = {regressao.se}")
eq1_str = str(f(x).evalf(4)).replace("**", "^").replace("*", "")
print(f"Equação: {eq1_str}")
eq1 = lambdify(x, f(x).evalf(4), "numpy")

#### Segunda parte
print("Q = a(H-h0)^n")
print("Q = a(X^n)")

xs = np.log((df[x_eixo]-0)[1:-2]) #<- h0 = 0, sem altura, sem vazão
ys = np.log(df[y_eixo][1:-2])

regressao = RegressaoLin(xs, ys) # <- Posso retirar um item que não é compatível com a transformada?
regressao.plot_series(just_series=True)

a = regressao.a
b = regressao.b

def f(x):
    y = symbols("y")
    eq = Eq(ln(y), a+b*ln(x))
    eq = solve(eq, y)
    return eq[0]

def f_inversa(y):
    x = symbols("x")
    eq = Eq(x, (y/np.exp(a))**(1/b))
    eq = solve(eq, x)
    return eq[0]


x = symbols("x")

print(f"a1 = {regressao.a}")
print(f"a2 = {regressao.b}")
print(f"r² = {regressao.r2}")
print(f"se = {regressao.se}")
eq2_str = str(f(x).evalf(4)).replace("**", "^").replace("*", "")
print(f"Equação: {eq2_str}")
eq2 = lambdify(x, f(x).evalf(4), "numpy")

print("Letra c")

plt.scatter(df[x_eixo], df[y_eixo], color="blue", label="Série observada")

xs = np.array(range(0, (int(df[x_eixo].max())+1)*1000))
xs = xs/1000

ys_parabola = eq1(xs)
plt.plot(xs, ys_parabola, color="red", label=eq1_str)

ys_exp = eq2(xs)
plt.plot(xs, ys_exp, color="green", label=eq2_str)

# Adicionar a legenda
plt.legend()

# Adicionar títulos e rótulos aos eixos
plt.title('Curva chave')
plt.xlabel('H(m)')
plt.ylabel('Q(m³/s)')

plt.show()

xs = df[x_eixo]
ys = df[y_eixo]

ys_est_parabola = eq1(xs)
s2_res_1 = np.sum(np.power(ys-ys_est_parabola, 2))/(xs.size-2)
print(f"Variância residual 1 (s²res) = {s2_res_1}")

ys_est_exponencial = eq2(xs)
s2_res_2 = np.sum(np.power(ys-ys_est_exponencial, 2))/(xs.size-2)
print(f"Variância residual 2 (s²res) = {s2_res_2}")

print("Letra d")

Q = 5200
fy = f_inversa(Q)

print(f"Altura para Q=5200m³/s: {fy:.4f}")
print(f"Checando: {eq2(np.array(fy))}")