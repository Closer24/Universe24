"""Exact one-axis geodesic arithmetic coupled to the local pp-wave geometry.

This is a prepared phase-space encoding at one computational node, not a
packet moving on board links or a derivation of general Einstein dynamics.
Evolution, preparation, and residual checks use integers only. Continuous
coordinates use a declared passive calibration, documented in the report.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from validation.geometry import ppwave_palatini_local as pp
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import lattice
from universe24.core.reciprocity import check_reciprocity

PROBES = ("probe.q", "probe.p", "probe.product", "clock.affine")
ZERO, PLUS_X = (0, 0, 0), (1, 0, 0)
P = 2  # Geometric calibration; Engine divisor remains six.


def build():
    original = pp.build()
    names = list(original.names[:44]) + list(PROBES)
    terms = [m for m in original.monomials if m.target < 44]
    def f(name, offset=ZERO):
        return (name, offset, "b")
    one_way = {"designated_one_way":
               "Prepared test-worldline response and product register; no matter backreaction or common force potential is claimed."}
    for name in PROBES[:2]:
        terms.append((name, 6, (f(name),)))
        for direction, sign in ((PLUS_X, 1), (ZERO, -1)):
            terms.append((name, 3*sign, (f("X.W01", direction), f(name)), one_way))
    terms.append((PROBES[2], 6, (f(PROBES[0]), f(PROBES[1])), one_way))
    for direction, sign in ((PLUS_X, 1), (ZERO, -1)):
        terms.append((PROBES[2], 18*sign,
                      (f("X.W01", direction), f(PROBES[0]), f(PROBES[1])), one_way))
    terms.append((PROBES[3], 6, (f(PROBES[3]),)))
    return Tensor(names, terms, strict_support=True)


def prepare(tensor, curvature=1, epsilon=1, L=5):
    """One complete seed; nonbinary curvature is allowed for failure controls."""
    if type(curvature) is not int or type(epsilon) is not int or epsilon not in (0, 1):
        raise ValueError("Integer curvature and epsilon in {0,1} required")
    if type(L) is not int or L < 5 or L % 2 != 1:
        raise ValueError("Use an odd local chart with L>=5")
    lat = lattice(L)
    xyz = lat.all_coords().astype(object)
    x, y = xyz[:, 0]-L//2, xyz[:, 1]-L//2
    F = curvature*(x*x-y*y)
    Fx, Fy = 2*curvature*x, -2*curvature*y
    fields = {}
    for a in range(4):
        for mu in range(4):
            fields[f"E{a}{mu}"] = P*int(a == mu)+pp.ETA[a]*pp.NULL[a]*pp.NULL[mu]*F
    for a, b in pp.PAIRS:
        fields[f"W{a}{b}"] = (Fx if (a, b) in ((0, 1), (1, 3)) else
                               Fy if (a, b) in ((0, 2), (2, 3)) else np.zeros(lat.N, dtype=object))
    b_values = np.zeros((48, lat.N), dtype=object)
    for bank in ("X", "Y"):
        for name, value in fields.items():
            b_values[tensor.gear_index(f"{bank}.{name}")] = value
    a_values, r_values = b_values.copy(), np.zeros_like(b_values)
    carrier = lat.index(L//2, L//2, 0)
    q, p, w, n = (tensor.gear_index(name) for name in PROBES)
    b_values[q, carrier] = 1
    a_values[q, carrier] = 1+curvature
    a_values[p, carrier] = -curvature
    a_values[w, carrier] = -curvature*(1+curvature)
    a_values[n, carrier] = -1
    r_values[n, carrier] = epsilon
    return State(L, a_values, b_values, r_values), carrier


def decode_official(rows, initial, epsilon):
    """Sector-specific decoder: rows plus four initial triples, no live state.

    Silent nonzero fixed points make missing=zero invalid in general. Here
    p,w,n have zero quotient whenever absent; q is recovered from w=q*p and
    the calibrated positive branch. This is not a general click inverse.
    """
    if epsilon not in (0, 1):
        raise ValueError("Unknown norm sector")
    a, b = [list(values) for values in initial]
    decoded = [b.copy()]
    for row in rows:
        following = [None] + [int(row.get(name, 0))-a[i] for i, name in enumerate(PROBES) if i]
        p, w = following[1:3]
        if p:
            q, remainder = divmod(w, p)
            if remainder or q < 1:
                raise AssertionError("Product/positive-branch preparation lost")
        else:
            if w:
                raise AssertionError("Zero momentum with nonzero product")
            q = initial[1][0]
        following[0] = q
        if PROBES[0] in row and int(row[PROBES[0]]) != q+a[0]:
            raise AssertionError("Position click disagrees with independent product decoding")
        a, b = b, following
        decoded.append(b.copy())
    return decoded


def run_case(tensor, curvature, epsilon, steps, length_scale):
    seed, carrier = prepare(tensor, curvature, epsilon)
    engine, state = Engine(tensor), seed
    ids = [tensor.gear_index(name) for name in PROBES]
    initial = [[int(value) for value in array[ids, carrier]] for array in (seed.a, seed.b)]
    retained, rows, trace = [initial[1]], [], hashlib.sha256()
    for tick in range(1, steps+1):
        following = engine.step(state)
        old_q, old_p, _, old_n = retained[-1]
        q = (1+curvature)*old_q+3*curvature*old_p
        p = curvature*old_q+(1+curvature)*old_p
        expected = [q, p, q*p, old_n+1]
        actual = [int(value) for value in following.b[ids, carrier]]
        assert actual == expected
        assert q*q-3*p*p == 1
        assert np.array_equal(following.b[:44], seed.b[:44])
        assert np.array_equal(following.r, seed.r)
        assert engine.inverse_step(following).same_as(state)
        log = engine.clicks(state, following, tick).select("official")
        row = {tensor.names[int(g)]: int(value)
               for g, node, value in zip(log.gear, log.node, log.quotient)
               if int(node) == carrier and int(g) in ids}
        # Read-only audit: missing p,w,n rows really do have quotient zero.
        for name, gear in zip(PROBES[1:], ids[1:]):
            assert row.get(name, 0) == int(following.b[gear, carrier])+int(state.a[gear, carrier])
        rows.append(row)
        retained.append(actual)
        state = following
        trace.update(bytes.fromhex(pp.digest(state)))
    assert engine.rewind(state, steps).same_as(seed)
    decoded = decode_official(rows, initial, epsilon)
    assert decoded == retained
    observations = []
    for q, p, w, n in decoded:
        # Exact normalization numerator for h=g/P^2 and X=q/length_scale.
        norm_num = -curvature*(q*q+3*p*p)-epsilon*length_scale**2+3*p*p+curvature*q*q
        assert norm_num == -epsilon*length_scale**2
        observations.append(dict(n=n, q=q, p=p, product=w,
            transverse_position_numerator=q, transverse_position_denominator=length_scale,
            T_alpha_numerator=(1+epsilon)*n, T_alpha_denominator=2,
            T_sqrt3_numerator=w, T_sqrt3_denominator=2*length_scale**2,
            norm_numerator=norm_num, norm_denominator=length_scale**2,
            coordinate_time_derivative_numerator=(1+epsilon)*length_scale**2+curvature*(q*q+3*p*p),
            coordinate_time_derivative_denominator=2*length_scale**2))
    # The geometry is stationary, so one exact Cartan check covers every tick.
    E, T2, R2, palatini = pp.cartan(seed, seed, seed, P)
    _, ricci, _, _ = pp.exact_inverse_metric_and_ricci(E, R2, P)
    bulk = np.array([0 < x < seed.L-1 and 0 < y < seed.L-1 for x,y,z in seed.lattice.all_coords()])
    assert pp.peak(T2[bulk]) == pp.peak(palatini[bulk]) == pp.peak(ricci[bulk]) == 0
    return dict(curvature=curvature, epsilon_from_clock_remainder=epsilon,
        carrier=list(seed.lattice.coords(carrier)), initial_probe_a_b=initial,
        steps=steps, length_scale=length_scale, full_seed_sha256=pp.digest(seed),
        full_final_sha256=pp.digest(state), full_trace_sha256=trace.hexdigest(),
        exact_rewind=True, official_rows=rows, decoded=observations,
        maximum_counter=state.max_abs(), click_only_prepared_decoder_pass=True,
        all_samples_within_coordinate_timelike_patch=all(curvature*row[0]**2 < length_scale**2 for row in decoded),
        bulk_curvature_numerator_peak=pp.peak(R2[bulk]), bulk_torsion_palatini_ricci_zero=True,
        seam_torsion_peak=pp.peak(T2[~bulk]), seam_palatini_peak=pp.peak(palatini[~bulk]))


def negative_controls(tensor):
    engine = Engine(tensor)
    curved, carrier = prepare(tensor, 1, 1)
    flat, _ = prepare(tensor, 0, 1)
    flat.a[44:], flat.b[44:], flat.r[44:] = curved.a[44:], curved.b[44:], curved.r[44:]
    # All probe triples identical; only initial geometry differs.
    assert np.array_equal(curved.a[44:], flat.a[44:]) and np.array_equal(curved.b[44:], flat.b[44:])
    curved_next, flat_next = engine.step(curved), engine.step(flat)
    q_curved, q_flat = int(curved_next.b[44, carrier]), int(flat_next.b[44, carrier])
    assert (q_curved, q_flat) == (2, 0)
    bad, node = prepare(tensor, 2, 1)
    after = engine.run(bad, 2)
    q, p, w = map(int, after.b[44:47, node])
    assert w-q*p == -48
    assert engine.rewind(after, 2).same_as(bad)
    # Naively declaring all missing quotients zero loses a stationary q=1.
    flat_seed, node = prepare(tensor, 0, 1)
    flat_after = engine.step(flat_seed)
    return dict(geometry_only_change_first_q=dict(curved=q_curved,flat=q_flat,
                    identical_complete_probe_initial_state=True),
                nonbinary_curvature=dict(curvature=2,steps=2,product_defect=w-q*p,exact_rewind=True),
                naive_missing_row_decoder=dict(predicted_q=-int(flat_seed.a[44,node]),
                                               actual_q=int(flat_after.b[44,node]),passes=False))


def run(steps=16, length_scale=2**30):
    if type(steps) is not int or steps < 2 or type(length_scale) is not int or length_scale < 1:
        raise ValueError("Integer steps>=2 and positive integer length calibration required")
    tensor = build()
    reciprocal = check_reciprocity(tensor)
    assert tensor.G == 48 and tensor.rank == 4 and tensor.b_only
    assert not tensor.support_violations() and reciprocal.ok and len(reciprocal.designated) == 7
    cases = [run_case(tensor, c, epsilon, steps, length_scale) for c,epsilon in ((0,1),(1,1),(1,0))]
    assert cases[1]["official_rows"] == cases[2]["official_rows"]
    assert cases[1]["full_seed_sha256"] != cases[2]["full_seed_sha256"]
    return dict(schema="ppwave-geodesic-clock-v1",
        scope="Exact selected one-axis phase-space geodesics and calibrated clock readout; not spatial board propagation or general relativity emergence",
        tensor=dict(D=6,gears=48,rank=tensor.rank,monomials=len(tensor.monomials),
                    fingerprint=tensor.fingerprint,strict_single_edge=True,
                    one_way_designations=len(reciprocal.designated),full_reciprocity=False),
        calibration=dict(coframe_P=P,alpha="acosh(2)",length_scale=length_scale,
            X="q/length_scale",U="alpha*n",V="(sqrt(3)*product/length_scale^2+epsilon*alpha*n)/2",
            T="V+U/2",Z="V-U/2",proper_time="alpha*n for epsilon=1 in h=g/P^2; raw g proper time is P times this",
            metric="h=-2dU dV+dX^2+dY^2+c*(X^2-Y^2)dU^2; Y=0",
            continuous_calibration_is_passive=True),
        cases=cases,controls=negative_controls(tensor),
        null_and_timelike_sectors_have_identical_official_records=True,
        official_records_alone_determine_norm_sector=False,
        limitations=["The constant curvature selector c is restricted to 0 or 1 and is fixed by preparation.",
          "Geometry drives test-worldline registers without backreaction; seven one-way terms are explicit.",
          "Positions are encoded inside one computational node, not transported across board links.",
          "Proper time is proved for a calibrated selected geodesic, not emergent universal clock dynamics.",
          "The null sector is a distinct retained remainder choice, not a propagating photon or detector model.",
          "Prepared clock data and a sector-specific decoder are required; official records alone are not an invertible state.",
          "The transverse periodic geometry seams still fail the vacuum equations.",
          "Only the growing transverse direction is included; this is not a full two-transverse-direction geodesic integrator."])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", type=int, default=16)
    parser.add_argument("--length-scale", type=int, default=2**30)
    parser.add_argument("--out", type=Path, default=ROOT/"runs/ppwave-geodesic/report.json")
    args = parser.parse_args()
    report = run(args.steps, args.length_scale)
    report["source_sha256"] = {str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (Path(__file__).resolve(), Path(pp.__file__).resolve())}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(dict(tensor=report["tensor"],controls=report["controls"],
        cases=[{k:c[k] for k in ("curvature","epsilon_from_clock_remainder","steps","exact_rewind",
            "all_samples_within_coordinate_timelike_patch","maximum_counter")} for c in report["cases"]]),indent=2))
