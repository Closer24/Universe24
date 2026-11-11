"""CHIRAL weak SU(2) block (Study 7, HAND-M1 = CHIRAL-BUILDER): a research candidate enabled by the current default_system composition.

TENSOR BLOCKS ONLY (layers/ contract). NEW file; no existing package file is modified. Source: s7/AGREE_H.md (twin-signed
HAND-M1 11:24:18 / HAND-M2 11:25:40 UTC), rows E1-E7 and joint recommendation 1-2; Study-7 prototype
s7/HAND-M1_work/h3_chiral_board.py (exact checks there: vacuum = Wilson-Dirac, rewind, Noether 0/648, R* PASS).

Physics in one paragraph (labels: see NOTES_chiral.md)
  A weak SU(2) acts on a SPECIES DOUBLET of two Dirac pairs (the default "matter" + a partner "matter2"), only on the
  components selected by the projector P_W = (1 - G5 V)/2 (chirality x charge circulation, V = J J'): P-odd, C-odd,
  CP-even, CPT-even (AGREE_H E1). Masses and the doubler-lifting Wilson term become the vacuum imprint of a Higgs
  quaternion Phi = v + phi (Yukawa and Wilson-Yukawa); at phi = W = 0 the matter input is build_matter's free Wilson-Dirac
  pair BIT FOR BIT (hop = kappa A, wilson = w v, mass = 2 y v), so the approved matter block is untouched.

Algebra (package basis = layers/matter.py; integer):
  pair:    G5 = 1_2 (x) 1_4 (x) s_z (= -P_x P_y P_z),  V = J J',  Pi_W = 1 - G5 V (= 2 P_W), Pi_S = 1 + G5 V
  doublet: 32 = (matter, matter2) (x) 16;  t1 = eps (x) 1_16, t2 = s_x (x) J', t3 = s_z (x) J'  (integer quaternion units,
           commuting with P_d, W0, J, J', G5, V);  rho(q) = q0 + q1 t1 + q2 t2 + q3 t3.
Potential of THIS block (the vacuum parts A(...) and v(...) are build_matter's own entries and are NOT repeated here):
  Psi = sum_x sum_d (kappa/2) b(x+e_d)^T P_d rho(conj W(x,d)) Pi_W b(x)                 transport through the weak link
      + sum_x (ytot/2) b(x)^T [rho(phi) Pi_W W0 + W0 Pi_W rho(phi)^T] b(x)               Yukawa (on-site incl. Wilson)
      - sum_x sum_d (w/2) b(x+e)^T [rho(phi(x+e)) Pi_W W0 + W0 Pi_W rho(phi(x))^T] b(x)   Wilson-Yukawa (link)
      + sum_x (D/2)|phi|^2 - (lam_H/4) (|v + phi|^2 - v^2)^2                               Higgs inertia + OD4 spring
  with ytot = y + 3w. Every term is rank <= 3 except the ONE OD4 spring (minus sign; B1-GAUGE convention). b-only,
  reciprocal (one potential, field signs +1), B3-local (node or one face link). The weak links (W = U - A, 4 gears per
  link) and their dynamics (link inertia, 2-path plaquette gears, OD4 spring) are B1-GAUGE's su2 block
  (layers/gauge.py, imported read-only) WITHOUT its own quaternion matter (as layers/em_compact.py does for u1).
Gauge symmetry (exact polynomial identity): b(x) -> [rho(g) P_W + (1 - P_W)] b(x), phi -> g (v + phi) - v,
  U(x,d) -> g(x) U g(x+e)^-1 (and B1-GAUGE's 2-path rule). Local SU(2) = exact Noether/Gauss (observe/chiral.py);
  Pi_W is not diagonal in the package basis, so local Q8 is NOT a bit-exact signed-permutation covariance here (that needs
  the charge-diagonal integral form, AGREE_H E3: owner decision 2).

Standalone-block limitations (NOTES_chiral.md; the complete default adds ehop and replaces the bare-mass lapse):
  * no Higgs kinetic term: the W gets no Higgs-mechanism mass in this candidate (short range OPEN);
  * the doublet partner matter2 is EM-neutral; E1 couples only "matter", so composed with E1 the local t1, t2 Gauss laws
    are broken (charged W; hypercharge structure = integrator/owner item); t3 survives E1;
  * the matter lapse dresses the BARE mass entry m W0 (matter_lapse_c / split): that breaks the local chiral SU(2) at
    O(U) in the composed system (a covariant dressing of the Yukawa would be a rank-4 non-spring term): graviweak = Study 9;
  * the heavy Wilson-Yukawa doublers (4 w v n_pi) couple with MIRROR chirality at odd corners and the time-doubler sector
    J- is a mirror world (AGREE_H E7, B3-B5): exact law, vector-like spectrum.
This block does not read any lapse; it composes identically with matter lapse "C" (default) or "split".
"""
from __future__ import annotations

from fractions import Fraction

import numpy as np

from ..core.tensor import Block, GearType
from .gauge import Poly, build_gauge, default_regime, deviation_terms
from .matter import algebra, build_matter, matter_names

CHIRAL_DEFAULT_ON = False                  # DECLARED CANDIDATE: OWNER decision 5 is CONDITIONAL (manager 11:58)
Q_DEFAULT = (1 << 33) + 1
HOP, WILSON, MASS = 1 << 31, 1 << 30, 4915 << 22      # the v2 default matter (layers/system.py)
A_LINK = 1 << 16                           # weak-link vacuum norm (B1-GAUGE default_regime at Q = 2^33 + 1)
V_HIGGS = 1 << 16                          # Higgs vev (integer); w = WILSON / v, y = MASS / (2 v)
LAM_HIGGS = 4
AXES = ("x", "y", "z")
ZERO = (0, 0, 0)
UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
HIGGS = ("H_1", "H_i", "H_j", "H_k")

REVERSOR_CHIRAL = {
    "R* (CPT; kept)": "inversion o [matter: W0 J' K per pair (neg_r = Mp)] o [links/2-paths: conjugate (+ re-base, 2-path "
                      "(k1,k2) -> (k2,k1))] o [Higgs: identity] o Mp on every gear; involution",
    "T_phys = C K o Mp": "matter C K per pair (Kramers: X^2 = -1 on matter), links/Higgs (w0, w1, -w2, -w3)",
    "board 'T' = K o M": "= C.T physically; NOT a reversor of this block (expected FAIL)",
    "CP forward": "inversion o [matter C W0 per pair] o [links (w0, -w1, w2, w3) + re-base] o [Higgs (p0, p1, -p2, -p3)]",
    "P, C forward": "BROKEN by design (P-odd, C-odd)"}


# ======================================================================================== algebra
def chiral_algebra() -> dict:
    """Integer matrices (numpy int64) of the doublet: P (32x32, x3), W0, J, Jp, K, C, G5, V, PiW, PiS, t (x3)."""
    alg = algebra("pair")
    I2 = np.eye(2, dtype=np.int64)
    SZ = np.diag([1, -1]).astype(np.int64)
    SX = np.array([[0, 1], [1, 0]], np.int64)
    EPS = np.array([[0, 1], [-1, 0]], np.int64)
    G5_16 = np.kron(I2, np.kron(np.eye(4, dtype=np.int64), SZ))
    V16 = alg["V"]
    E16 = np.eye(16, dtype=np.int64)
    lift = lambda M: np.kron(I2, M)
    out = {"P": [lift(p) for p in alg["P"]], "W0": lift(alg["W0"]), "J": lift(alg["J"]), "Jp": lift(alg["Jp"]),
           "K": lift(alg["K"]), "C": lift(alg["C"]), "G5": lift(G5_16), "V": lift(V16),
           "PiW": lift(E16 - G5_16 @ V16), "PiS": lift(E16 + G5_16 @ V16),
           "t": [np.kron(EPS, E16), np.kron(SX, alg["Jp"]), np.kron(SZ, alg["Jp"])],
           "G5_16": G5_16, "PiW16": E16 - G5_16 @ V16}
    return out


def check_chiral_algebra() -> dict:
    """Exact integer checks (AGREE_H A1, E1)."""
    A = chiral_algebra()
    E = np.eye(32, dtype=np.int64)
    t = A["t"]
    comm = lambda X, Y: not (X @ Y - Y @ X).any()
    acomm = lambda X, Y: not (X @ Y + Y @ X).any()
    ok = {}
    ok["G5 = -P_x P_y P_z"] = bool(np.array_equal(A["G5"], -(A["P"][0] @ A["P"][1] @ A["P"][2])))
    ok["t_a quaternion units (t1 t2 = t3, t_a^2 = -1)"] = bool(
        np.array_equal(t[0] @ t[1], t[2]) and all(np.array_equal(x @ x, -E) for x in t))
    ok["t_a antisymmetric"] = all(np.array_equal(x.T, -x) for x in t)
    ok["t_a commute with P_d, W0, J, Jp, G5, V"] = all(comm(x, Y) for x in t
                                                       for Y in A["P"] + [A["W0"], A["J"], A["Jp"], A["G5"], A["V"]])
    ok["PiW^2 = 2 PiW, symmetric"] = bool(np.array_equal(A["PiW"] @ A["PiW"], 2 * A["PiW"])
                                         and np.array_equal(A["PiW"].T, A["PiW"]))
    ok["W0 PiW = PiS W0 (mass/Wilson flip the weak half)"] = bool(np.array_equal(A["W0"] @ A["PiW"],
                                                                                A["PiS"] @ A["W0"]))
    ok["PiW commutes with P_d, J, Jp"] = all(comm(A["PiW"], Y) for Y in A["P"] + [A["J"], A["Jp"]])
    ok["G5 anticommutes only with W0 (checked: W0)"] = bool(acomm(A["G5"], A["W0"]))
    return {k: bool(v) for k, v in ok.items()}


def _rho(t, q):
    E = np.eye(32, dtype=np.int64)
    return q[0] * E + q[1] * t[0] + q[2] * t[1] + q[3] * t[2]


# ======================================================================================== builders
def chiral_params(Q: int = Q_DEFAULT, *, hop: int = HOP, wilson: int = WILSON, mass: int = MASS, A: int = A_LINK,
                  v: int = V_HIGGS, lam_H: int = LAM_HIGGS) -> dict:
    """Integer parameters with the vacuum identities hop = kappa A, wilson = w v, mass = 2 y v (raise otherwise)."""
    for nm, x in (("Q", Q), ("hop", hop), ("wilson", wilson), ("mass", mass), ("A", A), ("v", v), ("lam_H", lam_H)):
        if type(x) is not int:
            raise TypeError(f"{nm} must be a Python int")
    if Q < 3 or Q % 2 == 0:
        raise ValueError("ONE ODD Q (vacuum 3Q - 1 is R'-fixed only for odd Q)")
    if hop % A or wilson % v or mass % (2 * v):
        raise ValueError("need hop = kappa A, wilson = w v, mass = 2 y v with integers kappa, w, y")
    kappa, w, y = hop // A, wilson // v, mass // (2 * v)
    if kappa % 2 or w % 2:
        raise ValueError("kappa and w must be even (Pi_W = 2 P_W carries a factor 1/2)")
    return {"Q": Q, "D": 6 * Q, "hop": hop, "wilson": wilson, "mass": mass, "A": A, "kappa": kappa, "v": v, "w": w,
            "y": y, "ytot": y + 3 * w, "lam_H": lam_H}


def build_partner(Q: int = Q_DEFAULT, *, hop: int = HOP, wilson: int = WILSON, mass: int = MASS,
                  name: str = "matter2") -> Block:
    """The doublet partner: a second free Dirac pair with the SAME parameters (build_matter, read-only)."""
    return build_matter(Q=Q, hop=hop, mass=mass, wilson=wilson, species="pair", name=name)


def build_weak_links(Q: int = Q_DEFAULT, *, A: int = A_LINK, name: str = "wsu2", use_P: bool = True,
                     lam: int = 4) -> Block:
    """B1-GAUGE's su2 link block at its default family (2-path gears, OD4 spring) WITHOUT its psi gears (kappa = mass =
    0 decouples them; they are then removed, as layers/em_compact.build_u1_links does for u1)."""
    try:
        reg = default_regime(Q)
    except ValueError:
        reg = None
    if reg is not None and reg["A"] == A:
        kP, cP, beta = reg["kappa_P"], reg["c_P"], reg["beta"]
    else:
        kP, cP, beta = (256, 0, 6 * Q - 2 * A * A) if use_P else (0, 0, 0)
    blk = build_gauge(group="su2", Q=Q, A=A, kappa=0, mass=0, lam=lam, use_P=use_P, kappa_P=kP if use_P else 0,
                      c_P=cP if use_P else 0, beta=beta if use_P else 0, name=name)
    keep = tuple(g for g in blk.gears if not g.name.startswith("psi_"))
    terms = tuple(t for t in blk.terms if not str(t[0]).startswith("psi_")
                  and not any(str(f[0]).startswith("psi_") for f in t[2]))
    params = dict(blk.params, source="layers.gauge.build_gauge(group='su2', kappa=0, mass=0) minus its psi gears",
                  role="weak SU(2) links of the chiral candidate")
    return Block(keep, terms, name=name, vacuum={g.name: blk.vacuum[g.name] for g in keep}, params=params,
                 doc=blk.doc + " [psi gears removed by CHIRAL-BUILDER]", Q=Q)


def build_chiral_coupling(*, Q: int = Q_DEFAULT, matter: Block, partner: Block, links: Block, name: str = "chiral",
                          hop: int = HOP, wilson: int = WILSON, mass: int = MASS, v: int = V_HIGGS,
                          lam_H: int = LAM_HIGGS, label: str = "audit") -> Block:
    """The chiral coupling block (Higgs gears + all matter-W and matter-phi couplings; see the module docstring)."""
    mp, pp, lp = matter.params, partner.params, links.params
    for p_ in (mp, pp):
        if p_.get("species") != "pair":
            raise ValueError("the doublet is made of two 16-channel pairs")
        if (p_["hop"], p_["wilson"], p_["mass"]) != (hop, wilson, mass):
            raise ValueError("matter and partner must carry the block's (hop, wilson, mass): vacuum identity")
        if p_["Q"] != Q:
            raise ValueError("ONE divisor")
    if lp["Q"] != Q or lp.get("group") != "su2":
        raise ValueError("links must be the su2 link block at the same Q")
    prm = chiral_params(Q, hop=hop, wilson=wilson, mass=mass, A=lp["A"], v=v, lam_H=lam_H)
    D, kappa, w, ytot = prm["D"], prm["kappa"], prm["w"], prm["ytot"]
    A = chiral_algebra()
    P, W0, PiW, t = A["P"], A["W0"], A["PiW"], A["t"]
    mnames = [matter.qualify(x) for x in matter_names("pair")] + [partner.qualify(x) for x in matter_names("pair")]
    lnames = {k: [links.qualify(f"U{AXES[k]}_{c}") for c in ("1", "i", "j", "k")] for k in range(3)}
    hq = [f"{name}.{h}" for h in HIGGS]          # qualified Higgs names (this block's namespace)
    x0 = {hq[0]: v}

    def b(off):
        return [Poly.var(g, off) for g in mnames]

    def bil(left, M, right):                      # left^T M right, M integer 32x32 (sparse)
        out = Poly()
        rows, cols = np.nonzero(M)
        for i, j in zip(rows, cols):
            out = out + left[i] * right[j] * int(M[i, j])
        return out

    rho_c = [np.eye(32, dtype=np.int64)] + list(t)
    conj = (1, -1, -1, -1)
    phi = Poly()
    b0 = b(ZERO)
    # transport through the weak link (W part only): (kappa/2) b(x+e)^T P_d rho(conj W) PiW b(x)
    for k in range(3):
        be = b(UNIT[k])
        for c in range(4):
            M = P[k] @ rho_c[c] @ PiW
            phi = phi + Poly.var(lnames[k][c]) * bil(be, M, b0) * Fraction(kappa * conj[c], 2)
    # Higgs (physical Phi = v + phi): Yukawa phi-part, on-site
    Hp = lambda off: [Poly.var(h, off) for h in hq]          # deviation phi (no shift) for the couplings
    H0 = Hp(ZERO)
    for c in range(4):
        M = rho_c[c] @ PiW @ W0
        phi = phi + H0[c] * (bil(b0, M, b0) + bil(b0, M.T, b0)) * Fraction(ytot, 2)
    # Wilson-Yukawa phi-part, link: -(w/2) b(x+e)^T [rho(phi(x+e)) PiW W0 + W0 PiW rho(phi(x))^T] b(x)
    for k in range(3):
        be = b(UNIT[k])
        He = Hp(UNIT[k])
        for c in range(4):
            M1 = rho_c[c] @ PiW @ W0
            M2 = W0 @ PiW @ rho_c[c].T
            phi = phi + He[c] * bil(be, M1, b0) * Fraction(-w, 2) + H0[c] * bil(be, M2, b0) * Fraction(-w, 2)
    # Higgs inertia (D/2)|Phi|^2 and OD4 spring -(lam/4)(|Phi|^2 - v^2)^2, physical Phi = v + phi
    Hs = [Poly.var(h, ZERO, x0.get(h, 0)) for h in hq]
    nrm = Poly()
    for h in Hs:
        nrm = nrm + h * h
    phi = phi + nrm * Fraction(D, 2)
    if lam_H:
        dn = nrm - v * v
        phi = phi - dn * dn * Fraction(lam_H, 4)
    terms = deviation_terms(phi, D, x0)
    gears = [GearType(h, label) for h in HIGGS]
    r0 = 3 * Q - 1
    params = dict(prm, matter=matter.name, partner=partner.name, links=links.name, label=label,
                  potential=("(kappa/2) b'^T P_d rho(conj W) PiW b + Yukawa/Wilson-Yukawa phi-parts + Higgs inertia "
                             "+ OD4 spring; vacuum parts are build_matter's"),
                  reversor=REVERSOR_CHIRAL, candidate="DECLARED CANDIDATE (OWNER decision 5 CONDITIONAL)",
                  default_on=CHIRAL_DEFAULT_ON)
    return Block(tuple(gears), tuple(terms), name=name, vacuum={h: r0 for h in HIGGS}, params=params,
                 doc="chiral Gamma5.V weak SU(2) coupling + Higgs (research candidate; enabled in default_system)", Q=Q)


def chiral_blocks(Q: int = Q_DEFAULT, *, matter: Block | None = None, include_matter: bool = False,
                  hop: int = HOP, wilson: int = WILSON, mass: int = MASS, A: int = A_LINK, v: int = V_HIGGS,
                  lam_H: int = LAM_HIGGS, use_P: bool = True, link_lam: int = 4,
                  names=("matter", "matter2", "wsu2", "chiral")) -> tuple:
    """The candidate's blocks. ``matter``: the existing first doublet member (e.g. default_system's "matter"); if None
    it is built here (name names[0]). Returns (matter2, wsu2, chiral), preceded by matter if include_matter=True (the
    stand-alone chiral system)."""
    if matter is None:
        matter = build_matter(Q=Q, hop=hop, mass=mass, wilson=wilson, species="pair", name=names[0])
    partner = build_partner(Q, hop=hop, wilson=wilson, mass=mass, name=names[1])
    links = build_weak_links(Q, A=A, name=names[2], use_P=use_P, lam=link_lam)
    coup = build_chiral_coupling(Q=Q, matter=matter, partner=partner, links=links, name=names[3], hop=hop,
                                 wilson=wilson, mass=mass, v=v, lam_H=lam_H)
    out = (partner, links, coup)
    return ((matter,) + out) if include_matter else out


def compose_with_default(system, *, on: bool = CHIRAL_DEFAULT_ON, partner_lapse: bool = True, **kw):
    """Return a NEW layers.system.System with the chiral candidate appended (``on=True``), else ``system`` unchanged.

    This helper defaults to on=False for explicit standalone composition. The
    current default_system enables it (or compose_electroweak) explicitly.
    partner_lapse=True copies the selected matter lapse and beta terms to the
    partner. Equal couplings alone do not establish the equivalence principle;
    the composed electroweak default instead replaces these bare-mass terms.
    """
    if not on:
        return system
    from .system import System
    Q = system.Q
    matter = system.by_name("matter")
    blocks = list(system.blocks)
    new = chiral_blocks(Q, matter=matter, hop=matter.params["hop"], wilson=matter.params["wilson"],
                        mass=matter.params["mass"], **kw)
    blocks += list(new)
    info = dict(system.info)
    info["chiral"] = {"status": "DECLARED CANDIDATE (OWNER decision 5 CONDITIONAL)", "blocks": [b.name for b in new],
                      "params": {k: new[-1].params[k] for k in ("A", "kappa", "v", "w", "y", "ytot", "lam_H")}}
    if partner_lapse and system.info.get("gravity") and system.info.get("matter_lapse") == "C":
        from .gravity_select import ONEWAY_LAPSE_WHY
        from .matter_lapse_c import build_matter_beta_read_c, build_matter_lapse_c
        P = system.info["P"]
        field = system.info["lapse_field"]
        partner = new[0]
        blocks.append(build_matter_lapse_c(Q=Q, P=P, field=field, matter=partner,
                                           oneway=(system.info.get("lapse") == "od2"), name="mlapse2",
                                           why=ONEWAY_LAPSE_WHY))
        if system.info.get("beta"):
            blocks.append(build_matter_beta_read_c(Q=Q, P=P, G="beta.G", matter=partner, name="mbeta2"))
        info["chiral"]["partner_lapse"] = "matter_lapse C (mlapse2, mbeta2)"
    elif partner_lapse and system.info.get("gravity"):
        info["chiral"]["partner_lapse"] = ("NOT added: matter_lapse is not 'C' (split form rebuilds gravity_blocks); "
                                           "matter2 is then un-lapsed (EP violation for the partner): integrator item")
    info["pending_owner"] = [p for p in info.get("pending_owner", []) if "chirality" not in p] + [
        "chirality law (decision 5): CANDIDATE composed (layers/chiral.py), CONDITIONAL"]
    return System(Q, tuple(blocks), info)


__all__ = ["CHIRAL_DEFAULT_ON", "Q_DEFAULT", "HOP", "WILSON", "MASS", "A_LINK", "V_HIGGS", "LAM_HIGGS", "HIGGS",
           "REVERSOR_CHIRAL", "chiral_algebra", "check_chiral_algebra", "chiral_params", "build_partner",
           "build_weak_links", "build_chiral_coupling", "chiral_blocks", "compose_with_default"]
