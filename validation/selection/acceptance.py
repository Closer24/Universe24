"""Independent review of prepared reversible selection and saved apparatus runs.

The expected Boolean map uses a literal cycle, not the candidate's F, sorting
function, interpolation or preparation helper. Saved integer traces are checked
by the prior independent scalar Rule3 oracle. Neither audit advances physics.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
from itertools import product
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import Engine, State, exact_json
from universe24.system.bundle import create_bundle, load_bundle
from universe24.system.decoder import default_protocol, decode_transition
from universe24.system.runtime import run_bundle, verify_run
from validation.clock_links.acceptance_audit import scalar_step, structural_certificate


STATES = tuple(product((0, 1), repeat=3))
# Independently transcribed specification: only this 3-cycle moves.
CYCLE = ((0, 0, 1), (1, 1, 0), (1, 0, 1))
TABLE = {state: state for state in STATES}
TABLE.update({CYCLE[i]: CYCLE[(i + 1) % 3] for i in range(3)})
INVERSE = {output: source for source, output in TABLE.items()}
DIRECTIONS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def _xyz(node, side):
    return node // (side * side), (node // side) % side, node % side


def _index(point, side):
    x, y, z = (coordinate % side for coordinate in point)
    return (x * side + y) * side + z


def independent_gate(values, side, direction=(1, 0, 0), *, inverse=False):
    """Literal local permutation and one-lane transport with direct indexing."""
    values = np.asarray(values, dtype=object)
    if values.shape != (3, side**3) or any((type(v) is not int and not isinstance(v, np.integer))
                                          or int(v) not in (0, 1) for v in values.flat):
        raise ValueError("independent gate expects three Boolean lanes")
    if tuple(direction) not in DIRECTIONS:
        raise ValueError("one face direction required")
    result = np.empty_like(values)
    for node in range(side**3):
        point = _xyz(node, side)
        other = _index(tuple(point[k] + direction[k] for k in range(3)), side)
        if inverse:
            inputs = (int(values[0, node]), int(values[1, other]), int(values[2, node]))
            result[:, node] = INVERSE[inputs]
        else:
            output = TABLE[tuple(int(values[g, node]) for g in range(3))]
            result[0, node], result[1, other], result[2, node] = output
    return result


def independent_prepare(values, side, direction, carry):
    values = np.asarray(values, dtype=object)
    return State(side, independent_gate(values, side, direction, inverse=True), values,
                 np.full_like(values, carry))


def finite_ring_certificate():
    """Exhaust the closed three-site periodic ring, including every memory bit."""
    def update(state):
        out = [0] * 9
        for node in range(3):
            m, x, y = TABLE[(state[node], state[3 + node], state[6 + node])]
            out[node], out[3 + (node + 1) % 3], out[6 + node] = m, x, y
        return tuple(out)
    states = tuple(product((0, 1), repeat=9))
    mapping = {state: update(state) for state in states}
    assert len(set(mapping.values())) == 512
    assert all(sum(source[3:]) == sum(target[3:]) for source, target in mapping.items())
    cycles, unseen = Counter(), set(states)
    while unseen:
        start = min(unseen)
        current, length = start, 0
        while current in unseen:
            unseen.remove(current)
            current = mapping[current]
            length += 1
        assert current == start
        cycles[length] += 1
    return {"complete_ring_states": 512, "bijection": True,
            "cycle_lengths": {str(length): count for length, count in sorted(cycles.items())},
            "largest_period": max(cycles), "carrier_occupancy_conserved": True,
            "indefinite_strict_state_score_growth": "impossible on this finite permutation sector",
            "scope": "three-site ring; the general finite-state recurrence argument is separate from unbounded Rule3 integers"}


def native_audit(out):
    from validation.selection.clocks import build_native_gate
    from validation.selection.complexity import SORT_GATE
    expected_table = tuple(TABLE[state] for state in STATES)
    assert SORT_GATE == expected_table
    assert len(set(expected_table)) == 8
    assert all(TABLE[(0, x, y)][1] >= TABLE[(0, x, y)][2] for x, y in product((0, 1), repeat=2))
    # Retaining provenance changes total three-bit Hamming weight.
    assert sum(CYCLE[0]) == 1 and sum(TABLE[CYCLE[0]]) == 2
    states_checked, integers_checked, rewinds = 0, 0, 0
    certificates, intervention_rows = [], []
    representative = None
    rng = np.random.default_rng(800403)
    for direction in DIRECTIONS:
        tensor = build_native_gate(expected_table, direction=direction, name="selection")
        certificate = structural_certificate(tensor)
        certificates.append({"direction": list(direction), "tensor_hash": tensor.fingerprint, **certificate})
        engine = Engine(tensor)
        for triple, carry in product(STATES, range(6)):
            current = np.repeat(np.asarray(triple, dtype=object)[:, None], 27, axis=1)
            seed = independent_prepare(current, 3, direction, carry)
            expected = independent_gate(current, 3, direction)
            actual = engine.step(seed)
            assert np.array_equal(actual.b, expected)
            assert actual.same_as(scalar_step(tensor, seed))
            assert np.array_equal(actual.r, seed.r)
            assert engine.inverse_step(actual).same_as(seed)
            states_checked += 1
            integers_checked += 3 * 3 * 27
        for sample in range(4):
            current = rng.integers(0, 2, size=(3, 27)).astype(object)
            seed = independent_prepare(current, 3, direction, sample % 6)
            actual, expected = seed, current
            count = sum(int(v) for v in current[1:].flat)
            for _ in range(12):
                expected = independent_gate(expected, 3, direction)
                following = engine.step(actual)
                assert following.same_as(scalar_step(tensor, actual))
                assert np.array_equal(following.a, actual.b)
                assert np.array_equal(following.b, expected)
                assert np.array_equal(following.a, independent_gate(expected, 3, direction, inverse=True))
                assert sum(int(v) for v in following.b[1:].flat) == count
                assert np.array_equal(following.r, seed.r)
                actual = following
                states_checked += 1
                integers_checked += 3 * 3 * 27
            assert engine.rewind(actual, 12).same_as(seed)
            rewinds += 1
            if representative is None:
                representative = tensor, seed
        # Outside a=F^-1(b), Boolean interpretation is NOT invariant.
        zero = np.zeros((3, 27), dtype=object)
        bad = independent_prepare(zero, 3, direction, 5)
        bad.a[0, 0] = 1
        after = engine.step(bad)
        assert int(after.b[0, 0]) == -1
        assert after.same_as(scalar_step(tensor, bad))
        assert engine.inverse_step(after).same_as(bad)
        for side in (3, 5):
            for origin in (0, side**3 - 1):
                current = np.zeros((3, side**3), dtype=object)
                point = _xyz(origin, side)
                other = _index(tuple(point[k] + direction[k] for k in range(3)), side)
                current[1, other] = 1
                for node in range(side**3):
                    position = _xyz(node, side)
                    neighbor = _index(tuple(position[k] + direction[k] for k in range(3)), side)
                    current[2, node] = current[1, neighbor]
                alternative = current.copy(); alternative[0, origin] = 1
                left, right = [independent_prepare(value, side, direction, 4) for value in (current, alternative)]
                assert all(np.array_equal(getattr(left, field)[1:], getattr(right, field)[1:]) for field in ("a", "b", "r"))
                seeds = [left.to_dict(), right.to_dict()]
                differences = []
                outside_checks = 0
                for step in range(1, 5):
                    left, right = engine.step(left), engine.step(right)
                    differences.append(int(np.count_nonzero(left.b[1:] != right.b[1:])))
                    for node in range(side**3):
                        position = _xyz(node, side)
                        distance = sum(min((position[k]-point[k]) % side, (point[k]-position[k]) % side) for k in range(3))
                        if distance > step:
                            for field in ("a", "b", "r"):
                                assert np.array_equal(getattr(left, field)[:, node], getattr(right, field)[:, node])
                                outside_checks += 3
                assert differences == [2, 2, 2, 2]
                assert engine.rewind(left, 4).same_as(State.from_dict(seeds[0]))
                assert engine.rewind(right, 4).same_as(State.from_dict(seeds[1]))
                intervention_rows.append({"side": side, "direction": list(direction), "origin": origin,
                                          "same_complete_initial_carrier": True, "carrier_component_differences": differences,
                                          "outside_cone_integer_checks": outside_checks,
                                          "seeds": seeds, "finals": [left.to_dict(), right.to_dict()]})
    tensor, seed = representative
    channels = [{"index": i, "name": gear.name, "label": gear.label,
                 "owner": "independent_native_control", "purpose": "Prepared Boolean gate audit, no physical stress claim"}
                for i, gear in enumerate(tensor.gears)]
    bundle = create_bundle(tensor, seed, channels=channels, protocol=default_protocol(),
                           model={"id": "selection-independent-control", "version": "1",
                                  "domain": "Three-channel finite Boolean audit only"})
    runtime = run_bundle(bundle, Path(out) / "native-run", steps=12)
    return {"explicit_collision_table": [{"before": list(state), "after": list(TABLE[state])} for state in STATES],
            "ready_memory_sorting": True, "all_memory_hamming_conservation": False,
            "only_carrier_occupancy_conserved": True, "physical_energy_momentum_claim": False,
            "states_compared": states_checked, "retained_integer_comparisons": integers_checked,
            "full_rewinds": rewinds, "all_six_carries_and_directions": True,
            "off_sector_boolean_counterexamples": 6, "certificates": certificates,
            "history_interventions": intervention_rows, "finite_ring": finite_ring_certificate(),
            "saved_run": {key: runtime[key] for key in ("run_id", "bundle_id", "tensor_hash", "steps")}}


def source_identity_audit():
    """Independently differentiate the proposed homogeneous joint potential."""
    phi, chi, pi, eta, q, p, mass, omega, coupling, trace = sp.symbols("phi chi pi eta q p m2 w2 g K")
    intensity = phi**2 + chi**2
    joint = (pi*pi + eta*eta + p*p + mass*intensity + omega*q*q)/2 + coupling*q*intensity
    speed = {phi: pi, chi: eta, q: p,
             pi: trace*pi - mass*phi - 2*coupling*q*phi,
             eta: trace*eta - mass*chi - 2*coupling*q*chi,
             p: trace*p - omega*q - coupling*intensity}
    derivative = sp.expand(sum(sp.diff(joint, variable) * value for variable, value in speed.items()))
    assert sp.expand(derivative - trace*(pi*pi + eta*eta + p*p)) == 0
    charge = phi*eta - chi*pi
    assert sp.expand(sum(sp.diff(charge, variable)*value for variable, value in speed.items()) - trace*charge) == 0
    potential = joint.subs({pi:0, eta:0, p:0})
    valley = sp.expand(potential.subs(q, -coupling*intensity/omega))
    assert sp.expand(valley - mass*intensity/2 + coupling**2*intensity**2/(2*omega)) == 0
    assert potential.subs({phi:8, chi:0, q:-16, mass:1, omega:1, coupling:sp.Rational(1,4)}) == -96
    # Flat inhomogeneous p, q=0: assigned j=0 cannot balance pressure gradient.
    pressure_gradient = sp.diff(p*p/2, p).subs(p, 1)
    assert pressure_gradient == 1
    return {"homogeneous_total_exchange": "d_rho=trK*(Pi_phi^2+Pi_chi^2+p^2)",
            "homogeneous_charge_balance": "d_charge=trK*charge",
            "exact_symbolic_residuals": [0, 0],
            "potential_minimum_at_fixed_intensity": str(valley),
            "unbounded_potential_control": -96,
            "inhomogeneous_zero_momentum_pressure_defect": 1,
            "homogeneous_equation_identity": "passed",
            "generic_spatial_apparatus_conservation": "failed",
            "global_potential_lower_bound": "failed",
            "discrete_integer_energy_conservation": "not_proved_by_continuum_identity"}


def replay_saved(path):
    """Check existing saved data; never re-run a fixture to replace its evidence."""
    path = Path(path)
    runtime = verify_run(path)
    bundle = load_bundle(path / "bundle")
    structural_certificate(bundle.tensor)
    saved_events = []
    with gzip.open(path / "clicks.jsonl.gz", "rt", encoding="utf-8") as stream:
        saved_events = [exact_json.loads(line) for line in stream]
    expected_events, comparisons = [], 0
    with gzip.open(path / "full_trace.jsonl.gz", "rt", encoding="utf-8") as stream:
        for line in stream:
            record = exact_json.loads(line)
            before, after = (State.from_dict(record[field]) for field in ("before", "after"))
            assert scalar_step(bundle.tensor, before).same_as(after)
            expected_events.extend(decode_transition(record, bundle.tensor, run_id=runtime["run_id"]))
            comparisons += 3 * before.G * before.N
    assert saved_events == expected_events
    domain = {"model_id": bundle.model["id"], "domain": bundle.model["domain"]}
    if "projective.denominator" in bundle.tensor.names:
        denominator = bundle.tensor.gear_index("projective.denominator")
        # The source's current ratios, never its invalid old D=0 boundary slice.
        assert denominator == 0 and all(int(value)>0 for value in bundle.seed.b[denominator])
        assert all(int(value)==0 for value in bundle.seed.a[denominator])
        initial = {name.removeprefix("projective."): Fraction(int(bundle.seed.b[i, 0]), int(bundle.seed.b[denominator, 0]))
                   for i, name in enumerate(bundle.tensor.names) if name.startswith("projective.") and i != denominator}
        homogeneous = all(all(int(v)==int(row[0]) for v in row) for row in bundle.seed.b[:47])
        if bundle.model["id"] == "selection-reciprocal47" and homogeneous:
            trace = sum(initial[f"K{i}{i}"] for i in range(3))
            square = sum(initial[f"K{min(i,j)}{max(i,j)}"]**2 for i in range(3) for j in range(3))
            assert all(initial[f"B{i}{j}"] == int(i==j) for i in range(3) for j in range(3))
            assert all(initial[name]==0 for name in initial if name.startswith(("Xi_", "E", "M", "G")))
            assert initial["dust_amplitude"] == 0
            rho = (initial["Pi_phi"]**2 + initial["Pi_chi"]**2 +
                   Fraction(bundle.model["mass_squared"])*(initial["phi"]**2+initial["chi"]**2) +
                   initial["apparatus_p"]**2 + Fraction(bundle.model["omega_squared"])*initial["apparatus_q"]**2)/2
            rho += Fraction(bundle.model["interaction"])*initial["apparatus_q"]*(initial["phi"]**2+initial["chi"]**2)
            domain["initial_homogeneous_H_if_flat_zero_gradient"] = str(trace**2-square-2*rho)
            assert trace**2-square-2*rho == 0
        domain["readout"] = "current numerator/current positive D; old D=0 is boundary memory"
    if bundle.model.get("physical_record_stress"):
        domain["record_stress"] = bundle.model["physical_record_stress"]
        domain["physical_energy_source_acceptance"] = "not_established_for_audit_record_feedback"
    return {"path": str(path), "bundle_id": bundle.bundle_id, "run_id": runtime["run_id"],
            "tensor_hash": bundle.tensor.fingerprint, "steps": runtime["steps"],
            "channels": bundle.tensor.G, "retained_integer_comparisons": comparisons,
            "canonical_records_compared": len(saved_events), "complete_saved_scalar_replay": True,
            "maximum_integer_bits_by_step": runtime["maximum_integer_bits_by_step"], "scope": domain}


def audit(out, runs=()):
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("fresh acceptance directory required")
    out.mkdir(parents=True, exist_ok=True)
    native = native_audit(out)
    saved = [replay_saved(out / "native-run")] + [replay_saved(path) for path in runs]
    root = Path(__file__).resolve().parents[2]
    paths = ["validation/selection/acceptance.py", "validation/selection/clocks.py",
             "validation/selection/complexity.py", "validation/clock_links/acceptance_audit.py"]
    report = {"schema": "universe24/selection/independent-acceptance/1", "native": native,
              "homogeneous_source_review": source_identity_audit(), "saved_runs": saved,
              "source_sha256": {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in paths},
              "physical_gates": {"general_einstein": "not_tested", "metric_material_clock": "not_tested",
                                 "indefinite_boolean_complexity_growth": "excluded_by_finite_permutation",
                                 "Born_measure_from_native_gate": "not_derived",
                                 "full_48_record_energy_source": "not_supplied"}}
    (out / "acceptance.json").write_text(exact_json.dumps(report, sort_keys=True)+"\n", encoding="utf-8")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/selection/acceptance"))
    parser.add_argument("--run", type=Path, action="append", default=[])
    args = parser.parse_args(argv)
    report = audit(args.out, args.run)
    print(exact_json.dumps({"native_states":report["native"]["states_compared"],
                           "saved_runs":len(report["saved_runs"]), "physical_gates":report["physical_gates"]}))


if __name__ == "__main__":
    main()
