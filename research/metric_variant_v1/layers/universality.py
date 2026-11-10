"""UNIVERSALITY (UNIV-BUILDER, R-P1 row A1 / J4): the universal lapse for the compact gauge layers' OWN matter and for
the E1 photon. DECLARED CANDIDATE, DEFAULT OFF. NEW file; every other layer is imported read-only. TENSOR BLOCKS ONLY.

Pre-registration and results: NOTES_universality.md. Tests: tests/test_universality.py.

U1 GAUGE-LAYER MATTER (R1 pattern of layers/matter_lapse_c.py, written in GAUGE-INVARIANT composites)
    S(x)   = (M/2) |psi(x)|^2,  M = mass + 6 kappa A                (the k = 0 rest coefficient: cos w0 = M/D)
    H_k(x) = kappa <psi(x), U(x,k) psi(x+e_k)> - (kappa A/2)(|psi(x)|^2 + |psi(x+e_k)|^2)
             (= -(kappa A/2)|psi(x) - psi(x+e_k)|^2 in the vacuum U = A 1: a DIFFERENCE form, zero at k = 0)
    S + Sum_k H_k is identically the layer's own (mass/2)|psi|^2 + kappa <psi, U psi> (layers/gauge.py).
    Phi_L = - Sum_x (F(x)/(2P)) S(x) - Sum_{x,k} ((F(x) + F(x+e_k))/(2P)) H_k(x)   (clock 1 - U, link 1 - 2U; U = F/(2P))
  forms
    "site"  clock term only (H not lapsed). Gauge invariant; rank 3; integral iff M in 4P Z. The rest clock reads
            N = 1 - U exactly (cos-ratio); the gauge-matter TRANSPORT keeps the flat factor 1 (no link factor).
    "cov"   clock + the full covariant H (U = A 1 + W): gauge invariant; rank 4 (F psi W psi); integral iff M in 4P Z,
            kappa A in 4P Z and kappa in 2P Z. At the v2 default kappa/(2P) = 2^16/2^21 = 1/32: NOT integral
            (OBSTRUCTION; the builder raises). Built and tested at a DECLARED regime with kappa in 2P Z.
    "vac"   clock + H with U -> A 1 (matter_lapse_c applied literally): integral at the default but NOT locally gauge
            invariant: local Gauss/Noether fails at O(U) (the broken-covariance CONTRAST).
  The default gauge mass Q + 3 gives M = 4Q, not in 2P Z for odd Q: the variant uses the DATA-LEVEL mass
  ``universality_mass`` (Q - 1 at the default: M = 4(Q - 1) = 2^35, cos w0 = 2/3 - 2/(3Q)).

U2 THE E1 PHOTON (second-order field, gamma = 1): E1's transport u_A = D A + (Q-1) Lap A (component-wise) gets the link
  factor (1 - (F_x + F_y)/P) (= 1 - 4U uniform: c^2 -> c^2 (1 - 4U), coordinate light speed 1 - 2U) on every dual link
  (A_d(x), A_d(x+e_j)):
    Phi_gamma = + k Sum_{x,d,j} (F(x) + F(x+e_j)) (A_d(x+e_j) - A_d(x))^2,     k = (Q-1)/(2P) (integer: Q - 1 = 2Pk)
  reciprocal: the E1 gradient energy sources the lapse (u_F += k (dA)^2). Lorenz (accumulator identity) and continuity
  (matter equations untouched) stay exact; the dressed Gauss step identity acquires EXACTLY the term -2 g div l(t)
  (l = this block's part of u_A): exact Gauss for a uniform lapse (with (Q-1) -> (Q-1)(1 - 2F/P)), NOT for a
  non-uniform one (OBSTRUCTION, NOTES_universality.md T5). The lapse sits on the storage link (x, x+e_j), half a link
  off the dual link's centre x + (e_j + e_d)/2 (the centred read needs F at x + e_d: an edge offset, C8-type).

U3 SOURCING: the reciprocal partners of U1 (-(M/(4P))|psi|^2 per node: the rest energy) and U2 (+k (dA)^2: the field
  gradient energy). Both are b-only single-time quadratics: NOT exactly conserved (v3 §2 theorem, as for the Dirac pair).

Switch (for the integrator; layers/system.py is NOT edited here): keyword ``universality: bool = False`` in
default_system and, before the electroweak/chiral lines,
    if universality:  # UNIV-BUILDER (R-P1 A1): gauge-matter + E1 universal lapse, DEFAULT OFF
        from .universality import universality_blocks; blocks, info = universality_blocks(Q, blocks, info)  # noqa: E702
"""
from __future__ import annotations

from fractions import Fraction

from ..core.tensor import Block
from . import gravity as gr
from .gauge import ALGEBRAS, UNIT, Poly, build_gauge, gear_names, vec_dot

ZERO = (0, 0, 0)
GAUGE_GROUPS = ("su2", "su3", "u1")
FORMS = ("site", "cov", "vac")
UNIVERSALITY_DEFAULT_ON = False
WHY_TEST = ("UNIVERSALITY TEST read (one-way) of a static PRESCRIBED lapse gear (as matter_lapse_c WHY_C); the reciprocal "
            "block (oneway=False) is the composed form")


def rest_coefficient(params: dict) -> int:
    """M = mass + 6 kappa A: the k = 0 rest coefficient of the gauge matter in the vacuum (cos w0 = M/D)."""
    return params["mass"] + 6 * params["kappa"] * params["A"]


def universality_mass(params: dict, P: int) -> int:
    """The data-level gauge mass nearest to params['mass'] with M = mass + 6 kappa A in 4P Z (integral clock factor
    and reciprocal source). Default (Q = 2^33+1, A = kappa = 2^16, P = 2^20): Q + 3 -> Q - 1."""
    M = rest_coefficient(params)
    MU = ((2 * M + 4 * P) // (8 * P)) * 4 * P           # nearest multiple of 4P (ties up)
    return MU - 6 * params["kappa"] * params["A"]


def _poly_to_pot(poly: Poly) -> list:
    pot = []
    for key, c in poly.t.items():
        if not key:
            if c:
                raise ValueError("lapse composite has a constant term")
            continue
        pot.append((c, [(g, off) for g, off in key]))
    return pot


def gauge_lapse_potential(block: Block, *, P: int, field: str, form: str = "site") -> list:
    """Phi_L of U1 for one compact gauge layer block (qualified gear names), as (coeff, [(gear, offset), ...])."""
    if form not in FORMS:
        raise ValueError(f"form must be one of {FORMS}")
    p = block.params
    group = p["group"]
    if group not in GAUGE_GROUPS:
        raise ValueError("not a compact gauge layer block")
    alg = ALGEBRAS[group]
    A, kappa = p["A"], p["kappa"]
    M = rest_coefficient(p)
    matter, links, _paths = gear_names(group, p["use_P"])
    q = block.qualify
    x0 = {g: A * alg.one[c] for k in range(3) for c, g in enumerate(links[k])}
    uF = Fraction(-1, 2 * P)

    def psi(off):
        return [Poly.var(q(g), off) for g in matter]

    Fx = Poly.var(field, ZERO)
    p0 = psi(ZERO)
    total = Fx * vec_dot(p0, p0) * (uF * Fraction(M, 2))
    if form in ("cov", "vac"):
        for k in range(3):
            e = UNIT[k]
            pe = psi(e)
            if form == "cov":
                Uk = [Poly.var(q(g), ZERO, x0[g]) for g in links[k]]
            else:
                Uk = [Poly.const(A * alg.one[c]) for c in range(alg.m)]
            H = (vec_dot(p0, alg.apply(Uk, pe)) * kappa
                 - (vec_dot(p0, p0) + vec_dot(pe, pe)) * Fraction(kappa * A, 2))
            total = total + (Fx + Poly.var(field, e)) * H * uF
    return _poly_to_pot(total)


def _integrality_hint(p: dict, P: int, form: str) -> str:
    M = rest_coefficient(p)
    bad = []
    if M % (4 * P):
        bad.append(f"M = mass + 6 kappa A = {M} not in 4P Z (M/(4P) = {Fraction(M, 4 * P)})")
    if form in ("cov", "vac") and (p["kappa"] * p["A"]) % (4 * P):
        bad.append(f"kappa A = {p['kappa'] * p['A']} not in 4P Z")
    if form == "cov" and p["kappa"] % (2 * P):
        bad.append(f"kappa = {p['kappa']} not in 2P Z (kappa/(2P) = {Fraction(p['kappa'], 2 * P)}): the covariant "
                   "link factor on the gauge part kappa <psi, W psi> is not an integer coefficient")
    return "; ".join(bad) or "integral"


def build_gauge_lapse(*, block: Block, Q: int, P: int, field: str, form: str = "site", oneway: bool = False,
                      name: str | None = None, why: str = WHY_TEST) -> Block:
    """U1 for one compact gauge layer. oneway=False: ONE potential, reciprocal (the gauge matter sources F).
    oneway=True: only the gauge gears read F (designated; for a static PRESCRIBED lapse gear in tests)."""
    p = block.params
    pot = gauge_lapse_potential(block, P=P, field=field, form=form)
    hint = _integrality_hint(p, P, form)
    try:
        if oneway:
            matter, links, paths = gear_names(p["group"], p["use_P"])
            own = [block.qualify(g) for g in matter + [g for k in range(3) for g in links[k]]
                   + [g for v in paths.values() for g in v]]
            terms = gr.gradient_terms(pot, only=own, designation=why, what=f"universality lapse ({p['group']})")
        else:
            terms = gr.gradient_terms(pot, what=f"universality lapse ({p['group']})")
    except ValueError as exc:
        raise ValueError(f"universality form {form!r} on {block.name!r} is NOT integral at P = {P}: {hint}") from exc
    return Block((), tuple(terms), name=name or f"ulapse_{block.name}", Q=Q,
                 params={"Q": Q, "P": P, "field": field, "form": form, "oneway": oneway, "group": p["group"],
                         "M": rest_coefficient(p), "integrality": hint},
                 doc=f"universal lapse of the {p['group']} matter, form {form} (clock 1 - U on M |psi|^2 / 2"
                     + ("" if form == "site" else ", link 1 - 2U on the difference composite H") + ")")


def photon_lapse_potential(em: Block, *, P: int, field: str) -> list:
    """Phi_gamma of U2: + k Sum (F(x) + F(x+e_j)) (A_d(x+e_j) - A_d(x))^2, k = (Q-1)/(2P)."""
    Q = em.params["Q"]
    k = Fraction(Q - 1, 2 * P)
    pot = []
    for d in ("A_x", "A_y", "A_z"):
        g = em.qualify(d)
        for j in range(3):
            e = UNIT[j]
            for fo in (ZERO, e):
                pot.append((k, [(field, fo), (g, e), (g, e)]))
                pot.append((-2 * k, [(field, fo), (g, ZERO), (g, e)]))
                pot.append((k, [(field, fo), (g, ZERO), (g, ZERO)]))
    return pot


def build_photon_lapse(*, em: Block, Q: int, P: int, field: str, oneway: bool = False, name: str = "ulight",
                       why: str = WHY_TEST) -> Block:
    """U2: the E1 photon link lapse (reciprocal by default). Needs Q - 1 in 2P Z."""
    if (Q - 1) % (2 * P):
        raise ValueError("photon lapse needs Q - 1 = 2Pk")
    pot = photon_lapse_potential(em, P=P, field=field)
    if oneway:
        terms = gr.gradient_terms(pot, only=[em.qualify(d) for d in ("A_x", "A_y", "A_z")], designation=why,
                                  what="photon lapse")
    else:
        terms = gr.gradient_terms(pot, what="photon lapse")
    return Block((), tuple(terms), name=name, Q=Q,
                 params={"Q": Q, "P": P, "field": field, "oneway": oneway, "k": (Q - 1) // (2 * P),
                         "link_factor": "1 - (F_x + F_y)/P on every dual link of E1's component-wise Laplacian"},
                 doc="E1 photon link lapse (gamma = 1; reciprocal unless oneway)")


def universality_blocks(Q: int, blocks, info: dict, *, gauge_form: str = "site", photon: bool = True):
    """(blocks, info) with the universality candidate: gauge layers rebuilt at the data-level universality mass,
    one reciprocal U1 block per gauge layer, the reciprocal U2 block on E1. Needs gravity (info['lapse_field'])."""
    if not info.get("gravity"):
        raise ValueError("universality needs gravity=True (the ONE lapse field)")
    P, field = info["P"], info["lapse_field"]
    out, new_info, extra, masses = [], dict(info), [], {}
    for blk in blocks:
        if blk.params.get("group") in GAUGE_GROUPS and blk.name in GAUGE_GROUPS:
            p = blk.params
            mU = universality_mass(p, P)
            masses[blk.name] = {"mass_default": p["mass"], "mass_universality": mU,
                                "M": mU + 6 * p["kappa"] * p["A"], "cos_w0": str(Fraction(mU + 6 * p["kappa"] * p["A"],
                                                                                          6 * Q))}
            blk = build_gauge(group=p["group"], Q=Q, A=p["A"], kappa=p["kappa"], mass=mU, lam=p["lam"],
                              use_P=p["use_P"], kappa_P=p["kappa_P"], c_P=p["c_P"], beta=p["beta"], name=blk.name)
            extra.append(build_gauge_lapse(block=blk, Q=Q, P=P, field=field, form=gauge_form,
                                           oneway=(info.get("lapse") == "od2"), name=f"ulapse_{blk.name}"))
        out.append(blk)
    em_blocks = [b for b in out if b.name == "em" and any(g.name == "A_x" for g in b.gears)]
    if photon and em_blocks:
        extra.append(build_photon_lapse(em=em_blocks[0], Q=Q, P=P, field=field, oneway=(info.get("lapse") == "od2")))
    new_info["universality"] = {"status": "DECLARED CANDIDATE, DEFAULT OFF (UNIV-BUILDER)", "gauge_form": gauge_form,
                                "photon": bool(photon and em_blocks), "gauge_mass": masses,
                                "blocks": [b.name for b in extra],
                                "open": ("gauge-matter transport link factor (form cov) not integral at kappa = 2^16, "
                                         "P = 2^20; E1 Gauss exact only for a uniform lapse; gauge-link (W/gluon) "
                                         "energy neither reads nor sources the lapse")}
    return out + extra, new_info


def compose_universality(system, *, on: bool = UNIVERSALITY_DEFAULT_ON, **kw):
    """NEW System with the universality candidate (on=True), else ``system`` unchanged."""
    if not on:
        return system
    from .system import System
    blocks, info = universality_blocks(system.Q, list(system.blocks), system.info, **kw)
    return System(system.Q, tuple(blocks), info)


__all__ = ["build_gauge_lapse", "build_photon_lapse", "gauge_lapse_potential", "photon_lapse_potential",
           "rest_coefficient", "universality_mass", "universality_blocks", "compose_universality", "FORMS",
           "GAUGE_GROUPS", "UNIVERSALITY_DEFAULT_ON", "WHY_TEST"]
