"""HYBRID gravity source (Study 10, ST-2 port; OWNER decision 2 of 13:09 UTC: approved NEW LAW, designated one-way;
final adoption after the reversor test and a long run). NEW FILE; DEFAULT OFF. No existing package file is edited.

The lapse field F (= metric.h00 of the wave lapse) is sourced by a TWO-TIME density instead of the reciprocal b-only
source (Study 10 THEOREM G-NOGO-a / G1: under Rule3 no function of the present values b alone is conserved, so an
exactly conserved source must read the previous values a and has no b-only potential partner -> designated one-way):

    u_F(x) += e_L0(x) + rho(x)

    e_L0(x) = (k/2) [ 3 (|a_x|^2 + |b_x|^2) - (1/2)(a_x.(S b)_x + b_x.(S a)_x) ]      (L0, form C ports S at weight Q-1)
            = ( E_L0/2 - 3|a - b|^2 )_x / (4P)     with E_L0 = D(|a|^2+|b|^2) - 2 a^T H_L0 b, the Board-Noether energy
              (Tolman/TT energy of the dark sector; exact for a free L0 up to the remainder term and the 1/Q defect
              3|a-b|^2; equals the reciprocal L0 lapse source's time mean x cos^2(w/2); Q = 2Pk + 1, k even)
    rho(x)  = -g a_x^T J b_x                                                       (Dirac pair: rest-mass density)
              (the carrier-number Wronskian N_J/D: an internal Noether charge, exact with remainder for ANY lapse
              history; g = round((m/8P)/sin w0), cos w0 = m/D: equal to today's mass-source mean at rest; sign: the J+
              sense (b(t+1) ~ J b(t)) gravitates with U > 0, like L0)

The lapse ACTION on L0 and on the Dirac pair is unchanged (form C, R1); only their reciprocal b-only SOURCE monomials are
dropped (their one-way read of F is designated). Optional: GRAV-FIX (A) detuned beta (layers/gravity_beta_fix.py,
default ON here) and a detuned h00 (face weight (Q-1)/2: Study 10 AGREE_ST S21; default OFF).

Integrator switch (one line, NOT applied here; for layers/system.py when the owner adopts it):
    default_system(..., gravity_source="lapse"):  if gravity_source == "hybrid": return apply_hybrid(System(...))
"""
from __future__ import annotations

import math
from fractions import Fraction

from ..core.tensor import Block
from . import gravity as gr
from .gravity_l0c import l0c_lapse_potential
from .matter import algebra, matter_names
from .matter_lapse_c import matter_lapse_c_potential

ZERO = (0, 0, 0)
HYB_WHY = ("HYBRID gravity source (Study 10, owner decision 2, 13:09): two-time density (L0 Board-Noether energy / "
           "Dirac carrier-number Wronskian) read with a-reads; no b-only quadratic quantity is conserved under Rule3 "
           "(G-NOGO-a = G1), so an exactly conserved source has no reciprocal partner: designated one-way")
HYB_ACT_WHY = ("HYBRID: the lapse ACTION on L0 / the Dirac pair (form C, R1) kept; its reciprocal b-only source is "
               "replaced by the two-time hybrid source (one-way)")


def rho_g_default(matter: Block, P: int, Q: int) -> int:
    """g = round((m/8P)/sin w0), cos w0 = m/D (parameter choice; 2681 for the v2 default)."""
    m = matter.params["mass"]
    c = m / (6 * Q)
    return int(round(m / (8 * P) / math.sqrt(1.0 - c * c)))


def hybrid_source_terms(*, Q: int, P: int, field: str, ref: Block, matter: Block, g: int | None = None,
                        l0: bool = True, dirac: bool = True) -> list:
    """Monomials (target field) of e_L0 + rho, merged and integrality-checked. Every term carries HYB_WHY."""
    if (Q - 1) % (2 * P):
        raise ValueError("needs Q - 1 = 2Pk")
    k = (Q - 1) // (2 * P)
    if k % 2:
        raise ValueError("the L0 TT density needs k = (Q-1)/(2P) even (c1 = 3k/2)")
    acc: dict = {}

    def put(c, f1, f2):
        key = tuple(sorted((f1, f2)))
        acc[key] = acc.get(key, Fraction(0)) + Fraction(c)

    if l0:
        lg = [ref.qualify(gt.name) for gt in ref.gears]
        lset = set(lg)
        for nm in lg:                                            # (k/2) 3 (|a|^2 + |b|^2)
            for fld in ("a", "b"):
                put(Fraction(3 * k, 2), (nm, ZERO, fld), (nm, ZERO, fld))
        n_port = 0
        for t in ref.terms:                                      # -(k/2)(1/2)[a_x (S b)_x + b_x (S a)_x]
            target, c, factors = ref.qualify(t[0]), t[1], t[2]
            if len(factors) != 1:
                continue
            gname, off, fld = ref.qualify(factors[0][0]), tuple(factors[0][1]), factors[0][2]
            if fld != "b" or gname not in lset or target not in lset:
                continue
            if off == ZERO and gname == target and c == 6:
                continue                                         # the on-site 6 (absorbed in the 3|a-b|^2 defect)
            if c % (Q - 1):
                raise ValueError(f"L0 port entry {c} not in (Q-1) Z")
            w = Fraction(c, Q - 1)                               # signed port weight
            n_port += 1
            for f1, f2 in (("a", "b"), ("b", "a")):
                put(-Fraction(k, 2) * w / 2, (target, ZERO, f1), (gname, off, f2))
        if n_port == 0:
            raise ValueError("no L0 port terms found (is ref the form-C block?)")
    if dirac:
        g = rho_g_default(matter, P, Q) if g is None else int(g)
        Jm = algebra(matter.params.get("species", "pair"))["J"]
        mn = [matter.qualify(x) for x in matter_names(matter.params.get("species", "pair"))]
        for i in range(len(mn)):
            for j in range(len(mn)):
                if Jm[i, j]:
                    put(-g * int(Jm[i, j]), (mn[i], ZERO, "a"), (mn[j], ZERO, "b"))
    terms = []
    for (f1, f2), c in sorted(acc.items()):
        if c == 0:
            continue
        if c.denominator != 1:
            raise ValueError(f"hybrid source: non-integer coefficient {c} for factors {f1} {f2}")
        terms.append((field, int(c), (f1, f2), {"designated_one_way": HYB_WHY}))
    return terms


def build_hybrid_source(*, Q: int, P: int, field: str, ref: Block, matter: Block, g: int | None = None,
                        l0: bool = True, dirac: bool = True, name: str = "hsrc") -> Block:
    terms = hybrid_source_terms(Q=Q, P=P, field=field, ref=ref, matter=matter, g=g, l0=l0, dirac=dirac)
    return Block((), tuple(terms), name=name, Q=Q,
                 params={"Q": Q, "P": P, "field": field, "g": (rho_g_default(matter, P, Q) if g is None else g),
                         "l0": l0, "dirac": dirac, "law": "HYBRID (owner decision 2, 13:09): e_L0 + rho_J",
                         "designated": len(terms)},
                 doc="two-time hybrid gravity source: L0 Board-Noether energy / Dirac rest-mass Wronskian (one-way)")


def oneway_matter_lapse(*, Q: int, P: int, field: str, matter: Block, name: str = "mlapse") -> Block:
    pot = matter_lapse_c_potential(matter=matter, P=P, field=field)
    only = [matter.qualify(x) for x in matter_names(matter.params.get("species", "pair"))]
    terms = gr.gradient_terms(pot, only=only, designation=HYB_ACT_WHY, what="hybrid: matter lapse action")
    return Block((), tuple(terms), name=name, Q=Q, params={"Q": Q, "P": P, "field": field, "oneway": True,
                                                           "form": "C (Wilson difference), action only"},
                 doc="Dirac matter lapse action (form C), its b-only source removed (HYBRID)")


def oneway_l0_lapse(*, Q: int, P: int, field: str, body_signs, ns: str = "ref", name: str = "lapseL0") -> Block:
    pot = l0c_lapse_potential(Q, P, field, ns, body_signs)
    only = [f"{ns}.R{g:02d}" for g in range(48)]
    terms = gr.gradient_terms(pot, only=only, designation=HYB_ACT_WHY, what="hybrid: L0 lapse action")
    return Block((), tuple(terms), name=name, Q=Q, params={"Q": Q, "P": P, "field": field, "oneway": True,
                                                           "form": "C, action only", "body_signs": tuple(body_signs)},
                 doc="form-C L0 lapse action, its b-only source removed (HYBRID)")


def detuned_h00_metric(metric: Block, Q: int, gear: str = "h00", num: int = 1, den: int = 2) -> Block:
    """Copy of the metric block with h00's own stencil replaced by the Laplacian form at face weight (Q-1) num/den
    (AGREE_ST S21 option; DEFAULT OFF). Other components unchanged."""
    wG = Fraction((Q - 1) * num, den)
    if wG.denominator != 1:
        raise ValueError("detuned weight must be an integer")
    new = [t for t in metric.terms if not (t[0] == gear and len(t[2]) == 1 and t[2][0][0] == gear)]
    new += gr.gradient_terms(gr.laplacian_form_potential(gear, Q, int(wG)), what="detuned h00")
    return Block(metric.gears, tuple(new), name=metric.name, vacuum=dict(metric.vacuum),
                 params={**metric.params, "h00_detuned": f"(Q-1) {num}/{den}"}, doc=metric.doc, Q=Q)


def apply_hybrid(system, *, g: int | None = None, beta_fix: bool = True, detune_h00: bool = False):
    """Return a NEW System: the given (v2 default) system with the reciprocal L0/Dirac lapse blocks replaced by their
    one-way actions + the hybrid source block; GRAV-FIX (A) beta (beta_fix) and the detuned h00 (detune_h00)
    optional. Data (vacuum) unchanged."""
    from .system import System
    info = dict(system.info)
    Q, P = system.Q, info["P"]
    field = info.get("lapse_field", "metric.h00")
    if info.get("lapse") != "wave" or info.get("matter_lapse") != "C" or info.get("l0_lapse") != "W":
        raise ValueError("apply_hybrid needs the v2 default gravity (wave lapse, matter lapse C, L0 form C)")
    names = [blk.name for blk in system.blocks]
    if "mlapse" not in names or "lapseL0" not in names:
        raise ValueError("apply_hybrid needs the hands-OFF composition (default_system(chiral=False, electroweak=False)):"
                         " with electroweak ON the Dirac pair's lapse lives in the EW/chiral blocks (lapse x |Phi|^2), "
                         "where the hybrid rest-mass source is not yet ported (OPEN)")
    ref, matter = system.by_name("ref"), system.by_name("matter")
    beta_done = info.get("beta_form") == "detuned"
    blocks = []
    for blk in system.blocks:
        if blk.name == "mlapse":
            blk = oneway_matter_lapse(Q=Q, P=P, field=field, matter=matter, name="mlapse")
        elif blk.name == "lapseL0":
            blk = oneway_l0_lapse(Q=Q, P=P, field=field, body_signs=info["body_signs"], name="lapseL0")
        elif blk.name == "beta" and beta_fix and not beta_done:
            from .gravity_beta_fix import build_beta_detuned
            blk = build_beta_detuned(Q=Q, P=P, k=info["k"], field=blk.params["field"])
        elif blk.name == "metric" and detune_h00:
            blk = detuned_h00_metric(blk, Q)
        blocks.append(blk)
    hs = build_hybrid_source(Q=Q, P=P, field=field, ref=ref, matter=matter, g=g)
    blocks.append(hs)
    info["gravity_source"] = {"law": "HYBRID (owner decision 2, 13:09; NEW LAW, designated one-way)", "g": hs.params["g"],
                              "designated_source_monomials": hs.params["designated"],
                              "beta_fix_A": beta_fix or beta_done, "beta_already_detuned_by_default": beta_done,
                              "detune_h00": detune_h00,
                              "R-a datum": "use hybrid_datum(): the exact two-time total of the source at t = 0"}
    return System(Q, tuple(blocks), info)


def hybrid_system(*, g: int | None = None, beta_fix: bool = True, detune_h00: bool = False, **kw):
    """default_system(**kw) with the HYBRID source applied (DEFAULT OFF in default_system itself). Hands-OFF by
    default (chiral=False, electroweak=False): the system Study 10 analysed; the hands-ON port is OPEN."""
    from .system import default_system
    kw.setdefault("chiral", False)
    kw.setdefault("electroweak", False)
    return apply_hybrid(default_system(**kw), g=g, beta_fix=beta_fix, detune_h00=detune_h00)


__all__ = ["HYB_WHY", "HYB_ACT_WHY", "rho_g_default", "hybrid_source_terms", "build_hybrid_source",
           "oneway_matter_lapse", "oneway_l0_lapse", "detuned_h00_metric", "apply_hybrid", "hybrid_system"]
