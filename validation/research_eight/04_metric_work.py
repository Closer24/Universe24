"""Exact polarized energy/face-flux/work identity, not an Einstein model.

The two coefficients are retained autonomous affine backgrounds.  They are
not a solved metric and receive no stress backreaction.  This source-only
control tests the algebra needed before a joint discrete action can be built.
"""
from pathlib import Path
import hashlib
import json
import numpy as np

from universe24.core import Engine, GearType, Tensor
from universe24.core.lattice import lattice
from validation.geometry.team48.integer_sign_lift import SignProgram, prepare, physical_slices
from fractions import Fraction

FIELDS = ('phi', 'p', 'q', 'A', 'B')
ROOT = Path(__file__).resolve().parents[2]
ZERO = (0, 0, 0)


def program(*, nonconservative=False):
    terms = []
    def add(target, coefficient, fields):
        terms.append(('field.' + target, 3 * coefficient,
                      (('phase.sign', ZERO, 'b'),) + tuple(
                          ('field.' + name, offset, 'b') for name, offset in fields),
                      {'designated_one_way': 'Retained autonomous background control; no Einstein backreaction.'}))
    add('phi', 2, [('A', ZERO), ('p', ZERO)])
    for sign in (-1, 1):
        edge = (sign, 0, 0)
        coefficient_at = ZERO if nonconservative else edge
        add('p', sign, [('B', coefficient_at), ('q', edge)])
        add('q', sign, [('A', coefficient_at), ('p', edge)])
    add('A', 2, [])
    add('B', 4, [])
    tensor = Tensor([GearType('phase.sign', label='audit')] +
                    [GearType('field.' + n, label='audit') for n in FIELDS],
                    terms, strict_support=True)
    return SignProgram(tensor, FIELDS, Fraction(1), Fraction(1))


def shift(v, lat, sign=1):
    return v[lat.shift_index((sign, 0, 0))]


def delta(v, lat):
    return shift(v, lat) - shift(v, lat, -1)


def scalar_next(previous, current, lat, *, nonconservative=False):
    phi, p, q, A, B = current
    increments = [2*A*p,
                  B*delta(q, lat) if nonconservative else delta(B*q, lat),
                  A*delta(p, lat) if nonconservative else delta(A*p, lat),
                  np.full(lat.N, 2, dtype=object),
                  np.full(lat.N, 4, dtype=object)]
    return previous + np.asarray(increments, dtype=object)


def balance(previous, current, following, lat):
    _, pp, qp, Ap, Bp = previous
    _, p, q, A, B = current
    _, pn, qn, _, _ = following
    before = Ap*pp*p + Bp*qp*q
    after = A*p*pn + B*q*qn
    ap, bq = A*p, B*q
    face = ap*shift(bq, lat) + bq*shift(ap, lat)
    flux_div = face - shift(face, lat, -1)
    work = (A-Ap)*pp*p + (B-Bp)*qp*q
    return after-before-flux_div-work, after-before-flux_div, work


def peak(values):
    return int(max(abs(int(v)) for v in values))


def audit_case(nonconservative=False):
    L = 5
    lat = lattice(L)
    rng = np.random.default_rng(410411)
    slices = []
    x = lat.all_coords()[:, 0].astype(object)
    for t in (-1, 0):
        phi = 2*rng.integers(-5, 6, lat.N).astype(object)
        p = rng.integers(-4, 5, lat.N).astype(object)
        q = delta(phi, lat)//2
        A, B = 3+x+t, 5+2*x+2*t
        slices.append(np.asarray([phi, p, q, A, B], dtype=object))
    law = program(nonconservative=nonconservative)
    seed = prepare(law, *slices, L=L,
                   remainders=np.arange(6*lat.N).reshape(6, lat.N)%6)
    engine = Engine(law.tensor)
    state = seed
    exact_peak = omission_peak = gradient_peak = work_peak = max_bits = 0
    totals = []
    for tick in range(8):
        previous, current = physical_slices(law, state)
        expected = scalar_next(previous, current, lat, nonconservative=nonconservative)
        result = engine.step(state)
        result_old, following = physical_slices(law, result)
        assert np.array_equal(result_old, current)
        assert np.array_equal(following, expected)
        assert np.array_equal(result.r, seed.r)
        assert engine.inverse_step(result).same_as(state)
        residual, omitted, work = balance(previous, current, following, lat)
        exact_peak = max(exact_peak, peak(residual))
        omission_peak = max(omission_peak, peak(omitted))
        work_peak = max(work_peak, peak(work))
        gradient_peak = max(gradient_peak, peak(2*following[2]-delta(following[0], lat)))
        max_bits = max(max_bits, max(abs(int(v)).bit_length() for arr in
                                    (result.a, result.b, result.r) for v in arr.flat))
        # Summed divergence cancels on this periodic lattice.
        totals.append({'tick':tick+1, 'sum_balance_residual':int(sum(residual)),
                       'sum_polarized_energy_change':int(sum(omitted)),
                       'sum_metric_coefficient_work':int(sum(work))})
        state = result
    assert engine.rewind(state, 8).same_as(seed)
    if nonconservative:
        assert exact_peak > 0 and gradient_peak > 0
    else:
        assert exact_peak == 0 and gradient_peak == 0 and omission_peak > 0
        assert all(r['sum_polarized_energy_change'] == r['sum_metric_coefficient_work']
                   for r in totals)
    return {'case':'wrong_coefficient_outside_derivative' if nonconservative else 'compatible_flux',
            'channels':law.tensor.G, 'retained_integer_entries_per_node':3*law.tensor.G,
            'monomials':len(law.tensor), 'input_degree':law.tensor.rank-1,
            'strict_face_support':not law.tensor.support_violations(),
            'tensor_sha256':law.tensor.fingerprint, 'L':L, 'steps':8,
            'all_six_remainders_present':sorted(set(map(int, seed.r.flat))) == list(range(6)),
            'scalar_oracle_agrees':True, 'complete_inverse_and_rewind':True,
            'local_polarized_energy_flux_work_residual_peak':exact_peak,
            'wrong_omitted_work_residual_peak':omission_peak,
            'metric_coefficient_work_peak':work_peak,
            'twice_scalar_gradient_constraint_peak':gradient_peak,
            'max_retained_integer_bits':max_bits, 'global_balance_by_tick':totals}


def main():
    rows = [audit_case(), audit_case(nonconservative=True)]
    result = {'scope':'Autonomous variable-coefficient scalar wave algebra only; no Einstein geometry or reciprocal stress coupling',
              'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'cases':rows,
              'limitations':['No Einstein equations or operational clock are implemented.',
                             'A and B are retained affine background coefficients; no matter backreaction.',
                             'The time-polarized energy is not positive on arbitrary two-time histories.',
                             'No stability, continuum convergence, Maxwell coupling, or bounded-bit theorem is claimed.',
                             'The passive face-flux diagnostic has degree four; evolution has degree three.',
                             'This control is not appended to or substituted into the 44-channel candidate.']}
    out = ROOT/'runs/research_eight/04_metric_work.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'out':str(out), 'cases':[{k:v for k,v in row.items() if k != 'global_balance_by_tick'} for row in rows]}, indent=2))


if __name__ == '__main__':
    main()
