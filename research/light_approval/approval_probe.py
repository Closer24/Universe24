"""Eight prospective autonomous preparations; never prescribe the receiver input."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import time

from research.experiments.run import run_experiment
from research.light_approval.compute import canonical, local_trace, observe, write_json
from research.presenter.build import build
from research.presenter.export import bundle, write_bundle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "approval_protocol.json"


def max_run(values):
    longest = current = 0
    for value in values:
        current = current + 1 if value else 0
        longest = max(longest, current)
    return longest


def make_spec(p, phase, mask):
    xyz = p["receiver"]
    components = [
        {"name": "guide", "recipe": "GuideSegment", "at": xyz, "params": p["guide"]},
        {"name": "receiver", "recipe": "Receiver", "at": xyz, "params": {"remainders": p["receiver_remainders"]}},
    ]
    for name, offset, ab, present in zip(("left", "right"), p["source_offsets"],
                                       (p["left_source_ab"], p["right_source_ab_controls"][phase]), mask):
        components.append({"name": name, "recipe": "SignalSource", "at": [xyz[0]+offset, xyz[1], xyz[2]],
                           "params": {"a": ab[0], "b": ab[1], "present": present}})
    identifier = f"approval-phase{phase}-" + "".join(str(int(v)) for v in mask)
    return {"format": "universe24-assembly-experiment-v1", "id": identifier,
            "title": "Autonomous pending/approval probe: " + identifier,
            "description": "A prospective two-preloaded-source latch candidate. Every actual input arises from unchanged Rule3. Scalar conditional latch algebra is not assumed to guarantee this preparation works.",
            "question": p["question"], "board": p["board"], "components": components,
            "steps": p["steps"], "detectors": ["receiver.node"], "view": {"port": "receiver.memory"},
            "controls": {"right_phase": phase, "source_mask": mask},
            "provenance": {"protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()},
            "budget": {"max_frames": 33, "max_cells": 500000, "max_bytes": 67108864, "max_seconds": 60}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "records").mkdir()
    raw_protocol = PROTOCOL.read_bytes()
    p = json.loads(raw_protocol)
    (args.output / "protocol.json").write_bytes(raw_protocol)
    planned = [make_spec(p, phase, mask) for phase in (0, 1) for mask in p["source_masks"]]
    sources = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
               for folder in (ROOT/"universe24", ROOT/"research/components", ROOT/"research/presenter")
               for path in sorted(folder.rglob("*.py"))}
    for path in (Path(__file__), HERE/"compute.py", ROOT/"research/experiments/run.py"):
        sources[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    registration = {"protocol_sha256": hashlib.sha256(raw_protocol).hexdigest(), "specs": planned,
                    "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                    "source_sha256": sources}
    write_json(args.output / "registration.json", registration)
    started, cpu = time.monotonic(), time.process_time()
    rows, recordings = [], []
    for spec in planned:
        if time.process_time()-cpu > p["budget"]["max_cpu_seconds"] or time.monotonic()-started > p["budget"]["max_wall_seconds"]:
            raise RuntimeError("Registered secondary budget exceeded")
        result = run_experiment(spec)
        e = result["experiment"]
        trace = local_trace(e, p["receiver"])
        obs = observe(trace)
        inputs = [row["next_input"] for row in result["observations"]["receiver.node"]["trace"]]
        paired_inputs = [[int(row[0]), int(row[14])] for row in inputs]
        node_times = sorted({row["step"] for row in obs["all48_clicks"]})
        pending = [row[0] == [0, 0, 4] and row[14] == [0, 0, 2] for row in trace]
        record = [row[0][2] == row[14][2] == 0 and row[0][0]**2+row[0][1]**2 == 1 and row[14][0]**2+row[14][1]**2 == 0 for row in trace]
        first = node_times[0] if node_times else None
        first_input = next(({"update": t+1, "input": v} for t, v in enumerate(paired_inputs[:-1]) if any(v)), None)
        row = {"id": spec["id"], "controls": spec["controls"], "node_C_times": node_times,
               "events": obs["all48_clicks"], "first_paired_input": first_input,
               "pending_times": [i for i, value in enumerate(pending) if value],
               "maximum_pending_run": max_run(pending[1:]),
               "maximum_pending_before_first_C": max_run(pending[1:first]) if first else max_run(pending[1:]),
               "record_times": [i for i, value in enumerate(record) if value],
               "record_holds8_after_first_C": first is not None and first+8 <= len(record) and all(record[first:first+8]),
               "stationary_full_board": len({frame["state_sha256"] for frame in e["frames"]}) == 1,
               "full_rewind_equal": e["provenance"]["full_rewind_equal"],
               "frames": len(e["frames"]), "I": obs["I"], "remainder_pairs": obs["remainder_pairs"]}
        record_value = {"spec": spec, "assembly": result["assembly"], "experiment": e,
                        "detector_trace": trace, "detector_input_trace": inputs, "result": row}
        path = args.output / "records" / (spec["id"] + ".json.gz")
        path.write_bytes(gzip.compress(canonical(record_value).encode(), mtime=0))
        row["record"] = str(path.relative_to(args.output))
        row["record_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(row)
        recordings.append(e)
        print(canonical({"id": row["id"], "node_C_times": node_times, "pending_run": row["maximum_pending_run"], "record_hold8": row["record_holds8_after_first_C"]}), flush=True)
    phase_results = []
    for phase in (0, 1):
        cases = {"".join(str(int(x)) for x in row["controls"]["source_mask"]): row for row in rows if row["controls"]["right_phase"] == phase}
        both = cases["11"]
        checks = {
            "null_stationary_no_C": cases["00"]["stationary_full_board"] and not cases["00"]["node_C_times"],
            "left_only_no_C_through32": not cases["10"]["node_C_times"],
            "right_only_no_C_through32": not cases["01"]["node_C_times"],
            "left_only_pending4": cases["10"]["maximum_pending_run"] >= 4,
            "joint_pending4_before_C": both["maximum_pending_before_first_C"] >= 4,
            "joint_exactly_one_C_in_window": len(both["node_C_times"]) == 1 and 15 <= both["node_C_times"][0] <= 19,
            "joint_record_holds8": both["record_holds8_after_first_C"],
        }
        phase_results.append({"right_phase": phase, "right_initial_ab": p["right_source_ab_controls"][phase],
                              "checks": checks, "accepted": all(checks.values())})
    assert PROTOCOL.read_bytes() == raw_protocol
    for path, expected in sources.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected
    report = {"schema": "universe24-autonomous-approval-result-v1", "protocol_sha256": registration["protocol_sha256"],
              "base_commit": registration["base_commit"], "source_sha256": sources,
              "engine_runs": len(rows), "complete_states": sum(row["frames"] for row in rows),
              "forward_inverse_transitions": len(rows)*p["steps"], "all_full_rewinds_equal": all(row["full_rewind_equal"] for row in rows),
              "phase_results": phase_results, "accepted_phase_count": sum(row["accepted"] for row in phase_results),
              "cases": rows, "seconds": time.monotonic()-started, "cpu_seconds": time.process_time()-cpu,
              "scope": p["acceptance"]["scope"], "physical_entanglement_established": False}
    write_json(args.output / "result.json", report)
    write_bundle(args.output / "experiments.json", bundle(recordings, title="Autonomous pending/approval probes — all controls"))
    build(args.output / "experiments.json", args.output / "The_Presenter.html")
    print(canonical({k: v for k, v in report.items() if k not in ("source_sha256", "cases")}))


if __name__ == "__main__":
    main()
