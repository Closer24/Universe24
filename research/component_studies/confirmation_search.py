"""Bounded, preregistered search for a closed-board waiting/confirmation record.

All evolution is the unchanged reference Engine.advance. The full trace is
retained, including remainders; observation never supplies a runtime decision.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import time

from universe24.experiments.config import from_dict
from universe24.observation.clicks import classify
from research.signal_clocks.run import run_case, write_json

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = Path(__file__).with_name("confirmation_protocol.json")


def cases(protocol):
    family = protocol["family"]
    for number, (mode, geometry, distances, first, second) in enumerate(itertools.product(
        family["guide_modes"], family["geometries"], family["distance_pairs"],
        family["source_phases"], family["source_phases"],
    )):
        d1, d2 = distances
        yield {
            "id": f"confirmation-{number:03d}", "side": family["side"],
            "extent": family["extent"], "steps": family["steps"],
            "body_signs": protocol["model"]["body_signs"], "geometry": geometry,
            "guide_mode": mode, "source_offsets": [-d1, d2 if geometry == "opposed" else -d2],
            "source_ab": [first, second], "target_remainders": family["target_remainders"],
            "arrival_windows": [[d1, d1 + 1], [d2, d2 + 3]],
        }


def receiver_events(path, receiver):
    """Inspect every channel at the receiver using complete recorded snapshots."""
    events = []
    old = None
    for line in Path(path).read_text().splitlines():
        checkpoint = json.loads(line)
        state = from_dict(checkpoint["experiment"]).initial
        node = state.node(receiver)
        if old is not None:
            for g, (before, after) in enumerate(zip(old, node)):
                event = classify(before, after)
                if event is not None:
                    kind, quotient = event
                    events.append({"step": checkpoint["completed_steps"],
                        "address": [*receiver, g], "kind": kind, "quotient": quotient,
                        "before": list(before), "after": list(after)})
        old = node
    return events


def evaluate(case, runs):
    """Criteria fixed in confirmation_protocol.json; no fitted observer."""
    checks = {}
    d1, d2 = map(abs, case["source_offsets"])
    for mask, run in runs.items():
        checks[f"{mask}:all_inverses"] = run["all_one_step_inverses"] and run["complete_rewind"]
        checks[f"{mask}:boundary"] = run["initial_boundary_margin"] > case["steps"]
        checks[f"{mask}:complete"] = len(run["trace"]) == case["steps"] + 1
    null = runs["00"]
    checks["00:stationary"] = null["entire_board_stationary"]
    checks["00:no_receiver_C"] = not null["receiver_all_channel_events"]
    for mask, distance in (("10", d1), ("01", d2)):
        run = runs[mask]
        times = run["record_event_times"]
        checks[f"{mask}:one_R_in_window"] = len(times) == 1 and distance <= times[0] <= distance + 1
        checks[f"{mask}:waiting_symbol"] = bool(times) and all(
            row["memory"] == ([2, 4] if row["step"] < times[0] else [4, 2])
            for row in run["trace"])
        checks[f"{mask}:no_receiver_C"] = not run["receiver_all_channel_events"]
    both = runs["11"]
    times = both["record_event_times"]
    checks["11:two_R_in_windows"] = len(times) == 2 and d1 <= times[0] <= d1 + 1 and d2 <= times[1] <= d2 + 3
    checks["11:exact_symbol_sequence"] = len(times) == 2 and all(
        row["memory"] == ([2, 4] if row["step"] < times[0] else [4, 2] if row["step"] < times[1] else [0, 0])
        for row in both["trace"])
    checks["11:minimum_wait"] = len(times) == 2 and times[1] - times[0] >= 4
    checks["11:zero_waiting_counters"] = len(times) == 2 and all(
        all(a == b == 0 for a, b, _ in both["trace"][t]["detector"])
        for t in range(times[0], times[1]))
    checks["11:zero_waiting_input"] = len(times) == 2 and all(
        both["trace"][t]["next_input"] == [0, 0]
        for t in range(times[0], times[1] - 1))
    all_c = sorted({e["step"] for e in both["receiver_all_channel_events"]})
    checks["11:only_confirmation_C"] = len(times) == 2 and all_c == [times[1]]
    checks["11:causal_counterfactuals"] = len(times) == 2 and all(
        both["trace"][t - 1]["next_input"] != runs[mask]["trace"][t - 1]["next_input"]
        and any(both["trace"][t - 1]["next_input"])
        and any(term["b"] for port in both["trace"][t - 1]["six_inputs"] for term in port)
        for t, mask in zip(times, ("01", "10")))
    differences = {}
    for mask in ("01", "10"):
        differences[mask] = {
            "first_six_term_difference_old_step": next((t for t in range(case["steps"])
                if both["trace"][t]["six_inputs"] != runs[mask]["trace"][t]["six_inputs"]), None),
            "first_net_input_difference_old_step": next((t for t in range(case["steps"])
                if both["trace"][t]["next_input"] != runs[mask]["trace"][t]["next_input"]), None),
        }
    return {"id": case["id"], "passed": all(checks.values()), "checks": checks,
        "R_times": {mask: run["record_event_times"] for mask, run in runs.items()},
        "receiver_C_times": {mask: sorted({e["step"] for e in run["receiver_all_channel_events"]}) for mask, run in runs.items()},
        "causal_input_differences": differences}


def snapshot_sources(output):
    files = [PROTOCOL, Path(__file__), ROOT / "research/signal_clocks/preparation.py",
             ROOT / "research/signal_clocks/run.py", *sorted((ROOT / "universe24").rglob("*.py"))]
    manifest = {}
    for path in files:
        relative = path.relative_to(ROOT)
        data = path.read_bytes()
        manifest[str(relative)] = hashlib.sha256(data).hexdigest()
        target = output / "source" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    write_json(output / "source_manifest.json", manifest)
    return manifest


def execute(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    raw = PROTOCOL.read_bytes()
    protocol = json.loads(raw)
    if protocol["status"] != "frozen_before_search":
        raise ValueError("Search protocol must be frozen")
    (output / "protocol.frozen.json").write_bytes(raw)
    prepared = list(cases(protocol))
    assert len(prepared) == protocol["family"]["cases"]
    write_json(output / "candidate_manifest.json", prepared)
    sources = snapshot_sources(output)
    started = time.process_time()
    wall = time.monotonic()
    results = []
    run_count = 0
    failure = None
    for case in prepared:
        group = {}
        try:
            for mask in protocol["family"]["source_masks"]:
                if time.monotonic() - wall > protocol["budget"]["wall_seconds"]:
                    raise TimeoutError("Declared search wall budget exhausted")
                key = "".join(str(int(v)) for v in mask)
                folder = output / "cases" / (case["id"] + "-s" + key)
                run = run_case(case, tuple(mask), deadline_cpu=started + protocol["budget"]["cpu_seconds"],
                    max_cells=protocol["budget"]["max_stored_channels"], audit=True, output=folder)
                run["receiver_all_channel_events"] = receiver_events(folder / "states.jsonl", run["locations"]["origin"])
                write_json(folder / "receiver_events.json", run["receiver_all_channel_events"])
                group[key] = run
                run_count += 1
            result = evaluate(case, group)
            results.append(result)
            write_json(output / (case["id"] + ".json"), result)
            print(json.dumps({"case": case["id"], "passed": result["passed"],
                "R": result["R_times"], "C": result["receiver_C_times"],
                "cpu_seconds": round(time.process_time() - started, 3)}), flush=True)
        except (TimeoutError, MemoryError) as exc:
            failure = {"case": case["id"], "type": type(exc).__name__, "message": str(exc)}
            break
    summary = {
        "format": "universe24-confirmation-discovery-result-v1", "protocol_id": protocol["protocol_id"],
        "protocol_sha256": hashlib.sha256(raw).hexdigest(),
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "source_manifest": sources, "execution_status": "completed" if failure is None else "inconclusive",
        "case_count": len(prepared), "cases_completed": len(results), "runs_completed": run_count,
        "passing_cases": [result["id"] for result in results if result["passed"]],
        "failure": failure, "cpu_seconds": time.process_time() - started,
        "wall_seconds": time.monotonic() - wall, "results": results,
        "scope": protocol["scope"], "fresh_confirmation_performed": False,
    }
    write_json(output / "result.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    execute(parser.parse_args().output)
