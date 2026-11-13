"""An 18-channel, fixed-six Maxwell test field on a static optical background.

Only tensor and complete-seed construction live here. X/Y are counted channel
groups (12 field + 6 background channels), not extra retained histories.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from universe24.core import GearType, State, Tensor
from universe24.system.bundle import canonical_bytes, create_bundle
from universe24.system.decoder import default_protocol

SOURCE_PIN = 'e582960f6c9d2d134d3d6b28c08494e8bfafa86a'
PAIRS = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
CG = {pair: 12 + i for i, pair in enumerate(PAIRS)}
CG.update({(j, i): CG[i, j] for i, j in PAIRS})
EPS = ((0, 1, 2, 1), (1, 2, 0, 1), (2, 0, 1, 1),
       (0, 2, 1, -1), (2, 1, 0, -1), (1, 0, 2, -1))


def tensor():
    names = [f'{bank}_{field}{i}' for bank in ('X', 'Y')
             for field in ('D', 'B') for i in range(3)]
    names += [f'C{i}{j}' for i, j in PAIRS]
    terms = []
    for bank, sign in ((0, 1), (1, -1)):
        dst, src = 6 * bank, 6 * (1 - bank)
        for field in (0, 3):
            for i in range(3):
                terms.append((dst + field + i, 6, [(src + field + i, (0, 0, 0), 'b')]))
            for i, j, k, epsilon in EPS:
                for ell in range(3):
                    for shift in (-1, 1):
                        offset = tuple(shift if axis == j else 0 for axis in range(3))
                        terms.append((dst + field + i, sign * epsilon * shift,
                                      [(CG[k, ell], offset, 'b'),
                                       (src + 3 - field + ell, offset, 'b')]))
    for gear in range(12, 18):
        terms.append((gear, 6, [(gear, (0, 0, 0), 'b')]))
    return Tensor([GearType(name, 'audit') for name in names], terms, strict_support=True)


def curl(C, field, L):
    """Unscaled centered curl of C*field; used only during preparation/oracle checks."""
    v = np.asarray([sum(C[i, j] * field[j] for j in range(3))
                    for i in range(3)], dtype=object).reshape(3, L, L, L)
    result = np.zeros_like(v)
    for i, j, k, sign in EPS:
        result[i] += sign * (np.roll(v[k], -1, axis=j) - np.roll(v[k], 1, axis=j))
    return result.reshape(3, L ** 3)


def optical_matrix(values):
    return np.asarray([[values[CG[i, j]] for j in range(3)] for i in range(3)], dtype=object)


def divided_three(values):
    if any((values % 3).flat):
        raise ValueError('Exact prepared horizon exhausted; no rounding or repair is permitted')
    return values // 3


def ideal(values, L, *, inverse=False):
    """First-order shear oracle, never a substitute for Engine advancement."""
    values = np.asarray(values, dtype=object)
    C = optical_matrix(values)
    result = values.copy()
    result[:6], result[6:12] = values[6:12].copy(), values[:6].copy()
    if inverse:
        result[3:6] += divided_three(curl(C, values[6:9], L))
        result[6:9] -= divided_three(curl(C, values[3:6], L))
    else:
        result[:3] += divided_three(curl(C, values[9:12], L))
        result[9:12] -= divided_three(curl(C, values[:3], L))
    return result


def _integer(value, name, minimum):
    if type(value) is not int or value < minimum:
        raise ValueError(f'{name} must be an exact integer >= {minimum}')


def make_bundle(*, L=41, steps=24, geometry='flat', order=12, center=10,
                interface=14, amplitude=1, precision=None):
    """Prepare all fields, old histories and six-valued carries before execution.

    Q=3**(steps+1) clears a finite horizon's denominators in the seed only;
    neither Q nor the horizon changes the fixed tensor or the Engine divisor.
    A supplied lower precision is an explicitly declared negative control.
    """
    for name, value, minimum in (('L', L, 3), ('steps', steps, 2), ('order', order, 2),
                                 ('center', center, 0), ('interface', interface, 1),
                                 ('amplitude', amplitude, 0)):
        _integer(value, name, minimum)
    if steps % 2 or order % 2:
        raise ValueError('steps and binomial order must be even')
    if center >= L or interface >= L or order + 1 > L:
        raise ValueError('pulse and interface must fit the declared lattice')
    if center - order // 2 < 0 or center + order // 2 >= L:
        raise ValueError('initial electric pulse must not wrap the periodic seam')
    if geometry not in ('flat', 'fast', 'step'):
        raise ValueError('unknown static optical background')
    if precision is not None:
        _integer(precision, 'precision', 1)
    preparation_scale = 3 ** (steps + 1) if precision is None else precision
    q = np.ones(L, dtype=object)
    if geometry == 'fast':
        q[:] = 2
    elif geometry == 'step':
        q[interface:] = 2
    plane = np.zeros((18, L), dtype=object)
    plane[CG[0, 0]] = 1
    plane[CG[1, 1]] = plane[CG[2, 2]] = q
    for j in range(order + 1):
        plane[1, center - order // 2 + j] = 6 * math.comb(order, j) * preparation_scale * amplitude
    qD = q * plane[1]
    plane[5] = plane[1] + (np.roll(qD, -1) - np.roll(qD, 1)) // 6
    values = np.repeat(plane, L * L, axis=1)
    previous = ideal(values, L, inverse=True)
    carries = np.asarray([[(gear + x) % 6 for x in range(L)] for gear in range(18)])
    seed = State(L, previous, values, np.repeat(carries, L * L, axis=1))
    law = tensor()
    channels = [{'index': i, 'name': gear.name, 'label': gear.label,
                 'owner': 'classical-test-field' if i < 12 else 'static-optical-background',
                 'purpose': ('counted electromagnetic shear group with complete a,b,r'
                             if i < 12 else 'frozen symmetric C entry with complete a,b,r')}
                for i, gear in enumerate(law.gears)]
    model = {'id': 'maxwell-light-packet-candidate', 'version': '1',
             'domain': 'finite prepared Maxwell test field on a prescribed static optical background',
             'source_pin': SOURCE_PIN, 'preparation': {
                 'L': L, 'steps': steps, 'geometry': geometry, 'order': order, 'center': center,
                 'interface': interface, 'amplitude': amplitude, 'Q': str(preparation_scale),
                 'precision_control': precision is not None, 'q_profile': [int(v) for v in q]},
             'readout': {'time_per_tick': '1/3', 'length_per_cell': '1',
                         'metric': 'Omega^2 diag(-1,1/q^2,1/q,1/q)',
                         'complete_fields': 'X at even ticks; odd Y is a circuit stage'},
             'physical_acceptance': 'blocked',
             'limitations': ['no dynamical Einstein source', 'no operational detector or proper clock',
                             'raw arithmetic clicks are not photons',
                             'finite-grid tails outside the target continuum null cone',
                             'finite prepared precision horizon; centered-grid Nyquist modes']}
    return create_bundle(law, seed, channels=channels, protocol=default_protocol(), model=model)


def export_inputs(bundle, out):
    """Write raw inputs for the existing python -m universe24 prepare command."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    values = {'tensor': bundle.tensor.to_dict(), 'seed': bundle.seed.to_dict(),
              'channels': list(bundle.channels), 'protocol': bundle.protocol, 'model': bundle.model}
    for name, value in values.items():
        (out / f'{name}.json').write_bytes(canonical_bytes(value))
    return out
