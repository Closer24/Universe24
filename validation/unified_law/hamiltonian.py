"""Independent canonical source/dust checks for the shared spinor-beta law.

The selected candidate is imported, never redefined here. Symbolic canonical
Hamilton equations provide an independent physical target. No solver or
Hamiltonian projection advances retained state in this validation module.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as s

from . import constrained_coordinates as coordinates

ROOT = Path(__file__).resolve().parents[2]


def canonical_hamiltonian(volume, volume_momentum, phi, scalar_momentum):
    """Dust proper-time Hamiltonian, 8 pi G=1 and scalar mass squared=1."""
    return (-s.Rational(3, 4)*volume*volume_momentum**2
            +scalar_momentum**2/(2*volume)+volume*phi**2/2)


def canonical_audit():
    """Derive Hamilton equations independently, then push forward spinors."""
    volume, volume_momentum, phi, scalar_momentum, dust_energy = s.symbols(
        'volume volume_momentum phi scalar_momentum dust_energy', real=True)
    canonical = (volume, volume_momentum, phi, scalar_momentum)
    hamiltonian = canonical_hamiltonian(*canonical)
    canonical_rhs = (s.diff(hamiltonian, volume_momentum), -s.diff(hamiltonian, volume),
                     s.diff(hamiltonian, scalar_momentum), -s.diff(hamiltonian, phi))

    values, drift, decoded = coordinates.symbolic_candidate()
    k, physical_momentum, physical_phi, dust = (decoded[name]
        for name in ('k', 'p', 'phi', 'dust'))
    # v=exp(-3 beta)>0 is treated algebraically while its derivative is supplied
    # exactly by the common beta equation. No exponential occurs in the tensor.
    decoded_canonical = (volume, 2*k, physical_phi, volume*physical_momentum)
    substitution = dict(zip(canonical, decoded_canonical))
    volume_rhs = -3*drift['beta']*volume

    def derivative(expression):
        return s.expand(s.diff(expression, volume)*volume_rhs
            +sum(s.diff(expression, values[name])*drift[name] for name in coordinates.FIELDS))

    residuals = [s.expand(derivative(value)-rhs.subs(substitution, simultaneous=True))
                 for value, rhs in zip(decoded_canonical, canonical_rhs)]
    assert all(value == 0 for value in residuals)
    energy = volume*dust**2
    physical_hamiltonian = hamiltonian.subs(substitution, simultaneous=True)
    assert s.expand(physical_hamiltonian+energy) == 0
    assert derivative(energy) == 0
    assert s.expand(derivative(physical_hamiltonian)) == 0

    rho = (physical_momentum**2+physical_phi**2)/2+dust**2
    pressure = (physical_momentum**2-physical_phi**2)/2
    assert s.expand(3*k*k-rho) == 0
    assert s.expand(derivative(rho)-3*k*(rho+pressure)) == 0
    assert s.expand(derivative(k)-(physical_momentum**2+dust**2)/2) == 0
    # A dust-free Hamiltonian cannot silently retain the same sourced metric.
    assert energy != 0
    return {'candidate': 'spinor_beta_mass1',
        'canonical_coordinates': ['v=exp(-3 beta)', 'p_v=2k', 'phi', 'Pi=v*p'],
        'Hamiltonian': '-3*v*p_v^2/4 + Pi^2/(2*v) + v*phi^2/2',
        'dust_energy': 'E=v*dust^2',
        'all_four_canonical_equations_exact': True,
        'Hamiltonian_plus_dust_identically_zero': True,
        'comoving_dust_energy_continuously_constant': True,
        'Hamiltonian_continuously_constant': True,
        'Friedmann_and_continuity_exact': True,
        'Raychaudhuri': 'kdot=(p^2+dust^2)/2 >= 0',
        'metric_domain': 'v=exp(-3 beta)>0 for every finite real beta',
        'physical_time': 'synchronous dust proper time; lapse=1',
        'scope': 'Continuum pushforward of the shared candidate, not exact finite-tick energy conservation.'}


def false_invariant_control():
    """Exact C=0 does not make arbitrary spinor dynamics physical.

    The simple legal-coordinate transformation doubles the spinor amplitude
    while holding beta fixed. C remains identically zero, but E grows by16.
    This is a passive counterexample, not a claimed candidate Engine step.
    """
    values, _, physical = coordinates.symbolic_candidate()
    wrong = {name: (values[name] if name == 'beta' else 2*values[name])
             for name in coordinates.FIELDS}
    after = coordinates.physical(wrong)
    assert s.expand(coordinates.constraint(after)) == 0
    assert s.expand(after['dust']**2-16*physical['dust']**2) == 0
    assert s.expand(after['k']-4*physical['k']) == 0
    return {'constraint_still_zero': True, 'dust_energy_multiplier': 16,
            'wrong_dynamics_rejected_by_dust_mass': True,
            'claim': 'Algebraic Friedmann closure must be accompanied by dynamical/source convergence.'}


def harmonic_interface_audit():
    """Unselected compact quadratic compiler interface, independently derived.

    This is not a second Engine candidate. It records the canonical bridge
    needed if a future native quadratic first-order compiler replaces the
    selected cubic spinor compiler.
    """
    volume, momentum, scalar_momentum, amplitude, dust_energy = s.symbols(
        'v P Pi r E', real=True)
    physical = {'k': momentum/(2*volume), 'p': scalar_momentum/volume,
                'phi': amplitude/volume, 'dust_squared': dust_energy/volume}
    fields = (volume, momentum, scalar_momentum, amplitude)
    drift = (-s.Rational(3, 2)*volume*momentum,
             -amplitude**2-dust_energy*volume,
             -volume*amplitude,
             volume*scalar_momentum-s.Rational(3, 2)*momentum*amplitude)
    constraint = (-s.Rational(3, 4)*momentum**2+scalar_momentum**2/2
                  +amplitude**2/2+dust_energy*volume)
    derivative = lambda expression: s.factor(sum(s.diff(expression, field)*velocity
                                                for field, velocity in zip(fields, drift)))
    assert derivative(constraint) == 0
    # The physical constraint equals -2 C_H / v^2.
    physical_constraint = (6*physical['k']**2-physical['p']**2-physical['phi']**2
                           -2*physical['dust_squared'])
    assert s.factor(physical_constraint+2*constraint/volume**2) == 0
    assert s.factor(derivative(physical['phi'])-volume*physical['p']) == 0
    assert s.factor(derivative(physical['p'])-volume*(3*physical['k']*physical['p']-physical['phi'])) == 0
    assert s.factor(derivative(physical['dust_squared'])-volume*3*physical['k']*physical['dust_squared']) == 0
    raychaudhuri = 3*physical['k']**2-(physical['phi']**2+physical['dust_squared'])/2
    residual = s.factor(derivative(physical['k'])-volume*raychaudhuri)
    assert residual == 0
    return {'selected_for_current_Engine': False,
        'variables': ['v', 'P=2*v*k', 'Pi=v*p', 'r=v*phi'],
        'fixed_parameter': 'E=v*dust^2', 'RHS': [str(value) for value in drift],
        'maximum_polynomial_degree': max(s.Poly(value, *fields).total_degree() for value in drift),
        'constraint': str(constraint), 'constraint_continuously_conserved': True,
        'proper_clock': 'dT/dlambda=v>0',
        'no_extra_phi_register': 'phi=r/v; its equation follows identically',
        'Einstein_pushforward_on_constraint': True,
        'domain': 'v>0, E>=0 and C_H=0',
        'native_complete_map': 'not_implemented; do not transfer selected spinor evidence'}


def main():
    result = {'canonical': canonical_audit(), 'negative_control': false_invariant_control(),
              'future_harmonic_interface': harmonic_interface_audit(),
              'source_sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                  for path in (Path(__file__), Path(coordinates.__file__))},
              'remaining_gates': ['Measure finite-tick comoving dust mass drift on the actual shared tensor.',
                  'Establish fixed-proper-time convergence of all decoded sources and metric.',
                  'A dust-time gauge is not a counted autonomous detector or retained clock record.']}
    path = ROOT/'runs/unified_law/02_hamiltonian.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
