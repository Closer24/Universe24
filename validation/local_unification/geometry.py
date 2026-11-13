"""Source-coupled finite-chart Einstein sector of the carrier/record tensor.

Twelve complete channels use the unchanged Engine.  The continuum readout is
an exact two-null-stream chart on a proved finite causal interior, not a
global periodic universe or a general/massive Einstein model.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np

from validation.padding import sector_state
from universe24.core import Engine, GearType, State, Tensor, lattice
from universe24.core import exact_json
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run
from validation.local_unification import native

ZERO = (0, 0, 0)
PROFILE_NAMES = ("geometry.A.plus", "geometry.A.minus", "geometry.B.plus", "geometry.B.minus")
# target, opposite-bank profile, opposite-bank directional source, offset sign
PROFILE_ROWS = ((8, 10, (4, 6), -1), (9, 11, (5, 7), 1),
                (10, 8, (0, 2), 1), (11, 9, (1, 3), -1))


def build_tensor(direction=(1, 0, 0), *, source_coupling=True, coupled=True):
    """Substitute Delta^2 F=-q into the actual paired shift compiler.

    For plus profiles u_A=3(3 B-B(x-d)-q_B) and
    u_B=3(3 A-A(x+d)-q_A); minus reverses d.
    Complete Rule3 inversion remains valid outside the physical chart.
    """
    if type(source_coupling) is not bool:
        raise ValueError("source_coupling must be an exact boolean")
    base = native.build_tensor(direction, coupled=coupled)
    direction = tuple(direction)
    terms = [(m.target, m.coeff, [(f.gear, f.offset, f.field) for f in m.factors])
             for m in base.monomials]
    for target, source, rails, sign in PROFILE_ROWS:
        offset = tuple(sign*v for v in direction)
        terms += [(target, 9, [(source, ZERO, "b")]),
                  (target, -3, [(source, offset, "b")])]
        if source_coupling:
            terms += [(target, -3, [(rail, ZERO, "b")]) for rail in rails]
    return Tensor(list(base.gears)+[GearType(name, "audit") for name in PROFILE_NAMES],
                  terms, strict_support=True)


def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an exact integer >= {minimum}")
    return value


def _rational(value):
    if type(value) in (int, Fraction):
        return Fraction(value)
    if isinstance(value, np.integer) and not isinstance(value, np.bool_):
        return Fraction(int(value))
    raise ValueError("exact rational values required; floats and booleans rejected")


def _axis_coordinate(L, direction):
    direction = native._options(direction, True, True)
    axis = next(i for i, value in enumerate(direction) if value)
    coordinate = lattice(L).all_coords()[:, axis]
    return coordinate if direction[axis] == 1 else L-1-coordinate


def antiderivative(source, *, height):
    """Integer coefficients whose interior centered Laplacian is -source."""
    if len(source) < 3 or any(type(q) is not int or q < 0 for q in source):
        raise ValueError("nonnegative exact source coefficients required")
    _integer(height, "height", 1)
    result = [height, height]
    for j in range(1, len(source)-1):
        result.append(2*result[-1]-result[-2]-source[j])
    return result


def prepare_fixture(L=19, steps=6, direction=(1, 0, 0), *, coupled=True,
                    remove_first_record=False):
    """Plane-tile the repeated encounter, away from the finite-chart seam.

    Every geometry coefficient/history is retained before evolution.  Initial
    profile construction is static preparation, never a runtime solve.
    """
    _integer(L, "L", 7)
    _integer(steps, "steps", 2)
    if L % 2 != 1 or steps % 2 or L < 2*(steps+3)+1:
        raise ValueError("odd L >= 2*(microsteps+3)+1 and even microsteps required")
    if type(remove_first_record) is not bool or type(coupled) is not bool:
        raise ValueError("preparation options must be exact booleans")
    coordinate = _axis_coordinate(L, direction)
    center = L//2
    current = np.zeros((12, L**3), dtype=object)
    for distance in (0, 2):
        if not (remove_first_record and distance == 0):
            current[4, coordinate == center-distance] = 1
        current[7, coordinate == center+distance] = 1
    for distance in (1, 3):
        current[0, coordinate == center-distance] = 1
        current[3, coordinate == center+distance] = 1
    profiles = []
    representatives = [int(np.flatnonzero(coordinate == j)[0]) for j in range(L)]
    for bank, offset in ((0, 8), (4, 10)):
        for lane in (0, 1):
            q = [int(current[bank+lane, node])+int(current[bank+lane+2, node])
                 for node in representatives]
            profile = antiderivative(q, height=8*L*L)
            current[offset+lane] = np.asarray(profile, dtype=object)[coordinate]
            profiles.append(profile)
    previous = np.zeros_like(current)
    previous[:8] = native.first_order(current[:8], L, direction, coupled=coupled, inverse=True)
    grid = lattice(L)
    direction = tuple(direction)
    previous[8] = current[10, grid.shift_index(direction)]
    previous[9] = current[11, grid.shift_index(tuple(-v for v in direction))]
    previous[10:12] = current[8:10]
    carries = np.asarray([[(g+n) % 6 for n in range(L**3)] for g in range(12)], dtype=object)
    seed = State(L, previous, current, carries)
    protocol = {
        "schema": "universe24/two-null-stream-chart/1", "L": L,
        "direction": list(direction), "microsteps": steps, "ticks_per_macro": 2,
        "receiver_coordinate": center, "safe_coefficient_margin": steps+1,
        "spline_support": 2, "interior_coordinate": center,
        "initial_profiles": profiles, "collision_coupled": coupled,
        "physical_domain": "finite causal interior with R>0; not periodic spacetime",
        "readout": "full retained state at even microticks, cubic B-spline metric and linear-hat source",
    }
    return build_tensor(direction, coupled=coupled), seed, protocol


def profile_constraints(state, direction=(1, 0, 0)):
    """All sites, including every nonphysical periodic seam, are returned."""
    grid = state.lattice
    plus = grid.shift_index(tuple(direction))
    minus = grid.shift_index(tuple(-v for v in direction))
    result = []
    for row, rails in ((8, (0, 2)), (9, (1, 3)), (10, (4, 6)), (11, (5, 7))):
        f = state.b[row].astype(object)
        result.append(f[plus]-2*f+f[minus]+state.b[rails[0]]+state.b[rails[1]])
    return np.asarray(result, dtype=object)


def ideal_step(current, L, direction=(1, 0, 0), *, coupled=True):
    """Independent characteristic shift oracle, valid only in the chart."""
    grid = lattice(L)
    result = np.zeros_like(current)
    result[:8] = native.first_order(current[:8], L, direction, coupled=coupled)
    result[8:10] = current[10:12]
    result[10] = current[8, grid.shift_index(tuple(-v for v in direction))]
    result[11] = current[9, grid.shift_index(tuple(direction))]
    return result


def b1(value):
    """Centered linear cardinal B-spline, evaluated exactly."""
    return max(Fraction(0), 1-abs(_rational(value)))


def b3(value, derivative=0):
    """Centered cubic cardinal B-spline and its first two derivatives."""
    if type(derivative) is not int or derivative not in (0, 1, 2):
        raise ValueError("derivative must be an exact integer in 0..2")
    x = _rational(value)
    if derivative == 2:
        return b1(x+1)-2*b1(x)+b1(x-1)
    sign = 1 if x >= 0 else -1
    a = abs(x)
    if a >= 2:
        return Fraction(0)
    if derivative == 1:
        return sign*((-12*a+9*a*a)/6 if a < 1 else -(2-a)**2/2)
    return (4-6*a*a+3*a*a*a)/6 if a < 1 else (2-a)**3/6


def reconstruct(coefficients, x, *, derivative=0, degree=3):
    """Compact-support reconstruction; no future lookup or state mutation."""
    if (type(degree) is not int or degree not in (1, 3)
            or type(derivative) is not int or derivative not in (0, 1, 2)
            or (degree == 1 and derivative)):
        raise ValueError("use B1, or B3 with derivative 0..2")
    x = _rational(x)
    kernel = b1 if degree == 1 else lambda value: b3(value, derivative)
    return sum((_rational(value)*kernel(x-j) for j, value in enumerate(coefficients)), Fraction(0))


def validate_protocol(protocol):
    if type(protocol) is not dict or protocol.get("schema") != "universe24/two-null-stream-chart/1":
        raise ValueError("unsupported physical chart protocol")
    L = _integer(protocol.get("L"), "L", 7)
    steps = _integer(protocol.get("microsteps"), "microsteps", 2)
    if L % 2 != 1 or steps % 2 or L < 2*(steps+3)+1:
        raise ValueError("unsafe chart extent or horizon")
    native._options(protocol.get("direction", ()), True, True)
    for name, expected in (("ticks_per_macro", 2), ("spline_support", 2),
                           ("safe_coefficient_margin", steps+1),
                           ("interior_coordinate", L//2), ("receiver_coordinate", L//2)):
        if type(protocol.get(name)) is not int or protocol[name] != expected:
            raise ValueError(f"wrong {name} in chart protocol")
    if type(protocol.get("collision_coupled")) is not bool:
        raise ValueError("declare collision_coupled as an exact boolean")
    profiles = protocol.get("initial_profiles")
    if (type(profiles) is not list or len(profiles) != 4
            or any(type(row) is not list or len(row) != L for row in profiles)
            or any(type(value) is not int or value <= 0 for row in profiles for value in row)):
        raise ValueError("declare four complete positive integer profile charts")
    return True


def readout(state, microstep, protocol, *, coordinate=None):
    """Exact snapshot readout, conditional on independently verified evolution.

    A passing current-slice residual does not by itself establish that this
    state was generated by the declared tensor.  Saved-run replay and the
    causal-chart certificate are separate mandatory checks.
    """
    _integer(microstep, "microstep")
    validate_protocol(protocol)
    if not isinstance(state, State):
        raise ValueError("a complete exact State is required")
    try:
        state = State(state.L, state.a, state.b, state.r)
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid exact retained State") from exc
    state = sector_state(state, 12)
    if (state.L != protocol["L"] or state.b.shape[0] != 12
            or microstep % 2 or microstep > protocol["microsteps"]):
        raise ValueError("readout requires twelve channels and even in-horizon microticks")
    if any(value < 0 or value >= 6 for value in state.r.flat):
        raise ValueError("all retained carries must be in 0..5")
    native.validate_prepared_state(State(state.L, state.a[:8], state.b[:8], state.r[:8]),
                                   protocol["direction"], coupled=protocol["collision_coupled"])
    x = _rational(protocol["interior_coordinate"] if coordinate is None else coordinate)
    margin = microstep+3
    if not margin <= x <= state.L-1-margin:
        raise ValueError("spline support is outside the verified causal chart")
    coords = _axis_coordinate(state.L, protocol["direction"])
    rows = []
    for row in range(12):
        values = []
        for j in range(state.L):
            plane = state.b[row, coords == j]
            if any(value != plane[0] for value in plane):
                raise ValueError("physical readout requires plane-symmetric current fields")
            values.append(int(plane[0]))
        rows.append(values)
    fp = [rows[8][j]+rows[10][j] for j in range(state.L)]
    fm = [rows[9][j]+rows[11][j] for j in range(state.L)]
    qp = [sum(rows[r][j] for r in (0, 2, 4, 6)) for j in range(state.L)]
    qm = [sum(rows[r][j] for r in (1, 3, 5, 7)) for j in range(state.L)]
    R = reconstruct(fp, x)+reconstruct(fm, x)
    if R <= 0:
        raise ValueError("Lorentzian chart requires R>0")
    np_, nm = reconstruct(qp, x, degree=1), reconstruct(qm, x, degree=1)
    residual = (reconstruct(fp, x, derivative=2)+np_, reconstruct(fm, x, derivative=2)+nm)
    if any(residual):
        raise ValueError("same-state source/curvature constraint failed")
    return {"macro_time": Fraction(microstep, 2), "coordinate": x, "R": R,
            "n_plus": np_, "n_minus": nm, "G_uu": np_/R, "G_vv": nm/R,
            "other_Einstein_components": 0, "scalar_curvature": 0,
            "energy_numerator": np_+nm, "momentum_numerator": np_-nm,
            "dominant_energy_numerator": np_+nm-abs(np_-nm),
            "source_curvature_residual": residual}


@lru_cache(maxsize=1)
def symbolic_certificate():
    """Independent metric->connection->Ricci, divergence and affine rays."""
    import sympy as s
    u, v, y, z = s.symbols("u v y z", real=True)
    f, g = s.Function("f")(u), s.Function("g")(v)
    R = f+g
    coords = (u, v, y, z)
    metric = s.Matrix([[0, -R**s.Rational(-1, 2), 0, 0],
                       [-R**s.Rational(-1, 2), 0, 0, 0], [0, 0, R, 0], [0, 0, 0, R]])
    inv = metric.inv()
    gamma = [[[s.simplify(sum(inv[a,d]*(s.diff(metric[d,c],coords[b])+
                  s.diff(metric[d,b],coords[c])-s.diff(metric[b,c],coords[d]))
                  for d in range(4))/2) for c in range(4)] for b in range(4)] for a in range(4)]
    ricci = s.Matrix(4, 4, lambda a,b: s.simplify(sum(
        s.diff(gamma[c][a][b],coords[c])-s.diff(gamma[c][a][c],coords[b])+
        sum(gamma[c][c][d]*gamma[d][a][b]-gamma[c][b][d]*gamma[d][a][c]
            for d in range(4)) for c in range(4))))
    scalar = s.simplify(sum(inv[a,b]*ricci[a,b] for a in range(4) for b in range(4)))
    expected = s.diag(-s.diff(f,u,2)/R, -s.diff(g,v,2)/R, 0, 0)
    residual = [s.simplify(value) for value in ricci-scalar*metric/2-expected]
    raised = s.simplify(inv*expected*inv)
    divergence = [s.simplify(sum(s.diff(raised[mu,nu],coords[mu])+
        sum(gamma[mu][mu][k]*raised[k,nu]+gamma[nu][mu][k]*raised[mu,k]
            for k in range(4)) for mu in range(4))) for nu in range(4)]
    accelerations = []
    for axis in (0, 1):
        ray = [s.sqrt(R) if j == axis else s.Integer(0) for j in range(4)]
        accelerations += [s.simplify(sum(ray[mu]*s.diff(ray[nu],coords[mu])+
            sum(gamma[nu][mu][k]*ray[mu]*ray[k] for k in range(4)) for mu in range(4)))
                          for nu in range(4)]
    assert residual == [0]*16 and scalar == 0
    assert divergence == [0]*4 and accelerations == [0]*8
    return {"Einstein_component_identities": 16, "covariant_balance_identities": 4,
            "affine_null_geodesic_components": 8, "all_exact_residuals_zero": True,
            "metric": "ds2=-2 R^(-1/2)du dv+R(dy2+dz2), R=f(u)+g(v)>0",
            "source": "T_uu=-f''/R, T_vv=-g''/R; 8piG=c=1",
            "physical_coordinates": "u=t-x,v=t+x; one macrotime=two Engine ticks",
            "orthonormal_energy": "rho=(n_plus+n_minus)/(2sqrt(R)),flux=(n_plus-n_minus)/(2sqrt(R))"}


def _json(value):
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, dict):
        return {key: _json(item) for key,item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json(item) for item in value]
    return value


def audit(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    law, seed, protocol = prepare_fixture()
    engine = Engine(law)
    state, ideal = seed, seed.b.copy()
    coords = _axis_coordinate(seed.L, protocol["direction"])
    cases, peak_bits = [], []
    comparisons = source_checks = 0
    for tick in range(protocol["microsteps"]+1):
        safe = (coords >= tick+1)&(coords <= seed.L-2-tick)
        assert np.array_equal(state.b[:,safe], ideal[:,safe])
        assert not any(int(v) for v in profile_constraints(state)[:,safe].flat)
        comparisons += int(12*np.sum(safe))
        source_checks += int(4*np.sum(safe))
        peak_bits.append(max(abs(int(v)).bit_length() for a in (state.a,state.b,state.r) for v in a.flat))
        if tick % 2 == 0:
            cases.append(readout(state, tick, protocol))
        if tick < protocol["microsteps"]:
            following = engine.step(state)
            assert engine.inverse_step(following).same_as(state)
            assert np.array_equal(following.r, seed.r)
            ideal = ideal_step(ideal, state.L)
            state = following
    assert engine.rewind(state, protocol["microsteps"]).same_as(seed)

    wrong = build_tensor(source_coupling=False)
    wrong_state = Engine(wrong).run(seed, 2)
    assert Engine(wrong).rewind(wrong_state, 2).same_as(seed)
    wrong_defect = max(abs(int(v)) for v in profile_constraints(wrong_state)[:,
                      (coords >= 3)&(coords <= seed.L-4)].flat)
    assert wrong_defect > 0
    qsum = sum(int(v) for v in seed.b[:8].flat)
    seam = max(abs(int(v)) for v in profile_constraints(seed).flat)
    assert qsum > 0 and seam > 0

    # Source intervention with compatible re-preparation is a new physical
    # preparation.  Its initial metric changes with its initial source.
    _, source_seed, source_protocol = prepare_fixture(remove_first_record=True)
    original_readout = readout(seed, 0, protocol)
    altered_readout = readout(source_seed, 0, source_protocol)
    assert original_readout["R"] != altered_readout["R"]
    assert original_readout["G_uu"] != altered_readout["G_uu"]

    # Holding geometry fixed instead is an explicitly off-constraint control.
    mechanical = source_seed.copy()
    for field in ("a", "b", "r"):
        getattr(mechanical, field)[8:] = getattr(seed, field)[8:]
    base_next, source_next = engine.step(seed), engine.step(mechanical)
    response = int(np.sum(base_next.b[8:] != source_next.b[8:]))
    assert response > 0 and engine.inverse_step(source_next).same_as(mechanical)

    # Collision-off preserves total directional sources and all geometry,
    # although records/carriers differ.  This is a degenerate stress response.
    off_law, off_seed, _ = prepare_fixture(coupled=False)
    assert np.array_equal(seed.b, off_seed.b)
    original, disconnected = seed, off_seed
    label_differences = 0
    for _ in range(protocol["microsteps"]):
        original = engine.step(original)
        disconnected = Engine(off_law).step(disconnected)
        assert np.array_equal(original.b[8:], disconnected.b[8:])
        for rails in ((0,2,4,6),(1,3,5,7)):
            assert np.array_equal(sum(original.b[r] for r in rails),
                                  sum(disconnected.b[r] for r in rails))
        label_differences += int(np.sum(original.b[:8] != disconnected.b[:8]))
    assert label_differences > 0
    assert Engine(off_law).rewind(disconnected, protocol["microsteps"]).same_as(off_seed)

    channels = [{"index": i, "name": gear.name, "owner": "null_streams" if i < 8 else "geometry",
                 "label": gear.label, "purpose": "retained carrier/record rail" if i < 8
                 else "retained source-coupled spline coefficient"} for i,gear in enumerate(law.gears)]
    bundle = create_bundle(law, seed, channels=channels, protocol=default_protocol(),
        model={"id": "local-unification-two-null-stream-chart", "version": "1",
               "domain": "Plane-symmetric finite causal chart; even ticks; positive R; not global periodic Einstein"})
    run = run_bundle(bundle, out/"runtime", steps=protocol["microsteps"])
    verified = verify_run(out/"runtime")
    report = {
        "schema": "universe24/local-unification/geometry/1", "tensor_hash": law.fingerprint,
        "channels": bundle.tensor.G, "active_channels": law.G, "retained_integers_per_node": 3*bundle.tensor.G, "degree": law.rank-1,
        "strict_support_violations": len(law.support_violations()),
        "protocol": protocol, "symbolic": symbolic_certificate(),
        "interior_coefficient_comparisons": comparisons, "interior_source_constraints": source_checks,
        "readouts": cases, "peak_bits_by_tick": peak_bits,
        "wrong_source_defect": wrong_defect, "wrong_source_rewind": True,
        "compatible_source_intervention": {"original": original_readout, "altered": altered_readout},
        "off_constraint_source_intervention_geometry_changes": response,
        "collision_off_same_geometry": True, "collision_off_label_differences": label_differences,
        "global_periodic_source_sum": qsum, "initial_seam_defect": seam,
        "runtime": run, "runtime_verified": verified["run_id"],
        "scope": {"restricted_null_source_Einstein_chart": "passed",
                  "global_periodic_Einstein": "failed", "massive_matter": "not_tested",
                  "operational_proper_time_clock": "not_tested", "general_Einstein": "not_established"},
    }
    (out/"geometry.json").write_text(exact_json.dumps(_json(report), sort_keys=True)+"\n")
    return _json(report)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/local-unification/geometry"))
    args = parser.parse_args(argv)
    report = audit(args.out)
    print(exact_json.dumps({key:report[key] for key in ("tensor_hash", "channels", "scope")}, sort_keys=True))


if __name__ == "__main__":
    main()
