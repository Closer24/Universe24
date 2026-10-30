"""David's probe of stage 5 (algebra/ring.py) on the module's own functions, exact integers.

usage: python3 -I p4_ring.py <worktree>/src
  T T = +1 on a hand, -1 on a twin hand; Lagrange N<phi,psi> + N<T phi,psi> = rho_phi rho_psi; S . S = rho rho;
  Kramers <T phi, phi> = 0; T reverses the spin, S(T psi) = -S(psi), and keeps rho; the overlap is sesquilinear;
  T commutes with the 2O lifts it must (the half-turn lifts i sigma_k, exact over Z[i]); the product is the ring's.
"""
import random
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.ring import add, axis, conj, mul, norm, overlap, pair, reverse  # noqa: E402

rng = random.Random(28)
B = 1 << 120


def g():
    return (rng.randint(-B, B), rng.randint(-B, B))


def tw():
    return (g(), g())


neg = lambda z: (-z[0], -z[1])  # noqa: E731
I = (0, 1)
fails = dict.fromkeys(("TT_hand", "TT_twin", "lagrange", "SS", "kramers", "spin", "sesqui", "lifts", "ring"), 0)
N = 20000
for _ in range(N):
    z, w, v = g(), g(), g()
    phi, psi = tw(), tw()
    fails["TT_hand"] += conj(conj(z)) != z
    fails["TT_twin"] += reverse(reverse(psi)) != (neg(psi[0]), neg(psi[1]))
    rp, rq = axis(phi)[0], axis(psi)[0]
    fails["lagrange"] += norm(overlap(phi, psi)) + norm(overlap(reverse(phi), psi)) != rp * rq
    rho, S = axis(psi)
    fails["SS"] += S[0] ** 2 + S[1] ** 2 + S[2] ** 2 != rho * rho
    fails["kramers"] += overlap(reverse(psi), psi) != (0, 0)
    rho2, S2 = axis(reverse(psi))
    fails["spin"] += (rho2, S2) != (rho, tuple(-x for x in S))
    # <phi, c psi> = c <phi, psi> and <c phi, psi> = conj(c) <phi, psi>
    c = g()
    cpsi = (mul(c, psi[0]), mul(c, psi[1]))
    cphi = (mul(c, phi[0]), mul(c, phi[1]))
    fails["sesqui"] += overlap(phi, cpsi) != mul(c, overlap(phi, psi)) or overlap(cphi, psi) != mul(conj(c), overlap(phi, psi))
    # half-turn lifts i sigma_x, i sigma_y, i sigma_z on (u, d), exact over Z[i]; T must commute with each
    u, d = psi
    lifts = [
        lambda p: (mul(I, p[1]), mul(I, p[0])),          # i sigma_x
        lambda p: (p[1], neg(p[0])),                      # i sigma_y
        lambda p: (mul(I, p[0]), neg(mul(I, p[1]))),      # i sigma_z
    ]
    fails["lifts"] += any(reverse(L(psi)) != L(reverse(psi)) for L in lifts)
    # the ring: associative, commutative, distributive, conj a ring map, the norm multiplicative
    fails["ring"] += (mul(mul(z, w), v) != mul(z, mul(w, v)) or mul(z, w) != mul(w, z)
                      or mul(z, add(w, v)) != add(mul(z, w), mul(z, v)) or conj(mul(z, w)) != mul(conj(z), conj(w))
                      or norm(mul(z, w)) != norm(z) * norm(w) or pair(z, w) != mul(conj(z), w))
for k, v in fails.items():
    print(f"{k}: failures {v} of {N} (120-bit draws)")
