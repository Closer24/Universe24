"""Frozen finite opposing-packet study using only the reference Rule3 engine.

python -m research.message_mechanism.interaction_search --output NEW_DIRECTORY
All assembly happens before capture. Observers never modify a state.
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

from research.components import (BoardSpec, GuideSegment, GuidedPacketSource,
                                 Patch, Receiver, finalize, place, plain)
from research.presenter.export import capture, _portable_state, state_sha256
from universe24 import Channel, State
from universe24.observation.clicks import classify
from universe24.core.group_2o import DIRECTIONS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "interaction_protocol.json"


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(data):
    return hashlib.sha256(canonical(data).encode()).hexdigest()


def save(path, data):
    raw = (json.dumps(data, sort_keys=True, indent=2) + "\n").encode()
    if path.suffix == ".gz":
        path.write_bytes(gzip.compress(raw, mtime=0))
    else:
        path.write_bytes(raw)


def reverse_patch(patch):
    """Exact even-sector time reversal, including every halo remainder."""
    return Patch(patch.kind, {address: (value.b, value.a, 4-value.r)
                             for address, value in patch.cells},
                 tensor=patch.tensor, background=patch.background,
                 ports=patch.ports, sources=patch.sources,
                 evidence_domains=("J reverses complete even-sector Rule3 trajectories.",))


def cases(protocol):
    family = protocol["family"]
    for direction in (1, -1):
        yield {"id": "carrier-right" if direction == 1 else "carrier-left",
               "family": "carrier", "direction": direction}
    for phase in ("discovery", "holdout"):
        delays = family[phase + "_right_source_delays"]
        for seam, delay, control in itertools.product(
                family["seam_remainder_pairs"], delays,
                protocol["source_contract"]["controls"]):
            yield {"id": f"seam-{seam[0]}-{seam[1]}-delay-{delay}-{control}",
                   "family": phase, "seam": seam, "delay": delay,
                   "control": control}


def prepare(protocol, case):
    geo = protocol["geometry"]
    center = (0, geo["y"], geo["z"])
    board = BoardSpec(protocol["side"])
    left = geo["left_source_x"]
    placements = []
    if case["family"] == "carrier":
        reverse = case["direction"] < 0
        pair = (4, 0) if reverse else (0, 4)
        source = GuidedPacketSource()
        if reverse:
            source = reverse_patch(source)
        placements = [
            place(GuideSegment(start=0, stop=board.side-1,
                               sockets=tuple(range(left, left+4)),
                               remainder_pair=pair), at=center, name="guide"),
            place(source, at=(left, center[1], center[2]), name="source"),
        ]
        return finalize(board, placements)
    right = geo["right_source_x_before_delay"] + case["delay"]
    seam = geo["seam_x"]
    placements.extend([
        place(GuideSegment(start=0, stop=seam-1,
                           sockets=tuple(range(left, left+4)),
                           remainder_pair=geo["left_guide_remainders"]),
              at=center, name="left-guide"),
        place(GuideSegment(start=seam+1, stop=board.side-1,
                           sockets=tuple(range(right, right+4)),
                           remainder_pair=geo["right_guide_remainders"]),
              at=center, name="right-guide"),
        place(Receiver(remainders=case["seam"]),
              at=(seam, center[1], center[2]), name="seam"),
        place(GuidedPacketSource(present=case["control"][0] == "1"),
              at=(left, center[1], center[2]), name="left-source"),
        place(reverse_patch(GuidedPacketSource(present=case["control"][1] == "1")),
              at=(right, center[1], center[2]), name="right-source"),
    ])
    return finalize(board, placements)


def translated(state, dx):
    return State(state.cube, state.background,
                 {((address[0]+dx) % state.cube.side, *address[1:]): value
                  for address, value in state.cells.items()})


def probes(protocol, engine, states):
    geo = protocol["geometry"]
    xs = [geo["left_outlet_x"], *geo["memory_nodes_x"], geo["right_outlet_x"]]
    result = {}
    for x in xs:
        xyz = (x, geo["y"], geo["z"])
        nodes = [[list(value) for value in state.node(xyz)] for state in states]
        events, inputs = [], []
        for t, (old, new) in enumerate(zip(states, states[1:]), 1):
            for g in range(48):
                event = classify(old.at((*xyz, g)), new.at((*xyz, g)))
                if event is not None:
                    events.append({"step": t, "channel": g,
                                   "kind": event[0], "ell": event[1]})
            row = {"step": t, "pair": []}
            for g in (0, 14):
                terms = []
                for d, delta in enumerate(DIRECTIONS):
                    address = (*tuple((xyz[j]+delta[j]) % old.cube.side
                                      for j in range(3)), engine.coupling.ports[d][g])
                    terms.append(engine.coupling.weights[d][g] * old.at(address).b)
                row["pair"].append({"channel": g, "signed_terms": terms,
                                    "u": sum(terms),
                                    "ell": new.at((*xyz, g)).b + old.at((*xyz, g)).a})
            inputs.append(row)
        windows = []
        initial_pair = [nodes[0][0][2], nodes[0][14][2]]
        if x in geo["memory_nodes_x"]:
            for start in range(12, len(states)-8):
                node = nodes[start]
                if (all(v[0] == v[1] == 0 for v in node)
                        and all(nodes[t] == node for t in range(start, start+9))
                        and [node[0][2], node[14][2]] != initial_pair):
                    windows.append({"start": start, "through": start+8,
                                    "pair": [node[0][2], node[14][2]]})
        lo, hi = protocol["readouts"]["outbound_window_inclusive"]
        outbound = [row for row in events
                    if lo <= row["step"] <= hi and row["channel"] in (0, 14)]
        result[str(x)] = {"position": list(xyz), "nodes": nodes, "events": events,
                          "inputs": inputs, "pair_outbound_C": outbound,
                          "quiet_windows_before_null_comparison": windows}
    return result


def first_nonlinearity(group):
    cases_by_control = {row["case"]["control"]: row for row in group}
    for t in range(len(group[0]["states"])):
        states = {mask: row["states"][t] for mask, row in cases_by_control.items()}
        addresses = set().union(*(state.cells for state in states.values()))
        for address in sorted(addresses):
            values = {mask: state.at(address) for mask, state in states.items()}
            for component in (0, 1):
                expected = values["10"][component] + values["01"][component] - values["00"][component]
                actual = values["11"][component]
                if actual != expected:
                    return {"step": t, "address": list(address),
                            "component": "ab"[component], "actual11": actual,
                            "linear_control_combination": expected}
    return None


def compare(protocol, group):
    by = {row["case"]["control"]: row for row in group}
    geo = protocol["geometry"]
    left, right = str(geo["left_outlet_x"]), str(geo["right_outlet_x"])
    counts = {mask: {side: len(row["probes"][x]["pair_outbound_C"])
                     for side, x in (("left", left), ("right", right))}
              for mask, row in by.items()}
    distinct = len({row["final_hash"] for row in group}) == 4
    cancelled = {}
    for side, incoming, other in (("right", "10", "01"), ("left", "01", "10")):
        cancelled[side] = bool(counts[incoming][side] and not counts[other][side]
                               and not counts["00"][side] and not counts["11"][side]
                               and by[incoming]["final_hash"] != by["11"]["final_hash"])
    quiet = []
    for mask, row in by.items():
        if mask == "00":
            continue
        for x in geo["memory_nodes_x"]:
            key = str(x)
            for window in row["probes"][key]["quiet_windows_before_null_comparison"]:
                start, through = window["start"], window["through"]
                if all(row["probes"][key]["nodes"][t] != by["00"]["probes"][key]["nodes"][t]
                       for t in range(start, through+1)):
                    quiet.append({"control": mask, "x": x, **window})
    case = group[0]["case"]
    return {"family": case["family"], "seam": case["seam"], "delay": case["delay"],
            "outbound_pair_C_counts": counts, "strict_local_cancellation": cancelled,
            "quiet_remainder_records": quiet, "four_final_states_distinct": distinct,
            "first_nonlinear_counter_interaction": first_nonlinearity(group),
            "center_pair_input_waveforms": {mask: [p["pair"] for p in row["probes"][str(geo["seam_x"])]["inputs"]]
                                              for mask, row in by.items()}}


def run(output):
    protocol_bytes = PROTOCOL.read_bytes()
    protocol = json.loads(protocol_bytes)
    protocol_hash = hashlib.sha256(protocol_bytes).hexdigest()
    output.mkdir(parents=True, exist_ok=False)
    (output / "records").mkdir()
    (output / "probes").mkdir()
    (output / "assemblies").mkdir()
    (output / "protocol.json").write_bytes(protocol_bytes)
    started_wall, started_cpu = time.monotonic(), time.process_time()
    source_hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                     for path in [Path(__file__).resolve(), PROTOCOL,
                                  *sorted((ROOT / "universe24").rglob("*.py")),
                                  *sorted((ROOT / "research/components").glob("*.py"))]}
    results, comparisons, current = [], [], []
    for index, case in enumerate(cases(protocol), 1):
        if (index > protocol["budget"]["max_engine_cases"]
                or time.process_time()-started_cpu > protocol["budget"]["max_cpu_seconds"]
                or time.monotonic()-started_wall > protocol["budget"]["max_wall_seconds"]):
            raise RuntimeError("Explicit interaction study budget reached")
        prepared = prepare(protocol, case)
        steps = protocol["family"]["carrier_check_steps"] if case["family"] == "carrier" else protocol["steps"]
        recording = capture(prepared.engine, prepared.initial, steps,
                            id=case["id"], title="Opposing compact packets: " + case["id"],
                            description="Initial data only. Complementary guides and exact time-reversed packet. Local readouts do not erase full states.",
                            view={"position": [64, 64, 64], "channel": 0},
                            max_frames=steps+1, max_cells=500000, max_seconds=90)
        recording["provenance"]["interaction_protocol_sha256"] = protocol_hash
        recording["provenance"]["interaction_case"] = case
        states = [_portable_state(frame, recording["side"], Channel(*map(int, recording["background"])))
                  for frame in recording["frames"]]
        boundary = [{"step": t, "address": list(address)} for t, state in enumerate(states)
                    for address, value in state.cells.items()
                    if (value.a or value.b) and any(q in (0, state.cube.side-1) for q in address[:3])]
        if boundary:
            raise AssertionError("Active support touched periodic boundary")
        translation_equal = None
        if case["family"] == "carrier":
            translation_equal = all(state == translated(states[0], case["direction"]*t)
                                    for t, state in enumerate(states))
            if not translation_equal:
                raise AssertionError("Exact carrier translation check failed")
        trace = probes(protocol, prepared.engine, states)
        raw = canonical(recording).encode()
        record_path = output / "records" / (case["id"] + ".json.gz")
        record_path.write_bytes(gzip.compress(raw, mtime=0))
        save(output / "probes" / (case["id"] + ".json.gz"), trace)
        save(output / "assemblies" / (case["id"] + ".json.gz"), plain(prepared.manifest))
        row = {"case": case, "initial_hash": state_sha256(states[0]),
               "final_hash": state_sha256(states[-1]), "record_sha256": hashlib.sha256(raw).hexdigest(),
               "record_gzip_sha256": hashlib.sha256(record_path.read_bytes()).hexdigest(),
               "frames": len(states), "all_transition_inverses": True, "full_rewind_equal": True,
               "no_active_wrap": not boundary, "carrier_translation_equal": translation_equal,
               "max_sparse_cells": max(len(s.cells) for s in states),
               "max_active_channels": max(sum(bool(c.a or c.b) for c in s.cells.values()) for s in states),
               "probes_sha256": digest(trace), "assembly_sha256": digest(plain(prepared.manifest))}
        results.append(row)
        if case["family"] != "carrier":
            current.append({**row, "states": states, "probes": trace})
            if len(current) == 4:
                comparisons.append(compare(protocol, current))
                current = []
        print(f"{index}/{protocol['family']['total_engine_cases']} {case['id']} cells={row['max_sparse_cells']}", flush=True)
    if len(results) != protocol["family"]["total_engine_cases"]:
        raise AssertionError("Wrong frozen case count")
    changed_sources = [name for name, sha in source_hashes.items()
                       if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != sha]
    if changed_sources:
        raise RuntimeError("Source/protocol changed during study: " + repr(changed_sources))
    summary = {"format": "universe24-interaction-evidence-v1", "protocol_sha256": protocol_hash,
               "checkout_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "source_sha256": source_hashes, "body_signs": protocol["body_signs"], "seed": None,
               "cases": results, "comparisons": comparisons,
               "strict_cancellation_groups": sum(any(c["strict_local_cancellation"].values()) for c in comparisons),
               "quiet_record_groups": sum(bool(c["quiet_remainder_records"]) for c in comparisons),
               "nonlinear_interaction_groups": sum(c["first_nonlinear_counter_interaction"] is not None for c in comparisons),
               "all_four_control_states_distinct": all(c["four_final_states_distinct"] for c in comparisons),
               "cpu_seconds": time.process_time()-started_cpu,
               "wall_seconds": time.monotonic()-started_wall,
               "interpretation": "Finite initial-data experiment. A vanished local signal is not deletion or quantum collapse; this study does not establish physical light, internal path enumeration, complexity selection, or entanglement."}
    save(output / "summary.json", summary)
    print(canonical({k: summary[k] for k in ("strict_cancellation_groups", "quiet_record_groups", "nonlinear_interaction_groups", "cpu_seconds", "wall_seconds")}), flush=True)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)
