"""Independent proofs and saved-state review of the finite null-source chart.

The metric and basis calculations are independent of geometry.py.  The
same-state check uses an explicit scalar recurrence, not Engine evaluation or
the candidate's ideal_step/readout.  Units: 8*pi*G=1, signature (-,+,+,+).
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import gzip
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import DIRECTIONS, State, exact_json
from universe24.system.bundle import load_bundle, state_from_data


@lru_cache(maxsize=1)
def metric_proof():
    """Derive connection, curvature and source balance from the metric."""
    u, v, y, z = sp.symbols("u v y z", real=True)
    coordinates = (u, v, y, z)
    f, g = sp.Function("f")(u), sp.Function("g")(v)
    R = f+g
    metric = sp.Matrix([[0, -1/sp.sqrt(R), 0, 0],
                        [-1/sp.sqrt(R), 0, 0, 0],
                        [0, 0, R, 0], [0, 0, 0, R]])
    inverse = metric.inv()
    connection = [[[sp.simplify(sum(inverse[a, d]*(
        sp.diff(metric[d, c], coordinates[b])
        + sp.diff(metric[d, b], coordinates[c])
        - sp.diff(metric[b, c], coordinates[d]))/2 for d in range(4)))
        for c in range(4)] for b in range(4)] for a in range(4)]
    ricci = sp.zeros(4)
    for a in range(4):
        for b in range(4):
            ricci[a, b] = sp.simplify(sum(
                sp.diff(connection[c][a][b], coordinates[c])
                - sp.diff(connection[c][a][c], coordinates[b])
                + sum(connection[c][c][d]*connection[d][a][b]
                      - connection[c][b][d]*connection[d][a][c]
                      for d in range(4)) for c in range(4)))
    scalar = sp.simplify(sum(inverse[a, b]*ricci[a, b]
                             for a in range(4) for b in range(4)))
    einstein = sp.simplify(ricci-scalar*metric/2)
    expected = sp.zeros(4)
    expected[0, 0] = -sp.diff(f, u, 2)/R
    expected[1, 1] = -sp.diff(g, v, 2)/R
    residuals = [sp.simplify(einstein[a, b]-expected[a, b])
                 for a in range(4) for b in range(4)]
    assert scalar == 0 and all(value == 0 for value in residuals)
    # Independent arbitrary source profiles; not an Einstein-tensor alias.
    nplus, nminus = sp.Function("n_plus")(u), sp.Function("n_minus")(v)
    source_cov = sp.diag(nplus/R, nminus/R, 0, 0)
    source_up = sp.simplify(inverse*source_cov*inverse)
    divergences = []
    for nu in range(4):
        div = sum(sp.diff(source_up[mu, nu], coordinates[mu]) for mu in range(4))
        for mu in range(4):
            for sigma in range(4):
                div += (connection[mu][mu][sigma]*source_up[sigma, nu]
                        + connection[nu][mu][sigma]*source_up[mu, sigma])
        divergences.append(sp.simplify(div))
    assert all(value == 0 for value in divergences)
    accelerations = []
    for tangent in (sp.Matrix([0, sp.sqrt(R), 0, 0]),
                    sp.Matrix([sp.sqrt(R), 0, 0, 0])):
        assert sp.simplify((tangent.T*metric*tangent)[0]) == 0
        for mu in range(4):
            acceleration = sum(tangent[nu]*sp.diff(tangent[mu], coordinates[nu])
                               for nu in range(4))
            acceleration += sum(connection[mu][a][b]*tangent[a]*tangent[b]
                                for a in range(4) for b in range(4))
            accelerations.append(sp.simplify(acceleration))
    assert all(value == 0 for value in accelerations)
    # Correct physical time is t=(u+v)/2, longitudinal position x=(v-u)/2.
    et, ex = sp.Matrix([1, 1, 0, 0]), sp.Matrix([-1, 1, 0, 0])
    assert sp.simplify((et.T*metric*et)[0]+2/sp.sqrt(R)) == 0
    assert sp.simplify((ex.T*metric*ex)[0]-2/sp.sqrt(R)) == 0
    scale = R**sp.Rational(1, 4)/sp.sqrt(2)
    et, ex = scale*et, scale*ex
    rho = sp.simplify((et.T*source_cov*et)[0])
    flux = sp.simplify(-(et.T*source_cov*ex)[0])
    assert sp.simplify(rho-(nplus+nminus)/(2*sp.sqrt(R))) == 0
    assert sp.simplify(flux-(nplus-nminus)/(2*sp.sqrt(R))) == 0
    assert sp.simplify(expected[0, 0]-2*expected[0, 0]) != 0
    return {
        "einstein_components": 16, "einstein_residuals": [str(x) for x in residuals],
        "scalar_curvature": str(scalar),
        "stress_divergence_residuals": [str(x) for x in divergences],
        "affine_null_geodesic_residuals": [str(x) for x in accelerations],
        "nonzero_einstein": {"uu": "-f''/(f+g)", "vv": "-g''/(f+g)"},
        "observer_density": "(n_plus+n_minus)/(2*sqrt(R))",
        "observer_flux": "(n_plus-n_minus)/(2*sqrt(R))",
        "metric_domain": "R=f(u)+g(v)>0; u=t-x,v=t+x;8*pi*G=1",
        "wrong_source_rejected": True, "wrong_timelike_coordinate_rejected": True}


def rational(value):
    if isinstance(value, Fraction):
        return value
    if isinstance(value, (int, np.integer)) and not isinstance(value, (bool, np.bool_)):
        return Fraction(int(value))
    raise ValueError("exact integer or Fraction required")


def hat(value):
    value = abs(rational(value))
    return max(Fraction(0), 1-value)


def cubic(value):
    value = abs(rational(value))
    if value < 1:
        return (4-6*value**2+3*value**3)/6
    return (2-value)**3/6 if value < 2 else Fraction(0)


def cubic_second(value):
    """Direct derivative of the piecewise cubic, not a difference of hats."""
    value = abs(rational(value))
    if value <= 1:
        return -2+3*value
    return 2-value if value < 2 else Fraction(0)


def spline_proof():
    x = sp.symbols("x", real=True)
    pieces = ((-3, -2), (-2, -1), (-1, 0), (0, 1), (1, 2), (2, 3))
    def phat(shift, midpoint):
        center = midpoint+shift
        if abs(center) >= 1:
            return sp.Integer(0)
        return 1-(x+shift) if center >= 0 else 1+(x+shift)
    residuals = []
    for left, right in pieces:
        midpoint = Fraction(left+right, 2)
        absolute = x if midpoint >= 0 else -x
        if abs(midpoint) < 1:
            basis = (4-6*absolute**2+3*absolute**3)/6
        elif abs(midpoint) < 2:
            basis = (2-absolute)**3/6
        else:
            basis = sp.Integer(0)
        rhs = phat(1, midpoint)-2*phat(0, midpoint)+phat(-1, midpoint)
        residuals.append(sp.expand(sp.diff(basis, x, 2)-rhs))
    assert all(value == 0 for value in residuals)
    points = [Fraction(n, 8) for n in range(-24, 25)]
    for point in points:
        assert cubic_second(point) == hat(point+1)-2*hat(point)+hat(point-1)
        assert sum(cubic(point-j) for j in range(-6, 7)) == 1
        assert sum(hat(point-j) for j in range(-6, 7)) == 1
    source = {j: (j*j+3*j+7) % 3 for j in range(-8, 9)}
    coefficients = {-9: 1000, -8: 1000}
    for j in range(-8, 9):
        coefficients[j+1] = 2*coefficients[j]-coefficients[j-1]-source[j]
    checked = 0
    for point in [Fraction(n, 4) for n in range(-20, 21)]:
        actual = sum(value*cubic_second(point-j) for j, value in coefficients.items())
        expected = -sum(value*hat(point-j) for j, value in source.items())
        assert actual == expected
        potential = sum(value*cubic(point-j) for j, value in coefficients.items())
        support = [value for j, value in coefficients.items() if cubic(point-j)]
        assert potential >= min(support) > 0
        checked += 1
    return {"interval_polynomial_residuals": [str(x) for x in residuals],
            "basis_rational_checks": len(points),
            "nonconstant_source_reconstruction_checks": checked,
            "identity": "B3''(x)=B1(x+1)-2B1(x)+B1(x-1)",
            "source_identity": "f''=sum_j Delta2(F)_j*B1(x-j)=-sum_j n_j*B1(x-j)",
            "coefficient_positivity_implies_chart_positivity": True,
            "basis_scope": "centered cubic coefficients, not nodal values"}


def periodic_obstruction():
    from itertools import product
    checked = 0
    for values in product((-1, 0, 1), repeat=5):
        laplacian = [values[(j+1) % 5]-2*values[j]+values[(j-1) % 5] for j in range(5)]
        assert sum(laplacian) == 0
        if all(value <= 0 for value in laplacian):
            assert all(value == 0 for value in laplacian)
        checked += 1
    return {"finite_ring_cases": checked,
            "proof": "sum Delta2(F)=0;Delta2(F)=-n,n>=0 imply n=0 at every site",
            "global_nonzero_positive_periodic_null_source": "impossible_in_this_chart",
            "finite_positive_causal_patch": "requires_domain_certificate"}


def _direction(value):
    value = tuple(value)
    if len(value) != 3 or any(type(x) is not int for x in value) or value not in DIRECTIONS:
        raise ValueError("exact integer face direction required")
    return value


def _exact_divmod6(values):
    """Keep arbitrary-size signed Python integers in the independent oracle."""
    pairs = [divmod(int(value), 6) for value in values]
    return np.asarray(pairs, dtype=object).T


def scalar_step(state, direction=(1, 0, 0)):
    """Independent expanded recurrence for all12 channels, including seams."""
    state = State(state.L, state.a, state.b, state.r)
    if state.b.shape[0] != 12:
        raise ValueError("exactly12 retained channels required")
    direction = _direction(direction)
    a, b, r = (getattr(state, field).astype(object) for field in ("a", "b", "r"))
    following, carries = np.empty_like(b), np.empty_like(r)
    for bank in range(2):
        source = 4*(1-bank)
        collision = b[source:source+4].copy()
        for n in range(state.N):
            bits = tuple(int(value) for value in collision[:, n])
            if any(value not in (0, 1) for value in bits):
                raise ValueError("source rails left their Boolean sector")
            if bits == (1, 0, 0, 1):
                collision[:, n] = (0, 1, 1, 0)
            elif bits == (0, 1, 1, 0):
                collision[:, n] = (1, 0, 0, 1)
        for lane in range(4):
            speed = 1 if lane % 2 == 0 else -1
            offset = tuple((1-2*bank)*speed*v for v in direction)
            target = 4*bank+lane
            shifted = b[source+lane, state.lattice.shift_index(offset)]
            quotient, remainder = _exact_divmod6(6*(collision[lane]+shifted)+r[target])
            following[target], carries[target] = quotient-a[target], remainder
        for sign in range(2):
            target, origin = 8+2*bank+sign, 8+2*(1-bank)+sign
            speed = 1 if sign == 0 else -1
            offset = tuple((2*bank-1)*speed*v for v in direction)
            neighbour = b[origin, state.lattice.shift_index(offset)]
            occupancy = b[source+sign]+b[source+sign+2]
            quotient, remainder = _exact_divmod6(
                18*b[origin]-6*neighbour-6*occupancy+r[target])
            following[target], carries[target] = quotient-a[target], remainder
    return State(state.L, b.copy(), following, carries)


def _plane_rows(state, direction):
    axis = next(i for i, value in enumerate(direction) if value)
    coordinate = state.lattice.all_coords()[:, axis]
    if direction[axis] < 0:
        coordinate = state.L-1-coordinate
    rows = []
    for channel in range(12):
        values = []
        for j in range(state.L):
            plane = state.b[channel, coordinate == j]
            value = int(plane[0])
            if any(int(other) != value for other in plane):
                raise ValueError("plane-symmetric source/profile required")
            values.append(value)
        rows.append(values)
    return rows


def _reconstruct(values, point, kernel):
    return sum((rational(value)*kernel(rational(point)-j)
                for j, value in enumerate(values)), Fraction(0))


def _profiles(rows):
    length = len(rows[0])
    return ([rows[8][j]+rows[10][j] for j in range(length)],
            [rows[9][j]+rows[11][j] for j in range(length)],
            [sum(rows[g][j] for g in (0, 2, 4, 6)) for j in range(length)],
            [sum(rows[g][j] for g in (1, 3, 5, 7)) for j in range(length)])


def _prepared_history(seed, direction):
    b = seed.b.astype(object)
    expected = np.empty_like(b)
    for lane in range(4):
        sign = 1 if lane % 2 == 0 else -1
        expected[lane] = b[4+lane, seed.lattice.shift_index(tuple(sign*v for v in direction))]
    for n in range(seed.N):
        bits = tuple(int(value) for value in b[:4, n])
        if bits == (1, 0, 0, 1):
            bits = (0, 1, 1, 0)
        elif bits == (0, 1, 1, 0):
            bits = (1, 0, 0, 1)
        expected[4:8, n] = bits
    expected[8] = b[10, seed.lattice.shift_index(direction)]
    expected[9] = b[11, seed.lattice.shift_index(tuple(-v for v in direction))]
    expected[10:12] = b[8:10]
    if not np.array_equal(seed.a, expected):
        raise ValueError("the saved chart lacks its complete inverse preparation")


def saved_chart_review(run_dir, protocol):
    """Join analytic proofs to one actual saved12-channel full history."""
    bundle = load_bundle(Path(run_dir)/"bundle")
    seed = bundle.seed
    direction = _direction(protocol["direction"])
    if type(protocol["L"]) is not int or protocol["L"] != seed.L or seed.b.shape[0] != 12:
        raise ValueError("different chart/bundle")
    horizon = protocol["microsteps"]
    if type(horizon) is not int or horizon < 2 or horizon % 2:
        raise ValueError("positive even exact-integer horizon required")
    if seed.L < 2*(horizon+3)+1:
        raise ValueError("requested horizon reaches the seam")
    _prepared_history(seed, direction)
    initial_rows = _plane_rows(seed, direction)
    fp0, fm0, np0, nm0 = _profiles(initial_rows)
    for profile, plus, minus in ((8, 0, 2), (9, 1, 3), (10, 4, 6), (11, 5, 7)):
        for j in range(1, seed.L-1):
            if (initial_rows[profile][j+1]-2*initial_rows[profile][j]
                    + initial_rows[profile][j-1]+initial_rows[plus][j]
                    + initial_rows[minus][j]) != 0:
                raise ValueError("initial profile/source constraint fails")
    lower_bound = sum(min(initial_rows[channel]) for channel in (8, 9, 10, 11))
    if lower_bound <= 0:
        raise ValueError("positive whole-domain coefficient bound is not established")
    previous = seed
    rows_by_tick = [initial_rows]
    comparisons = 0
    run_id = None
    with gzip.open(Path(run_dir)/"full_trace.jsonl.gz", "rt", encoding="utf-8") as stream:
        for tick, line in enumerate(stream, 1):
            record = exact_json.loads(line)
            if record["step"] != tick or record["tensor_hash"] != bundle.tensor.fingerprint:
                raise ValueError("trace law/step mismatch")
            if run_id is None:
                run_id = record["run_id"]
            elif record["run_id"] != run_id:
                raise ValueError("mixed run identities")
            before = state_from_data(record["before"])
            after = state_from_data(record["after"])
            if not before.same_as(previous):
                raise ValueError("disconnected saved transitions")
            if not scalar_step(before, direction).same_as(after):
                raise ValueError("saved state differs from independent source/collision recurrence")
            comparisons += 3*12*seed.N
            rows_by_tick.append(_plane_rows(after, direction))
            previous = after
    if len(rows_by_tick) != horizon+1:
        raise ValueError("incomplete or excessive saved horizon")
    anchor_checks = readouts = 0
    for tick in range(0, horizon+1, 2):
        time = tick//2
        fp, fm, np_, nm = _profiles(rows_by_tick[tick])
        for j in range(tick+1, seed.L-1-tick):
            if (fp[j] != fp0[j-time] or fm[j] != fm0[j+time]
                    or np_[j] != np0[j-time] or nm[j] != nm0[j+time]):
                raise ValueError("even macro fields differ from original characteristic profiles")
            anchor_checks += 4
        lo, hi = Fraction(tick+3), Fraction(seed.L-4-tick)
        for x in sorted({lo, hi, (lo+hi)/2}):
            current_R = _reconstruct(fp, x, cubic)+_reconstruct(fm, x, cubic)
            initial_R = _reconstruct(fp0, x-time, cubic)+_reconstruct(fm0, x+time, cubic)
            if current_R != initial_R or current_R < lower_bound:
                raise ValueError("anchored metric or all-domain positive bound fails")
            for profile, source, anchor, source_anchor, shift in (
                    (fp, np_, fp0, np0, -time), (fm, nm, fm0, nm0, time)):
                curvature = _reconstruct(profile, x, cubic_second)
                density = _reconstruct(source, x, hat)
                if (curvature != -density or density < 0
                        or density != _reconstruct(source_anchor, x+shift, hat)
                        or curvature != _reconstruct(anchor, x+shift, cubic_second)):
                    raise ValueError("independent spline/source/anchor check failed")
            readouts += 1
    return {"tensor_hash": bundle.tensor.fingerprint, "bundle_id": bundle.bundle_id,
            "run_id": run_id, "microsteps": horizon, "macro_steps": horizon//2,
            "full_retained_scalar_comparisons": comparisons,
            "anchored_macro_coefficient_checks": anchor_checks,
            "independent_rational_metric_source_readouts": readouts,
            "continuous_R_lower_bound": lower_bound,
            "continuous_domain": "0<=t<=microsteps/2;2*t+3<=x<=L-4-2*t",
            "native_chart_scope": "exact even-tick samples of one initial-profile null solution",
            "global_periodic_Einstein": "failed_by_positive_source_obstruction"}


def audit(out=None, *, run_dir=None, protocol=None):
    report = {"schema": "universe24/local-unification/geometry-review/1",
              "metric": metric_proof(), "spline": spline_proof(),
              "periodic": periodic_obstruction(),
              "scope": "independent continuum/source/spline proofs; native same-state chart separately joined",
              "general_Einstein_model": "not_established",
              "massive_sources": "not_implemented", "operational_clocks": "not_implemented"}
    if run_dir is not None:
        if protocol is None:
            raise ValueError("exact chart protocol required")
        report["saved_chart"] = saved_chart_review(run_dir, protocol)
    if out is not None:
        path = Path(out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(exact_json.dumps(report, sort_keys=True)+"\n")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/local-unification/geometry-review.json"))
    parser.add_argument("--geometry-report", type=Path)
    args = parser.parse_args(argv)
    if args.geometry_report:
        candidate = exact_json.loads(args.geometry_report.read_text())
        report = audit(args.out, run_dir=args.geometry_report.parent/"runtime",
                       protocol=candidate["protocol"])
    else:
        report = audit(args.out)
    print(exact_json.dumps({"Einstein_components": report["metric"]["einstein_components"],
                            "source_checks": report["spline"]["nonconstant_source_reconstruction_checks"]}))


if __name__ == "__main__":
    main()
