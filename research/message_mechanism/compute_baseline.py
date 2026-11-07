"""Frozen compact-packet/receiver baseline; only the reference engine evolves.

python -m research.message_mechanism.compute_baseline --output NEW_DIRECTORY
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from research.experiments.run import run_experiment
from research.light_approval.compute import canonical, digest, local_trace, observe, write_json
from research.presenter.build import build
from research.presenter.export import bundle, write_bundle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "protocol_baseline.json"


def cases(protocol):
    values = protocol["apparatus"]["receiver_remainders"]
    for r0, r14, present in itertools.product(values, values, (True, False)):
        yield {"id": f"packet-r{r0}{r14}-{'on' if present else 'off'}",
               "remainders": [r0, r14], "present": present}


def spec_for(protocol, case):
    source, receiver = (protocol["apparatus"][key] for key in ("source", "receiver"))
    sockets = protocol["apparatus"]["source_socket_x"] + [receiver[0]]
    return {
        "format": "universe24-assembly-experiment-v1", "id": case["id"],
        "title": "Compact packet / receiver: " + case["id"],
        "description": "A complete prepared guided packet meets a passive initial remainder defect. All48 channels and the transverse halo are retained. No runtime message or detector operation is added.",
        "question": protocol["question"], "board": protocol["board"], "steps": protocol["steps"],
        "components": [
            {"name": "guide", "recipe": "GuideSegment", "at": [0, source[1], source[2]],
             "params": {"start": 0, "stop": protocol["board"]["side"]-1,
                        "sockets": sockets, "remainder_pair": protocol["apparatus"]["guide_pair"]}},
            {"name": "source", "recipe": "GuidedPacketSource", "at": source,
             "params": {"present": case["present"]}},
            {"name": "receiver", "recipe": "Receiver", "at": receiver,
             "params": {"remainders": case["remainders"]}},
        ], "detectors": ["receiver.node"], "view": {"port": "receiver.memory"},
        "controls": case,
        "provenance": {"protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(), "case": case},
        "budget": {"max_frames": protocol["steps"]+1, "max_cells": 500000,
                   "max_bytes": 67108864, "max_seconds": 60},
    }


def assess(protocol, case, trace, inputs):
    result = observe(trace)
    start, stop = protocol["receiver"]["pending_states_inclusive"]
    target = [(case["remainders"][0]-2) % 6, (case["remainders"][1]+2) % 6]
    full_target = [2]*48
    full_target[0], full_target[14] = target
    target_fail = next((t for t in range(start, stop+1) if [row[2] for row in trace[t]] != full_target), None)
    counter_fail = next((t for t in range(stop+1) if any(a or b for a, b, r in trace[t])), None)
    click_fail = next((item for item in result["all48_clicks"] if item["step"] <= stop), None)
    area = [[0]*48]
    for row in inputs[:-1]:
        area.append([old+int(u) for old, u in zip(area[-1], row)])
    result.update({"target_pair": target, "full_target_remainders": full_target,
                   "target_attained_at_first_arrival": [row[2] for row in trace[start]] == full_target,
                   "first_target_mismatch_state": target_fail,
                   "first_nonzero_receiver_counter_state": counter_fail,
                   "first_disallowed_receiver_C": click_fail,
                   "cumulative_input_area": area,
                   "pending_accepted": bool(case["present"] and target != case["remainders"]
                                            and target_fail is None and counter_fail is None and click_fail is None)})
    return result


def source_hashes():
    files = [p for folder in ("universe24", "research/components", "research/presenter", "research/experiments")
             for p in (ROOT/folder).rglob("*.py")]
    files.extend([Path(__file__), ROOT/"research/light_approval/compute.py"])
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}


def translated_equal(experiment):
    bg, side = list(experiment["background"]), experiment["side"]
    def state(frame):
        return {tuple(row[:4]): row[4:] for row in frame["cells"]}
    # The complete sparse map includes the uniform periodic guide and all halo entries.
    return all({((a[0]+1) % side, *a[1:]): value for a, value in state(old).items()} == state(new)
               for old, new in zip(experiment["frames"], experiment["frames"][1:]))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    started, cpu = time.monotonic(), time.process_time()
    raw = PROTOCOL.read_bytes()
    protocol, sources = json.loads(raw), source_hashes()
    planned = list(cases(protocol))
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/"records").mkdir()
    (args.output/"protocol.json").write_bytes(raw)
    registration = {"protocol_sha256": hashlib.sha256(raw).hexdigest(), "source_sha256": sources,
                    "planned_cases": planned,
                    "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()}
    write_json(args.output/"registration.json", registration)
    rows, display = [], []
    for number, case in enumerate(planned, 1):
        if time.process_time()-cpu > protocol["budget"]["max_cpu_seconds"] or time.monotonic()-started > protocol["budget"]["max_wall_seconds"]:
            write_json(args.output/"failure.json", {"reason": "Prospective study budget exhausted", "completed": len(rows)})
            raise RuntimeError("Study budget exhausted")
        spec = spec_for(protocol, case)
        result = run_experiment(spec)
        experiment = result["experiment"]
        trace = local_trace(experiment, protocol["apparatus"]["receiver"])
        detector_rows = result["observations"]["receiver.node"]["trace"]
        inputs = [row["next_input"] for row in detector_rows]
        assessment = assess(protocol, case, trace, inputs)
        record = {"case": case, "spec": spec, "assembly": result["assembly"], "experiment": experiment,
                  "detector_trace": trace, "detector_input_trace": inputs,
                  "detector_observations": result["observations"], "assessment": assessment}
        path = args.output/"records"/(case["id"]+".json.gz")
        path.write_bytes(gzip.compress(canonical(record).encode(), mtime=0))
        hashes = [frame["state_sha256"] for frame in experiment["frames"]]
        row = {"case": case, "assessment": assessment, "record": str(path.relative_to(args.output)),
               "record_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
               "initial_state_sha256": hashes[0], "final_state_sha256": hashes[-1],
               "stationary": len(set(hashes)) == 1, "translation_every_step": translated_equal(experiment),
               "frames": len(hashes), "full_rewind_equal": experiment["provenance"]["full_rewind_equal"]}
        rows.append(row)
        if case["id"] in protocol["presenter_cases"]:
            display.append(experiment)
        print(f"{number}/18 {case['id']} pending={assessment['pending_accepted']} firstC={assessment['first_disallowed_receiver_C']}", flush=True)
    assert PROTOCOL.read_bytes() == raw and source_hashes() == sources
    result = {"format": "universe24-message-interface-result-v1", "registration": registration,
              "engine_runs": len(rows), "complete_states": sum(r["frames"] for r in rows),
              "forward_inverse_transitions": len(rows)*protocol["steps"],
              "pending_accepted": sum(r["assessment"]["pending_accepted"] for r in rows),
              "all_full_rewinds_equal": all(r["full_rewind_equal"] for r in rows),
              "all_null_boards_stationary": all(r["stationary"] for r in rows if not r["case"]["present"]),
              "translation_control_passed": next(r["translation_every_step"] for r in rows if r["case"]["id"] == "packet-r04-on"),
              "cpu_seconds": time.process_time()-cpu, "wall_seconds": time.monotonic()-started, "cases": rows,
              "physical_light_or_quantum_measurement_established": False}
    write_json(args.output/"result.json", result)
    display.sort(key=lambda e: protocol["presenter_cases"].index(e["id"]))
    write_bundle(args.output/"experiments.json", bundle(display, title="Message mechanism: packet / receiver interface"))
    build(args.output/"experiments.json", args.output/"The_Presenter.html")
    print(canonical({k: v for k, v in result.items() if k not in ("cases", "registration")}))


if __name__ == "__main__":
    main()
