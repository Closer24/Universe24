"""Symbolic support/parity and exact Wronskian checks, before Engine evidence."""
import hashlib
import json
from pathlib import Path
import random

import numpy as np
import sympy as s

from universe24.core.lattice import lattice
from . import geometry_positive_pairs as geometry
from . import matter_charged as charged


def main():
    names = geometry.replace_fields(charged.FIELDS)
    fields = {name:s.Symbol(name) for name in names}
    jet = {(name,i):s.Symbol(f'd{i}_{name}') for name in names for i in range(3)}
    rhs,_,_ = geometry.equations(fields,lambda n,i:jet[n,i],fermi_equations=charged.equations)
    offsets = geometry.phase_offsets(names)
    symbols = list(fields.values())+list(jet.values())
    symbol_names = {value:name for name,value in fields.items()}
    symbol_names.update({value:name for (name,_),value in jet.items()})
    degree = max(s.Poly(s.expand(value),*symbols).total_degree() for value in rhs.values())
    assert degree == 3
    derivatives = set(jet.values())
    cubic_count = 0
    for name,expr in rhs.items():
        for term in s.Add.make_args(s.expand(expr)):
            powers = term.as_powers_dict()
            term_degree = sum(powers.get(v,0) for v in symbols)
            assert sum(powers.get(v,0) for v in derivatives) <= 1
            if term_degree == 3:
                cubic_count += 1
                parity = offsets[name]+sum(powers.get(v,0)*offsets[symbol_names[v]] for v in symbols)
                assert parity % 2 == 1, (name,term,parity)

    # Exact continuum coordinate change, without a division by an amplitude.
    for a in range(3):
        p,q = fields[f'diag_p{a}'],fields[f'diag_q{a}']
        assert s.expand(2*p*rhs[f'diag_p{a}']+2*q*rhs[f'diag_q{a}']
                        -fields[f'K{a}{a}']*(p*p+q*q)) == 0

    p,q,past_p,past_q,rate = s.symbols('p q past_p past_q rate')
    next_p,next_q = past_p+rate*p,past_q+rate*q
    assert s.expand(next_p*q-next_q*p+(p*past_q-q*past_p)) == 0
    rng = random.Random(714)
    controls = []
    for axis in range(3):
        past_p,past_q,p,q = 1,1,1,0
        initial_area = p*past_q-q*past_p
        minimum_diagonal = p*p+q*q
        for step in range(24):
            rate = rng.randint(-4,4)
            past_p,past_q,p,q = p,q,past_p+rate*p,past_q+rate*q
            assert p*past_q-q*past_p == (-1)**(step+1)*initial_area
            assert p*p+q*q > 0
            minimum_diagonal = min(minimum_diagonal,p*p+q*q)
        controls.append({'axis':axis,'steps':24,'minimum_diagonal':minimum_diagonal,
                         'final_diagonal':p*p+q*q,'absolute_wronskian':abs(initial_area)})

    # A deliberate product-rule counterexample must remain visible in passive
    # diagnostics: at the origin p=0, p(+y)=2,p(-y)=0 gives D(p²)=2,2pDp=0.
    lat = lattice(3)
    snapshot = {name:np.zeros(lat.N,dtype=object) for name in geometry.FIELDS}
    for axis in range(3):
        snapshot[f'diag_q{axis}'][:] = 1
    snapshot['diag_p0'][lat.index(0,1,0)] = 2
    def partial(name,axis):
        plus = tuple(int(i == axis) for i in range(3))
        minus = tuple(-v for v in plus)
        return (snapshot[name][lat.shift_index(plus)]-snapshot[name][lat.shift_index(minus)])/s.Integer(2)
    _,jet_constraints,_ = geometry.equations(snapshot,partial)
    literal_constraints,_ = geometry.sampled_constraints(snapshot,lat)
    origin = lat.index(0,0,0)
    assert jet_constraints['C010'][origin] == 0
    assert literal_constraints['C010'][origin] == -2

    result = {'status':'symbolic cubic parity and positive-pair identities passed; Engine compilation separate',
              'physical_fields':len(names),'prospective_sign_clock_channels':1,
              'prospective_total_channels':len(names)+1,'maximum_physical_rhs_degree':degree,
              'single_face_derivative_support':True,'cubic_monomials':cubic_count,
              'every_cubic_staggered_phase_parity_odd':True,'phase_offsets':offsets,
              'continuum_Bdiag_equation_identity':True,'wronskian_sign_flip_identity':True,
              'exact_scalar_leapfrog_controls':controls,
              'composite_derivative_negative_control':{'constraint':'C010','continuum_jet_value':0,
                                                       'literal_centered_value':-2},
              'engine_compiled_in_this_audit':False,'constraint_preservation_proved':False,
              'controlled_refinement_of_computational_second_mode_proved':False,
              'source_sha256':{str(path):hashlib.sha256(path.read_bytes()).hexdigest() for path in (
                  Path('experiments/geometry/team48/geometry_positive_pairs.py'),
                  Path('experiments/geometry/team48/geometry_positive_audit.py'),
                  Path('experiments/geometry/team48/matter_charged.py'))}}
    path = Path('runs/team48/geometry/positive_pairs_audit.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
