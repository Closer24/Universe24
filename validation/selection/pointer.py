"""Retained pulse memory and feedback, compiled as fixed Rule3 data.

The native three-channel control is a validation primitive, not another
supported universe. The append adapter adds one audit memory to a supplied
bundle. Raw feedback into a projective field is a declared test approximation,
not a source-complete physical interaction or a Born-rule instrument.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np

from universe24.core import exact_json
from universe24.core.engine import Engine, State, exact_array
from universe24.core.lattice import DIRECTIONS, ZERO
from universe24.core.tensor import Factor, GearType, Monomial, Tensor
from universe24.system.bundle import create_bundle, load_bundle, validate_bundle
from universe24.system.decoder import default_protocol, decode_transition, make_transition
from universe24.system.runtime import run_bundle

POINTER_NAME = "selection.pointer_memory"
VERSION = "retained-pointer/1"


def velocity(state, channel):
    """Full-state diagnostic. Not a quantity reconstructed from click absence."""
    return state.b[channel].astype(object) - state.a[channel].astype(object)


def append_native_pointer(base, *, writer_name, writer_power=1, clock_name=None,
                          feedback_target=None, feedback=1, memory_a=None,
                          memory_b=None, memory_r=None):
    """Append u_m=6b_m+3F, and optionally add 3*feedback*(b_m-a_m).

    F is a raw retained b-field power, optionally times a raw local clock
    b-field. F is an integer datum, not a decoded physical projective value.
    Complete carry retention proves v'=v+F for all six remainders. All
    preparation happens before evolution; this function supplies no callbacks.
    """
    base = validate_bundle(base)
    if base.tensor.G >= 48:
        raise ValueError("one pointer channel would exceed 48")
    if POINTER_NAME in base.tensor.names:
        raise ValueError("pointer memory already present")
    if type(writer_power) is not int or not 1 <= writer_power <= 3:
        raise ValueError("writer_power must be 1, 2 or 3")
    if type(feedback) is not int:
        raise ValueError("feedback must be an exact integer")
    writer = base.tensor.gear_index(writer_name)
    factors = [Factor(writer, ZERO, "b")] * writer_power
    if clock_name is not None:
        factors.append(Factor(base.tensor.gear_index(clock_name), ZERO, "b"))
    if len(factors) > 3:
        raise ValueError("clock-gated writer exceeds degree three")
    if any(base.tensor.gears[f.gear].link is not None for f in factors):
        raise ValueError("pointer writer ports must be node fields")
    index = base.tensor.G
    gears = list(base.tensor.gears) + [GearType(POINTER_NAME, label="audit")]
    terms = list(base.tensor.monomials) + [
        Monomial(index, 6, (Factor(index, ZERO, "b"),)),
        Monomial(index, 3, tuple(factors))]
    if feedback_target is not None:
        target = base.tensor.gear_index(feedback_target)
        if base.tensor.gears[target].link is not None:
            raise ValueError("feedback target must be a node field")
        terms.extend((Monomial(target, 3 * feedback, (Factor(index, ZERO, "b"),)),
                      Monomial(target, -3 * feedback, (Factor(index, ZERO, "a"),))))
    designations = [(target, factors, why)
                    for (target, factors), why in base.tensor.designations.items()]
    tensor = Tensor(gears, terms, designated_one_way=designations, strict_support=True)
    original = base.seed
    arrays = []
    for field, value in (("a", memory_a), ("b", memory_b), ("r", memory_r)):
        extra = (np.zeros((1, original.N), dtype=object) if value is None
                 else exact_array(value, (1, original.N)))
        arrays.append(np.concatenate((getattr(original, field).astype(object), extra), axis=0))
    channels = list(base.channels) + [{
        "index": index, "name": POINTER_NAME, "label": "audit", "owner": "test_pointer",
        "purpose": "Raw integer persistent velocity record; zero declared physical stress is a test approximation",
        "readout_dependencies": [POINTER_NAME, writer_name] + ([] if clock_name is None else [clock_name])}]
    return create_bundle(tensor, State(original.L, *arrays), channels=channels,
                         protocol=base.protocol, model={
                             "id": "proposal-retained-pointer", "version": VERSION,
                             "domain": "Mechanical retained memory/feedback test; no physical detector or conserved record stress",
                             "base_model": base.model, "base_bundle_id": base.bundle_id,
                             "writer_name": writer_name, "writer_power": writer_power,
                             "clock_name": clock_name, "feedback_target": feedback_target,
                             "feedback": feedback,
                             "physical_record_stress": "not supplied; audit-memory test approximation",
                             "projective_feedback": "raw numerator perturbation; not a proved physical continuum coupling"})


def native_control(*, side=7, direction=0, amplitude=1, second_amplitude=0,
                   carry=0, feedback=1, history=0):
    """Three retained channels: traveling pulse, persistent memory, later response.

    Each complete seed fixes its propagation direction and apparatus history.
    No precomputed trajectory or per-step input is used. The periodic wave
    returns after side updates; the finite persistence claim stops before it.
    """
    for name, value in (("side", side), ("direction", direction), ("amplitude", amplitude),
                        ("second_amplitude", second_amplitude), ("carry", carry),
                        ("feedback", feedback), ("history", history)):
        if type(value) is not int:
            raise ValueError(f"{name} must be an exact integer")
    if side < 5 or not 0 <= direction < 6 or not 0 <= carry < 6:
        raise ValueError("invalid side, direction or carry")
    forward, backward = DIRECTIONS[direction], DIRECTIONS[direction ^ 1]
    gears = [GearType(name, label="audit") for name in
             ("control.pulse", "control.memory", "control.response")]
    terms = [(0, 3, [(0, forward, "b")]), (0, 3, [(0, backward, "b")]),
             (1, 6, [(1, ZERO, "b")]), (1, 3, [(0, ZERO, "b"), (0, ZERO, "b")]),
             (2, 6, [(2, ZERO, "b")]), (2, 3 * feedback, [(1, ZERO, "b")]),
             (2, -3 * feedback, [(1, ZERO, "a")])]
    tensor = Tensor(gears, terms, strict_support=True)
    a = np.zeros((3, side ** 3), dtype=object)
    b = np.zeros_like(a)
    r = np.full_like(a, carry)
    seed = State(side, a, b, r)
    first = seed.lattice.index(0, 0, 0)
    axis = direction // 2
    transverse = (axis + 1) % 3
    second_xyz = [0, 0, 0]
    second_xyz[transverse] = 2
    second = seed.lattice.index(*second_xyz)
    b[0, first], b[0, second] = amplitude, second_amplitude
    a[0] = b[0, seed.lattice.shift_index(forward)]
    detectors = [seed.lattice.neighbour(first, direction), seed.lattice.neighbour(second, direction)]
    # Equal current memory b with different old a carries a real retained
    # history intervention, rather than an external reader-selected branch.
    a[1, detectors[0]] = -history
    seed = State(side, a, b, r)
    channels = [{"index": i, "name": g.name, "label": "audit", "owner": "native_pointer_control",
                 "purpose": "Finite causal memory/feedback validation only"} for i, g in enumerate(gears)]
    bundle = create_bundle(tensor, seed, channels=channels, protocol=default_protocol(), model={
        "id": "validation-native-pointer-control", "version": VERSION,
        "domain": "Exact native finite-window pulse-memory-feedback control, no geometry/energy/Born interpretation",
        "direction": direction, "detector_nodes": detectors, "amplitudes": [amplitude, second_amplitude],
        "history": history, "feedback": feedback, "recurrence_period": side})
    return bundle


def _oracle(state, *, direction, feedback):
    """Hand-expanded independent scalar update; never evaluates Tensor or Engine."""
    old = state.to_dict()
    a, b, r = (old[name] for name in ("a", "b", "r"))
    nxt_b = [[0] * state.N for _ in range(3)]
    nxt_r = [[0] * state.N for _ in range(3)]
    for node in range(state.N):
        plus = state.lattice.neighbour(node, direction)
        minus = state.lattice.neighbour(node, direction ^ 1)
        values = (3 * (b[0][plus] + b[0][minus]),
                  6 * b[1][node] + 3 * b[0][node] ** 2,
                  6 * b[2][node] + 3 * feedback * (b[1][node] - a[1][node]))
        for channel, u in enumerate(values):
            quotient, remainder = divmod(2 * u + r[channel][node], 6)
            nxt_b[channel][node] = quotient - a[channel][node]
            nxt_r[channel][node] = remainder
    return State(state.L, b, nxt_b, nxt_r)


def inspect_control(bundle, *, steps=None):
    """Collect every declared local tick, retaining both possible port outcomes."""
    model = bundle.model
    steps = bundle.seed.L + 1 if steps is None else steps
    direction, feedback = model["direction"], model["feedback"]
    state, engine = bundle.seed, Engine(bundle.tensor)
    initial = state.copy()
    nodes = model["detector_nodes"]
    rows = []
    record_count = 0
    max_bits = 0
    for step in range(steps + 1):
        v = velocity(state, 1)
        rows.append({"tick": step, "pulse": [int(state.b[0, n]) for n in nodes],
                     "record_velocity": [int(v[n]) for n in nodes],
                     "response": [int(state.b[2, n]) for n in nodes],
                     "outcomes": [name for name, n in zip(("left", "right"), nodes) if v[n] > 0]})
        max_bits = max(max_bits, max(abs(int(x)).bit_length() for field in (state.a, state.b, state.r) for x in field.flat))
        if step == steps:
            break
        before = state
        state = engine.step(before)
        if not state.same_as(_oracle(before, direction=direction, feedback=feedback)):
            raise AssertionError("independent pointer oracle mismatch")
        if not engine.inverse_step(state).same_as(before):
            raise AssertionError("pointer inverse mismatch")
        record_count += len(decode_transition(make_transition(bundle.tensor, before, state,
                              run_id="native-pointer-control", step=step + 1), bundle.tensor))
    if not engine.rewind(state, steps).same_as(initial):
        raise AssertionError("pointer complete rewind failed")
    return {"tensor_hash": bundle.tensor.fingerprint, "bundle_id": bundle.bundle_id,
            "channels": bundle.tensor.G, "steps": steps, "local_ticks": rows,
            "independent_scalar_oracle": True, "exact_complete_rewind": True,
            "maximum_integer_bits": max_bits, "canonical_arithmetic_records": record_count,
            "ready_tick": 0, "arrival_tick": 1, "decision_tick": 2,
            "feedback_first_tick": 3, "last_tick_before_second_write": bundle.seed.L + 1,
            "record_definition": "v=b_memory-a_memory; label present iff v>0; every port retained",
            "interpretation": "Finite causal record/feedback control, not exclusive outcome selection or physical proper-time ticks"}


def audit_appended(base, out, *, steps=4):
    """Check the actual 47+1 handoff, retaining its physical-feedback caveat.

    Zero-history connected/disconnected runs first agree, then the newly
    acquired raw record changes retained apparatus. A separate matched-history
    intervention establishes that the record is a cause, not a display label.
    Raw feedback is not an energy-complete extension of the physical model.
    """
    from universe24.tests.test_migration import scalar_step

    if not hasattr(base, "tensor"):
        base = load_bundle(base)
    if base.tensor.G != 47:
        raise ValueError("actual handoff audit requires the declared 47-channel source")
    if type(steps) is not int or not 3 <= steps <= 5:
        raise ValueError("actual handoff audit supports three/four updates plus an explicit exploratory fifth")
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("appended audit output must be new or empty")
    out.mkdir(parents=True, exist_ok=True)
    quiet = append_native_pointer(base, writer_name="projective.apparatus_q")
    active = append_native_pointer(base, writer_name="projective.apparatus_q",
                                   feedback_target="projective.apparatus_p")
    memory_a = [[0] * base.seed.N]
    memory_a[0][0] = -1
    history = append_native_pointer(base, writer_name="projective.apparatus_q",
                                    feedback_target="projective.apparatus_p", memory_a=memory_a)
    assert quiet.tensor.G == active.tensor.G == history.tensor.G == 48
    assert active.tensor.fingerprint == history.tensor.fingerprint
    assert np.array_equal(active.seed.b, history.seed.b)
    assert np.array_equal(active.seed.r, history.seed.r)
    bundles = {"source_preserving_record": quiet, "raw_record_feedback": active,
               "matched_old_memory": history}
    engines = {name: Engine(bundle.tensor) for name, bundle in bundles.items()}
    states = {name: bundle.seed for name, bundle in bundles.items()}
    physical = base.seed
    physical_engine = Engine(base.tensor)
    writer = active.tensor.gear_index("projective.apparatus_q")
    target = active.tensor.gear_index("projective.apparatus_p")
    carrier = [base.tensor.gear_index("projective." + name)
               for name in ("phi", "chi", "Pi_phi", "Pi_chi")]
    rows = []
    for tick in range(1, steps + 1):
        before = states
        states = {name: engines[name].step(state) for name, state in before.items()}
        physical = physical_engine.step(physical)
        for name, state in states.items():
            assert state.same_as(scalar_step(bundles[name].tensor, before[name]))
            assert engines[name].inverse_step(state).same_as(before[name])
            assert np.array_equal(velocity(state, 47), velocity(before[name], 47) + before[name].b[writer])
        quiet_state, active_state, history_state = (states[name] for name in bundles)
        assert all(np.array_equal(getattr(quiet_state, field)[:47], getattr(physical, field))
                   for field in ("a", "b", "r"))
        rows.append({"tick": tick,
                     "source_preserving_projection_equal": True,
                     "new_record_feedback_target_differs": not np.array_equal(quiet_state.b[target], active_state.b[target]),
                     "new_record_feedback_carrier_differs": any(not np.array_equal(getattr(quiet_state, f)[carrier],
                                                                                  getattr(active_state, f)[carrier]) for f in ("a", "b", "r")),
                     "matched_old_memory_target_differs": not np.array_equal(active_state.b[target], history_state.b[target]),
                     "matched_old_memory_carrier_differs": any(not np.array_equal(getattr(active_state, f)[carrier],
                                                                                  getattr(history_state, f)[carrier]) for f in ("a", "b", "r")),
                     "record_nonzero_nodes": int(np.count_nonzero(velocity(active_state, 47))),
                     "record_velocity_changes": not np.array_equal(velocity(active_state, 47), velocity(before["raw_record_feedback"], 47))})
    assert any(row["new_record_feedback_target_differs"] for row in rows)
    assert rows[0]["matched_old_memory_target_differs"]
    for name, state in states.items():
        assert engines[name].rewind(state, steps).same_as(bundles[name].seed)
    runs = {name: run_bundle(bundle, out / name, steps=steps) for name, bundle in bundles.items()}
    report = {"schema": "universe24/selection-pointer-appended/1", "channels": 48,
              "base_bundle_id": base.bundle_id, "base_tensor_hash": base.tensor.fingerprint,
              "writer": "projective.apparatus_q", "feedback_target": "projective.apparatus_p",
              "steps": steps, "complete_scalar_oracle_and_rewind": True,
              "horizon_status": "four-update protocol; fifth update, if present, is an exploratory check of the observed p-to-q-to-carrier delay",
              "source_preserving_projection": True, "matched_history_changes_target": True,
              "acquired_record_changes_future_target": True, "rows": rows,
              "source_sha256": {"validation/selection/pointer.py": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
              "runs": {name: {k: r[k] for k in ("run_id", "bundle_id", "tensor_hash", "maximum_integer_bits_by_step")}
                       for name, r in runs.items()},
              "physical_scope": "Source-preserving variant leaves the supplied47 equations intact. Raw-feedback variant is an explicit test perturbation without record stress or a proved continuum coupling; no conservation or physical detector promotion.",
              "finite_record_persistence": "not established on this continuously driven q preparation",
              "exclusive_choice": "not implemented", "Born_rule": "not derived"}
    (out / "appended.json").write_text(exact_json.dumps(report, sort_keys=True) + "\n")
    return report


def audit(out):
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("pointer output must be new or empty")
    out.mkdir(parents=True, exist_ok=True)
    cases = []
    for direction in range(6):
        for carry in range(6):
            bundle = native_control(direction=direction, carry=carry)
            result = inspect_control(bundle)
            rows = result["local_ticks"]
            assert rows[0]["record_velocity"] == rows[1]["record_velocity"] == [0, 0]
            assert rows[1]["pulse"] == [1, 0]
            assert all(row["record_velocity"] == [1, 0] for row in rows[2:])
            assert rows[2]["response"] == [0, 0] and rows[3]["response"] == [1, 0]
            cases.append({"direction": direction, "carry": carry, **result})
    controls = {}
    for name, kwargs in (("no_source", {"amplitude": 0}), ("double_source", {"second_amplitude": 1}),
                         ("disconnected", {"feedback": 0}), ("matched_history", {"history": 2}),
                         ("signed_amplitude", {"amplitude": -2})):
        controls[name] = inspect_control(native_control(**kwargs))
    assert all(row["record_velocity"] == [0, 0] and row["response"] == [0, 0]
               for row in controls["no_source"]["local_ticks"])
    assert controls["double_source"]["local_ticks"][2]["outcomes"] == ["left", "right"]
    assert all(row["response"] == [0, 0] for row in controls["disconnected"]["local_ticks"])
    assert controls["matched_history"]["local_ticks"][1]["response"] == [2, 0]
    recurrence = inspect_control(native_control(), steps=9)
    assert recurrence["local_ticks"][9]["record_velocity"] == [2, 0]
    representative = native_control()
    runtime = run_bundle(representative, out / "native-run", steps=8)
    report = {"schema": "universe24/selection-pointer-audit/1",
              "source_sha256": {"validation/selection/pointer.py": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
              "source_commit_base": "main4c494c1+PR49a3013a9", "scope": "native three-channel finite-window mechanical control",
              "cases": cases, "controls": controls, "recurrence": recurrence,
              "run_id": runtime["run_id"], "bundle_id": runtime["bundle_id"],
              "protocol": {"ready_tick": 0, "arrival_tick": 1, "record_tick": 2, "feedback_tick": 3,
                           "persistence_ticks": list(range(2, 9)), "all_trials_kept": True},
              "passed": ["causal_arrival", "retained_velocity_persistence", "later_local_feedback", "no_source",
                         "matched_history_changes_board", "disconnected_feedback", "six_directions_all_carries",
                         "independent_oracle", "complete_rewind", "generic_runtime_replay"],
              "failed": {"exclusive_choice": "both prepared pulses produce both retained records",
                         "indefinite_unchanged_record": "periodic pulse returns and increments record at tick9"},
              "not_tested": ["shared_metric", "physical_record_stress", "energy_balance", "Born_rule", "Bell", "structural_growth"]}
    (out / "pointer.json").write_text(exact_json.dumps(report, sort_keys=True) + "\n")
    (out / "instrument_trials.json").write_text(exact_json.dumps({
        "allowed_outcomes": ["left", "right"], "decision_index": 2, "persistence_ticks": 7,
        "trials": [{"id": name, "outcomes": [row["outcomes"] for row in result["local_ticks"]]}
                   for name, result in [("single_source", cases[0])] + list(controls.items())]}, sort_keys=True) + "\n")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/selection/pointer"))
    args = parser.parse_args(argv)
    report = audit(args.out)
    print(exact_json.dumps({"cases": len(report["cases"]), "passed": report["passed"], "failed": report["failed"]}))


if __name__ == "__main__":
    main()
