"""Independent exact coordinate-geometry audit for the triangular reduction.

Run from repository root:
  python -m experiments.geometry.team48.geometry_triangular_audit
The coordinate oracle constructs connection and Ricci from arbitrary rational
triad jets. It never uses frame_equations to construct expected quantities.
"""
import json
import hashlib
from pathlib import Path
import random

import sympy as s

from universe24.algebra.frame_equations import FIELDS as FULL_FIELDS
from universe24.algebra.frame_equations import equations as full_equations
from experiments.geometry.team48.geometry_triangular import FIELDS, equations, rotate_rhs

A = range(3)


def omega(K):
    return s.Matrix(3,3,lambda a,b:s.sign(b-a)*K[a,b])


def coordinate_oracle(seed):
    """General spatial 2-jets; time jet chosen only to realize Bdot=(K+O)B."""
    rng = random.Random(seed)
    def r():
        return s.Rational(rng.randint(-3,3), rng.randint(1,3))
    def upper():
        return s.Matrix(3,3,lambda a,i:r() if a <= i else 0)
    def symmetric():
        V = s.zeros(3)
        for a in A:
            for b in range(a,3):
                V[a,b] = V[b,a] = r()
        return V
    B = upper()
    for a in A:
        B[a,a] = a+2
    dB = [upper() for i in A]
    ddB = [[s.zeros(3) for j in A] for i in A]
    for i in A:
        for j in range(i,3):
            ddB[i][j] = ddB[j][i] = upper()
    K, dK = symmetric(), [symmetric() for i in A]
    O, dO = omega(K), [omega(dK[i]) for i in A]
    E = B.inv()
    dE = [-E*dB[i]*E for i in A]
    ddE = [[E*dB[j]*E*dB[i]*E+E*dB[i]*E*dB[j]*E-E*ddB[i][j]*E
            for j in A] for i in A]
    Bt = (K+O)*B
    dBt = [(dK[i]+dO[i])*B+(K+O)*dB[i] for i in A]
    Et = -E*Bt*E

    # [e_b,e_c]=C^a_bc e_a, calculated directly in coordinates.
    bracket = [[[sum(B[b,i]*dB[i][c,j]-B[c,i]*dB[i][b,j] for i in A)
                 for j in A] for c in A] for b in A]
    C = [[[sum(bracket[b][c][j]*E[j,a] for j in A) for c in A] for b in A] for a in A]
    Ct = [[[sum(sum(Bt[b,i]*dB[i][c,j]+B[b,i]*dBt[i][c,j]
                   -Bt[c,i]*dB[i][b,j]-B[c,i]*dBt[i][b,j] for i in A)*E[j,a]
                  +bracket[b][c][j]*Et[j,a] for j in A)
            for c in A] for b in A] for a in A]
    dC = [[[[sum(sum(dB[k][b,i]*dB[i][c,j]+B[b,i]*ddB[k][i][c,j]
                     -dB[k][c,i]*dB[i][b,j]-B[c,i]*ddB[k][i][b,j] for i in A)*E[j,a]
                    +bracket[b][c][j]*dE[k][j,a] for j in A)
              for c in A] for b in A] for a in A] for k in A]

    # Koszul formula: Gamma_ab c=<nabla_(e_c)e_b,e_a>.
    def koszul(C):
        return [[[(C[a][c][b]-C[c][b][a]+C[b][a][c])/2 for c in A] for b in A] for a in A]
    G, Gt, dG = koszul(C), koszul(Ct), [koszul(dC[i]) for i in A]

    # Independent coordinate-metric Ricci calculation.
    g, gi = E*E.T, B.T*B
    dg = [dE[i]*E.T+E*dE[i].T for i in A]
    dgi = [dB[i].T*B+B.T*dB[i] for i in A]
    ddg = [[ddE[i][j]*E.T+dE[i]*dE[j].T+dE[j]*dE[i].T+E*ddE[i][j].T
            for j in A] for i in A]
    christoffel = [[[sum(gi[i,l]*(dg[j][l,k]+dg[k][l,j]-dg[l][j,k]) for l in A)/2
                    for k in A] for j in A] for i in A]
    dchristoffel = [[[[sum(dgi[p][i,l]*(dg[j][l,k]+dg[k][l,j]-dg[l][j,k])
                        +gi[i,l]*(ddg[p][j][l,k]+ddg[p][k][l,j]-ddg[p][l][j,k])
                        for l in A)/2 for k in A] for j in A] for i in A] for p in A]
    ricci_coordinate = s.Matrix(3,3,lambda j,k:sum(
        dchristoffel[i][i][j][k]-dchristoffel[k][i][j][i]
        +sum(christoffel[i][i][l]*christoffel[l][j][k]
             -christoffel[i][k][l]*christoffel[l][j][i] for l in A) for i in A))
    ricci_frame = B*ricci_coordinate*B.T

    full = {f'B{a}{i}':B[a,i] for a in A for i in A}
    full.update({f'K{a}{b}':K[a,b] for a in A for b in range(a,3)})
    full.update({f'G{a}{b}{c}':G[a][b][c] for a in A for b in range(a+1,3) for c in A})
    derivatives = {(f'B{a}{j}',i):dB[i][a,j] for a in A for j in A for i in A}
    derivatives.update({(f'K{a}{b}',i):dK[i][a,b] for a in A for b in range(a,3) for i in A})
    derivatives.update({(f'G{a}{b}{c}',i):dG[i][a][b][c]
                        for a in A for b in range(a+1,3) for c in A for i in A})
    rhs, constraints, ricci = equations({n:full[n] for n in FIELDS},lambda n,i:derivatives[n,i])
    connection_errors = [rhs[f'G{a}{b}{c}']-Gt[a][b][c]
                         for a in A for b in range(a+1,3) for c in A if f'G{a}{b}{c}' in FIELDS]
    ricci_errors = list(s.Matrix(ricci)-ricci_frame)
    torsion_errors = [v for n,v in constraints.items() if n.startswith('C')]
    assert all(v == 0 for v in connection_errors+ricci_errors+torsion_errors)
    assert G[0][2][1] == G[0][1][2]
    assert all(dG[i][0][2][1] == dG[i][0][1][2] for i in A)
    return {'seed':seed, 'triad_determinant':str(B.det()), 'all_three_spatial_directions':True,
            'connection_time_derivative_error':0,'ricci_coordinate_oracle_error':0,
            'torsion_error':0,'frobenius_alias_error':0}


def symbolic_checks():
    full = {name:s.Symbol(name) for name in FULL_FIELDS}
    jet = {(name,i):s.Symbol(f'd{i}_{name}') for name in FULL_FIELDS for i in A}
    base, _, _ = full_equations(full, lambda n,i:jet[n,i])
    rotated = rotate_rhs(full,lambda n,i:jet[n,i],base)
    delta_rhs = s.factor(rotated['G021']-rotated['G012'])
    expected = (full['G021']-full['G012'])*(-full['K00']+full['K11']+full['K22'])
    assert s.expand(delta_rhs-expected) == 0
    for name in ('B10','B20','B21'):
        assert s.expand(rotated[name].subs({full[n]:0 for n in ('B10','B20','B21')})) == 0
    rhs, _, _ = equations({n:full[n] for n in FIELDS},lambda n,i:jet[n,i])
    polynomials = [s.Poly(s.expand(v), *list(full.values()), *list(jet.values())) for v in rhs.values()]
    degree = max(p.total_degree() for p in polynomials)
    assert degree == 2
    # Each differential term has one derivative variable, multiplied only by
    # local fields. A centered derivative therefore has one face endpoint.
    derivative_symbols = set(jet.values())
    for value in rhs.values():
        for term in s.Add.make_args(s.expand(value)):
            derivative_degree = sum(term.as_powers_dict().get(v,0) for v in derivative_symbols)
            assert derivative_degree <= 1
    diagonal = [full[f'B{i}{i}'] for i in A]
    determinant = s.prod(diagonal)
    determinant_rhs = sum(s.diff(determinant,diagonal[a])*rhs[f'B{a}{a}'] for a in A)
    assert s.expand(determinant_rhs-determinant*sum(full[f'K{i}{i}'] for i in A)) == 0
    # A restricted, flat Milne slice: B00=1/t, K00=-1/t, others static.
    # Continuum Bdot=-B^2, Kdot=K^2. Forward Euler at dt=t hits B00=0.
    # This deliberately rejects any claim that polynomial gauge reduction
    # by itself preserves nondegeneracy under an arbitrary discrete update.
    return {'field_count':len(FIELDS),'fields':list(FIELDS),'maximum_rhs_degree':degree,
            'single_face_derivative_support':True,'triangular_zero_identity':True,
            'frobenius_difference_rhs':str(delta_rhs),
            'determinant_continuum_identity':'dt(det B) = trace(K) det B',
            'discrete_nondegeneracy_proved':False,
            'generic_constraint_preservation_proved':False}


def positive_shear_control():
    """A genuine positive polynomial clock primitive, not an Einstein solver."""
    def transform(values, direction=1):
        p, q, r, shear = values
        t = direction*shear
        return (p+2*t*q+t*t*r, q+t*r, r, shear)
    traces = []
    for shear in (-3,-1,1,2):
        current = (1,0,1,shear)
        previous = transform(current,-1)
        initial = previous,current
        for _ in range(7):
            p,q,r,t = current
            u = (6*p+6*t*t*r,6*q,6*r,6*t)
            ell_remainder = [divmod(2*v,6) for v in u]
            next_state = tuple(value[0]-old for value,old in zip(ell_remainder,previous))
            assert all(value[1] == 0 for value in ell_remainder)
            assert next_state == transform(current)
            previous,current = current,next_state
            assert current[0]*current[2]-current[1]**2 == 1 and current[0] > 0
        traces.append({'shear':shear,'steps':7,'final':list(current),'determinant':1,'positive':True})
        for _ in range(7):
            p,q,r,t = previous
            u = (6*p+6*t*t*r,6*q,6*r,6*t)
            old_previous = tuple((2*v)//6-new for v,new in zip(u,current))
            previous,current = old_previous,previous
        assert (previous,current) == initial
    return {'status':'exact fixed-six reversible positivity primitive only',
            'geometric_matrix':'[[p,q],[q,r]]','maximum_input_degree':3,
            'einstein_rate_matching_proved':False,'traces':traces}


def main():
    result = {'status':'exact geometric identities passed; not a discrete Einstein constraint solver',
              'symbolic':symbolic_checks(),
              'coordinate_oracle':[coordinate_oracle(seed) for seed in (7,19,31,43)],
              'positive_shear_control':positive_shear_control(),
              'source_sha256':{str(path):hashlib.sha256(path.read_bytes()).hexdigest() for path in (
                  Path('experiments/geometry/team48/geometry_triangular.py'),
                  Path('experiments/geometry/team48/geometry_triangular_audit.py'),
                  Path('universe24/algebra/frame_equations.py'))}}
    path = Path('runs/team48/geometry/triangular_audit.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
