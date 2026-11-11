"""Optional one-way scalar clock modulation stored as fixed integer tensor terms. The former automatic cosmic assembly and stability window were retired. Explicit blocks remain algebraic experiments, not a physical clock derivation."""
from __future__ import annotations
from ..core.tensor import Block
from .one import COSMIC_NS, one_system
from .system import System
ZERO = (0, 0, 0)
CLOCKGEN_NS = 'clockgen'
HAND = f'{COSMIC_NS}.Th'
LAPSE = 'metric.h00'
KAPPA_DEFAULT = 1
MODES = ('drive', 'param')
WHY_CLOCK_DRIVE = 'ADDITIVE CONTRAST (Study 34 CG1, CLK-A; default OFF): the cosmic hand is a one-way source of the lapse, u[h00] += kappa Theta; the hand does not feel the lapse (THEOREM O row Theta: no additive source on the hand); every lapse READER feels each turn, no matter gear reads Theta; it cannot bound the uniform lapse'
WHY_CLOCK_PARAM = 'Explicit one-way parametric tensor coupling; the clock does not receive the reciprocal response. No stability claim.'

def build_clockgen(*, kappa: int=KAPPA_DEFAULT, mode: str='drive', hand: str=HAND, lapse: str=LAPSE, name: str=CLOCKGEN_NS) -> Block:
    """The clock-law block: 0 gear types, ONE designated term targeting the lapse (see the module docstring)."""
    if type(kappa) is not int or kappa == 0:
        raise ValueError('kappa must be a nonzero Python int (integer coefficient)')
    if mode not in MODES:
        raise ValueError(f'mode must be one of {MODES}')
    if mode == 'drive':
        terms = ((lapse, kappa, ((hand, ZERO, 'b'),), {'designated_one_way': WHY_CLOCK_DRIVE}),)
        law = 'u[h00] += kappa * Theta (rank 2, on-site, one-way)'
    else:
        terms = ((lapse, kappa, ((hand, ZERO, 'b'), (lapse, ZERO, 'b')), {'designated_one_way': WHY_CLOCK_PARAM}),)
        law = 'u[h00] += kappa * Theta * F (rank 3, on-site, one-way)'
    return Block((), terms, name=name, vacuum={}, params={'kappa': kappa, 'mode': mode, 'hand': hand, 'lapse': lapse, 'law': law}, doc='Study 34 clock law (CLK-A): the hand acts on the lapse only; default OFF')

def clockgen_system(*, kappa: int=KAPPA_DEFAULT, mode: str='drive', one_kw: dict | None=None) -> System:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')
THETA0_LOG2_CLOCK = 21
CLOCK_LAWS = ('CG2', 'CG1', 'off')

def one_system_clock(*, law: str='CG2', theta0_log2: int=THETA0_LOG2_CLOCK, kappa: int=1, one_kw: dict | None=None) -> System:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def clock_window(L: int, theta0: int=1 << THETA0_LOG2_CLOCK, kappa: int=1, A_c: int=1024, g_w: int=1310, W6: float=0.01658) -> dict:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def _ns(name: str) -> str:
    return name.split('.', 1)[0]

def theta_reader_census(tensor, hand: str=HAND) -> dict:
    """Every gear (and namespace) whose input contains the hand as a factor. The owner rule (Study 34) holds iff no
    package MATTER gear is among them; the allowed set is the hand itself (face terms), the cosmic block's own
    reader gears M1/M2 (CC-A's species, see G5) and the lapse (the universal clock)."""
    names = tensor.names
    th = tensor.gear_index(hand)
    by_target: dict[str, int] = {}
    for m in tensor.monomials:
        if any((f.gear == th for f in m.factors)):
            by_target[names[m.target]] = by_target.get(names[m.target], 0) + 1
    allowed = {hand, f'{COSMIC_NS}.M1', f'{COSMIC_NS}.M2', LAPSE}
    bad = {k: v for k, v in by_target.items() if k not in allowed}
    return {'readers_of_theta': by_target, 'outside_allowed': bad, 'no_matter_reads_theta': not bad, 'allowed': sorted(allowed)}

def lapse_reader_census(tensor, lapse: str=LAPSE) -> dict:
    """Which namespaces read the lapse (= which clocks can feel a cosmic turn through time), with monomial counts,
    split by degree and designation. Read-only."""
    names = tensor.names
    F = tensor.gear_index(lapse)
    desig = set(tensor.designations.keys()) if hasattr(tensor, 'designations') else set()
    out: dict[str, dict] = {}
    for m in tensor.monomials:
        if m.target == F:
            continue
        if any((f.gear == F for f in m.factors)):
            rec = out.setdefault(_ns(names[m.target]), {'monomials': 0, 'by_degree': {}, 'designated': 0, 'target_gears': set()})
            rec['monomials'] += 1
            rec['by_degree'][m.degree] = rec['by_degree'].get(m.degree, 0) + 1
            rec['designated'] += int((m.target, m.factors) in desig)
            rec['target_gears'].add(names[m.target])
    for rec in out.values():
        rec['target_gear_count'] = len(rec.pop('target_gears'))
    return out

def lapse_source_census(tensor, lapse: str=LAPSE) -> dict:
    """Which namespaces SOURCE the lapse (monomials targeting the lapse, by the namespace of their factors)."""
    names = tensor.names
    F = tensor.gear_index(lapse)
    out: dict[str, int] = {}
    for m in tensor.monomials:
        if m.target != F:
            continue
        nss = sorted({_ns(names[f.gear]) for f in m.factors})
        key = '+'.join(nss)
        out[key] = out.get(key, 0) + 1
    return out
__all__ = ['CLOCKGEN_NS', 'HAND', 'LAPSE', 'KAPPA_DEFAULT', 'MODES', 'WHY_CLOCK_DRIVE', 'WHY_CLOCK_PARAM', 'build_clockgen', 'clockgen_system', 'theta_reader_census', 'lapse_reader_census', 'lapse_source_census', 'THETA0_LOG2_CLOCK', 'CLOCK_LAWS', 'one_system_clock', 'clock_window']
