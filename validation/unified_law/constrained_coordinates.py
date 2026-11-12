"""One cubic homogeneous Einstein-scalar-dust vector field in constrained coordinates.

Four real spinor coordinates plus beta=log(B) are the common candidate. The
physical decoder obeys the Hamiltonian constraint identically. This module
proves the exact continuum pushforward; the coordinator owns the actual native
or projective Engine compilation and its separate convergence/cost obligations.
"""
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path

import sympy as s

FIELDS = ('sa', 'sb', 'sc', 'se', 'beta')
PHYSICAL_FIELDS = ('k', 'p', 'phi', 'dust', 'beta')
ROOT = Path(__file__).resolve().parents[2]


def physical(values):
    """Quadratic passive decoder; k<=0 and C=0 for every real spinor.

The spatial metric is decoded separately as B=exp(beta), gamma_inverse=B^2 I.
No exponential enters :func:`equations`. Values may be Fractions or symbols.
"""
    a, b, c, e = (values[name] for name in FIELDS[:4])
    sigma = F(1, 2)*(a*a+3*b*b)
    tau = c*c+3*e*e
    momentum = a*c+3*b*e
    transverse = b*c-a*e
    return {'k': -sigma-F(1, 12)*tau,
            'p': momentum,
            'phi': 2*sigma-F(1, 6)*tau-transverse,
            'dust': sigma-F(1, 12)*tau+transverse,
            'beta': values['beta']}


decode = physical


def equations(values, partial=None):
    """Cubic polynomial RHS in synchronous normal proper time, mass squared=1.

``partial`` is unused: this is a homogeneous sector and cannot represent
spatial packets or arbitrary geometry. The signature permits static compilation.
"""
    a, b, c, e = (values[name] for name in FIELDS[:4])
    decoded = physical(values)
    k, phi, dust = (decoded[name] for name in ('k', 'phi', 'dust'))
    difference, total = dust-phi, dust+2*phi
    return {
        'sa': F(3, 2)*a*k+F(1, 4)*a*total+F(1, 2)*b+F(1, 6)*c-F(1, 4)*e*difference,
        'sb': -F(1, 6)*a+F(3, 2)*b*k+F(1, 4)*b*total+F(1, 12)*c*difference+F(1, 6)*e,
        'sc': -a+F(3, 2)*b*difference+F(3, 2)*c*k-F(1, 4)*c*total-F(1, 2)*e,
        'se': -F(1, 2)*a*difference-b+F(1, 6)*c+F(3, 2)*e*k-F(1, 4)*e*total,
        'beta': k,
    }


def reference_rhs(decoded):
    """Independent homogeneous massive Einstein-scalar-dust target."""
    k, p, phi, dust = (decoded[name] for name in PHYSICAL_FIELDS[:4])
    return {'k': 3*k*k-F(1, 2)*(phi*phi+dust*dust),
            'p': 3*k*p-phi, 'phi': p,
            'dust': F(3, 2)*k*dust, 'beta': k}


@lru_cache(maxsize=1)
def symbolic_candidate():
    """Return (symbolic input dict, polynomial RHS dict, physical output dict)."""
    values = dict(zip(FIELDS, s.symbols('sa sb sc se beta', real=True)))
    return values, equations(values), physical(values)


def constraint(decoded):
    return 6*decoded['k']**2-decoded['p']**2-decoded['phi']**2-2*decoded['dust']**2


def symbolic_audit():
    values, drift, decoded = symbolic_candidate()
    variables = tuple(values.values())
    assert s.expand(constraint(decoded)) == 0
    pushed = {name: s.expand(sum(s.diff(decoded[name], values[field])*drift[field]
                                    for field in FIELDS)) for name in PHYSICAL_FIELDS}
    target = reference_rhs(decoded)
    assert all(s.expand(pushed[name]-target[name]) == 0 for name in PHYSICAL_FIELDS)
    degrees = {name: s.Poly(s.expand(value), *variables).total_degree()
               for name, value in drift.items()}
    terms = {name: len(s.Poly(s.expand(value), *variables).terms())
             for name, value in drift.items()}
    assert max(degrees.values()) == 3 and degrees['beta'] == 2
    # Exact continuity and scalar phase identities in the same proper time.
    rho = (decoded['p']**2+decoded['phi']**2)/2+decoded['dust']**2
    pressure = (decoded['p']**2-decoded['phi']**2)/2
    derivative = lambda expression: s.expand(sum(s.diff(expression, values[name])*drift[name]
                                                 for name in FIELDS))
    assert s.expand(derivative(rho)-3*decoded['k']*(rho+pressure)) == 0
    assert s.expand(derivative(decoded['dust']**2)-3*decoded['k']*decoded['dust']**2) == 0
    assert s.expand(derivative(decoded['k'])-(decoded['p']**2+decoded['dust']**2)/2) == 0
    # Decoder is invariant under common phase exp(omega theta), omega^2=-3.
    # A rational phase (cos,sin/√3)=(1/2,1/2) has unit norm and period six.
    a,b,c,e = (values[name] for name in FIELDS[:4])
    phase = {'sa': (a-3*b)/2, 'sb': (a+b)/2,
             'sc': (c-3*e)/2, 'se': (c+e)/2, 'beta': values['beta']}
    rotated = physical(phase)
    assert all(s.expand(rotated[name]-decoded[name]) == 0 for name in PHYSICAL_FIELDS)
    rotated_rhs = equations(phase)
    pushed_phase = {'sa': (drift['sa']-3*drift['sb'])/2,
                    'sb': (drift['sa']+drift['sb'])/2,
                    'sc': (drift['sc']-3*drift['se'])/2,
                    'se': (drift['sc']+drift['se'])/2, 'beta': drift['beta']}
    assert all(s.expand(rotated_rhs[name]-pushed_phase[name]) == 0 for name in FIELDS)
    vertical = {'sa': -3*b, 'sb': a, 'sc': -3*e, 'se': c, 'beta': s.Integer(0)}
    assert all(s.expand(sum(s.diff(decoded[name],values[field])*vertical[field]
                               for field in FIELDS)) == 0 for name in PHYSICAL_FIELDS)
    assert all(s.expand(sum(s.diff(drift[name],values[field])*vertical[field]
                                -s.diff(vertical[name],values[field])*drift[field]
                                for field in FIELDS)) == 0 for name in FIELDS)
    # Wrong physical dynamics remains detectable although C=0 is automatic.
    wrong = dict(drift)
    wrong['sc'] = 0
    wrong_phi_dot = s.expand(sum(s.diff(decoded['phi'],values[name])*wrong[name] for name in FIELDS))
    wrong_residual = s.expand(wrong_phi_dot-decoded['p'])
    assert wrong_residual != 0
    return {'constraint_identity': True, 'all_five_pushforward_equations': True,
            'mass_squared': 1, 'lapse': 1, 'proper_time_rescaling': False,
            'degrees': degrees, 'monomial_counts': terms,
            'continuum_energy_exchange_identity': True,
            'dust_volume_identity': 'd(dust^2)/dt=3*k*dust^2; Bdot=k*B',
            'monotone_curvature_identity': 'kdot=(p^2+dust^2)/2>=0; k<=0',
            'global_future_continuum_bound': 'k0<=k(t)<=0; weighted spinor norm -k is nonincreasing',
            'finite_time_metric_bound': 'exp(beta0+k0*T)<=B(t)<=exp(beta0) for 0<=t<=T',
            'common_phase_equivariance': True,
            'continuous_phase_generator_annihilates_decoder_and_commutes_with_drift': True,
            'wrong_spinor_dynamics_rejected_despite_zero_constraint': True,
            'wrong_dynamics_scalar_residual': str(s.factor(wrong_residual)),
            'scope': 'Homogeneous isotropic neutral radial massive scalar and comoving dust; expanding branch k<=0.'}


def source_builder_audit():
    """Compare to the existing full44 corrected Einstein source, not only our ODE."""
    from validation.completion import formulation
    values, drift, decoded = symbolic_candidate()
    full = {name: s.Integer(0) for name in formulation.FIELDS}
    B = s.symbols('B', positive=True)
    for i in range(3):
        full[f'B{i}{i}'] = B
        full[f'K{i}{i}'] = decoded['k']
    full['phi'], full['Pi_phi'], full['dust_amplitude'] = decoded['phi'], decoded['p'], decoded['dust']
    rhs, constraints, _ = formulation.equations(full, lambda *_: s.Integer(0), mass_squared=1)
    target = reference_rhs(decoded)
    for i in range(3):
        assert s.expand(rhs[f'K{i}{i}']-target['k']) == 0
        assert s.expand(rhs[f'B{i}{i}']-decoded['k']*B) == 0
    assert s.expand(rhs['phi']-target['phi']) == 0
    assert s.expand(rhs['Pi_phi']-target['p']) == 0
    assert s.expand(rhs['dust_amplitude']-target['dust']) == 0
    assert all(s.expand(value) == 0 for value in constraints.values())
    active = {'phi','Pi_phi','dust_amplitude',*(f'B{i}{i}' for i in range(3)),*(f'K{i}{i}' for i in range(3))}
    assert all(s.expand(rhs[name]) == 0 for name in formulation.FIELDS if name not in active)
    return {'actual_full44_source_matches': True, 'all_33_constraints_zero': True,
            'omitted_field_velocities_zero': True, 'same_metric_equation_Bdot_kB': True}


def rational_samples():
    count=0
    for coords in itertools.product(range(-2,3), repeat=4):
        values = dict(zip(FIELDS, [*(F(v,3) for v in coords),F(1,7)]))
        out = physical(values)
        assert constraint(out) == 0 and out['k'] <= 0
        count += 1
    seed = dict(zip(FIELDS, (F(1),F(0),F(0),F(0),F(0))))
    return {'signed_rational_cases':count, 'constraint_and_expanding_branch':True,
            'exact_representable_seed':{name:str(value) for name,value in seed.items()},
            'seed_physical':{name:str(value) for name,value in physical(seed).items()},
            'seed_drift':{name:str(value) for name,value in equations(seed).items()},
            'seed_global_continuum_phase_rate_lower_bound':'1/4 for the nonzero radial scalar pair',
            'arbitrary_rational_physical_seed_exact_lift':False}


def main():
    result={'candidate':'spinor_beta_mass1', 'fields':list(FIELDS),
            'symbolic':symbolic_audit(), 'existing_source':source_builder_audit(),
            'rational_samples':rational_samples(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'status':'exact constrained cubic continuum candidate; Engine realization is a separate shared audit',
            'limitations':['Five continuum coordinates are not five complete compiled retained channels.',
                'Physical decoder is many-to-one; complete retained spinors/carries/history must not be discarded.',
                'No spatial modes, anisotropy, charged phase, Maxwell field or detector is encoded.',
                'Constraint identity alone does not establish the correct dynamics or convergence.']}
    out=ROOT/'runs/unified_law/01_coordinates.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
