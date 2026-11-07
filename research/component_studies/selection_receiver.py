"""Final bounded route-to-prepared-receiver trial; no further search follows."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import time

from research.experiments.run import assemble, recorded_states, run_experiment, source_hashes
from research.component_studies.selection_search import PAIRS, SIDES, canonical, digest, save
from universe24.experiments.config import checkpoint_data


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def spec_for(case, protocol_hash):
    origin = [64, 64, 64]
    components = [{"name": "source", "recipe": "SignalSource", "at": origin,
                   "params": {"a": 0, "b": 1, "present": case["source_present"]}}]
    detectors = []
    for side, label in SIDES:
        if "isolated_side" in case and case["isolated_side"] != side:
            continue
        pattern = case["patterns"][0 if side == -1 else 1]
        components.append({"name": label, "recipe": "PairedArm", "at": origin,
                           "params": {"direction": side, "length": 7,
                                      "gate_pairs": [list(PAIRS[letter]) for letter in pattern]}})
        name = label + "_receiver"
        components.append({"name": name, "recipe": "Receiver", "at": [64 + 8 * side, 64, 64],
                           "params": {"remainders": [4, 2]}})
        detectors.append(name + ".node")
    return {"format": "universe24-assembly-experiment-v1", "id": case["id"],
            "title": f"Route to prepared receiver: {case['patterns'][0]}/{case['patterns'][1]}, {case['kind']}, source {'on' if case['source_present'] else 'off'}",
            "description": "The waiting remainder pair is prepared at time zero. A single central source drives the actual route. This trial requires one genuine receiver click and a retained record; no autonomous waiting-state writing or uniqueness approval is assumed.",
            "board": {"side": 129, "background": [0, 0, 2], "body_signs": [1, 1, 1]},
            "components": components, "steps": 48, "detectors": detectors,
            "view": {"port": detectors[0], "index": 0},
            "budget": {"max_frames": 49, "max_cells": 200000, "max_bytes": 16777216, "max_seconds": 30},
            "provenance": {"protocol_sha256": protocol_hash,
                           "waiting_state": "Initially prepared, not written by an earlier signal",
                           "unique_path_approval": "Not computed or claimed"}}


def manifest(protocol_hash):
    cases = []
    for pair in (("OR", "NO"), ("NO", "OR"), ("OR", "OR"), ("NO", "NO")):
        for present in (True, False):
            cases.append({"id": f"receiver-joint-{pair[0]}-{pair[1]}-s{int(present)}",
                          "kind": "joint", "patterns": list(pair), "source_present": present})
    for side, label in SIDES:
        for pattern in ("OR", "NO"):
            for present in (True, False):
                cases.append({"id": f"receiver-iso-{label}-{pattern}-s{int(present)}",
                              "kind": "isolated", "patterns": [pattern, pattern],
                              "isolated_side": side, "source_present": present})
    return [{"case": case, "spec": spec_for(case, protocol_hash)} for case in cases]


def analyze(case, result, states):
    receivers = {}
    for side, label in SIDES:
        if "isolated_side" in case and case["isolated_side"] != side:
            continue
        name = label + "_receiver.node"
        report = result["observations"][name]
        events = report["arithmetic_events"]
        times = sorted({event["step"] for event in events})
        event_time = times[0] if times else None
        trace = report["trace"]
        memories = [[row["memory"][0], row["memory"][14]] for row in trace]
        one = len(times) == 1
        in_window = one and 12 <= times[0] <= 15
        record_at = event_time is not None and memories[event_time] == [0, 0]
        retained = event_time is not None and all(pair == [0, 0] for pair in memories[event_time:])
        driven = event_time is not None and any(int(value) != 0 for value in trace[event_time - 1]["next_input"])
        quiet = all(row["detector"] == trace[0]["detector"] for row in trace[1:])
        first_bad_record = (next((t for t in range(event_time, len(memories)) if memories[t] != [0, 0]), None)
                            if event_time is not None else None)
        first_leak = next((row["step"] for row in trace[1:] if row["detector"] != trace[0]["detector"]), None)
        receivers[str(side)] = {"port": name, "pattern": case["patterns"][0 if side == -1 else 1],
            "C_bank_times": times, "C_event_count": len(events),
            "exactly_one_C_bank": one, "event_in_declared_window": in_window,
            "record_zero_zero_at_first_event": record_at, "record_retained_through_48": retained,
            "nonzero_actual_input_at_first_event": driven,
            "first_event_old_input_pair": [trace[event_time - 1]["next_input"][i] for i in (0, 14)] if event_time else None,
            "first_event_old_six_inputs_pair": [trace[event_time - 1]["six_inputs"][i] for i in (0, 14)] if event_time else None,
            "first_record_failure_step": first_bad_record, "first_complete_node_change": first_leak,
            "complete_node_quiet_all_1_to_48": quiet,
            "waiting_record_series": memories,
            "single_click_retaining_success": one and in_window and record_at and retained and driven}
    stationary = all(state == states[0] for state in states)
    if not case["source_present"]:
        required, success = True, stationary
    elif case["kind"] == "isolated":
        required = True
        success = receivers[str(case["isolated_side"])]["single_click_retaining_success"]
    elif case["patterns"][0] != case["patterns"][1]:
        required = True
        winner = -1 if case["patterns"][0] == "OR" else 1
        success = receivers[str(winner)]["single_click_retaining_success"] and receivers[str(-winner)]["complete_node_quiet_all_1_to_48"]
    else:
        required, success = False, None
    return {"case": case, "receivers": receivers, "required_case": required,
            "required_case_passed": success, "entire_board_stationary": stationary,
            "full_rewind": result["experiment"]["provenance"]["full_rewind_equal"],
            "max_stored_channels": max(len(state.cells) for state in states)}


def main(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    protocol_path = HERE / "selection_receiver_protocol.json"
    raw = protocol_path.read_bytes()
    protocol, protocol_hash = json.loads(raw), hashlib.sha256(raw).hexdigest()
    items = manifest(protocol_hash)
    if len(items) != protocol["preparation"]["registered_trajectories"]:
        raise ValueError("Joined case count differs from the frozen protocol")
    (output / "protocol.json").write_bytes(raw)
    save(output / "candidate_manifest.json", items)
    hashes = source_hashes()
    hashes.update({str(p.relative_to(ROOT)): digest(p) for p in (Path(__file__), protocol_path, HERE / "selection_search.py")})
    for relative in hashes:
        target = output / "source" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    save(output / "source_manifest.json", hashes)
    started_cpu, started_wall = time.process_time(), time.monotonic()
    results, failure = {}, None
    for item in items:
        case, spec = item["case"], item["spec"]
        try:
            if time.process_time() - started_cpu > protocol["budget"]["additional_cpu_seconds"]:
                raise TimeoutError("Joined CPU budget exhausted")
            if time.monotonic() - started_wall > protocol["budget"]["wall_seconds"]:
                raise TimeoutError("Joined wall budget exhausted")
            if any(digest(ROOT / relative) != value for relative, value in hashes.items()):
                raise RuntimeError("A frozen source changed during the joined batch")
            folder = output / "cases" / case["id"]
            result = run_experiment(spec, folder)
            states = recorded_states(result["experiment"])
            prepared = assemble(spec)
            analysis = analyze(case, result, states)
            if analysis["max_stored_channels"] > protocol["budget"]["maximum_stored_channels"]:
                raise MemoryError("Joined stored-channel cap exceeded")
            margin = min(min(value, 128 - value) for address in states[0].cells for value in address[:3])
            if margin <= 48:
                raise AssertionError("Joined preparation is not within a nonwrapping cone")
            analysis["initial_boundary_margin"] = margin
            with gzip.open(folder / "states.jsonl.gz", "xt", encoding="utf-8", compresslevel=6) as handle:
                for step, state in enumerate(states):
                    handle.write(canonical(checkpoint_data(state, prepared.engine, step)) + "\n")
            analysis["trace_sha256"] = digest(folder / "states.jsonl.gz")
            analysis["portable_bundle_sha256"] = digest(folder / "experiments.json")
            save(folder / "analysis.json", analysis)
            results[case["id"]] = analysis
            print(canonical({"completed": len(results), "registered": len(items),
                             "cpu_seconds": round(time.process_time() - started_cpu, 3)}), flush=True)
        except Exception as exc:
            failure = {"case": case["id"], "type": type(exc).__name__, "message": str(exc)}
            break
    required = [row for row in results.values() if row["required_case"]]
    summary = {"execution_status": "completed" if failure is None else "inconclusive", "failure": failure,
        "runs_completed": len(results), "runs_registered": len(items),
        "required_cases": len(required), "required_passed": sum(row["required_case_passed"] for row in required),
        "joined_single_click_retaining_component_passed": (all(row["required_case_passed"] for row in required) if failure is None else None),
        "failed_required_ids": [row["case"]["id"] for row in required if not row["required_case_passed"]],
        "all_full_rewinds": all(row["full_rewind"] for row in results.values()),
        "forward_steps": 48 * len(results), "cpu_seconds": time.process_time() - started_cpu,
        "cumulative_cpu_seconds": protocol["budget"]["prior_cpu_seconds"] + time.process_time() - started_cpu,
        "cumulative_trajectories": protocol["budget"]["prior_trajectories"] + len(results),
        "autonomous_waiting_state_written": False, "internally_computed_unique_path_approval": False,
        "higher_complexity_preference": False, "no_further_search_in_this_iteration": True}
    save(output / "result.json", {"summary": summary, "analyses": results, "protocol_sha256": protocol_hash,
        "cases": {key: {"analysis": f"cases/{key}/analysis.json", "native_trace": f"cases/{key}/states.jsonl.gz",
                         "portable_bundle": f"cases/{key}/experiments.json"} for key in results}})
    print(canonical(summary), flush=True)
    return 0 if failure is None else 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    raise SystemExit(main(parser.parse_args().output))
