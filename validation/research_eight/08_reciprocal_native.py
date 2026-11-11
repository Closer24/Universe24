"""Reciprocal native-lattice edge primitive and compiler-obstruction controls.

This is a two-field mechanical primitive, not an Einstein geometry model.
Run: python -m validation.research_eight.08_reciprocal_native
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO, lattice
from universe24.core.tensor import AcyclicityError


ROOT = Path(__file__).resolve().parents[2]


def make_tensor(*, one_way=False):
    terms = [(name, 6, ((name, ZERO, 'b'),)) for name in ('phi', 'g')]
    def term(target, coeff, factors):
        terms.append((target, coeff, tuple((name, offset, 'b') for name, offset in factors)))
    for sign in (-1, 1):
        edge = (sign, 0, 0)
        # F_phi=(g_i^2+g_j^2)*(phi_j-phi_i), for each adjacent edge.
        for gpos in (ZERO, edge):
            term('phi', 1, [('g', gpos), ('g', gpos), ('phi', edge)])
            term('phi', -1, [('g', gpos), ('g', gpos), ('phi', ZERO)])
        if not one_way:
            # F_g=-g_i*(phi_j-phi_i)^2 from the SAME edge potential.
            term('g', -1, [('g', ZERO), ('phi', edge), ('phi', edge)])
            term('g', 2, [('g', ZERO), ('phi', edge), ('phi', ZERO)])
            term('g', -1, [('g', ZERO), ('phi', ZERO), ('phi', ZERO)])
    return Tensor([GearType('phi', label='audit'), GearType('g', label='audit')],
                  terms, strict_support=True)


def forces(b, lat, *, one_way=False):
    phi, g = b
    fphi, fg = np.zeros_like(phi), np.zeros_like(g)
    for sign in (-1, 1):
        ix = lat.shift_index((sign, 0, 0))
        difference = phi[ix]-phi
        fphi += (g*g+g[ix]*g[ix])*difference
        if not one_way:
            fg -= g*difference*difference
    return np.asarray([fphi, fg], dtype=object)


def scalar_step(state, *, one_way=False):
    force = forces(state.b, lattice(state.L), one_way=one_way)
    pn = 6*(state.b-state.a)+state.r+2*force
    return State(state.L, state.b, state.b+pn//6, pn%6)


def potential_identity():
    x, y, g, h = sp.symbols('x y g h')
    v = (g*g+h*h)*(y-x)**2/2
    expected = [(g*g+h*h)*(y-x), -(g*g+h*h)*(y-x),
                -g*(y-x)**2, -h*(y-x)**2]
    actual = [-sp.diff(v, s) for s in (x,y,g,h)]
    assert all(sp.expand(a-b) == 0 for a,b in zip(actual, expected))
    assert sp.expand(actual[0]+actual[1]) == 0
    # Reciprocity is a derivative identity; deleting the g reaction breaks it.
    mixed = sp.diff(actual[0], g)
    assert sp.expand(mixed-sp.diff(actual[2], x)) == 0
    assert mixed.subs({x:0,y:1,g:1,h:1}) == 2
    return {'edge_potential':'(g_i^2+g_j^2)*(phi_j-phi_i)^2/2',
            'force_gradient_and_reciprocity':'passed',
            'shift_symmetry_opposite_phi_forces':'passed',
            'one_way_mixed_derivative_defect':2}


def audit(one_way=False):
    tensor = make_tensor(one_way=one_way)
    engine = Engine(tensor)
    lat = lattice(3)
    x = lat.all_coords()[:,0].astype(int)
    b = np.asarray([[int(i==1) for i in x], [1]*lat.N],dtype=object)
    r = np.asarray([[(i+g)%6 for i in range(lat.N)] for g in range(2)],dtype=object)
    seed = State(3,b,b,r)
    state = seed
    momentum = int(sum(6*(seed.b[0]-seed.a[0])+seed.r[0]))
    rows = []
    for tick in range(7):
        pi = 6*(state.b-state.a)+state.r
        assert int(sum(pi[0])) == momentum
        rows.append({'tick':tick, 'total_phi_native_momentum':int(sum(pi[0])),
                     'max_bits':state.max_abs().bit_length(),
                     'complete_state_max_bits':max(abs(int(v)).bit_length()
                                                   for arr in (state.a,state.b,state.r)
                                                   for v in arr.flat),
                     'g_zero_nodes':sum(int(v==0) for v in state.b[1]),
                     'g_min':str(min(state.b[1])), 'g_max':str(max(state.b[1]))})
        if tick==6:
            break
        expected = scalar_step(state,one_way=one_way)
        after = engine.step(state)
        assert after.same_as(expected)
        assert engine.inverse_step(after).same_as(state)
        state = after
    assert engine.rewind(state,6).same_as(seed)
    if one_way:
        assert np.array_equal(state.b[1],seed.b[1])
    else:
        assert rows[1]['g_zero_nodes']>0
        assert not np.array_equal(state.b[1],seed.b[1])
    return {'case':'one_way_negative' if one_way else 'reciprocal',
            'channels':tensor.G,'integers_per_node':3*tensor.G,
            'monomials':len(tensor),'degree':tensor.rank-1,
            'strict_face_support':not tensor.support_violations(),
            'tensor_sha256':tensor.fingerprint,'all_six_remainders_in_seed':True,
            'native_scalar_oracle':True,'step_inverse_full_rewind':True,
            'total_phi_native_momentum_conserved':True,'rows':rows,
            'einstein_geometry':'not_tested','physical_energy':'not_tested',
            'continuum_refinement':'not_tested'}


def compiler_controls():
    try:
        Tensor(['q'],[('q',1,(('q',ZERO,'a'),))])
    except AcyclicityError:
        self_a_rejected=True
    else:
        raise AssertionError('self-a read accepted')
    try:
        Tensor(['q'],[('q',1,(('q',ZERO,'r'),))])
    except (ValueError,TypeError):
        r_read_rejected=True
    else:
        raise AssertionError('r input accepted')
    # q,a are equal but the native canonical p differs. Any u(a,b) is equal.
    # A desired F=p kick would require different u, so cannot be direct u(a,b).
    p0,p1=6*(5-3)+0,6*(5-3)+1
    assert p1-p0==1
    # A pure p-kick at fixed q cannot occur in one native microtick for all p.
    q,p,f=0,5,1
    assert q+(p+2*f)//6 != q
    return {'self_a_input_rejected':self_a_rejected,'r_input_rejected':r_read_rejected,
            'same_a_b_distinct_p_example':[p0,p1],
            'general_momentum_force_not_directly_readable':True,
            'pure_kick_not_one_native_tick_example':{'q':q,'p':p,'F':f,'q_next':1},
            'multi_tick_general_lifting_compiler':'not_implemented'}


def independent_symbol_review():
    """Re-extract actual-code principal matrices independently of audit07.

    This is a review of the continuum RHS extension, not an Engine orbit,
    continuum-equivalence oracle or constraint-restricted symbol theorem.
    """
    from universe24.algebra import frame_equations as full
    from validation.geometry.team48 import geometry_triangular as triangular
    rows=[]
    for module in (full,triangular):
        names=module.FIELDS
        jets=sp.symbols('d:'+str(len(names)))
        index={name:i for i,name in enumerate(names)}
        flat={name:sp.Integer(name.startswith('B') and name[1]==name[2]) for name in names}
        for direction in ((0,0,1),(1,2,3)):
            rhs,constraints,ricci=module.equations(flat,lambda name,i:direction[i]*jets[index[name]])
            matrix=sp.Matrix([rhs[name] for name in names]).jacobian(jets)
            nullities=[len((matrix**power).nullspace()) for power in (1,2,3)]
            assert nullities==([14,16,18] if module is full else [10,12,14])
            row={'fields':len(names),'direction':direction,'original_zero_nullities_A_A2_A3':nullities}
            if module is full:
                for a in range(3):
                    for b in range(a,3):
                        rhs[f'K{a}{b}']+=(ricci[b][a]-ricci[a][b])/2
                for a in range(3):
                    for b in range(a+1,3):
                        for c in range(3):
                            rhs[f'G{a}{b}{c}']-=sp.Rational(1,4)*(int(a==c)*constraints[f'M{b}']
                                                                           -int(b==c)*constraints[f'M{a}'])
                corrected=sp.Matrix([rhs[name] for name in names]).jacobian(jets)
                n2=sum(v*v for v in direction)
                annihilator=corrected
                for scale in (1,sp.Rational(1,2),sp.Rational(1,8)):
                    annihilator=annihilator*(corrected**2-scale*n2*sp.eye(len(names)))
                assert annihilator.is_zero_matrix
                lam=sp.Symbol('lambda')
                expected=lam**14*(lam**2-n2)**2*(lam**2-sp.Rational(n2,2))*(lam**2-sp.Rational(n2,8))**2
                assert sp.expand(corrected.charpoly(lam).as_expr()-expected)==0
                row.update({'candidate_squarefree_annihilator':True,
                            'candidate_characteristic_polynomial':str(sp.factor(expected))})
            rows.append(row)
    return {'status':'independently_reproduced_in_two_directions', 'rows':rows,
            'all_direction_proof':'see independent audit07; not asserted by these two samples',
            'nonlinear_constraint_propagation':'not_tested', 'coupled_Einstein_model':'not_tested'}


def main():
    report={'scope':'Two-field reciprocal mechanical edge primitive; not a metric or Einstein model.',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'potential':potential_identity(),'runs':[audit(),audit(True)],
            'compiler':compiler_controls(), 'principal_symbol_cross_review':independent_symbol_review(),
            'limitations':['g is a dynamical stiffness coordinate, not an Einstein metric.',
                           'Initial positive g reaches zero, so squaring alone is not nondegeneracy.',
                           'Momentum is the phi shift-symmetry charge, not spacetime momentum.',
                           'No energy conservation, boundedness, refinability or clock is established.',
                           'This primitive is not added to the 44-channel allocation.']}
    out=ROOT/'runs/research_eight/08_reciprocal_native.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'out':str(out),'runs':[{k:v for k,v in row.items() if k!='rows'} for row in report['runs']],
                      'max_bits':[r['rows'][-1]['max_bits'] for r in report['runs']],
                      'first_g_zero_nodes':report['runs'][0]['rows'][1]['g_zero_nodes']}))


if __name__=='__main__':
    main()
