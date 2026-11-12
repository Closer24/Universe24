"""One complete eight-channel native diagonal Bianchi-I research law.

This extends the PR59 volume-history construction by two conserved diagonal
shear charges. Only Engine advances state. Metric roots/logs are passive.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path

import mpmath as mp
import numpy as np

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO, lattice
from universe24.system.bundle import canonical_bytes, create_bundle
from universe24.system.decoder import default_protocol

ROOT = Path(__file__).resolve().parents[2]
PREDECESSOR = '228f581d02971435c0cd70548ff56267378ffc31'
NAMES = ('volume', 'dust_charge', 'scalar_charge', 'reference_velocity',
         'scalar_offset', 'proper_tick', 'shear1', 'shear2')
FROZEN = (1, 2, 3, 4, 6, 7)


def exact_integer(value, name):
    if type(value) is not int:
        raise TypeError(f'{name} must be an exact Python integer')
    return value


def exact_fraction(value, name):
    if type(value) not in (int, F):
        raise TypeError(f'{name} must be an exact integer or Fraction')
    return F(value)


def native_tensor():
    terms = [(name, 6, ((name, ZERO, 'b'),)) for name in NAMES]
    terms.append(('volume', 18, (('dust_charge', ZERO, 'b'),)))
    return Tensor([GearType(name, label='audit') for name in NAMES], terms,
                  strict_support=True)


@dataclass(frozen=True)
class Program:
    N: int
    tensor: Tensor

    @property
    def h(self):
        return F(1, self.N)


def build(N=24):
    exact_integer(N, 'N')
    if N <= 0:
        raise ValueError('N must be positive')
    return Program(N, native_tensor())


def _check_program(program):
    if type(program) is not Program:
        raise TypeError('expected this Bianchi-I Program')
    exact_integer(program.N, 'N')
    if program.N <= 0 or program.tensor.fingerprint != native_tensor().fingerprint:
        raise ValueError('wrong tensor or static time calibration')


def _domain(V, U, D, P, Uref, h):
    if D <= 0 or P == 0 or V <= 0 or U <= 0:
        raise ValueError('mixed expanding chart needs D>0, P!=0, V>0, U>0')
    K = U*U-3*D*V
    if K <= 0 or Uref <= 0 or Uref*Uref <= K:
        raise ValueError('current flow constant and retained reference must be on the positive log chart')
    past_V, past_U = V-h*U+F(3, 4)*D*h*h, U-F(3, 2)*D*h
    if past_V <= 0 or past_U <= 0 or past_U*past_U <= K:
        raise ValueError('retained previous slice is outside the expanding positive-volume chart')


def prepare(program, *, L=3, V=F(7, 3), U=F(4), D=1, P=2,
            S=(1, -1, 0), phi_ref=0, tau_tick=0, remainders=None):
    """Prepare all old/current/carry registers; never impose the constraint."""
    _check_program(program)
    exact_integer(L, 'L')
    lat = lattice(L)
    V, U = exact_fraction(V, 'V'), exact_fraction(U, 'U')
    D, P, phi_ref, tau_tick = (exact_integer(v, name) for v, name in
                             ((D, 'D'), (P, 'P'), (phi_ref, 'phi_ref'), (tau_tick, 'tau_tick')))
    if type(S) not in (tuple, list) or len(S) != 3:
        raise ValueError('supply three exact integer shear charges with zero trace')
    S = tuple(exact_integer(value, 'S') for value in S)
    if sum(S) != 0:
        raise ValueError('diagonal shear charges must have zero trace')
    _domain(V, U, D, P, U, program.h)
    W, J = 4*program.N**2*V, 4*program.N*U
    if W.denominator != 1 or J.denominator != 1:
        raise ValueError('volume/velocity are not integral in the declared static units')
    W, J = int(W), int(J)
    b = (W, D, P, J, phi_ref, tau_tick, S[0], S[1])
    a = (W-J+3*D, D, P, J, phi_ref, tau_tick-1, S[0], S[1])
    a = np.array([[value]*lat.N for value in a], dtype=object)
    b = np.array([[value]*lat.N for value in b], dtype=object)
    if remainders is None:
        r = np.array([[(g+n) % 6 for n in range(lat.N)] for g in range(8)], dtype=object)
    else:
        r = np.array(remainders, dtype=object)
        if r.shape != (8, lat.N) or any(type(v) is not int or not 0 <= v < 6 for v in r.flat):
            raise ValueError('supply all eight integer remainder rows, each in 0..5')
    state = State(L, a, b, r)
    read_conserved(program, state)
    return state


def read_conserved(program, state):
    """Read actual complete history; off-constraint states remain off constraint."""
    _check_program(program)
    if not isinstance(state, State) or state.G != 8 or state.N != state.L**3:
        raise ValueError('a complete eight-channel cube is required')
    for array in (state.a, state.b, state.r):
        if array.shape != (8, state.N):
            raise ValueError('wrong complete-state shape')
        if any(isinstance(v, (bool, np.bool_)) or not isinstance(v, (int, np.integer)) for v in array.flat):
            raise TypeError('every retained entry must be an exact integer')
    if any(not 0 <= int(v) < 6 for v in state.r.flat):
        raise ValueError('invalid remainder')
    if any(any(int(v) != int(row[0]) for v in row) for ar in (state.a, state.b) for row in ar):
        raise ValueError('this Bianchi-I interpretation requires homogeneous physical histories')
    a, b = ([int(v) for v in ar[:, 0]] for ar in (state.a, state.b))
    if any(a[g] != b[g] for g in FROZEN) or b[5]-a[5] != 1:
        raise ValueError('charges/anchors must be frozen and proper-time counter has unit slope')
    W, D, P, reference, phi_ref, tick, S1, S2 = b
    S = (S1, S2, -S1-S2)
    J = W-a[0]+3*D
    V, U, Uref = F(W, 4*program.N**2), F(J, 4*program.N), F(reference, 4*program.N)
    _domain(V, U, D, P, Uref, program.h)
    S2norm = sum(s*s for s in S)
    K = F(3, 2)*(P*P+S2norm)
    constraint_residual = U*U-3*D*V-K
    invariant = J*J-12*D*W-24*program.N**2*(P*P+S2norm)
    assert F(invariant, 16*program.N**2) == constraint_residual
    return {'V': V, 'U': U, 'D': D, 'P': P, 'S': S, 'Uref': Uref,
            'phi_ref': phi_ref, 'tau': F(tick, program.N), 'W': W, 'J': J,
            'K': K, 'K_flow': U*U-3*D*V, 'Q': constraint_residual, 'invariant': invariant,
            'H': tuple(U/(3*V)+F(s, 1)/V for s in S),
            'rho': F(P*P, 2)/V**2+F(D, 1)/V, 'pressure': F(P*P, 2)/V**2}


def _mp(value):
    value = F(value)
    return mp.mpf(value.numerator)/value.denominator


def physical(program, state, *, dps=60):
    """Passive metric/scalar chart, anchored by retained data, never by tick lookup.

    The flow constant U²−3DV, not the desired source constraint, sets the log
    branch. Consequently off-constraint inputs are not repaired by this readout.
    """
    exact_integer(dps, 'dps')
    if dps < 20:
        raise ValueError('physical diagnostic precision must be at least 20 decimal digits')
    r = read_conserved(program, state)
    with mp.workdps(dps):
        V = _mp(r['V'])
        q = mp.sqrt(_mp(r['K_flow']))
        # Exact rational subtraction precedes conversion; log1p avoids loss
        # when current and reference velocities nearly coincide or lie near q.
        # Orient the ratio positively: a backward anchor can otherwise round
        # log1p's argument to -1 at a legal near-root state.
        high, low, sign = (r['U'], r['Uref'], 1) if r['U'] >= r['Uref'] else (r['Uref'], r['U'], -1)
        high_mp, low_mp = _mp(high), _mp(low)
        numerator = 2*q*_mp(high-low)*(low_mp+q)
        denominator = (high_mp+q)*_mp(low**2-r['K_flow'])
        I = sign*mp.log1p(numerator/denominator)/q
        scale = tuple(mp.root(V, 3)*mp.exp(s*I) for s in r['S'])
        r.update(I=+I, phi=mp.mpf(r['phi_ref'])+r['P']*I,
                 a=tuple(+v for v in scale), metric=tuple(+(v*v) for v in scale),
                 scalar_velocity=_mp(F(r['P'], 1)/r['V']),
                 dust_amplitude=mp.sqrt(_mp(F(r['D'], 1)/r['V'])))
    return r


def scalar_step(state, *, source_coupling=True):
    """Direct scalar Rule3 oracle with no tensor evaluator."""
    a, b, r = (np.zeros((8, state.N), dtype=object) for _ in range(3))
    for g in range(8):
        for n in range(state.N):
            u = 6*int(state.b[g, n])
            if g == 0 and source_coupling:
                u += 18*int(state.b[1, n])
            ell, carry = divmod(2*u+int(state.r[g, n]), 6)
            a[g, n], b[g, n], r[g, n] = int(state.b[g, n]), ell-int(state.a[g, n]), carry
    return State(state.L, a, b, r)


def complete_bits(state):
    return max(abs(int(v)).bit_length() for ar in (state.a, state.b, state.r) for v in ar.flat)


def identity(program, seed):
    return {'tensor_sha256': program.tensor.fingerprint,
            'seed_sha256': sha256(canonical_bytes(seed.to_dict())).hexdigest(),
            'N': program.N, 'h': str(program.h), 'channels': seed.G,
            'retained_integers_per_node': 3*seed.G, 'nodes': seed.N}


def trace(N=24, *, steps=None, **preparation):
    program = build(N)
    if steps is None:
        steps = N//8
    exact_integer(steps, 'steps')
    if steps < 0:
        raise ValueError('steps must be nonnegative')
    seed = prepare(program, **preparation)
    states, reads = [seed], [read_conserved(program, seed)]
    engine = Engine(program.tensor)
    for _ in range(steps):
        previous = states[-1]
        current = engine.step(previous)
        assert current.same_as(scalar_step(previous))
        assert engine.inverse_step(current).same_as(previous)
        assert np.array_equal(current.r, seed.r)
        before, after = reads[-1], read_conserved(program, current)
        assert after['V'] == before['V']+program.h*before['U']+F(3, 4)*before['D']*program.h**2
        assert after['U'] == before['U']+F(3, 2)*before['D']*program.h
        assert after['Q'] == reads[0]['Q']
        assert after['tau'] == before['tau']+program.h
        for key in ('D', 'P', 'S', 'Uref', 'phi_ref', 'K_flow'):
            assert after[key] == reads[0][key]
        states.append(current); reads.append(after)
    assert engine.rewind(states[-1], steps).same_as(seed)
    return {'program': program, 'seed': seed, 'states': states, 'readouts': reads,
            'physical': [physical(program, state) for state in states],
            'bits': [complete_bits(state) for state in states], **identity(program, seed)}


def make_bundle(program, seed):
    r = read_conserved(program, seed)
    if r['Q'] != 0:
        raise ValueError('the declared physical research bundle requires Q=0; no repair is performed')
    purposes = ('volume; both histories encode velocity', 'conserved comoving dust mass',
                'conserved signed scalar momentum', 'retained scalar/metric reference velocity',
                'retained scalar integration offset', 'proper-time coordinate; not a material clock',
                'first conserved diagonal shear charge', 'second conserved diagonal shear charge')
    channels = [{'index': i, 'name': gear.name, 'label': gear.label,
                 'owner': 'validation.conservation_closure', 'purpose': purposes[i]+'; complete a,b,r retained'}
                for i, gear in enumerate(program.tensor.gears)]
    model = {'id': 'native-massless-dust-bianchi-i-research', 'version': '1',
             'domain': 'Homogeneous diagonal Bianchi I; expanding mixed massless scalar and dust; Q=0',
             'N': program.N, 'proper_step': str(program.h), 'mass_squared': 0,
             'units': 'c=8*pi*G=1; synchronous lapse1',
             'readout': 'validation.conservation_closure.common.physical; passive full-state diagnostic',
             'metric': 'ds2=-dt2+sum_i[V^(2/3)*exp(2*S_i*I)*dx_i^2]; I_dot=1/V',
             'anchors': 'I=0 at retained Uref; phi=phi_ref+P*I; S3=-S1-S2',
             'spatial_gradients': 'not implemented', 'operational_detector': 'not implemented'}
    return create_bundle(program.tensor, seed, channels=channels,
                         protocol=default_protocol(), model=model)
