"""The click of a split's sizes as Gaussian norms: rho rho_d + S . m = 2 N(<phi, psi>) (Fierz), and
N(<phi, psi>) + N(<phi_perp, psi>) = rho rho_d (Lagrange), on random Gaussian-integer spinors."""
import random
random.seed(24)
def conj(z): return (z[0], -z[1])
def mul(z, w): return (z[0]*w[0] - z[1]*w[1], z[0]*w[1] + z[1]*w[0])
def add(z, w): return (z[0]+w[0], z[1]+w[1])
def norm(z): return z[0]*z[0] + z[1]*z[1]
def bil(psi):
    a, b = psi
    rho = norm(a) + norm(b)
    ab = mul(conj(a), b)
    S = (ab[0] + ab[0], ab[1] + ab[1], norm(a) - norm(b))
    return rho, S
bad = 0
for _ in range(20000):
    g = lambda: (random.randint(-10**6, 10**6), random.randint(-10**6, 10**6))
    psi, phi = (g(), g()), (g(), g())
    rho, S = bil(psi); rd, m = bil(phi)
    overlap = add(mul(conj(phi[0]), psi[0]), mul(conj(phi[1]), psi[1]))
    perp = ((-phi[1][0], phi[1][1]), (phi[0][0], -phi[0][1]))  # (-conj(phi2), conj(phi1))
    over_perp = add(mul(conj(perp[0]), psi[0]), mul(conj(perp[1]), psi[1]))
    lhs = rho*rd + sum(s*t for s, t in zip(S, m))
    if lhs != norm(overlap) + norm(overlap) or norm(overlap) + norm(over_perp) != rho*rd:
        bad += 1
print("draws 20000, failures", bad)
