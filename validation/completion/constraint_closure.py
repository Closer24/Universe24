"""Homogeneous Einstein constraint target and exact history-lift obstruction.

Run ``python -m validation.completion.constraint_closure``. The cubic rational
map is a preparation-derived target, NOT an accepted runtime update. The actual
five-channel Rule3 lift is tested and correctly fails constraint preservation.
"""
from fractions import Fraction as F
from functools import lru_cache, reduce
from math import lcm
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as s

from universe24.core import Engine, GearType, Tensor
from universe24.core.lattice import ZERO
from validation.geometry.team48 import refinement_integer_projective as projective
from . import common45, formulation

ROOT = Path(__file__).resolve().parents[2]
FIELDS = ('k', 'p', 'phi', 'dust')


@lru_cache(maxsize=1)
def symbolic_target():
    k, p, phi, dust, h, mu = s.symbols('k p phi dust h mu', real=True)
    state = s.Matrix([k, p, phi, dust])
    form_metric = s.diag(6, -1, -mu, -2)
    force = s.Matrix([3*k*k-(mu*phi*phi+dust*dust)/2,
                      3*k*p-mu*phi, p, 3*k*dust/2])
    generator = s.Matrix([[0, 0, -mu*phi/2, -dust/2],
                          [0, 0, -mu, 0], [-3*phi, 1, 0, 0],
                          [-3*dust/2, 0, 0, 0]])
    assert force == 3*k*state+generator*state
    assert generator.T*form_metric+form_metric*generator == s.zeros(4)
    left = s.eye(4)-h*generator/2
    right = s.eye(4)+h*generator/2
    delta = s.factor(left.det())
    # Symbolic adjugate is used ONCE in preparation; no runtime inverse.
    numerator = (left.adjugate()*right*state).applyfunc(s.expand)
    denominator = s.expand(delta*(1-3*h*k))
    constraint = (state.T*form_metric*state)[0]
    assert s.expand((numerator.T*form_metric*numerator)[0]-delta**2*constraint) == 0
    assert all(s.Poly(value, *state).total_degree() <= 3 for value in numerator)
    assert s.Poly(denominator, *state).total_degree() == 3
    for i in range(4):
        assert s.simplify(s.diff(numerator[i]/denominator, h).subs(h, 0)-force[i]) == 0
    return state, h, mu, form_metric, force, generator, delta, numerator, denominator


def constraint(values, mass_squared=1):
    k, p, phi, dust = values
    return 6*k*k-p*p-mass_squared*phi*phi-2*dust*dust


def algebra_audit():
    state, h, mu, form_metric, force, generator, delta, numerator, denominator = symbolic_target()
    k, p, phi, dust = state
    initial = constraint(state, mu)
    derivative = sum(s.diff(initial, state[i])*force[i] for i in range(4))
    assert s.expand(derivative-6*k*initial) == 0
    defect = s.expand((force.T*form_metric*force)[0])
    assert s.expand(constraint(state+h*force, mu)-(1+6*h*k)*initial-h*h*defect) == 0
    quotient, remainder = s.reduced(defect, [initial], k, p, phi, dust, mu)
    assert s.expand(defect-quotient[0]*initial-remainder) == 0
    strong = {k: -1, p: 0, phi: 2, dust: 1, mu: 1}
    massless = {k: -1, p: 2, phi: 0, dust: 1, mu: 0}
    assert initial.subs(strong) == initial.subs(massless) == 0
    assert defect.subs(strong) == -7 and defect.subs(massless) == -3
    # A nonzero remainder makes the constraint ideal failure exact, not sampled.
    assert remainder != 0
    return {'continuous_constraint_identity': 'Cdot=6*k*C',
        'Euler_identity': 'C(z+hF)=(1+6*h*k)*C(z)+h^2*F.T*form_metric*F',
        'Euler_defect': str(s.factor(defect)),
        'Euler_defect_mod_constraint': str(s.factor(remainder)),
        'strong_massive_coefficient': '-7', 'massless_coefficient': '-3',
        'Cayley_generator_skew_identity': True,
        'Cayley_delta': str(delta),
        'target_constraint_cofactor': '(1-3*h*k)^(-2)',
        'target_first_order_consistency': True,
        'target_numerator_degrees': [s.Poly(v, *state).total_degree() for v in numerator],
        'target_denominator_degree': s.Poly(denominator, *state).total_degree(),
        'target_domain': 'delta!=0 and 1-3*h*k!=0; no global domain or invertibility theorem',
        'target_status': 'exact constrained rational target; not a Rule3 implementation'}


def build_history_lift(*, dt=F(1, 16), mass_squared=1):
    """Compile cubic target numerator/denominator, retaining mandatory history.

    This is an admissible FIVE-channel reduced research tensor. The actual
    recurrence is x_next=multiplier*target_homogeneous(x)-x_old, and is not the
    rational target. Its failed constraint gate is an intended negative control.
    """
    if any(isinstance(value, (float, bool, np.floating, np.bool_))
           for value in (dt, mass_squared)):
        raise TypeError('Use exact rational step and mass squared')
    dt, mass_squared = F(dt), F(mass_squared)
    if dt <= 0:
        raise ValueError('The prepared step must be positive')
    state, h, mu, _, _, _, _, numerator, denominator = symbolic_target()
    symbols = s.symbols('den k p phi dust')
    den, raw = symbols[0], symbols[1:]
    expressions = [denominator, *numerator]
    homogeneous = []
    for expression in expressions:
        polynomial = s.Poly(expression.subs({h: s.Rational(dt), mu: mass_squared}), *state)
        homogeneous.append(s.expand(sum(coefficient*den**(3-sum(powers))
            *s.prod(raw[j]**power for j, power in enumerate(powers))
            for powers, coefficient in polynomial.terms())))
    coefficients = [coefficient for expression in homogeneous
                    for _, coefficient in s.Poly(expression, *symbols).terms()]
    multiplier = max(2, reduce(lcm, (int(s.denom(v)) for v in coefficients), 1))
    names = ('projective.denominator', *(f'projective.{name}' for name in FIELDS))
    terms = []
    for target, expression in zip(names, homogeneous):
        for powers, coefficient in s.Poly(expression, *symbols).terms():
            factors = tuple((names[j], ZERO, 'b') for j, power in enumerate(powers)
                            for _ in range(power))
            terms.append((target, 3*int(multiplier*coefficient), factors))
    tensor = Tensor([GearType(name, label='audit') for name in names], terms, strict_support=True)
    program = projective.ProjectiveProgram(tensor, FIELDS, F(dt), F(1), 3, multiplier)
    return program, tuple(homogeneous), symbols


def history_audit():
    program, polynomials, symbols = build_history_lift()
    values = np.array([[-1]*27, [0]*27, [2]*27, [1]*27], dtype=object)
    carries = np.array([[(g+n) % 6 for n in range(27)] for g in range(5)], dtype=object)
    seed = projective.prepare(program, values, L=3, denominator=4, remainders=carries)
    state, engine = seed, Engine(program.tensor)
    rows = []
    for tick in range(1, 4):
        old = state
        oracle = formulation.previous.scalar_oracle(program.tensor, old)
        substitutions = dict(zip(symbols, map(int, old.b[:, 0])))
        target = [F(polynomial.subs(substitutions)) for polynomial in polynomials]
        state = engine.step(old)
        assert state.same_as(oracle) and engine.inverse_step(state).same_as(old)
        assert np.array_equal(state.r, seed.r)
        assert all(int(state.b[j, 0]) == program.multiplier*target[j]-int(old.a[j, 0])
                   for j in range(5))
        decoded = projective.readout(program, state)
        value = constraint(decoded[:, 0])
        if tick == 1:
            assert value == 0
        elif tick == 2:
            assert value != 0
            # Exact bilinear cross-history source: both target and old slice lie on C=0.
            assert constraint(target[1:]) == constraint(old.a[1:, 0]) == 0
            bilinear = (6*target[1]*int(old.a[1, 0])-target[2]*int(old.a[2, 0])
                        -target[3]*int(old.a[3, 0])-2*target[4]*int(old.a[4, 0]))
            assert constraint(state.b[1:, 0]) == -2*program.multiplier*bilinear
        rows.append({'tick': tick, 'constraint': str(value),
            'constraint_float': float(value), 'max_retained_bits': max(abs(int(v)).bit_length()
                for array in (state.a, state.b, state.r) for v in array.flat)})
    assert engine.rewind(state, 3).same_as(seed)
    assert not program.tensor.support_violations()
    return {'channels': 5, 'retained_integers_per_node': 15, 'degree': 3,
        'monomials': len(program.tensor), 'multiplier': program.multiplier,
        'tensor_sha256': program.tensor.fingerprint, 'strict_face_support': True,
        'nodes': 27, 'all_six_remainders': True, 'oracle_and_full_rewind': True,
        'first_tick_constraint_zero': True, 'second_tick_constraint_gate': 'failed',
        'cross_history_defect_identity': True, 'rows': rows,
        'scope': 'Reduced homogeneous four-field target only; not appended to full45'}


def common_first_step_audit():
    program = common45.build45()
    seed = common45.weak_seed(program)
    before = common45.decode_fields(program, seed)
    after_state = Engine(program.tensor).step(seed)
    after = common45.decode_fields(program, after_state)
    fields = [before['K00'], before['Pi_phi'], before['phi'], before['dust_amplitude']]
    target_state, h, mu, form_metric, force, *_ = symbolic_target()
    substitutions = dict(zip(target_state, fields)) | {mu: 1, h: s.Rational(program.dt)}
    predicted = (program.dt**2*(force.T*form_metric*force)[0]).subs(substitutions)
    measured = constraint([after['K00'], after['Pi_phi'], after['phi'], after['dust_amplitude']])
    _, constraints, _ = formulation.equations(after, lambda *_: F(0))
    assert constraint(fields) == 0 and measured == predicted == constraints['H']
    assert measured != 0
    return {'tensor_sha256': program.tensor.fingerprint,
        'seed_sha256': hashlib.sha256(common45.canonical_bytes(seed.to_dict())).hexdigest(),
        'initial_constraint': '0', 'first_step_constraint': str(measured),
        'general_identity_matches_actual_full45': True, 'discrete_constraint_gate': 'failed'}


def main():
    result = {'algebra': algebra_audit(), 'actual_reduced_history_lift': history_audit(),
        'common45': common_first_step_audit(),
        'source_sha256': {str(Path(__file__).relative_to(ROOT)): hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        'status': 'target theorem passed; mandatory-memory implementation constraint gate failed',
        'limitations': ['No full45 constraint-preserving tensor supplied.',
            'Rational target needs nonzero denominators and is not a global map theorem.',
            'Removing old history, resetting it or feeding an external solver is forbidden.',
            'Native linear-wave and nonlinear potential laws do not implement this target.']}
    path = ROOT/'runs/completion/07_constraint_closure.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
