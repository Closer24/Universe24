"""Actual projective instability and native linear-wave convergence audit.

Run: python -m validation.completion.time_stability
Only Engine.step advances retained state. References/decoders are passive.
This three-channel linear wave is NOT the corrected45 Einstein candidate.
"""
from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO, lattice
from validation.geometry.team48 import refinement_integer_projective as projective


def bits(state):
    return max(abs(int(v)).bit_length() for a in (state.a, state.b, state.r) for v in a.flat)


def native_tensor(coefficient=1):
    """nu=coefficient/3; fixed-six carries are retained, never projected out.

    One shared period-four sign and two opposite chiral wave fields: 3 total
    channels / 9 retained integers per node. Same tensor for every resolution.
    """
    if type(coefficient) is not int:
        raise TypeError('coefficient must be an exact integer')
    phase = 'wave.sign'
    terms = []
    for field, direction in (('wave.plus', 1), ('wave.minus', -1)):
        for offset, sign in (((1, 0, 0), 1), ((-1, 0, 0), -1)):
            terms.append((field, coefficient * direction * sign,
                          ((phase, ZERO, 'a'), (phase, ZERO, 'b'), (field, offset, 'b')),
                          {'designated_one_way': 'Computational sign; not a physical clock or reciprocal matter coupling.'}))
    return Tensor([GearType(n, label='audit') for n in (phase, 'wave.plus', 'wave.minus')],
                  terms, strict_support=True)


def prepare_native(previous, current, *, L, remainder_offset=0):
    previous, current = np.asarray(previous, dtype=object), np.asarray(current, dtype=object)
    shape = (2, L**3)
    if previous.shape != shape or current.shape != shape:
        raise ValueError(f'Expected physical integer slices {shape}')
    # s_a=s_b=1; previous physical slice = -s_b*a, current = s_a*b.
    a = np.vstack((np.ones((1, L**3), dtype=object), -previous))
    b = np.vstack((np.ones((1, L**3), dtype=object), current))
    r = np.array([(j+remainder_offset) % 6 for j in range(3*L**3)], dtype=object).reshape(3, L**3)
    return State(L, a, b, r)


def decoded(state, scale=1):
    sa, sb = int(state.a[0, 0]), int(state.b[0, 0])
    assert sa in (-1, 1) and sb in (-1, 1)
    assert np.all(state.a[0] == sa) and np.all(state.b[0] == sb)
    factor = 1 if scale == 1 else F(1, scale)
    return -sb * state.a[1:].astype(object) * factor, sa * state.b[1:].astype(object) * factor


def native_scalar_oracle(state, coefficient):
    """Independent scalar address arithmetic, no Tensor evaluator/gather map."""
    L, N = state.L, state.N
    aa, bb, rr = [np.zeros((3, N), dtype=object) for _ in range(3)]
    for x in range(L):
        for y in range(L):
            for z in range(L):
                j = (x*L+y)*L+z
                jp, jm = (((x+1) % L)*L+y)*L+z, (((x-1) % L)*L+y)*L+z
                for g in range(3):
                    u = 0 if g == 0 else (coefficient*(1 if g == 1 else -1)
                         *int(state.a[0, j])*int(state.b[0, j])
                         *(int(state.b[g, jp])-int(state.b[g, jm])))
                    ell, rnew = divmod(2*u+int(state.r[g, j]), 6)
                    aa[g, j], bb[g, j], rr[g, j] = int(state.b[g, j]), ell-int(state.a[g, j]), rnew
    return State(L, aa, bb, rr)


def projective_mode(degree, theta, steps):
    """Real two-component implementation of the exact complex Fourier mode."""
    program = projective.compile_projective(('x', 'y'),
        lambda f, partial: {'x': -f['y'], 'y': f['x']}, dt=theta, degree=degree)
    initial = np.array([[F(1) if j % 2 else F(-1) for j in range(27)],
                        [F(1, 2) if j % 3 else F(-1, 2) for j in range(27)]], dtype=object)
    carries = np.array([j % 6 for j in range(81)], dtype=object).reshape(3, 27)
    seed = projective.prepare(program, initial, L=3, denominator=4, remainders=carries)
    engine, state = Engine(program.tensor), seed
    trace, scalar_checks = [], 0
    for n in range(1, steps+1):
        old = state
        # Independent integer polynomial recurrence, including BOTH retained slices.
        expected = np.empty_like(old.b, dtype=object)
        C, d, h = program.multiplier, degree, theta
        for j in range(27):
            D, X, Y = map(int, old.b[:, j])
            expected[0, j] = C*D**d-int(old.a[0, j])
            expected[1, j] = int(C*D**(d-1)*(X-h*Y))-int(old.a[1, j])
            expected[2, j] = int(C*D**(d-1)*(Y+h*X))-int(old.a[2, j])
        state = engine.step(old)
        assert np.array_equal(state.b, expected) and np.array_equal(state.a, old.b)
        assert np.array_equal(state.r, carries)
        assert engine.inverse_step(state).same_as(old)
        values = projective.readout(program, state)
        for j in range(27):
            initial_norm2 = initial[0, j]**2+initial[1, j]**2
            norm2 = values[0, j]**2+values[1, j]**2
            assert norm2 >= (1+theta**2)**n*initial_norm2
            scalar_checks += 1
        trace.append({'step': n, 'max_retained_bits': bits(state),
                      'amplitude_ratio': math.sqrt(float((values[0, 0]**2+values[1, 0]**2)/F(5, 4))),
                      'proved_lower_bound': float((1+theta**2)**n)**0.5})
    assert engine.rewind(state, steps).same_as(seed)
    return {'status': 'passed', 'physical_stability_gate': 'failed', 'degree': degree,
            'theta': str(theta), 'channels': 3, 'exact_mode_comparisons': scalar_checks,
            'all_six_remainders': True, 'full_rewind': True, 'trace': trace}


def symbolic_invariant():
    a = sp.symbols('a', real=True)
    M = sp.Matrix([[2*sp.I*a, 1], [1, 0]])
    H = sp.Matrix([[1, -sp.I*a], [sp.I*a, 1]])
    assert sp.simplify(M.conjugate().T*H*M-H) == sp.zeros(2)
    return {'status': 'passed', 'identity': 'M* H M = H',
            'H_eigenvalues': ['1-a', '1+a'], 'nu': '1/3',
            'uniform_Euclidean_power_bound': 'sqrt(2)'}


def cayley_history_control():
    """A unitary rational proposal plus linear D growth still has memory bias."""
    # R=(1/5)[[3,-4],[4,3]], exactly the Cayley rotation with h*omega=1.
    names = ('cayley.D', 'cayley.X', 'cayley.Y')
    matrix = ((5, 0, 0), (0, 3, -4), (0, 4, 3))
    tensor = Tensor([GearType(n, label='audit') for n in names],
                    [(names[g], 3*c, ((names[k], ZERO, 'b'),))
                     for g, row in enumerate(matrix) for k, c in enumerate(row) if c],
                    strict_support=True)
    b = np.array([[2]*27, [2]*27, [0]*27], dtype=object)
    r = np.array([j % 6 for j in range(81)], dtype=object).reshape(3, 27)
    seed = State(3, np.zeros_like(b), b, r)
    engine, state, steps = Engine(tensor), seed, 120
    for n in range(1, steps+1):
        old = state
        state = engine.step(old)
        for j in range(27):
            for g in range(3):
                assert int(state.b[g, j]) == sum(matrix[g][k]*int(old.b[k, j]) for k in range(3))-int(old.a[g, j])
        norm2 = F(int(state.b[1, 0])**2+int(state.b[2, 0])**2, int(state.b[0, 0])**2)
        if n == 1:
            assert norm2 == 1
        else:
            assert norm2 > 1
    assert engine.rewind(state, steps).same_as(seed)
    return {'status': 'passed', 'stability_gate': 'failed', 'steps': steps,
            'first_decoded_step_unit_norm': True, 'final_amplitude': math.sqrt(float(norm2)),
            'max_retained_bits': bits(state), 'denominator_bit_growth': 'linear in steps',
            'full_rewind': True, 'all_six_remainders': True}


def native_oracle_test():
    rng = np.random.default_rng(12112026)
    previous = rng.integers(-101, 102, (2, 27)).astype(object)
    current = rng.integers(-101, 102, (2, 27)).astype(object)
    seed = prepare_native(previous, current, L=3)
    tensor, state = native_tensor(), seed
    engine = Engine(tensor)
    changed_carries, max_bits, exact_steps = 0, bits(seed), 180
    for _ in range(exact_steps):
        old = state
        state = engine.step(old)
        assert state.same_as(native_scalar_oracle(old, 1))
        assert engine.inverse_step(state).same_as(old)
        changed_carries += int(np.count_nonzero(state.r != old.r))
        max_bits = max(max_bits, bits(state))
        # Check the exact decoded carry identity with denominator six cleared.
        oldprev, oldnow = decoded(old)
        _, now = decoded(state)
        plus, minus = lattice(3).shift_index((1, 0, 0)), lattice(3).shift_index((-1, 0, 0))
        for g, sign in enumerate((1, -1)):
            lhs = 6*(now[g]-oldprev[g])-2*sign*(oldnow[g, plus]-oldnow[g, minus])
            rhs = int(old.b[0, 0])*(old.r[g+1].astype(object)-state.r[g+1].astype(object))
            assert np.array_equal(lhs, rhs)
    assert changed_carries > 0 and engine.rewind(state, exact_steps).same_as(seed)
    return {'status': 'passed', 'steps': exact_steps, 'scalar_register_comparisons': exact_steps*3*27*3,
            'changed_remainder_entries': changed_carries, 'all_six_remainders': True,
            'signed_seeds': True, 'full_rewind': True, 'max_retained_bits': max_bits,
            'channels': tensor.G, 'retained_integers_per_node': 3*tensor.G,
            'degree': tensor.rank-1, 'strict_support_violations': len(tensor.support_violations()),
            'tensor_fingerprint': tensor.fingerprint}


def native_refinement(L):
    """Fixed T=1/3, h=dx/3; scale=L^3 is preparation/readout only."""
    scale, h, T = L**3, 1/(3*L), 1/3
    x = lattice(L).all_coords()[:, 0]/L
    w = 2*math.pi
    current = np.array([np.sin(w*x), 0.7*np.cos(w*x)])
    # Second-order backward Taylor seed uses initial data and derivatives only.
    derivative = np.array([w*np.cos(w*x), 0.7*w*np.sin(w*x)])
    previous = current-h*derivative-h*h*w*w*current/2
    oldint = np.rint(scale*previous).astype(np.int64).astype(object)
    nowint = np.rint(scale*current).astype(np.int64).astype(object)
    seed = prepare_native(oldint, nowint, L=L)
    state, engine = seed, Engine(native_tensor())
    refprev, refnow = oldint.astype(float)/scale, nowint.astype(float)/scale
    plus, minus = lattice(L).shift_index((1, 0, 0)), lattice(L).shift_index((-1, 0, 0))
    max_bits = bits(seed)
    for _ in range(L):
        state = engine.step(state)
        inc = (refnow[:, plus]-refnow[:, minus])/3
        inc[1] *= -1
        refprev, refnow = refnow, refprev+inc
        max_bits = max(max_bits, bits(state))
    oldout, out = decoded(state, scale)
    oldout, out = oldout.astype(float), out.astype(float)
    target = np.array([np.sin(w*(x+T)), 0.7*np.cos(w*(x-T))])
    rms = float(np.sqrt(np.mean((out-target)**2)))
    # Mean over two fields and nodes, sum over the two time slices.
    carry_error = float(np.sqrt(np.mean((out-refnow)**2+(oldout-refprev)**2)))
    carry_bound = math.sqrt(2)*L*5/(6*scale)
    assert carry_error <= carry_bound+1e-12
    assert engine.rewind(state, L).same_as(seed)
    return {'L': L, 'steps': L, 'physical_time': '1/3', 'dt': str(F(1, 3*L)),
            'amplitude_scale': scale, 'continuum_rms_error': rms,
            'carry_pair_rms_error': carry_error, 'proved_carry_bound': carry_bound,
            'max_retained_bits': max_bits, 'full_rewind': True,
            'tensor_fingerprint': engine.tensor.fingerprint}


def negative_controls():
    L, steps = 4, 40
    profile = np.array([1, 0, -1, 0], dtype=object)
    x = lattice(L).all_coords()[:, 0]
    previous = np.vstack((profile[x], np.zeros(L**3, dtype=object)))
    current = np.zeros_like(previous)
    seed = prepare_native(previous, current, L=L)
    results = []
    for coefficient in (3, 4):
        engine, state = Engine(native_tensor(coefficient)), seed
        for _ in range(steps):
            state = engine.step(state)
        _, out = decoded(state)
        amplitude = max(abs(int(v)) for v in out[0])
        assert amplitude >= steps
        assert engine.rewind(state, steps).same_as(seed)
        results.append({'nu': str(F(coefficient, 3)), 'steps': steps, 'amplitude': amplitude,
                        'seed_amplitude': 1, 'full_rewind': True,
                        'stability_gate': 'failed', 'negative_control': 'passed'})
    assert results[0]['amplitude'] == steps
    assert results[1]['amplitude'] > steps**2
    return results


def main():
    refinement = [native_refinement(L) for L in (12, 24, 48)]
    assert len({r['tensor_fingerprint'] for r in refinement}) == 1
    assert refinement[2]['continuum_rms_error'] < refinement[1]['continuum_rms_error'] < refinement[0]['continuum_rms_error']
    for previous, current in zip(refinement, refinement[1:]):
        current['observed_order'] = math.log2(previous['continuum_rms_error']/current['continuum_rms_error'])
    report = {'status': 'passed', 'scope': 'projective frozen-mode failure and native linear wave only',
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'projective_modes': [projective_mode(2, F(1, 3), 10), projective_mode(3, F(1, 3), 6)],
              'cayley_linear_denominator_negative_control': cayley_history_control(),
              'native_fourier_identity': symbolic_invariant(), 'native_scalar_oracle': native_oracle_test(),
              'native_fixed_time_refinement': refinement, 'native_negative_controls': negative_controls(),
              'nonlinear_einstein_time_integration': 'blocked',
              'same_tensor_as_corrected45': False, 'physical_proper_clock': 'not_tested',
              'full_coupled_physical_acceptance': 'not_tested'}
    folder = Path('runs/completion')
    folder.mkdir(parents=True, exist_ok=True)
    output = folder/'time_stability.json'
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
