"""Independent, passive audits for staged Rule3 building-block research.

This module uses exact matrix routing and its own complete-state scalar oracle.
It never supplies runtime inputs, modifies an experiment, or chooses an outcome.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import gzip
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import re
import resource
import signal
import subprocess
import time

from research.component_review.audit import (
    Snapshot, advance, rewind, coupling_fingerprint, transition_events,
)
from research.message_mechanism.audit import declared_initial as previous_initial
from research.message_mechanism.audit import input_terms
from research.reference.algebra import DIRECTIONS, algebra, coupling

ROOT = Path(__file__).resolve().parents[2]
BASE_COMMIT = "b552f90d"
DECIMAL = re.compile(r"(?:0|-[1-9][0-9]*|[1-9][0-9]*)\Z")
_REPLAY_PROGRESS = {"complete_dynamical_records": 0, "complete_states": 0, "forward_inverse_transitions": 0}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    path = Path(path)
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)


def exact_int(value):
    if type(value) is int:
        return value
    if type(value) is str and DECIMAL.fullmatch(value):
        return int(value)
    raise AssertionError("Noncanonical exact integer")


def declared_initial(spec):
    """Independent initial preparation, extended only for reviewed recipes."""
    board = spec["board"]
    if "tensor" not in board:
        return previous_initial(spec)
    tensor = board["tensor"]
    signs = tuple(tensor["body_signs"])
    matrix = coupling(signs)
    assert tensor["model_id"] == "universe24-2O-body-013-v1"
    assert tensor["ports"] == [list(row) for row in matrix.ports]
    assert tensor["weights"] == [list(row) for row in matrix.weights]
    assert tensor["fingerprint"] == coupling_fingerprint(signs)
    return previous_initial({**spec, "board": {"side": board["side"],
        "background": board.get("background", [0, 0, 2]), "body_signs": list(signs)}})


def read_states(experiment):
    background = tuple(exact_int(v) for v in experiment["background"])
    states = []
    for t, frame in enumerate(experiment["frames"]):
        assert frame["step"] == t, "Nonconsecutive frame"
        raw = {"side": experiment["side"], "background": experiment["background"], "cells": frame["cells"]}
        assert digest(raw) == frame["state_sha256"], "State digest mismatch"
        cells, previous = {}, None
        for row in frame["cells"]:
            assert len(row) == 7
            address = tuple(row[:4])
            assert previous is None or previous < address, "State addresses not sorted and unique"
            previous = address
            triple = tuple(exact_int(v) for v in row[4:])
            assert triple != background, "Redundant explicit background channel"
            cells[address] = triple
        states.append(Snapshot(experiment["side"], background, cells))
    assert states, "Empty complete recording"
    return states


def audit_tensor(experiment, signs):
    tensor, expected = experiment["coupling"], coupling(tuple(signs))
    assert tensor["model"] == "universe24-2O-body-013-v1"
    assert tensor["body_signs"] == list(signs)
    assert tensor["directions"] == [list(v) for v in DIRECTIONS]
    assert tensor["ports"] == [list(v) for v in expected.ports], "Recorded ports differ from matrix algebra"
    assert tensor["weights"] == [list(v) for v in expected.weights], "Recorded weights differ from matrix algebra"
    assert tensor["fingerprint"] == coupling_fingerprint(tuple(signs))


def all_events(states):
    events, changes = [], []
    for t, (old, new) in enumerate(zip(states, states[1:]), 1):
        addresses = sorted(set(old.cells) | set(new.cells))
        for address in addresses:
            before, after = old.at(address), new.at(address)
            if before[2] != after[2]:
                changes.append({"step": t, "address": list(address), "before_r": before[2], "after_r": after[2]})
            quotient = before[0]+after[1]
            if quotient and before != after:
                events.append({"step": t, "address": list(address),
                               "kind": ((after[2]-before[2])//2) % 3,
                               "quotient": str(quotient)})
    return events, changes


def audit_observations(states, signs, observations):
    """Recompute all saved observer values; no channel or C class is suppressed."""
    reports = {}
    for name, saved in observations.items():
        addresses = [tuple(a) for a in saved["addresses"]]
        assert len(addresses) == len(set(addresses))
        assert len(saved["trace"]) == len(states)
        events, change_times = [], []
        for t, (state, row) in enumerate(zip(states, saved["trace"])):
            assert row["step"] == t
            triples = [state.at(a) for a in addresses]
            assert [[exact_int(v) for v in triple] for triple in row["detector"]] == [list(v) for v in triples]
            assert row["memory"] == [v[2] for v in triples]
            assert [exact_int(v) for v in row["magnitude"]] == [a*a+b*b for a, b, r in triples]
            inputs, terms = input_terms(state, addresses, signs)
            assert [exact_int(v) for v in row["next_input"]] == inputs, "Actual input sum mismatch"
            assert row["six_inputs"] == terms, "Actual six-port contributions mismatch"
            current_events = []
            if t:
                old = states[t-1]
                if any(old.at(a)[2] != state.at(a)[2] for a in addresses):
                    change_times.append(t)
                for address in addresses:
                    before, after = old.at(address), state.at(address)
                    quotient = before[0]+after[1]
                    if quotient and before != after:
                        current_events.append({"step": t, "address": list(address),
                                               "kind": ((after[2]-before[2])//2) % 3,
                                               "quotient": str(quotient)})
            assert row["arithmetic_events"] == current_events, "A recorded arithmetic C was hidden or changed"
            events.extend(current_events)
        assert saved["arithmetic_events"] == events
        assert saved["record_event_times"] == change_times
        reports[name] = {"addresses": len(addresses), "C_events": len(events),
                         "C_by_kind": dict(sorted(Counter(e["kind"] for e in events).items())),
                         "R_change_times": change_times}
    return reports


def source_control(on, off, allowed_counter_addresses):
    """Ablation changes only declared source counters, never passive apparatus."""
    assert on.side == off.side and on.background == off.background
    allowed = set(map(tuple, allowed_counter_addresses))
    changes = []
    for address in set(on.cells) | set(off.cells):
        a, b = on.at(address), off.at(address)
        assert a[2] == b[2], "Source ablation changed an apparatus remainder"
        if address not in allowed:
            assert a == b, "Source ablation changed undeclared apparatus counters"
        else:
            assert b[:2] == (0, 0), "Declared absent source counters are not zero"
        if a != b:
            changes.append(address)
    return sorted(changes)


def audit_record(record, *, expected_initial=None, deadline=None):
    spec, experiment = record["spec"], record["experiment"]
    board = spec["board"]
    signs = tuple(board.get("body_signs", board.get("tensor", {}).get("body_signs", (1, 1, 1))))
    assert len(signs) == 3 and all(type(s) is int and s in (-1, 1) for s in signs)
    audit_tensor(experiment, signs)
    states = read_states(experiment)
    assert len(states) == spec["steps"]+1
    assert all(state.side == spec["board"]["side"] for state in states)
    independent_initial = declared_initial(spec)
    assert states[0] == independent_initial, "Independent initial preparation mismatch"
    if expected_initial is not None:
        assert states[0] == expected_initial, "Initial state violates registered preparation"
    for t, (old, new) in enumerate(zip(states, states[1:]), 1):
        if deadline is not None and time.process_time() > deadline:
            raise TimeoutError("Independent audit CPU budget exhausted")
        assert advance(old, signs) == new, ("Independent forward mismatch", t)
        assert rewind(new, signs) == old, ("Independent inverse mismatch", t)
    current = states[-1]
    for expected in reversed(states[:-1]):
        current = rewind(current, signs)
        assert current == expected, "Full backward traversal mismatch"
    assert experiment["provenance"]["full_rewind_equal"] is True
    assert experiment["provenance"]["source_unchanged_during_capture"] is True
    observations = record.get("observations", record.get("detector_observations", {}))
    observed = audit_observations(states, signs, observations)
    events, changes = all_events(states)
    if "assembly" in record:
        assembly = record["assembly"]
        raw = assembly["raw_assignments"]
        assert len({tuple(v[:4]) for v in raw}) == len(raw)
        state = Snapshot(states[0].side, states[0].background,
                         {tuple(v[:4]): tuple(exact_int(x) for x in v[4:]) for v in raw})
        assert state == states[0], "Assembly manifest differs from independent preparation"
        assert assembly["runtime_callbacks"] is False
    boundary = [{"step": t, "address": list(address)} for t, state in enumerate(states)
                for address, value in state.cells.items() if any(value[:2])
                and any(v in (0, state.side-1) for v in address[:3])]
    _REPLAY_PROGRESS["complete_dynamical_records"] += 1
    _REPLAY_PROGRESS["complete_states"] += len(states)
    _REPLAY_PROGRESS["forward_inverse_transitions"] += len(states)-1
    return {"passed": True, "states": len(states), "forward_transitions": len(states)-1,
            "inverse_transitions": len(states)-1, "full_rewind_equal": True,
            "whole_board_C_count": len(events), "whole_board_C_sha256": digest(events),
            "whole_board_C_by_kind": dict(sorted(Counter(e["kind"] for e in events).items())),
            "whole_board_R_change_count": len(changes), "whole_board_R_sha256": digest(changes),
            "initial_state_sha256": digest(states[0].canonical()),
            "final_state_sha256": digest(states[-1].canonical()),
            "boundary_counter_hits": boundary, "observations": observed}, states


def synthesis_initial(protocol, values=None, present=True):
    values = [2]*22 if values is None else list(values)
    assert len(values) == 22 and all(type(v) is int and v in (0, 2, 4) for v in values)
    receiver, source = protocol["receiver"], protocol["source"]
    spec = {"board": protocol["board"], "components": [
        {"name": "guide", "recipe": "GuideSegment", "at": [0, *receiver[1:]],
         "params": {"start": 0, "stop": 48, "sockets": [17, 18, 19, 20, 21, 22, 23, 24], "remainder_pair": [0, 4]}},
        {"name": "source", "recipe": "GuidedPacketSource", "at": source, "params": {"present": present}},
        {"name": "receiver", "recipe": "Receiver", "at": receiver, "params": {"remainders": [4, 2]}},
        {"name": "apparatus", "recipe": "Patch", "at": [0, 0, 0],
         "params": {"kind": "receiver", "cells": [[*a, 0, 0, r]
                    for a, r in zip(protocol["unknown_remainder_addresses"], values)]}}]}
    return previous_initial(spec)


def synthesis_cones(protocol):
    """Independent matrix-derived dependency proof for the registered Pilot A."""
    assert protocol["board"] == {"side": 49, "body_signs": [1, 1, 1], "background": [0, 0, 2]}
    assert protocol["source"] == [17, 24, 24] and protocol["receiver"] == [24, 24, 24]
    assert protocol["steps"] == 12 and protocol["pending_states"] == [4, 12]
    assert protocol["ready_pair"] == [4, 2] and protocol["pending_pair"] == [2, 4]
    assert protocol["allowed_remainders"] == [0, 2, 4]
    matrix = coupling((1, 1, 1))
    assert protocol["tensor"]["ports"] == [list(row) for row in matrix.ports]
    assert protocol["tensor"]["weights"] == [list(row) for row in matrix.weights]
    assert protocol["tensor"]["fingerprint"] == coupling_fingerprint((1, 1, 1))
    addresses = [(x, 24, 24, g) for x in (21, 22, 23) for g in (0, 14)]
    for x in (22, 23):
        for d in range(2, 6):
            dx, dy, dz = DIRECTIONS[d]
            for sender in (0, 14):
                receiving = [g for g in range(48) if matrix.ports[d ^ 1][g] == sender]
                assert len(receiving) == 1
                addresses.append((x+dx, 24+dy, 24+dz, receiving[0]))
    assert protocol["unknown_remainder_addresses"] == [list(a) for a in addresses]
    initial, absent = synthesis_initial(protocol), synthesis_initial(protocol, present=False)
    assert all(value[:2] == (0, 0) for value in absent.cells.values())
    active = {a for a, v in initial.cells.items() if any(v[:2])}
    source_control(initial, absent, [(x, 24, 24, g) for x in range(17, 21) for g in (0, 14)])
    inverse = [{sender: receiver for receiver, sender in enumerate(row)} for row in matrix.ports]
    forward = [active]
    for t in range(12):
        affected = set(forward[-1])
        for x, y, z, sender in forward[-1]:
            for d, (dx, dy, dz) in enumerate(DIRECTIONS):
                affected.add(((x-dx) % 49, (y-dy) % 49, (z-dz) % 49, inverse[d][sender]))
        forward.append(affected)
    receiver_addresses = {(24, 24, 24, g) for g in range(48)}
    needed = [set(receiver_addresses) for _ in range(13)]
    for t in reversed(range(1, 13)):
        needed[t] &= forward[t]
        for x, y, z, g in needed[t]:
            needed[t-1].add((x, y, z, g))
            for d, (dx, dy, dz) in enumerate(DIRECTIONS):
                needed[t-1].add(((x+dx) % 49, (y+dy) % 49, (z+dz) % 49, matrix.ports[d][g]))
    needed[0] &= forward[0]
    # Every state actually used by a retained update is either retained itself
    # or has the proved exact stationary initial triple outside influence.
    for t in range(1, 13):
        for x, y, z, g in needed[t]:
            parents = {(x, y, z, g)} | {((x+dx) % 49, (y+dy) % 49, (z+dz) % 49, matrix.ports[d][g])
                         for d, (dx, dy, dz) in enumerate(DIRECTIONS)}
            assert parents & forward[t-1] <= needed[t-1]
    details = {"source_active_addresses": [list(a) for a in sorted(active)],
               "forward_counts": list(map(len, forward)), "dependency_counts": list(map(len, needed)),
               "encoded_channel_updates": sum(map(len, needed[1:])),
               "forward_sets_sha256": [digest(sorted(s)) for s in forward],
               "dependency_sets_sha256": [digest(sorted(s)) for s in needed],
               "complete_receiver_observations": {"channels": 48, "states": list(range(13))},
               "source_off_stationary_for_every_apparatus_assignment": True,
               "stationary_proof": "Outside possible influence, a=b=u=0 and any r in0..5 give quotient0 and unchanged r. An arbitrary initial remainder alone cannot create activity.",
               "independent_matrix_dependencies": True, "closure_verified": True,
               "solver_result_reviewed": False}
    assert details["encoded_channel_updates"] == 24776
    return initial, forward, needed, details


def audit_synthesis_query(protocol, query_path):
    """Compare every saved assertion with a fresh independent matrix encoding.

    This checks the submitted formula, not the correctness of a SAT solver or
    the validity of an UNSAT proof certificate. No search is performed here.
    """
    import z3
    initial, forward, needed, details = synthesis_cones(protocol)
    scaled = "equivalent_to" in protocol
    matrix = coupling((1, 1, 1))
    unknowns = {tuple(a): z3.Int(("initial_s_" if scaled else "initial_r_")+"_".join(map(str, a))) for a in protocol["unknown_remainder_addresses"]}
    assertions = ([constraint for r in unknowns.values() for constraint in (r >= 0, r <= 2)] if scaled
                  else [z3.Or(*(r == v for v in (0, 2, 4))) for r in unknowns.values()])
    states = {}
    def at(t, address):
        if not t or address not in forward[t]:
            a, b, r = initial.at(address)
            if scaled:
                assert r % 2 == 0
                r //= 2
            return z3.IntVal(a), z3.IntVal(b), unknowns.get(address, z3.IntVal(r))
        assert address in needed[t]
        return states[(t, address)]
    for t in range(1, 13):
        for address in sorted(needed[t]):
            x, y, z, g = address
            old = at(t-1, address)
            incoming = z3.Sum([matrix.weights[d][g]*at(t-1,
                ((x+dx) % 49, (y+dy) % 49, (z+dz) % 49, matrix.ports[d][g]))[1]
                for d, (dx, dy, dz) in enumerate(DIRECTIONS)])
            name = "on_"+str(t)+"_"+"_".join(map(str, address))
            b, r = z3.Int(name+"_b"), z3.Int(name+("_s" if scaled else "_r"))
            equation = 3*(b+old[0])+r == incoming+old[2] if scaled else 6*(b+old[0])+r == 2*incoming+old[2]
            assertions.extend((equation, r >= 0, r < (3 if scaled else 6)))
            states[(t, address)] = old[1], b, r
    for t in range(13):
        for g in range(48):
            address = (24, 24, 24, g)
            a, b, r = at(t, address)
            if scaled:
                r = 2*r
            assertions.extend((a == 0, b == 0))
            if t >= 4:
                assertions.append(r == (4 if g == 14 else 2))
            if t:
                previous = at(t-1, address)
                if scaled:
                    previous = previous[0], previous[1], 2*previous[2]
                assertions.append(z3.Not(z3.And(b+previous[0] != 0,
                    z3.Or(previous[0] != a, previous[1] != b, previous[2] != r))))
    absent = synthesis_initial(protocol, present=False)
    for t in range(13):
        for g in range(48):
            a, b, r = absent.at((24, 24, 24, g))
            assertions.extend((z3.IntVal(a) == 0, z3.IntVal(b) == 0, z3.IntVal(r) == (4 if g == 0 else 2)))
    raw = gzip.decompress(Path(query_path).read_bytes()).decode()
    actual = z3.parse_smt2_string(raw)
    assert len(actual) == len(assertions), "Submitted SMT assertion count differs"
    normalized = 0
    for i, (saved, expected) in enumerate(zip(actual, assertions)):
        if not saved.eq(expected):
            # SMT-LIB represents negative integer literals as unary minus;
            # normalize this and ordinary exact arithmetic on both sides.
            assert z3.simplify(saved).eq(z3.simplify(expected)), ("Submitted SMT assertion differs from independent encoding", i)
            normalized += 1
    return {"passed": True, "query_sha256": file_digest(query_path), "assertions_checked": len(assertions),
            "encoded_channel_updates": details["encoded_channel_updates"],
            "assertions_requiring_exact_arithmetic_normalization": normalized,
            "solver_version": z3.get_version_string(), "search_performed": False,
            "encoding": "even-remainder-bijection" if scaled else "original-remainder",
            "independent_unsat_proof_certificate_checked": False,
            "scope": "Every saved assertion equals an independently constructed exact matrix-derived Rule3, domain, receiver or stationary-control assertion; solver correctness is a separate assumption."}


def orbit_cases():
    vectors = [v for v in itertools.product(range(-2, 3), repeat=2) if abs(v[0])+abs(v[1]) <= 2]
    cases = []
    for i, (signs, channel) in enumerate(itertools.product(itertools.product((-1, 1), repeat=3), range(48))):
        side, (a, b) = (3, 5, 9)[i % 3], vectors[i % 13]
        cases.append({"id": f"orbit-label-{i:03d}", "family": "labels", "side": side,
                      "location": [0, side-1, channel % side], "body_signs": list(signs),
                      "channel": channel, "a": a, "b": b, "r": i % 6, "phase": i % 4, "present": True})
    for i, ((a, b), r, phase) in enumerate(itertools.product(vectors, range(6), range(4))):
        cases.append({"id": f"orbit-values-{i:03d}", "family": "values", "side": 5,
                      "location": [2, 2, 2], "body_signs": [1, -1, 1] if i % 2 else [1, 1, 1],
                      "channel": i % 48, "a": a, "b": b, "r": r, "phase": phase, "present": True})
    for phase, r in itertools.product(range(4), range(6)):
        matching = (vectors.index((1, 0))*6+r)*4+phase
        cases.append({"id": f"orbit-off-p{phase}-r{r}", "family": "off", "side": 5,
                      "location": [2, 2, 2], "body_signs": [1, -1, 1] if matching % 2 else [1, 1, 1], "channel": matching % 48,
                      "a": 1, "b": 0, "r": r, "phase": phase, "present": False})
    for d, field, delta in itertools.product(range(6), ("r", "b"), (-1, 1)):
        cases.append({"id": f"orbit-disturb-d{d}-{field}{delta:+d}", "family": "disturbance", "side": 9,
                      "location": [4, 4, 4], "body_signs": [1, 1, 1], "channel": 0,
                      "a": 1, "b": 0, "r": 2, "phase": 0, "present": True,
                      "disturbance": {"direction": d, "field": field, "delta": 2*delta if field == "r" else delta}})
    return cases


def orbit_state(case, step=0, *, disturbed=False):
    """Exact isolated formula; halo recipients are solved from receiver routing."""
    a, b, side = case["a"], case["b"], case["side"]
    phase = (case["phase"]+step) % 4 if case["present"] else case["phase"]
    x, y, z = case["location"]
    channel = case["channel"]
    center = (x, y, z, channel)
    aa, bb = ((a, b), (b, -a), (-a, -b), (-b, a))[phase] if case["present"] else (0, 0)
    cells = {center: (aa, bb, case["r"])}
    matrix = coupling(tuple(case["body_signs"]))
    prefixes = (0, b, b-a, -a, 0)
    recipients = []
    for d, (dx, dy, dz) in enumerate(DIRECTIONS):
        candidates = [g for g in range(48) if matrix.ports[d ^ 1][g] == channel]
        assert len(candidates) == 1
        recipient = candidates[0]
        weight = matrix.weights[d ^ 1][recipient]
        possible = [r for r in (0, 2, 4) if all(0 <= r+2*weight*u < 6 for u in prefixes)]
        assert possible, "No independent passive halo remainder exists"
        base_r = min(possible, key=lambda r: (abs(r-2), r))
        address = ((x+dx) % side, (y+dy) % side, (z+dz) % side, recipient)
        cells[address] = (0, 0, base_r+2*weight*prefixes[phase])
        recipients.append(address)
    if disturbed and "disturbance" in case:
        assert step == 0
        perturbation = case["disturbance"]
        address = recipients[perturbation["direction"]]
        value = list(cells[address])
        index = {"a": 0, "b": 1, "r": 2}[perturbation["field"]]
        value[index] += perturbation["delta"]
        if index == 2:
            value[index] %= 6
        cells[address] = tuple(value)
    return Snapshot(side, (0, 0, 2), cells), recipients


def audit_orbit(folder, *, deadline=None):
    folder = Path(folder)
    protocol_hash = "2558e39c4d728b1b9ed18f3f04f090b2666efc4b3ea758b1c9821daba30890bf"
    summary = load(folder/"result.json")
    registration = load(folder/"registration.json")
    assert file_digest(folder/"protocol.json") == registration["protocol_sha256"] == protocol_hash
    assert summary["registration"] == registration
    for path, sha in registration["source_sha256"].items():
        assert file_digest(ROOT/path) == sha, ("Orbit execution source changed", path)
    cases = orbit_cases()
    assert registration["cases"] == cases and len(cases) == 744
    assert {p.name for p in (folder/"records").glob("*.json.gz")} == {c["id"]+".json.gz" for c in cases}
    rows, disturbances = [], []
    for case, reported in zip(cases, summary["cases"]):
        assert case == reported["case"]
        path = folder/"records"/(case["id"]+".json.gz")
        assert file_digest(path) == reported["record_sha256"]
        record = load(path)
        assert record["case"] == case and record["spec"]["controls"] == case
        assert record["spec"]["steps"] == 8
        expected, halo = orbit_state(case, disturbed=True)
        replay, states = audit_record(record, expected_initial=expected, deadline=deadline)
        mismatch = next((t for t, state in enumerate(states) if state != orbit_state(case, t)[0]), None)
        period = next((t for t in range(1, 5) if states[t] == states[0]), None)
        expected_period = 4 if case["present"] and (case["a"] or case["b"]) else 1
        raw_events, _ = all_events(states)
        events = [{"step": e["step"], "address": e["address"], "kind": e["kind"], "ell": int(e["quotient"])} for e in raw_events]
        center = (*case["location"], case["channel"])
        samples = [{"step": t, "center": list(state.at(center)),
                    "center_all48": [list(state.at((*case["location"], g))) for g in range(48)],
                    "halo": [list(state.at(a)) for a in halo],
                    "center_magnitude": sum(v*v for v in state.at(center)[:2]),
                    "noncenter_counter_addresses": [list(a) for a, v in sorted(state.cells.items()) if a != center and any(v[:2])]}
                   for t, state in enumerate(states)]
        assessment = record["assessment"]
        assert assessment["first_full_state_formula_mismatch"] == mismatch
        assert assessment["minimal_return_at_most_four"] == period
        assert assessment["expected_period"] == expected_period
        assert assessment["all_world_C"] == events and assessment["samples"] == samples
        passed = mismatch is None and period == expected_period and not events
        assert assessment["isolated_contract_passed"] == reported["isolated_contract_passed"] == passed
        assert assessment["signal_written_memory_established"] is False
        if case["family"] != "disturbance":
            assert passed, ("Isolated preparation violates registered formula", case["id"])
        else:
            disturbances.append({"id": case["id"], "initial_formula_mismatch": mismatch,
                                 "minimal_return_at_most_four": period, "C_events": len(events),
                                 "noncenter_activity_observed": any(s["noncenter_counter_addresses"] for s in samples),
                                 "interpretation": "Mismatch at state0 is built into the perturbation, not by itself a dynamical instability test."})
        if case["family"] == "off":
            on, _ = orbit_state({**case, "present": True})
            source_control(on, states[0], [center])
            assert all(s == states[0] for s in states)
        rows.append({"id": case["id"], "family": case["family"], "record_sha256": file_digest(path),
                     "replay_passed": True, "formula_passed": passed,
                     "states": len(states), "forward_inverse_transitions": len(states)-1,
                     "C_events": len(events), "minimal_return_at_most_four": period})
    assert len(summary["cases"]) == 744
    assert summary["unperturbed_passed"] == 720
    return {"passed": True, "kind": "orbit", "protocol_sha256": protocol_hash,
            "full_recordings_independently_replayed": 744, "complete_states": 6696,
            "forward_transitions": 5952, "inverse_transitions": 5952, "full_reverse_traversals": 744,
            "prepared_orbit_formula_passed": 720, "disturbance_cases": 24,
            "independent_receiver_halo_construction": True,
            "source_off_same_halo_stationary_controls": 24,
            "scope": "All744 registered joint preparations; finite sampling is not the full Cartesian product of every sign/channel/vector/remainder/phase/side. Exact isolated formula is checked separately from incoming capture.",
            "incoming_capture_established": False, "boundary_scope": "Periodic wrapping is intentional for label-family placements; no no-wrap claim is made.",
            "disturbances": disturbances, "records": rows}


def composition_initial(arrangement, present):
    receiver = [16, 16, 24] if arrangement == "isolated" else [16, 8, 16]
    spec = {"board": {"side": 33, "body_signs": [1, 1, 1]}, "components": [
        {"name": "guide", "recipe": "GuideSegment", "at": [0, 8, 16],
         "params": {"start": 0, "stop": 32, "sockets": [4, 5, 6, 7]+([16] if arrangement == "connected" else []), "remainder_pair": [0, 4]}},
        {"name": "carrier", "recipe": "GuidedPacketSource", "at": [4, 8, 16], "params": {"present": present}},
        {"name": "memory", "recipe": "Receiver", "at": receiver, "params": {"remainders": [4, 2]}}]}
    prepared = previous_initial(spec)
    clock = orbit_state({"a": 1, "b": 0, "r": 2, "phase": 0, "present": True,
                         "side": 33, "body_signs": [1, 1, 1], "location": [16, 24, 16], "channel": 0})[0]
    cells = dict(prepared.cells)
    for address, triple in clock.cells.items():
        assert address not in cells or cells[address] == triple
        cells[address] = triple
    return Snapshot(33, (0, 0, 2), cells)


def audit_composition(folder, *, deadline=None):
    folder = Path(folder)
    summary, protocol = load(folder/"result.json"), load(folder/"protocol.json")
    protocol_hash = digest(protocol)
    assert protocol_hash in ("d8a29c5ba027ea1e88f5833ae2dc09d15a8e66fb48701b6fdc9050164078b7f8", "3b47d20ab17498c67501f7428a553ddc5593db9c851fc70c25d975ada28962d1", "fdc3e66f8b239faf994d05b521d93709a856017be0b9b80eda6d163093f4942e")
    assert protocol_hash == summary["protocol_sha256"]
    for name, expected in summary["source_sha256"].items():
        if file_digest(ROOT/name) != expected:
            assert name == "research/staged_blocks/stages.json", ("Composition execution source changed", name)
            assert expected in {file_digest(p) for p in (ROOT/'research/staged_blocks/evidence/catalog_history').glob('*.json')}
    if not protocol_hash.startswith('d8a29'):
        original = ROOT/'research/staged_blocks/evidence/composition'
        old_protocol = load(original/'protocol.json')
        assert {k: v for k, v in protocol.items() if k != 'catalog_sha256'} == {k: v for k, v in old_protocol.items() if k != 'catalog_sha256'}
        certificate = load(folder/'catalog_equivalence.json')
        for row in certificate['records']:
            name = 'records/'+row['id']+'.json.gz'
            old, new = load(original/name), load(folder/name)
            assert file_digest(original/name) == row['original_record_sha256']
            assert file_digest(folder/name) == row.get('reviewed_catalog_record_sha256', row.get('current_record_sha256'))
            assert old['experiment']['frames'] == new['experiment']['frames'] and old['assessment'] == new['assessment']
    expected_ids = [f"four-blocks-{arrangement}-{control}"
                    for arrangement, control in itertools.product(("isolated", "connected"), ("on", "off"))]
    assert [spec["id"] for spec in protocol["cases"]] == expected_ids
    assert set(summary["records"]) == {"records/"+identifier+".json.gz" for identifier in expected_ids}
    clock_positions = {(16, 24, 16)} | {(16+dx, 24+dy, 16+dz) for dx, dy, dz in DIRECTIONS}
    clock_addresses = sorted((*p, g) for p in clock_positions for g in range(48))
    grouped, rows = {}, []
    for spec in protocol["cases"]:
        path = folder/"records"/(spec["id"]+".json.gz")
        record = load(path)
        assert record["spec"] == spec
        arrangement, present = spec["controls"]["arrangement"], spec["controls"]["carrier_present"]
        expected = composition_initial(arrangement, present)
        replay, states = audit_record(record, expected_initial=expected, deadline=deadline)
        receiver = (16, 16, 24) if arrangement == "isolated" else (16, 8, 16)
        trace = [[state.at((*receiver, g)) for g in range(48)] for state in states]
        clocks = [tuple(state.at(a) for a in clock_addresses) for state in states]
        assert len(set(clocks[:4])) == 4, "Clock has a proper divisor of the claimed four-cycle"
        period4 = all(value == clocks[t % 4] for t, value in enumerate(clocks))
        all_c, _ = all_events(states)
        receiver_c = [event for event in all_c if tuple(event["address"][:3]) == receiver]
        target = [(0, 0, 2)]*48
        target[14] = (0, 0, 4)
        pending = (all(row == target for row in trace[9:18])
            and all(not any(v[:2]) for row in trace[:18] for v in row)
            and not any(e["step"] <= 17 for e in receiver_c))
        measured = {"prepared_clock_full_region_period4": period4,
                    "clock_initial_state_repeats_at4": clocks[4] == clocks[0],
                    "receiver_stays_at_initial_record": all(row == trace[0] for row in trace),
                    "first_receiver_change": next((t for t, row in enumerate(trace) if row != trace[0]), None),
                    "strict_zero_counter_pending_goal": pending,
                    "pending_write_state": 9, "pending_last_required_state": 17,
                    "all_arithmetic_events": all_c, "arithmetic_classes_retained": [0, 1, 2],
                    "receiver_arithmetic_events": receiver_c,
                    "signal_capture_proven": False, "approval_release_demonstrated": False, "physical_photon_claim": False}
        if arrangement == "isolated":
            lane = ((8, 16), (7, 16), (9, 16), (8, 15), (8, 17))
            translation = all(state.at((x, y, z, g)) == states[0].at(((x-(t if present else 0)) % 33, y, z, g))
                for t, state in enumerate(states) for x in range(33) for y, z in lane for g in range(48))
            measured["carrier_translation_or_stationary_off_control"] = translation
            assert translation and period4 and measured["receiver_stays_at_initial_record"]
        assert measured == record["assessment"], ("Composition assessment mismatch", spec["id"])
        grouped[(arrangement, present)] = {"states": states, "receiver": trace, "clock": clocks}
        rows.append({"id": spec["id"], "record_sha256": file_digest(path), "matrix_replay": replay,
                     "minimal_clock_period": 4, "strict_pending_accepted": pending,
                     "first_receiver_change": measured["first_receiver_change"]})
    differences = {}
    for arrangement in ("isolated", "connected"):
        on, off = grouped[(arrangement, True)], grouped[(arrangement, False)]
        source_control(on["states"][0], off["states"][0], [(x, 8, 16, g) for x in range(4, 8) for g in (0, 14)])
        changed = [t for t, (a, b) in enumerate(zip(on["receiver"], off["receiver"])) if a != b]
        assert changed == summary["checks"][arrangement]["receiver_differs_from_source_off_at"]
        assert on["clock"] == off["clock"]
        differences[arrangement] = changed
    # Catalog status gates are metadata, never runtime instructions. No failed
    # capture or interaction result may silently promote a scientific claim.
    for gate in summary["contract_reports"]:
        if gate["stage"] in ("quiet_capture", "orbit_capture", "waiting_capture", "approval_release", "split_1_to_2", "router", "finite_ack"):
            assert not gate["allowed"] and not gate["claim_ready"] and gate["runtime_controller"] is False
    assert summary["isolated_coexistence_passed"] is True
    assert summary["connected_strict_pending_goal_passed"] is False
    assert summary["new_capture_or_approval_claim"] is False
    return {"passed": True, "kind": "composition", "protocol_sha256": protocol_hash,
            "full_recordings_independently_replayed": 4, "complete_states": 100,
            "forward_transitions": 96, "inverse_transitions": 96, "full_reverse_traversals": 4,
            "independent_initial_recipe_composition": True, "both_source_controls_preserve_clock_and_all_remainders": True,
            "isolated_coexistence": True, "clock_complete336_region_minimal_period": 4,
            "receiver_source_effect_times": differences, "connected_strict_pending_accepted": False,
            "incoming_capture_established": False, "scientific_stage_gates_checked": True,
            "records": rows}


def interaction_geometry(protocol, case):
    geo = protocol["geometry"]
    center = (geo["clock_x"], geo["clock_y"], geo["clock_z"])
    matrix = coupling(tuple(protocol["board"]["body_signs"]))
    receivers = [g for g in range(48) if matrix.ports[3][g] == case["guide_target_channel"]]
    assert len(receivers) == 1
    nodes = (center, *(tuple(a+b for a, b in zip(center, delta)) for delta in DIRECTIONS))
    return center, receivers[0], nodes


def interaction_initial(protocol, case):
    geo, board = protocol["geometry"], protocol["board"]
    assert board["side"] in (129, 137, 161, 193)
    assert board == {"side": board["side"], "background": [0, 0, 2], "body_signs": [1, 1, 1]}
    source = [geo["packet_x"], geo["row_y"], geo["row_z"]]
    seed = previous_initial({"board": board, "components": [
        {"name": "guide", "recipe": "GuideSegment", "at": [0, source[1], source[2]],
         "params": {"start": 0, "stop": board["side"]-1, "sockets": list(range(source[0], source[0]+4)), "remainder_pair": [0, 4]}},
        {"name": "packet", "recipe": "GuidedPacketSource", "at": source, "params": {"present": case["control"][0] == "1"}}]})
    center, channel, nodes = interaction_geometry(protocol, case)
    matrix = coupling((1, 1, 1))
    q, phase = (1 if case["guide_target_channel"] == 0 else -1), case["phase"]
    counters = ((0, q), (q, 0), (0, -q), (-q, 0))[phase] if case["control"][1] == "1" else (0, 0)
    cells = dict(seed.cells)
    cells[(*center, channel)] = (*counters, case["clock_remainder"])
    for d, position in enumerate(nodes[1:]):
        recipients = [g for g in range(48) if matrix.ports[d ^ 1][g] == channel]
        assert len(recipients) == 1
        g = recipients[0]
        base = (0 if q == 1 else 4) if d == 3 or d == case["compensation_direction"] else 2
        value = base + (2*q*matrix.weights[d ^ 1][g] if phase in (1, 2) else 0)
        assert 0 <= value < 6
        cells[(*position, g)] = (0, 0, value)
    return Snapshot(board["side"], (0, 0, 2), cells)


@lru_cache(maxsize=64)
def packet_template(x, y, z, direction):
    prepared = previous_initial({"board": {"side": 129}, "components": [
        {"name": "guide", "recipe": "GuideSegment", "at": [0, y, z],
         "params": {"start": x-1, "stop": x+4, "sockets": list(range(x, x+4)), "remainder_pair": [0, 4]}},
        {"name": "packet", "recipe": "GuidedPacketSource", "at": [x, y, z]}]})
    if direction == 1:
        return prepared.cells
    return Snapshot(129, (0, 0, 2), {a: (-v[1], -v[0], v[2]) for a, v in prepared.cells.items()}).cells


def interaction_observations(protocol, case, states):
    center, channel, nodes = interaction_geometry(protocol, case)
    positions = set(nodes)
    addresses = [(*position, g) for position in nodes for g in range(48)]
    region = [[list(state.at(a)) for a in addresses] for state in states]
    ctr = [list(state.at((*center, channel))) for state in states]
    matrix = coupling(tuple(protocol["board"]["body_signs"]))
    inverse = [{sender: receiver for receiver, sender in enumerate(row)} for row in matrix.ports]
    events = [{"step": e["step"], "address": e["address"], "kind": e["kind"], "ell": int(e["quotient"])}
              for e in all_events(states)[0]]
    boundary, inputs = [], []
    for t, old in enumerate(states[:-1], 1):
        external = []
        for source, triple in sorted(old.cells.items()):
            if not triple[1] or source[:3] in positions:
                continue
            for d, delta in enumerate(DIRECTIONS):
                position = tuple((source[j]+delta[j]) % old.side for j in range(3))
                if position not in positions:
                    continue
                g = inverse[d ^ 1][source[3]]
                external.append({"target": [*position, g], "source": list(source),
                                 "term": matrix.weights[d ^ 1][g]*triple[1]})
        boundary.append({"update": t, "nonzero_external_terms": external})
        sums, terms = input_terms(old, [(*center, channel)], protocol["board"]["body_signs"])
        inputs.append({"update": t, "terms": [{"source": term["address"], "term": term["weight"]*int(term["b"])} for term in terms[0]], "u": sums[0]})
    holds = []
    for start in protocol["readouts"]["eligible_hold_starts"]:
        end = start+8
        if end >= len(states) or any(boundary[t]["nonzero_external_terms"] for t in range(start, end)):
            continue
        frames, chosen = region[start:end+1], ctr[start:end+1]
        pairs = [(v[0]*v[0]+v[1]*v[1], v[2]) for v in chosen]
        periodic = all(frames[t] == frames[t+4] for t in range(5))
        others_quiet = all(not any(value[:2]) for frame in frames for i, value in enumerate(frame) if i != channel)
        if periodic and others_quiet and not any(inputs[t]["u"] for t in range(start, end)) and len(set(pairs)) == 1 and pairs[0][0] in (1, 2, 4) and pairs[0][1] in (0, 2, 4):
            holds.append({"kind": "retained_orbit", "start": start, "through": end, "R": list(pairs[0])})
        if all(not any(value[:2]) for frame in frames for value in frame) and all(frame == frames[0] for frame in frames) and chosen[0][2] != ctr[0][2]:
            holds.append({"kind": "quiet_remainder", "start": start, "through": end, "R": list(pairs[0])})
    carriers = []
    geo = protocol["geometry"]
    y, z = geo["row_y"], geo["row_z"]
    for direction, x in ((1, geo["forward_outlet_x"]), (-1, geo["backward_outlet_x"])):
        for start in range(18, len(states)-3):
            good = True
            for k in range(4):
                origin = x+direction*k
                actual = {a: v for a, v in states[start+k].cells.items() if origin-1 <= a[0] <= origin+4 and abs(a[1]-y) <= 1 and abs(a[2]-z) <= 1}
                if actual != packet_template(origin, y, z, direction):
                    good = False
                    break
            if good:
                carriers.append({"start": start, "direction": direction, "outlet_x": x, "through": start+3, "full_local_template_equal": True})
    hits = [{"step": t, "address": list(a)} for t, state in enumerate(states) for a, v in state.cells.items()
            if any(v[:2]) and any(c in (0, state.side-1) for c in a[:3])]
    return {"region_nodes": [list(n) for n in nodes], "region_addresses": [list(a) for a in addresses],
            "region_trace": region, "center_address": [*center, channel], "center_trace": ctr,
            "center_inputs": inputs, "boundary_inputs": boundary, "all_C": events,
            "center_C": [e for e in events if tuple(e["address"]) == (*center, channel)],
            "candidate_holds": holds, "outgoing_carriers": carriers, "active_boundary_hits": hits}


def interaction_group(group):
    ctr = {mask: value["observations"]["center_trace"] for mask, value in group.items()}
    nonlinear = []
    for t in range(41):
        for j in (0, 1):
            expected = ctr["10"][t][j]+ctr["01"][t][j]-ctr["00"][t][j]
            if ctr["11"][t][j] != expected:
                nonlinear.append({"step": t, "component": "ab"[j], "actual": ctr["11"][t][j], "linear_controls": expected})
    bags = {mask: Counter((e["kind"], e["ell"]) for e in row["observations"]["center_C"]) for mask, row in group.items()}
    excess = bags["11"]-(bags["10"]+bags["01"])
    retained = [candidate for candidate in group["11"]["observations"]["candidate_holds"]
                if all([ctr[mask][t][0]**2+ctr[mask][t][1]**2, ctr[mask][t][2]] != candidate["R"]
                       for mask in ("10", "01") for t in range(candidate["start"], candidate["through"]+1))]
    addresses = set().union(*(row["states"][0].cells for row in group.values()))
    same_r = all(len({row["states"][0].at(a)[2] for row in group.values()}) == 1 for a in addresses)
    null = all(s == group["00"]["states"][0] for s in group["00"]["states"])
    clock = group["01"]["states"]
    period = all(a == b for a, b in zip(clock, clock[4:]))
    valid = same_r and null and period
    return {"matched_initial_remainders": same_r, "null_static": null, "clock_only_full_state_period4": period,
            "controlled_activation": bool(excess and nonlinear and valid),
            "novel_center_C_signatures": [[kind, ell, count] for (kind, ell), count in sorted(excess.items())],
            "first_nonlinear_center_counter": nonlinear[0] if nonlinear else None,
            "retained_records": retained if valid else [],
            "outgoing_carriers": {mask: row["observations"]["outgoing_carriers"] for mask, row in group.items()},
            "center_C_counts": {mask: sum(v.values()) for mask, v in bags.items()},
            "all_C_counts": {mask: len(row["observations"]["all_C"]) for mask, row in group.items()},
            "full_state_final_hashes": {mask: row["experiment"]["frames"][-1]["state_sha256"] for mask, row in group.items()},
            "release_established": False}


def interaction_provenance(folder, registration):
    """Check the historical executable, allowing only the declared JSON whitespace fix."""
    folder = Path(folder)
    changes = []
    for path, sha in registration["source_sha256"].items():
        if file_digest(ROOT/path) == sha:
            continue
        assert path == "research/staged_blocks/interactions.py", ("Interaction source changed", path)
        metadata = load(folder/"packaging.json")
        old_path = folder/metadata["executed_source_snapshot"]
        assert file_digest(old_path) == sha == metadata["executed_source_sha256"]
        before = '    write_json(output/"experiments.json", bundle(examples, title="The Presenter: packet and clock controls"))'
        after = '    (output/"experiments.json").write_text(canonical(bundle(examples, title="The Presenter: packet and clock controls"))+"\\n")'
        old, new = old_path.read_text(), (ROOT/path).read_text()
        assert old.count(before) == 1 and old.replace(before, after) == new, "Undeclared scientific source change"
        portable = load(folder/"experiments.json")
        assert digest(portable) == metadata["semantic_sha256"]
        assert len(portable["experiments"]) == 8
        for experiment in portable["experiments"]:
            native = load(folder/"records"/(experiment["id"]+".json.gz"))
            assert experiment == native["experiment"], "Packaging changed a native experiment"
        assert sum(p.stat().st_size for p in folder.rglob("*") if p.is_file()) <= 20971520
        changes.append({"path": path, "executed_sha256": sha, "current_sha256": file_digest(ROOT/path),
                        "scope": "One final Presenter JSON whitespace serialization change; exact executed source retained, all eight native experiments equal."})
    return {"registered_scientific_sources_verified": True, "postrun_serialization_changes": changes}


def audit_interaction(folder, *, deadline=None):
    folder = Path(folder)
    protocol_hash = "0bf67cf858fb75dc2c44be9d9f96ccd2c3538c8a088cd4fe210079b26b477d1d"
    protocol, summary, registration = load(folder/"protocol.json"), load(folder/"result.json"), load(folder/"registration.json")
    assert file_digest(folder/"protocol.json") == protocol_hash == registration["protocol_sha256"] == summary["protocol_sha256"]
    provenance = interaction_provenance(folder, registration)
    geometries = []
    for stage, gs, ds in (("base", (0, 14), (None,)), ("compensation", (0,), (0, 1, 2, 4, 5))):
        for g, r, phase, direction in itertools.product(gs, (0, 2, 4), range(4), ds):
            suffix = "none" if direction is None else str(direction)
            geometries.append({"id": f"{stage}-g{g}-r{r}-p{phase}-d{suffix}", "stage": stage,
                               "guide_target_channel": g, "clock_remainder": r, "phase": phase, "compensation_direction": direction})
    assert registration["geometries"] == geometries and len(geometries) == 84
    assert summary["status"] == "completed" and summary["completed_cases"] == 336
    assert len(summary["cases"]) == 336 and len(summary["groups"]) == 84
    assert {p.name for p in (folder/"records").glob("*.json.gz")} == {g["id"]+"-"+mask+".json.gz" for g in geometries for mask in ("00", "10", "01", "11")}
    records, results = [], []
    for i, geometry in enumerate(geometries):
        group = {}
        for j, mask in enumerate(("00", "10", "01", "11")):
            case = {**geometry, "control": mask}
            path = folder/"records"/(geometry["id"]+"-"+mask+".json.gz")
            record = load(path)
            row = summary["cases"][4*i+j]
            assert file_digest(path) == row["record_gzip_sha256"] and digest(record) == row["record_sha256"]
            assert record["spec"]["controls"] == case == row["case"]
            assert record["spec"]["steps"] == 40
            native = {k: v for k, v in record.items() if k != "observations"}
            replay, states = audit_record(native, expected_initial=interaction_initial(protocol, case), deadline=deadline)
            observed = interaction_observations(protocol, case, states)
            assert observed == record["observations"], ("Independent interaction observer mismatch", geometry["id"], mask)
            assert not observed["active_boundary_hits"]
            group[mask] = {"states": states, "observations": observed, "experiment": record["experiment"]}
            assert record["assessment"] == summary["groups"][i]
            records.append({"id": record["spec"]["id"], "record_sha256": file_digest(path),
                            "states": len(states), "forward_inverse_transitions": 40,
                            "all_C_count": len(observed["all_C"]), "full_rewind_equal": True})
        center, h, _ = interaction_geometry(protocol, geometry)
        packet = [(x, 64, 64, g) for x in range(48, 52) for g in (0, 14)]
        for on, off, addresses in (("11", "01", packet), ("10", "00", packet), ("11", "10", [(*center, h)]), ("01", "00", [(*center, h)])):
            source_control(group[on]["states"][0], group[off]["states"][0], addresses)
        measured = interaction_group(group)
        for key, value in measured.items():
            assert value == summary["groups"][i][key], ("Independent interaction criterion mismatch", geometry["id"], key)
        results.append({"id": geometry["id"], **{k: v for k, v in measured.items() if k not in ("full_state_final_hashes",)}})
    counts = {"controlled_activation_groups": sum(r["controlled_activation"] for r in results),
              "retained_orbit_groups": sum(any(c["kind"] == "retained_orbit" for c in r["retained_records"]) for r in results),
              "quiet_record_groups": sum(any(c["kind"] == "quiet_remainder" for c in r["retained_records"]) for r in results),
              "joint_outgoing_carrier_groups": sum(bool(r["outgoing_carriers"]["11"]) for r in results)}
    assert all(summary[k] == v for k, v in counts.items())
    return {"passed": True, "kind": "interaction", "protocol_sha256": protocol_hash,
            "full_recordings_independently_replayed": 336, "complete_states": 13776,
            "forward_transitions": 13440, "inverse_transitions": 13440, "full_reverse_traversals": 336,
            "full336_region_and_every_external_incoming_term_checked": True,
            "all_world_C_events_checked": True, "four_source_controls_preserve_every_remainder": True,
            "registered_memory_predicate_unchanged": True, "release_established": False,
            "scope": "All84 registered +++ geometries and their336 complete control recordings; activation, retained I/r orbit, quiet memory and transport remain distinct predicates.",
            **counts, "provenance": provenance, "groups": results, "records": records}


def phase_base_protocol(case):
    protocol = load(ROOT/'research/staged_blocks/interaction_protocol.json')
    c = case['side']//2
    protocol['board']['side'] = case['side']
    protocol['geometry'] = {'row_y': c, 'row_z': c, 'packet_x': c-16-case['delay'],
                            'clock_x': c, 'clock_y': c+1, 'clock_z': c,
                            'forward_outlet_x': c+8, 'backward_outlet_x': c-8}
    return protocol


def phase_initial(case):
    initial = interaction_initial(phase_base_protocol(case), case)
    c = initial.side//2
    reference = (c, c+24, c+24, 0)
    assert initial.at(reference) == initial.background
    return Snapshot(initial.side, initial.background, {**initial.cells, reference: (0, 1, 2)})


def phase_observations(case, states):
    base = phase_base_protocol(case)
    out = interaction_observations(base, case, states)
    c = case['side']//2
    center = (c, c+24, c+24)
    nodes = (center, *(tuple(center[j]+d[j] for j in range(3)) for d in DIRECTIONS))
    addresses = [(*xyz, g) for xyz in nodes for g in range(48)]
    region = [[list(s.at(a)) for a in addresses] for s in states]
    trace = [list(s.at((*center, 0))) for s in states]
    matrix = coupling((1, 1, 1))
    inverse = [{sender: receiver for receiver, sender in enumerate(row)} for row in matrix.ports]
    cycle = ((0, 1), (1, 0), (0, -1), (-1, 0))
    expected = []
    for t in range(len(states)):
        cells = {(*center, 0): (*cycle[t % 4], 2)}
        for d, xyz in enumerate(nodes[1:]):
            recipient = inverse[d ^ 1][0]
            cells[(*xyz, recipient)] = (0, 0, 2+2*matrix.weights[d ^ 1][recipient]*(t % 4 in (1, 2)))
        expected.append([list(cells.get(a, states[0].background)) for a in addresses])
    inputs, boundaries = [], []
    for t, (old, new) in enumerate(zip(states, states[1:]), 1):
        sums, terms = input_terms(old, [(*center, 0)], (1, 1, 1))
        inputs.append({'update': t, 'terms': [{'source': term['address'], 'term': term['weight']*int(term['b'])} for term in terms[0]],
                       'u': sums[0], 'ell': new.at((*center, 0))[1]+old.at((*center, 0))[0]})
        external = []
        for source, triple in sorted(old.cells.items()):
            if not triple[1] or source[:3] in nodes:
                continue
            for d, delta in enumerate(DIRECTIONS):
                position = tuple((source[j]+delta[j]) % old.side for j in range(3))
                if position in nodes:
                    g = inverse[d ^ 1][source[3]]
                    external.append({'source': list(source), 'target': [*position, g], 'term': matrix.weights[d ^ 1][g]*triple[1]})
        boundaries.append({'update': t, 'nonzero_external_terms': external})
    out['reference'] = {'center': list(center), 'region_nodes': [list(n) for n in nodes],
                        'region_addresses': [list(a) for a in addresses], 'region_trace': region,
                        'center_trace': trace, 'inputs': inputs, 'boundary_inputs': boundaries,
                        'complete_region_matches_isolated_formula': region == expected,
                        'all_external_terms_zero': all(not b['nonzero_external_terms'] for b in boundaries)}
    def distance(a, b):
        return sum(min(abs(a[j]-b[j]), states[0].side-abs(a[j]-b[j])) for j in range(3))
    active = [a for a, v in states[0].cells.items() if any(v[:2]) and a[:3] != center]
    to_ref = min((distance(a, n) for a in active for n in nodes), default=None)
    to_target = min(distance(center, n) for n in out['region_nodes'])
    out['causal_separation'] = {'non_reference_to_reference_region': to_ref, 'reference_to_target_region': to_target,
                                'valid': (to_ref is None or to_ref > 40) and to_target > 40}
    out['phase_trace'] = []
    for t, (v, ref) in enumerate(zip(out['center_trace'], trace)):
        dot, cross = v[0]*ref[0]+v[1]*ref[1], v[0]*ref[1]-v[1]*ref[0]
        energy, ref_energy = sum(a*a for a in v[:2]), sum(a*a for a in ref[:2])
        out['phase_trace'].append({'step': t, 'D': dot, 'X': cross, 'I_target': energy, 'I_reference': ref_energy,
                                   'identity_equal': dot*dot+cross*cross == energy*ref_energy})
    for t, row in enumerate(out['center_inputs']):
        row['ell'] = out['center_trace'][t+1][1]+out['center_trace'][t][0]
    return out


def phase_verdict(case, out):
    alphabet = ((1, 0), (0, 1), (-1, 0), (0, -1))
    mask = case['control']
    expected = alphabet[-case['delay'] % 4] if mask == '11' else alphabet[case['phase']] if mask == '01' else (0, 0)
    predicted = all((v['D'], v['X']) == expected for v in out['phase_trace'][32:41])
    frames = out['region_trace'][32:41]
    channel = out['center_address'][3]
    if mask[1] == '1':
        hold = (all(frames[t] == frames[t+4] for t in range(5))
                and all(not any(v[:2]) for frame in frames for j, v in enumerate(frame) if j != channel)
                and all(sum(v*v for v in frame[channel][:2]) == 1 and frame[channel][2] == case['clock_remainder'] for frame in frames))
    else:
        hold = all(frame == frames[0] for frame in frames) and all(not any(v[:2]) for frame in frames for v in frame)
    isolation = all(not row['nonzero_external_terms'] for row in out['boundary_inputs'][32:40])
    quotient = all(row['u'] == row['ell'] == 0 for row in out['center_inputs'][32:40])
    reference = out['reference']
    ref_valid = reference['complete_region_matches_isolated_formula'] and reference['all_external_terms_zero'] and all(row['u'] == row['ell'] == 0 for row in reference['inputs'])
    return {'expected_DX': list(expected), 'prediction_matches': predicted,
            'target_complete_hold': hold, 'target_external_terms_zero': isolation,
            'target_hold_input_and_quotient_zero': quotient, 'reference_valid': ref_valid,
            'causal_separation_valid': out['causal_separation']['valid'],
            'phase_identity_all_states': all(row['identity_equal'] for row in out['phase_trace']),
            'passed': all((predicted, hold, isolation, quotient, ref_valid, out['causal_separation']['valid']))}


def audit_phase(folder, *, deadline=None):
    folder = Path(folder)
    protocol, summary, registration = load(folder/'protocol.json'), load(folder/'result.json'), load(folder/'registration.json')
    protocol_hash = 'cce7942e8fddc8e8ca068b56fa156b9563345facce8989fdef5cc22638dabfed'
    assert file_digest(folder/'protocol.json') == protocol_hash == registration['protocol_sha256'] == summary['protocol_sha256']
    for path, sha in registration['source_sha256'].items():
        assert file_digest(ROOT/path) == sha, ('Phase source changed', path)
    geometries = []
    for side, r, phase, delay in itertools.product((129, 161), (0, 4), range(4), (1, 2, 3, 5)):
        geometries.append({'id': f'phase-L{side}-r{r}-p{phase}-d{delay}', 'side': side,
                           'clock_remainder': r, 'phase': phase, 'delay': delay,
                           'stage': 'phase', 'guide_target_channel': 0, 'compensation_direction': None})
    assert geometries == registration['geometries']
    assert summary['status'] == 'completed' and summary['completed_cases'] == 256
    assert len(summary['cases']) == 256 and len(summary['groups']) == 64
    assert {p.name for p in (folder/'records').glob('*.json.gz')} == {g['id']+'-'+mask+'.json.gz' for g in geometries for mask in ('00', '10', '01', '11')}
    reports, groups = [], []
    for i, geometry in enumerate(geometries):
        rows = {}
        for j, mask in enumerate(('00', '10', '01', '11')):
            case = {**geometry, 'control': mask}
            path = folder/'records'/(geometry['id']+'-'+mask+'.json.gz')
            record, declared = load(path), summary['cases'][4*i+j]
            assert file_digest(path) == declared['record_gzip_sha256'] and digest(record) == declared['record_sha256']
            assert record['spec']['controls'] == case == declared['case']
            assert record['spec']['steps'] == 40
            native = {k: v for k, v in record.items() if k != 'observations'}
            replay, states = audit_record(native, expected_initial=phase_initial(case), deadline=deadline)
            observed = phase_observations(case, states)
            assert observed == record['observations'], ('Independent phase observer mismatch', geometry['id'], mask)
            assert not observed['active_boundary_hits']
            verdict = phase_verdict(case, observed)
            assert verdict == declared['assessment'] == summary['groups'][i]['case_verdicts'][mask]
            assert record['assessment'] == summary['groups'][i]
            rows[mask] = {'states': states, 'observations': observed, 'verdict': verdict, 'experiment': record['experiment']}
            reports.append({'id': declared['id'], 'record_sha256': file_digest(path), 'states': 41, 'forward_inverse_transitions': 40,
                            'all_C_count': len(observed['all_C']), 'full_rewind_equal': True})
        c, x = geometry['side']//2, geometry['side']//2-16-geometry['delay']
        h = interaction_geometry(phase_base_protocol(case), case)[1]
        packet = [(a, c, c, g) for a in range(x, x+4) for g in (0, 14)]
        for on, off, addresses in (('11', '01', packet), ('10', '00', packet), ('11', '10', [(c, c+1, c, h)]), ('01', '00', [(c, c+1, c, h)])):
            source_control(rows[on]['states'][0], rows[off]['states'][0], addresses)
        success = all(row['verdict']['passed'] for row in rows.values())
        changed = geometry['phase'] != -geometry['delay'] % 4
        hashes = {mask: row['experiment']['frames'][-1]['state_sha256'] for mask, row in rows.items()}
        group = {'geometry': geometry, 'matched_initial_remainders': True, 'synchronization_passed': success,
                 'expected_changed_phase': changed, 'retained_changed_phase': success and changed,
                 'already_aligned': success and not changed, 'case_verdicts': {mask: row['verdict'] for mask, row in rows.items()},
                 'full_state_final_hashes': hashes, 'four_final_states_distinct': len(set(hashes.values())) == 4}
        assert all(value == summary['groups'][i][key] for key, value in group.items())
        groups.append(group)
    counts = {'synchronization_groups': sum(g['synchronization_passed'] for g in groups),
              'retained_changed_phase_groups': sum(g['retained_changed_phase'] for g in groups),
              'already_aligned_groups': sum(g['already_aligned'] for g in groups)}
    assert all(summary[k] == v for k, v in counts.items())
    return {'passed': True, 'kind': 'interaction_phase', 'protocol_sha256': protocol_hash,
            'full_recordings_independently_replayed': 256, 'complete_states': 10496,
            'forward_transitions': 10240, 'inverse_transitions': 10240, 'full_reverse_traversals': 256,
            'all_world_C_events_checked': True, 'four_source_controls_preserve_every_remainder': True,
            'full_target_and_reference_regions_checked': True, 'every_external_incoming_term_checked': True,
            'scope': 'All64 registered geometries and256 controls. The passive relative-phase observer is not an implemented local comparator, detector, presence latch, capture or release.',
            **counts, 'groups': groups, 'records': reports}


@lru_cache(maxsize=64)
def signed_packet_template(x, direction, signs):
    board = {'side': 129, 'body_signs': list(signs)}
    initial = previous_initial({'board': board, 'components': [
        {'name': 'guide', 'recipe': 'GuideSegment', 'at': [0, 64, 64],
         'params': {'start': x-1, 'stop': x+4, 'sockets': list(range(x, x+4)), 'remainder_pair': [0, 4]}},
        {'name': 'packet', 'recipe': 'GuidedPacketSource', 'at': [x, 64, 64]}]})
    return initial.cells if direction == 1 else Snapshot(129, initial.background, {a: (-v[1], -v[0], v[2]) for a, v in initial.cells.items()}).cells


def signed_initial(case=None, *, method=None, signs=None, direction=1):
    if case is not None:
        method, signs = case['seed_method'], tuple(case['body_signs'])
    seed_signs = signs if method == 'tensor_aware' else (1, 1, 1)
    board = {'side': 129, 'body_signs': list(seed_signs), 'background': [0, 0, 2]}
    initial = previous_initial({'board': board, 'components': [
        {'name': 'guide', 'recipe': 'GuideSegment', 'at': [0, 64, 64],
         'params': {'start': 0, 'stop': 128, 'sockets': [48, 49, 50, 51], 'remainder_pair': [0, 4]}},
        {'name': 'packet', 'recipe': 'GuidedPacketSource', 'at': [48, 64, 64],
         'params': {'present': case is None or case['control'][0] == '1'}}]})
    if case is None:
        return initial if direction == 1 else Snapshot(129, initial.background, {a: (-v[1], -v[0], v[2]) for a, v in initial.cells.items()})
    matrix = coupling(tuple(seed_signs))
    inverse = [{sender: receiver for receiver, sender in enumerate(row)} for row in matrix.ports]
    center, h = (64, 65, 64), inverse[3][0]
    q = matrix.weights[3][h]
    phase = case['phase']
    counters = ((0, q), (q, 0), (0, -q), (-q, 0))[phase] if case['control'][1] == '1' else (0, 0)
    cells = dict(initial.cells)
    cells[(*center, h)] = (*counters, case['clock_remainder'])
    for d, delta in enumerate(DIRECTIONS):
        position = tuple(center[j]+delta[j] for j in range(3))
        g = inverse[d ^ 1][h]
        r = (0 if d == 3 else 2)+2*q*matrix.weights[d ^ 1][g]*(phase in (1, 2))
        assert 0 <= r < 6
        cells[(*position, g)] = (0, 0, r)
    return Snapshot(129, initial.background, cells)


def signed_observations(case, states):
    protocol = load(ROOT/'research/staged_blocks/interaction_protocol.json')
    protocol['board']['body_signs'] = case['body_signs']
    out = interaction_observations(protocol, case, states)
    carriers = []
    for direction, x in ((1, 72), (-1, 56)):
        for start in range(18, 38):
            equal = True
            for k in range(4):
                origin = x+direction*k
                actual = {a: v for a, v in states[start+k].cells.items() if origin-1 <= a[0] <= origin+4 and abs(a[1]-64) <= 1 and abs(a[2]-64) <= 1}
                if actual != signed_packet_template(origin, direction, tuple(case['body_signs'])):
                    equal = False
                    break
            if equal:
                carriers.append({'start': start, 'through': start+3, 'direction': direction, 'outlet_x': x, 'full_local_template_equal': True})
    out['outgoing_carriers'] = carriers
    out['forward_outlet_active_steps'] = [t for t in range(20, 41) if any(any(states[t].at((72, 64, 64, g))[:2]) for g in range(48))]
    out['forward_outlet_C'] = [e for e in out['all_C'] if 20 <= e['step'] <= 40 and e['address'][:3] == [72, 64, 64]]
    return out


def audit_signed(folder, *, deadline=None):
    folder = Path(folder)
    protocol, result, registration = load(folder/'protocol.json'), load(folder/'result.json'), load(folder/'registration.json')
    protocol_hash = '2ec8edac07fa5595fc0f490ce7c717b73d999e7df03cb624b0e01a84b5d090a2'
    assert file_digest(folder/'protocol.json') == protocol_hash == registration['protocol_sha256'] == result['protocol_sha256']
    for path, sha in registration['source_sha256'].items():
        assert file_digest(ROOT/path) == sha, ('Signed source changed', path)
    geometries = []
    for method, signs, r, phase in itertools.product(('same_seed', 'tensor_aware'), ((1, 1, 1), (1, -1, 1)), (0, 4), range(4)):
        label = ''.join('p' if s == 1 else 'm' for s in signs)
        geometries.append({'id': f'signed-{method}-{label}-r{r}-p{phase}', 'seed_method': method,
                           'body_signs': list(signs), 'clock_remainder': r, 'phase': phase,
                           'stage': 'signed', 'guide_target_channel': 0, 'compensation_direction': None})
    assert registration['geometries'] == geometries
    assert result['status'] == 'completed' and result['completed_cases'] == 136
    assert len(result['cases']) == 136 and len(result['groups']) == 32 and len(result['carrier_checks']) == 8
    assert len(list((folder/'records').glob('*.json.gz'))) == 136
    records, carriers, carrier_results, groups = [], {}, [], []
    def read_record(row, expected):
        path = folder/row['record']
        record = load(path)
        assert file_digest(path) == row['record_gzip_sha256'] and digest(record) == row['record_sha256']
        native = {k: v for k, v in record.items() if k != 'observations'}
        replay, states = audit_record(native, expected_initial=expected, deadline=deadline)
        records.append({'id': row['id'], 'record_sha256': file_digest(path), 'states': len(states),
                        'forward_inverse_transitions': len(states)-1, 'all_C_count': replay['whole_board_C_count'], 'full_rewind_equal': True})
        return record, states
    for i, (method, signs, direction) in enumerate(itertools.product(('same_seed', 'tensor_aware'), ((1, 1, 1), (1, -1, 1)), (1, -1))):
        record, states = read_record(result['cases'][i], signed_initial(method=method, signs=signs, direction=direction))
        equal = [state == Snapshot(129, states[0].background, {((a[0]+direction*t) % 129, *a[1:]): v for a, v in states[0].cells.items()}) for t, state in enumerate(states)]
        assessment = {'seed_method': method, 'body_signs': list(signs), 'direction': direction,
                      'complete_translation_equal': all(equal), 'state_equal_by_step': equal}
        assert assessment == record['assessment'] == result['carrier_checks'][i]
        assert record['observations'] == {'translation_equal_by_state': equal}
        carriers[method, signs, direction] = all(equal)
        carrier_results.append(assessment)
    for i, geometry in enumerate(geometries):
        group = {}
        for j, mask in enumerate(('00', '10', '01', '11')):
            case = {**geometry, 'control': mask}
            record, states = read_record(result['cases'][8+4*i+j], signed_initial(case))
            assert record['spec']['controls'] == case
            observed = signed_observations(case, states)
            assert observed == record['observations'], ('Signed observer mismatch', geometry['id'], mask)
            assert not observed['active_boundary_hits']
            assert record['assessment'] == result['groups'][i]
            group[mask] = {'states': states, 'observations': observed, 'experiment': record['experiment']}
        packet = [(x, 64, 64, g) for x in range(48, 52) for g in (0, 14)]
        h = coupling(tuple(geometry['body_signs'])).ports[2][0]
        for on, off, addresses in (('11', '01', packet), ('10', '00', packet), ('11', '10', [(64, 65, 64, h)]), ('01', '00', [(64, 65, 64, h)])):
            source_control(group[on]['states'][0], group[off]['states'][0], addresses)
        measured = interaction_group(group)
        valid = carriers[geometry['seed_method'], tuple(geometry['body_signs']), 1]
        eligible = valid and measured['clock_only_full_state_period4']
        active = {mask: row['observations']['forward_outlet_active_steps'] for mask, row in group.items()}
        measured.update(pristine_forward_carrier_valid=valid, singleton_gates_passed=eligible,
                        strict_forward_cancellation=bool(eligible and active['10'] and not active['00'] and not active['01'] and not active['11']),
                        forward_outlet_active=active,
                        forward_carrier_suppression=bool(eligible and any(c['direction'] == 1 for c in measured['outgoing_carriers']['10']) and not any(c['direction'] == 1 for c in measured['outgoing_carriers']['11'])))
        assert all(value == result['groups'][i][key] for key, value in measured.items()), ('Signed group verdict mismatch', geometry['id'])
        groups.append({'id': geometry['id'], **measured})
    counts = {'singleton_eligible_groups': sum(g['singleton_gates_passed'] for g in groups),
              'strict_forward_cancellation_groups': sum(g['strict_forward_cancellation'] for g in groups),
              'forward_carrier_suppression_groups': sum(g['forward_carrier_suppression'] for g in groups),
              'retained_record_groups': sum(bool(g['retained_records']) for g in groups)}
    assert all(result[key] == value for key, value in counts.items())
    return {'passed': True, 'kind': 'interaction_signed', 'protocol_sha256': protocol_hash,
            'full_recordings_independently_replayed': 136, 'complete_states': 5320,
            'forward_transitions': 5184, 'inverse_transitions': 5184, 'full_reverse_traversals': 136,
            'all_world_C_events_checked': True, 'four_source_controls_preserve_every_remainder': True,
            'scope': 'Every signed comparison and eight pristine controls; failed singleton transport cannot count as interaction cancellation. Local silence is not full-state deletion.',
            **counts, 'carrier_checks': carrier_results, 'groups': groups, 'records': records}


def audit_synthesis(folder, *, deadline=None):
    folder = Path(folder)
    protocol, registration, result = load(folder/'protocol.json'), load(folder/'registration.json'), load(folder/'result.json')
    protocol_hash = file_digest(folder/'protocol.json')
    assert protocol_hash == registration['protocol_sha256'] == result['protocol_sha256']
    assert protocol_hash in ('70d4fee4bdabaa902897d257a50db024370585bccda388bf3d51f3f2af3bdd98', 'd1b5419701fbdc79be883ad6c8ff4add55dbcd737f4f20e717ac369c07b0a85b')
    for path, expected in registration['source_sha256'].items():
        assert file_digest(ROOT/path) == expected, ('Synthesis execution source changed', path)
    assert result['sources_unchanged'] is True
    if 'equivalent_to' in protocol:
        original = load(ROOT/'research/staged_blocks/synthesis_protocol_a.json')
        omit = {'id', 'status', 'encoding', 'equivalent_to'}
        assert {k: v for k, v in protocol.items() if k not in omit} == {k: v for k, v in original.items() if k not in omit}
    query = audit_synthesis_query(protocol, folder/'query.smt2.gz')
    solver = load(folder/'solver_result.json')
    assert solver['query_sha256'] == query['query_sha256']
    assert solver['encoded_channel_updates'] == query['encoded_channel_updates']
    # These two registered executions ended unknown, without witnesses or proofs.
    # A future SAT or UNSAT result needs a separate reviewed acceptance path.
    assert result['status'] == 'inconclusive_solver' and result['reason'] == 'timeout'
    assert solver['answer'] == 'unknown' and result['accepted'] is False and result['records'] == []
    assert not list((folder/'records').glob('*.json*'))
    cpu = result['cpu_seconds']
    limit = protocol['budget']['max_cpu_seconds']
    return {'passed': True, 'kind': 'synthesis', 'protocol_sha256': protocol_hash,
            'status': result['status'], 'solver_answer': solver['answer'], 'query': query,
            'registered_sources_verified': True, 'witnesses': 0,
            'producer_cpu_seconds': cpu, 'registered_cpu_limit': limit, 'cpu_overrun_seconds': max(0, cpu-limit),
            'scientific_acceptance': False, 'excluded_registered_family': False,
            'independent_unsat_proof_certificate_checked': False,
            'scope': 'Submitted equations independently audited; both bounded solver timeouts are inconclusive. No witness, exclusion or physical conclusion follows.'}


def phase_information_retention(folder):
    """Locate the discarded local input-phase distinction in the full final state."""
    folder = Path(folder)
    rows = []
    for side, r, delay in itertools.product((129, 161), (0, 4), (1, 2, 3, 5)):
        recordings = [load(folder/'records'/f'phase-L{side}-r{r}-p{phase}-d{delay}-11.json.gz') for phase in range(4)]
        finals = [read_states(record['experiment'])[-1] for record in recordings]
        protected = {tuple(a) for record in recordings[:1] for name in ('region_addresses',) for a in record['observations'][name]}
        protected |= {tuple(a) for a in recordings[0]['observations']['reference']['region_addresses']}
        assert len({digest(s.canonical()) for s in finals}) == 4
        assert all(all(s.at(a) == finals[0].at(a) for a in protected) for s in finals)
        differences = []
        for i, j in itertools.combinations(range(4), 2):
            changed = [a for a in sorted(finals[i].cells.keys() | finals[j].cells.keys()) if finals[i].at(a) != finals[j].at(a)]
            assert changed and all(a not in protected for a in changed)
            differences.append({'initial_phases': [i, j], 'different_full_state_channels': len(changed), 'first_difference_outside_both_clock_regions': list(changed[0])})
        rows.append({'side': side, 'remainder': r, 'delay': delay, 'four_full_final_states_distinct': True,
                     'target_and_reference_full_regions_equal': True, 'pairwise_differences': differences})
    return {'passed': True, 'families': rows, 'scope': 'The locally erased initial phase remains distinguishable outside both complete clock regions; full rewind already reconstructs every initial preparation.'}


def audit_manifest(manifest_path, *, max_cpu_seconds=600):
    path = Path(manifest_path).resolve()
    manifest = load(path)
    assert manifest['format'] == 'universe24-staged-independent-audit-manifest-v1'
    assert manifest['base_commit'].startswith(BASE_COMMIT)
    assert len({study['id'] for study in manifest['studies']}) == len(manifest['studies'])
    start_cpu, start_wall = time.process_time(), time.monotonic()
    sources = {str(p.relative_to(ROOT)): file_digest(p) for package in ('universe24', 'research') for p in sorted((ROOT/package).rglob('*.py'))}
    git_identity = {'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                    'tree': subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], cwd=ROOT, text=True).strip(),
                    'tracked_status': subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, text=True).strip()}
    deadline = start_cpu+max_cpu_seconds
    results, failure = [], None
    try:
        for study in manifest['studies']:
            before_progress = dict(_REPLAY_PROGRESS)
            checked = {}
            for item in [study['protocol'], study['result'], *study['records']]:
                candidate = (path.parent/item['path']).resolve()
                assert candidate.is_relative_to(ROOT), 'Evidence path outside repository'
                assert file_digest(candidate) == item['sha256'], ('Manifest hash mismatch', item['path'])
                checked[item['path']] = item['sha256']
            folder = (path.parent/study['result']['path']).resolve().parent
            protocol_path = (path.parent/study['protocol']['path']).resolve()
            assert protocol_path == folder/'protocol.json'
            expected_records = {p.resolve() for p in (folder/'records').glob('*.json*')}
            manifest_records = {(path.parent/item['path']).resolve() for item in study['records']}
            assert expected_records == manifest_records, 'Manifest does not cover every complete retained recording'
            kind = study['kind']
            protocol = load(protocol_path)
            if kind == 'orbit':
                function = audit_orbit
            elif kind == 'composition':
                if protocol['format'] == 'universe24-four-piece-phase-demo-v1':
                    function = audit_recipe_demo
                elif protocol['format'] == 'universe24-composed-recipe-equivalence-v1':
                    function = audit_composed_recipes
                else:
                    function = audit_composition
            elif kind in ('interaction', 'interaction_phase', 'interaction_signed'):
                fmt = protocol['format']
                if fmt == 'universe24-staged-phase-memory-protocol-v1':
                    function = audit_phase
                elif fmt == 'universe24-staged-signed-comparison-protocol-v1':
                    function = audit_signed
                elif fmt == 'universe24-staged-transmission-protocol-v1':
                    function = audit_transmission
                elif fmt == 'universe24-pause-bridge-protocol-v1':
                    function = audit_bridge
                else:
                    function = audit_interaction
            elif kind == 'synthesis':
                function = audit_synthesis
            elif kind == 'motion':
                function = audit_motion
            else:
                raise AssertionError('Unreviewed study kind: '+kind)
            study_start = time.process_time()
            before_progress = dict(_REPLAY_PROGRESS)
            try:
                if study_start >= deadline:
                    raise TimeoutError('Final combined audit CPU budget exhausted')
                result = function(folder, deadline=deadline)
                if function == audit_phase:
                    result['information_retention'] = phase_information_retention(folder)
            except Exception as exc:
                failure = {'study': study['id'], 'type': type(exc).__name__, 'message': str(exc),
                           'incomplete_study_dynamical_replay_progress': {k: _REPLAY_PROGRESS[k]-before_progress[k] for k in before_progress},
                           'scope': 'Only listed earlier studies completed acceptance auditing. Dynamical replay progress in this failed or interrupted study does not imply scientific acceptance.'}
                break
            result['id'] = study['id']
            result['audit_cpu_seconds'] = time.process_time()-study_start
            result['manifest_checked_files'] = checked
            results.append(result)
            print(canonical({'study': study['id'], 'passed': result['passed'], 'audit_cpu_seconds': result['audit_cpu_seconds']}), flush=True)
    except Exception as exc:
        failure = {'study': study.get('id'), 'type': type(exc).__name__, 'message': str(exc),
                   'incomplete_study_dynamical_replay_progress': {k: _REPLAY_PROGRESS[k]-before_progress[k] for k in before_progress},
                   'scope': 'The current input/provenance check or audit failed. Only earlier listed studies completed; this report is not a combined pass.'}
    unchanged = all(file_digest(ROOT/name) == sha for name, sha in sources.items())
    if not unchanged and failure is None:
        failure = {'type': 'SourceMutation', 'message': 'A registered Python source changed during the combined audit'}
    return {'format': 'universe24-staged-independent-audit-v1', 'passed': failure is None,
            'manifest_sha256': file_digest(path), 'base_commit': manifest['base_commit'],
            'cpu_seconds': time.process_time()-start_cpu, 'wall_seconds': time.monotonic()-start_wall,
            'cpu_budget_seconds': max_cpu_seconds, 'platform': platform.platform(), 'machine': platform.machine(),
            'logical_processors': os.cpu_count(), 'python_version': platform.python_version(),
            'peak_resident_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
            'independent_auditor_sha256': file_digest(__file__), 'studies': results,
            'execution_git_identity': git_identity, 'execution_source_sha256': sources,
            'execution_sources_unchanged': unchanged,
            'failure': failure,
            'claim_limit': 'Audit pass means correspondence to the frozen definitions and complete records, not success of every scientific target or proof of physical reality.'}



def transmission_observations(case, states):
    protocol = phase_base_protocol(case)
    out = interaction_observations(protocol, case, states)
    c, delay = case['side']//2, case['delay']
    source = c-16-delay
    def matches(t, x):
        actual = {a: v for a, v in states[t].cells.items() if x-1 <= a[0] <= x+4 and abs(a[1]-c) <= 1 and abs(a[2]-c) <= 1}
        return actual == packet_template(x, c, c, 1)
    incoming = [{'step': t, 'origin_x': source+t, 'full_template_equal': matches(t, source+t)} for t in range(delay+4, delay+8)]
    forward = [{'step': 24+delay+k, 'origin_x': c+8+k, 'full_template_equal': matches(24+delay+k, c+8+k)} for k in range(4)]
    addresses = [(c, c+1, c, g) for g in range(48)]
    _, initial_terms = input_terms(states[0], addresses, (1, 1, 1))
    donors = [[term['address'] for term in row] for row in initial_terms]
    weights = [[term['weight'] for term in row] for row in initial_terms]
    inputs = []
    for t, state in enumerate(states[:-1], 1):
        sums, terms = input_terms(state, addresses, (1, 1, 1))
        inputs.append({'update': t, 'six_signed_terms': [[term['weight']*int(term['b']) for term in row] for row in terms], 'input_sums': sums})
    edge = min((min(q, states[0].side-1-q) for a, v in states[0].cells.items() if any(v[:2]) for q in a[:3]), default=None)
    out.update(incoming_fixed=incoming, forward_fixed=forward, incoming_complete=all(row['full_template_equal'] for row in incoming),
               forward_complete=all(row['full_template_equal'] for row in forward),
               clock_node_inputs={'position': [c, c+1, c], 'donor_addresses': donors, 'weights': weights, 'trace': inputs},
               minimum_initial_active_boundary_distance=edge)
    return out


def audit_transmission(folder, *, deadline=None):
    folder = Path(folder)
    protocol, result, registration = load(folder/'protocol.json'), load(folder/'result.json'), load(folder/'registration.json')
    protocol_hash = '5ecb50a57920ce4ba2c730ecd418dabc588aaafd61315cb38b76bef1ef57d18d'
    assert file_digest(folder/'protocol.json') == protocol_hash == result['protocol_sha256'] == registration['protocol_sha256']
    for path, sha in registration['source_sha256'].items():
        assert file_digest(ROOT/path) == sha, ('Transmission source changed', path)
    geometries = []
    for family, side, delay in itertools.product(('enable', 'aligned_suppress'), (137, 193), (4, 5, 8, 9)):
        phase = ((2 if family == 'enable' else 0)-delay) % 4
        geometries.append({'id': f'transmission-{family}-L{side}-d{delay}', 'family': family, 'side': side, 'delay': delay,
                           'phase': phase, 'stage': 'base', 'guide_target_channel': 0, 'clock_remainder': 0, 'compensation_direction': None})
    assert registration['planned_groups'] == geometries
    assert result['status'] == 'completed' and result['completed_cases'] == 64
    assert len(result['cases']) == 64 and len(result['groups']) == 16
    assert {p.name for p in (folder/'records').glob('*.json.gz')} == {g['id']+'-'+mask+'.json.gz' for g in geometries for mask in ('00', '10', '01', '11')}
    groups, records = [], []
    for i, geometry in enumerate(geometries):
        rows = {}
        for j, mask in enumerate(('00', '10', '01', '11')):
            case = {**geometry, 'control': mask}
            ledger = result['cases'][4*i+j]
            path = folder/ledger['record']
            assert file_digest(path) == ledger['record_gzip_sha256']
            record = load(path)
            assert record['case'] == record['spec']['controls'] == ledger['case'] == case
            native = {k: v for k, v in record.items() if k != 'observations'}
            replay, states = audit_record(native, expected_initial=interaction_initial(phase_base_protocol(case), case), deadline=deadline)
            observed = transmission_observations(case, states)
            assert observed == record['observations'], ('Transmission observer mismatch', geometry['id'], mask)
            assert record['assessment'] == result['groups'][i]
            assert ledger['fixed_forward'] == observed['forward_complete'] and ledger['all_C_count'] == len(observed['all_C'])
            rows[mask] = {'states': states, 'observations': observed, 'experiment': record['experiment']}
            records.append({'id': ledger['id'], 'record_sha256': file_digest(path), 'states': 41, 'forward_inverse_transitions': 40,
                            'all_C_count': len(observed['all_C']), 'full_rewind_equal': True})
        c, x = geometry['side']//2, geometry['side']//2-16-geometry['delay']
        h = coupling((1, 1, 1)).ports[2][0]
        packet, clock = [(a, c, c, g) for a in range(x, x+4) for g in (0, 14)], [(c, c+1, c, h)]
        for on, off, addresses in (('11', '01', packet), ('10', '00', packet), ('11', '10', clock), ('01', '00', clock)):
            assert source_control(rows[on]['states'][0], rows[off]['states'][0], addresses) == sorted(addresses)
        predictions = {'00': False, '10': geometry['family'] == 'aligned_suppress', '01': False, '11': geometry['family'] == 'enable'}
        controls = {}
        for mask, row in rows.items():
            out = row['observations']
            incoming = [v['full_template_equal'] for v in out['incoming_fixed']]
            forward = [v for v in out['outgoing_carriers'] if v['direction'] == 1]
            backward = [v for v in out['outgoing_carriers'] if v['direction'] == -1]
            checks = {'incoming_prediction': all(incoming) if mask[0] == '1' else not any(incoming),
                      'fixed_forward_prediction': out['forward_complete'] == predictions[mask],
                      'no_unexpected_late_forward': predictions[mask] or not forward,
                      'no_backward_carrier': not backward, 'no_active_boundary': not out['active_boundary_hits'],
                      'initial_boundary_margin': out['minimum_initial_active_boundary_distance'] is None or out['minimum_initial_active_boundary_distance'] > 40,
                      'full_state_inverse': True}
            controls[mask] = {'checks': checks, 'passed': all(checks.values()), 'expected_forward': predictions[mask],
                              'observed_forward': out['forward_complete'], 'forward_scan': forward, 'backward_scan': backward,
                              'all_C_count': len(out['all_C']), 'center_C_count': len(out['center_C'])}
        hashes = {mask: row['experiment']['frames'][-1]['state_sha256'] for mask, row in rows.items()}
        final_on, final_off = rows['11']['states'][-1], rows['10']['states'][-1]
        changed = [a for a in final_on.cells.keys() | final_off.cells.keys() if final_on.at(a) != final_off.at(a)]
        outside = [a for a in changed if not (c+7 <= a[0] <= c+15 and abs(a[1]-c) <= 1 and abs(a[2]-c) <= 1)]
        clock_states = rows['01']['states']
        checks = {'matched_initial_remainders': True, 'source_counter_masks_disjoint': not (set(packet) & set(clock)),
                  'source_counter_masks_exact': True, 'null_static': all(s == rows['00']['states'][0] for s in rows['00']['states']),
                  'clock_only_full_period4': all(a == b for a, b in zip(clock_states, clock_states[4:])),
                  'four_final_states_distinct': len(set(hashes.values())) == 4, 'all_control_predictions': all(v['passed'] for v in controls.values())}
        group = {'geometry': geometry, 'checks': checks, 'passed': all(checks.values()), 'controls': controls,
                 'full_state_final_hashes': hashes, 'clock_control_final_differences': len(changed),
                 'clock_control_final_differences_outside_outlet_region': len(outside),
                 'effective_coupler_supported': all(checks.values()), 'splitter_or_payload_release_established': False}
        assert group == result['groups'][i], ('Transmission acceptance mismatch', geometry['id'])
        groups.append(group)
    passed = sum(g['passed'] for g in groups)
    assert passed == result['passed_groups'] and result['accepted'] == (passed == 16)
    return {'passed': True, 'kind': 'interaction_transmission', 'protocol_sha256': protocol_hash,
            'full_recordings_independently_replayed': 64, 'complete_states': 2624,
            'forward_transitions': 2560, 'inverse_transitions': 2560, 'full_reverse_traversals': 64,
            'passed_groups': passed, 'registered_transmission_acceptance': passed == 16,
            'all_world_C_and_all48_six_input_terms_checked': True, 'source_controls_checked': True,
            'scope': 'Prepared counter state controls exact carrier transmission under separately registered enabling/suppressing preparations; no runtime switch, splitter, incoming-written controller, total-output silence or stored-payload release is established.',
            'groups': groups, 'records': records}



def audit_recipe_demo(folder, *, deadline=None):
    folder = Path(folder)
    protocol, result, registration = load(folder/'protocol.json'), load(folder/'result.json'), load(folder/'registration.json')
    protocol_hash = digest(protocol)
    assert protocol_hash == registration['protocol_sha256'] == '4b10e5df4c853b0ac173fe3767a94e8e0d2a740c1134f67719ef2c572cf765e3'
    assert result['status'] == 'completed' and result['new_scope_claim'] is False
    for path, sha in registration['source_sha256'].items():
        if file_digest(ROOT/path) != sha:
            assert path == 'research/staged_blocks/stages.json'
            assert sha in {file_digest(p) for p in (ROOT/'research/staged_blocks/evidence/catalog_history').glob('*.json')}
    assert registration['source_sha256'] == result['source_sha256']
    reference_folder = ROOT/'research/staged_blocks/evidence/interactions/phase_v1'
    certificate = load(folder/'trajectory_equivalence.json')
    reports = []
    for index, mask in enumerate(('00', '10', '01', '11')):
        case = {'side': 129, 'clock_remainder': 0, 'phase': 0, 'delay': 1,
                'guide_target_channel': 0, 'compensation_direction': None, 'control': mask}
        identity = 'recipe-phase-L129-r0-p0-d1-'+mask
        path = folder/'records'/(identity+'.json.gz')
        record = load(path)
        assert record['spec'] == protocol['specs'][index]
        replay, states = audit_record(record, expected_initial=phase_initial(case), deadline=deadline)
        reference = load(reference_folder/'records'/('phase-L129-r0-p0-d1-'+mask+'.json.gz'))
        assert record['experiment']['frames'] == reference['experiment']['frames']
        row = certificate['rows'][index]
        assert row['control'] == mask and file_digest(path) == row['new_record_sha256']
        assert file_digest(reference_folder/'records'/('phase-L129-r0-p0-d1-'+mask+'.json.gz')) == row['old_record_sha256']
        assert result['records'][index]['state_hashes'] == [f['state_sha256'] for f in record['experiment']['frames']]
        relative = record['relative_phase']
        assert relative['observer'] == protocol['observer']
        target, reference_address = (64, 65, 64, 2), (64, 88, 88, 0)
        expected = []
        for t, state in enumerate(states):
            a, b, r = state.at(target)
            c, d, rr = state.at(reference_address)
            dot, cross, energy, ref_energy = a*c+b*d, a*d-b*c, a*a+b*b, c*c+d*d
            events = []
            if t:
                for role, address in (('target', target), ('reference', reference_address)):
                    before, after = states[t-1].at(address), state.at(address)
                    ell = before[0]+after[1]
                    if ell and before != after:
                        events.append({'role': role, 'kind': ((after[2]-before[2])//2) % 3, 'ell': ell})
            expected.append({'step': t, 'D': dot, 'X': cross, 'I_target': energy, 'I_reference': ref_energy,
                             'target_remainder': r, 'reference_remainder': rr,
                             'arithmetic_events': events, 'identity_equal': dot*dot+cross*cross == energy*ref_energy})
        assert expected == relative['trace']
        assert [(v['D'], v['X']) for v in expected] == [(v['D'], v['X']) for v in reference['observations']['phase_trace']]
        reports.append({'id': identity, 'record_sha256': file_digest(path), 'complete_states': 41,
                        'forward_inverse_transitions': 40, 'full_rewind_equal': True, 'exact_original_full_frames_equal': True})
    # Exercise the reusable constructor over the entire validated initial family;
    # compare to independent matrix-derived preparation, without new evolution.
    from research.staged_blocks.recipes import phase_assembly
    prep_result = load(ROOT/'research/staged_blocks/evidence/recipe_equivalence/result.json')
    assert file_digest(ROOT/'research/staged_blocks/recipes.py') == prep_result['recipe_source_sha256']
    assert file_digest(reference_folder/'result.json') == prep_result['registered_phase_result_sha256']
    assert len(prep_result['rows']) == 256 and prep_result['cases'] == 256
    prepared = []
    for index, (side, r, phase, delay, mask) in enumerate(itertools.product((129, 161), (0, 4), range(4), (1, 2, 3, 5), ('00', '10', '01', '11'))):
        if deadline is not None and time.process_time() > deadline:
            raise TimeoutError('Recipe preparation audit CPU limit')
        case = {'side': side, 'clock_remainder': r, 'phase': phase, 'delay': delay,
                'guide_target_channel': 0, 'compensation_direction': None, 'control': mask}
        spec = phase_assembly(side=side, r=r, phase=phase, delay=delay, control=mask).experiment_spec()
        initial = declared_initial(spec)
        expected = phase_initial(case)
        assert initial == expected
        identity = f'phase-L{side}-r{r}-p{phase}-d{delay}-{mask}'
        historical = load(reference_folder/'records'/(identity+'.json.gz'))['experiment']
        frame0 = historical['frames'][0]
        assert initial == Snapshot(side, (0, 0, 2), {tuple(v[:4]): tuple(exact_int(x) for x in v[4:]) for v in frame0['cells']})
        assert prep_result['rows'][index] == {'id': identity, 'canonical_initial_bytes_equal': True,
                                            'recorded_initial_hash_equal': True, 'state_sha256': frame0['state_sha256']}
        prepared.append({'id': identity, 'full_initial_state_equal': True})
    return {'passed': True, 'kind': 'composition_recipe_demo', 'protocol_sha256': protocol_hash,
            'full_recordings_independently_replayed': 4, 'complete_states': 164,
            'forward_transitions': 160, 'inverse_transitions': 160, 'full_reverse_traversals': 4,
            'reusable_recipe_preparations_independently_checked': 256,
            'passive_DX_and_C_recomputed': True, 'original_validated_full_frames_equal': True,
            'scope': 'Four reusable initial-data pieces reproduce the existing finite phase family exactly. Preparation equivalence does not enlarge behavioral scope; the passive D/X observer is not a physical comparator.',
            'preparations': prepared, 'records': reports}



def bridge_initial(case):
    side, delay, mask = case['side'], case['delay'], case['control']
    assert side in (129, 161) and delay in range(4)
    c, x0 = side//2, side//2-24-delay
    matrix = coupling((1, 1, 1))
    inverse = [{sender: receiver for receiver, sender in enumerate(row)} for row in matrix.ports]
    cells, debt, contributions, sources = {}, Counter(), {}, {}
    lanes = (('lower', 0, 14, 0, (0, 4, 8)), ('upper', 6, 36, 2, (2, 6)))
    for lane, (name, primary, companion, dy, starts) in enumerate(lanes):
        selected = starts if case['stage'] != 'pristine' or mask[lane] == '1' else ()
        def A(i):
            return sum(i == start or i == start+1 for start in selected)
        sources[name] = []
        for x in range(side):
            i = x-x0
            a, b, r = A(i)-A(i-1), A(i-1)-A(i-2), 4*(A(i)+A(i-2))
            assert 0 <= r < 6
            for g, sign, remainder in ((primary, 1, r), (companion, -1, 4-r)):
                address = (x, c+dy, c, g)
                assert address not in cells
                if a or b:
                    sources[name].append(list(address))
                cells[address] = (sign*a if mask[lane] == '1' else 0, sign*b if mask[lane] == '1' else 0, remainder)
                if A(i-1):
                    for d, delta in enumerate(DIRECTIONS[2:], 2):
                        recipient = (*[address[j]+delta[j] for j in range(3)], inverse[d ^ 1][g])
                        weight = matrix.weights[d ^ 1][recipient[3]]
                        value = sign*weight*A(i-1)
                        debt[recipient] += value
                        contributions.setdefault(recipient, []).append({'lane': name, 'source': list(address), 'direction': d, 'contribution': value})
    shared = []
    for address, value in sorted(debt.items()):
        assert address not in cells
        r = 2-2*value
        assert 0 <= r < 6
        cells[address] = (0, 0, r)
        if len(contributions[address]) > 1:
            shared.append({'address': list(address), 'contributions': contributions[address], 'remainder': r})
    center, replacements = (c, c+1, c), []
    if case['stage'] != 'pristine':
        phase = case['phase']
        address = (*center, 2)
        assert address not in cells
        cells[address] = (*((0, 1), (1, 0), (0, -1), (-1, 0))[phase], 0)
        sources['clock'] = [list(address)]
        for d, delta in enumerate(DIRECTIONS):
            recipient = (*[center[j]+delta[j] for j in range(3)], inverse[d ^ 1][2])
            old = cells.get(recipient, (0, 0, 2))
            r0 = 0 if d in (2, 3) else 2
            assert old == (0, 0, r0)
            new = (0, 0, r0+2*(phase in (1, 2)))
            cells[recipient] = new
            replacements.append({'address': list(recipient), 'before': list(old), 'after': list(new)})
    metadata = {'origin_x': x0, 'center': list(center), 'shared_halo_assignments': shared,
                'clock_joint_replacements': replacements,
                'halo_contribution_sha256': digest({str(a): rows for a, rows in sorted(contributions.items())}),
                'sources': {key: value for key, value in sources.items() if value}}
    return Snapshot(side, (0, 0, 2), cells), metadata


def bridge_observations(case, states):
    protocol = phase_base_protocol(case)
    protocol['geometry']['packet_x'] = case['side']//2-24-case['delay']
    protocol['readouts']['eligible_hold_starts'] = []
    observations = interaction_observations(protocol, case, states)
    for t, row in enumerate(observations['center_inputs']):
        row['ell'] = observations['center_trace'][t+1][1]+observations['center_trace'][t][0]
    return observations


def bridge_verdict(case, states, out):
    if case['stage'] == 'pristine':
        mismatch = next((t for t, state in enumerate(states) if state != Snapshot(state.side, state.background, {((a[0]+t) % state.side, *a[1:]): v for a, v in states[0].cells.items()})), None)
        return {'complete_translation': mismatch is None, 'first_translation_mismatch': mismatch,
                'active_boundary_hits': len(out['active_boundary_hits'])}
    T = 14+case['delay']
    word = out['center_inputs'][T-1:T+10]
    center, region = out['center_trace'], out['region_trace']
    expected_inputs = [-1]+[0]*9+[1]
    lower = [-1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1]
    upper = [0, 0, -1, 0, 1, 0, -1, 0, 1, 0, 0]
    node = [frame[:48] for frame in region[T:T+10]]
    events = [{k: e[k] for k in ('step', 'kind', 'ell')} for e in out['center_C'] if T <= e['step'] <= T+10]
    items = [('registered_prestate', center[T-1], [-1, 0, 0]),
             ('net_word', [row['u'] for row in word], expected_inputs),
             ('lower_word', [row['terms'][3]['term'] for row in word], lower),
             ('upper_word', [row['terms'][2]['term'] for row in word], upper),
             ('other_four_input_terms_zero', all(row['terms'][d]['term'] == 0 for row in word for d in (0, 1, 4, 5)), True),
             ('clock_pause_states', center[T:T+10], [[0, 0, 4]]*10),
             ('complete_center_node_unchanged', all(frame == node[0] for frame in node), True),
             ('complete_center_node_zero_counters', all(not any(v[:2]) for frame in node for v in frame), True),
             ('clock_restart', center[T+10], [0, 1, 0]),
             ('registered_clock_C', events, [{'step': T, 'kind': 2, 'ell': -1}, {'step': T+10, 'kind': 1, 'ell': 1}]),
             ('endpoint_quotients', [word[0]['ell'], word[-1]['ell']], [-1, 1])]
    checks = [{'condition': name, 'passed': actual == expected, 'actual': actual, 'expected': expected} for name, actual, expected in items]
    holds = []
    for start in (T, T+1):
        frames = region[start:start+9]
        holds.append({'start': start, 'through': start+8,
                      'all_336_counters_zero': all(not any(v[:2]) for frame in frames for v in frame),
                      'all_336_triples_unchanged': all(frame == frames[0] for frame in frames),
                      'target_remainder4': center[start][2] == 4,
                      'every_external_term_zero': all(not row['nonzero_external_terms'] for row in out['boundary_inputs'][start:start+8])})
    autonomous = any(all(value for key, value in hold.items() if key not in ('start', 'through')) for hold in holds)
    return {'first_update': T, 'last_update': T+10, 'outcome_A_autonomous': autonomous,
            'autonomous_windows': holds, 'outcome_B_word_pause_restart': all(c['passed'] for c in checks),
            'checks': checks, 'first_mismatch': next((c for c in checks if not c['passed']), None),
            'canceling_input_updates': [{'update': row['update'], 'terms': [term['term'] for term in row['terms']]} for row in word if row['u'] == 0 and any(term['term'] for term in row['terms'])],
            'center_C_count_full_horizon': len(out['center_C']), 'all_C_count': len(out['all_C']),
            'active_boundary_hits': len(out['active_boundary_hits'])}


def audit_bridge(folder, *, deadline=None):
    folder = Path(folder)
    protocol, result, registration = load(folder/'protocol.json'), load(folder/'result.json'), load(folder/'registration.json')
    protocol_hash = '546ac6077a371c45e7556cd1f47cd41224b4a610997042334cd9828b19c25325'
    assert file_digest(folder/'protocol.json') == protocol_hash == registration['protocol_sha256'] == result['protocol_sha256']
    for path, sha in registration['source_sha256'].items():
        assert file_digest(ROOT/path) == sha, ('Bridge source changed', path)
    cases = [{'id': f'bridge-pristine-L{side}-{label}', 'side': side, 'delay': 0, 'phase': 0, 'stage': 'pristine',
              'guide_target_channel': 0, 'control': mask} for side in (129, 161) for label, mask in (('lower', '10'), ('upper', '01'), ('combined', '11'))]
    geometries = [{'id': f'bridge-L{side}-d{delay}', 'side': side, 'delay': delay, 'phase': (2-delay) % 4,
                   'stage': 'encounter', 'guide_target_channel': 0} for side, delay in itertools.product((129, 161), range(4))]
    cases += [{**g, 'control': mask} for g in geometries for mask in ('00', '10', '01', '11')]
    assert registration['cases'] == cases and result['status'] == 'completed' and result['completed_cases'] == 38
    assert len(result['cases']) == 38 and len(result['groups']) == 8
    assert {p.name for p in (folder/'records').glob('*.json.gz')} == {c['id']+'-'+c['control']+'.json.gz' for c in cases}
    records, group_rows, groups, pristine_passes = [], {}, [], 0
    for i, case in enumerate(cases):
        ledger = result['cases'][i]
        path = folder/ledger['record']
        record = load(path)
        assert case == ledger['case'] == record['spec']['controls']
        assert file_digest(path) == ledger['record_gzip_sha256'] and digest(record) == ledger['record_sha256']
        initial, metadata = bridge_initial(case)
        assert metadata == record['spec']['provenance']['joint_preparation'], ('Bridge halo provenance mismatch', case['id'])
        native = {k: v for k, v in record.items() if k != 'observations'}
        replay, states = audit_record(native, expected_initial=initial, deadline=deadline)
        out = bridge_observations(case, states)
        assert out == record['observations'], ('Bridge actual observer mismatch', case['id'], case['control'])
        measured = bridge_verdict(case, states, out)
        assert measured == record['assessment'] == ledger['assessment'], ('Bridge acceptance mismatch', case['id'], case['control'])
        assert not out['active_boundary_hits']
        records.append({'id': ledger['id'], 'record_sha256': file_digest(path), 'states': len(states),
                        'forward_inverse_transitions': len(states)-1, 'all_C_count': len(out['all_C']), 'full_rewind_equal': True})
        if i < 6:
            pristine_passes += measured['complete_translation']
            assert record['group_assessment'] is None
            continue
        group_rows[case['control']] = {'states': states, 'out': out, 'verdict': measured, 'metadata': metadata, 'experiment': record['experiment']}
        if case['control'] != '11':
            continue
        rows = group_rows
        lower, upper = metadata['sources']['lower'], metadata['sources']['upper']
        for on, off, addresses in (('11', '01', lower), ('10', '00', lower), ('11', '10', upper), ('01', '00', upper)):
            assert source_control(rows[on]['states'][0], rows[off]['states'][0], addresses) == sorted(map(tuple, addresses))
        control_fail = all(not rows[mask]['verdict']['outcome_B_word_pause_restart'] for mask in ('00', '10', '01'))
        null = rows['00']['states']
        group = {'geometry': geometries[len(groups)], 'matched_initial_remainders': True,
                 'null_clock_complete_period4': all(a == b for a, b in zip(null, null[4:])),
                 'outcome_A_autonomous': measured['outcome_A_autonomous'],
                 'outcome_B_driven_pause': control_fail and measured['outcome_B_word_pause_restart'],
                 'all_controls_fail_complete_bridge': control_fail,
                 'case_verdicts': {mask: row['verdict'] for mask, row in rows.items()},
                 'final_state_hashes': {mask: row['experiment']['frames'][-1]['state_sha256'] for mask, row in rows.items()},
                 'scope': 'Prearranged two-train driven waiting; not an independent approval computation.'}
        assert group == result['groups'][len(groups)] == record['group_assessment']
        groups.append(group)
        group_rows = {}
    counts = {'pristine_translation_passes': pristine_passes,
              'outcome_A_autonomous_groups': sum(g['outcome_A_autonomous'] for g in groups),
              'outcome_B_driven_pause_groups': sum(g['outcome_B_driven_pause'] for g in groups)}
    assert all(result[k] == value for k, value in counts.items())
    return {'passed': True, 'kind': 'interaction_bridge', 'protocol_sha256': protocol_hash,
            'full_recordings_independently_replayed': 38, 'complete_states': 1366,
            'forward_transitions': 1328, 'inverse_transitions': 1328, 'full_reverse_traversals': 38,
            'joint_initial_halo_independently_constructed': True, 'all_six_actual_terms_and_full48_and336_regions_checked': True,
            'all_world_C_and_all_source_controls_checked': True,
            'scope': 'Autonomous protected-region memory and internally driven net-zero center waiting are independently distinct predicates. Prearranged initial trains do not compute approval or establish one C per source.',
            **counts, 'groups': groups, 'records': records}



def portable_snapshot_digest(state):
    return digest({'side': state.side, 'background': [str(state.background[0]), str(state.background[1]), state.background[2]],
                   'cells': [[*a, str(v[0]), str(v[1]), v[2]] for a, v in sorted(state.cells.items())]})


def translated_snapshot(state, q):
    return Snapshot(state.side, state.background,
                    {(*[(a[j]+q[j]) % state.side for j in range(3)], a[3]): v for a, v in state.cells.items()})


def motion_comparison(states, period, displacement):
    shifted = [translated_snapshot(s, displacement) for s in states]
    matches, mismatch = [], None
    for t in range(len(states)-period):
        actual, expected = states[t+period], shifted[t]
        if actual == expected:
            matches.append(t)
        elif mismatch is None:
            address = next(a for a in sorted(actual.cells.keys() | expected.cells.keys()) if actual.at(a) != expected.at(a))
            mismatch = {'start_step': t, 'end_step': t+period, 'address': list(address),
                        'actual': [str(v) for v in actual.at(address)], 'expected': [str(v) for v in expected.at(address)]}
    alias = all(q % states[0].side == 0 for q in displacement)
    invariant = shifted[0] == states[0]
    equal = len(matches) == len(states)-period
    return {'period': period, 'displacement': list(displacement), 'comparison_count': len(states)-period,
            'matching_start_steps': matches, 'all_complete_comparisons_equal': equal,
            'shift_aliases_identity': alias, 'initial_translation_invariant': invariant,
            'nontrivial_relative_periodicity': equal and not alias and not invariant, 'first_mismatch': mismatch}


def audit_motion(folder, *, deadline=None):
    folder = Path(folder)
    protocol, result, registration = load(folder/'protocol.json'), load(folder/'result.json'), load(folder/'registration.json')
    protocol_hash = '0953cffb1815d8b6677668fccdd02c75958b3c243306875e3804b4352694c620'
    assert file_digest(folder/'protocol.json') == protocol_hash == result['protocol_sha256'] == registration['protocol_sha256']
    for path, sha in registration['source_sha256'].items():
        assert file_digest(ROOT/path) == sha, ('Motion source changed', path)
    assert protocol['periods'] == [1, 2, 3, 4] and protocol['relative_shifts'] == [list(d) for d in DIRECTIONS]
    assert protocol['static_translations'] == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert protocol['observer_displacements'] == [[0, 0, 0], [1, 0, 0]]
    assert result['status'] == 'completed' and result['completed_recordings'] == len(protocol['sources']) == 13
    assert len(result['analyses']) == 13 and result['new_native_experiment_records'] == 0
    samples_path = folder/result['observer_samples']['path']
    assert file_digest(samples_path) == result['observer_samples']['sha256']
    samples = load(samples_path)
    assert samples['native_trajectories_rewritten'] is False and len(samples['records']) == 13
    reports, comparisons, covariance_count, total_frames = [], 0, 0, 0
    for index, source in enumerate(protocol['sources']):
        path = ROOT/source['path']
        assert file_digest(path) == source['sha256']
        record, saved = load(path), result['analyses'][index]
        native = {k: v for k, v in record.items() if k != 'observations'}
        replay, states = audit_record(native, deadline=deadline)
        assert len(states) == source['frames'] and states[0].side == source['side']
        assert saved['id'] == record['experiment']['id'] == source['id']
        signs = tuple(record['experiment']['coupling']['body_signs'])
        relative = [motion_comparison(states, p, q) for q in DIRECTIONS for p in range(1, 5)]
        ordinary = [motion_comparison(states, p, (0, 0, 0)) for p in range(1, 5)]
        assert relative == saved['relative_periodicity'] and ordinary == saved['ordinary_periodicity']
        comparisons += sum(r['comparison_count'] for r in relative)
        covariance = []
        for t in (0, len(states)-2):
            for q in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                old, expected = translated_snapshot(states[t], q), translated_snapshot(states[t+1], q)
                actual = advance(old, signs)
                assert actual == expected and rewind(actual, signs) == old
                covariance.append({'native_start_step': t, 'displacement': list(q),
                                   'translated_initial_sha256': portable_snapshot_digest(old),
                                   'translated_expected_sha256': portable_snapshot_digest(expected),
                                   'engine_forward_sha256': portable_snapshot_digest(actual),
                                   'forward_equal': True, 'full_inverse_equal': True, 'first_mismatch': None})
        assert covariance == saved['static_translation_checks']
        covariance_count += len(covariance)
        total_frames += len(states)
        actual_observers = []
        for q in ((0, 0, 0), (1, 0, 0)):
            rows = []
            for t, state in enumerate(states):
                position = tuple((source['observer_origin'][j]+t*q[j]) % state.side for j in range(3))
                rows.append({'native_step': t, 'native_position': list(position), 'native_state_sha256': portable_snapshot_digest(state),
                             'full_48_channel_node': [[str(v) for v in state.at((*position, g))] for g in range(48)]})
            actual_observers.append({'format': 'universe24-passive-native-address-observer-v1', 'origin': source['observer_origin'],
                                     'displacement_per_sample': list(q), 'native_steps_per_sample': 1,
                                     'mutates_or_evolves_state': False, 'is_native_engine_trajectory': False, 'samples': rows})
        assert samples['records'][index] == {'recording_id': source['id'], 'native_record_sha256': source['sha256'], 'observers': actual_observers}
        found = [{'period': row['period'], 'displacement': row['displacement']} for row in relative if row['nontrivial_relative_periodicity']]
        assert saved['nontrivial_matches'] == found
        expected = source['expected_motion']
        checks = {'motion_expectation': ({'period': 1, 'displacement': [1, 0, 0]} in found) if expected == 'carrier_plus_x' else not found}
        if 'expected_ordinary_period' in source:
            checks['ordinary_period_expectation'] = ordinary[source['expected_ordinary_period']-1]['all_complete_comparisons_equal']
        if expected == 'trivial_symmetry_only':
            checks['raw_equalities_rejected_as_static_symmetry'] = all(row['all_complete_comparisons_equal'] and row['initial_translation_invariant'] and not row['nontrivial_relative_periodicity'] for row in relative)
        checks.update(all_static_covariance_checks=True, native_states_unchanged=True)
        assert checks == saved['checks'] and saved['expectations_passed'] == all(checks.values())
        reports.append({'id': source['id'], 'object_scope': source['object_scope'], 'native_record_sha256': source['sha256'],
                        'complete_frames': len(states), 'native_full_replay': True, 'nontrivial_matches': found,
                        'ordinary_periods': [r['period'] for r in ordinary if r['all_complete_comparisons_equal']],
                        'scope': 'All native starts, p1..4 and six unit shifts only.'})
    assert comparisons == 8556 and covariance_count == 78 and total_frames == 389
    apparatus = any(row['nontrivial_matches'] for row in reports if row['object_scope'] == 'complete_apparatus')
    assert result['whole_apparatus_motion_established'] == apparatus is False
    assert result['accepted'] is True and result['moving_detector_or_clock_established'] is False
    return {'passed': True, 'kind': 'motion', 'protocol_sha256': protocol_hash,
            'existing_native_recordings_independently_replayed': 13, 'existing_complete_states': total_frames,
            'existing_forward_transitions': total_frames-13, 'existing_inverse_transitions': total_frames-13,
            'relative_parameter_pairs_checked': 312, 'complete_state_pair_comparisons': comparisons,
            'independent_translated_forward_inverse_checks': covariance_count, 'all_passive_full48_samples_checked': True,
            'new_native_experiment_records': 0, 'whole_apparatus_motion_established': False,
            'scope': 'Static translation covariance and passive sampling are not moving physical observers. Carrier translation passes; full-apparatus motion has no match only in this finite p/shift family.', 'sources': reports}



def audit_composed_recipes(folder, *, deadline=None):
    folder = Path(folder)
    protocol, result = load(folder/'protocol.json'), load(folder/'result.json')
    protocol_hash = '255c2f26e6723bf6048d4912e7dd9221f4f6a6e5c8657874ebf218d0cf59df2c'
    assert file_digest(folder/'protocol.json') == protocol_hash == result['protocol_sha256']
    assert protocol['counts'] == result['counts'] == {'effective_coupler': 64, 'driven_pause': 32}
    assert result['cases'] == 96 and result['new_trajectories_generated'] == 0 and result['status'] == 'passed'
    for field in ('source_sha256', 'frozen_protocol_sha256', 'frozen_result_sha256', 'record_gzip_sha256'):
        for name, sha in protocol[field].items():
            assert file_digest(ROOT/name) == sha, ('Composed recipe pinned input changed', name)
    from research.staged_blocks.composed_recipes import effective_coupler, two_lane_pause
    names = [('effective_coupler', p) for p in sorted((ROOT/'research/staged_blocks/evidence/transmission_v1/records').glob('*.json.gz'))]
    names += [('driven_pause', p) for p in sorted((ROOT/'research/staged_blocks/evidence/pause_bridge_v1/records').glob('bridge-L*.json.gz'))]
    assert {str(p.relative_to(ROOT)) for _, p in names} == set(protocol['record_gzip_sha256']) and len(names) == len(result['rows']) == 96
    reports = []
    for index, (kind, path) in enumerate(names):
        if deadline is not None and time.process_time() > deadline:
            raise TimeoutError('Composed recipe audit CPU budget exhausted')
        record = load(path)
        case = record['spec']['controls']
        kwargs = {key: case[key] for key in ('side', 'delay', 'control')}
        if kind == 'effective_coupler':
            constructor = effective_coupler(family=case['family'], **kwargs)
            expected = interaction_initial(phase_base_protocol(case), case)
        else:
            constructor = two_lane_pause(**kwargs)
            expected, _ = bridge_initial(case)
        initial = declared_initial(constructor.experiment_spec())
        assert initial == expected, ('Public recipe differs from independent algebra', kind, case)
        experiment, frame0 = record['experiment'], record['experiment']['frames'][0]
        stored = Snapshot(experiment['side'], tuple(exact_int(v) for v in experiment['background']),
                          {tuple(v[:4]): tuple(exact_int(x) for x in v[4:]) for v in frame0['cells']})
        assert initial == stored and portable_snapshot_digest(initial) == frame0['state_sha256']
        row = {'id': record['spec']['id'], 'kind': kind, 'record': str(path.relative_to(ROOT)),
               'canonical_initial_bytes_equal': True, 'recorded_initial_hash_equal': True,
               'state_sha256': frame0['state_sha256']}
        assert result['rows'][index] == row
        reports.append(row)
    return {'passed': True, 'kind': 'composition_public_recipe_equivalence', 'protocol_sha256': protocol_hash,
            'independently_reconstructed_initial_states': 96, 'counts': protocol['counts'],
            'new_trajectories_generated': 0, 'all_pinned_inputs_verified': True,
            'scope': 'Public immutable constructors reproduce all64 transmission and32 driven-pause initial states and independent algebra. No new behavior, autonomous memory or approval claim is introduced.',
            'preparations': reports}


def audit_waveform_scalars(folder):
    """Check retrospective actual inputs and identities without new trajectories."""
    folder = Path(folder)
    registration, result = load(folder/'registration.json'), load(folder/'result.json')
    assert file_digest(folder/'protocol.json') == registration['protocol_sha256'] == result['protocol_sha256']
    assert file_digest(ROOT/'research/staged_blocks/waveform_analysis.py') == registration['observer_source_sha256']
    checked = 0
    for source in registration['sources']:
        native_path = ROOT/source['path']
        assert file_digest(native_path) == source['sha256']
        record, saved = load(native_path), load(folder/'records'/(source['id']+'.json.gz'))
        assert saved['source_sha256'] == source['sha256'] and saved['source_record'] == source['path']
        states = read_states(record['experiment'])
        signs = record['experiment']['coupling']['body_signs']
        for label, probe in saved['probes'].items():
            addresses = [(*probe['position'], g) for g in range(48)]
            expected_states = [[list(s.at(a)) for a in addresses] for s in states]
            assert expected_states == probe['states']
            cumulative_u, cumulative_ell = [0]*48, [0]*48
            for t, (old, new) in enumerate(zip(states, states[1:])):
                sums, terms = input_terms(old, addresses, signs)
                step = probe['transitions'][t]
                assert step['old_state'] == t and step['new_state'] == t+1
                for g, address in enumerate(addresses):
                    before, after = old.at(address), new.at(address)
                    u, ell = sums[g], after[1]+before[0]
                    assert after[0] == before[1] and divmod(2*u+before[2], 6) == (ell, after[2])
                    cumulative_u[g] += u
                    cumulative_ell[g] += ell
                    assert after[2]-states[0].at(address)[2] == 2*cumulative_u[g]-6*cumulative_ell[g]
                    assert sum(v*v for v in after[:2])-sum(v*v for v in before[:2]) == ell*ell-2*before[0]*ell
                    event = {'kind': ((after[2]-before[2])//2) % 3, 'ell': ell} if ell and before != after else None
                    row = {'channel': g, 'u': u, 'ell': ell,
                           'terms': [{'direction': term['direction'], 'sender': term['address'], 'weight': term['weight'], 'b': int(term['b']), 'term': term['weight']*int(term['b'])} for term in terms[g]],
                           'cumulative_u': cumulative_u[g], 'cumulative_ell': cumulative_ell[g], 'C': event,
                           'r_change': after[2]-before[2], 'counter_change': before[:2] != after[:2],
                           'returns_to_initial_triple': after == states[0].at(address)}
                    assert row == step['channels'][g], ('Waveform scalar mismatch', source['id'], label, t, g)
                    checked += 1
            for g, summary in enumerate(probe['channels']):
                word = [step['channels'][g]['u'] for step in probe['transitions']]
                assert word == summary['input_word'] and sum(word) == summary['sum_u']
                assert cumulative_ell[g] == summary['sum_ell']
                assert summary['initial'] == expected_states[0][g] and summary['final'] == expected_states[-1][g]
                events = [{'update': t+1, **step['channels'][g]['C']} for t, step in enumerate(probe['transitions']) if step['channels'][g]['C'] is not None]
                assert events == summary['events']
    assert checked == 55296 and len(registration['sources']) == 16
    candidate = load(folder/'records/base-g0-r0-p1-dnone-11.json.gz')
    reference = load(folder/'records/base-g0-r0-p1-dnone-01.json.gz')
    g = candidate['clock_channel']
    center = candidate['probes']['clock']
    assert g == 2
    assert [(t+1, step['channels'][g]['u'], step['channels'][g]['C']) for t, step in enumerate(center['transitions']) if step['channels'][g]['u']] == [(15, -1, {'kind': 2, 'ell': -1}), (16, 1, {'kind': 1, 'ell': 1})]
    for t in range(16, 41):
        a, b, r = center['states'][t][g]
        c, d, rr = reference['probes']['clock']['states'][t][g]
        assert (a, b) == (-d, c)
        if t > 16:
            assert center['transitions'][t-1]['channels'][g]['u'] == 0
            assert center['transitions'][t-1]['channels'][g]['C'] is None
    return {'passed': True, 'protocol_sha256': registration['protocol_sha256'], 'source_records_checked': 16,
            'exact_scalar_transitions_checked': checked, 'all_six_actual_input_terms_checked': True,
            'priority_actual_word': [{'update': 15, 'u': -1, 'kind': 2, 'ell': -1}, {'update': 16, 'u': 1, 'kind': 1, 'ell': 1}],
            'retrospective_priority_phase_offset': 3, 'retrospective_priority_phase_states': [16, 40],
            'new_trajectories': 0, 'quiet_word_classifier_statuses_independently_checked': False,
            'scope': 'Independent scalar/actual-six-input/C/identity and designated retrospective phase check on previously fully replayed records. Quiet-word classification statuses are outside this audit; no new component acceptance.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--max-cpu-seconds', type=float, default=600)
    args = parser.parse_args(argv)
    if args.max_cpu_seconds <= 5:
        parser.error('The combined audit requires a CPU budget greater than five seconds')
    # Reserve two CPU seconds for recording an honest interrupted scope. The
    # kernel limit is in whole seconds; the hard limit is below the public cap.
    soft = int(time.process_time()+args.max_cpu_seconds-2)
    hard = soft+1
    resource.setrlimit(resource.RLIMIT_CPU, (soft, hard))
    def cpu_limit(_number, _frame):
        raise TimeoutError('Kernel CPU budget signal received; reserved time writes partial audit scope')
    signal.signal(signal.SIGXCPU, cpu_limit)
    result = audit_manifest(args.manifest, max_cpu_seconds=args.max_cpu_seconds)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(canonical({'passed': result['passed'], 'studies': len(result['studies']), 'cpu_seconds': result['cpu_seconds']}))
    if not result['passed']:
        raise SystemExit(1)
    return result


if __name__ == '__main__':
    main()
