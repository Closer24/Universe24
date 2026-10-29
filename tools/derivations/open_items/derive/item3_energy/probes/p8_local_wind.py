"""P8 (question 4): the wind's local law at every Node-clock, with J and the drive, on the engine's own tick.

The wind's density at the clock i (each Mesh shared half and half between its two ends), doubled to stay whole:
    2 e_i = 2 W (a - b)^2 + 2 s D a b + s SUM over the six Spokes of g (a - a_j)(b - b_j)      (SUM_i e_i = E)
Derived (DRAFT.md, Q4): over one tick,
    2 de_i = 2 (a+ - b)(s T_k q - (r+ - r)) - SUM over the Spokes of 2 Phi,
    2 Phi(i -> j) = s g (a - a_j) [(a+ - b) + (a+_j - b_j)],   Phi(j -> i) = -Phi(i -> j)
so the wind at a clock moves by exactly its own click's work, its fine tooth's defect, and what its Meshes carry.
Checked per gear row and site: the law, the flux's antisymmetry, the densities' sum against P1's E; and the mutant with no
flux.
"""

import numpy as np
from common import act, ints, layout_of, state_of, wind
from tensor24.engine.state import Plan

ROWS, TERMS, PLANES = 3, 12, 5


def density2(lay, a, b):
    nb, meshes, grip, g, _, _, _ = lay
    w, s, d = g.w, g.stretch, g.spring
    mesh = (s[:, :, None] * grip[:, meshes] * (a[:, None, :] - a[:, nb]) * (b[:, None, :] - b[:, nb])).sum(axis=1)
    return 2 * w * (a - b) ** 2 + 2 * s * d * a * b + mesh


def flux2(lay, a, b, a1):
    """2 Phi per Spoke and site: (rows, 6, sites)."""
    nb, meshes, grip, g, _, _, _ = lay
    v = a1 - b
    return g.stretch[:, :, None] * grip[:, meshes] * (a[:, None, :] - a[:, nb]) * (v[:, None, :] + v[:, nb])


def main():
    rng = np.random.default_rng(8)
    law = anti = total = mutant = ticks = clicked = 0
    for world in range(300):
        shape = tuple(int(x) for x in rng.integers(1, 4, size=3))
        n = int(np.prod(shape))
        w = ints(rng, 1, 10, (ROWS, n))
        idx = [rng.integers(0, h, size=TERMS).astype(np.intp) for h in (PLANES * ROWS, PLANES * ROWS, ROWS)]
        plan = Plan(idx[0], idx[1], ints(rng, -3, 4, TERMS), idx[2])
        lay = layout_of(shape, w, ints(rng, 1, 4, (ROWS, 1)), ints(rng, -2, 4, (ROWS, 1)), ints(rng, 1, 4, (ROWS, 1)),
                        ints(rng, 1, 10, (ROWS, 1)), ints(rng, -3, 4, (ROWS, 3 * n)), plan)
        st = state_of(ints(rng, -40, 41, (ROWS, n)), ints(rng, -40, 41, (ROWS, n)),
                      ints(rng, 0, 1 << 20, (ROWS, n)) % w, ints(rng, 0, 1 << 20, (ROWS, n)) % lay.gearing.drive)
        g, nb = lay.gearing, lay.nb
        back = np.array([1, 0, 3, 2, 5, 4])  # the opposite Spoke
        for _ in range(6):
            now, _, _, q, _ = act(lay, st)
            ticks += 1
            e0, e1 = density2(lay, st.a, st.b), density2(lay, now.a, now.b)
            phi = flux2(lay, st.a, st.b, now.a)
            work = 2 * (now.a - st.b) * (g.stretch * g.kick * q - (now.r - st.r))
            law += int((e1 - e0 == work - phi.sum(axis=1)).all())
            mutant += int((e1 - e0 == work).all())
            anti += int(all((phi[:, sp, i] + phi[:, back[sp], nb[sp, i]] == 0).all()
                            for sp in range(6) for i in range(n)))
            total += int(all(e0.sum(axis=1) == 2 * wind(lay, st.a, st.b)))
            clicked += int(any(int(x) != 0 for x in q.flatten()))
            if max(abs(int(x)) for x in now.a.flatten()) > 1 << 50:
                break
            st = now
    print(f"300 worlds (W 1..9, s 1..3, D -2..3, grips -3..3, J random, T_d 1..9), {ticks} round-ticks, {clicked} with a drive quantum")
    print(f"  the local law 2 de_i = 2 (a+ - b)(s T_k q - (r+ - r)) - SUM 2 Phi, at every row and site: {law} of {ticks}")
    print(f"  the flux antisymmetric across every Mesh, Phi(i -> j) = -Phi(j -> i): {anti} of {ticks}")
    print(f"  the densities sum to the wind E of P1: {total} of {ticks}")
    print(f"  mutant, the law with no flux: {mutant} of {ticks}")


if __name__ == "__main__":
    main()
