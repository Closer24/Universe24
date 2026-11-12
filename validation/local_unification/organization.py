"""Predeclared repeated-use and structural controls for the shared local law.

This module observes Engine histories. It never chooses an update, resets a
record or supplies a runtime input. Functional repeated routing and spatial
motif diversity are deliberately reported as different quantities.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
from itertools import product
from pathlib import Path
import random

import numpy as np

from universe24.core import Engine, State, exact_json
from universe24.core.lattice import DIRECTIONS, lattice
from validation.selection.complexity import structure_trace, episode_gate


# Independent literal four-rail involution: only1001 and0110 exchange.
COLLISION = tuple((0, 1, 1, 0) if bits == (1, 0, 0, 1) else
                  (1, 0, 0, 1) if bits == (0, 1, 1, 0) else bits
                  for bits in product(range(2), repeat=4))
PROTOCOL = {
    "schema": "universe24/local-unification-organization/1",
    "preregistration": "https://github.com/Closer24/Universe24/issues/63#issuecomment-6813374026",
    "paired_bank_amendment": "https://github.com/Closer24/Universe24/issues/63#issuecomment-6813381567",
    "conservative_law_amendment": "https://github.com/Closer24/Universe24/issues/63#issuecomment-6813432154",
    "sides": [3, 5], "seeds": [101, 509, 2027], "steps": 24,
    "memory_preparations": ["ready", "depleted", "mixed"],
    "directions": [list(d) for d in DIRECTIONS],
    "variants": ["shared", "record_transport_off", "collision_off"],
    "collision_readout": "old B=(record+,record-,carrier+,carrier-) to new A at every microstep",
    "correction": "input(x,y)=(0,1), output(x,y)=(1,0)",
    "unsorting": "input(x,y)=(1,0), output(x,y)=(0,1)",
    "repeat_key": "same physical node and same microstep parity (one bank stream)",
    "functional_gate": "at least two corrections at one predeclared receiver/stream; all other outcomes retained",
    "structural_score": "original distinct persistent nonuniform axial Boolean carrier triples, separately per bank at two-microstep checkpoints",
    "structural_growth_gate": "original four-episode strict-growth test; no changed thresholds",
    "claim": "Finite prepared repeat use is distinct from sustained structural growth and physical acceptance",
}


def _digest(value):
    return hashlib.sha256(exact_json.dumps(value, sort_keys=True).encode()).hexdigest()


def _bit(value):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or int(value) not in (0, 1):
        raise ValueError("Boolean carrier/record readout requires exact bits")
    return int(value)


def _rows(state):
    if not isinstance(state, State) or state.G != 8:
        raise ValueError("the declared paired-bank law has eight complete channels")
    for g in range(8):
        for value in state.b[g]:
            _bit(value)
    return state.b


def collision_rows(before, after, *, coupled=True):
    """All local outputs, checked against a literal truth table.

    This does not certify the spatial streaming, source equation or Engine
    recurrence; those require full-state replay. It also keeps ties/nulls.
    """
    left, right = _rows(before), _rows(after)
    if before.L != after.L:
        raise ValueError("collision cannot change lattice size")
    rows = []
    for n in range(before.N):
        incoming = tuple(_bit(left[g, n]) for g in (4, 5, 6, 7))
        outgoing = tuple(_bit(right[g, n]) for g in (0, 1, 2, 3))
        rp, rm, x, y = incoming
        expected = COLLISION[8*rp+4*rm+2*x+y] if coupled else incoming
        if outgoing != expected:
            raise ValueError("saved collision disagrees with independent literal permutation")
        _, _, xp, yp = outgoing
        kind = ("correction" if (x, y, xp, yp) == (0, 1, 1, 0) else
                "unsorting" if (x, y, xp, yp) == (1, 0, 0, 1) else
                "tie" if x == y else "unchanged_split")
        rows.append({"node": n, "incoming": list(incoming), "outgoing": list(outgoing),
                     "kind": kind, "ready": (rp, rm) == (1, 0),
                     "record_state": "ready" if (rp, rm) == (1, 0) else "depleted" if (rp, rm) == (0, 1) else "missing" if (rp, rm) == (0, 0) else "double",
                     "order_delta": xp-yp-x+y})
    return rows


def functional_trace(states, *, coupled=True, receiver=0, collision_phase=0):
    """Describe one predeclared receiver and the entire unfiltered history."""
    states = list(states)
    if not states or not 0 <= receiver < states[0].N or collision_phase not in (0, 1):
        raise ValueError("a valid receiver and bank-stream phase are required")
    totals = Counter()
    corrections = Counter()
    unsorting = Counter()
    counts_by_step = []
    receiver_rows = []
    for step, (before, after) in enumerate(zip(states, states[1:]), 1):
        rows = collision_rows(before, after, coupled=coupled)
        counts = Counter(row["kind"] for row in rows)
        counts["ready_inputs"] = sum(row["ready"] for row in rows)
        for record_state in ("depleted", "missing", "double"):
            counts[record_state+"_inputs"] = sum(row["record_state"] == record_state for row in rows)
        counts["order_delta"] = sum(row["order_delta"] for row in rows)
        for key, count in counts.items():
            totals[key] += count
        for row in rows:
            key = (row["node"], (step-1) % 2)
            if row["kind"] == "correction":
                corrections[key] += 1
            elif row["kind"] == "unsorting":
                unsorting[key] += 1
        counts_by_step.append({"step": step, **dict(counts)})
        if (step-1) % 2 == collision_phase:
            receiver_rows.append({"step": step, **rows[receiver]})
    key = (receiver, collision_phase)
    return {"receiver": receiver, "collision_phase": collision_phase,
            "all_collision_count": max(0, len(states)-1)*states[0].N,
            "totals": dict(totals), "counts_by_step": counts_by_step,
            "receiver_events": receiver_rows,
            "receiver_corrections": corrections[key],
            "receiver_unsorting": unsorting[key],
            "receiver_repeat_gate": corrections[key] >= 2,
            "sites_and_streams_with_two_corrections": sum(v >= 2 for v in corrections.values()),
            "all_outcomes_included": True,
            "interpretation": "prepared functional routing; not a structural complexity score"}


def structural_trace(states, direction):
    """Keep the previous metric/gate unchanged, on each two-tick bank history."""
    states = list(states)
    if not states:
        raise ValueError("complete initial state is required")
    checkpoints = states[::2]
    result = []
    for bank, start in (("A", 0), ("B", 4)):
        values = [state.b[[start, start+2, start+3]].copy() for state in checkpoints]
        score = structure_trace(values, states[0].L, direction)
        # Count actual memory changes over each two-tick window. These are a
        # declared local activity diagnostic, not calibrated physical bursts.
        counts = [sum(int(states[k].b[start, n]) != int(states[k+2].b[start, n])
                      for n in range(states[0].N))
                  for k in range(0, len(states)-2, 2)]
        result.append({"bank": bank, "microsteps": list(range(0, len(states), 2)),
                       "scores": [s["score"] for s in score],
                       "activity_counts": counts, "growth": episode_gate(score, counts)})
    return {"banks": result,
            "scope": "same spatial motif formula; paired-bank activity uses retained memory differences, not canonical click classes",
            "overall_strict_growth": all(row["growth"]["strict_growth"] for row in result)}


def stationary_gate_check():
    """Exact conditional order means; no sampling or entropy identification."""
    if len(set(COLLISION)) != 16:
        raise AssertionError("literal collision must be a permutation")
    rows = []
    for rp, rm, x, y in product(range(2), repeat=4):
        _, _, xp, yp = COLLISION[8*rp+4*rm+2*x+y]
        rows.append({"input": [rp, rm, x, y], "delta_x_minus_y": xp-yp-x+y})
    means = {"ready": Fraction(sum(r["delta_x_minus_y"] for r in rows if r["input"][:2] == [1, 0]), 4),
             "depleted": Fraction(sum(r["delta_x_minus_y"] for r in rows if r["input"][:2] == [0, 1]), 4),
             "uniform": Fraction(sum(r["delta_x_minus_y"] for r in rows), 16)}
    assert means == {"ready": Fraction(1, 2), "depleted": Fraction(-1, 2), "uniform": Fraction(0)}
    return {"rows": rows, "exact_means": {k: str(v) for k, v in means.items()},
            "theorem": "For bijective F on a finite invariant set and invariant mu, E_mu[C(F(S))-C(S)]=0 by change of variables.",
            "paired_bank_scope": "The eight Boolean carrier/record lanes form an autonomous finite permutation on a finite board; organization depending on them cannot grow strictly forever.",
            "full_state_scope": "On the proved preparation a=F^-1(b) with fixed legal carries, the complete state is also finite and recurrent. No unbounded recoil registers are present.",
            "physical_entropy_claim": False}


def structural_negative_controls():
    rng = random.Random(9331)
    fresh = [np.asarray([[0]*125]+[[rng.randrange(2) for _ in range(125)] for _ in range(2)], dtype=object)
             for _ in range(25)]
    frozen = [fresh[0]]*25
    periodic = [fresh[i % 2] for i in range(25)]
    values = {}
    for name, history in (("fresh_random", fresh), ("frozen_random", frozen), ("periodic", periodic)):
        scores = structure_trace(history, 5, (1, 0, 0))
        gate = episode_gate(scores, [0, 1, 0]*8)
        values[name] = {"scores": [s["score"] for s in scores], "growth": gate,
                        "this_is_an_Engine_trajectory": False}
    assert max(values["frozen_random"]["scores"]) == 38
    assert not values["frozen_random"]["growth"]["strict_growth"]
    return {"controls": values, "interpretation": "readout falsifiers, not added dynamical experiments",
            "frozen_score_exposes_organization_ambiguity": True}


def _current(side, seed_number, memory):
    if memory not in PROTOCOL["memory_preparations"]:
        raise ValueError("unknown memory preparation")
    rng = random.Random(seed_number)
    rows = np.zeros((8, side**3), dtype=object)
    for bank in (0, 4):
        for g in range(bank, bank+4):
            rows[g] = [rng.randrange(2) for _ in range(side**3)]
        if memory != "mixed":
            rows[bank] = [int(memory == "ready")]*side**3
            rows[bank+1] = [int(memory == "depleted")]*side**3
    return rows


def _run_case(side, direction, seed_number, memory, variant, steps):
    from validation.local_unification import native
    options = {"direction": direction,
               "coupled": variant != "collision_off", "stream_records": variant != "record_transport_off"}
    law = native.build_tensor(**options)
    current = _current(side, seed_number, memory)
    carries = np.asarray([[(g+n+seed_number) % 6 for n in range(side**3)] for g in range(8)], dtype=object)
    initial = native.prepare_state(current, side, remainders=carries, **options)
    engine, states = Engine(law), [initial]
    max_bits = 0
    for _ in range(steps):
        before = states[-1]
        expected = native.first_order(before.b, side, **options)
        after = engine.step(before)
        if not np.array_equal(after.b, expected):
            raise AssertionError("Engine disagrees with shared first-order map")
        if not engine.inverse_step(after).same_as(before):
            raise AssertionError("complete inverse failed")
        if not np.array_equal(after.r, carries):
            raise AssertionError("compiled integer map changed a retained carry")
        max_bits = max(max_bits, max(abs(int(v)).bit_length() for array in (after.a, after.b, after.r) for v in array.flat))
        states.append(after)
    assert engine.rewind(states[-1], steps).same_as(initial)
    functional = functional_trace(states, coupled=options["coupled"])
    structural = structural_trace(states, direction)
    data = [state.to_dict() for state in states]
    spec = {"side": side, "direction": list(direction),
            "seed": seed_number, "memory": memory, "variant": variant, "steps": steps}
    return {**spec, "tensor_hash": law.fingerprint, "seed_hash": _digest(data[0]),
            "complete_trace_hash": _digest(data), "functional": functional, "structural": structural,
            "max_retained_bits": max_bits, "complete_rewind": True,
            "first_order_oracle_comparisons": steps*8*side**3,
            "comparison_preparation": "variants share current bits/carries; inverse-prepared old histories may differ"}, {"spec": spec, "tensor_hash": law.fingerprint, "states": data}


def repeated_task_audit():
    """A designed finite packet train, separately from the held-out panel."""
    from validation.local_unification import native
    rows = []
    for side, direction, variant in product((7, 9), DIRECTIONS,
                                            ("shared", "record_transport_off", "collision_off", "late_supply_removed")):
        options = {"direction": direction, "coupled": variant != "collision_off",
                   "stream_records": variant != "record_transport_off"}
        law, seed, specification = native.repeated_fixture(side, **options)
        if variant == "late_supply_removed":
            current = seed.b.copy()
            for channel, distance in ((4, -2), (0, -3)):
                current[channel, seed.lattice.index(*(distance*d for d in direction))] = 0
            seed = native.prepare_state(current, side, remainders=seed.r, **options)
        engine, states = Engine(law), [seed]
        for _ in range(specification["steps"]):
            after = engine.step(states[-1])
            assert engine.inverse_step(after).same_as(states[-1])
            states.append(after)
        assert engine.rewind(states[-1], specification["steps"]).same_as(seed)
        phases = [functional_trace(states, coupled=options["coupled"],
                                   receiver=specification["receiver"], collision_phase=phase)
                  for phase in (0, 1)]
        corrections = sorted(row["step"] for phase in phases for row in phase["receiver_events"]
                             if row["kind"] == "correction")
        if variant == "shared":
            assert corrections == [1, 2, 5, 6]
            assert all(p["receiver_repeat_gate"] for p in phases)
        elif variant == "collision_off":
            assert corrections == []
        elif variant == "late_supply_removed":
            assert corrections == [1, 2]
            assert not any(p["receiver_repeat_gate"] for p in phases)
        else:
            assert corrections != [1, 2, 5, 6]
        rows.append({"side": side, "direction": list(direction), "variant": variant,
                     "tensor_hash": law.fingerprint, "complete_seed_hash": _digest(seed.to_dict()),
                     "specification": specification, "phases": phases,
                     "correction_microsteps": corrections, "complete_rewind": True})
    return {"cases": rows, "case_count": len(rows),
            "same_law_late_supply_control": True,
            "claim": "Two useful collisions per bank cohort from a finite complete preparation; removing the later ready supply removes the second collision.",
            "excluded_claim": "No indefinitely renewed supply, autonomous computation of higher complexity, physical clock or cosmological burst is established."}


def audit(out, *, full_panel=True):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    archive = out/"complete_panel.jsonl.gz"
    rows = []
    sides = PROTOCOL["sides"] if full_panel else [3]
    seeds = PROTOCOL["seeds"] if full_panel else [101]
    directions = DIRECTIONS if full_panel else [DIRECTIONS[0]]
    with gzip.open(archive, "wt", encoding="utf-8") as stream:
        for side, direction, seed_number, memory, variant in product(sides, directions, seeds, PROTOCOL["memory_preparations"], PROTOCOL["variants"]):
            summary, raw = _run_case(side, direction, seed_number, memory, variant, PROTOCOL["steps"])
            stream.write(exact_json.dumps(raw, sort_keys=True)+"\n")
            rows.append(summary)
    shared = [r for r in rows if r["variant"] == "shared"]
    counts = Counter(row["structural"]["banks"][bank]["growth"]["status"] for row in shared for bank in (0, 1))
    report = {"protocol": PROTOCOL, "full_panel": full_panel, "cases": rows,
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "stationary": stationary_gate_check(), "negative_controls": structural_negative_controls(),
              "repeated_task": repeated_task_audit(),
              "native_source_sha256": hashlib.sha256(Path(__file__).with_name("native.py").read_bytes()).hexdigest(),
              "inherited_metric_source_sha256": hashlib.sha256(Path(__file__).parents[1].joinpath("selection", "complexity.py").read_bytes()).hexdigest(),
              "case_count": len(rows), "shared_case_count": len(shared),
              "shared_receiver_repeat_passes": sum(r["functional"]["receiver_repeat_gate"] for r in shared),
              "shared_bank_growth_outcomes": dict(counts),
              "complete_panel_archive": str(archive),
              "complete_panel_archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
              "scope": {"functional": "finite prepared repeated routing, all receiver outcomes retained",
                        "structural": "old motif score with explicit negative controls; no universal complexity identification",
                        "Einstein_source": "requires independent common-law physical proof",
                        "physical_clock": "not established by microstep parity or memory activity",
                        "cosmological_burst": "not established"}}
    (out/"organization.json").write_text(exact_json.dumps(report, sort_keys=True)+"\n")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/local-unification/organization"))
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args(argv)
    report = audit(args.out, full_panel=not args.quick)
    print(exact_json.dumps({k: report[k] for k in ("case_count", "shared_case_count", "shared_receiver_repeat_passes", "shared_bank_growth_outcomes")}, sort_keys=True))


if __name__ == "__main__":
    main()
