"""Probe 3: per-site stress of the bang pattern; spinor identities (S.S = rho^2, Fierz, Lagrange)."""
import random

p1 = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2]
L = 4
def hand(x, y, z, t, sense=1):
    return 1j ** (((p1[4 * (x % 4) + (y % 4)] + z) + sense * t) % 4)
for sense in (1, -1):
    sites = set()
    for x in range(L):
        for y in range(L):
            for z in range(L):
                vel = hand(x, y, z, 1, sense) - hand(x, y, z, -1, sense)  # u_in + u_out ~ next - before
                g = []
                for e in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
                    g.append((hand(x + e[0], y + e[1], z + e[2], 0, sense) - hand(x - e[0], y - e[1], z - e[2], 0, sense)) / 2)
                P = tuple(round((vel.conjugate() * ga).real, 9) for ga in g)
                T = tuple(round(abs(ga) ** 2, 9) for ga in g)
                sites.add((P, T))
    print("rotation sense", sense, "distinct (momentum, diagonal stress) per site:", sites)

# spinor identities over Gaussian integers
random.seed(7)
def gi():
    return complex(random.randint(-10**6, 10**6), random.randint(-10**6, 10**6))
def S_of(a, b):
    c = a.conjugate() * b
    return (2 * c.real, 2 * c.imag, abs(a) ** 2 - abs(b) ** 2)
fail = 0
for _ in range(20000):
    p = (gi(), gi()); f = (gi(), gi())
    rho = abs(p[0]) ** 2 + abs(p[1]) ** 2
    rhod = abs(f[0]) ** 2 + abs(f[1]) ** 2
    S = S_of(*p); m = S_of(*f)
    ov = f[0].conjugate() * p[0] + f[1].conjugate() * p[1]
    fperp = (-f[1].conjugate(), f[0].conjugate())
    ovp = fperp[0].conjugate() * p[0] + fperp[1].conjugate() * p[1]
    ok1 = abs(sum(s * s for s in S) - rho * rho) <= 1e-6 * rho * rho
    ok2 = abs(rho * rhod + sum(a * b for a, b in zip(S, m)) - 2 * abs(ov) ** 2) <= 1e-6 * rho * rhod
    ok3 = abs(abs(ov) ** 2 + abs(ovp) ** 2 - rho * rhod) <= 1e-6 * rho * rhod
    fail += not (ok1 and ok2 and ok3)
print("S.S = rho^2, Fierz, Lagrange failures in 20,000:", fail, "(so S = 0 forces rho = 0: no pure twin state has an 'open axis')")
