"""Bounded whole-state motion audit and passive native-address observers.

Spatial translation of a complete initial state is used only in explicitly
registered covariance checks. No translated frame sequence is exported as an
engine-generated trajectory, and no observer changes an evolving state.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import time

from universe24 import Coupling, Engine, State
from research.experiments.run import recorded_states
from research.presenter.export import state_sha256

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "motion_protocol.json"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def write_json(path, value):
    Path(path).write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def vector(value):
    value = tuple(value)
    if len(value) != 3 or any(type(v) is not int for v in value):
        raise ValueError("Expected three integer coordinates")
    return value


def translate_state(state, displacement):
    """Return T_q(S), retaining every channel and the periodic background."""
    q = vector(displacement)
    side = state.cube.side
    cells = {tuple((a[j] + q[j]) % side for j in range(3)) + (a[3],): v
             for a, v in state.cells.items()}
    return State(state.cube, state.background, cells)


def first_difference(left, right):
    if left.cube != right.cube or left.background != right.background:
        return {"metadata_differ": True}
    for address in sorted(left.cells.keys() | right.cells.keys()):
        if left.at(address) != right.at(address):
            return {"address": list(address),
                    "actual": [str(v) for v in left.at(address)],
                    "expected": [str(v) for v in right.at(address)]}
    return None


def relative_periodicity(states, period, displacement, *, translated=None):
    """Compare complete native states, excluding aliases and static symmetry.

Every available start time is reported. Acceptance is a whole-recording check,
not a cropped-region or retrospectively chosen subwindow check.
"""
    if type(period) is not int or period < 1 or period >= len(states):
        raise ValueError("Period must have at least one complete comparison")
    q = vector(displacement)
    side = states[0].cube.side
    alias = all(v % side == 0 for v in q)
    if translated is None:
        translated = [translate_state(state, q) for state in states]
    if len(translated) != len(states):
        raise ValueError("Translated comparison cache has the wrong length")
    invariant = translated[0] == states[0]
    matching = []
    first_mismatch = None
    for t in range(len(states) - period):
        if states[t + period] == translated[t]:
            matching.append(t)
        elif first_mismatch is None:
            first_mismatch = {"start_step": t, "end_step": t + period,
                              **first_difference(states[t + period], translated[t])}
    raw_equal = len(matching) == len(states) - period
    return {"period": period, "displacement": list(q),
            "comparison_count": len(states) - period, "matching_start_steps": matching,
            "all_complete_comparisons_equal": raw_equal,
            "shift_aliases_identity": alias, "initial_translation_invariant": invariant,
            "nontrivial_relative_periodicity": raw_equal and not alias and not invariant,
            "first_mismatch": first_mismatch}


def sample_moving_observer(states, origin, displacement, period=1):
    """Read native x0+n*q at native t=n*p; never reindex or evolve states.

The returned object deliberately has no experiment/frames schema. It contains
exact full-node samples, not a new purported Rule3 trajectory in another frame.
"""
    origin, q = vector(origin), vector(displacement)
    if type(period) is not int or period < 1:
        raise ValueError("Observer period must be a positive integer")
    if not states:
        raise ValueError("Observer requires complete native states")
    side = states[0].cube.side
    if any(not 0 <= v < side for v in origin):
        raise ValueError("Observer origin is outside the native cube")
    rows = []
    for n, t in enumerate(range(0, len(states), period)):
        state = states[t]
        if state.cube != states[0].cube:
            raise ValueError("Observer cannot switch board geometry")
        position = tuple((origin[j] + n * q[j]) % side for j in range(3))
        rows.append({"native_step": t, "native_position": list(position),
                     "native_state_sha256": state_sha256(state),
                     "full_48_channel_node": [[str(v) for v in triple] for triple in state.node(position)]})
    return {"format": "universe24-passive-native-address-observer-v1",
            "origin": list(origin), "displacement_per_sample": list(q),
            "native_steps_per_sample": period, "mutates_or_evolves_state": False,
            "is_native_engine_trajectory": False, "samples": rows}


def source_hashes():
    paths = [Path(__file__), PROTOCOL, ROOT / "research/experiments/run.py",
             ROOT / "research/presenter/export.py"]
    paths.extend((ROOT / "universe24").rglob("*.py"))
    return {str(p.relative_to(ROOT)): file_hash(p) for p in sorted(set(paths))}


def expectation_checks(source, analyses, ordinary):
    found = [row for row in analyses if row["nontrivial_relative_periodicity"]]
    expected = source["expected_motion"]
    if expected == "carrier_plus_x":
        motion = any(row["period"] == 1 and row["displacement"] == [1, 0, 0] for row in found)
    elif expected in ("none_in_registered_domain", "trivial_symmetry_only"):
        motion = not found
    else:
        raise ValueError("Unknown prospective motion expectation")
    checks = {"motion_expectation": motion}
    if source.get("expected_ordinary_period"):
        p = source["expected_ordinary_period"]
        checks["ordinary_period_expectation"] = next(row["all_complete_comparisons_equal"]
                                                     for row in ordinary if row["period"] == p)
    if expected == "trivial_symmetry_only":
        checks["raw_equalities_rejected_as_static_symmetry"] = all(
            row["all_complete_comparisons_equal"] and row["initial_translation_invariant"]
            and not row["nontrivial_relative_periodicity"] for row in analyses)
    return checks


def validate_protocol(p):
    if p["periods"] != [1, 2, 3, 4]:
        raise ValueError("This study registers periods one through four")
    shifts = [vector(v) for v in p["relative_shifts"]]
    if len(set(shifts)) != 6 or any(sum(abs(v) for v in q) != 1 for q in shifts):
        raise ValueError("Six distinct nonzero unit-axis shifts are required")
    if len(p["sources"]) != 13 or len({s["id"] for s in p["sources"]}) != 13:
        raise ValueError("Exactly thirteen distinct recordings are registered")
    for source in p["sources"]:
        path = (ROOT / source["path"]).resolve()
        if ROOT not in path.parents or file_hash(path) != source["sha256"]:
            raise ValueError("Pinned native recording mismatch: " + source["id"])
    if 2 * len(p["static_translations"]) * len(p["sources"]) != p["budget"]["new_one_step_checks"]:
        raise ValueError("Static translation check count is not the registered budget")


def run(output):
    output = Path(output)
    raw = PROTOCOL.read_bytes()
    p = json.loads(raw)
    validate_protocol(p)
    output.mkdir(parents=True, exist_ok=False)
    (output / "protocol.json").write_bytes(raw)
    hashes = source_hashes()
    registration = {"format": "universe24-staged-motion-registration-v1",
                    "protocol_sha256": hashlib.sha256(raw).hexdigest(), "source_sha256": hashes,
                    "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                    "registered_before_analysis": True, "new_native_experiment_records": 0,
                    "pinned_recordings": len(p["sources"]), "seed": None}
    write_json(output / "registration.json", registration)
    start, cpu = time.monotonic(), time.process_time()
    analyses, observer_records = [], []
    reason = None
    for source in p["sources"]:
        if time.process_time() - cpu >= p["budget"]["max_cpu_seconds"] - 5:
            reason = "cpu_budget_before_next_recording"
            break
        if time.monotonic() - start >= p["budget"]["max_wall_seconds"] - 5:
            reason = "wall_budget_before_next_recording"
            break
        record = json.loads(gzip.decompress((ROOT / source["path"]).read_bytes()))
        experiment = record["experiment"]
        states = recorded_states(experiment)
        if experiment["id"] != source["id"] or experiment["side"] != source["side"] or len(states) != source["frames"]:
            raise ValueError("Frozen recording metadata mismatch")
        original_hashes = [state_sha256(state) for state in states]
        if original_hashes != [frame["state_sha256"] for frame in experiment["frames"]]:
            raise ValueError("Native complete-state hash mismatch")
        engine = Engine(Coupling(tuple(experiment["coupling"]["body_signs"])))
        tensor = experiment["coupling"]
        if (engine.coupling.fingerprint != tensor["fingerprint"]
                or [list(row) for row in engine.coupling.ports] != tensor["ports"]
                or [list(row) for row in engine.coupling.weights] != tensor["weights"]):
            raise ValueError("Frozen native tensor differs from its exact body-sign specification")
        relative = []
        for q in p["relative_shifts"]:
            translated = [translate_state(state, q) for state in states]
            relative.extend(relative_periodicity(states, period, q, translated=translated) for period in p["periods"])
        ordinary = [relative_periodicity(states, period, (0, 0, 0), translated=states) for period in p["periods"]]
        covariance = []
        for t in (0, len(states) - 2):
            for q in p["static_translations"]:
                old = translate_state(states[t], q)
                expected = translate_state(states[t + 1], q)
                actual = engine.advance(old)
                inverse = engine.rewind(actual)
                covariance.append({"native_start_step": t, "displacement": q,
                                   "translated_initial_sha256": state_sha256(old),
                                   "translated_expected_sha256": state_sha256(expected),
                                   "engine_forward_sha256": state_sha256(actual),
                                   "forward_equal": actual == expected, "full_inverse_equal": inverse == old,
                                   "first_mismatch": first_difference(actual, expected)})
        samples = [sample_moving_observer(states, source["observer_origin"], q)
                   for q in p["observer_displacements"]]
        observer_records.append({"recording_id": source["id"], "native_record_sha256": source["sha256"], "observers": samples})
        unchanged = original_hashes == [state_sha256(state) for state in states]
        checks = {**expectation_checks(source, relative, ordinary),
                  "all_static_covariance_checks": all(c["forward_equal"] and c["full_inverse_equal"] for c in covariance),
                  "native_states_unchanged": unchanged}
        analyses.append({"id": source["id"], "source_path": source["path"], "source_sha256": source["sha256"],
                         "object_scope": source["object_scope"], "side": experiment["side"], "complete_frames": len(states),
                         "body_signs": experiment["coupling"]["body_signs"], "relative_periodicity": relative,
                         "ordinary_periodicity": ordinary, "static_translation_checks": covariance,
                         "nontrivial_matches": [{"period": a["period"], "displacement": a["displacement"]}
                                                for a in relative if a["nontrivial_relative_periodicity"]],
                         "checks": checks, "expectations_passed": all(checks.values())})
        print(source["id"] + ": " + canonical(analyses[-1]["nontrivial_matches"]), flush=True)
    inputs_unchanged = all(file_hash(ROOT / s["path"]) == s["sha256"] for s in p["sources"])
    sources_unchanged = source_hashes() == hashes and PROTOCOL.read_bytes() == raw
    if not inputs_unchanged or not sources_unchanged:
        raise RuntimeError("Frozen source or native recording changed during analysis")
    observer_path = output / "observer_samples.json.gz"
    observer_path.write_bytes(gzip.compress(canonical({"format": "universe24-passive-observer-collection-v1",
                                                      "native_trajectories_rewritten": False,
                                                      "records": observer_records}).encode(), mtime=0))
    elapsed_cpu, elapsed_wall = time.process_time() - cpu, time.monotonic() - start
    complete = len(analyses) == len(p["sources"]) and reason is None
    budget_ok = elapsed_cpu <= p["budget"]["max_cpu_seconds"] and elapsed_wall <= p["budget"]["max_wall_seconds"]
    result = {"format": "universe24-staged-motion-result-v1", "protocol_sha256": registration["protocol_sha256"],
              "status": "completed" if complete and budget_ok else "budget_stopped", "stop_reason": reason,
              "registered_recordings": len(p["sources"]), "completed_recordings": len(analyses),
              "new_native_experiment_records": 0, "native_trajectories_rewritten": False,
              "new_one_step_checks": sum(len(a["static_translation_checks"]) for a in analyses),
              "all_static_covariance_checks": all(a["checks"]["all_static_covariance_checks"] for a in analyses),
              "whole_apparatus_motion_established": any(a["nontrivial_matches"] for a in analyses
                                                        if next(s for s in p["sources"] if s["id"] == a["id"])["object_scope"] == "complete_apparatus"),
              "source_records_unchanged": inputs_unchanged, "sources_unchanged": sources_unchanged,
              "accepted": complete and budget_ok and all(a["expectations_passed"] for a in analyses),
              "analyses": analyses, "observer_samples": {"path": observer_path.name, "sha256": file_hash(observer_path)},
              "cpu_seconds": elapsed_cpu, "wall_seconds": elapsed_wall,
              "scope": p["scope"], "moving_detector_or_clock_established": False}
    write_json(output / "result.json", result)
    if sum(path.stat().st_size for path in output.rglob("*") if path.is_file()) > p["budget"]["max_recorded_bytes"]:
        raise RuntimeError("Motion analysis exceeded its registered output budget")
    print(canonical({key: result[key] for key in ("status", "completed_recordings", "new_one_step_checks", "accepted", "cpu_seconds")}), flush=True)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    return run(parser.parse_args(argv).output)


if __name__ == "__main__":
    main()
