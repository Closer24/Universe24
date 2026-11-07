"""Fresh phase-conditioned competition checks through the generic runner.

The 432-run selection prediction remains refuted. This separate protocol
tests an explicitly narrower component and fixed input-response comparisons.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import time

from research.experiments.run import assemble, recorded_states, run_experiment, source_hashes
from research.component_studies.selection_search import PAIRS, SIDES, canonical, digest, save
from universe24.experiments.config import checkpoint_data
from universe24.observation.clicks import classify


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def case_id(length, kind, phase_index=None, left=None, right=None, side=None, pattern=None):
    if kind == "no_source":
        return f"l{length}-null-{left}-{right}"
    if kind == "isolated":
        return f"l{length}-iso-p{phase_index}-{'L' if side == -1 else 'R'}-{pattern}"
    return f"l{length}-joint-p{phase_index}-{left}-{right}"


def make_case(geometry, kind, *, phase=(0, 1), phase_index=0,
              patterns=("OR", "NO"), isolated_side=None):
    case = {**geometry, "kind": kind, "phase": list(phase), "phase_index": phase_index,
            "patterns": list(patterns), "source_present": kind != "no_source"}
    if isolated_side is not None:
        case["isolated_side"] = isolated_side
        case["pattern"] = patterns[0 if isolated_side == -1 else 1]
    case["id"] = case_id(geometry["arm_length"], kind, phase_index=phase_index,
        left=patterns[0], right=patterns[1], side=isolated_side, pattern=case.get("pattern"))
    return case


def build_spec(case, protocol_sha256):
    length = case["arm_length"]
    origin = [case["side"] // 2] * 3
    components = [{"name": "source", "recipe": "SignalSource", "at": origin,
                   "params": {"a": case["phase"][0], "b": case["phase"][1],
                              "present": case["source_present"]}}]
    readouts = []
    for side, label in SIDES:
        if "isolated_side" in case and side != case["isolated_side"]:
            continue
        pattern = case["patterns"][0 if side == -1 else 1]
        components.append({"name": label, "recipe": "PairedArm", "at": origin,
            "params": {"direction": side, "length": length,
                       "gate_pairs": [list(PAIRS[letter]) for letter in pattern]}})
        clauses = []
        for g in range(48):
            r = 4 if g == 0 else 0 if g == 14 else 2
            clauses.extend({"port": label + ".outlet", "index": g,
                            "component": component, "equals": str(value)}
                           for component, value in (("a", 0), ("b", 0), ("r", r)))
        readouts.append({"id": label + "-outlet-null", "label": label + " outlet equals initial state",
                         "kind": "all_equal", "clauses": clauses})
    return {"format": "universe24-assembly-experiment-v1", "id": case["id"],
            "title": f"Competition {case['patterns'][0]}/{case['patterns'][1]}: length {length}, input {case['phase']}, {case['kind']}",
            "description": "A recorded closed-board initial preparation. The fixed protocol, not this display, determines acceptance. No physical-light or higher-complexity preference claim.",
            "board": {"side": case["side"], "background": [0, 0, 2], "body_signs": [1, 1, 1]},
            "components": components, "steps": case["steps"], "readouts": readouts,
            "detectors": [], "view": {"port": "source.signal", "index": 0},
            "budget": {"max_frames": 57, "max_cells": 200000, "max_bytes": 16777216, "max_seconds": 30},
            "provenance": {"protocol_sha256": protocol_sha256, "original_all_phase_holdout_gate": "closed",
                           "claim": "Separate prospective phase-conditioned competition test"}}


def make_manifest(protocol, protocol_hash):
    cases = []
    for geometry in protocol["preparation"]["geometries"]:
        pairs = protocol["preparation"]["all_joint_pairs"]
        for left, right in pairs:
            cases.append(make_case(geometry, "no_source", patterns=(left, right)))
        for p, phase in enumerate(protocol["preparation"]["ordered_inputs"]):
            for side, _ in SIDES:
                for pattern in protocol["preparation"]["patterns"]:
                    cases.append(make_case(geometry, "isolated", phase=phase, phase_index=p,
                                          patterns=(pattern, pattern), isolated_side=side))
            for pair in pairs:
                cases.append(make_case(geometry, "joint", phase=phase, phase_index=p, patterns=pair))
    if len(cases) != protocol["preparation"]["registered_trajectories"]:
        raise AssertionError("Follow-up manifest size differs from protocol")
    return [{"case": case, "spec": build_spec(case, protocol_hash)} for case in cases]


def observe(case, states):
    origin = (case["side"] // 2,) * 3
    reports = {}
    for side, _ in SIDES:
        position = (origin[0] + side * case["arm_length"], origin[1], origin[2])
        baseline = [states[0].at((*position, g)) for g in range(48)]
        report = {"arrival_tuple": [None, None, None], "b_transmission": False,
                  "strong_quiet": True, "C_events": [], "C_bank_times": [],
                  "remainder_change_times": [], "position": list(position)}
        for t, state in enumerate(states):
            values = [state.at((*position, g)) for g in range(48)]
            changed = values != baseline
            b_changed = any(value.b != old.b for value, old in zip(values, baseline))
            if t and changed and report["arrival_tuple"][0] is None:
                report["arrival_tuple"][0] = t
            if t and b_changed and report["arrival_tuple"][1] is None:
                report["arrival_tuple"][1] = t
            if case["window"][0] <= t <= case["window"][1]:
                report["b_transmission"] |= b_changed
                report["strong_quiet"] &= not changed
            if t:
                previous = [states[t - 1].at((*position, g)) for g in range(48)]
                if any(a.r != b.r for a, b in zip(previous, values)):
                    report["remainder_change_times"].append(t)
                events = []
                for g, (old, new) in enumerate(zip(previous, values)):
                    event = classify(old, new)
                    if event is not None:
                        kind, quotient = event
                        events.append({"step": t, "address": [*position, g], "kind": kind,
                                       "quotient": quotient, "before": list(old), "after": list(new)})
                if events:
                    report["C_events"].extend(events)
                    report["C_bank_times"].append(t)
                    if report["arrival_tuple"][2] is None:
                        report["arrival_tuple"][2] = t
        report["C_in_window"] = any(case["window"][0] <= t <= case["window"][1] for t in report["C_bank_times"])
        report["functional"] = report["b_transmission"] and report["C_in_window"]
        reports[str(side)] = report
    return reports


def assess(protocol, records):
    rows, primary, flips_by_length = [], [], {}
    inputs = protocol["preparation"]["ordered_inputs"]
    for geometry in protocol["preparation"]["geometries"]:
        length = geometry["arm_length"]
        consistent = {}
        for p, phase in enumerate(inputs):
            pair_rows = []
            for left, right in protocol["preparation"]["all_joint_pairs"]:
                identifier = case_id(length, "joint", phase_index=p, left=left, right=right)
                required = [identifier] + [case_id(length, "isolated", phase_index=p, side=s, pattern=pattern)
                                           for s, pattern in ((-1, left), (1, right))]
                if not all(key in records for key in required):
                    continue
                isolated = [records[required[1]]["outlets"]["-1"], records[required[2]]["outlets"]["1"]]
                out = records[identifier]["outlets"]
                sole = [s for s, _ in SIDES if out[str(s)]["functional"] and out[str(-s)]["strong_quiet"]]
                functional = all(item["functional"] for item in isolated)
                winner = (left if sole[0] == -1 else right) if len(sole) == 1 else None
                row = {"id": identifier, "arm_length": length, "phase_index": p, "input": phase,
                       "patterns": [left, right], "both_isolated_functional": functional,
                       "isolated_arrival_tuples": [r["arrival_tuple"] for r in isolated],
                       "matched_arrivals": isolated[0]["arrival_tuple"] == isolated[1]["arrival_tuple"],
                       "unique_side": sole[0] if len(sole) == 1 else None,
                       "winning_pattern": winner, "competitive": functional and len(sole) == 1}
                rows.append(row)
                if left != right:
                    pair_rows.append(row)
            if len(pair_rows) == 2 and all(row["competitive"] for row in pair_rows) and len({row["winning_pattern"] for row in pair_rows}) == 1:
                consistent[p] = pair_rows[0]["winning_pattern"]
        null_ids = [case_id(length, "no_source", left=l, right=r)
                    for l, r in protocol["preparation"]["all_joint_pairs"]]
        complete_null = all(key in records for key in null_ids)
        null_pass = complete_null and all(records[key]["entire_board_stationary"] for key in null_ids)
        primary.append({"arm_length": length, "source_input": [0, 1],
                        "both_swaps_functional_and_OR_only": consistent.get(0) == "OR",
                        "null_stationary": null_pass,
                        "passed": consistent.get(0) == "OR" and null_pass})
        flips = []
        for i, j in itertools.combinations(sorted(consistent), 2):
            if consistent[i] == consistent[j]:
                continue
            norms = [sum(value * value for value in inputs[p]) for p in (i, j)]
            flips.append({"input_indices": [i, j], "inputs": [inputs[i], inputs[j]],
                          "winning_patterns": [consistent[i], consistent[j]], "counter_norms": norms,
                          "same_amplitude_phase_controlled": norms[0] == norms[1]})
        flips_by_length[str(length)] = {"consistent_competitive_inputs": {str(k): v for k, v in consistent.items()},
                                         "flips": flips}
    common = None
    for data in flips_by_length.values():
        keys = {(tuple(row["input_indices"]), tuple(row["winning_patterns"]), row["same_amplitude_phase_controlled"])
                for row in data["flips"]}
        common = keys if common is None else common & keys
    common_rows = [{"input_indices": list(indices), "winning_patterns": list(winners),
                    "same_amplitude_phase_controlled": phase_only}
                   for indices, winners, phase_only in sorted(common or ())]
    return {"primary_fresh_geometry_checks": primary, "comparisons": rows,
            "input_response": flips_by_length, "cross_geometry_flips": common_rows,
            "primary_passed": len(primary) == 2 and all(row["passed"] for row in primary),
            "phase_controlled_flip_passed": any(row["same_amplitude_phase_controlled"] for row in common_rows),
            "input_controlled_flip_passed": bool(common_rows)}


def main(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    path = HERE / "selection_followup_protocol.json"
    raw = path.read_bytes()
    protocol, protocol_hash = json.loads(raw), hashlib.sha256(raw).hexdigest()
    manifest = make_manifest(protocol, protocol_hash)
    (output / "protocol.json").write_bytes(raw)
    save(output / "candidate_manifest.json", manifest)
    hashes = source_hashes()
    hashes.update({str(p.relative_to(ROOT)): digest(p) for p in (Path(__file__), path, HERE / "selection_search.py")})
    for relative in hashes:
        target = output / "source" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    save(output / "source_manifest.json", hashes)
    records, failure = {}, None
    start_cpu, start_wall = time.process_time(), time.monotonic()
    for item in manifest:
        case, spec = item["case"], item["spec"]
        try:
            if time.process_time() - start_cpu > protocol["budget"]["additional_cpu_seconds"]:
                raise TimeoutError("Frozen follow-up CPU budget exhausted")
            if time.monotonic() - start_wall > protocol["budget"]["wall_seconds"]:
                raise TimeoutError("Frozen follow-up wall budget exhausted")
            if any(digest(ROOT / relative) != expected for relative, expected in hashes.items()):
                raise RuntimeError("A frozen source changed before the next follow-up case")
            folder = output / "cases" / case["id"]
            result = run_experiment(spec, folder)
            states = recorded_states(result["experiment"])
            prepared = assemble(spec)
            if max(len(state.cells) for state in states) > protocol["budget"]["maximum_stored_channels"]:
                raise MemoryError("Follow-up retained-state channel cap exceeded")
            margin = min(min(v, case["side"] - 1 - v) for address in states[0].cells for v in address[:3])
            if margin <= case["steps"]:
                raise AssertionError("Follow-up preparation could wrap within its horizon")
            with gzip.open(folder / "states.jsonl.gz", "xt", encoding="utf-8", compresslevel=6) as handle:
                for t, state in enumerate(states):
                    handle.write(canonical(checkpoint_data(state, prepared.engine, t)) + "\n")
            analysis = {"case": case, "outlets": observe(case, states),
                        "entire_board_stationary": all(state == states[0] for state in states),
                        "full_rewind": result["experiment"]["provenance"]["full_rewind_equal"],
                        "initial_boundary_margin": margin, "max_stored_channels": max(len(s.cells) for s in states),
                        "trace_sha256": digest(folder / "states.jsonl.gz"),
                        "portable_bundle_sha256": digest(folder / "experiments.json"),
                        "spec_sha256": result["spec_sha256"]}
            save(folder / "analysis.json", analysis)
            records[case["id"]] = analysis
            if len(records) % 20 == 0:
                print(canonical({"completed": len(records), "registered": len(manifest),
                                 "cpu_seconds": round(time.process_time() - start_cpu, 3)}), flush=True)
        except Exception as exc:
            failure = {"case": case["id"], "type": type(exc).__name__, "message": str(exc)}
            break
    verdict = assess(protocol, records)
    summary = {"execution_status": "completed" if failure is None else "inconclusive", "failure": failure,
               "runs_completed": len(records), "runs_registered": len(manifest),
               "cpu_seconds": time.process_time() - start_cpu, "wall_seconds": time.monotonic() - start_wall,
               "cumulative_cpu_seconds": protocol["budget"]["prior_cpu_seconds"] + time.process_time() - start_cpu,
               "all_full_rewinds": all(r["full_rewind"] for r in records.values()),
               "forward_steps": sum(r["case"]["steps"] for r in records.values()),
               "primary_passed": verdict["primary_passed"] if failure is None else None,
               "phase_controlled_flip_passed": verdict["phase_controlled_flip_passed"] if failure is None else None,
               "input_controlled_flip_passed": verdict["input_controlled_flip_passed"] if failure is None else None,
               "original_prediction_status": "finite_prediction_refuted", "original_holdout_gate": "closed",
               "higher_cooperation_selection_claim": False, "joined_waiting_receiver_claim": False}
    save(output / "result.json", {"summary": summary, "verdict": verdict,
          "protocol_sha256": protocol_hash,
          "cases": {key: {"analysis": f"cases/{key}/analysis.json", "trace": f"cases/{key}/states.jsonl.gz",
                           "portable_bundle": f"cases/{key}/experiments.json", "trace_sha256": record["trace_sha256"]}
                    for key, record in records.items()}})
    print(canonical(summary), flush=True)
    return 0 if failure is None else 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    raise SystemExit(main(parser.parse_args().output))
