"""Exact independent arithmetic/original-RHS audits for projective refinement."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np

from universe24.core import Engine
from universe24.core.lattice import lattice
from universe24.tests.test_migration import scalar_step
from .refinement_integer_projective import compile_projective, build_charged, prepare, readout
from . import geometry_triangular as triangular
from . import matter_charged as charged
from . import matter_dust_square as square


def charged_builder(fields, partial):
    """Research equations only; no dependency on the historical PR39 audit."""
    return triangular.equations(fields, partial, fermi_equations=square.equations,
                                base_equations=charged.equations, mass_squared=0)


def evaluated_rhs(program, builder, current, lat):
    fields = dict(zip(program.fields, current))

    def partial(name, axis):
        plus = tuple(int(i == axis) for i in range(3))
        minus = tuple(-v for v in plus)
        return (fields[name][lat.shift_index(plus)]-fields[name][lat.shift_index(minus)])/(2*program.dx)

    result = builder(fields, partial)
    rhs = result[0] if isinstance(result, tuple) else result
    return np.array([np.broadcast_to(rhs[name], (lat.N,)) for name in program.fields], dtype=object)


def generic_quadratic(fields, derivative):
    x, y = fields['x'], fields['y']
    return {'x': F(1, 7)+F(2, 3)*x-x*x+x*derivative('y', 0),
            'y': -1-F(1, 2)*y+x*y+derivative('x', 2)}


def generic_cubic(fields, derivative):
    x, y = fields['x'], fields['y']
    return {'x': F(1, 5)+y-F(2, 3)*x*x*y+x*x*derivative('y', 0),
            'y': F(1, 2)*x-y*y*y}


def check_program(name, program, builder, *, ticks=4, large=False):
    lat = lattice(3)
    values = np.array([F((i*7+j*3)%9-4, 6) for i in range(len(program.fields))
                       for j in range(lat.N)], dtype=object).reshape(len(program.fields), lat.N)
    if large:
        values[0, 0] = F(-(1 << 83), 3)
    remainders = np.array([int(i%6) for i in range(program.tensor.G*lat.N)], dtype=object).reshape(program.tensor.G, lat.N)
    initial = prepare(program, values, L=3, remainders=remainders)
    engine, state = Engine(program.tensor), initial
    rows = []
    previous = None
    for tick in range(ticks):
        current = readout(program, state)
        euler = current + program.dt*evaluated_rhs(program, builder, current, lat)
        following = engine.step(state)
        oracle = scalar_step(program.tensor, state)
        assert following.same_as(oracle), (name, 'independent scalar update')
        d_old, d = int(state.a[0, 0]), int(state.b[0, 0])
        d_next = program.multiplier*d**program.degree-d_old
        assert np.all(following.b[0] == d_next) and d_next > d
        epsilon = F(d_old, d_next)
        expected = euler if previous is None else euler+epsilon*(euler-previous)
        assert np.array_equal(readout(program, following), expected), (name, 'ratio identity')
        assert np.array_equal(following.r, remainders), (name, 'carry changed')
        assert engine.inverse_step(following).same_as(state)
        rows.append({'tick':tick+1,'denominator_bits':d_next.bit_length(),
                     'maximum_state_bits':following.max_abs().bit_length(),
                     'epsilon_zero':epsilon == 0,
                     'ratio_identity_exact':True,'scalar_oracle_exact':True})
        previous, state = current, following
    assert engine.rewind(state, ticks).same_as(initial)
    bad = state.copy()
    bad.b[0, 1] += 1
    try:
        readout(program, bad)
    except ValueError:
        pass
    else:
        raise AssertionError('Nonuniform denominator accepted')
    return {'name':name,'channels':program.tensor.G,'retained_integers_per_node':3*program.tensor.G,
            'dt':str(program.dt),'dx':str(program.dx),'degree':program.degree,
            'coefficient_multiplier':program.multiplier,'monomials':len(program.tensor),
            'tensor_sha256':program.tensor.fingerprint,'single_face_violations':len(program.tensor.support_violations()),
            'old_a_reads':0,'all_six_remainder_classes_checked':True,
            'complete_rewind':True,'first_step_exact_euler':True,'nonuniform_readout_rejected':True,
            'steps':rows,'initial_data_constrained_GR':False}


def check_positive_spatial():
    """Cross-check nodewise W for varying K/matter, not just homogeneous data."""
    from functools import partial
    from . import geometry_positive_pairs as positive
    from . import matter_charged as charged
    from . import matter_dust_square as square
    fields = positive.replace_fields(square.FIELDS_CHARGED)
    builder = partial(positive.equations, fermi_equations=square.equations,
                      base_equations=charged.equations, mass_squared=0)
    program = compile_projective(fields, builder, dt=F(1, 64), dx=F(1, 4), degree=3)
    current = np.array([F((i+j*2)%7-3, 5) for i in range(len(fields)) for j in range(27)],
                       dtype=object).reshape(len(fields), 27)
    for axis in range(3):
        current[fields.index(f'diag_p{axis}')] = 1
        current[fields.index(f'diag_q{axis}')] = 0
    carry = np.array([int(i%6) for i in range(44*27)],dtype=object).reshape(44,27)
    seed = prepare(program, current, L=3, remainders=carry)
    for axis in range(3):
        seed.a[1+fields.index(f'diag_q{axis}')] = 1
    engine, state = Engine(program.tensor), seed
    initial_d = int(seed.b[0,0])
    previous = None
    bit_counts = []
    for tick in range(4):
        for axis in range(3):
            p, q = (1+fields.index(f'diag_{label}{axis}') for label in ('p','q'))
            w = state.b[p]*state.a[q]-state.b[q]*state.a[p]
            assert all(v == initial_d for v in w)
            assert all(int(x)**2+int(y)**2 > 0 for x,y in zip(state.b[p],state.b[q]))
        if tick == 3:
            break
        current = readout(program,state)
        euler = current+program.dt*evaluated_rhs(program,builder,current,lattice(3))
        following = engine.step(state)
        assert following.same_as(scalar_step(program.tensor,state))
        next_d = int(following.b[0,0])
        if previous is None:
            memory = np.array([F(int(v),next_d) for v in state.a[1:].flat],dtype=object).reshape(current.shape)
            expected = euler-memory
        else:
            expected = euler+F(int(state.a[0,0]),next_d)*(euler-previous)
        assert np.array_equal(readout(program,following),expected)
        assert np.array_equal(following.r,carry)
        assert engine.inverse_step(following).same_as(state)
        bit_counts.append(following.max_abs().bit_length())
        previous,state = current,following
    assert engine.rewind(state,3).same_as(seed)
    return {'name':'positive44_nonuniform_spatial_crosscheck','channels':44,
            'dt':str(program.dt),'dx':str(program.dx),'degree':3,
            'monomials':len(program.tensor),'tensor_sha256':program.tensor.fingerprint,
            'Wronskian_nodewise_exact':True,'Wronskian_value':initial_d,
            'all_six_remainder_classes_checked':True,'complete_rewind':True,
            'all_nodes_positive_diagonals':True,'independent_scalar_oracle':True,
            'first_memory_perturbation_and_later_ratio_identity_exact':True,
            'maximum_retained_bits_by_tick':bit_counts,'initial_data_constrained_GR':False}


def audit():
    rows = [check_program('quadratic_signed_spatial',
                          compile_projective(('x','y'), generic_quadratic, dt=F(1, 32), dx=F(1, 5)),
                          generic_quadratic, large=True),
            check_program('cubic_signed_spatial',
                          compile_projective(('x','y'), generic_cubic, dt=F(1, 64), dx=F(1, 7), degree=3),
                          generic_cubic, ticks=3)]
    for h in (F(1, 2), F(1, 8), F(1, 32)):
        rows.append(check_program('charged41_fractional_step',build_charged(dt=h,dx=F(1, 4)),charged_builder,ticks=3))
    rows.append(check_positive_spatial())
    directory = Path(__file__).resolve().parent
    return {'status':'all_exact_projective_encoding_checks_passed','programs':rows,
            'full_Einstein_gate':False,'spacetime_convergence_gate':False,
            'integer_coefficient_obstruction_removed':True,'bounded_bit_memory':False,
            'source_sha256':{str(path.relative_to(directory.parents[2])):hashlib.sha256(path.read_bytes()).hexdigest()
                             for path in sorted(directory.glob('refinement_integer*')) if path.is_file()}}


if __name__ == '__main__':
    result = audit()
    output = Path('runs/team48/refinement_integer/audit.json')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'checks':len(result['programs']),
                      'channels':[row['channels'] for row in result['programs']],
                      'output':str(output)},indent=2))
