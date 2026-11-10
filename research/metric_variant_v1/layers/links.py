"""DYNAMIC BASE LINKS (owner decision G9-c; departs from AGENTS item 5 -> lives only in this variant package).

"The node's symmetry made local" (SYSTEM_DESIGN_v5 section 12). Tensor blocks only (no state, no run).

c2 = the board's INTERNAL right-Q8 symmetry made local. The 48 reference labels are the elements of 2O; right
multiplication (R_q v)(g) = v(g q) by q in Q8 = {+-1, +-i, +-j, +-k} commutes with every +++ port (exhaustive,
M2_commutant48), so Phi_ref = Q sum_x sum_{d=+x,+y,+z} b(x)^T W_d b(x+e_d) is invariant under the GLOBAL map
b -> R_q b. Making it local puts a link variable U(x,d) on every base link, coupled as

    Phi_ref + Phi_c2 = sum_x sum_d b(x)^T W_d rho(U(x,d)) b(x+e_d),     vacuum rho(U) = Q * 1  (today's board).

Two link algebras (both built here; choose with ``algebra``):
  * "ZQ8" (8 gears per link): the integer GROUP ALGEBRA Z[Q8], rho(U) = sum_q U_q R_q (a homomorphism: R_p R_q =
    R_pq). Local Q8 acts by PERMUTATIONS (b(x) -> R_k(x) b(x), U -> [k(x)] U [k(x+e)]^-1): bit-exact local
    covariance on all 48 labels, no sign maps. Z[Q8] (x) R = R^4 (sign characters, acting on V+) + H (acting on the
    spinorial V-); the continuous SU(2) acts on the H part: exact Noether (Gauss) identity for the V- isospin.
    U = A [1] + W with kappa * A = Q.
  * "H" (4 gears per link): the integer QUATERNION acting on V- only, through the integer generators
    R_{e_a} - R_{-e_a} (= 2 T_a on V-, 0 on V+): Phi_c2 = kappa sum_a W_a b^T W_d (R_{e_a} - R_{-e_a}) b'. On V- the
    connection is U_eff = Q + 2 kappa W = 2 kappa (A + W), A = Q/(2 kappa) (a half-integer). V+ (incl. the reference
    light) stays uncoupled. THEOREM (proof in NOTES_gauge.md): no 4-component integer link can carry a bit-exact
    LOCAL Q8 covariance on the 48 labels (the signed commutant of the ports is {+-R_q}; R_{-1} != -1 on V+); the
    H form keeps: global Q8 (bit-exact), local centre Z2 (bit-exact when kappa | Q), continuous local SU(2) on V-
    as an exact Noether identity.
Spring (OD4, the only rank-4 term, minus sign): Phi -= (lam/4) (|U|^2 - A^2)^2 (ZQ8, Euclidean norm of the 8
coefficients; gauge invariant), and for H Phi -= (lam/2) (m W_0 + |W|^2)^2 with m = Q/kappa, i.e. (lam/8)(|U|^2 -
A^2)^2 * 4 in the physical link U = m/2 + W (integer coefficients).

R-M2 Q-LATTICE RULE (manager 09:23): terms targeting L0 gears have u-coefficient +-kappa. kappa = 0 mod Q keeps the
L0 remainders on the Q-lattice (exact joint mirror rhoL0 + M' fixing the joint vacuum). For ZQ8 this forces
kappa = Q, A = 1 (a COARSE link: one unit of W = one full reference coupling). A finer link (kappa < Q) is allowed
but DECLARED: then no exact mirror fixes the L0 vacuum (the plain per-gear M stays an exact reversor of the b-only
tensor but maps the vacuum (0,0,2Q) to (0,0,4Q-1)).

LINKS FROZEN: kappa = lam = 0 gives no coupling at all; the link gears sit at their vacuum and the reference board
runs exactly as today (observe.audit.frozen_equivalence).

c1 (EXPLORATORY, ``build_c1_weights``): the minimal frame-side register: every +++ port entry (g -> ports[d][g])
gets its own dynamical integer weight V_g(x,d) (48 gears per link axis), coupling b_g(x) V_g b_{ports[d][g]}(x+e_d);
vacuum V = A with kappa*A = Q is today's (curved) +++ connection bit for bit. Not adopted (see NOTES_gauge.md).
"""
from __future__ import annotations

from fractions import Fraction

# Manager ruling (after the 09:46 interim): c2 ships as an exact block, DEFAULT OFF (never part of a default composed system); c1 is
# NOT ADOPTED (exploratory). Both stay owner-level items: generic excited reference data blow up (NOTES_gauge.md).
C2_DEFAULT_ON = False
C1_ADOPTED = False

from ..core.tensor import Block, GearType
from .gauge import AXES, UNIT, Poly, deviation_terms, vec_dot

Q8_LABEL = {"1": 0, "i": 3, "j": 6, "-1": 14, "k": 17, "-k": 21, "-i": 33, "-j": 36}
Q8_ORDER = ("1", "i", "j", "k", "-1", "-i", "-j", "-k")     # Z[Q8] component order


def _ref():
    from universe24.core.coupling import coupling
    from universe24.core.group_2o import group
    return coupling((1, 1, 1)), group()


def q8_mul_names():
    """Multiplication of Q8 element names, from universe24's 2O table (read-only)."""
    _, G = _ref()
    lab = Q8_LABEL
    inv = {v: k for k, v in lab.items()}
    return {(p, q): inv[G.multiplication[lab[p]][lab[q]]] for p in Q8_ORDER for q in Q8_ORDER}


def right_perm(qname: str) -> list[int]:
    """Label map of R_q: (R_q v)(g) = v(g q), i.e. new[g] = old[mul[g][q]]."""
    _, G = _ref()
    q = Q8_LABEL[qname]
    return [G.multiplication[g][q] for g in range(48)]


def _link_names(algebra: str):
    if algebra == "ZQ8":
        comps = [c.replace("-", "m") for c in Q8_ORDER]
    elif algebra == "H":
        comps = ["1", "i", "j", "k"]
    else:
        raise ValueError("algebra must be 'ZQ8' or 'H'")
    return {k: [f"W{AXES[k]}_{c}" for c in comps] for k in range(3)}


def build_c2(*, Q: int, kappa: int, lam: int = 0, algebra: str = "ZQ8", ref: str = "ref", name: str = "c2",
             field_label: str = "audit", declare_off_lattice: bool = False) -> Block:
    """c2 dynamic base links (see the module docstring).

    Parameters (keyword-only): Q (ODD; one divisor 6Q); kappa (integer coupling of the link to the reference;
    ZQ8: kappa * A = Q with A = Q // kappa an integer; H: kappa | Q, A = Q/(2 kappa)); lam (spring >= 0); ref = the
    namespace of the reference block (gears "<ref>.R00".."R47"); kappa = lam = 0 -> links frozen.
    """
    if type(Q) is not int or Q < 1 or Q % 2 == 0:
        raise ValueError("Q must be an ODD positive int")
    if type(kappa) is not int or kappa < 0 or type(lam) is not int or lam < 0:
        raise ValueError("kappa, lam must be non-negative ints")
    if kappa % Q and not declare_off_lattice:
        raise ValueError("R-M2 / ARCH R7 (binding): terms writing into L0 need u-coefficients = 0 mod Q, i.e. kappa in "
                         "{0, Q}; pass declare_off_lattice=True only for a DECLARED non-shipped variant")
    C, G = _ref()
    D = 6 * Q
    links = _link_names(algebra)
    rn = [f"{ref}.R{g:02d}" for g in range(48)]
    x0 = {}
    if kappa:
        if Q % kappa:
            raise ValueError("kappa must divide Q (vacuum: kappa * A = Q, resp. 2 kappa A = Q)")
        m = Q // kappa
    else:
        m = 1
    if algebra == "ZQ8":
        A = m
        for k in range(3):
            x0[links[k][0]] = A
    else:
        A = Fraction(m, 2)
    phi = Poly()
    for k in range(3):
        d = 2 * k
        e = UNIT[k]
        Wk = [Poly.var(g, (0, 0, 0), x0.get(g, 0)) for g in links[k]]
        if kappa:
            if algebra == "ZQ8":
                for c, qn in enumerate(Q8_ORDER):
                    perm = right_perm(qn)
                    for g in range(48):
                        h = C.ports[d][g]
                        term = Poly.var(rn[g]) * Poly.var(rn[perm[h]], e) * (kappa * C.weights[d][g])
                        phi = phi + Wk[c] * term
                # remove the vacuum part kappa*A*b^T W_d b' (it IS the reference block's Phi_ref)
                for g in range(48):
                    phi = phi - Poly.var(rn[g]) * Poly.var(rn[C.ports[d][g]], e) * (Q * C.weights[d][g])
            else:
                for c, qn in enumerate(("1", "i", "j", "k")):
                    pp, pm = right_perm(qn), right_perm(("-" + qn) if qn != "1" else "-1")
                    for g in range(48):
                        h = C.ports[d][g]
                        bb = (Poly.var(rn[pp[h]], e) - Poly.var(rn[pm[h]], e)) * (kappa * C.weights[d][g])
                        phi = phi + Wk[c] * Poly.var(rn[g]) * bb
        phi = phi + vec_dot(Wk, Wk) * Fraction(D, 2)
        if lam:
            if algebra == "ZQ8":
                N = vec_dot(Wk, Wk) - A * A
                phi = phi - N * N * Fraction(lam, 4)
            else:
                N = Wk[0] * m + vec_dot(Wk, Wk)
                phi = phi - N * N * Fraction(lam, 2)
    terms = deviation_terms(phi, D, x0)
    gears = [GearType(g, field_label, link=k) for k in range(3) for g in links[k]]
    r0 = 3 * Q - 1
    params = {"Q": Q, "kappa": kappa, "lam": lam, "algebra": algebra, "ref": ref, "A": A if algebra == "ZQ8" else str(A),
              "m": m, "X0": dict(x0), "r0": r0,
              "q_lattice_compliant": kappa % Q == 0,
              "reversor": {"ref.*": "rhoL0 (b, a, 4Q + 2(r mod 2Q) - r): exact iff every term into L0 is = 0 mod Q",
                           "new gears": "Mp (b, a, R'(r)); fixes r0 = 3Q-1 for odd Q",
                           "also exact": "M on every gear (b-only tensor), not vacuum-fixing"}}
    doc = (f"c2 dynamic base links ({algebra}): right-Q8 of the 48 labels made local; kappa = {kappa}, lam = {lam}; "
           f"vacuum W = 0 is today's board bit for bit; "
           + ("terms targeting L0 are = 0 mod Q (R-M2 rule met)" if kappa % Q == 0 else
              "DECLARED: terms targeting L0 are NOT = 0 mod Q, so no exact mirror fixes the L0 vacuum"))
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: r0 for g in gears}, params=params, doc=doc,
                 Q=Q)


def build_c1_weights(*, Q: int, kappa: int, lam: int = 0, ref: str = "ref", name: str = "c1",
                     field_label: str = "audit") -> Block:
    """EXPLORATORY c1: one dynamical integer weight per +++ port entry (48 gears per link axis).
    Phi = sum_x sum_d sum_g V_g(x,d) w_d(g) b_g(x) b_{ports[d][g]}(x+e_d) with V = A + V~, kappa*A = Q... written as
    kappa * V_g * (...) with vacuum kappa*A = Q, minus Phi_ref (already in the reference block); link inertia D/2 V^2;
    spring -(lam/4) sum_g (V_g^2 - A^2)^2 per entry. Vacuum V~ = 0 = today's +++ connection (curved: order-3
    plaquette holonomy of the port permutations)."""
    if type(Q) is not int or Q % 2 == 0:
        raise ValueError("Q must be ODD")
    C, _ = _ref()
    D = 6 * Q
    if kappa and Q % kappa:
        raise ValueError("kappa must divide Q")
    if kappa % Q:
        raise ValueError("R-M2 / ARCH R7 (binding): kappa must be 0 or Q (u-coefficients into L0 = 0 mod Q)")
    A = Q // kappa if kappa else 1
    rn = [f"{ref}.R{g:02d}" for g in range(48)]
    names = {k: [f"V{AXES[k]}_{g:02d}" for g in range(48)] for k in range(3)}
    x0 = {names[k][g]: A for k in range(3) for g in range(48)}
    phi = Poly()
    for k in range(3):
        d, e = 2 * k, UNIT[k]
        for g in range(48):
            V = Poly.var(names[k][g], (0, 0, 0), A)
            bb = Poly.var(rn[g]) * Poly.var(rn[C.ports[d][g]], e) * C.weights[d][g]
            if kappa:
                phi = phi + V * bb * kappa - bb * Q
            phi = phi + V * V * Fraction(D, 2)
            if lam:
                N = V * V - A * A
                phi = phi - N * N * Fraction(lam, 4)
    terms = deviation_terms(phi, D, x0)
    gears = [GearType(g, field_label, link=k) for k in range(3) for g in names[k]]
    r0 = 3 * Q - 1
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: r0 for g in gears},
                 params={"Q": Q, "kappa": kappa, "lam": lam, "A": A, "X0": dict(x0), "r0": r0, "ref": ref},
                 doc="EXPLORATORY c1 port-weight register (48 gears per link axis); not adopted", Q=Q)


__all__ = ["build_c2", "build_c1_weights", "right_perm", "q8_mul_names", "Q8_LABEL", "Q8_ORDER"]
