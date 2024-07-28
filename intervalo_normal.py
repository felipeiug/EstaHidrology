from solvers import *

serie = [
    0.0092, 0.0085, 0.0083, 0.0091,
    0.0078, 0.0084, 0.0091, 0.0088,
    0.0086, 0.0090, 0.0089, 0.0093,
    0.0081, 0.0092, 0.0085, 0.0090,
    0.0085, 0.0088, 0.0088, 0.0093,
]

intervalo = Normal(serie)

print(f"Intervalo de confiança:")
for confianca in [80, 90, 95]:
    mi, sigma = intervalo.get_media_desvio(confianca=confianca)
    print(f"{confianca}%: μ e σ desconhecidos: μ = ({mi[0]:.6f} a {mi[1]:.6f}), σ² = ({(sigma[0]**2):.12f} a {(sigma[1]**2):.12f}) | Δμ={mi[1]-mi[0]}, Δσ²={(sigma[1]**2)-(sigma[0]**2)}")
