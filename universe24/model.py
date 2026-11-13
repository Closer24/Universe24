"""One fixed reversible signal/clock coupling, with an explicit positive sector.

Six directional face views share the 48-channel node budget. The proven
Boolean sector selects one orientation at a time; simultaneous independent
six-face populations, a Lorentzian metric and Einstein dynamics are unproved.
Preparation and readouts never advance the Engine.
"""
from __future__ import annotations
from functools import lru_cache
import itertools
import numpy as np
from universe24.algebra.group_2o import group
from universe24.core import State, Tensor, GearType
from universe24.core.symmetry import require_equivariant, CONTRACT
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol

MODEL_ID = 'universe24/clock-collision48'
ZERO = (0, 0, 0)
MEMORY, CLOCK, SELECTOR, COUNTER = 2, 6, 1, 4


def frames():
    return tuple(tuple(r[i][0] for i in range(3)) for r in group().rotations)


def roles(root=0):
    if type(root) is not int or not 0 <= root < 48: raise ValueError('root must be an exact label in 0..47')
    row=group().multiplication[root]
    return dict(signal=root,memory=row[MEMORY],clock=row[CLOCK],selector=row[SELECTOR],counter=row[COUNTER])


def collision(p,m,c):
    return p+m*c-p*m,c+p*m-p*c,m+p*c-m*c


@lru_cache(maxsize=1)
def coupling_tensor():
    """The sole built-in law; all retained values use the fixed positive bias."""
    bias = 1
    original=[(g,6,[(g,ZERO,'b')]) for g in range(48)]
    def add(target,coef,*args): original.append((target,coef,[(g,at,'b') for g,at in args]))
    tab=group().multiplication
    for g,n in enumerate(frames()):
        minus=tuple(-v for v in n)
        m,c,s=(tab[g][v] for v in (MEMORY,CLOCK,SELECTOR))
        gate=(s,ZERO)
        # F=C S: stream signal, then an onsite reversible collision.
        for coef,factors in [(3,[(g,minus)]),(-3,[(g,ZERO)]),(3,[(m,ZERO),(c,ZERO)]),(-3,[(g,minus),(m,ZERO)])]:
            add(g,coef,gate,*factors)
        for target,items in [(m,[(3,[(c,ZERO)]),(-3,[(m,ZERO)]),(3,[(g,minus),(m,ZERO)]),(-3,[(g,minus),(c,ZERO)])]),
                             (c,[(3,[(m,ZERO)]),(-3,[(c,ZERO)]),(3,[(g,minus),(c,ZERO)]),(-3,[(m,ZERO),(c,ZERO)])])]:
            for coef,factors in items:add(target,coef,gate,*factors)
        # F^-1=S^-1 C: inverse collision is C itself.
        for coef,factors in [(3,[(g,n)]),(-3,[(g,ZERO)]),(3,[(m,n),(c,n)]),(-3,[(g,n),(m,n)])]:
            add(g,coef,gate,*factors)
        for target,items in [(m,[(3,[(c,ZERO)]),(-3,[(m,ZERO)]),(3,[(g,ZERO),(m,ZERO)]),(-3,[(g,ZERO),(c,ZERO)])]),
                             (c,[(3,[(m,ZERO)]),(-3,[(c,ZERO)]),(3,[(g,ZERO),(c,ZERO)]),(-3,[(m,ZERO),(c,ZERO)])])]:
            for coef,factors in items:add(target,coef,gate,*factors)
    terms=[]
    # Affine conjugation b=bias+x retains exactly the same Rule3 divider.
    for target,coefficient,factors in original:
        for chosen in itertools.product((False,True),repeat=len(factors)):
            omitted=len(factors)-sum(chosen)
            coefficient_shifted=coefficient*(-bias)**omitted
            if coefficient_shifted:
                terms.append((target,coefficient_shifted,[factor for factor,keep in zip(factors,chosen) if keep]))
    terms.extend((g,6*bias,[]) for g in range(48) if bias)
    law=Tensor([GearType(f'clock_g{g:02d}','official') for g in range(48)],terms,strict_support=True)
    require_equivariant(law)
    return law


def _size(L):
    if type(L) is not int or L < 3:
        raise ValueError('L must be an exact integer >=3')


def _exact_array(values):
    result = np.asarray(values, dtype=object)
    if any(isinstance(v, (bool, np.bool_)) or
           not isinstance(v, (int, np.integer)) for v in result.flat):
        raise ValueError('exact integers required')
    return result


def sector_map(values, L, root=0, *, inverse=False):
    """Independent Boolean oracle on the declared sector, never runtime input.

    The isolated retained counter advances by one. Its inverse at raw value
    one reaches zero; future-positive seeds therefore start it at two or more.
    """
    _size(L)
    rr = roles(root)
    x = _exact_array(values) - 1
    if x.shape != (48, L**3):
        raise ValueError('48 complete channel rows required')
    if np.any(np.delete(x, list(rr.values()), axis=0)) or np.any(x[rr['selector']] != 1):
        raise ValueError('outside selector-separated prepared sector')
    bits = x[[rr[k] for k in ('signal', 'memory', 'clock')]]
    if np.any((bits != 0) & (bits != 1)) or np.any(x[rr['counter']] < 0):
        raise ValueError('Boolean deviations and positive counter required')
    p, m, c = (x[rr[k]].reshape(L, L, L) for k in ('signal', 'memory', 'clock'))
    direction = frames()[root]
    axis = next(k for k, v in enumerate(direction) if v)
    sign = direction[axis]
    table = {(0,0,0):(0,0,0), (0,0,1):(0,1,0), (0,1,0):(0,0,1), (0,1,1):(1,1,0),
             (1,0,0):(1,0,0), (1,0,1):(1,0,1), (1,1,0):(0,1,1), (1,1,1):(1,1,1)}
    if not inverse:
        p = np.roll(p, sign, axis=axis)
    output = np.empty((3, L**3), dtype=object)
    for site, triple in enumerate(zip(p.flat, m.flat, c.flat)):
        output[:, site] = table[tuple(map(int, triple))]
    if inverse:
        output[0] = np.roll(output[0].reshape(L,L,L), -sign, axis=axis).reshape(-1)
    result = x.copy()
    for name, row in zip(('signal', 'memory', 'clock'), output):
        result[rr[name]] = row
    result[rr['counter']] += -1 if inverse else 1
    return result + 1


def prepare_fields(*, L, signal, memory, clock, root=0, counter_start=2):
    """Prepare explicit spatial Boolean fields and a counted coordinate clock."""
    _size(L)
    rr = roles(root)
    if type(counter_start) is not int or counter_start < 2:
        raise ValueError('counter_start must be an exact integer >=2')
    values = np.ones((48, L**3), dtype=object)
    values[rr['selector']] = 2
    values[rr['counter']] = counter_start
    for name, supplied in (('signal', signal), ('memory', memory), ('clock', clock)):
        raw = _exact_array(supplied)
        if raw.shape not in ((L**3,), (L,L,L)):
            raise ValueError('every field must explicitly cover the lattice')
        if np.any((raw != 0) & (raw != 1)):
            raise ValueError('Boolean deviations required')
        values[rr[name]] += raw.reshape(-1)
    previous = sector_map(values, L, root, inverse=True)
    return State(L, previous, values, np.ones((48,L**3), dtype=int))


def _planes(L, root, sites):
    sites = tuple(sites)
    if any(type(site) is not int or not 0 <= site < L for site in sites):
        raise ValueError('plane positions must be exact integers in 0..L-1')
    axis = next(k for k, v in enumerate(frames()[root]) if v)
    coordinates = np.indices((L,L,L))[axis].reshape(-1)
    return np.isin(coordinates, sites).astype(object) * 1


def make_model_bundle(*, L=7, root=0, signal_sites=(0,), memory_sites=(),
                      clock_sites=(2,), counter_start=2):
    """Seal the one built-in model; these are preparations of the same tensor."""
    _size(L)
    rr = roles(root)
    seed = prepare_fields(L=L, root=root, counter_start=counter_start,
                          signal=_planes(L,root,signal_sites),
                          memory=_planes(L,root,memory_sites),
                          clock=_planes(L,root,clock_sites))
    tensor = coupling_tensor()
    return create_bundle(tensor, seed,
        channels=[{'index':g, 'name':gear.name, 'label':gear.label,
                   'owner':'clock-collision48',
                   'purpose':'complete regular channel; no uncounted link state'}
                  for g,gear in enumerate(tensor.gears)],
        protocol=default_protocol(),
        model={'id':MODEL_ID, 'version':'1', 'role':'universe-candidate',
               'symmetry':CONTRACT, 'root':root, 'bias':1, 'roles':rr,
               'domain':'one selected orientation; spatial Boolean signal/clock fields',
               'counter':'prepared coordinate counter, not material proper time',
               'physics_acceptance':'blocked'})


def electromagnetic_fields(state):
    """Root-independent 2O-vector readout selected by retained selectors.

    On the prepared sector this is E=e_root*p, B=m_root*p. It is not the
    prior ungated sum of all channel frames and establishes no general
    Maxwell equation or photon-number interpretation.
    """
    if state.G!=48:raise ValueError('48 complete channels required')
    x=state.b.astype(object)-1
    electric=np.zeros((3,state.N),dtype=object)
    magnetic=np.zeros_like(electric)
    tab=group().multiplication
    for g,rotation in enumerate(group().rotations):
        weight=x[g]*x[tab[g][SELECTOR]]
        for axis in range(3):
            electric[axis]+=rotation[axis][1]*weight
            magnetic[axis]+=rotation[axis][2]*weight
    return electric,magnetic


def excitation_account(state, root=0):
    """Logical charges on the declared sector, not a calibrated physical energy."""
    sector_map(state.b, state.L, root)  # validate the readout domain
    rr = roles(root)
    p, m, c = (state.b[rr[k]] - 1 for k in ('signal', 'memory', 'clock'))
    return {'free_signal': sum(map(int, p)),
            'stored_signal': sum(map(int, m*c)),
            'signal_charge': sum(map(int, p+m*c)),
            'clock_sites': sum(map(int, m+c-m*c))}
