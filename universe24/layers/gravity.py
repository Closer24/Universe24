"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Iterable, Sequence
from ..core.tensor import Block, GearType
ZERO = (0, 0, 0)
AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
SIX = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
COMPONENTS = ('h00', 'h0x', 'h0y', 'h0z', 'hxx', 'hyy', 'hzz', 'hxy', 'hxz', 'hyz')
SPATIAL = ('x', 'y', 'z')

def vacuum_r0() -> int:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    return 2

def _sub(p, q):
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])

def _add(p, q):
    return (p[0] + q[0], p[1] + q[1], p[2] + q[2])

def _neg(p):
    return (-p[0], -p[1], -p[2])

def gradient_terms(potential: Iterable, only: Iterable[str] | None=None, signs: dict | None=None, designation: str | None=None, what: str='') -> list[tuple]:
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
            rest = tuple(sorted(((gg, _sub(oo, o)) for i, (gg, oo) in enumerate(mono) if i != j)))
            s = 1 if signs is None else signs.get(g, 1)
            key = (g, rest)
            acc[key] = acc.get(key, 0) + s * c
    terms = []
    for (g, rest), c in sorted(acc.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        if c == 0:
            continue
        if c.denominator != 1:
            raise ValueError(f'{what}: non-integer coefficient {c} for target {g!r} with factors {rest}Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.')
        t = (g, int(c), tuple(((gg, o, 'b') for gg, o in rest)))
        if designation is not None:
            t = t + ({'designated_one_way': designation},)
        terms.append(t)
    return terms

def wave_potential(g: str, w: int, carrier: int) -> list:
    """Phi of the gear g with face weight w and on-site value carrier: u = w Sum_6 b + carrier b."""
    pot = [(Fraction(carrier, 2), [(g, ZERO), (g, ZERO)])]
    for e in AXES:
        pot.append((w, [(g, ZERO), (g, e)]))
    return pot

def headroom_potential(g: str) -> list:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    return wave_potential(g, 0, 6)

def laplacian_form_potential(g: str, w: int) -> list:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    return wave_potential(g, w, 6 - 6 * w)

def lap_potential(coeff, target: str, f_mono: Sequence) -> list:
    """Phi monomials of coeff * target(x) * Lap f (x), f = prod of (gear, offset) factors at ONE point (offset 0):
    Lap f(x) = Sum_6 f(x+e) - 6 f(x). Every monomial lives on one link (B3)."""
    pot = []
    for e in SIX:
        pot.append((coeff, [(target, ZERO)] + [(g, _add(o, e)) for g, o in f_mono]))
    pot.append((-6 * Fraction(coeff), [(target, ZERO)] + list(f_mono)))
    return pot
YEE = {'h00': None, 'hxx': None, 'hyy': None, 'hzz': None, 'h0x': 0, 'h0y': 1, 'h0z': 2, 'hxy': None, 'hxz': None, 'hyz': None}
PLAQUETTE = {'hxy': (0, 1), 'hxz': (0, 2), 'hyz': (1, 2)}

def build_metric(*, name: str='metric', components: Sequence[str]=COMPONENTS, label: str='audit', r0: int | None=None) -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    r0 = vacuum_r0() if r0 is None else r0
    bad = [c for c in components if c not in COMPONENTS]
    if bad:
        raise ValueError(f'unknown metric components {bad}')
    gears = tuple((GearType(c, label, YEE[c]) for c in components))
    pot = []
    for c in components:
        pot += headroom_potential(c)
    terms = gradient_terms(pot, what='metric')
    return Block(gears, tuple(terms), name=name, vacuum={c: r0 for c in components}, params={'components': tuple(components), 'label': label, 'r0': r0, 'reversor': {c: 'Mp' for c in components}, 'spatial_wave_speed_squared': '0', 'stencil': 'u=6*b; spatial weight zero', 'physical_status': 'inertial components only, no propagating metric derived'}, doc='Ten inertial field components with Yee storage metadata; no gravitational dynamics derived')

@dataclass(frozen=True)
class MatterSpec:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    name: str
    gears: tuple
    order: int = 2
    carrier: dict = field(default_factory=dict)
    site: dict = field(default_factory=dict)
    laplacian: dict = field(default_factory=dict)
    hops: tuple = ()
    label: str = 'official'

    def q(self, g: str) -> str:
        return f'{self.name}.{g}'

    def carrier_of(self, g: str) -> int:
        if g in self.carrier:
            return self.carrier[g]
        return 6 if self.order == 2 else 0

    def site_potential(self, qualify: bool=True) -> list:
        nm = self.q if qualify else lambda g: g
        pot = []
        for (t, s), H in self.site.items():
            if t == s:
                pot.append((Fraction(H, 2), [(nm(t), ZERO), (nm(t), ZERO)]))
            else:
                pot.append((H, [(nm(t), ZERO), (nm(s), ZERO)]))
        return pot

    def link_potentials(self, qualify: bool=True) -> list:
        """[(axis, [(c, mono), ...]) ...]: the transport potential of ONE link (x, x + e_axis), per axis."""
        nm = self.q if qualify else lambda g: g
        out = []
        for ax, e in enumerate(AXES):
            pot = []
            for t, w in self.laplacian.items():
                pot += [(Fraction(-w, 2), [(nm(t), e), (nm(t), e)]), (w, [(nm(t), ZERO), (nm(t), e)]), (Fraction(-w, 2), [(nm(t), ZERO), (nm(t), ZERO)])]
            for t, s, axis, c in self.hops:
                if axis == ax:
                    pot.append((c, [(nm(t), ZERO), (nm(s), e)]))
            if pot:
                out.append((ax, pot))
        return out

def build_matter(spec: MatterSpec, *, r0: int | None=None) -> Block:
    """The matter block of a spec: u = dPhi_m/db (reciprocal by construction). Vacuum (0, 0, r0)."""
    spec = _resolve_carriers(spec)
    r0 = vacuum_r0() if r0 is None else r0
    pot = []
    for g in spec.gears:
        pot.append((Fraction(spec.carrier_of(g), 2), [(g, ZERO), (g, ZERO)]))
    pot += spec.site_potential(qualify=False)
    for _ax, lp in spec.link_potentials(qualify=False):
        pot += lp
    terms = gradient_terms(pot, what=f'matter {spec.name}')
    return Block(tuple((GearType(g, spec.label) for g in spec.gears)), tuple(terms), name=spec.name, vacuum={g: r0 for g in spec.gears}, params={'order': spec.order, 'site': dict(spec.site), 'laplacian': dict(spec.laplacian), 'reversor': {g: 'Mp' for g in spec.gears}, 'hops': tuple(spec.hops), 'carrier': {g: spec.carrier_of(g) for g in spec.gears}}, doc='matter defined by a MatterSpec (gradient of Phi_m)')

def atom_spec(name: str, mu: int, n: int=1, label: str='official') -> MatterSpec:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    gears = tuple((f'c{i}' for i in range(n))) if n > 1 else ('c',)
    return MatterSpec(name, gears, 2, {}, {(g, g): -mu for g in gears}, {}, (), label)

def load_pair_spec(name: str, mu: int, anti: bool=False, label: str='official') -> MatterSpec:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    if anti:
        return MatterSpec(name, ('X', 'Y'), 2, {'X': 'anti', 'Y': 'anti'}, {('X', 'X'): mu, ('Y', 'Y'): mu}, {}, (), label)
    return MatterSpec(name, ('X', 'Y'), 2, {}, {('X', 'X'): -mu, ('Y', 'Y'): -mu}, {}, (), label)

def light_spec(name: str, label: str='official') -> MatterSpec:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    return MatterSpec(name, ('L',), 2, {}, {}, {'L': 0}, (), label)

def kg_spec(name: str, mu: int, label: str='official') -> MatterSpec:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    return MatterSpec(name, ('K',), 2, {}, {('K', 'K'): -mu}, {'K': 0}, (), label)

def weyl_spec(name: str, s: int, m: int=0, wilson: int=0, label: str='official') -> MatterSpec:
    """Minimal FIRST-ORDER test matter (pi/2 carrier): two gears (X, Y), J-hopping on every axis
    Phi_link = s [X(x) Y(x+e) - Y(x) X(x+e)] (u_X = s(Y(x+e) - Y(x-e)), u_Y = -s(X(x+e) - X(x-e))), on-site mass m
    and Wilson term (difference form, weight wilson). Structure test matter for OD2 (not a 3-D Dirac spinor)."""
    hops = []
    for ax in range(3):
        hops += [('X', 'Y', ax, s), ('Y', 'X', ax, -s)]
    site = {('X', 'X'): m, ('Y', 'Y'): m} if m else {}
    lap = {'X': wilson, 'Y': wilson} if wilson else {}
    return MatterSpec(name, ('X', 'Y'), 1, {}, site, lap, tuple(hops), label)

def _resolve_carriers(spec: MatterSpec) -> MatterSpec:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    car = {g: -6 * 1 if spec.carrier.get(g) == 'anti' else spec.carrier[g] for g in spec.carrier}
    return MatterSpec(spec.name, spec.gears, spec.order, car, spec.site, spec.laplacian, spec.hops, spec.label)

def build_test_matter(spec: MatterSpec) -> Block:
    return build_matter(_resolve_carriers(spec))

def lapse_factors(order: int, gamma: str) -> tuple[Fraction, Fraction]:
    """(c_site, c_link) of Phi_int = -c_site (F/P) Phi_site - c_link ((F_x + F_y)/P) Phi_link.
    order 2: clock 1 - 2U, links 1 - 4U (GR) or 1 - 2U (1911); order 1: half of each (N, N/psi^2)."""
    if order not in (1, 2):
        raise ValueError('matter order must be 1 or 2')
    if gamma not in ('GR', '1911'):
        raise ValueError("gamma must be 'GR' (gamma = 1) or '1911' (lapse-only light control)")
    c_site = Fraction(1) if order == 2 else Fraction(1, 2)
    c_link = c_site if gamma == 'GR' else c_site / 2
    return (c_site, c_link)

def lapse_potential(F: str, P: int, matters: Sequence[MatterSpec], gamma: str='GR') -> list:
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

def build_lapse(*, P: int, field: str, matters: Sequence[MatterSpec], gamma: str='GR', name: str='lapse') -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    pot = lapse_potential(field, P, [_resolve_carriers(m) for m in matters], gamma)
    terms = gradient_terms(pot, what='lapse')
    return Block((), tuple(terms), name=name, vacuum={}, params={'P': P, 'field': field, 'gamma': gamma, 'matters': tuple(((m.name, m.order) for m in matters))}, doc='universal lapse: clock factor on on-site entries, link factor on transport entries; reciprocal')
G_READ_WHY = 'beta=1 auxiliary G read by matter (clock factor +G/P, link factor +(17/8)(G_x+G_y)/P): a reciprocal partner would source G with the matter energy, giving G = F^2/(2P) - F at FIRST order and destroying the lapse; no rank-3 reciprocal form exists (the reciprocal equivalent is the OD4 quartic, build_beta_rank4)'
G_SOURCE_WHY = 'beta=1 auxiliary G sourced by -k Lap(F^2) (exact discrete Leibniz) with F not reading G: the agreed S1 X1 form (one-way); its reciprocal completion is reciprocal_source=True'

def beta_matter_factors(order: int) -> tuple[Fraction, Fraction]:
    """Second-order coefficients (site, per-link-endpoint) of G/P: order 2: N^2 += 2U^2 = G/P (site), lambda +=
    (17/2)U^2 = (17/8)(G_x + G_y)/P; order 1: N += U^2/2 = G/(4P), N/psi^2 += (9/4)U^2 = (9/16)(G_x + G_y)/P."""
    return (Fraction(1), Fraction(17, 8)) if order == 2 else (Fraction(1, 4), Fraction(9, 16))

def build_beta(*, P: int, k: int, field: str, matters: Sequence[MatterSpec]=(), reciprocal_source: bool=False, name: str='beta', gear: str='G', r0: int | None=None) -> Block:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def build_beta_rank4(*, P: int, field: str, matters: Sequence[MatterSpec], name: str='beta4') -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    pot = []
    for spec in matters:
        spec = _resolve_carriers(spec)
        c2s = Fraction(1, 2) if spec.order == 2 else Fraction(1, 8)
        c2l = Fraction(17, 8) if spec.order == 2 else Fraction(9, 16)
        for c, mono in spec.site_potential():
            pot.append((c2s * Fraction(c) / P ** 2, [(field, ZERO), (field, ZERO)] + mono))
        for ax, lp in spec.link_potentials():
            e = AXES[ax]
            for c, mono in lp:
                for f1, f2, wgt in ((ZERO, ZERO, Fraction(1, 4)), (ZERO, e, Fraction(1, 2)), (e, e, Fraction(1, 4))):
                    pot.append((wgt * c2l * Fraction(c) / P ** 2, [(field, f1), (field, f2)] + mono))
    terms = gradient_terms(pot, what='beta rank4')
    return Block((), tuple(terms), name=name, vacuum={}, params={'P': P, 'field': field, 'matters': tuple((m.name for m in matters))}, doc='OD4 reciprocal beta = 1 quartics (on-site / on-link)')
ND_SELF_WHY = 'N-design self law (1+N) Lap N = Sum_e (delta_e N)^2 (lattice form of (1+N) Lap N = 2|grad N|^2): the Euler-Lagrange equation of the NON-polynomial potential |grad psi|^2, psi = 2/(1+N); no polynomial (rank <= 4) potential reproduces it'
ND_AUX_WHY = 'N-design auxiliary (a2, crem, lamrem): static law by the exact discrete Leibniz identity, feed-forward chain from N (one-way by construction, S1 X5/X11)'
ND_SRC_WHY = 'N-design York-weighted source -sigma n C from the prescribed static density gear n (MECHANISM, S1-M2 Y4); n does not feel N (a static prescribed load)'
ND_READ_WHY = 'N-design metric read by test clocks (A = 1 + 2 eps + a2) and test light (lambda = 1 + 4 eps + lamrem, or A*C at rank 4): test bodies of the static vacuum construction (one-way; a reciprocal read would source the auxiliaries with matter energy, as for G). OD4 status of the rank-4 A*C light weight: its quartics (nu_x nu_y, nu crem, a2 crem, a2 nu times (delta b)^2) are INDEFINITE cross-quartics, not -lambda q^2 springs; they are kept only as designated one-way test-light reads'

def build_ndesign(*, P: int, k: int, sigma0: int, w_a2: int, w_c: int, w_lam: int | None=None, clocks: Sequence[MatterSpec]=(), lights: Sequence[MatterSpec]=(), rank4: bool=False, name: str='nd', r0: int | None=None) -> Block:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')
OD2_READ_WHY = 'OD2 centred read of the accumulator metric by matter: the accumulators are slaved to the harmonic constants (rounding-free input K = 0 mod D); a reciprocal matter source on them would break the exact momentum constraints (S4 A8/B8); the physical source enters through the hij stress'
OD2_ACC_WHY = 'OD2 accumulator (S4 A8/B8): a slaved gear integrating the harmonic condition exactly, D_t h0i = -Div_i hbar (h00: D_t h00 = -Div_0 h0); its b-reads are the integration, not a force, and have no partner (hij and h0i do not read the accumulators at single time)'
OD2_STRESS_WHY = 'OD2 b-only first-order stress source of hij (S4 B8, P-vii(c)): the matter does not read hij back at single time (its hij coupling, if any, is a separate block)'

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
    return 'h' + SPATIAL[a] + SPATIAL[b]

def build_od2(*, name: str='od2', stress: Sequence[tuple]=(), reads: Sequence[tuple]=(), label: str='audit', r0: int | None=None) -> Block:
    """OD2 build (S4 A8, B8, C1, P-vi, P-vii(c)): 6 hij F-gears (headroom stencil) + 3 h0i (link gears) and h00
    ACCUMULATORS, read at centred times; NO remainder-reading input.

    h0i: u = D b - (D/2)[Div_i(hbar(t)) - Div_i(hbar(t-1))] (reads hij's a): K = 2u = 0 mod D, so r never changes
         and C^i(t) = h0i(t+1) - h0i(t) + Div_i(t) is EXACTLY constant (Div_i: ``_div_spatial_terms``).
    h00: u = D b - (D/2)[Div_0(t) - Div_0(t-1)], Div_0 = Sum_i [h0i(x) - h0i(x - e_i)] (reads h0i's a):
         C^0(t) = h00(t+1) - h00(t) + Div_0(t) EXACTLY constant.
    ``stress``: extra b-only source terms (target local hij name, coeff, factors) from the matter (designated
    one-way, OD2_STRESS_WHY). ``reads``: matter terms reading the accumulators at centred times (two-time reads), e.g.
    from ``od2_centred_lapse_read``. Acyclic: hij (stage 0) -> h0i -> h00 -> matter."""
    r0 = vacuum_r0() if r0 is None else r0
    D = 6
    hij = [comp_name(i, j) for i in range(3) for j in range(i, 3)]
    gears = [GearType(c, label, None) for c in hij] + [GearType(f'h0{SPATIAL[i]}', label, i) for i in range(3)] + [GearType('h00', label, None)]
    terms = []
    for c in hij:
        terms += gradient_terms(headroom_potential(c), what='od2 hij')
    acc = {'designated_one_way': OD2_ACC_WHY}
    for i in range(3):
        t = f'h0{SPATIAL[i]}'
        terms.append((t, D, ((t, ZERO, 'b'),)))
        terms += [x + (acc,) for x in _div_spatial_terms(t, comp_name, i, 'b', -(D // 2))]
        terms += _div_spatial_terms(t, comp_name, i, 'a', D // 2)
    for i in range(3):
        h0 = f'h0{SPATIAL[i]}'
        for fld, sg in (('b', -1), ('a', 1)):
            for x in [('h00', sg * (D // 2), ((h0, ZERO, fld),)), ('h00', -sg * (D // 2), ((h0, _neg(AXES[i]), fld),))]:
                terms.append(x + (acc,) if fld == 'b' else x)
    terms.append(('h00', D, (('h00', ZERO, 'b'),)))
    for t in stress:
        terms.append(tuple(t[:3]) + ({'designated_one_way': OD2_STRESS_WHY},))
    for t in reads:
        terms.append(tuple(t))
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: r0 for g in gears}, params={'label': label, 'n_stress': len(stress), 'n_reads': len(reads), 'reversor_staggered': 'observe.gravity.od2_staggered_reversor (hij Mp/M; h0i (a,b) -> (-h0i(t+1), -b); h00 (a,b) -> (h00(t+2), h00(t+1)); r kept)'}, doc='OD2: hij F-gears + rounding-free h0i, h00 accumulators (exact harmonic constants)')

def od2_lookahead_h00(ns: str) -> list:
    """h00(t+1) as a linear form of the snapshot (b, a): 2 b_h00 - a_h00 - [Div_0(b) - Div_0(a)]: list of
    (coeff, (gear, offset, field))."""
    q = lambda g: f'{ns}.{g}'
    out = [(2, (q('h00'), ZERO, 'b')), (-1, (q('h00'), ZERO, 'a'))]
    for i in range(3):
        h0 = q(f'h0{SPATIAL[i]}')
        out += [(-1, (h0, ZERO, 'b')), (1, (h0, _neg(AXES[i]), 'b')), (1, (h0, ZERO, 'a')), (-1, (h0, _neg(AXES[i]), 'a'))]
    return out

def od2_centred_lapse_read(ns: str, spec: MatterSpec, P: int, g00: int=1) -> list:
    """Matter terms reading h00 one step AHEAD (centred, S4-M M_grav_mirror: 'g00 * h00_next * mass b'):
    u_t += g00 * h00(t+1) * (H b)_t / P on the on-site entries; two-time reads (designated one-way, OD2_READ_WHY)."""
    spec = _resolve_carriers(spec)
    out = []
    for (t, s), H in spec.site.items():
        pairs = [(t, s)] if t == s else [(t, s), (s, t)]
        for tt, ss in pairs:
            for c, f in od2_lookahead_h00(ns):
                coeff = Fraction(g00 * c * H, P)
                if coeff.denominator != 1:
                    raise ValueError('od2 read: H*g00 must be divisible by P')
                out.append((spec.q(tt), int(coeff), (f, (spec.q(ss), ZERO, 'b')), {'designated_one_way': OD2_READ_WHY}))
    return out

def od2_hop_stress(ns: str, spec: MatterSpec, kappa: int) -> list:
    """b-only first-order (link-local) stress sources of hij from the matter's hop entries (generic interface):
    s^{jj}(x) += kappa * Sum_{hops on axis j} c b_t(x) b_s(x + e_j);
    s^{ij}(x) += kappa * [hop bilinear on axis i + hop bilinear on axis j] / 2 (i != j). Integer kappa (even for
    i != j terms with odd c)."""
    out = []
    for i in range(3):
        for j in range(i, 3):
            comp = f'{comp_name(i, j)}'
            for t, s, ax, c in spec.hops:
                if ax not in (i, j):
                    continue
                coeff = Fraction(kappa * c, 1 if i == j else 2)
                if coeff.denominator != 1:
                    raise ValueError('od2 stress: kappa * c must be even for off-diagonal components')
                out.append((comp, int(coeff), ((spec.q(t), ZERO, 'b'), (spec.q(s), AXES[ax], 'b'))))
    return out

def spec_from_block(block: Block, *, order: int, carrier: dict | None=None, laplacian: dict | None=None, label: str | None=None) -> MatterSpec:
    """GENERIC interface extraction: the MatterSpec of ANY linear, reciprocal matter block (e.g. a later B1-EM block).

    Its degree-1 monomials are classified: on-site factors -> the on-site (mass/clock) entries H_ts (the declared
    carrier and the declared difference-form transport diagonal -6w are removed from the diagonal); face-offset factors
    -> transport entries (difference-form weights ``laplacian`` {gear: w} are recognised, every other face entry
    becomes a generic hop c b_t(x) b_s(x + e) on the positive axis). Raises if the block has non-linear terms or is not
    reciprocal (the lapse multiplies a POTENTIAL, so the matter must have one)."""
    carrier = dict(carrier or {})
    laplacian = dict(laplacian or {})
    gears = tuple((g.name for g in block.gears))
    gset = set(gears)
    site: dict = {}
    hops = {}
    face = {}
    for t in block.terms:
        target, c, factors = (t[0], t[1], t[2])
        if target not in gset:
            continue
        if len(factors) != 1 or factors[0][2] != 'b' or factors[0][0] not in gset:
            raise ValueError(f'spec_from_block: only linear b-only matter is supported, got {t!r}')
        s, off = (factors[0][0], tuple(factors[0][1]))
        if off == ZERO:
            site[target, s] = site.get((target, s), 0) + c
        else:
            face[target, s, off] = face.get((target, s, off), 0) + c
    for g in gears:
        c0 = carrier.get(g, 6 if order == 2 else 0)
        site[g, g] = site.get((g, g), 0) - c0 + 6 * laplacian.get(g, 0)
    for (t, s, off), c in face.items():
        partner = face.get((s, t, _neg(off)), None)
        if partner != c:
            raise ValueError(f'spec_from_block: face entry {(t, s, off)} has no reciprocal partner')
        if t == s and laplacian.get(t, 0):
            if c != laplacian[t]:
                raise ValueError(f'spec_from_block: face weight of {t} is {c}, declared laplacian {laplacian[t]}')
            continue
        if off in AXES:
            hops[t, s, AXES.index(off)] = c
    sym = {}
    for (t, s), H in site.items():
        if site.get((s, t), 0) != H:
            raise ValueError(f'spec_from_block: on-site entries ({t},{s}) not symmetric')
        a, b = sorted((t, s))
        if H:
            sym[a, b] = H
    return MatterSpec(block.name, gears, order, carrier, sym, laplacian, tuple(((t, s, ax, c) for (t, s, ax), c in sorted(hops.items()))), label if label is not None else block.gears[0].label if block.gears else 'official')
STATIC_LOAD_WHY = 'Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.'

def build_static_load(*, field: str, coeff: int=1, name: str='sload', r0: int | None=None) -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    r0 = vacuum_r0() if r0 is None else r0
    terms = gradient_terms(wave_potential('n', 0, 6), what='static load')
    terms.append((field, coeff, ((f'{name}.n', ZERO, 'b'), (f'{name}.n', ZERO, 'b')), {'designated_one_way': STATIC_LOAD_WHY}))
    return Block((GearType('n', 'audit'),), tuple(terms), name=name, vacuum={'n': r0}, params={'field': field, 'coeff': coeff, 'reversor': {'n': 'Mp'}}, doc='prescribed static load (MECHANISM)')
