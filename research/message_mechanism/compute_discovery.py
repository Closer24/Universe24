"""Bounded initial-condition discovery of passive packet converters.

python -m research.message_mechanism.compute_discovery --output NEW_DIRECTORY
No search decision is supplied to an evolving board. Each candidate is an
independent complete initial preparation under the unchanged reference engine.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from research.components import TensorSpec
from research.experiments.run import assemble, run_experiment
from research.light_approval.compute import canonical, digest, local_trace, observe, write_json
from research.message_mechanism.compute_baseline import source_hashes
from research.presenter.build import build
from research.presenter.export import bundle, write_bundle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE/"protocol_discovery.json"


def cases(p):
    pairs = list(itertools.product(p["even_remainders"], repeat=2))
    for i, values in enumerate(itertools.product(pairs, repeat=3)):
        yield {"id": f"row3-{i:03d}", "family": "row3", "row_pairs": [[x, list(pair)] for x, pair in zip((45,46,47), values)]}
    for x in (47, 46):
        for i, (row, side) in enumerate(itertools.product(pairs, repeat=2)):
            yield {"id": f"side{x}-{i:03d}", "family": f"side{x}", "row_pairs": [[47, list(row)]], "side_x": x, "side_pair": list(side)}


def spec_for(p, case, present=True):
    source, receiver = p["source"], p["receiver"]
    sockets = list(range(source[0], source[0]+4)) + [receiver[0]] + [x for x, pair in case["row_pairs"]]
    components = [
        {"name": "guide", "recipe": "GuideSegment", "at": [0, source[1], source[2]],
         "params": {"start": 0, "stop": p["board"]["side"]-1, "sockets": sockets, "remainder_pair": p["guide_pair"]}},
        {"name": "source", "recipe": "GuidedPacketSource", "at": source, "params": {"present": present}},
        {"name": "receiver", "recipe": "Receiver", "at": receiver, "params": {"remainders": p["receiver_remainders"]}},
    ]
    for x, pair in case["row_pairs"]:
        components.append({"name": f"converter-{x}", "recipe": "Receiver", "at": [x, receiver[1], receiver[2]], "params": {"remainders": pair}})
    if "side_pair" in case:
        tensor = TensorSpec.from_signs(p["board"]["body_signs"])
        channels = [tensor.ports[2][g] for g in (0,14)]
        components.append({"name": "side-converter", "recipe": "Patch", "at": [case["side_x"], receiver[1]+1, receiver[2]],
                           "params": {"kind": "receiver", "cells": [[0,0,0,g,0,0,r] for g,r in zip(channels, case["side_pair"])],
                                      "ports": {"node": [[0,0,0,g] for g in range(48)]}}})
    identifier = case["id"] + ("-on" if present else "-off")
    return {"format": "universe24-assembly-experiment-v1", "id": identifier,
            "title": "Passive converter discovery: " + identifier,
            "description": "A stationary initial remainder patch changes the actual packet interaction through unchanged Rule3. This is a discovery candidate, not a validated approval/cancellation mechanism.",
            "question": p["question"], "board": p["board"], "steps": p["steps"], "components": components,
            "detectors": ["receiver.node"], "view": {"port": "receiver.memory"},
            "controls": {"case": case, "present": present},
            "provenance": {"protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(), "phase": "discovery"},
            "budget": {"max_frames": p["steps"]+1, "max_cells": 500000, "max_bytes": 67108864, "max_seconds": 60}}


def assess(p, trace, inputs):
    obs = observe(trace)
    target = [[0,0,2] for _ in range(48)]
    target[0][2], target[14][2] = p["acceptance"]["target_pair"]
    quiet = [all(a == b == 0 for a,b,r in state) for state in trace]
    targets = [state == target for state in trace]
    click_times = {row["step"] for row in obs["all48_clicks"]}
    lo, hi = p["acceptance"]["write_window_inclusive"]
    wait = p["acceptance"]["quiet_subsequent_updates"]
    accepted_at = next((t for t in range(lo, hi+1) if all(targets[t:t+wait+1]) and len(targets[t:t+wait+1]) == wait+1
                        and all(quiet[:t+wait+1]) and not any(k <= t+wait for k in click_times)), None)
    longest, best_start = 0, None
    for t in range(lo, hi+1):
        if not all(quiet[:t+1]) or any(k <= t for k in click_times):
            continue
        length = 0
        for s in range(t, len(targets)):
            if not targets[s] or not quiet[s] or s in click_times:
                break
            length += 1
        if length > longest:
            longest, best_start = length, t
    return {"accepted": accepted_at is not None, "accepted_write_state": accepted_at,
            "maximum_quiet_target_states_before_C": longest, "best_target_start": best_start,
            "first_receiver_C": obs["all48_clicks"][0] if obs["all48_clicks"] else None,
            "all48_C": obs["all48_clicks"], "remainder_pairs": obs["remainder_pairs"],
            "pair_actual_inputs": [[row[0], row[14]] for row in inputs],
            "final_input_area": [sum(row[g] for row in inputs[:-1]) for g in range(48)]}


def fingerprint_state(state):
    return digest({"side": state.cube.side, "background": state.background,
                   "cells": [[*address, *value] for address,value in sorted(state.cells.items())]})


def screen(p, spec, deadline_cpu, deadline_wall):
    prepared = assemble(spec)
    state = prepared.initial
    trace, inputs, inverse = [], [], True
    max_cells = len(state.cells)
    for t in range(p["steps"]+1):
        if time.process_time() > deadline_cpu or time.monotonic() > deadline_wall:
            return {"status": "inconclusive-budget", "completed_updates": t}, None, None
        if len(state.cells) > p["budget"]["max_stored_channels_per_state"]:
            return {"status": "inconclusive-support-limit", "completed_updates": t}, None, None
        sums = prepared.engine.input_sums(state)
        trace.append([list(value) for value in state.node(p["receiver"])])
        inputs.append([sums.get((*p["receiver"], g), 0) for g in range(48)])
        if t < p["steps"]:
            following = prepared.engine.advance(state)
            inverse = inverse and prepared.engine.rewind(following) == state
            if not inverse:
                raise AssertionError("Reference full-state inverse mismatch")
            state = following
            max_cells = max(max_cells, len(state.cells))
    return {"status": "completed", "assessment": assess(p, trace, inputs), "all_step_inverses_equal": inverse,
            "final_state_sha256": fingerprint_state(state), "max_stored_channels": max_cells}, trace, inputs


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    started, cpu = time.monotonic(), time.process_time()
    raw = PROTOCOL.read_bytes()
    p = json.loads(raw)
    planned = list(cases(p))
    assert len(planned) == p["budget"]["max_candidates"]
    sources = source_hashes()
    sources[str(Path(__file__).relative_to(ROOT))] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/"records").mkdir()
    (args.output/"protocol.json").write_bytes(raw)
    write_json(args.output/"registration.json", {"protocol_sha256": hashlib.sha256(raw).hexdigest(), "source_sha256": sources,
               "planned_cases": planned, "base_commit": subprocess.check_output(["git","rev-parse","HEAD"], cwd=ROOT, text=True).strip()})
    rows, retained = [], {}
    best, first = {}, {}
    with gzip.GzipFile(filename=str(args.output/"ledger.jsonl.gz"), mode="wb", mtime=0) as ledger:
        for number, case in enumerate(planned, 1):
            spec = spec_for(p, case)
            row, trace, inputs = screen(p, spec, cpu+p["budget"]["max_cpu_seconds"], started+p["budget"]["max_wall_seconds"])
            row.update({"case": case, "spec_sha256": digest(spec)})
            ledger.write((canonical({**row, "receiver_trace": trace, "actual_input_trace": inputs})+"\n").encode())
            rows.append(row)
            if row["status"] != "completed":
                if row["status"] == "inconclusive-budget":
                    break
                continue
            family = case["family"]
            first.setdefault(family, row)
            if family not in best or row["assessment"]["maximum_quiet_target_states_before_C"] > best[family]["assessment"]["maximum_quiet_target_states_before_C"]:
                best[family] = row
            if row["assessment"]["accepted"]:
                retained[case["id"]] = row
            if number % 50 == 0 or row["assessment"]["accepted"]:
                print(f"{number}/{len(planned)} {case['id']} accepted={row['assessment']['accepted']} beststates={row['assessment']['maximum_quiet_target_states_before_C']}", flush=True)
    for row in list(first.values()) + list(best.values()):
        retained[row["case"]["id"]] = row
    display, record_rows = [], []
    # Retained source-on witnesses and matched stationary null controls are full
    # generic recordings, independently replayed from their initial preparation.
    for row in retained.values():
        for present in (True, False):
            if len(record_rows) >= p["budget"]["max_recording_replays"]:
                raise RuntimeError("Full evidence replay budget exhausted; no component acceptance")
            spec = spec_for(p, row["case"], present)
            result = run_experiment(spec)
            e = result["experiment"]
            trace = local_trace(e, p["receiver"])
            inputs = [[int(v) for v in item["next_input"]] for item in result["observations"]["receiver.node"]["trace"]]
            assessment = assess(p, trace, inputs)
            if present:
                assert assessment == row["assessment"], "Discovery replay changed the frozen observer"
            stationary = len({frame["state_sha256"] for frame in e["frames"]}) == 1
            if not present:
                assert stationary
            record = {"spec": spec, "case": row["case"], "assembly": result["assembly"], "experiment": e,
                      "detector_trace": trace, "detector_input_trace": inputs,
                      "detector_observations": result["observations"], "assessment": assessment}
            path = args.output/"records"/(spec["id"]+".json.gz")
            path.write_bytes(gzip.compress(canonical(record).encode(), mtime=0))
            record_rows.append({"id": spec["id"], "record": str(path.relative_to(args.output)),
                                "record_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                "stationary": stationary, "full_rewind_equal": e["provenance"]["full_rewind_equal"]})
            # One best example per family and its null, at most six, remain small.
            if row is best.get(row["case"]["family"]):
                display.append(e)
    for name, expected in sources.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected
    assert PROTOCOL.read_bytes() == raw
    counts = Counter(row["status"] for row in rows)
    report = {"format": "universe24-message-discovery-result-v1", "protocol_sha256": hashlib.sha256(raw).hexdigest(),
              "candidate_count": len(rows), "planned_candidate_count": len(planned), "status_counts": dict(counts),
              "discovery_acceptances": [row["case"] for row in rows if row.get("assessment", {}).get("accepted")],
              "best_per_family": best, "retained_records": record_rows,
              "all_screened_step_inverses_equal": all(row.get("all_step_inverses_equal", False) for row in rows if row["status"] == "completed"),
              "ledger_sha256": hashlib.sha256((args.output/"ledger.jsonl.gz").read_bytes()).hexdigest(),
              "cpu_seconds": time.process_time()-cpu, "wall_seconds": time.monotonic()-started,
              "validated_new_component": False, "physical_light_or_quantum_measurement_established": False}
    write_json(args.output/"result.json", report)
    write_bundle(args.output/"experiments.json", bundle(display[:6], title="Message mechanism: passive converter discovery"))
    build(args.output/"experiments.json", args.output/"The_Presenter.html")
    print(canonical({k: v for k,v in report.items() if k not in ("best_per_family", "retained_records")}))


if __name__ == "__main__":
    main()
