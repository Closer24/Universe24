"""Independent complete-state audit of registered message-mechanism searches.

Read-only: exact matrix routing, scalar arithmetic and inverse are independent
of production tables and updater. Recorded observations never drive evolution.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import time

from research.component_review.audit import (
    Snapshot, advance, rewind, coupling_fingerprint,
)
from research.reference.algebra import DIRECTIONS, algebra, coupling

ROOT = Path(__file__).resolve().parents[2]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    path = Path(path)
    if not path.exists() and Path(str(path)+".gz").exists():
        path = Path(str(path)+".gz")
    data = path.read_bytes()
    return json.loads(gzip.decompress(data) if path.suffix == ".gz" else data)


def declared_initial(spec):
    """Rebuild supported data-only preparations without production assembly.

    Packet halo is derived by looking up the unique receiving matrix channel,
    not by copying the production sender-to-receiver lookup.
    """
    board = spec["board"]
    side = board["side"]
    signs = tuple(board.get("body_signs", (1, 1, 1)))
    reference = coupling(signs)
    matrices = algebra()
    cells = {}
    for component in spec["components"]:
        params, recipe = component.get("params", {}), component["recipe"]
        local = {}
        if recipe == "GuideSegment":
            pair = params.get("remainder_pair", (4, 0))
            local = {(x, 0, 0, g): (0, 0, r)
                     for x in range(params["start"], params["stop"]+1)
                     if x not in params.get("sockets", ())
                     for g, r in zip((0, 14), pair)}
        elif recipe == "Receiver":
            local = {(0, 0, 0, g): (*map(int, ab), r)
                     for g, ab, r in zip((0, 14),
                         params.get("counters", ((0, 0), (0, 0))),
                         params.get("remainders", (4, 0)))}
        elif recipe == "SignalSource":
            a, b = int(params.get("a", 0)), int(params.get("b", 1))
            if not params.get("present", True):
                a = b = 0
            local = {(0, 0, 0, g): (s*a, s*b, 2)
                     for g, s in ((0, 1), (14, -1))}
        elif recipe == "GuidedPacketSource":
            for x in range(4):
                a = {0: 1, 2: -1}.get(x, 0) if params.get("present", True) else 0
                b = {1: 1, 3: -1}.get(x, 0) if params.get("present", True) else 0
                local[(x, 0, 0, 0)] = (a, b, 4)
                local[(x, 0, 0, 14)] = (-a, -b, 0)
            for x in (1, 2):
                for direction in range(2, 6):
                    dx, dy, dz = DIRECTIONS[direction]
                    for sender, sign in ((0, 1), (14, -1)):
                        receivers = [g for g in range(48)
                                     if reference.ports[direction ^ 1][g] == sender]
                        assert len(receivers) == 1
                        receiver = receivers[0]
                        weight = reference.weights[direction ^ 1][receiver]
                        local[(x+dx, dy, dz, receiver)] = (0, 0, 2-2*sign*weight)
        elif recipe == "Patch":
            for row in params["cells"]:
                address = tuple(row[:4])
                assert address not in local, "Duplicate raw patch address"
                local[address] = tuple(map(int, row[4:]))
        else:
            raise AssertionError("Unreviewed recipe: " + recipe)
        orientation = component.get("orientation", 0)
        rotation = matrices.rotations[orientation]
        for address, value in local.items():
            xyz = [sum(rotation[i][j]*address[j] for j in range(3))
                   + component["at"][i] for i in range(3)]
            if component.get("wrap", False):
                xyz = [v % side for v in xyz]
            target = (*xyz, matrices.multiplication[orientation][address[3]])
            assert target not in cells or cells[target] == value, "Initial patch conflict"
            cells[target] = value
    return Snapshot(side, tuple(board.get("background", (0, 0, 2))), cells)


def snapshots(experiment):
    result = []
    for index, frame in enumerate(experiment["frames"]):
        assert frame["step"] == index, "Frame index mismatch"
        raw = {"side": experiment["side"], "background": experiment["background"],
               "cells": frame["cells"]}
        assert digest(raw) == frame["state_sha256"], "State hash mismatch"
        cells = {}
        for row in frame["cells"]:
            assert len(row) == 7
            address = tuple(row[:4])
            assert address not in cells, "Duplicate state address"
            cells[address] = tuple(map(int, row[4:]))
        result.append(Snapshot(experiment["side"], tuple(map(int, experiment["background"])), cells))
    return result


def input_terms(state, addresses, signs):
    reference = coupling(tuple(signs))
    terms, sums = [], []
    for x, y, z, channel in addresses:
        row = []
        for direction, (dx, dy, dz) in enumerate(DIRECTIONS):
            sender = ((x+dx) % state.side, (y+dy) % state.side,
                      (z+dz) % state.side, reference.ports[direction][channel])
            row.append({"direction": direction, "address": list(sender),
                        "weight": reference.weights[direction][channel],
                        "b": str(state.at(sender)[1])})
        terms.append(row)
        sums.append(sum(term["weight"]*int(term["b"]) for term in row))
    return sums, terms


def audit_experiment(experiment, spec, *, oracle=True):
    signs = tuple(spec["board"].get("body_signs", (1, 1, 1)))
    assert tuple(experiment["coupling"]["body_signs"]) == signs
    assert experiment["coupling"]["fingerprint"] == coupling_fingerprint(signs)
    states = snapshots(experiment)
    assert len(states) == spec["steps"]+1
    assert all(state.side == spec["board"]["side"] for state in states)
    assert states[0] == declared_initial(spec), "Independent initial preparation mismatch"
    if oracle:
        for index, (old, new) in enumerate(zip(states, states[1:]), 1):
            assert advance(old, signs) == new, ("Matrix forward mismatch", index)
            assert rewind(new, signs) == old, ("Matrix inverse mismatch", index)
        recovered = states[-1]
        for expected in reversed(states[:-1]):
            recovered = rewind(recovered, signs)
            assert recovered == expected, "Full reverse traversal mismatch"
        assert recovered == states[0]
    assert experiment["provenance"]["full_rewind_equal"] is True
    assert experiment["provenance"]["source_unchanged_during_capture"] is True
    return states


def receiver_observations(states, position, signs):
    addresses = [(*position, g) for g in range(48)]
    trace = [[list(state.at(a)) for a in addresses] for state in states]
    inputs_and_terms = [input_terms(state, addresses, signs) for state in states]
    inputs, terms = [row[0] for row in inputs_and_terms], [row[1] for row in inputs_and_terms]
    events = []
    for t, (before, after) in enumerate(zip(trace, trace[1:]), 1):
        for g, (old, new) in enumerate(zip(before, after)):
            quotient = old[0] + new[1]
            if quotient and old != new:
                events.append({"step": t, "channel": g, "ell": quotient})
    area = [[0]*48]
    for row in inputs[:-1]:
        area.append([a+b for a, b in zip(area[-1], row)])
    # Telescoping quotient identity holds in each actual receiver channel.
    for t in range(1, len(states)):
        for g in range(48):
            ell_sum = sum(trace[s-1][g][0]+trace[s][g][1] for s in range(1, t+1))
            assert trace[t][g][2]-trace[0][g][2] == 2*area[t][g]-6*ell_sum
    return {"trace": trace, "inputs": inputs, "terms": terms,
            "events": events, "input_area": area}


def check_recorded_observations(record, measured, detector="receiver.node"):
    assert record["detector_trace"] == measured["trace"], "Detector state mismatch"
    assert [[int(v) for v in row] for row in record["detector_input_trace"]] == measured["inputs"], "Detector input mismatch"
    if "detector_observations" in record:
        observations = record["detector_observations"][detector]["trace"]
        assert len(observations) == len(measured["trace"])
        for t, observed in enumerate(observations):
            assert observed["six_inputs"] == measured["terms"][t], "Six-term input mismatch"
            assert [[int(v) for v in row] for row in observed["detector"]] == measured["trace"][t]
            assert list(map(int, observed["next_input"])) == measured["inputs"][t]


def baseline_predicates(case, measured, *, start=13, stop=21):
    trace, events = measured["trace"], measured["events"]
    target = [(case["remainders"][0]-2) % 6, (case["remainders"][1]+2) % 6]
    target_failure = next((t for t in range(start, stop+1)
                           if [trace[t][0][2], trace[t][14][2]] != target), None)
    counter_failure = next((t for t in range(stop+1)
                            if any(a or b for a, b, r in trace[t])), None)
    other_failure = next((t for t in range(start, stop+1)
                          if any(trace[t][g][2] != trace[0][g][2]
                                 for g in range(48) if g not in (0, 14))), None)
    click_failure = next((event for event in events if event["step"] <= stop), None)
    return {"target_pair": target, "first_target_mismatch_state": target_failure,
            "first_nonzero_receiver_counter_state": counter_failure,
            "first_other_remainder_mismatch_state": other_failure,
            "first_disallowed_receiver_C": click_failure,
            "pending_accepted": bool(case["present"] and target != case["remainders"]
                and all(v is None for v in (target_failure, counter_failure, other_failure, click_failure)))}


def audit_baseline(folder):
    folder = Path(folder)
    protocol_hash = "9a397bfee30dcca86ff15c41085fa8182804b79ddf82cd9f959c9e93fa4c391f"
    protocol = load(folder/"protocol.json")
    registration = load(folder/"registration.json")
    summary = load(folder/"result.json")
    assert file_digest(folder/"protocol.json") == protocol_hash == registration["protocol_sha256"]
    assert file_digest(ROOT/"research/message_mechanism/protocol_baseline.json") == protocol_hash
    for path, expected in registration["source_sha256"].items():
        assert file_digest(ROOT/path) == expected, ("Source changed", path)
    assert protocol["steps"] == 24
    assert protocol["board"] == {"side": 129, "background": [0, 0, 2], "body_signs": [1, 1, 1]}
    expected_cases = [{"id": f"packet-r{r0}{r14}-{'on' if present else 'off'}",
                       "remainders": [r0, r14], "present": present}
                      for r0, r14, present in itertools.product((0, 2, 4), (0, 2, 4), (True, False))]
    assert registration["planned_cases"] == expected_cases
    assert len(summary["cases"]) == 18
    assert {p.name for p in (folder/"records").glob("*.json.gz")} == {c["id"]+".json.gz" for c in expected_cases}
    rows, initial_by_case = [], {}
    for case, reported in zip(expected_cases, summary["cases"]):
        path = folder/"records"/(case["id"]+".json.gz")
        record = load(path)
        assert file_digest(path) == reported["record_sha256"]
        assert record["case"] == reported["case"] == case
        assert record["spec"]["controls"] == case
        assert record["spec"]["board"] == protocol["board"]
        assert record["spec"]["steps"] == protocol["steps"]
        assert record["spec"]["provenance"]["protocol_sha256"] == protocol_hash
        assert record["spec"]["components"] == [
            {"name": "guide", "recipe": "GuideSegment", "at": [0, 64, 64],
             "params": {"start": 0, "stop": 128, "sockets": [32, 33, 34, 35, 48],
                        "remainder_pair": [0, 4]}},
            {"name": "source", "recipe": "GuidedPacketSource", "at": [32, 64, 64],
             "params": {"present": case["present"]}},
            {"name": "receiver", "recipe": "Receiver", "at": [48, 64, 64],
             "params": {"remainders": case["remainders"]}}], "Preparation differs from frozen geometry"
        states = audit_experiment(record["experiment"], record["spec"])
        initial_by_case[case["id"]] = states[0]
        measured = receiver_observations(states, protocol["apparatus"]["receiver"], (1, 1, 1))
        check_recorded_observations(record, measured)
        result = baseline_predicates(case, measured)
        assessment = record["assessment"]
        for key in ("target_pair", "first_target_mismatch_state", "first_nonzero_receiver_counter_state",
                    "first_disallowed_receiver_C", "pending_accepted"):
            assert result[key] == assessment[key], ("Registered predicate mismatch", case["id"], key)
        assert assessment["all48_clicks"] == measured["events"]
        assert assessment["cumulative_input_area"] == measured["input_area"]
        assert reported["assessment"] == assessment
        stationary = all(s == states[0] for s in states)
        translation = all(Snapshot(old.side, old.background,
            {((x+1) % old.side, y, z, g): value for (x, y, z, g), value in old.cells.items()}) == new
            for old, new in zip(states, states[1:]))
        assert stationary == reported["stationary"]
        assert translation == reported["translation_every_step"]
        if not case["present"]:
            assert stationary
        if case["id"] == "packet-r04-on":
            assert translation
        boundary_counter = any(any(v[:2]) and any(coordinate in (0, 128) for coordinate in address[:3])
                               for state in states for address, v in state.cells.items())
        assert not boundary_counter, "Nonzero counter reached periodic boundary"
        rows.append({"id": case["id"], **result, "states": len(states),
                     "transitions": len(states)-1, "full_rewind_equal": True,
                     "stationary": stationary, "exact_translation": translation,
                     "all48_C_events": measured["events"], "record_sha256": file_digest(path),
                     "no_nonzero_counter_at_periodic_boundary": True})
    for r0, r14 in itertools.product((0, 2, 4), repeat=2):
        on = initial_by_case[f"packet-r{r0}{r14}-on"]
        off = initial_by_case[f"packet-r{r0}{r14}-off"]
        changed = {a for a in set(on.cells) | set(off.cells) if on.at(a) != off.at(a)}
        assert changed == {(x, 64, 64, g) for x in range(32, 36) for g in (0, 14)}
        assert all(on.at(a)[2] == off.at(a)[2] and off.at(a)[:2] == (0, 0) for a in changed)
    assert sum(row["pending_accepted"] for row in rows) == summary["pending_accepted"]
    return {"passed": True, "protocol_sha256": protocol_hash, "runs": 18,
            "complete_states": 450, "independent_forward_transitions": 432,
            "independent_inverse_transitions": 432, "full_reverse_traversals": 18,
            "pending_accepted": sum(row["pending_accepted"] for row in rows),
            "all18_full48_states_inputs_and_six_terms_checked": True,
            "all9_source_ablations_preserve_remainders_and_halo": True,
            "no_wrap_checked": True, "cases": rows}


def interaction_spec(protocol, case):
    """Independent declaration of the complementary guides and J packet."""
    side, geo = protocol["side"], protocol["geometry"]
    y, z, left = geo["y"], geo["z"], geo["left_source_x"]
    board = {"side": side, "background": [0, 0, 2], "body_signs": [1, 1, 1]}
    def packet(name, x, present, reverse=False):
        part = {"name": name, "recipe": "GuidedPacketSource", "at": [x, y, z], "params": {"present": present}}
        if not reverse:
            return part
        state = declared_initial({"board": board, "components": [{**part, "at": [0, y, z]}]})
        return {"name": name, "recipe": "Patch", "at": [x, y, z],
                "params": {"kind": "signal-source", "cells": [[a, b-y, c-z, g, bb, aa, 4-r]
                    for (a, b, c, g), (aa, bb, r) in sorted(state.cells.items())]}}
    def guide(name, start, stop, sockets, pair):
        return {"name": name, "recipe": "GuideSegment", "at": [0, y, z],
                "params": {"start": start, "stop": stop, "sockets": sockets, "remainder_pair": pair}}
    if case["family"] == "carrier":
        reverse = case["direction"] == -1
        components = [guide("guide", 0, side-1, list(range(left, left+4)), [4, 0] if reverse else [0, 4]),
                      packet("source", left, True, reverse)]
        steps = 8
    else:
        right = geo["right_source_x_before_delay"]+case["delay"]
        components = [guide("left-guide", 0, 63, list(range(left, left+4)), [0, 4]),
                      guide("right-guide", 65, side-1, list(range(right, right+4)), [4, 0]),
                      {"name": "seam", "recipe": "Receiver", "at": [64, y, z], "params": {"remainders": case["seam"]}},
                      packet("left-source", left, case["control"][0] == "1"),
                      packet("right-source", right, case["control"][1] == "1", True)]
        steps = 32
    return {"board": board, "components": components, "steps": steps}


def interaction_probes(states):
    result = {}
    for x in (56, 63, 64, 65, 72):
        measured = receiver_observations(states, [x, 64, 64], (1, 1, 1))
        nodes = measured["trace"]
        events = []
        for event in measured["events"]:
            t, g = event["step"], event["channel"]
            events.append({**event, "kind": ((nodes[t][g][2]-nodes[t-1][g][2])//2) % 3})
        inputs = [{"step": t, "pair": [
            {"channel": g, "signed_terms": [v["weight"]*int(v["b"]) for v in measured["terms"][t-1][g]],
             "u": measured["inputs"][t-1][g], "ell": nodes[t-1][g][0]+nodes[t][g][1]}
            for g in (0, 14)]} for t in range(1, len(states))]
        windows = []
        if x in (63, 64, 65):
            for t in range(12, len(states)-8):
                if (all(v[:2] == [0, 0] for v in nodes[t])
                        and [nodes[t][g][2] for g in (0, 14)] != [nodes[0][g][2] for g in (0, 14)]
                        and all(nodes[k] == nodes[t] for k in range(t, t+9))):
                    windows.append({"start": t, "through": t+8, "pair": [nodes[t][g][2] for g in (0, 14)]})
        result[str(x)] = {"position": [x, 64, 64], "nodes": nodes, "events": events,
                          "inputs": inputs, "pair_outbound_C": [e for e in events if 20 <= e["step"] <= 32 and e["channel"] in (0, 14)],
                          "quiet_windows_before_null_comparison": windows}
    return result


def interaction_comparison(group):
    counts = {mask: {name: len(row["probes"][str(x)]["pair_outbound_C"])
                    for name, x in (("left", 56), ("right", 72))} for mask, row in group.items()}
    final_states = [row["states"][-1] for row in group.values()]
    distinct = all(a != b for a, b in itertools.combinations(final_states, 2))
    cancelled = {side: bool(counts[single][side] and not counts[other][side]
                    and not counts["00"][side] and not counts["11"][side]
                    and group[single]["states"][-1] != group["11"]["states"][-1])
                 for side, single, other in (("left", "01", "10"), ("right", "10", "01"))}
    quiet = []
    for mask in ("00", "10", "01", "11"):
        if mask == "00":
            continue
        for x in (63, 64, 65):
            probe = group[mask]["probes"][str(x)]
            null = group["00"]["probes"][str(x)]
            for window in probe["quiet_windows_before_null_comparison"]:
                if all(probe["nodes"][t] != null["nodes"][t] for t in range(window["start"], window["through"]+1)):
                    quiet.append({"control": mask, "x": x, **window})
    nonlinear = None
    for t in range(33):
        states = {mask: row["states"][t] for mask, row in group.items()}
        for address in sorted(set().union(*(state.cells for state in states.values()))):
            for c in (0, 1):
                expected = states["10"].at(address)[c]+states["01"].at(address)[c]-states["00"].at(address)[c]
                actual = states["11"].at(address)[c]
                if actual != expected:
                    nonlinear = {"step": t, "address": list(address), "component": "ab"[c],
                                 "actual11": actual, "linear_control_combination": expected}
                    break
            if nonlinear:
                break
        if nonlinear:
            break
    return {"outbound_pair_C_counts": counts, "strict_local_cancellation": cancelled,
            "quiet_remainder_records": quiet, "four_final_states_distinct": distinct,
            "first_nonlinear_counter_interaction": nonlinear,
            "center_pair_input_waveforms": {mask: [p["pair"] for p in row["probes"]["64"]["inputs"]]
                                             for mask, row in group.items()}}


def audit_interactions(folder):
    folder = Path(folder)
    protocol_hash = "49f06de82b605e1bf22eeea5d073ef43fd70ceb9d1e23a2b63e0ccab1bba912c"
    protocol, summary = load(folder/"protocol.json"), load(folder/"summary.json")
    assert file_digest(folder/"protocol.json") == summary["protocol_sha256"] == protocol_hash
    for path, expected in summary["source_sha256"].items():
        assert file_digest(ROOT/path) == expected, ("Interaction source changed", path)
    expected_cases = [{"id": "carrier-right" if d == 1 else "carrier-left", "family": "carrier", "direction": d} for d in (1, -1)]
    for family, delays in (("discovery", (0, 2, 4)), ("holdout", (1, 3))):
        expected_cases += [{"id": f"seam-{seam[0]}-{seam[1]}-delay-{delay}-{mask}", "family": family,
                            "seam": list(seam), "delay": delay, "control": mask}
                           for seam, delay, mask in itertools.product(((0, 4), (2, 2), (4, 0)), delays, ("00", "10", "01", "11"))]
    assert [row["case"] for row in summary["cases"]] == expected_cases
    assert {p.name for p in (folder/"records").glob("*.json.gz")} == {c["id"]+".json.gz" for c in expected_cases}
    group, rows, comparisons = {}, [], []
    for case, row in zip(expected_cases, summary["cases"]):
        path = folder/"records"/(case["id"]+".json.gz")
        e = load(path)
        assert file_digest(path) == row["record_gzip_sha256"]
        assert digest(e) == row["record_sha256"]
        assert e["provenance"]["interaction_case"] == case
        assert e["provenance"]["interaction_protocol_sha256"] == protocol_hash
        states = audit_experiment(e, interaction_spec(protocol, case))
        manifest = load(folder/"assemblies"/(case["id"]+".json"))
        assert digest(manifest) == row["assembly_sha256"], "Lossless assembly content hash mismatch"
        manifest_state = Snapshot(129, (0, 0, 2), {tuple(v[:4]): tuple(v[4:]) for v in manifest["raw_assignments"]})
        assert manifest_state == states[0], "Assembly manifest differs from independent initial state"
        observed = interaction_probes(states)
        assert observed == load(folder/"probes"/(case["id"]+".json")), ("Interaction probe mismatch", case["id"])
        assert digest(observed) == row["probes_sha256"]
        assert not any(any(v[:2]) and any(c in (0, 128) for c in a[:3]) for state in states for a, v in state.cells.items())
        if case["family"] == "carrier":
            for t, state in enumerate(states):
                expected = Snapshot(129, (0, 0, 2), {((x+case["direction"]*t) % 129, y, z, g): value
                                     for (x, y, z, g), value in states[0].cells.items()})
                assert state == expected
        else:
            group[case["control"]] = {"states": states, "probes": observed}
            if len(group) == 4:
                null = group["00"]["states"][0]
                assert all(s == null for s in group["00"]["states"])
                for mask, entry in group.items():
                    initial = entry["states"][0]
                    differences = {a for a in set(initial.cells) | set(null.cells) if initial.at(a) != null.at(a)}
                    expected_diff = set()
                    for bit, x in zip(mask, (48, 77+case["delay"])):
                        if bit == "1":
                            expected_diff |= {(u, 64, 64, g) for u in range(x, x+4) for g in (0, 14)}
                    assert differences == expected_diff
                    assert all(initial.at(a)[2] == null.at(a)[2] for a in differences)
                measured = interaction_comparison(group)
                original = summary["comparisons"][len(comparisons)]
                for key, value in measured.items():
                    assert original[key] == value, ("Interaction comparison mismatch", case["id"], key)
                eligible = {side: bool(measured["outbound_pair_C_counts"][single][side]
                    and not measured["outbound_pair_C_counts"][other][side]
                    and not measured["outbound_pair_C_counts"]["00"][side])
                    for side, single, other in (("left", "01", "10"), ("right", "10", "01"))}
                witnesses = {}
                for single in ("10", "01"):
                    a, b = group[single]["states"][-1], group["11"]["states"][-1]
                    address = next(address for address in sorted(set(a.cells) | set(b.cells)) if a.at(address) != b.at(address))
                    witnesses[single] = {"address": list(address), "single_final": list(a.at(address)), "joint_final": list(b.at(address))}
                comparisons.append({"family": case["family"], "seam": case["seam"], "delay": case["delay"],
                                    **{k: v for k, v in measured.items() if k != "center_pair_input_waveforms"},
                                    "control_eligible_for_strict_cancellation": eligible,
                                    "final_information_difference_witnesses": witnesses})
                group = {}
        rows.append({"id": case["id"], "states": len(states), "transitions": len(states)-1,
                     "record_sha256": file_digest(path), "full_rewind_equal": True})
    return {"passed": True, "protocol_sha256": protocol_hash, "runs": 62,
            "complete_states": sum(row["states"] for row in rows),
            "independent_forward_transitions": sum(row["transitions"] for row in rows),
            "independent_inverse_transitions": sum(row["transitions"] for row in rows),
            "full_reverse_traversals": 62, "all48_probe_states_and_pair_inputs_checked": True,
            "source_counter_only_controls_verified": True, "carrier_translation_both_directions": True,
            "strict_cancellation_groups": sum(any(row["strict_local_cancellation"].values()) for row in comparisons),
            "control_eligible_groups": sum(any(row["control_eligible_for_strict_cancellation"].values()) for row in comparisons),
            "joint_quiet_outlet_groups": sum(any(row["outbound_pair_C_counts"]["11"][side] == 0 for side in ("left", "right")) for row in comparisons),
            "lossless_probe_and_assembly_canonical_hashes_verified": True,
            "quiet_record_groups": sum(bool(row["quiet_remainder_records"]) for row in comparisons),
            "nonlinear_interaction_groups": sum(row["first_nonlinear_counter_interaction"] is not None for row in comparisons),
            "all_four_control_states_distinct": all(row["four_final_states_distinct"] for row in comparisons),
            "comparisons": comparisons, "cases": rows}


def discovery_cases():
    pairs = list(itertools.product((0, 2, 4), repeat=2))
    result = [{"id": f"row3-{index:03d}", "family": "row3",
               "row_pairs": [[x, list(pair)] for x, pair in zip((45, 46, 47), values)]}
              for index, values in enumerate(itertools.product(pairs, repeat=3))]
    for x in (47, 46):
        result.extend({"id": f"side{x}-{index:03d}", "family": f"side{x}",
                       "row_pairs": [[47, list(row)]], "side_x": x, "side_pair": list(side)}
                      for index, (row, side) in enumerate(itertools.product(pairs, repeat=2)))
    return result


def discovery_spec(case, present=True):
    components = [
        {"name": "guide", "recipe": "GuideSegment", "at": [0, 64, 64],
         "params": {"start": 0, "stop": 128, "sockets": [32, 33, 34, 35, 48]+[x for x, pair in case["row_pairs"]], "remainder_pair": [0, 4]}},
        {"name": "source", "recipe": "GuidedPacketSource", "at": [32, 64, 64], "params": {"present": present}},
        {"name": "receiver", "recipe": "Receiver", "at": [48, 64, 64], "params": {"remainders": [4, 2]}}]
    components.extend({"name": f"converter-{x}", "recipe": "Receiver", "at": [x, 64, 64], "params": {"remainders": pair}}
                      for x, pair in case["row_pairs"])
    if "side_pair" in case:
        channels = [coupling((1, 1, 1)).ports[2][g] for g in (0, 14)]
        components.append({"name": "side-converter", "recipe": "Patch", "at": [case["side_x"], 65, 64],
            "params": {"kind": "receiver", "cells": [[0, 0, 0, g, 0, 0, r] for g, r in zip(channels, case["side_pair"])],
                       "ports": {"node": [[0, 0, 0, g] for g in range(48)]}}})
    return {"board": {"side": 129, "background": [0, 0, 2], "body_signs": [1, 1, 1]},
            "steps": 40, "components": components}


def discovery_predicates(trace, inputs):
    assert len(trace) == len(inputs) == 41
    events = []
    for t in range(41):
        assert len(trace[t]) == len(inputs[t]) == 48
        assert all(len(v) == 3 and 0 <= v[2] < 6 and all(type(a) is int for a in v) for v in trace[t])
        if t:
            for g in range(48):
                old, new = trace[t-1][g], trace[t][g]
                ell, r = divmod(2*inputs[t-1][g]+old[2], 6)
                assert new == [old[1], ell-old[0], r], "Recorded receiver violates scalar update with recorded actual input"
                if ell and old != new:
                    events.append({"step": t, "channel": g, "ell": ell})
    target = [[0, 0, 2] for _ in range(48)]
    target[14][2] = 4
    clicks = {e["step"] for e in events}
    quiet = [all(v[0] == v[1] == 0 for v in node) for node in trace]
    writes = [t for t in range(13, 25) if all(quiet[:t+9])
              and not any(c <= t+8 for c in clicks) and all(trace[s] == target for s in range(t, t+9))]
    longest, best = 0, None
    for t in range(13, 25):
        if not all(quiet[:t+1]) or any(c <= t for c in clicks):
            continue
        length = 0
        for k in range(t, 41):
            if trace[k] != target or not quiet[k] or k in clicks:
                break
            length += 1
        if length > longest:
            longest, best = length, t
    return {"accepted": bool(writes), "accepted_write_state": writes[0] if writes else None,
            "maximum_quiet_target_states_before_C": longest, "best_target_start": best,
            "first_receiver_C": events[0] if events else None, "all48_C": events,
            "remainder_pairs": [[v[0][2], v[14][2]] for v in trace],
            "pair_actual_inputs": [[u[0], u[14]] for u in inputs],
            "final_input_area": [sum(row[g] for row in inputs[:-1]) for g in range(48)]}


def audit_discovery(folder):
    folder = Path(folder)
    protocol_hash = "53691277c609f7b1edbba3d31e0a24d0dbf65c9804e08661095754fa1ad0caa6"
    registration, summary = load(folder/"registration.json"), load(folder/"result.json")
    assert file_digest(folder/"protocol.json") == registration["protocol_sha256"] == summary["protocol_sha256"] == protocol_hash
    for path, expected in registration["source_sha256"].items():
        assert file_digest(ROOT/path) == expected, ("Discovery source changed", path)
    assert file_digest(folder/"ledger.jsonl.gz") == summary["ledger_sha256"]
    cases = discovery_cases()
    assert registration["planned_cases"] == cases
    rows = [json.loads(line) for line in gzip.decompress((folder/"ledger.jsonl.gz").read_bytes()).splitlines()]
    assert len(rows) == len(cases) == 891
    by_id = {}
    for case, row in zip(cases, rows):
        assert row["case"] == case and row["status"] == "completed"
        assert row["all_step_inverses_equal"] is True
        measured = discovery_predicates(row["receiver_trace"], row["actual_input_trace"])
        assert measured == row["assessment"], ("Discovery predicate mismatch", case["id"])
        by_id[case["id"]] = row
    accepted = [row["case"] for row in rows if row["assessment"]["accepted"]]
    assert summary["discovery_acceptances"] == accepted
    full_records = []
    retained_ids = set()
    for reported in summary["retained_records"]:
        path = folder/reported["record"]
        assert file_digest(path) == reported["record_sha256"]
        record = load(path)
        case, spec = record["case"], record["spec"]
        present = spec["controls"]["present"]
        expected = discovery_spec(case, present)
        for key in ("board", "steps", "components"):
            assert spec[key] == expected[key], ("Discovery preparation mismatch", key)
        if present:
            assert digest(spec) == by_id[case["id"]]["spec_sha256"]
        states = audit_experiment(record["experiment"], spec)
        measured = receiver_observations(states, [48, 64, 64], (1, 1, 1))
        check_recorded_observations(record, measured)
        assert discovery_predicates(measured["trace"], measured["inputs"]) == record["assessment"]
        if present:
            assert record["assessment"] == by_id[case["id"]]["assessment"]
            assert digest(states[-1].canonical()) == by_id[case["id"]]["final_state_sha256"]
            retained_ids.add(case["id"])
        else:
            assert all(state == states[0] for state in states)
        full_records.append({"id": spec["id"], "states": 41, "transitions": 40,
                             "record_sha256": file_digest(path), "full_rewind_equal": True})
    assert {case["id"] for case in accepted} <= retained_ids
    # Sampling rule declared to the producer before any discovery trajectories.
    sample_ids = sorted(row["case"]["id"] for row in rows if not row["assessment"]["accepted"])[:16]
    samples = []
    for identifier in sample_ids:
        row = by_id[identifier]
        states = [declared_initial(discovery_spec(row["case"]))]
        for t in range(40):
            states.append(advance(states[-1]))
            assert rewind(states[-1]) == states[-2]
        measured = receiver_observations(states, [48, 64, 64], (1, 1, 1))
        assert measured["trace"] == row["receiver_trace"]
        assert measured["inputs"] == row["actual_input_trace"]
        assert digest(states[-1].canonical()) == row["final_state_sha256"]
        current = states[-1]
        for expected in reversed(states[:-1]):
            current = rewind(current)
            assert current == expected
        samples.append({"id": identifier, "re_evolved_states": 41, "transitions": 40,
                        "full_final_digest_matches": True, "all48_receiver_inputs_match": True,
                        "full_rewind_equal": True})
    return {"passed": True, "protocol_sha256": protocol_hash,
            "all891_stored_receiver_scalar_updates_and_frozen_predicates_recomputed": True,
            "independently_validated_new_components": 0, "accepted_candidates": len(accepted),
            "retained_full_records": full_records,
            "complete_retained_states": 41*len(full_records),
            "retained_matrix_forward_transitions": 40*len(full_records),
            "retained_matrix_inverse_transitions": 40*len(full_records),
            "fresh_re_evolution_sample_rule": "Lexicographically first16 failed candidate IDs, declared before discovery runs",
            "fresh_re_evolution_samples": samples,
            "fresh_re_evolution_forward_transitions": 640, "fresh_re_evolution_inverse_transitions": 640,
            "scope": "All891 receiver ledgers checked arithmetically; complete dynamics independently replayed only for all retained records and16 predeclared failed samples. Unsampled intermediate whole-board states were not retained and are not claimed independently audited.",
            "holdouts": "None triggered: no discovery acceptance. A future hit requires newly frozen geometry, amplitude/sign perturbations and source controls."}


def reverse_endpoint_spec(case):
    packet, compensation = case["packet_x"], case["compensation_x"]
    return {"format": "universe24-assembly-experiment-v1", "id": case["id"]+"-endpoint",
            "board": {"side": 129, "background": [0, 0, 2], "body_signs": [1, 1, 1]}, "steps": 0,
            "components": [
                {"name": "guide", "recipe": "GuideSegment", "at": [0, 64, 64],
                 "params": {"start": 0, "stop": 128, "sockets": list(range(packet, packet+4))+[48, compensation], "remainder_pair": [0, 4]}},
                {"name": "packet", "recipe": "GuidedPacketSource", "at": [packet, 64, 64]},
                {"name": "receiver", "recipe": "Receiver", "at": [48, 64, 64], "params": {"remainders": [2, 4]}},
                {"name": "compensation", "recipe": "Receiver", "at": [compensation, 64, 64], "params": {"remainders": case["compensation_pair"]}}]}


def in_source_box(address):
    return 8 <= address[0] <= 40 and 48 <= address[1] <= 80 and 48 <= address[2] <= 80


def reverse_preparation_metrics(initial):
    receiver = [list(initial.at((48, 64, 64, g))) for g in range(48)]
    ready = [[0, 0, 2] for _ in range(48)]
    ready[0][2] = 4
    active = [a for a, v in initial.cells.items() if any(v[:2])]
    outside = [a for a in active if not in_source_box(a)]
    distance = min((sum(min(abs(a[d]-r), 129-abs(a[d]-r))
                        for d, r in enumerate((48, 64, 64))) for a in active), default=None)
    return {"initial_receiver": receiver,
            "initial_receiver_mismatches": sum(a != b for a, b in zip(receiver, ready)),
            "initial_active_channels": len(active), "source_box_violations": len(outside),
            "minimum_source_distance": distance,
            "initial_admissible": receiver == ready and bool(active) and not outside}


def reverse_predicates(preparation, measured):
    trace, inputs, events = measured["trace"], measured["inputs"], measured["events"]
    target = [[0, 0, 2] for _ in range(48)]
    target[14][2] = 4
    assert len(trace) == len(inputs) == 41
    area = [sum(row[g] for row in inputs[:32]) for g in range(48)]
    first = next((t for t, node in enumerate(trace) if node != trace[0]), None)
    checks = {"initial_admissible": preparation["initial_admissible"],
              "quiet_all48_prefix": all(all(v[:2] == [0, 0] for v in node) for node in trace),
              "no_receiver_C": not events,
              "target_retained32_through40": all(node == target for node in trace[32:]),
              "actual_pair_input_area": [area[0], area[14]] == [-1, 1],
              "causal_first_change": first is not None and preparation["minimum_source_distance"] is not None
                  and first >= preparation["minimum_source_distance"]}
    return {"checks": checks, "accepted": all(checks.values()), "first_receiver_change": first,
            "all48_C": events, "remainder_pairs": [[v[0][2], v[14][2]] for v in trace],
            "input_area_through32": area}


def audit_reverse(folder):
    folder = Path(folder)
    protocol_hash = "b426034d184a50e50e21722dae8773a19fc4d45f760ba05bf8796189eedb9221"
    registration, summary = load(folder/"registration.json"), load(folder/"result.json")
    ledger = load(folder/"preparation_ledger.json")
    assert file_digest(folder/"protocol.json") == registration["protocol_sha256"] == summary["protocol_sha256"] == protocol_hash
    for path, expected in registration["source_sha256"].items():
        assert file_digest(ROOT/path) == expected, ("Reverse search source changed", path)
    cases = [{"id": f"reverse-{i:03d}", "packet_x": x, "compensation_x": c, "compensation_pair": [a, b]}
             for i, (x, c, a, b) in enumerate(itertools.product((52, 56, 60), (47, 49), (0, 2, 4), (0, 2, 4)))]
    assert registration["planned_cases"] == cases
    assert len(ledger) == len(cases) == 54
    assert {p.name for p in (folder/"preparations").glob("*.json.gz")} == {c["id"]+".json.gz" for c in cases}
    initials, endpoints, metrics_by_id, preparation_rows = {}, {}, {}, []
    for case, row in zip(cases, ledger):
        assert row["case"] == case
        path = folder/row["preparation_record"]
        assert file_digest(path) == row["preparation_record_sha256"]
        record = load(path)
        endpoint_spec = reverse_endpoint_spec(case)
        assert record["endpoint_spec"] == endpoint_spec
        assert record["source_box_inclusive"] == [[8, 40], [48, 80], [48, 80]]
        endpoint = declared_initial(endpoint_spec)
        state, inverse_hashes = endpoint, [digest(endpoint.canonical())]
        for t in range(32):
            previous = rewind(state)
            assert advance(previous) == state
            state = previous
            inverse_hashes.append(digest(state.canonical()))
        assert inverse_hashes == row["inverse_state_sha256"], ("Independent inverse-preparation hash mismatch", case["id"])
        assert digest(state.canonical()) == row["initial_state_sha256"] == record["initial_state_sha256"]
        stored = Snapshot(129, (0, 0, 2), {tuple(v[:4]): tuple(v[4:]) for v in record["initial_cells"]})
        assert len(record["initial_cells"]) == len(stored.cells) and state == stored
        assert inverse_hashes[0] == row["endpoint_state_sha256"]
        metrics = reverse_preparation_metrics(state)
        for key, value in metrics.items():
            assert row[key] == value, ("Preparation eligibility mismatch", case["id"], key)
        initials[case["id"]], endpoints[case["id"]], metrics_by_id[case["id"]] = state, endpoint, metrics
        preparation_rows.append({"id": case["id"], **{k: v for k, v in metrics.items() if k != "initial_receiver"},
                                 "initial_state_sha256": inverse_hashes[-1], "inverse_steps": 32})
    best = min(ledger, key=lambda row: (row["initial_receiver_mismatches"], row["source_box_violations"], row["case"]["id"]))
    expected_retained = {row["case"]["id"] for row in ledger if row["initial_admissible"]}
    expected_retained |= {cases[0]["id"], best["case"]["id"]}
    expected_ids = {identifier+suffix for identifier in expected_retained for suffix in ("-on", "-source-box-off")}
    assert {row["id"] for row in summary["records"]} == expected_ids
    assert {p.name for p in (folder/"records").glob("*.json.gz")} == {identifier+".json.gz" for identifier in expected_ids}
    records, accepted = [], []
    for row in summary["records"]:
        path = folder/row["record"]
        assert file_digest(path) == row["record_sha256"]
        record = load(path)
        case, spec = record["case"], record["spec"]
        identifier, present = case["id"], spec["controls"]["present"]
        initial = initials[identifier]
        if not present:
            initial = Snapshot(129, (0, 0, 2), {a: (0, 0, v[2]) if in_source_box(a) else v for a, v in initial.cells.items()})
        assert spec["steps"] == 40 and spec["board"] == reverse_endpoint_spec(case)["board"]
        states = audit_experiment(record["experiment"], spec)
        assert states[0] == initial, "Source-box control changed outside triples or remainders"
        assert digest(states[0].canonical()) == digest(initial.canonical())
        if present:
            assert states[32] == endpoints[identifier], "Forward replay missed its constructed endpoint"
        measured = receiver_observations(states, [48, 64, 64], (1, 1, 1))
        check_recorded_observations(record, measured)
        assessment = reverse_predicates(metrics_by_id[identifier], measured)
        assert assessment == record["assessment"] == row["assessment"]
        if present and assessment["accepted"]:
            accepted.append(identifier)
        stationary = all(state == states[0] for state in states)
        assert stationary == row["stationary"]
        if not present and metrics_by_id[identifier]["initial_admissible"]:
            assert stationary
        records.append({"id": row["id"], "states": 41, "transitions": 40,
                        "stationary": stationary, "assessment": assessment,
                        "record_sha256": file_digest(path), "full_rewind_equal": True})
    assert accepted == summary["accepted_discoveries"]
    admissible = sum(row["initial_admissible"] for row in preparation_rows)
    assert admissible == summary["initial_admissible_count"]
    return {"passed": True, "protocol_sha256": protocol_hash, "preparations": 54,
            "independent_inverse_preparation_steps": 1728,
            "independent_forward_checks_of_inverse_preparation": 1728,
            "all54_full_initial_states_and33_hash_inverse_histories_verified": True,
            "initial_admissible": admissible, "accepted_discoveries": len(accepted),
            "retained_full_records": len(records), "retained_complete_states": 41*len(records),
            "retained_forward_transitions": 40*len(records), "retained_inverse_transitions": 40*len(records),
            "all_source_box_off_controls_preserve_every_remainder_and_outside_triple": True,
            "endpoint_return_is_a_construction_identity_not_success": True,
            "preparation_rows": preparation_rows, "records": records,
            "scope": "External inverse search only. Runtime recordings contain forward Rule3; no approval or cancellation component follows from reconstructing a chosen endpoint."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--interactions", type=Path)
    parser.add_argument("--discovery", type=Path)
    parser.add_argument("--reverse", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    started = time.process_time()
    report = {"format": "universe24-independent-message-audit-v1", "passed": True,
              "oracle": "Independent exact4x4 matrix coupling with explicit scalar forward and inverse arithmetic",
              "not_claimed": ["physical light", "all possibilities explored", "quantum entanglement", "complexity selection"]}
    if args.baseline:
        report["baseline"] = audit_baseline(args.baseline)
    if args.interactions:
        report["interactions"] = audit_interactions(args.interactions)
    if args.discovery:
        report["discovery"] = audit_discovery(args.discovery)
    if args.reverse:
        report["reverse_preparation"] = audit_reverse(args.reverse)
    report["cpu_seconds"] = time.process_time()-started
    report["audit_source_sha256"] = file_digest(__file__)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
    print(canonical({key: value for key, value in report.items() if key not in ("baseline", "interactions", "discovery", "reverse_preparation")}))


if __name__ == "__main__":
    main()
