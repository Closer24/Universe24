"""COMPACT-U(1) EM candidate (builder B1-EM, manager ruling 09:5x): the Dirac pair hops THROUGH integer complex links.

TENSOR BLOCKS ONLY. Reciprocal by construction (ONE potential, field sign +1 everywhere, b-only, rank 3 in the coupling;
the link dynamics, the 2-path plaquette gears and the OD4 spring are B1-GAUGE's u1 block, imported read-only).

Physical potential of the matter-link coupling (U = A*1 + W, the u1 block's deviation variables W stored):
    Psi = sum_x sum_d  b(x)^T M(U(x,d)) N_d b(x + e_d),   M(U) = U_re + U_im J',   N_d = kd P_d^T - kw W0
The vacuum part A*N_d is the matter block's own hopping (hop = A*kd, wilson = A*kw: build_matter(hop, wilson)), so
this block carries only the W part:
    Psi_c = sum_x sum_d b(x)^T [W_re(x,d) N_d + W_im(x,d) J' N_d] b(x + e_d)
    u_{W_re(x,d)} = b(x)^T N_d b(x+e_d),   u_{W_im(x,d)} = b(x)^T J' N_d b(x+e_d)
    u_b(x) += sum_d [W_re(x,d) N_d + W_im(x,d) J'N_d] b(x+e_d) + sum_d [W_re(x-e,d) N_d^T + W_im(x-e,d) (J'N_d)^T] b(x-e_d)
Gauge invariance (exact polynomial identity): b(x) -> M(g_x) b(x), U(x,d) -> g_x U(x,d) conj(g_{x+e_d}) (and B1-GAUGE's
P(x;k1,k2) -> g_x P conj(g_{x+e1+e2})); the integer subgroup Z4 = {1, i, -1, -i} acts by signed permutations
(M(i) = J'). The exact Gauss/Noether law (generator i: J' on the matter at y, left i on links/2-paths based at y,
minus right i on those ending at y) is evaluated by observe/em_compact.py.
"""
from __future__ import annotations

import numpy as np

from ..core.lattice import DIRECTIONS
from ..core.tensor import Block, GearType
from .matter import _block, _check_Q, _face, algebra, matter_names

AXES = ("x", "y", "z")


def link_names(ns: str = "u1") -> dict:
    """Qualified link gear names {axis: (re, im)} of the u1 block."""
    return {k: (f"{ns}.U{AXES[k]}_re", f"{ns}.U{AXES[k]}_im") for k in range(3)}


def build_u1_links(*, Q: int, A: int, lam: int, kappa_P: int, c_P: int, beta: int, use_P: bool = True,
                   name: str = "u1") -> Block:
    """B1-GAUGE's compact u1 block (layers/gauge.py, read-only import) WITHOUT its Gaussian-integer matter: called with
    kappa = 0 and mass = 0 (their matter is then decoupled) and the psi_* gears and their terms removed. The link
    inertia, 2-path gears and OD4 spring are theirs, unchanged (one potential; deviation form; Q declared)."""
    from .gauge import build_gauge
    blk = build_gauge(group="u1", Q=Q, A=A, kappa=0, mass=0, lam=lam, use_P=use_P, kappa_P=kappa_P, c_P=c_P,
                      beta=beta, name=name)
    keep = tuple(g for g in blk.gears if not g.name.startswith("psi_"))
    terms = tuple(t for t in blk.terms if not str(t[0]).startswith("psi_")
                  and not any(str(f[0]).startswith("psi_") for f in t[2]))
    params = dict(blk.params, source="layers.gauge.build_gauge(group='u1', kappa=0, mass=0) minus its psi gears",
                  matter="replaced by the B1-EM Dirac pair (layers/em_compact.py coupling)")
    kw = {"Q": Q} if "Q" in getattr(Block, "__dataclass_fields__", {}) else {}
    return Block(keep, terms, name=name, vacuum={g.name: blk.vacuum[g.name] for g in keep}, params=params,
                 doc=blk.doc + " [psi gears removed by B1-EM]", **kw)


def build_compact_coupling(*, Q: int, matter: Block, links: Block, kd: int, kw: int = 0, name: str = "cem") -> Block:
    """The W part of the matter-link coupling (see the module docstring). Requires the matter block's hop = A*kd and
    wilson = A*kw (A = links.params['A']) so that the vacuum hopping is the matter block's own."""
    _check_Q(Q)
    mp, lp = matter.params, links.params
    if mp.get("species") != "pair":
        raise ValueError("the compact route couples the charged species (the 16-channel pair)")
    if mp["Q"] != Q or lp["Q"] != Q:
        raise ValueError("ONE divisor: blocks with another Q")
    A = lp["A"]
    if mp["hop"] != A * kd or mp["wilson"] != A * kw:
        raise ValueError(f"vacuum hopping mismatch: need matter hop = A*kd = {A * kd}, wilson = A*kw = {A * kw}")
    alg = algebra("pair")
    P, W0, Jp = alg["P"], alg["W0"], alg["Jp"]
    mn = [matter.qualify(x) for x in matter_names("pair")]
    ln = {k: (links.qualify(f"U{AXES[k]}_re"), links.qualify(f"U{AXES[k]}_im")) for k in range(3)}
    n = 16
    terms = []
    Z = (0, 0, 0)
    for d in range(3):
        N = kd * P[d].T - kw * W0
        JN = Jp @ N
        fwd, back = _face(d, +1), _face(d, -1)
        wre, wim = ln[d]
        for i in range(n):
            for j in range(n):
                if N[i, j]:
                    c = int(N[i, j])
                    terms.append((wre, c, ((mn[i], Z, "b"), (mn[j], fwd, "b"))))               # u_Wre = b^T N b'
                    terms.append((mn[i], c, ((wre, Z, "b"), (mn[j], fwd, "b"))))               # u_b(x) += Wre N b(x+e)
                    terms.append((mn[j], c, ((wre, back, "b"), (mn[i], back, "b"))))           # u_b(x) += Wre(x-e) N^T b(x-e)
                if JN[i, j]:
                    c = int(JN[i, j])
                    terms.append((wim, c, ((mn[i], Z, "b"), (mn[j], fwd, "b"))))               # u_Wim = b^T J'N b'
                    terms.append((mn[i], c, ((wim, Z, "b"), (mn[j], fwd, "b"))))
                    terms.append((mn[j], c, ((wim, back, "b"), (mn[i], back, "b"))))
    return _block([], terms, name, {}, {"Q": Q, "kd": kd, "kw": kw, "A": A, "matter": matter.name,
                                        "links": links.name,
                                        "potential": "sum b(x)^T [W_re N_d + W_im J'N_d] b(x+e_d), N_d = kd P_d^T - kw W0",
                                        "reversor": "b-only: plain M' on every gear (fixes the joint vacuum, odd Q); "
                                                    "Dirac K o M' on the matter with the matching link map is not used"},
                  "compact-U(1) matter-link coupling (one potential, reciprocal, rank 3)", Q)


def default_compact(Q: int = (1 << 29) + 1, kd: int = 1 << 13, kw: int = 0, mass: int | None = None,
                    names=("matter", "u1", "cem")):
    """(matter, links, coupling) blocks of the compact candidate at B1-GAUGE's default family for Q = 2^29 + 1
    (A = 2^14, kappa_P = 256, c_P = 0, beta = 6Q - 2^29, lam = 4)."""
    from .matter import build_matter
    A = 1 << 14
    links = build_u1_links(Q=Q, A=A, lam=4, kappa_P=256, c_P=0, beta=6 * Q - (1 << 29), name=names[1])
    m = build_matter(Q=Q, hop=A * kd, mass=3 * Q if mass is None else mass, wilson=A * kw, name=names[0])
    c = build_compact_coupling(Q=Q, matter=m, links=links, kd=kd, kw=kw, name=names[2])
    return m, links, c
