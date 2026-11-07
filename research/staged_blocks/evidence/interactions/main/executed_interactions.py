"""Prospective full-board packet/clock interaction study; initial data only."""
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

from research.components import GuidedPacketSource, plain
from research.experiments.run import assemble, recorded_states, run_experiment
from research.presenter.export import bundle, state_sha256
from universe24 import Channel, Coupling, State
from universe24.core.group_2o import DIRECTIONS
from universe24.observation.clicks import clicks

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "interaction_protocol.json"


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(data):
    return hashlib.sha256(canonical(data).encode()).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n")


def geometry_cases(protocol):
    """Enumerate the complete registered family, independently of outcomes."""
    for stage in protocol["stages"]:
        for g, r, phase, direction in itertools.product(
                stage["guide_target_channels"], stage["clock_remainders"],
                stage["clock_phases"], stage["compensation_directions"]):
            suffix = "none" if direction is None else str(direction)
            yield {"id": f"{stage['name']}-g{g}-r{r}-p{phase}-d{suffix}",
                   "stage": stage["name"], "guide_target_channel": g,
                   "clock_remainder": r, "phase": phase,
                   "compensation_direction": direction}


def clock_geometry(protocol, case):
    geo = protocol["geometry"]
    center = (geo["clock_x"], geo["clock_y"], geo["clock_z"])
    coupling = Coupling(tuple(protocol["board"]["body_signs"]))
    channel = coupling.ports[2][case["guide_target_channel"]]
    nodes = (center, *(tuple(center[j]+d[j] for j in range(3)) for d in DIRECTIONS))
    return center, channel, nodes


def case_spec(case, protocol=None):
    """Pure seed recipe, consumable by the generic assembly/Presenter pipeline."""
    protocol = json.loads(PROTOCOL.read_text()) if protocol is None else protocol
    geo = protocol["geometry"]
    side = protocol["board"]["side"]
    coupling = Coupling(tuple(protocol["board"]["body_signs"]))
    center, h, nodes = clock_geometry(protocol, case)
    source_x = geo["packet_x"]
    cells = {(x, geo["row_y"], geo["row_z"], g): (0, 0, r)
             for x in range(side) if x not in range(source_x, source_x+4)
             for g, r in ((0, 0), (14, 4))}
    q = 1 if case["guide_target_channel"] == 0 else -1
    phase = case["phase"]
    ab = ((0, q), (q, 0), (0, -q), (-q, 0))[phase]
    if case["control"][1] == "0":
        ab = (0, 0)
    cells[(*center, h)] = (*ab, case["clock_remainder"])
    for d, xyz in enumerate(nodes[1:]):
        address = (*xyz, coupling.ports[d][h])
        base = (0 if q == 1 else 4) if d == 3 else 2
        if d == case["compensation_direction"]:
            base = 0 if q == 1 else 4
        r = base + (2*q*coupling.weights[d][h] if phase in (1, 2) else 0)
        if not 0 <= r < 6:
            raise ValueError("Registered joint clock halo is outside remainder domain")
        # This is an explicit joint initial-data definition before assembly.
        cells[address] = (0, 0, r)
    region = [(*xyz, g) for xyz in nodes for g in range(48)]
    ports = {"clock": [(*center, h)], "region": region,
             "forward": [(geo["forward_outlet_x"], geo["row_y"], geo["row_z"], g) for g in range(48)]}
    sockets = [{"name": f"packet-{x}", "addresses": [(x, geo["row_y"], geo["row_z"], g) for g in (0, 14)],
                "allowed_kinds": ["signal-source"]} for x in range(source_x, source_x+4)]
    identity = case["id"] + "-" + case["control"]
    return {"format": "universe24-assembly-experiment-v1", "id": identity,
            "title": "Prepared clock encounter: " + identity,
            "description": "Actual Rule3 packet/clock interaction on one fixed board. Complete matched source controls; transient arithmetic events are not capture or release.",
            "question": protocol["question"], "board": protocol["board"], "steps": protocol["steps"],
            "components": [
                {"name": "apparatus", "recipe": "Patch", "at": [0, 0, 0],
                 "params": {"kind": "joint-guide-clock", "cells": [[*a, *v] for a, v in sorted(cells.items())],
                            "ports": ports, "sources": {"clock": [(*center, h)]}, "sockets": sockets}},
                {"name": "packet", "recipe": "GuidedPacketSource",
                 "at": [source_x, geo["row_y"], geo["row_z"]],
                 "params": {"present": case["control"][0] == "1"}},
            ], "detectors": [], "view": {"port": "apparatus.clock"},
            "controls": case, "seed": None,
            "provenance": {"protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                           "preparation_only": True},
            "budget": {"max_frames": protocol["steps"]+1,
                       "max_cells": protocol["budget"]["max_cells_per_record"],
                       "max_bytes": 67108864,
                       "max_seconds": protocol["budget"]["max_seconds_per_record"]}}


def reverse_same_guide(state):
    """Exact full-state involution T(a,b,r)=(-b,-a,r); preparation/audit only."""
    return State(state.cube, state.background,
                 {address: Channel(-value.b, -value.a, value.r)
                  for address, value in state.cells.items()})


def _expected_packet(x, y, z, direction):
    cells = {(xx, y, z, g): Channel(0, 0, r)
             for xx in range(x-1, x+5) for g, r in ((0, 0), (14, 4))}
    for address, value in GuidedPacketSource().cells:
        value = value if direction == 1 else Channel(-value.b, -value.a, value.r)
        cells[(address[0]+x, address[1]+y, address[2]+z, address[3])] = value
    return {a: v for a, v in cells.items() if v != Channel(0, 0, 2)}


def packet_matches(state, x, y, z, direction):
    actual = {a: v for a, v in state.cells.items()
              if x-1 <= a[0] <= x+4 and abs(a[1]-y) <= 1 and abs(a[2]-z) <= 1}
    return actual == _expected_packet(x, y, z, direction)


def observe(protocol, case, prepared, states):
    center, h, nodes = clock_geometry(protocol, case)
    node_set = set(nodes)
    region = [(*xyz, g) for xyz in nodes for g in range(48)]
    region_trace = [[list(state.at(a)) for a in region] for state in states]
    center_trace = [list(state.at((*center, h))) for state in states]
    all_events, center_events, boundary, inputs = [], [], [], []
    for t, (old, new) in enumerate(zip(states, states[1:]), 1):
        events = [{"step": t, "address": list(event.address), "kind": event.kind,
                   "ell": event.quotient} for event in clicks(old, new, t)]
        all_events.extend(events)
        center_events.extend(e for e in events if tuple(e["address"]) == (*center, h))
        external = []
        for address, value in old.cells.items():
            if not value.b or address[:3] in node_set:
                continue
            for d in range(6):
                target = old.cube.adjacent(address, d, prepared.engine.coupling.ports[d][address[3]])
                if target[:3] in node_set:
                    external.append({"target": list(target), "source": list(address),
                                     "term": prepared.engine.coupling.weights[d][address[3]]*value.b})
        boundary.append({"update": t, "nonzero_external_terms": external})
        terms = []
        for d in range(6):
            donor = old.cube.adjacent((*center, h), d, prepared.engine.coupling.ports[d][h])
            terms.append({"source": list(donor), "term": prepared.engine.coupling.weights[d][h]*old.at(donor).b})
        inputs.append({"update": t, "terms": terms, "u": sum(v["term"] for v in terms)})
    candidates = []
    target_index = h  # center is the first complete node in region.
    for start in protocol["readouts"]["eligible_hold_starts"]:
        end = start + protocol["readouts"]["hold_updates"]
        if end >= len(states):
            continue
        isolation = all(not boundary[t]["nonzero_external_terms"] for t in range(start, end))
        if not isolation:
            continue
        frames = region_trace[start:end+1]
        ctr = center_trace[start:end+1]
        pairs = [(v[0]*v[0]+v[1]*v[1], v[2]) for v in ctr]
        periodic = all(frames[t] == frames[t+4] for t in range(len(frames)-4))
        others_quiet = all(not (v[0] or v[1]) for frame in frames
                           for i, v in enumerate(frame) if i != target_index)
        u_zero = all(inputs[t]["u"] == 0 for t in range(start, end))
        if (periodic and others_quiet and u_zero and len(set(pairs)) == 1
                and pairs[0][0] in (1, 2, 4) and pairs[0][1] in (0, 2, 4)):
            candidates.append({"kind": "retained_orbit", "start": start, "through": end,
                               "R": list(pairs[0])})
        if (all(not(v[0] or v[1]) for frame in frames for v in frame)
                and all(frame == frames[0] for frame in frames)
                and ctr[0][2] != center_trace[0][2]):
            candidates.append({"kind": "quiet_remainder", "start": start, "through": end,
                               "R": list(pairs[0])})
    carriers = []
    geo = protocol["geometry"]
    for direction, x in ((1, geo["forward_outlet_x"]), (-1, geo["backward_outlet_x"])):
        for start in range(18, len(states)-3):
            if all(packet_matches(states[start+k], x+direction*k, geo["row_y"], geo["row_z"], direction)
                   for k in range(4)):
                carriers.append({"start": start, "direction": direction, "outlet_x": x,
                                 "through": start+3, "full_local_template_equal": True})
    active_boundary = [{"step": t, "address": list(a)} for t, state in enumerate(states)
                       for a, v in state.cells.items()
                       if (v.a or v.b) and any(q in (0, state.cube.side-1) for q in a[:3])]
    return {"region_nodes": [list(n) for n in nodes], "region_addresses": [list(a) for a in region],
            "region_trace": region_trace, "center_address": [*center, h], "center_trace": center_trace,
            "center_inputs": inputs, "boundary_inputs": boundary, "all_C": all_events,
            "center_C": center_events, "candidate_holds": candidates, "outgoing_carriers": carriers,
            "active_boundary_hits": active_boundary}


def compare_group(rows):
    by = {r["case"]["control"]: r for r in rows}
    traces = {mask: r["observations"]["center_trace"] for mask, r in by.items()}
    nonlinear = []
    for t in range(len(traces["11"])):
        for j in (0, 1):
            predicted = traces["10"][t][j]+traces["01"][t][j]-traces["00"][t][j]
            if traces["11"][t][j] != predicted:
                nonlinear.append({"step": t, "component": "ab"[j], "actual": traces["11"][t][j],
                                  "linear_controls": predicted})
    bags = {mask: Counter((e["kind"], e["ell"]) for e in row["observations"]["center_C"])
            for mask, row in by.items()}
    novel = bags["11"] - (bags["10"] + bags["01"])
    retained = []
    for candidate in by["11"]["observations"]["candidate_holds"]:
        start, end = candidate["start"], candidate["through"]
        value = candidate["R"]
        if all([traces[mask][t][0]**2+traces[mask][t][1]**2, traces[mask][t][2]] != value
               for mask in ("10", "01") for t in range(start, end+1)):
            retained.append(candidate)
    states = {mask: row["states"] for mask, row in by.items()}
    addresses = set().union(*(s[0].cells for s in states.values()))
    same_remainders = all(len({s[0].at(a).r for s in states.values()}) == 1 for a in addresses)
    null_static = all(s == states["00"][0] for s in states["00"])
    clock_period4 = all(states["01"][t] == states["01"][t+4] for t in range(len(states["01"])-4))
    baseline_valid = same_remainders and null_static and clock_period4
    return {"geometry": {k: v for k, v in rows[0]["case"].items() if k != "control"},
            "matched_initial_remainders": same_remainders, "null_static": null_static,
            "clock_only_full_state_period4": clock_period4,
            "controlled_activation": bool(novel and nonlinear and baseline_valid),
            "novel_center_C_signatures": [[kind, ell, count] for (kind, ell), count in sorted(novel.items())],
            "first_nonlinear_center_counter": nonlinear[0] if nonlinear else None,
            "retained_records": retained if baseline_valid else [],
            "outgoing_carriers": {mask: r["observations"]["outgoing_carriers"] for mask, r in by.items()},
            "center_C_counts": {mask: sum(bag.values()) for mask, bag in bags.items()},
            "all_C_counts": {mask: len(r["observations"]["all_C"]) for mask, r in by.items()},
            "full_state_final_hashes": {mask: state_sha256(s[-1]) for mask, s in states.items()},
            "release_established": False,
            "release_scope": "This protocol does not test a subsequent interrogation or payload release."}


def presenter_selected(case):
    return (case["guide_target_channel"] == 0 and case["clock_remainder"] == 2
            and case["phase"] == 0
            and (case["stage"] == "base" or case["compensation_direction"] == 2))


def run(output, protocol_path=PROTOCOL):
    output = Path(output)
    protocol_bytes = Path(protocol_path).read_bytes()
    protocol = json.loads(protocol_bytes)
    output.mkdir(parents=True, exist_ok=False)
    (output/"records").mkdir()
    (output/"protocol.json").write_bytes(protocol_bytes)
    paths = [Path(__file__), PROTOCOL, *sorted((ROOT/"universe24").rglob("*.py")),
             *sorted((ROOT/"research/components").glob("*.py")), ROOT/"research/experiments/run.py",
             ROOT/"research/presenter/export.py"]
    source_hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    groups = list(geometry_cases(protocol))
    registration = {"format": "universe24-staged-interaction-registration-v1",
                    "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
                    "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                    "source_sha256": source_hashes, "geometries": groups,
                    "registered_cases": 4*len(groups), "seed": None,
                    "registered_before_capture": True}
    write_json(output/"registration.json", registration)
    start_cpu, start_wall = time.process_time(), time.monotonic()
    results, ledger, examples = [], [], []
    total_bytes = sum(p.stat().st_size for p in output.rglob("*") if p.is_file())
    stop_reason = None
    for index, geometry in enumerate(groups):
        if time.process_time()-start_cpu >= protocol["budget"]["max_cpu_seconds"]:
            stop_reason = "cpu_budget"
            break
        rows = []
        for mask in ("00", "10", "01", "11"):
            case = {**geometry, "control": mask}
            spec = case_spec(case, protocol)
            prepared = assemble(spec)
            recorded = run_experiment(spec)
            states = recorded_states(recorded["experiment"])
            observations = observe(protocol, case, prepared, states)
            if observations["active_boundary_hits"]:
                raise AssertionError("Active boundary return invalidates registered no-wrap horizon")
            rows.append({"case": case, "spec": spec, "assembly": recorded["assembly"],
                         "experiment": recorded["experiment"], "states": states,
                         "observations": observations})
        assessment = compare_group(rows)
        blobs = []
        for row in rows:
            wrapper = {"format": "universe24-staged-interaction-record-v1",
                       "spec": row["spec"], "assembly": row["assembly"],
                       "experiment": row["experiment"], "observations": row["observations"],
                       "assessment": assessment}
            raw = canonical(wrapper).encode()
            blobs.append((row, raw, gzip.compress(raw, mtime=0)))
        # Reserve room for the fixed replay subset and final machine-readable ledgers.
        if total_bytes + sum(len(blob) for _, _, blob in blobs) > protocol["budget"]["max_recorded_bytes"]-3000000:
            stop_reason = "recorded_data_budget"
            break
        for row, raw, compressed in blobs:
            identity = row["spec"]["id"]
            (output/"records"/(identity+".json.gz")).write_bytes(compressed)
            total_bytes += len(compressed)
            ledger.append({"id": identity, "case": row["case"], "record": "records/"+identity+".json.gz",
                           "record_sha256": hashlib.sha256(raw).hexdigest(),
                           "record_gzip_sha256": hashlib.sha256(compressed).hexdigest(),
                           "initial_state_sha256": state_sha256(row["states"][0]),
                           "final_state_sha256": state_sha256(row["states"][-1]),
                           "frames": len(row["states"]), "transitions": len(row["states"])-1,
                           "all_C_count": len(row["observations"]["all_C"]),
                           "candidate_holds": row["observations"]["candidate_holds"],
                           "outgoing_carriers": row["observations"]["outgoing_carriers"],
                           "full_state_inverse": row["experiment"]["provenance"]["full_rewind_equal"],
                           "no_active_boundary": True})
            if presenter_selected(row["case"]):
                examples.append(row["experiment"])
        results.append(assessment)
        print(f"{len(ledger)}/{registration['registered_cases']} {geometry['id']} activation={assessment['controlled_activation']} records={len(assessment['retained_records'])}", flush=True)
    if any(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != value for name, value in source_hashes.items()):
        raise RuntimeError("A registered execution source changed during the study")
    result = {"format": "universe24-staged-interaction-result-v1", "protocol_sha256": registration["protocol_sha256"],
              "status": "completed" if stop_reason is None else "budget_stopped", "stop_reason": stop_reason,
              "registered_cases": registration["registered_cases"], "completed_cases": len(ledger),
              "not_run_geometries": groups[len(results):], "groups": results, "cases": ledger,
              "controlled_activation_groups": sum(r["controlled_activation"] for r in results),
              "retained_orbit_groups": sum(any(c["kind"] == "retained_orbit" for c in r["retained_records"]) for r in results),
              "quiet_record_groups": sum(any(c["kind"] == "quiet_remainder" for c in r["retained_records"]) for r in results),
              "joint_outgoing_carrier_groups": sum(bool(r["outgoing_carriers"]["11"]) for r in results),
              "baseline_clock_period4_groups": sum(r["clock_only_full_state_period4"] for r in results),
              "release_established": False, "displayed_experiments": len(examples),
              "cpu_seconds": time.process_time()-start_cpu, "wall_seconds": time.monotonic()-start_wall,
              "scope": "Finite actual Rule3 trajectories. Activation, retained orbit, quiet record and outgoing carrier are separate predicates; no physical photon, path selection or release is inferred."}
    write_json(output/"result.json", result)
    write_json(output/"experiments.json", bundle(examples, title="The Presenter: packet and clock controls"))
    final_bytes = sum(p.stat().st_size for p in output.rglob("*") if p.is_file())
    if final_bytes > protocol["budget"]["max_recorded_bytes"]:
        raise RuntimeError("Final evidence exceeded its explicit recorded-data budget")
    print(canonical({k: result[k] for k in ("status", "completed_cases", "controlled_activation_groups",
                                           "retained_orbit_groups", "quiet_record_groups",
                                           "joint_outgoing_carrier_groups", "cpu_seconds")}), flush=True)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    return run(parser.parse_args(argv).output)


if __name__ == "__main__":
    main()
