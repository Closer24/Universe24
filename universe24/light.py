"""Native 48-channel, 2O-covariant light streams for the main bundle runtime.

Each quaternion label carries an oriented transverse plane-wave amplitude.
The fixed integer tensor and prepared histories give exact one-face translation
at every tick. There is no precision horizon, idle padding or second engine.
The physical domain is flat, axis-aligned transverse plane waves; general
Maxwell fields, dynamical Einstein backreaction and photon detection are not
established by this component.
"""
from functools import lru_cache
import math

import numpy as np

from .algebra.group_2o import group
from .core import GearType, State, Tensor
from .core.symmetry import CONTRACT, require_equivariant
from .system.bundle import create_bundle
from .system.decoder import default_protocol

MODEL_ID = 'universe24/light-stream48'


def orientations():
    """(propagation, electric, magnetic) frames in the fixed 2O label order."""
    return tuple(tuple(tuple(rotation[i][j] for i in range(3)) for j in range(3))
                 for rotation in group().rotations)


@lru_cache(maxsize=1)
def light_tensor():
    """u_g(x)=3[b_g(x-n_g)+b_g(x+n_g)], n_g=R_g e_x."""
    gears = [GearType(f'light_g{g:02d}', 'official') for g in range(48)]
    terms = []
    for g, (direction, _, _) in enumerate(orientations()):
        for sign in (-1, 1):
            terms.append((g, 3, [(g, tuple(sign * v for v in direction), 'b')]))
    law = Tensor(gears, terms, strict_support=True)
    require_equivariant(law)
    return law


def prepared_predecessor(values, L):
    """Construct a=S^-1(b) once, before evolution; no state advancement here."""
    values = np.asarray(values, dtype=object).reshape(48, L, L, L)
    previous = np.empty_like(values)
    for g, (direction, _, _) in enumerate(orientations()):
        axis = next(i for i, v in enumerate(direction) if v)
        previous[g] = np.roll(values[g], -direction[axis], axis=axis)
    return previous.reshape(48, L ** 3)


def make_light_bundle(*, L=13, axis=0, sign=1, polarization=None, center=4, order=4, amplitude=1):
    """Prepare one transverse plane packet; all 48 complete channels are retained."""
    if polarization is None:
        polarization = 1 if axis == 0 else 0
    for name, value, minimum in (('L', L, 3), ('axis', axis, 0), ('polarization', polarization, 0),
                                 ('center', center, 0), ('order', order, 2), ('amplitude', amplitude, 0)):
        if type(value) is not int or value < minimum:
            raise ValueError(f'{name} must be an exact integer >= {minimum}')
    if type(sign) is not int or sign not in (-1, 1):
        raise ValueError('sign must be +1 or -1')
    if axis > 2 or polarization > 2 or polarization == axis:
        raise ValueError('electric polarization must be transverse to a spatial axis')
    if order % 2 or center - order // 2 < 0 or center + order // 2 >= L:
        raise ValueError('even binomial packet must fit the declared lattice')
    direction = tuple(sign if i == axis else 0 for i in range(3))
    electric = tuple(int(i == polarization) for i in range(3))
    carrier = next(g for g, frame in enumerate(orientations()) if frame[:2] == (direction, electric))
    shape = np.zeros(L, dtype=object)
    for j in range(order + 1):
        shape[center - order // 2 + j] = amplitude * math.comb(order, j)
    coordinates = np.indices((L, L, L)).reshape(3, -1)
    values = np.zeros((48, L ** 3), dtype=object)
    values[carrier] = shape[coordinates[axis]]
    previous = prepared_predecessor(values, L)
    carries = np.asarray([(g + coordinates.sum(axis=0)) % 6 for g in range(48)])
    seed = State(L, previous, values, carries)
    law = light_tensor()
    channels = [{'index': g, 'name': gear.name, 'label': gear.label, 'owner': 'native-light',
                 'purpose': '2O regular-label transverse stream amplitude; complete a,b,r',
                 'propagation': list(frame[0]), 'electric_basis': list(frame[1]), 'magnetic_basis': list(frame[2])}
                for g, (gear, frame) in enumerate(zip(law.gears, orientations()))]
    model = {'id': MODEL_ID, 'version': '1', 'role': 'universe-candidate', 'symmetry': CONTRACT,
             'domain': 'flat spacetime; transverse plane profiles along the six signed cube axes',
             'preparation': {'L': L, 'axis': axis, 'sign': sign, 'polarization': polarization,
                             'center': center, 'order': order, 'amplitude': amplitude, 'carrier': carrier},
             'metric': {'signature': '-+++', 'time_per_tick': '1', 'length_per_edge': '1',
                        'local_null_speed': '1', 'role': 'fixed flat background; no dynamic gravity'},
             'field_readout': 'E=sum_g R_g e_y b_g; B=sum_g R_g e_z b_g',
             'scope': ['48 dynamical channels; no idle padding', 'exact prepared translation at every tick',
                       'two transverse polarizations per propagation direction',
                       'six discrete directions, not arbitrary-direction Maxwell convergence',
                       'no operational detector, Born probabilities or coupled Einstein source']}
    return create_bundle(law, seed, channels=channels, protocol=default_protocol(), model=model)


def electromagnetic_fields(state):
    """Exact passive vector readout. It never feeds the tensor or changes state."""
    if state.G != 48:
        raise ValueError('native light requires all 48 channels')
    electric = np.zeros((3, state.N), dtype=object)
    magnetic = np.zeros_like(electric)
    for g, (_, e, b) in enumerate(orientations()):
        for axis in range(3):
            electric[axis] += e[axis] * state.b[g].astype(object)
            magnetic[axis] += b[axis] * state.b[g].astype(object)
    return electric, magnetic
