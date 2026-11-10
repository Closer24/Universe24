"""EM layer (stage 1, builder B1-EM): design E1 of Study 4 (AGREE_M P-iv, P-vii(a); AGREE_P rows 2-23).

TENSOR BLOCKS ONLY. Exact integers, ONE divisor D = 6Q, deviation form (vacuum 0, every term carries a layer factor).

Gears (per node; labels: A and Phi are POTENTIAL gears, readout "audit" by OD1)
  A_x, A_y, A_z : Lorenz-gauge vector potential, LINK gears (Yee axis k: the link (x, x + e_k), stored at x)
  Phi           : the A^0 Lorenz ACCUMULATOR, node gear. Phi = phi / c^2 = 3 phi (c^2 = 1/3): physical phi = Phi / 3.

Inputs (u; K = 2u)
  A_d(x) : (Q - 1) * sum_{6 faces f} A_d.b(x + f) + 6 * A_d.b(x)                 ONE headroom stencil, the SAME Q as
           + sigma * b_{x+e_d}^T J' (hs P_d - ws W0) b_x                          every field gear: cone c_Q =
                                                                                  sqrt((Q - 1)/(3Q)) -> 1/sqrt3
           (hs, ws) = (hop, wilson) / g, g = gcd(hop, wilson): the source is the matter's EXACT free hopping current
           j_d = 2 b_{x+e}^T J' H_d b_x = 2 g * s_d (H_d = hop P_d - wilson W0), b-only, single time, A-free.
  Phi(x) : 3Q * [ 2 Phi.b - div A.b + div A.a ],  div F(x) = sum_d [F_d(x) - F_d(x - e_d)]
           K_Phi = 6Q [...] = 0 mod D: ROUNDING-FREE (remainder constant), so
           C(x) := Phi(t+1) - Phi(t) + div A(t)  is EXACTLY constant (= Phi.b - Phi.a + div A.a of any state): Lorenz.
  matter : + g_phi * phi_c(x) * V b(x)                                             (V = J J', charge-odd, on-site)
           + g_A * sum_d [A_d.b(x) + A_d.b(x - e_d)] * P_d J' b(x)                 (on-site alpha.A, no diamagnetic term)
           phi_c = Phi(t) + Phi(t+1) = 3 Phi.b - Phi.a - div A.b + div A.a          (TIME-CENTRED potential: the matter
           reads Phi's and A's a; a-read graph A -> Phi -> matter is acyclic: staged inverse A, Phi, matter.)

Gauge-covariant ratio (Study 4 PR-1): g_A / g_phi = hop / Q (the same q for phi and A; S4: hn/dd = 1/4).
Normalisation (documented, P-c): a static Phi shifts the matter u-operator by +-2 g_phi Phi (V = -s s' in the (J, J')
sector (i s, i s')), i.e. dE = 2 g_phi Phi / (D cos E) per unit Phi, with sin E = |beta|/D; in physical units
phi = Phi / 3, so q_phi(E) = 6 g_phi / (D cos E) per unit phi. A uniform A_d shifts k_d by g_A A_d / hop (small k).
With the headroom stencil the Lorenz relation is exact and the wave speed is c_Q; strictly phi = Phi (Q-1)/(3Q)
(1 - 1/Q from 1/3; negligible for the large Q of the demos).

EXACT IDENTITIES (event view; checked in tests/test_em.py, observe/em.py implements them)
  continuity : rho(t+1) - rho(t) + div j(t) = R(t),   rho = D a^T J' b,  R = b^T J' (r(t) - r(t+1))  (matter remainders)
  Lorenz     : C(t+1) = C(t) at every node (rounding-free accumulator)
  dressed Gauss: Y_g(t) := g D [Phi(t+1) - 2 Phi(t) + Phi(t-1)] - 2 g (Q-1) Lap Phi(t) - sigma rho(t) - g div r_A(t)
               obeys Y_g(t+1) - Y_g(t) = -sigma R(t) EXACTLY (derivation in NOTES_em.md). Static: -Lap Phi =
               sigma rho / (2 g (Q-1)).
  charge Noether: sum_x rho(t+1) - rho(t) = sum_x R(t).

RECIPROCITY (manager rule v5 §1b) — DESIGNATED, with the proof that it is unavoidable in E1 (NOTES_em.md §R):
  every b-only cross entry of E1 is ONE-WAY on the lattice. The exactly conserved current of matter whose A-coupling
  is on-site is the A-free link hopping current; its lattice transpose is the linear Peierls action, whose own
  conserved current gains a rank-4 diamagnetic term (Study 4 D4: 57,718/58,000 failures), and so on at every order
  (the expansion of e^{i theta} never closes at finite rank). The on-site alpha.A transpose (the on-site alpha
  current) is not conserved. Phi is a slaved accumulator: a matter source for Phi would break C == 0. Reciprocity
  (action = reaction) therefore holds in the CONTINUUM: b_{x+e}^T J' P_d b_x -> b^T P_d J' b, and Newton III needs
  only a species-independent source/action ratio (S4-M CF-1), which E1 has (C is an exact symmetry).
  Controls offered here: vector="peierls" (the literal transpose of the source; reciprocal; exactness lost),
  blind=c (a charge-blind action with no source; S4-P R17 Newton-III breaker).
  STATUS (manager ruling 09:5x): E1 ships DESIGNATED, accepted PROVISIONALLY as a documented variant. Its Newton III
  is EXACT only in C-symmetric preparations (there a2/a1 = -1 bit for bit, by the exact C o P symmetry of the
  prepared state, the vacuum 3Q-1 being R'-fixed) and APPROXIMATE otherwise: charge-weighted momentum ratio -0.984
  for unequal packets (demos/em EM-D1b, post-hoc), S4-P measured <= 2.4 %. The reciprocal EM candidate is the
  compact-U(1) route, layers/em_compact.py (one potential, 0 designations).
"""
from __future__ import annotations

from math import gcd

from ..core.lattice import DIRECTIONS
from ..core.tensor import Block, GearType
from .matter import _block, _check_Q, _face, algebra, matter_names

A_NAMES = ("A_x", "A_y", "A_z")
PHI = "Phi"
ZERO = (0, 0, 0)

# Reversor declared as DATA (binding condition 3): the exact STAGGERED reversor of E1 (s4 A7/P-iv), M' convention.
REVERSOR_EM = {"matter": "K o M' (layers.matter.REVERSOR_MATTER)", "A_d": "M' = (b, a, R'(r))",
               "Phi": "(a, b, r) -> (-Phi_next, -Phi.b, r), Phi_next = 2 Phi.b - Phi.a - div A.b + div A.a",
               "central": "X^2 = Jp on the matter gears",
               "vacuum": "X(vac) = vac for ODD Q, r0 = 3Q - 1 (even Q: no mirror-fixed remainder)",
               "alternative": "the same with M = (b, a, D-1-r) (S4-P convention) is exact too but moves 3Q-1 -> 3Q",
               "implementation": "prepare.em.x_reversor / prepare.em.x_reversor_core (core/reversors building blocks)"}

WHY_PHI_READ = ("E1 centred potential read (s4 A7/P-iv): the matter reads the Lorenz ACCUMULATOR Phi, which has no "
                "matter source by design (the charge reaches Phi only through the exact current -> A -> D_t Phi = "
                "-div A); a lattice transpose (Phi sourced by the on-site density) would break the exact Lorenz "
                "C == 0 (s4 A6). Unavoidable in E1; reciprocal in the continuum (Newton III via CF-1).")
WHY_A_READ = ("E1 on-site alpha.A (and the div A part of the centred potential): its lattice transpose (an on-site "
              "current) is NOT the exactly conserved current; the conserved current of on-site-coupled matter is the "
              "A-free link hopping current (s4 A4). The literal transpose of that current (linear Peierls) adds a "
              "rank-4 diamagnetic current and loses exact continuity/Gauss (s4 D4: 57,718/58,000); no finite rank "
              "closes. Unavoidable in E1; reciprocal in the continuum.")
WHY_SOURCE = ("E1 source = the EXACT free hopping current of the matter (s4 A4): exact continuity, Lorenz and dressed "
              "Gauss. Its literal partner (Peierls action) breaks them (D4). It is the continuum transpose of the "
              "on-site alpha.A action; Newton III needs only a species-independent source/action ratio (CF-1).")
WHY_ACC = ("Lorenz ACCUMULATOR (first-order-in-time relation D_t Phi = -div A, rounding-free, s4 A6): Phi is slaved "
           "to A; a reciprocal partner would add grad Phi to the A wave equation and leave Lorenz gauge.")
WHY_BLIND = "CONTROL ONLY (S4-P R17 / S4-M E8): charge-blind action with no matching source; breaks Newton III"
WHY_DRIVER = ("MECHANISM: prescribed current (driver gear = initial data of a sourceless marginal/linear gear) feeding "
              "the A source; a prescribed current has no reaction by construction")


def _hs_ws(hop: int, wilson: int) -> tuple[int, int, int]:
    g = gcd(hop, wilson)
    if g == 0:
        raise ValueError("matter with hop = wilson = 0 has no current")
    return hop // g, wilson // g, g


def build_em(*, Q: int, matter: Block | None, g_phi: int, g_A: int, sigma: int, stencil: str = "headroom",
             vector: str = "onsite", blind: int = 0, name: str = "em", label: str = "audit",
             r0: int | None = None) -> Block:
    """E1 electromagnetism block (A_x, A_y, A_z link gears + Phi accumulator + the matter couplings).

    Parameters (keyword-only; stored in Block.params)
    ----------
    Q       : the ONE divisor scale (D = 6Q); the field stencil uses this same Q.
    matter  : the matter Block (species "pair") the field couples to; None = pure field (no coupling, no source).
    g_phi   : on-site electric coupling (phi_c V b); g_A : on-site alpha.A coupling. Gauge-covariant: g_A/g_phi = hop/Q.
    sigma   : source coefficient (A_d input += sigma * s_d, s_d = j_d / (2g)); sigma = 0 makes the matter a TEST
              charge (no source; prepared static fields stay static).
    stencil : "headroom" (u = (Q-1) sum6 b + 6b; the design) or "edge" (u = Q sum6 b; control, c = 1/sqrt3).
    vector  : "onsite" (E1) or "peierls" (CONTROL: the literal transpose of the source, sigma*A_d(x) M_d^T b(x+e) +
              sigma*A_d(x-e) M_d b(x-e); reciprocal, but its exact current is not the source: Gauss fails, s4 D4).
    blind   : CONTROL integer c_b: u_matter += c_b Phi.b b (charge-blind action, no source; S4-P R17).
    r0      : vacuum remainder of A and Phi (default 3Q - 1).
    """
    _check_Q(Q)
    for nm, v in (("g_phi", g_phi), ("g_A", g_A), ("sigma", sigma), ("blind", blind)):
        if type(v) is not int:
            raise TypeError(f"{nm} must be a Python int")
    if stencil not in ("headroom", "edge"):
        raise ValueError("stencil must be 'headroom' or 'edge'")
    if vector not in ("onsite", "peierls"):
        raise ValueError("vector must be 'onsite' or 'peierls'")
    D = 6 * Q
    r0 = 3 * Q - 1 if r0 is None else r0
    gears = [GearType(A_NAMES[k], label, k) for k in range(3)] + [GearType(PHI, label)]
    terms = []
    # ---- field stencil (reciprocal: symmetric)
    w_nb, w_on = (Q - 1, 6) if stencil == "headroom" else (Q, 0)
    for k in range(3):
        for f in DIRECTIONS:
            terms.append((A_NAMES[k], w_nb, ((A_NAMES[k], f, "b"),)))
        if w_on:
            terms.append((A_NAMES[k], w_on, ((A_NAMES[k], ZERO, "b"),)))
    # ---- Lorenz accumulator: u_Phi = 3Q [2 Phi.b - divA.b + divA.a]
    terms.append((PHI, 6 * Q, ((PHI, ZERO, "b"),)))
    for k in range(3):
        back = _face(k, -1)
        terms.append((PHI, -3 * Q, ((A_NAMES[k], ZERO, "b"),), {"designated_one_way": WHY_ACC}))
        terms.append((PHI, 3 * Q, ((A_NAMES[k], back, "b"),), {"designated_one_way": WHY_ACC}))
        terms.append((PHI, 3 * Q, ((A_NAMES[k], ZERO, "a"),)))
        terms.append((PHI, -3 * Q, ((A_NAMES[k], back, "a"),)))
    params = {"Q": Q, "g_phi": g_phi, "g_A": g_A, "sigma": sigma, "stencil": stencil, "vector": vector,
              "blind": blind, "label": label, "r0": r0, "matter": None if matter is None else matter.name,
              "reversor": REVERSOR_EM}
    if matter is not None:
        mp = matter.params
        if mp.get("species") != "pair":
            raise ValueError("EM couples to the charged species: the 16-channel pair (species='pair')")
        if mp["Q"] != Q:
            raise ValueError("ONE divisor: the matter block has another Q")
        alg = algebra("pair")
        n = alg["n"]
        mn = [matter.qualify(x) for x in matter_names("pair")]
        hs, ws, g = _hs_ws(mp["hop"], mp["wilson"])
        params.update({"hop": mp["hop"], "wilson": mp["wilson"], "hs": hs, "ws": ws, "g": g})
        V, PJp, Jp, P, W0 = alg["V"], alg["PJp"], alg["Jp"], alg["P"], alg["W0"]
        Ms = [Jp @ (hs * P[d] - ws * W0) for d in range(3)]           # source matrices s_d = b(x+e)^T M_d b(x)
        # ---- source of A_d: sigma * b_{x+e_d}^T M_d b_x  (b-only, link)
        if sigma:
            for d in range(3):
                fwd = _face(d, +1)
                for i in range(n):
                    for j in range(n):
                        if Ms[d][i, j]:
                            terms.append((A_NAMES[d], int(sigma * Ms[d][i, j]),
                                          ((mn[i], fwd, "b"), (mn[j], ZERO, "b")), {"designated_one_way": WHY_SOURCE}))
        # ---- matter <- centred potential: g_phi * (3Phi.b - Phi.a - divA.b + divA.a) * V b
        for i in range(n):
            for j in range(n):
                if not V[i, j] or not g_phi:
                    continue
                c = int(g_phi * V[i, j])
                terms.append((mn[i], 3 * c, ((PHI, ZERO, "b"), (mn[j], ZERO, "b")), {"designated_one_way": WHY_PHI_READ}))
                terms.append((mn[i], -c, ((PHI, ZERO, "a"), (mn[j], ZERO, "b"))))
                for k in range(3):
                    back = _face(k, -1)
                    terms.append((mn[i], -c, ((A_NAMES[k], ZERO, "b"), (mn[j], ZERO, "b")),
                                  {"designated_one_way": WHY_A_READ}))
                    terms.append((mn[i], c, ((A_NAMES[k], back, "b"), (mn[j], ZERO, "b")),
                                  {"designated_one_way": WHY_A_READ}))
                    terms.append((mn[i], c, ((A_NAMES[k], ZERO, "a"), (mn[j], ZERO, "b"))))
                    terms.append((mn[i], -c, ((A_NAMES[k], back, "a"), (mn[j], ZERO, "b"))))
        # ---- vector potential
        if vector == "onsite" and g_A:
            for d in range(3):
                back = _face(d, -1)
                for i in range(n):
                    for j in range(n):
                        if PJp[d][i, j]:
                            c = int(g_A * PJp[d][i, j])
                            terms.append((mn[i], c, ((A_NAMES[d], ZERO, "b"), (mn[j], ZERO, "b")),
                                          {"designated_one_way": WHY_A_READ}))
                            terms.append((mn[i], c, ((A_NAMES[d], back, "b"), (mn[j], ZERO, "b")),
                                          {"designated_one_way": WHY_A_READ}))
        elif vector == "peierls" and sigma:
            # CONTROL: Psi_int = sigma * sum A_d(x) b(x+e)^T M_d b(x): u_m(x) += sigma A_d(x) M_d^T b(x+e)
            #          + sigma A_d(x-e) M_d b(x-e)  (literal transpose of the source; NOT designated)
            for d in range(3):
                fwd, back = _face(d, +1), _face(d, -1)
                for i in range(n):
                    for j in range(n):
                        if Ms[d][j, i]:
                            terms.append((mn[i], int(sigma * Ms[d][j, i]), ((A_NAMES[d], ZERO, "b"), (mn[j], fwd, "b"))))
                        if Ms[d][i, j]:
                            terms.append((mn[i], int(sigma * Ms[d][i, j]), ((A_NAMES[d], back, "b"), (mn[j], back, "b"))))
            # the Peierls control is reciprocal: remove the source designations
            terms = [t[:3] if (len(t) == 4 and t[0] in A_NAMES and t[3]["designated_one_way"] == WHY_SOURCE) else t
                     for t in terms]
        if blind:
            for i in range(n):
                terms.append((mn[i], blind, ((PHI, ZERO, "b"), (mn[i], ZERO, "b")), {"designated_one_way": WHY_BLIND}))
    vac = {nm: r0 for nm in A_NAMES + (PHI,)}
    return _block(gears, terms, name, vac, params,
                  "E1: Lorenz-gauge A_i link gears (headroom stencil) + rounding-free Lorenz accumulator Phi + "
                  "time-centred potential read + on-site alpha.A; source = exact free hopping current", Q)


def build_current_driver(*, Q: int, em: Block, axis: int, kappa: int, coupling: int, name: str = "drive",
                         r0: int | None = None) -> Block:
    """MECHANISM (labelled; never evidence): a prescribed current on the links of one Yee axis.

    One node gear S with u_S = kappa * S.b: kappa = D (= 6Q) makes it a marginal, ROUNDING-FREE, exactly static gear
    (prepare S.a = S.b: a steady current); |kappa| < D makes it a linear clock, cos W = kappa / D (an oscillating
    dipole). The field reads it ONE-WAY: u_{A_axis}(x) += coupling * S.b(x), i.e. a current on the link
    (x, x + e_axis) wherever S(x) != 0 (initial data). The implied charge is conserved by construction (a current on a
    link moves charge between its ends; the accumulator Phi needs no charge source).
    """
    _check_Q(Q)
    if axis not in (0, 1, 2):
        raise ValueError("axis must be 0, 1 or 2")
    D = 6 * Q
    if type(kappa) is not int or not -D <= kappa <= D or type(coupling) is not int:
        raise ValueError("kappa must be an int in [-D, D], coupling an int")
    r0 = 3 * Q - 1 if r0 is None else r0
    target = em.qualify(A_NAMES[axis])
    terms = [("S", kappa, (("S", ZERO, "b"),)),
             (target, coupling, (("S", ZERO, "b"),), {"designated_one_way": WHY_DRIVER})]
    return _block([GearType("S", "audit")], terms, name, {"S": r0},
                  {"Q": Q, "axis": axis, "kappa": kappa, "coupling": coupling, "em": em.name, "r0": r0,
                   "MECHANISM": True},
                  "MECHANISM: prescribed current driver gear", Q)
