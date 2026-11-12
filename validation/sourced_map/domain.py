"""Exact domain and bit-cost audit for the massless sourced volume sector.

This module validates a declared physical interval. It never vetoes, changes or
projects an Engine state. Native reversibility does not extend a singular
physical interpretation through zero spatial volume.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[2]


def exact(value):
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise TypeError('Domain arguments must be exact integers or Fractions')
    return F(value)


@dataclass(frozen=True)
class VolumePoint:
    q: F
    v: F
    scalar_charge: F
    dust_mass: F

    def __post_init__(self):
        for key in ('q', 'v', 'scalar_charge', 'dust_mass'):
            object.__setattr__(self, key, exact(getattr(self, key)))

    @property
    def residual(self):
        return self.v*self.v - 3*self.dust_mass*self.q - F(3, 2)*self.scalar_charge**2


def physical_point(point):
    """A scalar certificate, not a mutation or a runtime acceptance gate."""
    return point.q > 0 and point.dust_mass >= 0 and point.residual == 0


def exact_target(point, elapsed):
    """Independent polynomial solution in a declared physical time coordinate."""
    elapsed = exact(elapsed)
    mass = point.dust_mass
    return VolumePoint(point.q + elapsed*point.v + F(3, 4)*mass*elapsed**2,
                       point.v + F(3, 2)*mass*elapsed,
                       point.scalar_charge, mass)


def interval_certificate(point, elapsed):
    """Check q>0 on the entire interval, including an interior turning point.

    Checking the two saved endpoints is insufficient. A sufficiently large
    interval can pass through both zero-volume singularities and return to q>0.
    The polynomial trajectory continues arithmetically; its physical domain
    does not. Negative elapsed time is checked using the same closed interval.
    """
    elapsed = exact(elapsed)
    if not physical_point(point):
        raise ValueError('Initial point is outside the constrained positive-volume domain')
    samples = [F(0), elapsed]
    if point.dust_mass > 0:
        vertex = -F(2, 3)*point.v/point.dust_mass
        if min(samples) <= vertex <= max(samples):
            samples.append(vertex)
    values = [(time, exact_target(point, time).q) for time in samples]
    min_time, min_volume = min(values, key=lambda item: item[1])
    final = exact_target(point, elapsed)
    return {
        'whole_interval_valid': min_volume > 0,
        'minimum_volume': str(min_volume),
        'minimum_time': str(min_time),
        'initial_volume': str(point.q),
        'final_volume': str(final.q),
        'initial_velocity': str(point.v),
        'final_velocity': str(final.v),
        'both_endpoints_positive': point.q > 0 and final.q > 0,
        'constraint_preserved': final.residual == point.residual,
        'role': 'passive exact physical-domain validation only',
    }


def retained_volume_bound(a, b, mass, radius):
    """Bound |Q_n| for -radius <= n <= radius and Q''=6*mass.

    Histories are counted by applying this bound at radius+1 when a_n=Q_(n-1)
    is included. This bound is on retained integer size, not CPU wall time.
    """
    values = (a, b, mass, radius)
    if any(type(value) is not int for value in values):
        raise TypeError('Retained bound arguments must be exact Python integers')
    if radius < 0:
        raise ValueError('Radius cannot be negative')
    bound = abs(b) + radius*abs(b-a) + 3*abs(mass)*radius*(radius+1)
    return {'absolute_bound': bound, 'bit_bound': bound.bit_length()}


def symbolic_audit():
    q, v, charge, mass, h = s.symbols('q v charge mass h', real=True)
    q1, v1 = q+h*v+s.Rational(3, 4)*mass*h*h, v+s.Rational(3, 2)*mass*h
    invariant = v*v-3*mass*q-s.Rational(3, 2)*charge*charge
    assert s.expand(v1*v1-3*mass*q1-s.Rational(3, 2)*charge*charge-invariant) == 0
    q_back = q1-h*v1+s.Rational(3, 4)*mass*h*h
    assert s.expand(q_back-q) == 0
    assert s.expand(v1-s.Rational(3, 2)*mass*h-v) == 0
    # Physical identity follows from qdot=v and vdot=3M/2 on the constraint.
    k, p = -v/(3*q), charge/q
    d2 = mass/q
    kdot = s.diff(k, q)*v+s.diff(k, v)*s.Rational(3, 2)*mass
    k_residual = s.factor(kdot-(3*k*k-d2/2))
    assert k_residual == 0
    pdot = s.diff(p, q)*v
    assert s.factor(pdot-3*k*p) == 0
    physical_constraint = 6*k*k-p*p-2*d2
    assert s.factor(physical_constraint-s.Rational(2, 3)*invariant/q**2) == 0
    assert s.factor(s.diff(d2, q)*v-3*k*d2) == 0
    return {
        'invariant': 'v^2-3*M*q-(3/2)*P^2',
        'exact_target': 'q1=q+h*v+(3/4)*M*h^2; v1=v+(3/2)*M*h',
        'inverse': 'elapsed -> -elapsed',
        'physical_constraint': '6*k^2-p^2-2*d^2 = (2/(3*q^2))*invariant',
        'physical_fields': 'k=-v/(3*q), p=P/q, d^2=M/q, B=q^(-1/3)',
        'scope': 'mu=0, homogeneous/isotropic/neutral sourced sector; scalar phase handled separately',
        'identities_passed': True,
    }


def domain_audit():
    expanding = VolumePoint(1, 3, 2, 1)
    contracting = VolumePoint(1, -3, 2, 1)
    cases = []
    for initial in (expanding, contracting):
        for duration in (F(0), F(1, 16), F(1, 4), F(-1, 16), F(-1, 4), F(4), F(-4)):
            certificate = interval_certificate(initial, duration)
            assert certificate['constraint_preserved']
            cases.append({'elapsed': str(duration), **certificate})
    # Both endpoints are positive and constrained; the intervening branch is not.
    bad = interval_certificate(contracting, F(4))
    assert bad['both_endpoints_positive'] and not bad['whole_interval_valid']
    assert bad['minimum_volume'] == '-2' and bad['minimum_time'] == '2'
    assert exact_target(contracting, F(4)) == expanding
    assert not interval_certificate(expanding, F(-4))['whole_interval_valid']
    # Strict positivity excludes touching a singularity even if no negative q occurs.
    pure_dust = VolumePoint(3, -3, 0, 1)
    tangent = interval_certificate(pure_dust, F(4))
    assert tangent['both_endpoints_positive'] and tangent['minimum_volume'] == '0'
    assert not tangent['whole_interval_valid']
    # M=0 is a different source subcase, whose domain is linear in time.
    vacuum = VolumePoint(2, 0, 0, 0)
    assert interval_certificate(vacuum, F(100))['whole_interval_valid']
    # Many rational constrained points: expanding branch is forward invariant.
    count = 0
    for mass in range(1, 6):
        for charge in range(-4, 5):
            for velocity in range(1, 10):
                q = (F(velocity**2)-F(3, 2)*charge**2)/(3*mass)
                if q <= 0:
                    continue
                point = VolumePoint(q, velocity, charge, mass)
                for h in (F(1, 128), F(1, 3), F(17)):
                    certificate = interval_certificate(point, h)
                    assert certificate['whole_interval_valid']
                    assert certificate['constraint_preserved']
                    count += 1
    rejected = []
    for value in (True, 0.5, '1/2'):
        try:
            VolumePoint(value, 3, 2, 1)
        except TypeError:
            rejected.append(repr(value))
        else:
            raise AssertionError('Non-exact argument accepted')
    for point in (VolumePoint(0, 0, 0, 0), VolumePoint(1, 3, 2, -1), VolumePoint(1, 4, 2, 1)):
        try:
            interval_certificate(point, F(1, 8))
        except ValueError:
            rejected.append(str(point))
        else:
            raise AssertionError('Invalid initial physical point accepted')
    return {
        'cases': cases,
        'rational_forward_domain_checks': count,
        'cross_and_return_negative': bad,
        'touching_singularity_negative': tangent,
        'rejected_malformed_or_invalid_inputs': rejected,
        'all_forward_time_theorem': 'q>0, M>=0, v>=0 imply q(t)>=q(0)>0 for every t>=0',
        'backward_scope': 'For nonzero sourced expanding solutions, physical validity ends at a finite past singularity.',
        'no_runtime_veto': True,
    }


def integer_bound_audit():
    comparisons = 0
    cases = []
    for a, b, mass in ((7, 12, 1), (-19, 3, 7), (2**100, -(2**99), -11), (0, 0, 0)):
        for radius in (0, 1, 17, 100):
            bound = retained_volume_bound(a, b, mass, radius)
            actual = max(abs(b+n*(b-a)+3*mass*n*(n+1)) for n in range(-radius, radius+1))
            assert actual <= bound['absolute_bound']
            comparisons += 2*radius+1
            cases.append({'a': a, 'b': b, 'mass': mass, 'radius': radius,
                          'actual_max_abs': actual, **bound})
    return {
        'recurrence': 'Q_next=2*Q-Q_old+6*M',
        'closed_form': 'Q_n=b+n*(b-a)+3*M*n*(n+1)',
        'bound': '|Q_n|<=|b|+N*|b-a|+3*|M|*N*(N+1), |n|<=N',
        'all_history_bound': 'Use radius N+1 to cover a_n=Q_(n-1) as well.',
        'growth': 'O(log N) retained bits for fixed initial integers and fixed M; no rounding or discarded carries',
        'scalar_comparisons': comparisons,
        'cases': cases,
        'engine_status': 'This section proves the recurrence bound; the native compiler audit must establish its actual Engine realization.',
    }


def audit():
    return {'status': 'passed_scoped_exact_domain_controls',
            'symbolic': symbolic_audit(), 'domain': domain_audit(),
            'integer_cost': integer_bound_audit(),
            'source_sha256': {str(Path(__file__).relative_to(ROOT)): sha256(Path(__file__).read_bytes()).hexdigest()},
            'limitations': ['Massless sourced homogeneous sector only.',
                            'No physical continuation through zero volume.',
                            'A complete native encoding is a separate obligation; this validator cannot repair an Engine trajectory.',
                            'Proper clocks, spatial modes and massive-scalar closure are not established.']}


def main():
    result = audit()
    path = ROOT/'runs/sourced-map/domain.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'output': str(path),
                      'rational_domain_checks': result['domain']['rational_forward_domain_checks'],
                      'integer_bound_comparisons': result['integer_cost']['scalar_comparisons']}, indent=2))


if __name__ == '__main__':
    main()
