"""Public fixed-six system constructor and optional tensor composition helpers.

The default has 48 reference channels. Historical cosmic/electroweak assembly
calibrations are not reinterpreted as equivalent models at this divisor.
"""
from __future__ import annotations
from math import gcd
from ..core.lattice import DIRECTIONS
from ..core.tensor import Block, GearType
from .system import System, default_system
ZERO = (0, 0, 0)
COSMIC_NS = 'cosmic'
COSMIC_GEARS = ('Th', 'M1', 'M2', 'Lp', 'Lm', 'dp', 'dm')
REFERENCE_VERSION = 'fixed-six'
WHY_COUPLE = 'Explicit one-way clock modulation chosen as tensor data; the clock does not receive the reciprocal response.'

def cosmic_params(**options):
    raise NotImplementedError('the previous cosmic clock calibration is retired; use an explicit fixed-six clock construction')

def build_cosmic(**options):
    raise NotImplementedError('the previous cosmic clock calibration is retired; use an explicit fixed-six clock construction')

def theta_scale_block(block: Block, theta0: int, hand: str=f'{COSMIC_NS}.Th', select=None) -> Block:
    """COPY of ``block`` whose selected terms carry the hand as one common factor: an on-site term c * prod -> (c/Theta0)
    Theta_x * prod; a link term (factors on {0, e}) -> (c/(2 Theta0)) (Theta_x + Theta_{x+e}) * prod. Each scaled entry is
    designated one-way (the hand does not feel it). Raises if a coefficient is not divisible (integer grain) or if a term
    would reach rank 5 (it already has 3 factors). Unselected terms are kept unchanged (construction-time only)."""
    if type(theta0) is not int or theta0 <= 0:
        raise ValueError('theta0 must be a positive integer seed amplitude')
    out = []
    for t in block.terms:
        if select is not None and (not select(block, t)):
            out.append(t)
            continue
        target, c, facs = (t[0], int(t[1]), tuple(t[2]))
        if len(facs) >= 3:
            raise ValueError(f'block {block.name!r}: Theta x a degree-3 entry would be rank 5 (FORBIDDEN)')
        offs = {tuple(f[1]) for f in facs if tuple(f[1]) != ZERO}
        why = WHY_COUPLE + (' | ' + t[3]['designated_one_way'] if len(t) > 3 and t[3] else '')
        if not offs:
            if c % theta0:
                raise ValueError(f'block {block.name!r}: on-site coefficient {c} not divisible by Theta0 = {theta0}')
            out.append((target, c // theta0, facs + ((hand, ZERO, 'b'),), {'designated_one_way': why}))
        else:
            e, = offs
            if c % (2 * theta0):
                raise ValueError(f'block {block.name!r}: link coefficient {c} not divisible by 2 Theta0 = {2 * theta0}')
            for off in (ZERO, e):
                out.append((target, c // (2 * theta0), facs + ((hand, off, 'b'),), {'designated_one_way': why}))
    return Block(block.gears, tuple(out), name=block.name, vacuum=dict(block.vacuum), params=dict(block.params, theta_scaled={'theta0': theta0, 'hand': hand}), doc=block.doc + ' [Theta-scaled first-order entries: Study 22 coupling option]')

def _ns(name: str) -> str:
    return name.split('.', 1)[0]

def theta_reading_census(tensor, theta0: int=1, exclude=(COSMIC_NS,)) -> dict:
    """Exact census of which namespaces COULD read Theta as an (A)-class sector (THEOREM O): every gear's input must be
    Theta x (its present input) with integer coefficients at Theta0, i.e. each on-site coefficient c with Theta0 | c and
    each link coefficient with 2 Theta0 | c (link-averaged factor). Per gear type: first-order iff its own-gear inertia
    s_g = Sum of its degree-1 self coefficients (any offset) is < D/2. Reported per namespace: first-order gear count,
    max admissible Theta0 (gcd rule; 0 = impossible), entries that would become rank 5 (degree 3 already), entries reading
    E1 gears (Theta x E1 link/potential x matter: not the narrow kind), entries reading any link gear, two-time reads, and
    the E1 dressed-source entries reading the namespace (they would need Theta: rank 5), and LOAD-DRIVEN entries (no
    factor from a first-order node gear: e.g. a choice pair; not (A)-class: THEOREM O row A, AGREE_COSMIC C5)."""
    D = 6
    names = tensor.names
    gears = tensor.gears
    inertia = [0] * tensor.G
    for m in tensor.monomials:
        if m.degree == 1 and m.factors[0].gear == m.target and (m.factors[0].field == 'b'):
            inertia[m.target] += m.coeff
    first = [i for i in range(tensor.G) if abs(inertia[i]) < D // 2]
    per: dict[str, dict] = {}
    for i, nm in enumerate(names):
        ns = _ns(nm)
        if ns in exclude:
            continue
        rec = per.setdefault(ns, {'gear_types': 0, 'first_order_types': 0, 'second_order_types': 0, 'g_site': 0, 'g_link_half': 0, 'odd_link_coeff': 0, 'deg3_terms': 0, 'em_reads': 0, 'link_reads': 0, 'a_reads': 0, 'terms': 0, 'dressed_source_terms_reading_it': 0, 'load_terms': 0})
        rec['gear_types'] += 1
        rec['first_order_types' if i in first else 'second_order_types'] += 1
    fo = set(first)
    fo_node = {i for i in fo if gears[i].link is None}
    cross = {'cosmic_reads_package': 0, 'package_reads_cosmic': 0}
    for m in tensor.monomials:
        tns = _ns(names[m.target])
        if tns in exclude:
            cross['cosmic_reads_package'] += int(any((_ns(names[f.gear]) not in exclude for f in m.factors)))
            continue
        if any((_ns(names[f.gear]) in exclude for f in m.factors)):
            cross['package_reads_cosmic'] += 1
            continue
        if tns == 'em' and m.degree == 3:
            for f in m.factors:
                fns = _ns(names[f.gear])
                if fns != 'em' and fns in per and (f.gear in fo):
                    per[fns]['dressed_source_terms_reading_it'] += 1
                    break
        if m.target not in fo:
            continue
        rec = per[tns]
        rec['terms'] += 1
        link = any((f.offset != ZERO for f in m.factors))
        c = abs(m.coeff)
        if link:
            if c % 2:
                rec['odd_link_coeff'] += 1
            rec['g_link_half'] = gcd(rec['g_link_half'], c // 2)
        else:
            rec['g_site'] = gcd(rec['g_site'], c)
        rec['deg3_terms'] += int(m.degree == 3)
        rec['em_reads'] += int(any((_ns(names[f.gear]) == 'em' for f in m.factors)))
        rec['link_reads'] += int(any((gears[f.gear].link is not None for f in m.factors)))
        rec['a_reads'] += int(any((f.field == 'a' for f in m.factors)))
        rec['load_terms'] += int(not any((f.gear in fo_node for f in m.factors)))
    readers, non_readers = ([], [])
    for ns, rec in sorted(per.items()):
        if rec['first_order_types'] == 0:
            rec['theta0_max'] = 0
            rec['verdict'] = 'second-order (THEOREM O class C): cannot be a Theta reader'
        else:
            tmax = 0 if rec['odd_link_coeff'] else gcd(rec['g_site'], rec['g_link_half'])
            rec['theta0_max'] = tmax
            why = []
            if tmax < theta0:
                why.append(f'integer grain: max Theta0 = {tmax} < {theta0}')
            if rec['deg3_terms']:
                why.append(f"{rec['deg3_terms']} entries would become rank 5 (FORBIDDEN)")
            if rec['em_reads']:
                why.append(f"{rec['em_reads']} E1 entries (Theta x E1 x matter: not the narrow kind)")
            if rec['dressed_source_terms_reading_it']:
                why.append(f"its exact E1 source would need Theta x lapse x link x matter: {rec['dressed_source_terms_reading_it']} rank-5 entries (FORBIDDEN)")
            if rec['load_terms']:
                why.append(f"{rec['load_terms']} load-driven entries (no factor from a first-order node field: not (A)-class, THEOREM O row A / AGREE_COSMIC C5)")
            if rec['second_order_types']:
                why.append(f"{rec['second_order_types']} second-order gear types in the namespace")
            rec['verdict'] = 'CAN read Theta' if not why else 'cannot read Theta: ' + '; '.join(why)
        (readers if rec['verdict'] == 'CAN read Theta' else non_readers).append(ns)
    return {'theta0': theta0, 'D': D, 'per_namespace': per, 'readers': readers, 'non_readers': non_readers, 'first_order_gear_types': len(first), 'cross_reads': cross, 'block_diagonal': cross['cosmic_reads_package'] == 0 and cross['package_reads_cosmic'] == 0}

def reference_system(*, body_signs=(1, -1, 1), label='official', extra_blocks=(),
               communication: bool = False, **retired_options) -> System:
    """Reference dynamics with local message reception; no global clock.

    communication=False selects the previous 48-channel reference law and
    its original preparation explicitly, for historical regression checks.
    """
    if type(communication) is not bool:
        raise TypeError('communication must be a bool')
    from .communication import build_communication
    extra = tuple(extra_blocks)
    if communication:
        extra = (build_communication(label=label),) + extra
    system = default_system(body_signs=body_signs, label=label, extra_blocks=extra, **retired_options)
    model = 'local-communication' if communication else 'reference'
    system.info.update(implementation='fixed-six-' + model, communication=communication,
                       default_gear_count=54 if communication else 48)
    system.info['one'] = {'version': 'fixed-six-communication' if communication else 'fixed-six',
                         'default': model, 'cosmic': False, 'coupled_doublet': False,
                         'law': 'fixed tensor and initial state; scalar divisor six'}
    return system
