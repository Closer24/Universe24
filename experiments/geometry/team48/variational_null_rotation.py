"""Six-channel exact Lorentz mass-shell transport, NOT sourced Einstein GR.

The prepared integer map preserves X*Y-Z1^2-Z2^2 exactly. A fixed, weighted
calibration gives arbitrarily small null-rotation parameters without changing
the Rule3 divisor, tensor or channel count. This is a kinematic primitive:
no spacetime/worldline, stress divergence or Einstein constraint is supplied.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from universe24.core import Engine, State, Tensor

NAMES = ('null.X', 'null.Z1', 'null.Z2', 'null.Y', 'null.U1', 'null.U2')
ZERO = (0, 0, 0)


def build():
    def b(name):
        return (name, ZERO, 'b')
    terms = [(name, 6, (b(name),)) for name in NAMES]
    for parameter in NAMES[-2:]:
        terms.append(('null.Y', 6, (b(parameter), b(parameter), b('null.X')),
                      {'designated_one_way': 'Prepared Lorentz transport invariant, not a reciprocal gravity/matter force.'}))
    return Tensor(NAMES, terms, strict_support=True)


def prepare(subdivision, *, mass=2, parameters=(1, 2), L=3):
    if type(subdivision) is not int or subdivision < 1:
        raise ValueError('positive integer subdivision required')
    if type(mass) is not int or mass <= 0:
        raise ValueError('positive integer mass required')
    if len(parameters) != 2 or any(type(v) is not int for v in parameters):
        raise ValueError('two exact integer parameters required')
    u, v = parameters
    current = [mass, 0, 0, mass*subdivision**2, u, v]
    previous = [mass, -u*mass, -v*mass,
                mass*subdivision**2+(u*u+v*v)*mass, u, v]
    a, b = (np.repeat(np.array(row, dtype=object)[:, None], L**3, axis=1)
            for row in (previous, current))
    r = np.arange(6*L**3).reshape(6, L**3) % 6
    return State(L, a, b, r)


def read_momentum(state, subdivision, node=0):
    """Passive calibrated frame components, not energy conservation in time."""
    x, z1, z2, y = (int(state.b[i, node]) for i in range(4))
    yy = F(y, subdivision**2)
    return ((x+yy)/2, F(z1, subdivision), F(z2, subdivision), (x-yy)/2)


def symbolic_checks():
    t, u, v = sp.symbols('t u v', real=True)
    norm = u*u+v*v
    matrix = sp.Matrix([
        [1+norm*t*t/2, u*t, v*t, norm*t*t/2],
        [u*t, 1, 0, u*t], [v*t, 0, 1, v*t],
        [-norm*t*t/2, -u*t, -v*t, 1-norm*t*t/2]])
    eta = sp.diag(-1, 1, 1, 1)
    assert sp.simplify(matrix.T*eta*matrix-eta) == sp.zeros(4)
    assert sp.simplify(matrix.det()) == 1
    generator = sp.diff(matrix, t).subs(t, 0)
    assert sp.simplify(generator**3) == sp.zeros(4)
    assert sp.simplify(matrix-sp.eye(4)-t*generator-t*t*generator**2/2) == sp.zeros(4)
    assert sp.simplify(sp.diff(matrix, t)-generator*matrix) == sp.zeros(4)
    # A standard exact-energy method already needs a rational inverse even
    # for one harmonic oscillator. This is an obstruction to direct integer
    # substitution, not a no-go for other prepared/projective encodings.
    h = F(1, 2)
    midpoint = ((1-h*h/4)/(1+h*h/4), -h/(1+h*h/4))
    assert midpoint == (F(15, 17), F(-8, 17))
    assert sum(z*z for z in midpoint) == 1
    return {'Lorentz_identity': True, 'determinant_one': True,
            'exact_continuous_null_subgroup': True,
            'implicit_midpoint_unit_oscillator_step': list(map(str, midpoint)),
            'midpoint_direct_integer_seed_is_not_integer_closed': True}


def audit(out):
    tensor = build()
    engine = Engine(tensor)
    rows = []
    for subdivision in (1, 2, 4, 16, 64, 256):
        seed = prepare(subdivision)
        state = seed
        for tick in range(1, subdivision+1):
            before = state
            state = engine.step(state)
            assert engine.inverse_step(state).same_as(before)
            assert np.array_equal(state.r, seed.r)
            x, z1, z2, y, u, v = (int(state.b[i, 0]) for i in range(6))
            assert (x, z1, z2, y) == (2, 2*tick, 4*tick, 2*subdivision**2+10*tick*tick)
            assert x*y-z1*z1-z2*z2 == 4*subdivision**2
            energy, *momenta = read_momentum(state, subdivision)
            assert energy*energy-sum(p*p for p in momenta) == 4
        assert engine.rewind(state, subdivision).same_as(seed)
        rows.append({'subdivision': subdivision, 'updates': subdivision,
                     'physical_transport_parameter': '1',
                     'E_px_py_pz': list(map(str, read_momentum(state, subdivision))),
                     'mass_squared': '4', 'exact_rewind': True})
    assert all(row['E_px_py_pz'] == ['7', '2', '4', '-5'] for row in rows)
    large = prepare(16, mass=2**100+1, parameters=(-3, 5))
    large_next = engine.step(large)
    assert engine.inverse_step(large_next).same_as(large)
    E, *p = read_momentum(large_next, 16)
    assert E*E-sum(v*v for v in p) == (2**100+1)**2
    bad = prepare(4)
    bad.a[:] = bad.b
    following = engine.step(bad)
    E, *p = read_momentum(following, 4)
    wrong_norm = E*E-sum(v*v for v in p)
    assert wrong_norm != 4 and engine.inverse_step(following).same_as(bad)
    report = {'scope': 'exact Lorentz mass-shell transport primitive, not gravity or stress conservation',
              'channels': tensor.G, 'retained_integers_per_node': 3*tensor.G,
              'monomials': len(tensor), 'rank': tensor.rank,
              'tensor_fingerprint': tensor.fingerprint,
              'strict_single_edge': not tensor.support_violations(),
              'same_tensor_for_every_subdivision': True,
              'symbolic': symbolic_checks(), 'refinement': rows,
              'off_prepared_history_control': {'mass_squared_after': str(wrong_norm), 'exact_rewind': True},
              'limitations': ['No geometry dynamics, spacetime path, gravitational backreaction or physical clock.',
                  'Mass shell is preserved; the frame energy component is NOT separately conserved.',
                  'Only a two-parameter null-rotation subgroup of the full Lorentz group.',
                  'Constant retained U1/U2 and prepared histories are required.',
                  'No claim about Einstein Hamiltonian/momentum constraints or stress divergence.'],
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    report = audit(ROOT/'runs/team48/variational/null_rotation.json')
    print(json.dumps(report, indent=2))
