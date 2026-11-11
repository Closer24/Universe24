"""Independent rotation/gradient/local-gauge audit of the charged extension."""
import hashlib
import json
from pathlib import Path

import sympy as s

from . import geometry_triangular as geometry
from . import matter_charged as charged

A = range(3)


def main():
    names = tuple(n for n in charged.FIELDS
                  if n not in geometry.ZERO_FIELDS and n not in geometry.ALIASES)
    fields = {name:s.Symbol(name) for name in names}
    jet = {(name,i):s.Symbol(f'd{i}_{name}') for name in names for i in A}
    rhs, constraints, diagnostic = geometry.equations(
        fields,lambda n,i:jet[n,i],fermi_equations=charged.equations)
    full, _ = geometry.expand(fields,lambda n,i:jet[n,i])
    B = s.Matrix(3,3,lambda a,i:full[f'B{a}{i}'])
    K = s.Matrix(3,3,lambda a,b:full[f'K{min(a,b)}{max(a,b)}'])
    rotation = s.Matrix(3,3,lambda a,b:s.sign(b-a)*K[a,b])
    frame_rate = K+rotation
    potential = s.Matrix([fields[f'A{a}'] for a in A])
    electric = s.Matrix([fields[f'E{a}'] for a in A])
    scalar = s.Matrix([fields['phi'],fields['chi']])
    pi = s.Matrix([fields['Pi_phi'],fields['Pi_chi']])
    generator = s.Matrix([[0,-1],[1,0]])

    # Expected gradient rate is differentiated from its coordinate definition,
    # using only Phi_dot=Pi, Bdot=(K+Omega)B, A_dot=(K+Omega)A-E.
    raw_gradients = [s.Matrix([jet[n,i] for i in A]) for n in ('phi','chi')]
    covariant_gradients = [B*raw_gradients[c]-potential*(generator*scalar)[c] for c in range(2)]
    replace_xi = {fields[f'Xi_{name}{a}']:covariant_gradients[c][a]
                  for c,name in enumerate(('phi','chi')) for a in A}
    expected_potential_rate = frame_rate*potential-electric
    gradient_errors = []
    for c,name in enumerate(('phi','chi')):
        expected = (frame_rate*B*raw_gradients[c]
                    +B*s.Matrix([jet[f'Pi_{name}',i] for i in A])
                    -expected_potential_rate*(generator*scalar)[c]
                    -potential*(generator*pi)[c])
        gradient_errors += [s.expand(rhs[f'Xi_{name}{a}'].subs(replace_xi)-expected[a]) for a in A]
    potential_errors = [s.expand(rhs[f'A{a}']-expected_potential_rate[a]) for a in A]
    assert all(v == 0 for v in gradient_errors+potential_errors)

    # Spatially varying, time-independent infinitesimal electromagnetic gauge
    # transformation: delta Phi=theta J Phi, delta A_a=D_a theta (g=1).
    # Its time derivative changes A_a through the evolving frame itself.
    theta = s.Symbol('theta')
    dtheta = s.Matrix([s.Symbol(f'dtheta{i}') for i in A])
    variations = {v:0 for v in list(fields.values())+list(jet.values())}
    pairs = [('phi','chi'),('Pi_phi','Pi_chi')]
    pairs += [(f'Xi_phi{a}',f'Xi_chi{a}') for a in A]
    for real,imag in pairs:
        variations[fields[real]] = -theta*fields[imag]
        variations[fields[imag]] = theta*fields[real]
        for i in A:
            variations[jet[real,i]] = -theta*jet[imag,i]-dtheta[i]*fields[imag]
            variations[jet[imag,i]] = theta*jet[real,i]+dtheta[i]*fields[real]
    for a in A:
        variations[fields[f'A{a}']] = (B*dtheta)[a]

    def variation(expr):
        return s.expand(sum(s.diff(expr,var)*value for var,value in variations.items() if value != 0))

    expected_variations = {name:0 for name in rhs}
    for real,imag in pairs:
        expected_variations[real] = -theta*rhs[imag]
        expected_variations[imag] = theta*rhs[real]
    for a in A:
        expected_variations[f'A{a}'] = (frame_rate*B*dtheta)[a]
    gauge_errors = [s.expand(variation(value)-expected_variations[name]) for name,value in rhs.items()]
    assert all(v == 0 for v in gauge_errors)
    assert variation(diagnostic['electric_charge']) == 0
    assert all(variation(value) == 0 for value in diagnostic['electric_current'])

    symbols = list(fields.values())+list(jet.values())
    degree = max(s.Poly(s.expand(value),*symbols).total_degree() for value in rhs.values())
    assert degree == 2
    derivatives = set(jet.values())
    for expr in rhs.values():
        for term in s.Add.make_args(s.expand(expr)):
            assert sum(term.as_powers_dict().get(v,0) for v in derivatives) <= 1

    result = {'status':'exact charged frame compatibility and local gauge covariance passed',
              'physical_field_count':len(names),'sign_clock_channels':1,'total_channels':len(names)+1,
              'fields':list(names),'maximum_rhs_degree':degree,
              'single_face_derivative_support':True,'covariant_gradient_kinematic_error':0,
              'potential_rotation_kinematic_error':0,'local_infinitesimal_gauge_covariance_error':0,
              'electric_charge_and_current_gauge_invariant':True,
              'generic_discrete_constraint_preservation_proved':False,
              'source_sha256':{str(path):hashlib.sha256(path.read_bytes()).hexdigest() for path in (
                  Path('experiments/geometry/team48/geometry_triangular.py'),
                  Path('experiments/geometry/team48/geometry_charged_audit.py'),
                  Path('experiments/geometry/team48/matter_charged.py'),
                  Path('experiments/geometry/team48/matter_equations.py'))}}
    path = Path('runs/team48/geometry/charged_audit.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
