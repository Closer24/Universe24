"""Prepared finite clocks. These factories create data, never evolution rules."""
from itertools import product

from universe24.core.group_2o import DIRECTIONS
from .spec import Patch, TensorSpec


def _positive_tensor(tensor):
    tensor = TensorSpec() if tensor is None else tensor
    if not isinstance(tensor, TensorSpec):
        raise TypeError('tensor must be a TensorSpec')
    if tensor.body_signs != (1, 1, 1):
        raise ValueError('These prepared families require the +++ tensor')
    return tensor


def _integer(value, allowed, label):
    if type(value) is not int or value not in allowed:
        raise ValueError(label + ' must be an exact integer in ' + str(allowed))
    return value


def _boolean(value, label):
    if type(value) is not bool:
        raise TypeError(label + ' must be Boolean')
    return value


def _halo(core):
    return tuple(sorted({tuple(x[i] + d[i] for i in range(3))
                         for x in core for d in DIRECTIONS} - set(core)))


def _ports(core, halo):
    return {'core': tuple((*x, g) for x in core for g in range(48)),
            'halo': tuple((*x, g) for x in halo for g in range(48)),
            'center': ((*core[0], 0),)}


def LocalizedSixClock(*, phase=0, core_remainder=2, halo_parity=0,
                      active=True, tensor=None):
    """An eight-site cube and its 24-site remainder halo, period six in isolation.

    ``active=False`` removes counters but retains the complete prepared hardware.
    It is a counter-mask control, not an absent component. All 48 channels are
    assigned. Any additional donor input requires a separate interaction test.
    """
    tensor = _positive_tensor(tensor)
    _integer(phase, range(6), 'phase')
    _integer(core_remainder, range(6), 'core_remainder')
    _integer(halo_parity, range(2), 'halo_parity')
    _boolean(active, 'active')
    a, b = ((0, 1), (1, 1), (1, 0), (0, -1), (-1, -1), (-1, 0))[phase]
    aa, bb, prefix = a, b, 0
    prefixes = []
    for _ in range(6):
        prefixes.append(prefix)
        prefix += bb
        aa, bb = bb, bb - aa
    lo, hi = -2 * min(prefixes), 5 - 2 * max(prefixes)
    hr = next(r for r in range(lo, hi + 1) if r % 2 == halo_parity)
    core = tuple(product(range(2), repeat=3))
    halo = _halo(core)
    cells = {(*x, g): (a if active else 0, b if active else 0, core_remainder)
             for x in core for g in range(48)}
    cells.update({(*x, g): (0, 0, hr) for x in halo for g in range(48)})
    return Patch('localized-six-clock', cells, tensor=tensor, ports=_ports(core, halo),
                 evidence_domains=('Exact period six with the complete isolated prepared halo; '
                                   'active=False retains hardware. No physical mass identification.',))


def CompactFiveClock(*, shape='dimer', phase=0, conjugated=False,
                     active=True, tensor=None):
    """A period-five dimer or plaquette, including all halo remainders.

    J conjugation transforms counters AND remainders. ``active=False`` retains
    the prepared remainders. The signed conserved quantity is not electric charge.
    """
    tensor = _positive_tensor(tensor)
    if shape not in ('dimer', 'plaquette'):
        raise ValueError('shape must be dimer or plaquette')
    _integer(phase, range(5), 'phase')
    _boolean(conjugated, 'conjugated')
    _boolean(active, 'active')
    core = ((0, 0, 0), (1, 0, 0)) if shape == 'dimer' else tuple(
        (x, y, 0) for x, y in product(range(2), repeat=2))
    halo = _halo(core)
    degree = 1 if shape == 'dimer' else 2
    a, b, r, prefix = 0, 1, 4 if degree == 1 else 2, 0
    for _ in range(phase):
        ell, rn = divmod(2 * degree * b + r, 6)
        prefix += b
        a, b, r = b, ell - a, rn
    cells = {(*x, g): (a, b, r) for x in core for g in range(48)}
    cells.update({(*x, g): (0, 0, 2 * prefix) for x in halo for g in range(48)})
    if conjugated:
        cells = {addr: (-a, -b, 4 - r + 2 * (r % 2))
                 for addr, (a, b, r) in cells.items()}
    if not active:
        cells = {addr: (0, 0, v[2]) for addr, v in cells.items()}
    return Patch('compact-five-clock', cells, tensor=tensor, ports=_ports(core, halo),
                 evidence_domains=('Exact isolated prepared period-five ' + shape +
                                   '; active=False retains hardware. No physical charge or mass claim.',))


def CooperativeClockPair(*, first_active=True, second_active=True, tensor=None):
    """One joint period-six preparation with an explicitly shared four-site halo.

    Both cores active give the confined cycle. Either core alone disturbs the
    shared halo at step two. This is not spontaneous binding or a force law.
    """
    tensor = _positive_tensor(tensor)
    _boolean(first_active, 'first_active')
    _boolean(second_active, 'second_active')
    first = tuple(product(range(2), repeat=3))
    second = tuple((x + 3, y, z) for x, y, z in first)
    ah, bh = set(_halo(first)), set(_halo(second))
    shared = ah & bh
    cells = {(*x, g): (0, int(first_active), 2) for x in first for g in range(48)}
    cells.update({(*x, g): (0, -int(second_active), 2) for x in second for g in range(48)})
    cells.update({(*x, g): (0, 0, 2 if x in shared else 0 if x in ah else 4)
                  for x in ah | bh for g in range(48)})
    return Patch('cooperative-clock-pair', cells, tensor=tensor,
                 ports={'first': tuple((*x, g) for x in first for g in range(48)),
                        'second': tuple((*x, g) for x in second for g in range(48)),
                        'shared': tuple((*x, g) for x in sorted(shared) for g in range(48)),
                        'region': tuple(sorted(cells))},
                 evidence_domains=('Prepared joint period six; masks retain joint hardware. '
                                   'Isolated constituents are not valid replacements for this shared halo.',))
