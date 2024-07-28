from solvers import *
from distribuicoes import Gumbel_Max
import pandas as pd

serie = [
    576, 414,  472, 458, 684, 408, 371, 333, 570, 502, 810, 366, 690, 570,
    288, 295,  498, 470, 774, 388, 408, 448, 822, 414, 515, 748, 570, 726,
    580, 450,  478, 340, 246, 568, 520, 449, 357, 276, 736, 822, 550, 698,
    585, 1017, 437, 549, 601, 288, 481, 927, 827, 424, 603, 633, 695, 296, 427
]

df = pd.DataFrame({"dados": serie})

mom = MOM(df["dados"])
mvs = MVS(df["dados"])
mml = MML(df["dados"])

alfa_mom, beta_mom = mom.gumbel_max.parametros()
alfa_mvs, beta_mvs = mvs.gumbel_max.parametros(alfa_init=alfa_mom)
alfa_mml, beta_mml = mml.gumbel_max.parametros()

print(f"μ: {df['dados'].mean()}, σ: {df['dados'].std()}")

print(f"MOM -> α: {alfa_mom}, β: {beta_mom}")
print(f"MVS -> α: {alfa_mvs}, β: {beta_mvs}")
print(f"MML -> α: {alfa_mml}, β: {beta_mml}")

gum_mom = Gumbel_Max(alfa=alfa_mom, beta=beta_mom)
gum_mvs = Gumbel_Max(alfa=alfa_mvs, beta=beta_mvs)
gum_mml = Gumbel_Max(alfa=alfa_mml, beta=beta_mml)

print(f"MOM -> P(Q>1000): {gum_mom.p > 1000}")
print(f"MVS -> P(Q>1000): {gum_mvs.p > 1000}")
print(f"MML -> P(Q>1000): {gum_mml.p > 1000}")

print(f"MOM -> Q(T=100): {gum_mom.quantil_TR(100)}")
print(f"MVS -> Q(T=100): {gum_mvs.quantil_TR(100)}")
print(f"MML -> Q(T=100): {gum_mml.quantil_TR(100)}")

confianca = 95
print(f"\nIntervalo de confiança {confianca}%")
print("MOM:")
for tr in [2, 10, 50, 100, 500, 1000, 10000, 100000, 1000000, 1500000]:
    menor, maior = mom.gumbel_max.interval_Tr(confianca, tr)
    print(f"  Tr: {tr} -> [{maior}, {menor}] | {maior-menor}")

print("MVS:")
for tr in [2, 10, 50, 100, 500, 1000, 10000, 100000, 1000000, 1500000]:
    menor, maior = mvs.gumbel_max.interval_Tr(confianca, tr)
    print(f"  Tr: {tr} -> [{maior}, {menor}] | {maior-menor}")

print("MML:")
for tr in [2, 10, 50, 100, 500, 1000, 10000, 100000, 1000000, 1500000]:
    menor, maior = mml.gumbel_max.interval_Tr(confianca, tr)
    print(f"  Tr: {tr} -> [{maior}, {menor}] | {maior-menor}")

