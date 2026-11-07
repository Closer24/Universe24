"""Inverse preparation is external optimization; all recorded runtime is forward.

python -m research.message_mechanism.compute_reverse --output NEW_DIRECTORY
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

from research.experiments.run import assemble, recorded_states, run_experiment
from research.light_approval.compute import canonical, digest, local_trace, observe, write_json
from research.message_mechanism.compute_baseline import source_hashes
from research.message_mechanism.compute_discovery import fingerprint_state
from research.presenter.build import build
from research.presenter.export import bundle, write_bundle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE/"protocol_reverse.json"


def cases(p):
    for i, (packet_x, compensation_x, r0, r14) in enumerate(itertools.product(p["endpoint_packet_x"], p["endpoint_compensation_x"], p["even_remainders"], p["even_remainders"])):
        yield {"id": f"reverse-{i:03d}", "packet_x": packet_x, "compensation_x": compensation_x, "compensation_pair": [r0,r14]}


def endpoint_spec(p, case):
    y,z = p["receiver"][1:]
    sockets = list(range(case["packet_x"], case["packet_x"]+4)) + [p["receiver"][0], case["compensation_x"]]
    return {"format": "universe24-assembly-experiment-v1", "id": case["id"]+"-endpoint",
            "board": p["board"], "steps": 0,
            "components": [
                {"name": "guide", "recipe": "GuideSegment", "at": [0,y,z],
                 "params": {"start": 0, "stop": p["board"]["side"]-1, "sockets": sockets, "remainder_pair": p["guide_pair"]}},
                {"name": "packet", "recipe": "GuidedPacketSource", "at": [case["packet_x"],y,z]},
                {"name": "receiver", "recipe": "Receiver", "at": p["receiver"], "params": {"remainders": p["target_receiver_pair"]}},
                {"name": "compensation", "recipe": "Receiver", "at": [case["compensation_x"],y,z], "params": {"remainders": case["compensation_pair"]}},
            ]}


def receiver_state(pair):
    result = [[0,0,2] for _ in range(48)]
    result[0][2], result[14][2] = pair
    return result


def preparation(p, case):
    endpoint = assemble(endpoint_spec(p, case))
    state = endpoint.initial
    inverse_hashes = [fingerprint_state(state)]
    for _ in range(p["inverse_preparation_steps"]):
        previous = endpoint.engine.rewind(state)
        assert endpoint.engine.advance(previous) == state
        if len(previous.cells) > p["budget"]["max_stored_channels_per_state"]:
            raise RuntimeError("Registered inverse-preparation support budget exceeded")
        state = previous
        inverse_hashes.append(fingerprint_state(state))
    initial = state
    actual_receiver = [list(v) for v in initial.node(p["receiver"])]
    expected_receiver = receiver_state(p["initial_receiver_pair"])
    active = [a for a,v in initial.cells.items() if v.a or v.b]
    outside = [a for a in active if any(not lo <= coordinate <= hi for coordinate,(lo,hi) in zip(a[:3],p["source_box_inclusive"]))]
    distance = min((sum(min(abs(a[d]-p["receiver"][d]), p["board"]["side"]-abs(a[d]-p["receiver"][d])) for d in range(3)) for a in active), default=None)
    row = {"case": case, "initial_receiver": actual_receiver,
           "initial_receiver_mismatches": sum(a != b for a,b in zip(actual_receiver, expected_receiver)),
           "initial_active_channels": len(active), "source_box_violations": len(outside),
           "minimum_source_distance": distance, "initial_state_sha256": fingerprint_state(initial),
           "endpoint_state_sha256": inverse_hashes[0], "inverse_state_sha256": inverse_hashes,
           "all_inverse_preparation_steps_forward_checked": True,
           "initial_admissible": actual_receiver == expected_receiver and bool(active) and not outside}
    return row, initial, endpoint.initial


def forward_spec(p, case, initial, present):
    rows = []
    for a,v in sorted(initial.cells.items()):
        inside = all(lo <= coordinate <= hi for coordinate,(lo,hi) in zip(a[:3],p["source_box_inclusive"]))
        keep = present or not inside
        rows.append([*a, v.a if keep else 0, v.b if keep else 0, v.r])
    receiver = p["receiver"]
    identifier = case["id"] + ("-on" if present else "-source-box-off")
    return {"format": "universe24-assembly-experiment-v1", "id": identifier,
            "title": "Reverse-designed preparation: " + identifier,
            "description": "All inverse operations occurred in external initial preparation. This recording contains only forward unchanged Rule3 evolution. Initial-support and idle-receiver eligibility are separately tested; a failed preparation is not a component.",
            "question": p["question"], "board": p["board"], "steps": p["forward_steps"],
            "components": [{"name": "receiver", "recipe": "Patch", "at": [0,0,0],
                            "params": {"kind": "signal-source", "cells": rows,
                                       "ports": {"node": [[*receiver,g] for g in range(48)], "memory": [[*receiver,g] for g in (0,14)]}}}],
            "detectors": ["receiver.node"], "view": {"port": "receiver.memory"},
            "controls": {"case": case, "present": present},
            "provenance": {"protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(), "phase": "inverse-initial-preparation-discovery", "inverse_steps_before_run": p["inverse_preparation_steps"]},
            "budget": {"max_frames": p["forward_steps"]+1, "max_cells": 500000, "max_bytes": 67108864, "max_seconds": 60}}


def assess(p, preparation_row, trace, inputs):
    obs = observe(trace)
    t = p["inverse_preparation_steps"]
    target = receiver_state(p["target_receiver_pair"])
    quiet = all(all(a == b == 0 for a,b,r in state) for state in trace)
    retained = all(state == target for state in trace[t:])
    area = [sum(int(row[g]) for row in inputs[:t]) for g in range(48)]
    first_change = next((i for i,state in enumerate(trace) if state != trace[0]), None)
    causal = first_change is not None and first_change >= preparation_row["minimum_source_distance"]
    checks = {"initial_admissible": preparation_row["initial_admissible"], "quiet_all48_prefix": quiet,
              "no_receiver_C": not obs["all48_clicks"], "target_retained32_through40": retained,
              "actual_pair_input_area": [area[0],area[14]] == [-1,1], "causal_first_change": causal}
    return {"checks": checks, "accepted": all(checks.values()), "first_receiver_change": first_change,
            "all48_C": obs["all48_clicks"], "remainder_pairs": obs["remainder_pairs"], "input_area_through32": area}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    raw = PROTOCOL.read_bytes()
    p, started, cpu = json.loads(raw), time.monotonic(), time.process_time()
    planned = list(cases(p))
    assert len(planned) == p["budget"]["max_candidates"]
    sources = source_hashes()
    for name in ("compute_discovery.py", "compute_reverse.py"):
        path = HERE/name
        sources[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/"records").mkdir()
    (args.output/"preparations").mkdir()
    (args.output/"protocol.json").write_bytes(raw)
    write_json(args.output/"registration.json", {"protocol_sha256": hashlib.sha256(raw).hexdigest(), "source_sha256": sources, "planned_cases": planned,
               "base_commit": subprocess.check_output(["git","rev-parse","HEAD"], cwd=ROOT, text=True).strip()})
    rows, initials, endpoints = [], {}, {}
    for case in planned:
        if time.process_time()-cpu > p["budget"]["max_cpu_seconds"] or time.monotonic()-started > p["budget"]["max_wall_seconds"]:
            raise RuntimeError("Registered inverse-preparation budget exhausted")
        row, initial, endpoint = preparation(p, case)
        prepared_path = args.output/"preparations"/(case["id"]+".json.gz")
        prepared_path.write_bytes(gzip.compress(canonical({"endpoint_spec":endpoint_spec(p,case),
            "initial_cells":[[*a,*v] for a,v in sorted(initial.cells.items())],
            "initial_state_sha256":row["initial_state_sha256"],"source_box_inclusive":p["source_box_inclusive"]}).encode(),mtime=0))
        row["preparation_record"] = str(prepared_path.relative_to(args.output))
        row["preparation_record_sha256"] = hashlib.sha256(prepared_path.read_bytes()).hexdigest()
        rows.append(row)
        initials[case["id"]], endpoints[case["id"]] = initial, endpoint
        print(canonical({k:row[k] for k in ("case","initial_receiver_mismatches","source_box_violations","initial_admissible")}), flush=True)
    write_json(args.output/"preparation_ledger.json", rows)
    best = min(rows, key=lambda row: (row["initial_receiver_mismatches"], row["source_box_violations"], row["case"]["id"]))
    retained = {row["case"]["id"]:row for row in rows if row["initial_admissible"]}
    retained[rows[0]["case"]["id"]] = rows[0]
    retained[best["case"]["id"]] = best
    records, display, accepted = [], [], []
    for identifier,row in retained.items():
        for present in (True,False):
            if time.process_time()-cpu > p["budget"]["max_cpu_seconds"] or time.monotonic()-started > p["budget"]["max_wall_seconds"]:
                raise RuntimeError("Registered forward-recording budget exhausted")
            if len(records) >= p["budget"]["max_recording_replays"]:
                raise RuntimeError("Registered forward replay count exhausted")
            spec = forward_spec(p, row["case"], initials[identifier], present)
            result = run_experiment(spec)
            e = result["experiment"]
            endpoint_equal = None
            if present:
                endpoint_equal = recorded_states(e)[p["inverse_preparation_steps"]] == endpoints[identifier]
                assert endpoint_equal, "Forward replay did not reconstruct the exact prepared endpoint"
            trace = local_trace(e,p["receiver"])
            inputs = [[int(v) for v in item["next_input"]] for item in result["observations"]["receiver.node"]["trace"]]
            assessment = assess(p,row,trace,inputs)
            if present and assessment["accepted"]:
                accepted.append(identifier)
            stationary = len({frame["state_sha256"] for frame in e["frames"]}) == 1
            if not present and row["initial_admissible"]:
                assert stationary
            record = {"spec": spec, "case": row["case"], "preparation": row, "assembly": result["assembly"],
                      "experiment": e, "detector_trace": trace, "detector_input_trace": inputs,
                      "detector_observations": result["observations"], "assessment": assessment,
                      "complete_endpoint_reconstructed": endpoint_equal}
            path = args.output/"records"/(spec["id"]+".json.gz")
            path.write_bytes(gzip.compress(canonical(record).encode(),mtime=0))
            records.append({"id":spec["id"], "record":str(path.relative_to(args.output)), "record_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                            "stationary":stationary, "assessment":assessment, "full_rewind_equal":e["provenance"]["full_rewind_equal"],
                            "complete_endpoint_reconstructed":endpoint_equal})
            if len(display)<6:
                display.append(e)
    for name,expected in sources.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected
    assert PROTOCOL.read_bytes()==raw
    report={"format":"universe24-message-inverse-preparation-result-v1", "protocol_sha256":hashlib.sha256(raw).hexdigest(),
            "candidates":len(rows), "initial_admissible_count":sum(row["initial_admissible"] for row in rows),
            "accepted_discoveries":accepted, "best_initial_preparation":best,
            "all_inverse_preparation_steps_forward_checked":True, "preparation_inverse_steps":len(rows)*p["inverse_preparation_steps"],
            "records":records, "cpu_seconds":time.process_time()-cpu, "wall_seconds":time.monotonic()-started,
            "validated_new_component":False}
    write_json(args.output/"result.json",report)
    write_bundle(args.output/"experiments.json",bundle(display,title="Message mechanism: reverse-designed initial preparations"))
    build(args.output/"experiments.json",args.output/"The_Presenter.html")
    if time.process_time()-cpu > p["budget"]["max_cpu_seconds"] or time.monotonic()-started > p["budget"]["max_wall_seconds"]:
        raise RuntimeError("Registered total study budget exceeded")
    if sum(path.stat().st_size for path in args.output.rglob("*") if path.is_file()) > p["budget"]["max_output_bytes"]:
        raise RuntimeError("Registered evidence size budget exceeded")
    print(canonical({k:v for k,v in report.items() if k not in ("records","best_initial_preparation")}))


if __name__=="__main__":
    main()
