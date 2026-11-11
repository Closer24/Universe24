"""Read-only observables / audit maps for the unified-matter U(6) construction (layers/unified_matter.py). Reuses the frozen
observe.gauge.GaugeView machinery (Noether pieces, exact charge and remainder term, integer gauge maps) with the
M6(C) algebra and the 48 matter gears of the colour triplet."""
from __future__ import annotations
import random
import numpy as np
from ..core.tensor import Tensor
from ..layers.unified_matter import N6, algebra_u6, link_names, matter_gears, mn_index
from .gauge import GaugeView

class UnifiedMatterView(GaugeView):

    def __init__(self, tensor: Tensor, A: int, matter_ns=('q0', 'q1', 'q2'), link_ns: str='u6'):
        self.tensor = tensor
        self.alg = algebra_u6()
        self.group = 'u6'
        self.D = 6
        self.A = A
        self.name = link_ns
        self.p = {'group': 'u6', 'A': A}
        self.matter = [tensor.gear_index(g) for g in matter_gears(matter_ns)]
        self.links = {k: [tensor.gear_index(g) for g in v] for k, v in link_names(link_ns).items()}
        self.paths = {}
        self.x0 = np.zeros(tensor.G, dtype=object)
        for k in range(3):
            for c, gi in enumerate(self.links[k]):
                self.x0[gi] = A * self.alg.one[c]
        self.own = sorted(self.matter + [i for v in self.links.values() for i in v])

    def gauge_map(self, state, gfield):
        """Same audit map as GaugeView.gauge_map (integer, signed permutations + affine shift in deviation form),
        with the 72 x 72 two-sided products done by numpy on exact int64 sign matrices (speed only)."""
        from ..core.engine import OBJ, State
        from ..core.lattice import lattice
        from ..layers.gauge import UNIT
        from .gauge import rprime
        alg, D = (self.alg, self.D)
        lat = lattice(state.L)
        a, b, r = (state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ))
        na, nb, nr = (a.copy(), b.copy(), r.copy())
        cache = {}

        def two_sided(g, h):
            key = (tuple(g), tuple(h))
            if key not in cache:
                Lm = np.array(alg.left_matrix(list(g)), dtype=np.int64)
                Rm = np.array(alg.right_matrix(alg.dagger(list(h))), dtype=np.int64)
                cache[key] = Lm @ Rm
            return cache[key]

        def apply(rows, n, M, x0vec):
            M = np.asarray(M)
            src_a = [a[gi, n] + x0vec[i] for i, gi in enumerate(rows)]
            src_b = [b[gi, n] + x0vec[i] for i, gi in enumerate(rows)]
            for i, gi in enumerate(rows):
                nzj = np.flatnonzero(M[i])
                assert len(nzj) == 1
                j = int(nzj[0])
                s = int(M[i, j])
                na[gi, n] = s * src_a[j] - x0vec[i]
                nb[gi, n] = s * src_b[j] - x0vec[i]
                nr[gi, n] = r[rows[j], n] if s == 1 else int(rprime(np.array(r[rows[j], n]), D))
        for n in range(lat.N):
            x = lat.coords(n)
            g = list(gfield[n])
            apply(self.matter, n, np.array(alg.act_matrix(g), dtype=np.int64), [0] * alg.n)
            for k in range(3):
                h = list(gfield[lat.index(*(x[i] + UNIT[k][i] for i in range(3)))])
                apply(self.links[k], n, two_sided(g, h), [self.x0[i] for i in self.links[k]])
        return State(state.L, na, nb, nr)

def random_unit(rng: random.Random, kind: str='u6'):
    """A random integer unit of M6(C): a monomial matrix with entries +-1, +-i ('u6'), or a product
    (colour monomial 3x3 with entries +-1/+-i) (x) (pair monomial 2x2 with entries +-1/+-i) ('product')."""
    v = [0] * (2 * N6 * N6)
    if kind == 'u6':
        perm = list(range(N6))
        rng.shuffle(perm)
        for k in range(N6):
            ph = rng.randrange(4)
            v[mn_index(k, perm[k], ph % 2)] = 1 if ph < 2 else -1
        return v
    pc = list(range(3))
    rng.shuffle(pc)
    pw = list(range(2))
    rng.shuffle(pw)
    phc = [rng.randrange(4) for _ in range(3)]
    phw = [rng.randrange(4) for _ in range(2)]
    for a in range(3):
        for s in range(2):
            ph = (phc[a] + phw[s]) % 4
            v[mn_index(2 * a + s, 2 * pc[a] + pw[s], ph % 2)] = 1 if ph < 2 else -1
    return v
__all__ = ['UnifiedMatterView', 'random_unit']
