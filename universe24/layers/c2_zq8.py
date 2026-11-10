"""c2 as ZQ8 with ONE OD4 SPRING PER SIMPLE COMPONENT (INTEGRATOR, manager 11:2x: condition (c) of the sign-class
decision). NEW file; layers/links.py (frozen STAGE 1-GAUGE) is imported read-only and its ZQ8 construction is
repeated here with three DATA/PARAMETER changes:

  * body_signs: the reference ports/weights of either class (R_q commutes with the signed ports of +++ AND of the
    handed class (1,-1,1): 0 of 48 (q, d) pairs fail, checked 11:19 UTC), so local Q8 stays bit-exact;
  * port_weight w_p in {Q, Q - 1}: the L0 port weight the links multiply (kappa * A = w_p). Q is today's board;
    Q - 1 is the form-C L0 (layers/gravity_l0c.py). Fine links (kappa < w_p) are LEGAL under the ONE-VACUUM offset
    l0_offset = Q - 1 (R' fixes 3Q - 1 whatever the coefficients; no q-lattice rule);
  * the spring: R[Q8] = R (+) R (+) R (+) R (+) H (Wedderburn). The four 1-dim components are the sign characters eps
    (chi_0, chi_i, chi_j, chi_k; they act on V+), H acts on V-. ONE OD4 spring per simple component:
        Phi -= (lam/4) [ Sum_chi (chi(U)^2 - A^2)^2 + (|h(U)|^2 - A^2)^2 ],
        chi(U) = Sum_q chi(q) U_q,   h(U) = Sum_{a in 1,i,j,k} (U_a - U_{-a}) e_a,
    every term a class function (gauge invariant). The frozen links.py spring pins only the Euclidean norm of the 8
    coefficients (a mean of the component norms), so a single eps component can leave +-A: the M1 runaway mode.
Vacuum U = A [1]: every chi = A, h = A (today's board bit for bit at W = 0). Link inertia D/2 |U|^2 as in links.py.
Linear spring stiffness: 16 lam A^2 (eps directions), 4 lam A^2 (H radial); CFL needs 16 lam A^2 <= 2 D.
"""
from __future__ import annotations

from fractions import Fraction

from ..core.tensor import Block, GearType
from .gauge import UNIT, Poly, deviation_terms, vec_dot
from .links import Q8_LABEL, Q8_ORDER, _link_names, right_perm

# characters of Q8 on Q8_ORDER = ("1", "i", "j", "k", "-1", "-i", "-j", "-k")
CHARACTERS = {"eps0": (1, 1, 1, 1, 1, 1, 1, 1),
              "eps_i": (1, 1, -1, -1, 1, 1, -1, -1),
              "eps_j": (1, -1, 1, -1, 1, -1, 1, -1),
              "eps_k": (1, -1, -1, 1, 1, -1, -1, 1)}
H_PAIRS = ((0, 4), (1, 5), (2, 6), (3, 7))          # (q, -q) index pairs: h_a = U_a - U_{-a}


def _coupling(body_signs):
    from universe24.algebra.coupling import coupling
    return coupling(tuple(body_signs))


def components(U):
    """(chi values dict, |h|^2) of one link's 8 coefficients (Python ints or Polys)."""
    chis = {n: sum(s * u for s, u in zip(sig, U)) for n, sig in CHARACTERS.items()}
    h2 = sum((U[p] - U[m]) * (U[p] - U[m]) for p, m in H_PAIRS)
    return chis, h2


def build_c2_zq8(*, Q: int, kappa: int, lam: int, body_signs=(1, -1, 1), port_weight: int | None = None,
                 ref: str = "ref", name: str = "c2", field_label: str = "audit") -> Block:
    """ZQ8 dynamic base links (8 gears per link) with one OD4 spring per simple component (module docstring).
    kappa * A = port_weight (default Q - 1, the form-C L0); A = port_weight // kappa."""
    if type(Q) is not int or Q < 3 or Q % 2 == 0:
        raise ValueError("Q must be an ODD int >= 3")
    wp = Q - 1 if port_weight is None else port_weight
    if wp not in (Q, Q - 1):
        raise ValueError("port_weight must be Q (today's L0) or Q - 1 (form-C L0)")
    if type(kappa) is not int or kappa < 1 or wp % kappa:
        raise ValueError("kappa must be a positive divisor of the port weight (kappa * A = port weight)")
    if type(lam) is not int or lam < 0:
        raise ValueError("lam must be a non-negative int")
    C = _coupling(body_signs)
    D = 6 * Q
    A = wp // kappa
    links = _link_names("ZQ8")
    rn = [f"{ref}.R{g:02d}" for g in range(48)]
    x0 = {links[k][0]: A for k in range(3)}
    phi = Poly()
    for k in range(3):
        d = 2 * k
        e = UNIT[k]
        Wk = [Poly.var(g, (0, 0, 0), x0.get(g, 0)) for g in links[k]]
        for c, qn in enumerate(Q8_ORDER):
            perm = right_perm(qn)
            for g in range(48):
                h = C.ports[d][g]
                phi = phi + Wk[c] * (Poly.var(rn[g]) * Poly.var(rn[perm[h]], e) * (kappa * C.weights[d][g]))
        for g in range(48):                       # the vacuum part kappa A b^T W_d b' IS the L0 block's own port term
            phi = phi - Poly.var(rn[g]) * Poly.var(rn[C.ports[d][g]], e) * (wp * C.weights[d][g])
        phi = phi + vec_dot(Wk, Wk) * Fraction(D, 2)
        if lam:
            chis, h2 = components(Wk)
            for chi in chis.values():
                N = chi * chi - A * A
                phi = phi - N * N * Fraction(lam, 4)
            N = h2 - A * A
            phi = phi - N * N * Fraction(lam, 4)
    terms = deviation_terms(phi, D, x0)
    gears = [GearType(g, field_label, link=k) for k in range(3) for g in links[k]]
    r0 = 3 * Q - 1
    params = {"Q": Q, "kappa": kappa, "lam": lam, "A": A, "port_weight": "Q" if wp == Q else "Q-1",
              "body_signs": tuple(body_signs), "algebra": "ZQ8", "springs": "one OD4 per simple component "
              "(eps0, eps_i, eps_j, eps_k, H)", "ref": ref, "X0": dict(x0), "r0": r0,
              "stiffness_over_D": str(Fraction(16 * lam * A * A, D)),
              "reversor": {"every gear": "Mp (b, a, R'(r)); vacuum 3Q - 1 (l0_offset = Q - 1 on L0)"}}
    doc = (f"c2 ZQ8 links, one spring per simple component, kappa = {kappa}, A = {A}, lam = {lam}, port weight "
           f"{params['port_weight']}, body signs {tuple(body_signs)}")
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: r0 for g in gears}, params=params, doc=doc,
                 Q=Q)


def q8_gauge_map_names():
    """Q8 element names in links.py's component order (for the covariance check)."""
    return Q8_ORDER, Q8_LABEL


__all__ = ["build_c2_zq8", "CHARACTERS", "H_PAIRS", "components"]
