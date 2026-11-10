"""EINSTEIN (Study 28, builder EINF-A): the linearised Einstein (Fierz-Pauli, harmonic gauge) layer for ALL TEN metric
components, as a NEW composer on top of ONE. TENSOR BLOCKS ONLY. NEW file; no existing package file is modified (the metric
block is COPIED with new gear roles; layers/one.py, layers/gravity*.py stay frozen). DEFAULT OFF.

WHY A BASIS CHANGE (DeWitt). Linearised GR in harmonic gauge is Box hbar_{mu nu} = -16 pi G T_{mu nu}, i.e. ten free waves whose
kinetic form on component space is the DeWitt metric q(hbar) = hbar.hbar - hbar^2/2 (indices with eta = diag(-1, 1, 1, 1);
signature 6+, 4-). A reciprocal coupling Phi_int = (1/2) h_{mu nu} T^{mu nu} gives the RIGHT equation only if the field's kinetic
form is q; with ten independent "Euclidean" gears the reciprocal source of hbar would be the trace-reversed Tbar (static dust would
source hbar_ii: wrong; NOTES_gravity "DeWitt" note). Rule3's kinetic term is D*1 on every gear and cannot be changed; the
integer way to carry q is a basis in which 2q is diag(+-1) with EQUAL weights, plus the documented field signs (u = s dPhi/db,
GearType.sign; core/reciprocity.py supports them). Several exact rational bases exist (Sylvester fixes only the inertia 6+/4-);
this one keeps the package's lapse metric.h00 as a basis gear. Exact integer basis at the gravity scale P (U = F/(2P)):

    metric.h00 = F  = P h_00 = P (hbar_00 + hbar_kk)/2        s = +1   THE lapse, unchanged (it already is this combination)
    metric.a1       = P (hbar_xx - hbar_yy)/2                 s = +1   (the package's idle gear 'hxx', renamed)
    metric.a2       = P hbar_zz                               s = +1   ('hyy', renamed)
    metric.a3       = P (hbar_xx + hbar_yy + 2 hbar_zz)/2     s = -1   ('hzz', renamed)
    metric.h0i      = P hbar_0i (link gears)                  s = -1
    metric.hij      = P hbar_ij (i != j, plaquette gears)     s = +1
    2 q(hbar) = (4/P^2) (F^2 + a1^2 + a2^2 - a3^2 - Sum_i h0i^2 + Sum_{i<j} hij^2)     (exact; observe/einstein.dewitt_check)

and back:  P h_00 = F,  P h_xx = F + a1 - a3,  P h_yy = F - a1 - a3,  P h_zz = F + 2 a2 - 2 a3,  P h_0i = h0i,  P h_ij = hij.
Every gear keeps THE ONE headroom stencil u = (Q-1) Sum_6 b + 6 b (on-site 6, faces Q - 1; c^2 = (Q-1)/(3Q)): the free part of
the copied metric block is u-IDENTICAL to the package's (only names and documented signs change). z is singled out by the basis:
with the lapse h_00 kept as a basis gear, the rest of the diagonal sector has DeWitt form 2(Sum hbar_dd^2 - S^2), S = Sum hbar_kk,
of signature (2+, 1-), so no permuted trio of equal-sign gears completes it. (A cubic-symmetric integer basis exists if the lapse
is NOT a gear: 4q|diag = Sum_d (hbar_00 + 2 hbar_dd + S)^2 - (hbar_00 + 3S)^2; it would re-express every existing lapse block.)
The field equations themselves are cubic-symmetric; only the rounding pattern is not.

THE READER (board form of (1/2) h_{mu nu} T^{mu nu}). The kinetic term is fixed (D*1), so a metric multiplies the matter's
ONE-TIME potential: Phi_int = h_00 E_site + Sum_d (h_00 + h_dd)|link E_link,d (E = the positive mass / link energies). With the
basis above, P (h_00 + h_dd) = 2F + Delta_d, Delta_x = a1 - a3, Delta_y = -a1 - a3, Delta_z = 2 a2 - 2 a3 (exact):
  * the 2F part is TODAY's form-C lapse on L0 (lapseL0: clock factor 1 - F/P on M0, link factor 1 - (F_x + F_y)/P on T):
    unchanged; its source dPhi/dF = (E_site + Sum_d Ebar_d)/P is the GR source of h_00 = (hbar_00 + hbar_kk)/2, i.e. the
    active mass rho + Sum p (Tolman) - the package's lapse was already the y0 component of the DeWitt coupling;
  * NEW block 'einL0' = the Delta part on L0's difference transport (reciprocal; rank 3; B3 link monomials; coefficients
    k w and k w/2, k = (Q - 1)/(2P) = 2^12: integer). L0 sources a1, a2, a3 with its directional link energies (the diagonal
    stress) and reads h_dd on its d-links.
  Consequence (THEOREM of the construction, checked in tests/test_einstein.py): a source with T^ij = 0 (dust; E_link = 0) sources
  ONLY F, so a1 = a2 = a3 = 0, h_dd = h_00 and the link factor is 1 - 2 h_00: gamma = 1 is DERIVED from the Fierz-Pauli (DeWitt)
  field equation and the reader form, no longer a chosen link factor; the old 1911 control (link factor 1 - h_00) is a reader that
  is NOT of the form (1/2) h T.

WALLS (stated, not built; see NOTES_einstein.md):
  * h_ij (i != j) for SECOND-ORDER matter (L0, headroom light, KG): T^ij = d_i phi d_j phi needs two difference directions in
    one monomial = three nodes: B3-illegal at ANY rank (THEOREM, locality; observe.einstein.b3_offdiagonal_wall).
  * h_0i for second-order matter: FEELING it is impossible - the matter's two-time read of h_0i would read the a of its own
    partner gears: a cycle of a-reads (no staged inverse), FORBIDDEN by Rule3's reversibility rule (core/tensor.inverse_stages).
    A reciprocal (b-only) source is impossible too (T^0i = phi_dot d_i phi is two-time). A DESIGNATED one-way two-time source
    of h_0i is legal and simply NOT built (choice).
  * the visible Dirac doublet (hands ON, FIX-i): in the coupled ONE build (opt-in) every doublet entry carries the hand Theta, so
    the SU(2)-covariant lapse dressing of its Yukawa mass, F x Theta x Phi x psi psi, has degree 5 = rank 5: FORBIDDEN; the
    only rank-4 piece (F x Theta x bare mass x psi psi) breaks SU(2) at O(U) and is non-integral (6451/32). In ONE v1 the
    covariant F x Yukawa composite is rank 4 (narrow kind) but grain-blocked (412864/(2P)); the FIX-i EP debt stays.
  * OD4 spring energies cannot gravitate (F-4: F x |x|^4 has degree 5 in Phi = rank 5); light on plaquette links (D7): rank 5.

SECOND ORDER (E3). 'einbeta': L0 reads beta.G (G = F^2/(2P) for STATIC fields, the existing GRAV-FIX A gear): 1 - F/P + G/P on M0
(-g00 = 1 - 2U + 2 U^2: PPN beta = 1) and +(17/8)(G_x + G_y)/P on the transport (B1-GRAV's isotropic second-order link factor),
DESIGNATED one-way (a reciprocal partner would source G with matter energy at FIRST order; the reciprocal rank-4 quartic
F^2 x L0 needs (Q - 1)/(4P^2) in Z: grain-blocked at P = 2^20). The 3-graviton vertex is PARTIAL: its static 00-part is the
existing G source -(w_G/(2P)) Lap(F^2) (one-way); its one-axis one-time parts (h x (Delta_d h)^2, rank 3) are legal but NOT
built (unsafe with the ONE stencil's 1/(3Q) headroom where h_00 + h_dd < 0); cross-axis and two-time parts are impossible.

Nothing here is a physical claim; gear names are labels.
"""
from __future__ import annotations

from fractions import Fraction

from ..core.tensor import Block, GearType
from . import gravity as gr
from .gravity_l0 import l0_hops

ZERO = (0, 0, 0)
EIN_VERSION = "EINSTEIN v1 (Study 28, EINF-A): DeWitt basis + L0 diagonal stress + L0 beta read"
DEWITT_GEARS = ("h00", "a1", "a2", "a3", "h0x", "h0y", "h0z", "hxy", "hxz", "hyz")
RENAME = {"hxx": "a1", "hyy": "a2", "hzz": "a3"}
SIGNS = {"h00": 1, "a1": 1, "a2": 1, "a3": -1, "h0x": -1, "h0y": -1, "h0z": -1, "hxy": 1, "hxz": 1, "hyz": 1}
# P (h_00 + h_dd) = 2 F + Delta_d with Delta_d = Sum_g DELTA[d][g] * g
DELTA = {0: {"a1": 1, "a3": -1}, 1: {"a1": -1, "a3": -1}, 2: {"a2": 2, "a3": -2}}
# exact maps (coefficients of the stored gears, all divided by P)
H_LOWER = {   # P h_{mu nu} (lower indices) as integer combinations of the stored gears
    "00": {"h00": 1}, "xx": {"h00": 1, "a1": 1, "a3": -1}, "yy": {"h00": 1, "a1": -1, "a3": -1},
    "zz": {"h00": 1, "a2": 2, "a3": -2}, "0x": {"h0x": 1}, "0y": {"h0y": 1}, "0z": {"h0z": 1},
    "xy": {"hxy": 1}, "xz": {"hxz": 1}, "yz": {"hyz": 1}}
HBAR_LOWER = {   # P hbar_{mu nu}
    "00": {"h00": 2, "a2": 1, "a3": -2}, "xx": {"a1": 1, "a2": -1, "a3": 1}, "yy": {"a1": -1, "a2": -1, "a3": 1},
    "zz": {"a2": 1}, "0x": {"h0x": 1}, "0y": {"h0y": 1}, "0z": {"h0z": 1},
    "xy": {"hxy": 1}, "xz": {"hxz": 1}, "yz": {"hyz": 1}}

WHY_SIGN = {
    "a3": ("DeWitt metric (Fierz-Pauli kinetic form q = hbar.hbar - hbar^2/2) is indefinite: in the integer basis "
           "2q = (4/P^2)(F^2 + a1^2 + a2^2 - a3^2 - Sum h0i^2 + Sum hij^2) the conformal-type combination a3 carries -1"),
    "h0i": ("DeWitt metric: the mixed components enter q with -2 hbar_0i^2 (eta^00 eta^ii = -1), field sign -1 "
            "(the harmonic-gauge 'ghost' sign of the time-space components, as A_0 in Feynman gauge)"),
}
WHY_BETA = ("beta = 1 read of L0 (Study 28 E3): clock factor + G/P on M0 and (17/8)(G_x + G_y)/P on the difference transport, "
            "G = F^2/(2P) the GRAV-FIX A auxiliary; one-way as B1-GRAV's mbeta: a reciprocal partner would source G with the "
            "L0 energy at FIRST order (G = F^2/(2P) - F); the reciprocal rank-4 quartic F^2 x L0 needs (Q - 1)/(4 P^2) in Z "
            "(grain-blocked at P = 2^20)")
WHY_TESTLIGHT = ("test light (Study 28 E4 demos): a headroom gear READING the board-built metric (one-way test body; it does "
                 "not source the metric, so the field is the source's alone)")

WALLS = {
    "h_ij (i != j), second-order matter": "B3 (three nodes per monomial), at any rank: THEOREM (locality)",
    "h_0i, second-order matter": "feeling it = a-read cycle (Rule3 reversibility): THEOREM; no b-only (reciprocal) source "
                                 "(two-time); a designated one-way source is legal and NOT built",
    "visible Dirac doublet (hands ON)": "coupled ONE: F x Theta x Phi x psi psi = degree 5 = rank 5: FORBIDDEN; rank-4 bare-"
                                        "mass piece breaks SU(2) and is non-integral; ONE v1: narrow kind rank 4 but grain-"
                                        "blocked; FIX-i EP debt unchanged",
    "OD4 spring energy as a source (F-4)": "F x |x|^4: degree 5 in Phi = rank 5: FORBIDDEN (s11 AGREE_CL2 row 16)",
    "E1 photon reading the metric": "possible as for the test light, but exact E1 Gauss is then lost (UNIV T5 THEOREM): owner "
                                    "choice, NOT built",
    "3-graviton vertex": "only the one-time, one-axis part h x (Delta_d h)^2 is B3/rank-3 legal (d_i h d_j h, i != j: B3; "
                         "time-derivative parts: two-time); NOT built (OPEN)",
    "exactly conserved source / exact Bianchi": "G-NOGO-a and CL2 row 5: THEOREMS (any rank)",
}


# ====================================================================== the metric block in the DeWitt basis
def dewitt_metric_block(metric: Block) -> Block:
    """COPY of the package's metric block (layers/gravity.build_metric) with the DeWitt roles: hxx, hyy, hzz renamed a1, a2, a3;
    documented field signs SIGNS (-1 needs sign_why). The free headroom stencil is u-IDENTICAL (checked: every gear has
    on-site 6 and faces Q - 1 and nothing else). Construction-time only."""
    Q = metric.Q
    names = [g.name for g in metric.gears]
    if sorted(names) != sorted(gr.COMPONENTS):
        raise ValueError(f"expected the 10-component metric block, got {names}")
    stencil = {}
    for t in metric.terms:
        target, c, facs = t[0], t[1], t[2]
        if len(t) > 3 or len(facs) != 1 or facs[0][0] != target or facs[0][2] != "b":
            raise ValueError(f"metric block term {t!r} is not a free stencil term")
        stencil.setdefault(target, []).append((tuple(facs[0][1]), c))
    for g, ent in stencil.items():
        d = dict(ent)
        if d.get(ZERO) != 6 or len(d) != 7 or any(d[e] != Q - 1 for e in gr.SIX):
            raise ValueError(f"metric gear {g!r} is not on THE ONE headroom stencil")
    rn = lambda n: RENAME.get(n, n)
    gears = []
    for g in metric.gears:
        n = rn(g.name)
        s = SIGNS[n]
        why = "" if s == 1 else (WHY_SIGN["a3"] if n == "a3" else WHY_SIGN["h0i"])
        gears.append(GearType(n, g.label, g.link, s, why))
    terms = tuple((rn(t[0]), t[1], tuple((rn(f[0]), f[1], f[2]) for f in t[2])) for t in metric.terms)
    return Block(tuple(gears), terms, name=metric.name, vacuum={rn(k): v for k, v in metric.vacuum.items()},
                 params=dict(metric.params, dewitt={"roles": {"h00": "P h_00 = P (hbar_00 + hbar_kk)/2",
                                                              "a1": "P (hbar_xx - hbar_yy)/2", "a2": "P hbar_zz",
                                                              "a3": "P (hbar_xx + hbar_yy + 2 hbar_zz)/2",
                                                              "h0i": "P hbar_0i", "hij": "P hbar_ij"},
                                                    "signs": dict(SIGNS), "renamed": dict(RENAME)}),
                 doc=metric.doc + " [Study 28: DeWitt basis roles and field signs; stencil unchanged]", Q=Q)


# ====================================================================== L0: the diagonal-stress (Delta) part of the reader
def l0_delta_potential(Q: int, P: int, metric: str = "metric", ns: str = "ref", body_signs=(1, -1, 1)) -> list:
    """Phi_new = Sum_links (Delta_d(x) + Delta_d(x + e))/(2P) x E_link,d on L0's difference transport (the same monomials as
    layers.gravity_l0c.l0c_lapse_potential's link part, with F/P -> Delta_d/(2P))."""
    if (Q - 1) % P:
        raise ValueError("needs (Q - 1)/P an integer (Q - 1 = 2Pk)")
    k2 = Fraction(Q - 1, P)
    q = lambda g: f"{ns}.{g}"
    pot = []
    for t, s, ax, c in l0_hops(Q, body_signs, ns):
        w = Fraction(c, Q)
        e = gr.AXES[ax]
        for g, m in DELTA[ax].items():
            G = f"{metric}.{g}"
            cf = k2 * w * m / 2
            for fo in (ZERO, e):
                pot.append((cf / 2, [(G, fo), (q(t), ZERO), (q(s), ZERO)]))
                pot.append((cf / 2, [(G, fo), (q(t), e), (q(s), e)]))
                pot.append((-cf, [(G, fo), (q(t), ZERO), (q(s), e)]))
    return pot


def build_l0_dewitt(*, Q: int, P: int, metric: str = "metric", ns: str = "ref", body_signs=(1, -1, 1),
                    name: str = "einL0") -> Block:
    """The NEW reciprocal reader/source block of L0 for the diagonal anisotropic components (a1, a2, a3): u = s dPhi/db with the
    DeWitt field signs. Owns no gear. Rank 3."""
    pot = l0_delta_potential(Q, P, metric, ns, body_signs)
    signs = {f"{metric}.{g}": SIGNS[g] for g in ("a1", "a2", "a3")}
    terms = gr.gradient_terms(pot, signs=signs, what="einstein L0 DeWitt (Delta part)")
    return Block((), tuple(terms), name=name, Q=Q,
                 params={"Q": Q, "P": P, "metric": metric, "ns": ns, "body_signs": tuple(body_signs),
                         "reader": "link factor -(Delta_d(x) + Delta_d(x+e))/(2P) on the difference transport T",
                         "delta": {str(d): dict(v) for d, v in DELTA.items()}},
                 doc="L0 reads h_dd - h_00 and sources a1, a2, a3 with its directional link energies (diagonal stress)")


def build_l0_beta_read(*, Q: int, P: int, G: str = "beta.G", ns: str = "ref", body_signs=(1, -1, 1),
                       name: str = "einbeta") -> Block:
    """L0's beta = 1 read (E3): -(G/P) E_site - (17/8)((G_x + G_y)/P) E_link (sign: the factors multiply -E), designated."""
    if (Q - 1) % P:
        raise ValueError("needs (Q - 1)/P an integer")
    k2 = Fraction(Q - 1, P)
    q = lambda g: f"{ns}.{g}"
    pot = []
    for gi in range(48):                                   # site: E_site = ((Q-1)/2) b^T M0 b = k2 P (3|b|^2 - ...)/... x F/P
        nm = q(f"R{gi:02d}")
        pot.append((-3 * k2, [(G, ZERO), (nm, ZERO), (nm, ZERO)]))
    c_link = Fraction(17, 8)
    for t, s, ax, c in l0_hops(Q, body_signs, ns):
        w = Fraction(c, Q)
        e = gr.AXES[ax]
        pot.append((k2 * w, [(G, ZERO), (q(t), ZERO), (q(s), ZERO)]))
        for fo in (ZERO, e):
            pot.append((-c_link * k2 * w / 2, [(G, fo), (q(t), ZERO), (q(s), ZERO)]))
            pot.append((-c_link * k2 * w / 2, [(G, fo), (q(t), e), (q(s), e)]))
            pot.append((c_link * k2 * w, [(G, fo), (q(t), ZERO), (q(s), e)]))
    only = [q(f"R{gi:02d}") for gi in range(48)]
    terms = gr.gradient_terms(pot, only=only, designation=WHY_BETA, what="einstein L0 beta read")
    return Block((), tuple(terms), name=name, Q=Q,
                 params={"Q": Q, "P": P, "G": G, "ns": ns, "site": "+G/P on M0", "link": "+(17/8)(G_x+G_y)/P on T"},
                 doc="beta = 1 read of L0 (designated one-way)")


# ====================================================================== test light (demos / tests only)
def build_test_light(*, Q: int, P: int, metric: str = "metric", mode: str = "full", name: str = "light",
                     oneway: bool = True) -> Block:
    """A headroom gear L (u = (Q-1) Sum_6 L + 6 L, the ONE cone) reading the metric on its links:
    mode "full": link factor 1 - (h_00 + h_dd)|link = 1 - (2F + Delta_d)|link/(2P)   (the Einstein reader)
    mode "h00":  link factor 1 - h_00|link = 1 - (F_x + F_y)/(2P)                      (CONTROL: lapse only, '1911')
    mode "none": no metric read.  oneway: the light does not source (test body; designated)."""
    if mode not in ("full", "h00", "none"):
        raise ValueError("mode must be 'full', 'h00' or 'none'")
    Lq = f"{name}.L"
    terms = gr.gradient_terms(gr.headroom_potential("L", Q), what="test light wave")
    pot = []
    kq = Fraction(Q - 1, 2 * P)                              # (Q-1)/(2P) = k
    F = f"{metric}.h00"
    for ax, e in enumerate(gr.AXES):
        mono = ((1, [(Lq, ZERO), (Lq, ZERO)]), (1, [(Lq, e), (Lq, e)]), (-2, [(Lq, ZERO), (Lq, e)]))
        for fo in (ZERO, e):
            if mode == "full":
                for cc, mm in mono:
                    pot.append((kq * cc, [(F, fo)] + mm))
                    for g, m in DELTA[ax].items():
                        pot.append((kq * cc * m / 2, [(f"{metric}.{g}", fo)] + mm))
            elif mode == "h00":
                for cc, mm in mono:
                    pot.append((kq * cc / 2, [(F, fo)] + mm))
    if pot:
        if oneway:
            terms += gr.gradient_terms(pot, only=[Lq], designation=WHY_TESTLIGHT, what="test light read")
        else:
            signs = {f"{metric}.{g}": SIGNS[g] for g in ("a1", "a2", "a3")}
            terms += gr.gradient_terms(pot, signs=signs, what="test light read (reciprocal)")
    terms = [(t[0].split(".", 1)[1] if t[0] == Lq else t[0],) + tuple(t[1:]) for t in terms]
    return Block((GearType("L", "official"),), tuple(terms), name=name, vacuum={"L": 3 * Q - 1}, Q=Q,
                 params={"Q": Q, "P": P, "mode": mode, "oneway": oneway}, doc=f"test light ({mode})")


# ====================================================================== the composer (DEFAULT OFF)
def einstein_system(base=None, *, on: bool = False, l0_beta: bool = True):
    """base None -> layers.one.one_system(), whatever it returns (after the push: ONE v1, couple_doublet=False, fp 77f6d251...;
    the coupled build 593753fa... is an explicit opt-in). on=False returns base UNCHANGED. on=True: the metric block is
    replaced by its DeWitt copy (dewitt_metric_block; free part u-identical), and 'einL0' (+ 'einbeta' if l0_beta) is
    appended. Needs the wave lapse metric.h00, L0 in form C (l0_lapse 'W') and Q - 1 = 2Pk."""
    from .system import System
    if base is None:
        from .one import one_system
        base = one_system()
    if not on:
        return base
    info = dict(base.info)
    if info.get("lapse_field") != "metric.h00" or info.get("l0_lapse") != "W":
        raise ValueError("einstein layer needs the wave lapse metric.h00 and L0 in form C (l0_lapse 'W')")
    Q, P = base.Q, info["P"]
    names = [b.name for b in base.blocks]
    for nm in ("einL0", "einbeta"):
        if nm in names:
            raise ValueError(f"namespace {nm!r} is taken")
    blocks = [dewitt_metric_block(b) if b.name == "metric" else b for b in base.blocks]
    body_signs = tuple(base.by_name("ref").params["body_signs"])
    blocks.append(build_l0_dewitt(Q=Q, P=P, body_signs=body_signs))
    if l0_beta:
        if "beta" not in names:
            raise ValueError("l0_beta needs the beta block (beta.G)")
        blocks.append(build_l0_beta_read(Q=Q, P=P, body_signs=body_signs))
    info["einstein"] = {"version": EIN_VERSION, "on": True, "l0_beta": l0_beta, "signs": dict(SIGNS),
                        "roles": "metric.h00 = P h_00; a1, a2, a3, h0i, hij: see layers/einstein.py", "walls": WALLS}
    return System(Q, tuple(blocks), info)


__all__ = ["EIN_VERSION", "DEWITT_GEARS", "RENAME", "SIGNS", "DELTA", "H_LOWER", "HBAR_LOWER", "WALLS", "WHY_BETA",
           "dewitt_metric_block", "l0_delta_potential", "build_l0_dewitt", "build_l0_beta_read", "build_test_light",
           "einstein_system"]
