"""Stage-1 GRAVITY layer: tensor blocks only (no state, no run, no observation).

Every builder returns a ``core.tensor.Block``. Conventions (NOTES_gravity.md, design summary):

* ONE divisor D = 6Q for every gear; Q ODD. Rule3 identity: 6Q (b' + a) = 2u + r - r'.
* New gears start at (0, 0, r0) with r0 = 3Q - 1 (mid-range; fixed by the parity-preserving reversor R'(r) = D-2-r).
* Deviation form: every term targeting a new gear vanishes when the layer's own gears are 0.
* The potential scale P (U = F/(2P) for the lapse field F) and an integer k give Q = 2Pk + 1, so that every coupling
  coefficient is an integer (``gravity_Q``).
* Reciprocal (force) couplings are written as ONE potential Phi and differentiated by ``gradient_terms`` (u_g =
  dPhi/db_g), so action and reaction come from the same polynomial; deliberately one-way terms carry
  ``{"designated_one_way": "<why>"}``.

Blocks
------
``build_metric``      10 hbar^{mu nu} field gears, ONE headroom stencil u = (Q-1) Sum_6 b + 6b, Yee metadata.
``MatterSpec`` / ``build_matter``   the GENERIC matter interface (on-site mass/clock entries, transport entries) and
                      the matter block it defines (reciprocal by construction); minimal test matter helpers.
``build_lapse``       the ONE universal lapse block (clock factor on on-site entries, link factor on transport entries)
                      + its reciprocal source, from one potential; gamma="1911" is the lapse-only light CONTROL.
``build_beta``        beta = 1 auxiliary G (exact discrete Leibniz) with an optional reciprocal source form; matter's
                      G read designated one-way.
``build_beta_rank4``  OD4 alternative: the second-order clock/light factors as on-site / on-link quartics (reciprocal).
``build_ndesign``     static all-orders N-design (split, detuned remainder gears, density gear), rank 3; OD4 option
                      rank4=True: light weight = A*C instantaneous (on-link quartic).
``build_od2``         OD2: hij F-gears with b-only stress sources + rounding-free h0i, h00 accumulators; matter reads
                      at centred times.
Nothing here is a physical claim; gear names are labels.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Iterable, Sequence

from ..core.tensor import Block, GearType

ZERO = (0, 0, 0)
AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
SIX = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
COMPONENTS = ("h00", "h0x", "h0y", "h0z", "hxx", "hyy", "hzz", "hxy", "hxz", "hyz")
SPATIAL = ("x", "y", "z")


def vacuum_r0(Q: int) -> int:
    """New-layer vacuum remainder r0 = 3Q - 1 (needs odd Q to be fixed by R'(r) = D - 2 - r)."""
    return 3 * Q - 1


def gravity_Q(P: int, k: int) -> int:
    """Q = 2Pk + 1 (odd): the field/light link weight Q - 1 = 2Pk is then divisible by 2P."""
    if type(P) is not int or type(k) is not int or P < 1 or k < 1:
        raise ValueError("P and k must be positive ints")
    return 2 * P * k + 1


def _check_Q(Q):
    if type(Q) is not int or Q < 3 or Q % 2 == 0:
        raise ValueError("Q must be an odd int >= 3 (r0 = 3Q - 1 mirror-fixed needs odd Q)")


def _sub(p, q):
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def _add(p, q):
    return (p[0] + q[0], p[1] + q[1], p[2] + q[2])


def _neg(p):
    return (-p[0], -p[1], -p[2])


def gradient_terms(potential: Iterable, only: Iterable[str] | None = None, signs: dict | None = None,
                   designation: str | None = None, what: str = "") -> list[tuple]:
    """Terms of u_g = s_g dPhi/db_g for Phi = Sum_x Sum_m c_m prod_j b_{g_j}(x + o_j).

    ``potential``: iterable of (c, [(gear, offset), ...]) with c an int or Fraction; offsets of one monomial must lie in
    {0, e} for one face direction (B3, checked later by the Tensor). ``only``: differentiate only with respect to these
    gear names (a one-way read: the other partners are deliberately absent and the terms are designated). Coefficients
    are merged exactly and must be integers (ValueError otherwise, naming the offending entry)."""
    acc: dict = {}
    only_set = None if only is None else set(only)
    for c, mono in potential:
        c = Fraction(c)
        if c == 0:
            continue
        mono = [(g, tuple(o)) for g, o in mono]
        for j, (g, o) in enumerate(mono):
            if only_set is not None and g not in only_set:
                continue
            rest = tuple(sorted((gg, _sub(oo, o)) for i, (gg, oo) in enumerate(mono) if i != j))
            s = 1 if signs is None else signs.get(g, 1)
            key = (g, rest)
            acc[key] = acc.get(key, 0) + s * c
    terms = []
    for (g, rest), c in sorted(acc.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        if c == 0:
            continue
        if c.denominator != 1:
            raise ValueError(f"{what}: non-integer coefficient {c} for target {g!r} with factors {rest}; choose P, k, "
                             "masses as documented (Q - 1 = 2Pk, mass entries in 2P*Z, ...)")
        t = (g, int(c), tuple((gg, o, "b") for gg, o in rest))
        if designation is not None:
            t = t + ({"designated_one_way": designation},)
        terms.append(t)
    return terms


def wave_potential(g: str, w: int, carrier: int) -> list:
    """Phi of the gear g with face weight w and on-site value carrier: u = w Sum_6 b + carrier b."""
    pot = [(Fraction(carrier, 2), [(g, ZERO), (g, ZERO)])]
    for e in AXES:
        pot.append((w, [(g, ZERO), (g, e)]))
    return pot


def headroom_potential(g: str, Q: int) -> list:
    """THE ONE headroom stencil u = (Q-1) Sum_6 b + 6b (c_Q^2 = (Q-1)/(3Q))."""
    return wave_potential(g, Q - 1, 6)


def laplacian_form_potential(g: str, Q: int, w: int) -> list:
    """u = 6Q b + w Lap b = w Sum_6 b + (6Q - 6w) b: a massless gear with face weight w (detuned speed w/(3Q))."""
    return wave_potential(g, w, 6 * Q - 6 * w)


def lap_potential(coeff, target: str, f_mono: Sequence) -> list:
    """Phi monomials of coeff * target(x) * Lap f (x), f = prod of (gear, offset) factors at ONE point (offset 0):
    Lap f(x) = Sum_6 f(x+e) - 6 f(x). Every monomial lives on one link (B3)."""
    pot = []
    for e in SIX:
        pot.append((coeff, [(target, ZERO)] + [(g, _add(o, e)) for g, o in f_mono]))
    pot.append((-6 * Fraction(coeff), [(target, ZERO)] + list(f_mono)))
    return pot


# ====================================================================== 1. metric block
YEE = {"h00": None, "hxx": None, "hyy": None, "hzz": None, "h0x": 0, "h0y": 1, "h0z": 2,
       "hxy": None, "hxz": None, "hyz": None}
PLAQUETTE = {"hxy": (0, 1), "hxz": (0, 2), "hyz": (1, 2)}   # node-stored composites at x + (e_i + e_j)/2


def build_metric(*, Q: int, name: str = "metric", components: Sequence[str] = COMPONENTS, label: str = "audit",
                 r0: int | None = None) -> Block:
    """The 10 hbar^{mu nu} field gears (WS-B W1, board units), each THE ONE headroom stencil
    u = (Q-1) Sum_6 b + 6b, gradient of Phi_wave; c_Q = sqrt((Q-1)/(3Q)).

    Yee placement (metadata): h00, hii node gears; h0i link gears of axis i (stored at the base node); hij (i != j)
    node-stored plaquette composites, physical position x + (e_i + e_j)/2 (PLAQUETTE). Readout label "audit" (OD1).
    Sources are added by the coupling blocks (cross-layer terms targeting "<name>.<component>").
    Vacuum (0, 0, r0), r0 = 3Q - 1 by default."""
    _check_Q(Q)
    r0 = vacuum_r0(Q) if r0 is None else r0
    bad = [c for c in components if c not in COMPONENTS]
    if bad:
        raise ValueError(f"unknown metric components {bad}")
    gears = tuple(GearType(c, label, YEE[c]) for c in components)
    pot = []
    for c in components:
        pot += headroom_potential(c, Q)
    terms = gradient_terms(pot, what="metric")
    return Block(gears, tuple(terms), name=name, vacuum={c: r0 for c in components},
                 params={"Q": Q, "components": tuple(components), "label": label, "r0": r0,
                         "reversor": {c: "Mp" for c in components},
                         "stencil": "u = (Q-1) Sum_6 b + 6 b", "c_Q^2": f"{Q - 1}/{3 * Q}"},
                 doc="10 hbar^{mu nu} headroom F-gears (harmonic gauge, board units), Yee metadata", Q=Q)


# ====================================================================== 2. matter interface
@dataclass(frozen=True)
class MatterSpec:
    """GENERIC matter interface (what the gravity blocks multiply).

    ``name``: namespace of the matter block. ``gears``: local gear names. ``order``: 2 = second-order (KG-type)
    matter, carrier 6Q (b' + a = 2b + ...); 1 = first-order (Dirac-type) matter, carrier 0 (pi/2 carrier).
    ``carrier``: gear -> carrier coefficient (default 6Q for order 2, 0 for order 1; -6Q = a pi-carrier gear).
    ``site``: {(t, s): H_ts} with t <= s, the ON-SITE (mass/clock) entries: Phi_site = Sum_{t<s} H b_t b_s +
    Sum_t H_tt/2 b_t^2 (the lapse's clock factor multiplies exactly these). ``laplacian``: {t: w}: transport
    Phi_link = -(w/2) Sum_axes (b_t(x+e) - b_t(x))^2 (difference form). ``hops``: ((t, s, axis, c), ...):
    Phi_link += c b_t(x) b_s(x + e_axis) (generic link entries, e.g. first-order transport). The link factor of the
    lapse multiplies exactly the transport entries. Matter u = dPhi_m/db with
    Phi_m = Sum_x [carrier/2 b^2 + Phi_site + Phi_link]: reciprocal by construction."""
    name: str
    gears: tuple
    order: int = 2
    carrier: dict = field(default_factory=dict)
    site: dict = field(default_factory=dict)
    laplacian: dict = field(default_factory=dict)
    hops: tuple = ()
    label: str = "official"

    def q(self, g: str) -> str:
        return f"{self.name}.{g}"

    def carrier_of(self, g: str, Q: int) -> int:
        if g in self.carrier:
            return self.carrier[g]
        return 6 * Q if self.order == 2 else 0

    def site_potential(self, qualify: bool = True) -> list:
        nm = self.q if qualify else (lambda g: g)
        pot = []
        for (t, s), H in self.site.items():
            if t == s:
                pot.append((Fraction(H, 2), [(nm(t), ZERO), (nm(t), ZERO)]))
            else:
                pot.append((H, [(nm(t), ZERO), (nm(s), ZERO)]))
        return pot

    def link_potentials(self, qualify: bool = True) -> list:
        """[(axis, [(c, mono), ...]) ...]: the transport potential of ONE link (x, x + e_axis), per axis."""
        nm = self.q if qualify else (lambda g: g)
        out = []
        for ax, e in enumerate(AXES):
            pot = []
            for t, w in self.laplacian.items():
                pot += [(Fraction(-w, 2), [(nm(t), e), (nm(t), e)]), (w, [(nm(t), ZERO), (nm(t), e)]),
                        (Fraction(-w, 2), [(nm(t), ZERO), (nm(t), ZERO)])]
            for t, s, axis, c in self.hops:
                if axis == ax:
                    pot.append((c, [(nm(t), ZERO), (nm(s), e)]))
            if pot:
                out.append((ax, pot))
        return out


def build_matter(spec: MatterSpec, *, Q: int, r0: int | None = None) -> Block:
    """The matter block of a spec: u = dPhi_m/db (reciprocal by construction). Vacuum (0, 0, r0)."""
    _check_Q(Q)
    spec = _resolve_carriers(spec, Q)
    r0 = vacuum_r0(Q) if r0 is None else r0
    pot = []
    for g in spec.gears:
        pot.append((Fraction(spec.carrier_of(g, Q), 2), [(g, ZERO), (g, ZERO)]))
    pot += spec.site_potential(qualify=False)
    for _ax, lp in spec.link_potentials(qualify=False):
        pot += lp
    terms = gradient_terms(pot, what=f"matter {spec.name}")
    return Block(tuple(GearType(g, spec.label) for g in spec.gears), tuple(terms), name=spec.name,
                 vacuum={g: r0 for g in spec.gears},
                 params={"Q": Q, "order": spec.order, "site": dict(spec.site), "laplacian": dict(spec.laplacian),
                         "reversor": {g: "Mp" for g in spec.gears},
                         "hops": tuple(spec.hops), "carrier": {g: spec.carrier_of(g, Q) for g in spec.gears}},
                 doc="matter defined by a MatterSpec (gradient of Phi_m)", Q=Q)


# ---- minimal TEST matter (stage 1 only; the full matter is B1-EM's) --------------------------------------------
def atom_spec(name: str, mu: int, n: int = 1, label: str = "official") -> MatterSpec:
    """n on-site clock gears (no transport): u = 6Q b - mu b, 2 - 2cos w0 = mu/(3Q). Lapse: mu -> mu (1 - 2U)."""
    gears = tuple(f"c{i}" for i in range(n)) if n > 1 else ("c",)
    return MatterSpec(name, gears, 2, {}, {(g, g): -mu for g in gears}, {}, (), label)


def load_pair_spec(name: str, mu: int, anti: bool = False, label: str = "official") -> MatterSpec:
    """A circulating on-site pair (X, Y) of clocks (started in quadrature -> X^2 + Y^2 ~ const: a static source).
    anti=True: pi-carrier pair (carrier -6Q, H = +mu): stable, NEGATIVE source (anti-load used only to cancel the
    closed-board zero mode, as the studies' anti-lump; MECHANISM)."""
    if anti:
        return MatterSpec(name, ("X", "Y"), 2, {"X": "anti", "Y": "anti"}, {("X", "X"): mu, ("Y", "Y"): mu}, {}, (),
                          label)
    return MatterSpec(name, ("X", "Y"), 2, {}, {("X", "X"): -mu, ("Y", "Y"): -mu}, {}, (), label)


def light_spec(name: str, Q: int, label: str = "official") -> MatterSpec:
    """Massless headroom light: u = (Q-1) Sum_6 b + 6b = 6Q b + (Q-1) Lap b (the same stencil as every field gear)."""
    return MatterSpec(name, ("L",), 2, {}, {}, {"L": Q - 1}, (), label)


def kg_spec(name: str, Q: int, mu: int, label: str = "official") -> MatterSpec:
    """Massive KG test matter: u = 6Q b + (Q-1) Lap b - mu b (mu = 6: 'light one tooth short')."""
    return MatterSpec(name, ("K",), 2, {}, {("K", "K"): -mu}, {"K": Q - 1}, (), label)


def weyl_spec(name: str, s: int, m: int = 0, wilson: int = 0, label: str = "official") -> MatterSpec:
    """Minimal FIRST-ORDER test matter (pi/2 carrier): two gears (X, Y), J-hopping on every axis
    Phi_link = s [X(x) Y(x+e) - Y(x) X(x+e)] (u_X = s(Y(x+e) - Y(x-e)), u_Y = -s(X(x+e) - X(x-e))), on-site mass m
    and Wilson term (difference form, weight wilson). Structure test matter for OD2 (not a 3-D Dirac spinor)."""
    hops = []
    for ax in range(3):
        hops += [("X", "Y", ax, s), ("Y", "X", ax, -s)]
    site = {("X", "X"): m, ("Y", "Y"): m} if m else {}
    lap = {"X": wilson, "Y": wilson} if wilson else {}
    return MatterSpec(name, ("X", "Y"), 1, {}, site, lap, tuple(hops), label)


def _resolve_carriers(spec: MatterSpec, Q: int) -> MatterSpec:
    """Replace the symbolic carrier "anti" by -6Q (pi-carrier gear)."""
    car = {g: (-6 * Q if spec.carrier.get(g) == "anti" else spec.carrier[g]) for g in spec.carrier}
    return MatterSpec(spec.name, spec.gears, spec.order, car, spec.site, spec.laplacian, spec.hops, spec.label)


def build_test_matter(spec: MatterSpec, *, Q: int) -> Block:
    return build_matter(_resolve_carriers(spec, Q), Q=Q)


# ====================================================================== 3. universal lapse block
def lapse_factors(order: int, gamma: str) -> tuple[Fraction, Fraction]:
    """(c_site, c_link) of Phi_int = -c_site (F/P) Phi_site - c_link ((F_x + F_y)/P) Phi_link.
    order 2: clock 1 - 2U, links 1 - 4U (GR) or 1 - 2U (1911); order 1: half of each (N, N/psi^2)."""
    if order not in (1, 2):
        raise ValueError("matter order must be 1 or 2")
    if gamma not in ("GR", "1911"):
        raise ValueError("gamma must be 'GR' (gamma = 1) or '1911' (lapse-only light control)")
    c_site = Fraction(1) if order == 2 else Fraction(1, 2)
    c_link = c_site if gamma == "GR" else c_site / 2
    return c_site, c_link


def lapse_potential(F: str, P: int, matters: Sequence[MatterSpec], gamma: str = "GR") -> list:
    pot = []
    for spec in matters:
        c_site, c_link = lapse_factors(spec.order, gamma)
        for c, mono in spec.site_potential():
            pot.append((-c_site * Fraction(c) / P, [(F, ZERO)] + mono))
        for ax, lp in spec.link_potentials():
            e = AXES[ax]
            for c, mono in lp:
                pot.append((-c_link * Fraction(c) / P, [(F, ZERO)] + mono))
                pot.append((-c_link * Fraction(c) / P, [(F, e)] + mono))
    return pot


def build_lapse(*, Q: int, P: int, field: str, matters: Sequence[MatterSpec], gamma: str = "GR",
                name: str = "lapse") -> Block:
    """THE ONE UNIVERSAL LAPSE BLOCK (equivalence principle), from ONE potential

        Phi_int = Sum_species [ -c_site (F/P) Phi_site  -  c_link Sum_links ((F(x) + F(x+e))/P) Phi_link ],

    U := F/(2P). Action (metric x matter -> matter): every species' on-site (mass/clock) entries get the clock factor
    (1 - 2U for second-order matter, 1 - U for first-order), its transport entries the link factor (1 - 4U / 1 - 2U for
    gamma = 1). Source (matter x matter -> metric): dPhi_int/dF = the on-site mass energy -Phi_site/P plus the link
    gradient energy, i.e. the reaction of the SAME potential: Newton III exact, no designation.
    gamma="1911": lapse-only light CONTROL (link factor = clock factor). ``field``: qualified lapse gear (e.g.
    "metric.h00"). The block owns no gear; all its terms are cross-layer. Integrality: mass entries in 2P*Z (on-site
    diagonal), transport weights in 2P*Z (e.g. Q - 1 = 2Pk) for second-order matter, 4P*Z for first-order matter
    (half factors); otherwise ValueError naming the entry."""
    _check_Q(Q)
    pot = lapse_potential(field, P, [_resolve_carriers(m, Q) for m in matters], gamma)
    terms = gradient_terms(pot, what="lapse")
    return Block((), tuple(terms), name=name, vacuum={},
                 params={"Q": Q, "P": P, "field": field, "gamma": gamma,
                         "matters": tuple((m.name, m.order) for m in matters)},
                 doc="universal lapse: clock factor on on-site entries, link factor on transport entries; reciprocal",
                 Q=Q)


# ====================================================================== 4. beta = 1 (G auxiliary) and its OD4 form
G_READ_WHY = ("beta=1 auxiliary G read by matter (clock factor +G/P, link factor +(17/8)(G_x+G_y)/P): a reciprocal "
              "partner would source G with the matter energy, giving G = F^2/(2P) - F at FIRST order and destroying "
              "the lapse; no rank-3 reciprocal form exists (the reciprocal equivalent is the OD4 quartic, "
              "build_beta_rank4)")
G_SOURCE_WHY = ("beta=1 auxiliary G sourced by -k Lap(F^2) (exact discrete Leibniz) with F not reading G: the agreed "
                "S1 X1 form (one-way); its reciprocal completion is reciprocal_source=True")


def beta_matter_factors(order: int) -> tuple[Fraction, Fraction]:
    """Second-order coefficients (site, per-link-endpoint) of G/P: order 2: N^2 += 2U^2 = G/P (site), lambda +=
    (17/2)U^2 = (17/8)(G_x + G_y)/P; order 1: N += U^2/2 = G/(4P), N/psi^2 += (9/4)U^2 = (9/16)(G_x + G_y)/P."""
    return (Fraction(1), Fraction(17, 8)) if order == 2 else (Fraction(1, 4), Fraction(9, 16))


def build_beta(*, Q: int, P: int, k: int, field: str, matters: Sequence[MatterSpec] = (),
               reciprocal_source: bool = False, name: str = "beta", gear: str = "G", r0: int | None = None) -> Block:
    """beta = 1 auxiliary gear G (S1 X1): headroom stencil + source -k Lap(F^2), Q - 1 = 2Pk, so that the static law is
    G = F^2/(2P) exactly (discrete Leibniz). Potential Phi_G = -k Sum_x G(x) Lap(F^2)(x).
    reciprocal_source=False (DEFAULT, manager ruling 10:2x): the agreed one-way source (designated G_SOURCE_WHY).
    reciprocal_source=True: both derivatives (G's source AND F's back-reaction -2k F Lap G; static exterior changed
    only at O(U^3)) - exact and reciprocal, but DYNAMICALLY UNSTABLE with the ONE headroom stencil (finding F1: the
    coupled F-G fast speed c^2 (1 + F/P) exceeds the CFL bound, headroom 1/(3Q)); kept as an option for audit only.
    Matter reads G (second-order clock/light factors, ``beta_matter_factors``): designated one-way (G_READ_WHY)."""
    _check_Q(Q)
    if Q - 1 != 2 * P * k:
        raise ValueError("build_beta needs Q - 1 = 2Pk")
    r0 = vacuum_r0(Q) if r0 is None else r0
    gq = f"{name}.{gear}"
    terms = gradient_terms(headroom_potential(gear, Q), what="beta wave")
    src_pot = lap_potential(Fraction(-k), gq, [(field, ZERO), (field, ZERO)])
    if reciprocal_source:
        terms += gradient_terms(src_pot, what="beta source")
    else:
        terms += gradient_terms(src_pot, only=[gq], designation=G_SOURCE_WHY, what="beta source")
    read = []
    for spec in matters:
        spec = _resolve_carriers(spec, Q)
        c_site, c_link = beta_matter_factors(spec.order)
        for c, mono in spec.site_potential():
            read.append((c_site * Fraction(c) / P, [(gq, ZERO)] + mono))
        for ax, lp in spec.link_potentials():
            e = AXES[ax]
            for c, mono in lp:
                read.append((c_link * Fraction(c) / P, [(gq, ZERO)] + mono))
                read.append((c_link * Fraction(c) / P, [(gq, e)] + mono))
    mgears = [spec.q(g) for spec in matters for g in spec.gears]
    terms += gradient_terms(read, only=mgears, designation=G_READ_WHY, what="beta matter read")
    return Block((GearType(gear, "audit"),), tuple(terms), name=name, vacuum={gear: r0},
                 params={"Q": Q, "P": P, "k": k, "field": field, "reciprocal_source": reciprocal_source,
                         "reversor": {gear: "Mp"},
                         "matters": tuple(m.name for m in matters)},
                 doc="beta = 1 auxiliary G = F^2/(2P) by the exact discrete Leibniz identity", Q=Q)


def build_beta_rank4(*, Q: int, P: int, field: str, matters: Sequence[MatterSpec], name: str = "beta4") -> Block:
    """OD4 (rank 4) RECIPROCAL beta = 1: no G gear; the U^2 parts of the clock and light factors are on-site / on-link
    quartics of ONE potential: Phi += c2_site (F^2/P^2) Phi_site + c2_link (F_x F_y/P^2) Phi_link (order 2: 1/2 and
    17/8; order 1: 1/8 and 9/16), the link factor taken as Fbar^2 = ((F_x + F_y)/2)^2. OD4 decomposition (manager rule):
    site: -(mu/4P^2) (F b)^2 = -lambda q^2, q = F b (for a general symmetric -H >= 0: -(1/2) sum_k h_k (F v_k.b)^2);
    link: -(17 w/16P^2) (Fbar (b_y - b_x))^2; each on one node / one link, minus sign, negative semi-definite.
    Their F-derivative is the GR source weight (1 - 2U) ('-8 pi rho U'). Integrality: mass entries in 2P^2*Z and
    transport weights in 64P^2*Z (e.g. Q - 1 = 64 P^2 k)."""
    _check_Q(Q)
    pot = []
    for spec in matters:
        spec = _resolve_carriers(spec, Q)
        c2s = Fraction(1, 2) if spec.order == 2 else Fraction(1, 8)
        c2l = Fraction(17, 8) if spec.order == 2 else Fraction(9, 16)
        for c, mono in spec.site_potential():
            pot.append((c2s * Fraction(c) / P ** 2, [(field, ZERO), (field, ZERO)] + mono))
        for ax, lp in spec.link_potentials():
            e = AXES[ax]
            for c, mono in lp:
                # ((F_x + F_y)/2)^2 Phi_link: with Phi_link = -(w/2)(delta b)^2 this is -lambda q^2, q = Fbar delta b
                # (OD4: on one link, minus sign, negative semi-definite); F_x F_y alone would be an indefinite cross-quartic
                for f1, f2, wgt in ((ZERO, ZERO, Fraction(1, 4)), (ZERO, e, Fraction(1, 2)), (e, e, Fraction(1, 4))):
                    pot.append((wgt * c2l * Fraction(c) / P ** 2, [(field, f1), (field, f2)] + mono))
    terms = gradient_terms(pot, what="beta rank4")
    return Block((), tuple(terms), name=name, vacuum={},
                 params={"Q": Q, "P": P, "field": field, "matters": tuple(m.name for m in matters)},
                 doc="OD4 reciprocal beta = 1 quartics (on-site / on-link)", Q=Q)


# ====================================================================== 5. N-design (static, all orders)
ND_SELF_WHY = ("N-design self law (1+N) Lap N = Sum_e (delta_e N)^2 (lattice form of (1+N) Lap N = 2|grad N|^2): the "
               "Euler-Lagrange equation of the NON-polynomial potential |grad psi|^2, psi = 2/(1+N); no polynomial "
               "(rank <= 4) potential reproduces it")
ND_AUX_WHY = ("N-design auxiliary (a2, crem, lamrem): static law by the exact discrete Leibniz identity, feed-forward "
              "chain from N (one-way by construction, S1 X5/X11)")
ND_SRC_WHY = ("N-design York-weighted source -sigma n C from the prescribed static density gear n (MECHANISM, S1-M2 "
              "Y4); n does not feel N (a static prescribed load)")
ND_READ_WHY = ("N-design metric read by test clocks (A = 1 + 2 eps + a2) and test light (lambda = 1 + 4 eps + lamrem, "
               "or A*C at rank 4): test bodies of the static vacuum construction (one-way; a reciprocal read would "
               "source the auxiliaries with matter energy, as for G). OD4 status of the rank-4 A*C light weight: its "
               "quartics (nu_x nu_y, nu crem, a2 crem, a2 nu times (delta b)^2) are INDEFINITE cross-quartics, not "
               "-lambda q^2 springs; they are kept only as designated one-way test-light reads")


def build_ndesign(*, Q: int, P: int, k: int, sigma0: int, w_a2: int, w_c: int, w_lam: int | None = None,
                  clocks: Sequence[MatterSpec] = (), lights: Sequence[MatterSpec] = (), rank4: bool = False,
                  name: str = "nd", r0: int | None = None) -> Block:
    """Static all-orders N-design (S1 X5, X10, X11, Y15), split form with detuned remainder gears.

    Gears (deviation form, scale P): nu = P(N - 1); a2 = P eps^2 (eps = N - 1); crem = P Crem with
    C := (1+N)^4/16 = (1 + eps + a2/4)^2 = 1 + 2 eps + Crem; lamrem = P (lambda - 1 - 4 eps) with lambda = A C,
    A = 1 + 2 eps + a2 (omitted when rank4); n = prescribed static density (u = 6Q n: holds its initial value).
    nu: u = 6Q nu + (Q-1) Lap nu + k Sum_e [3 nu nu_e - 2 nu^2 - nu_e^2] - sigma0 P n C, i.e. static
    k P^2 [(1+N) Lap N - Sum_e (delta_e N)^2] = sigma0 P n C (York weight). Remainders: Laplacian-form gears with
    face weights w_a2, w_c, w_lam (DETUNED speeds w/(3Q); Y15) and Leibniz sources (exact static laws).
    Clocks read A on their on-site entries; lights read lambda (rank 3) or A*C (rank4=True: on-link quartic, OD4).
    All reads/sources are one-way (designated, see ND_*_WHY)."""
    _check_Q(Q)
    if Q - 1 != 2 * P * k:
        raise ValueError("build_ndesign needs Q - 1 = 2Pk")
    r0 = vacuum_r0(Q) if r0 is None else r0
    q = lambda g: f"{name}.{g}"
    nu, a2, cr, lr, n = q("nu"), q("a2"), q("crem"), q("lamrem"), q("n")
    gears = ["nu", "a2", "crem"] + ([] if rank4 else ["lamrem"]) + ["n"]
    terms = []
    # nu: wave part (reciprocal: headroom stencil), self law (designated), York source (designated)
    terms += gradient_terms(headroom_potential("nu", Q), what="nd nu wave")
    # nu * Lap-type self law: k [ nu Lap nu - Sum (d nu)^2 ] = k Sum_e [3 nu nu_e - 2 nu^2 - nu_e^2]
    self_terms = []
    for e in SIX:
        self_terms.append(("nu", 3 * k, (("nu", ZERO, "b"), ("nu", e, "b"))))
        self_terms.append(("nu", -2 * k, (("nu", ZERO, "b"), ("nu", ZERO, "b"))))
        self_terms.append(("nu", -k, (("nu", e, "b"), ("nu", e, "b"))))
    terms += [t + ({"designated_one_way": ND_SELF_WHY},) for t in self_terms]
    # York source: -sigma0 P n C = -sigma0 (P n + 2 n nu + n crem)
    terms += [("nu", -sigma0 * P, (("n", ZERO, "b"),), {"designated_one_way": ND_SRC_WHY}),
              ("nu", -2 * sigma0, (("n", ZERO, "b"), ("nu", ZERO, "b")), {"designated_one_way": ND_SRC_WHY}),
              ("nu", -sigma0, (("n", ZERO, "b"), ("crem", ZERO, "b")), {"designated_one_way": ND_SRC_WHY})]
    # density gear: free, holds its value
    terms += gradient_terms(wave_potential("n", 0, 6 * Q), what="nd n")

    def aux(gname, w, target_poly):
        """Laplacian-form remainder gear with static law gear = target_poly (P units): source -w Lap(target)."""
        out = gradient_terms(laplacian_form_potential(gname, Q, w), what=f"nd {gname} wave")
        pot = []
        for c, mono in target_poly:
            pot += lap_potential(-Fraction(w) * Fraction(c), "__T__", mono)
        src = []
        for c, mono in pot:
            rest = [(g, o, "b") for g, o in mono if g != "__T__"]
            if Fraction(c).denominator != 1:
                raise ValueError(f"nd {gname}: non-integer source coefficient {c}; choose weights in 16P*Z")
            src.append((gname, int(c), tuple(rest), {"designated_one_way": ND_AUX_WHY}))
        return out + src

    # a2 = nu^2 / P
    terms += aux("a2", w_a2, [(Fraction(1, P), [("nu", ZERO), ("nu", ZERO)])])
    # crem (P units) = nu^2/P + a2/2 + nu a2/(2P) + a2^2/(16P)
    terms += aux("crem", w_c, [(Fraction(1, P), [("nu", ZERO), ("nu", ZERO)]), (Fraction(1, 2), [("a2", ZERO)]),
                               (Fraction(1, 2 * P), [("nu", ZERO), ("a2", ZERO)]),
                               (Fraction(1, 16 * P), [("a2", ZERO), ("a2", ZERO)])])
    if not rank4:
        if w_lam is None:
            raise ValueError("w_lam needed unless rank4")
        # lamrem (P units) = 4 nu^2/P + a2 + crem + 2 nu a2/P + 2 nu crem/P + a2 crem/P
        terms += aux("lamrem", w_lam, [(Fraction(4, P), [("nu", ZERO), ("nu", ZERO)]), (1, [("a2", ZERO)]),
                                       (1, [("crem", ZERO)]), (Fraction(2, P), [("nu", ZERO), ("a2", ZERO)]),
                                       (Fraction(2, P), [("nu", ZERO), ("crem", ZERO)]),
                                       (Fraction(1, P), [("a2", ZERO), ("crem", ZERO)])])
    # reads (one-way, designated)
    read = []
    for spec in clocks:
        spec = _resolve_carriers(spec, Q)
        csite = Fraction(1) if spec.order == 2 else Fraction(1, 2)
        for c, mono in spec.site_potential():
            # (A - 1) Phi_site, A - 1 = 2 nu/P + a2/P  (order 1: sqrt(A) - 1 ~ (A - 1)/2 at first order only)
            read.append((csite * 2 * Fraction(c) / P, [(nu, ZERO)] + mono))
            read.append((csite * Fraction(c) / P, [(a2, ZERO)] + mono))
    for spec in lights:
        spec = _resolve_carriers(spec, Q)
        for ax, lp in spec.link_potentials():
            e = AXES[ax]
            for c, mono in lp:
                c = Fraction(c)
                if not rank4:
                    # (lambda_link - 1) Phi_link with lambda_link = 1 + 2(nu_x+nu_y)/P + (lam_x+lam_y)/(2P)
                    for o in (ZERO, e):
                        read.append((2 * c / P, [(nu, o)] + mono))
                        read.append((c / (2 * P), [(lr, o)] + mono))
                else:
                    # lambda_link = (A_x C_y + A_y C_x)/2, A = 1 + 2eps + a2, C = 1 + 2eps + crem (P units)
                    for o in (ZERO, e):
                        read.append((2 * c / P, [(nu, o)] + mono))
                        read.append((c / (2 * P), [(cr, o)] + mono))
                        read.append((c / (2 * P), [(a2, o)] + mono))
                    read.append((4 * c / P ** 2, [(nu, ZERO), (nu, e)] + mono))
                    read.append((c / P ** 2, [(nu, ZERO), (cr, e)] + mono))
                    read.append((c / P ** 2, [(nu, e), (cr, ZERO)] + mono))
                    read.append((c / P ** 2, [(a2, ZERO), (nu, e)] + mono))
                    read.append((c / P ** 2, [(a2, e), (nu, ZERO)] + mono))
                    read.append((c / (2 * P ** 2), [(a2, ZERO), (cr, e)] + mono))
                    read.append((c / (2 * P ** 2), [(a2, e), (cr, ZERO)] + mono))
    mgears = [spec.q(g) for spec in list(clocks) + list(lights) for g in spec.gears]
    terms += gradient_terms(read, only=mgears, designation=ND_READ_WHY, what="nd reads")
    return Block(tuple(GearType(g, "audit") for g in gears), tuple(terms), name=name, vacuum={g: r0 for g in gears},
                 params={"Q": Q, "P": P, "k": k, "sigma0": sigma0, "w_a2": w_a2, "w_c": w_c, "w_lam": w_lam,
                         "reversor": {g: "Mp" for g in gears},
                         "rank4": rank4, "clocks": tuple(m.name for m in clocks),
                         "lights": tuple(m.name for m in lights)},
                 doc="static all-orders N-design (split, detuned remainders); OD4 option rank4", Q=Q)


# ====================================================================== 6. OD2: accumulators + b-only stress sources
OD2_READ_WHY = ("OD2 centred read of the accumulator metric by matter: the accumulators are slaved to the harmonic "
                "constants (rounding-free input K = 0 mod D); a reciprocal matter source on them would break the "
                "exact momentum constraints (S4 A8/B8); the physical source enters through the hij stress")
OD2_ACC_WHY = ("OD2 accumulator (S4 A8/B8): a slaved gear integrating the harmonic condition exactly, "
               "D_t h0i = -Div_i hbar (h00: D_t h00 = -Div_0 h0); its b-reads are the integration, not a force, and "
               "have no partner (hij and h0i do not read the accumulators at single time)")
OD2_STRESS_WHY = ("OD2 b-only first-order stress source of hij (S4 B8, P-vii(c)): the matter does not read hij "
                  "back at single time (its hij coupling, if any, is a separate block)")


def _div_spatial_terms(target: str, comp_of, i: int, field: str, coeff: int) -> list:
    """coeff * Div_i X (field 'a' or 'b') at the link (x, x + e_i):
    Div_i = [X^{ii}(x + e_i) - X^{ii}(x)] + Sum_{j != i} [X^{ji}(x) - X^{ji}(x - e_j)] (Yee: X^{ii} on nodes,
    X^{ji} on plaquettes stored at x)."""
    out = [(target, coeff, ((comp_of(i, i), AXES[i], field),)), (target, -coeff, ((comp_of(i, i), ZERO, field),))]
    for j in range(3):
        if j != i:
            out.append((target, coeff, ((comp_of(j, i), ZERO, field),)))
            out.append((target, -coeff, ((comp_of(j, i), _neg(AXES[j]), field),)))
    return out


def comp_name(i: int, j: int) -> str:
    a, b = sorted((i, j))
    return "h" + SPATIAL[a] + SPATIAL[b]


def build_od2(*, Q: int, name: str = "od2", stress: Sequence[tuple] = (), reads: Sequence[tuple] = (),
              label: str = "audit", r0: int | None = None) -> Block:
    """OD2 build (S4 A8, B8, C1, P-vi, P-vii(c)): 6 hij F-gears (headroom stencil) + 3 h0i (link gears) and h00
    ACCUMULATORS, read at centred times; NO remainder-reading input.

    h0i: u = D b - (D/2)[Div_i(hbar(t)) - Div_i(hbar(t-1))] (reads hij's a): K = 2u = 0 mod D, so r never changes
         and C^i(t) = h0i(t+1) - h0i(t) + Div_i(t) is EXACTLY constant (Div_i: ``_div_spatial_terms``).
    h00: u = D b - (D/2)[Div_0(t) - Div_0(t-1)], Div_0 = Sum_i [h0i(x) - h0i(x - e_i)] (reads h0i's a):
         C^0(t) = h00(t+1) - h00(t) + Div_0(t) EXACTLY constant.
    ``stress``: extra b-only source terms (target local hij name, coeff, factors) from the matter (designated
    one-way, OD2_STRESS_WHY). ``reads``: matter terms reading the accumulators at centred times (two-time reads), e.g.
    from ``od2_centred_lapse_read``. Acyclic: hij (stage 0) -> h0i -> h00 -> matter."""
    _check_Q(Q)
    r0 = vacuum_r0(Q) if r0 is None else r0
    D = 6 * Q
    hij = [comp_name(i, j) for i in range(3) for j in range(i, 3)]
    gears = [GearType(c, label, None) for c in hij] + [GearType(f"h0{SPATIAL[i]}", label, i) for i in range(3)] + \
            [GearType("h00", label, None)]
    terms = []
    for c in hij:
        terms += gradient_terms(headroom_potential(c, Q), what="od2 hij")
    acc = {"designated_one_way": OD2_ACC_WHY}
    for i in range(3):
        t = f"h0{SPATIAL[i]}"
        terms.append((t, D, ((t, ZERO, "b"),)))
        terms += [x + (acc,) for x in _div_spatial_terms(t, comp_name, i, "b", -(D // 2))]
        terms += _div_spatial_terms(t, comp_name, i, "a", D // 2)
    for i in range(3):
        h0 = f"h0{SPATIAL[i]}"
        for fld, sg in (("b", -1), ("a", 1)):
            for x in [("h00", sg * (D // 2), ((h0, ZERO, fld),)), ("h00", -sg * (D // 2), ((h0, _neg(AXES[i]), fld),))]:
                terms.append(x + (acc,) if fld == "b" else x)
    terms.append(("h00", D, (("h00", ZERO, "b"),)))
    for t in stress:
        terms.append(tuple(t[:3]) + ({"designated_one_way": OD2_STRESS_WHY},))
    for t in reads:
        terms.append(tuple(t))
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: r0 for g in gears},
                 params={"Q": Q, "label": label, "n_stress": len(stress), "n_reads": len(reads),
                         "reversor_staggered": "observe.gravity.od2_staggered_reversor (hij Mp/M; h0i (a,b) -> "
                                               "(-h0i(t+1), -b); h00 (a,b) -> (h00(t+2), h00(t+1)); r kept)"},
                 doc="OD2: hij F-gears + rounding-free h0i, h00 accumulators (exact harmonic constants)", Q=Q)


def od2_lookahead_h00(ns: str) -> list:
    """h00(t+1) as a linear form of the snapshot (b, a): 2 b_h00 - a_h00 - [Div_0(b) - Div_0(a)]: list of
    (coeff, (gear, offset, field))."""
    q = lambda g: f"{ns}.{g}"
    out = [(2, (q("h00"), ZERO, "b")), (-1, (q("h00"), ZERO, "a"))]
    for i in range(3):
        h0 = q(f"h0{SPATIAL[i]}")
        out += [(-1, (h0, ZERO, "b")), (1, (h0, _neg(AXES[i]), "b")), (1, (h0, ZERO, "a")),
                (-1, (h0, _neg(AXES[i]), "a"))]
    return out


def od2_centred_lapse_read(ns: str, spec: MatterSpec, P: int, Q: int, g00: int = 1) -> list:
    """Matter terms reading h00 one step AHEAD (centred, S4-M M_grav_mirror: 'g00 * h00_next * mass b'):
    u_t += g00 * h00(t+1) * (H b)_t / P on the on-site entries; two-time reads (designated one-way, OD2_READ_WHY)."""
    spec = _resolve_carriers(spec, Q)
    out = []
    for (t, s), H in spec.site.items():
        pairs = [(t, s)] if t == s else [(t, s), (s, t)]
        for tt, ss in pairs:
            for c, f in od2_lookahead_h00(ns):
                coeff = Fraction(g00 * c * H, P)
                if coeff.denominator != 1:
                    raise ValueError("od2 read: H*g00 must be divisible by P")
                out.append((spec.q(tt), int(coeff), (f, (spec.q(ss), ZERO, "b")),
                            {"designated_one_way": OD2_READ_WHY}))
    return out


def od2_hop_stress(ns: str, spec: MatterSpec, kappa: int) -> list:
    """b-only first-order (link-local) stress sources of hij from the matter's hop entries (generic interface):
    s^{jj}(x) += kappa * Sum_{hops on axis j} c b_t(x) b_s(x + e_j);
    s^{ij}(x) += kappa * [hop bilinear on axis i + hop bilinear on axis j] / 2 (i != j). Integer kappa (even for
    i != j terms with odd c)."""
    out = []
    for i in range(3):
        for j in range(i, 3):
            comp = f"{comp_name(i, j)}"
            for (t, s, ax, c) in spec.hops:
                if ax not in (i, j):
                    continue
                coeff = Fraction(kappa * c, 1 if i == j else 2)
                if coeff.denominator != 1:
                    raise ValueError("od2 stress: kappa * c must be even for off-diagonal components")
                out.append((comp, int(coeff), ((spec.q(t), ZERO, "b"), (spec.q(s), AXES[ax], "b"))))
    return out


def spec_from_block(block: Block, *, Q: int, order: int, carrier: dict | None = None,
                    laplacian: dict | None = None, label: str | None = None) -> MatterSpec:
    """GENERIC interface extraction: the MatterSpec of ANY linear, reciprocal matter block (e.g. a later B1-EM block).

    Its degree-1 monomials are classified: on-site factors -> the on-site (mass/clock) entries H_ts (the declared
    carrier and the declared difference-form transport diagonal -6w are removed from the diagonal); face-offset factors
    -> transport entries (difference-form weights ``laplacian`` {gear: w} are recognised, every other face entry
    becomes a generic hop c b_t(x) b_s(x + e) on the positive axis). Raises if the block has non-linear terms or is not
    reciprocal (the lapse multiplies a POTENTIAL, so the matter must have one)."""
    carrier = dict(carrier or {})
    laplacian = dict(laplacian or {})
    gears = tuple(g.name for g in block.gears)
    gset = set(gears)
    site: dict = {}
    hops = {}
    face = {}
    for t in block.terms:
        target, c, factors = t[0], t[1], t[2]
        if target not in gset:
            continue
        if len(factors) != 1 or factors[0][2] != "b" or factors[0][0] not in gset:
            raise ValueError(f"spec_from_block: only linear b-only matter is supported, got {t!r}")
        s, off = factors[0][0], tuple(factors[0][1])
        if off == ZERO:
            site[(target, s)] = site.get((target, s), 0) + c
        else:
            face[(target, s, off)] = face.get((target, s, off), 0) + c
    for g in gears:
        c0 = carrier.get(g, 6 * Q if order == 2 else 0)
        site[(g, g)] = site.get((g, g), 0) - c0 + 6 * laplacian.get(g, 0)
    for (t, s, off), c in face.items():
        partner = face.get((s, t, _neg(off)), None)
        if partner != c:
            raise ValueError(f"spec_from_block: face entry {(t, s, off)} has no reciprocal partner")
        if t == s and laplacian.get(t, 0):
            if c != laplacian[t]:
                raise ValueError(f"spec_from_block: face weight of {t} is {c}, declared laplacian {laplacian[t]}")
            continue
        if off in AXES:
            hops[(t, s, AXES.index(off))] = c
    sym = {}
    for (t, s), H in site.items():
        if site.get((s, t), 0) != H:
            raise ValueError(f"spec_from_block: on-site entries ({t},{s}) not symmetric")
        a, b = sorted((t, s))
        if H:
            sym[(a, b)] = H
    return MatterSpec(block.name, gears, order, carrier, sym, laplacian,
                      tuple((t, s, ax, c) for (t, s, ax), c in sorted(hops.items())),
                      label if label is not None else (block.gears[0].label if block.gears else "official"))


STATIC_LOAD_WHY = ("MECHANISM: prescribed static load (a density gear holding its value, u = 6Q n) sourcing the lapse "
                   "field with coeff*n^2 without feeling it (as the studies' design (B) load rotors); a reciprocal "
                   "self-gravitating load of clock pairs collapses at U(0) ~ 0.3 (NOTES_gravity F3)")


def build_static_load(*, Q: int, field: str, coeff: int = 1, name: str = "sload", r0: int | None = None) -> Block:
    """Prescribed static load (MECHANISM, designated one-way): gear n with u = 6Q n (holds a = b = n) and the lapse
    source u_F += coeff * n^2 (coeff < 0: an anti-load). Not a force block: the load does not feel F."""
    _check_Q(Q)
    r0 = vacuum_r0(Q) if r0 is None else r0
    terms = gradient_terms(wave_potential("n", 0, 6 * Q), what="static load")
    terms.append((field, coeff, ((f"{name}.n", ZERO, "b"), (f"{name}.n", ZERO, "b")),
                  {"designated_one_way": STATIC_LOAD_WHY}))
    return Block((GearType("n", "audit"),), tuple(terms), name=name, vacuum={"n": r0},
                 params={"Q": Q, "field": field, "coeff": coeff, "reversor": {"n": "Mp"}},
                 doc="prescribed static load (MECHANISM)", Q=Q)
