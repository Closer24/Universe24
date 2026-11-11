"""Experimental single-physical-edge realization, using the existing Rule3 engine.

This is a NEW tensor, not an exact retiming or gauge-equivalent rewrite of ONE.
For each link-valued source gear U, introduce a node gear H carrying its old
polynomial. Replace all old U references by H, then couple the retained physical
link U to H at both endpoints with reciprocal linear springs. All original
polynomial terms survive on node variables; every added term occupies one edge.
No link metadata is erased, no update callback or copy operation runs at runtime.
See docs/SINGLE_EDGE_IMPLEMENTATION.md for equations, proof and limitations.
"""
from dataclasses import dataclass

from ..core.lattice import DIRECTIONS, ZERO
from ..core.tensor import GearType, Tensor


@dataclass(frozen=True)
class EdgeRealization:
    tensor: Tensor
    source_fingerprint: str
    source_gears: int
    # (original physical link index, new node mediator index)
    link_mediators: tuple[tuple[int, int], ...]
    stiffness: int


def single_edge_realization(source: Tensor, *, stiffness: int) -> EdgeRealization:
    """Build fixed integer data before a run; preserve rank <= 4 and staged inverse.

    The spring coefficient is an explicit model choice, not a consequence of
    Rule3. For an isolated inertial node/link chain, 0 < stiffness <= Q keeps
    linear mode eigenvalues inside [-D,D]; the uniform mode is marginal.
    Stability of the full composition is NOT implied.
    """
    if source.Q is None:
        raise ValueError('single-edge realization needs a declared common Q')
    if any(g.name.startswith('edgehub.') for g in source.gears):
        raise ValueError('edgehub namespace is reserved; do not localize twice')
    Q, D = source.Q, 6 * source.Q
    if type(stiffness) is not int or not 1 <= stiffness <= Q:
        raise ValueError('stiffness must be an integer in [1,Q]')
    gears = list(source.gears)
    pairs = []
    for i, gear in enumerate(source.gears):
        if gear.link is not None:
            pairs.append((i, len(gears)))
            gears.append(GearType('edgehub.' + gear.name, 'audit', None, gear.sign, gear.sign_why))
    remap = dict(pairs)
    terms = []
    for m in source.monomials:
        target = remap.get(m.target, m.target)
        factors = tuple((remap.get(f.gear, f.gear), f.offset, f.field) for f in m.factors)
        term = (target, m.coeff, factors)
        why = source.designations.get((m.target, m.factors))
        if why:
            term += ({'designated_one_way': why},)
        terms.append(term)
    k = stiffness
    for link, hub in pairs:
        e = DIRECTIONS[2 * source.gears[link].link]
        back = tuple(-v for v in e)
        # U(x,e) touches only x and x+e. H is an independent node register.
        terms.extend([
            (link, D - 2*k, ((link, ZERO, 'b'),)),
            (link, k, ((hub, ZERO, 'b'),)),
            (link, k, ((hub, e, 'b'),)),
            (hub, -2*k, ((hub, ZERO, 'b'),)),
            (hub, k, ((link, ZERO, 'b'),)),
            (hub, k, ((link, back, 'b'),)),
        ])
    tensor = Tensor(gears, terms, Q=Q, strict_support=True)
    return EdgeRealization(tensor, source.fingerprint, source.G, tuple(pairs), k)
