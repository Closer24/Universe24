"""Independent counting-measure and exclusive-selection audit of the NEW gates.

No Born sampler is implemented. Finite row sectors, prepared measures, actual
retained outcomes and arithmetic event streams are kept explicitly distinct.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
from itertools import product
from pathlib import Path

import numpy as np

from universe24.core import Engine, State, exact_json
from universe24.system.bundle import canonical_bytes
from universe24.system.decoder import decode_transition, make_transition
from validation.selection.clocks import build_native_gate, prepare_gate
from validation.selection.complexity import SORT_GATE
from validation.selection.pointer import native_control

ROW_STATES = tuple(product((0, 1), repeat=9))


def literal_gate(bits):
    """Independent branch/table specification; no polynomial evaluator."""
    m, x, y = bits
    memory = m ^ int(y == 1 and x == 0)
    return (memory, y, x) if memory else (memory, x, y)


def row_step(bits, inverse=False):
    """Three-site ring oracle using literal coordinates, not lattice shifts."""
    source = [list(bits[3*n:3*n+3]) for n in range(3)]
    table = {literal_gate(v): v for v in product((0, 1), repeat=3)}
    if inverse:
        source = [(source[n][0], source[(n+1) % 3][1], source[n][2]) for n in range(3)]
        return tuple(value for v in source for value in table[tuple(v)])
    result = [[0, 0, 0] for _ in range(3)]
    for n, old in enumerate(source):
        m, x, y = literal_gate(old)
        result[n][0], result[(n+1) % 3][1], result[n][2] = m, x, y
    return tuple(value for v in result for value in v)


def _row_array(bits):
    result = np.zeros((3, 27), dtype=object)
    for n in range(3):
        result[:, n*9] = bits[3*n:3*n+3]
    return result


def _extract_row(values):
    return tuple(int(values[g, n*9]) for n in range(3) for g in range(3))


def _outcome(x, y):
    return "multiple" if x and y else "preferred" if x else "other" if y else "none"


def _record(sink, family, tensor, before, after, identity, step=1):
    transition = make_transition(tensor, before, after, run_id=identity, step=step)
    events = decode_transition(transition, tensor)
    if sink is not None:
        sink({"family": family, "transition": transition, "events": events})
    return events


def cycle_measures():
    """Uniform cycle measures are stationary but need not give the same law."""
    seen, cycles = set(), []
    for bits in ROW_STATES:
        if bits in seen:
            continue
        cycle, state = [], bits
        while state not in seen:
            seen.add(state); cycle.append(state); state = row_step(state)
        assert state == bits
        cycles.append(cycle)
    one_particle = [cycle for cycle in cycles if sum(cycle[0][3*n+g]
                    for n in range(3) for g in (1, 2)) == 1]
    def share(cycle):
        return Fraction(sum(sum(s[3*n+1] for n in range(3)) for s in cycle), len(cycle))
    witnesses = []
    for cycle in (min(one_particle, key=share), max(one_particle, key=share)):
        # Average over spatial translates as well; stationarity and translation
        # symmetry still do not make the two ensemble predictions coincide.
        mass = Counter(tuple(s[3*((n+shift) % 3)+g] for n in range(3) for g in range(3))
                       for s in cycle for shift in range(3))
        pushed = Counter()
        for s, count in mass.items():
            pushed[row_step(s)] += count
        assert pushed == mass
        total = sum(mass.values())
        probability = Fraction(sum(count*sum(s[3*n+1] for n in range(3))
                                  for s, count in mass.items()), total)
        assert probability == share(cycle)
        witnesses.append({"cycle_length": len(cycle), "cycle": [list(s) for s in cycle],
                          "translation_averaged_support": len(mass),
                          "preferred_lane_probability": str(probability),
                          "same_particle_count": 1, "stationary": True,
                          "translation_invariant": True})
    assert witnesses[0]["preferred_lane_probability"] == "1/3"
    assert witnesses[1]["preferred_lane_probability"] == "1"
    return {"cycles": len(cycles), "one_particle_cycles": len(one_particle),
            "stationary_same_particle_number_witnesses": witnesses,
            "stationarity_determines_unique_measure": False}


def gate_audit(*, sink=None, carries=range(6)):
    assert tuple(literal_gate(b) for b in product((0, 1), repeat=3)) == SORT_GATE
    tensor = build_native_gate(SORT_GATE)
    engine = Engine(tensor)
    output_rows, details = set(), []
    record_contingency = Counter()
    for carry in carries:
        for index, bits in enumerate(ROW_STATES):
            current = _row_array(bits)
            seed = prepare_gate(SORT_GATE, current, 3,
                                remainders=np.full_like(current, carry))
            assert np.array_equal(seed.a, _row_array(row_step(bits, inverse=True)))
            after = engine.step(seed)
            expected = _row_array(row_step(bits))
            assert np.array_equal(after.b, expected)
            assert np.array_equal(after.a, seed.b) and np.array_equal(after.r, seed.r)
            assert engine.inverse_step(after).same_as(seed)
            events = _record(sink, "gate", tensor, seed, after, f"gate:{carry}:{index}")
            assert all(event["kind"] == "C0" for event in events)
            if carry == 0:
                output_rows.add(_extract_row(after.b))
                # Moving output of source0 has streamed to x=1, flat node9.
                x, y = int(after.b[1, 9]), int(after.b[2, 0])
                outcome = _outcome(x, y)
                memory_event = any(e["channel"] == 0 and e["node"] == 0 for e in events)
                record_contingency[(outcome, memory_event)] += 1
                details.append({"input": list(bits), "output": list(_extract_row(after.b)),
                                "local_input": list(bits[:3]), "local_outcome": outcome,
                                "memory_event": memory_event,
                                "all_memory_ready": not any(bits[3*n] for n in range(3))})
    if 0 not in carries:
        raise ValueError("carry0 required for the finite counting certificate")
    assert output_rows == set(ROW_STATES)
    def summary(rows):
        counts = Counter(row["local_outcome"] for row in rows)
        return {"count": len(rows), "counts": {k: counts[k] for k in ("none", "preferred", "other", "multiple")},
                "probabilities": {k: str(Fraction(counts[k], len(rows)))
                                  for k in ("none", "preferred", "other", "multiple")}}
    ready = [r for r in details if r["all_memory_ready"]]
    one = [r for r in details if sum(r["local_input"][1:]) == 1]
    ready_one = [r for r in ready if sum(r["local_input"][1:]) == 1]
    ready_surviving = sum(not any(row["output"][3*n] for n in range(3)) for row in ready)
    assert len(ready) == 64 and ready_surviving == 27
    assert summary(ready_one)["probabilities"]["preferred"] == "1"
    assert summary(one)["probabilities"]["preferred"] == "1/2"
    # The same observed G supports any explicitly supplied rational memory
    # distribution: for one particle, x_out=1-m and y_out=m.
    measure_family = []
    for p in (Fraction(0), Fraction(1, 3), Fraction(1, 2), Fraction(9, 10), Fraction(1)):
        mass = {bits: (p if bits[0] == 0 else 1-p)/2
                for bits in product((0, 1), repeat=3) if bits[1]+bits[2] == 1}
        preferred = sum(weight*literal_gate(bits)[1] for bits, weight in mass.items())
        assert sum(mass.values()) == 1 and preferred == p
        measure_family.append({"declared_P_memory_ready": str(p), "observed_P_preferred": str(preferred)})
    return {"tensor_hash": tensor.fingerprint, "channels": tensor.G,
            "enumerated_row_states": 512, "engine_transitions": 512*len(carries),
            "all_carry_classes": list(carries), "complete_inverse": True,
            "scope": "All512 states of one periodic3-node row embedded in L3; other rows zero. Arbitrary mixed carries are unchanged by coefficient divisibility, not exhaustively enumerated.",
            "uniform_sector_invariant": True, "uniform_all": summary(details),
            "ready_all": summary(ready), "uniform_one_particle_local": summary(one),
            "ready_one_particle_local": summary(ready_one),
            "ready_sector_surviving": ready_surviving, "ready_sector_size": len(ready),
            "exclusive_criterion": "x+y=1 iff exactly one collision output occupied; then x_out=1-m, y_out=m",
            "memory_event_vs_outcome": [{"outcome": k[0], "memory_event": k[1], "count": v}
                                        for k, v in sorted(record_contingency.items())],
            "declared_measure_sensitivity": measure_family, "cycle_measures": cycle_measures(),
            "rows": details, "Born_measure_derived": False}


def pointer_audit(*, sink=None, carries=range(6)):
    from universe24.tests.test_migration import scalar_step
    cases = [(a, b, 0, "ready_grid") for a, b in product(range(-2, 3), repeat=2)]
    cases += [(1, 1, h, "history_control") for h in (-1, 0, 1)]
    rows, counts = [], Counter()
    for carry in carries:
        for index, (a, b, history, family) in enumerate(cases):
            bundle = native_control(side=5, amplitude=a, second_amplitude=b, carry=carry, history=history)
            engine, state = Engine(bundle.tensor), bundle.seed
            initial = state.copy()
            nodes = bundle.model["detector_nodes"]
            observations, events_per_tick = [], []
            identity = f"pointer:{carry}:{index}"
            for step in range(7):
                velocity = [int(state.b[1, node]-state.a[1, node]) for node in nodes]
                observations.append(velocity)
                if step == 6:
                    break
                before, state = state, engine.step(state)
                assert state.same_as(scalar_step(bundle.tensor, before))
                assert engine.inverse_step(state).same_as(before)
                records = _record(sink, "pointer", bundle.tensor, before, state, identity, step+1)
                events_per_tick.append([sum(e["channel"] == 1 and e["node"] == node for e in records)
                                        for node in nodes])
            expected = [history+a*a, b*b]
            assert all(value == expected for value in observations[2:])
            assert engine.rewind(state, 6).same_as(initial)
            active = [value > 0 for value in expected]
            outcome = _outcome(*active)
            counts[(family, outcome)] += 1
            if history == 0:
                assert (sum(active) == 1) == ((a != 0) ^ (b != 0))
            rows.append({"id": identity, "family": family, "amplitudes": [a, b], "history": history,
                         "carry": carry, "decision_velocity": expected, "outcome": outcome,
                         "velocities": observations, "memory_events_per_tick": events_per_tick,
                         "complete_inverse": True})
    return {"trials": len(rows), "engine_transitions": 6*len(rows), "rows": rows,
            "engineering_counts": [{"family": k[0], "outcome": k[1], "count": v} for k,v in sorted(counts.items())],
            "decision_tick": 2, "persistence_ticks": [2, 3, 4, 5, 6],
            "exact_ready_choice_criterion": "Exactly one nonzero prepared amplitude iff exactly one positive record at tick2, for zero history.",
            "history_formula": "v_left=history+amplitude_left^2; v_right=amplitude_right^2",
            "measure_role": "complete engineering parameter sweep, not a physical statistical ensemble",
            "exclusive_for_two_nonzero_sources": False, "Born_measure_derived": False}


def bell_control():
    """Factorized response certificate; not a physical analyzer/source model."""
    maximum = Fraction(0)
    means = tuple(Fraction(k, 4) for k in range(-4, 5))
    for a0, a1, b0, b1 in product(means, repeat=4):
        maximum = max(maximum, abs(a0*(b0+b1)+a1*(b0-b1)))
    assert maximum == 2
    # Independent settings locally toggle prepared memory. With a single
    # occupied carrier, the measured truth table is s=1-2*(m xor setting).
    tables = []
    for m_a, m_b in product((0, 1), repeat=2):
        correlations = []
        for x, y in product((0, 1), repeat=2):
            out_a, out_b = literal_gate((m_a ^ x, 1, 0)), literal_gate((m_b ^ y, 1, 0))
            correlations.append((out_a[1]-out_a[2])*(out_b[1]-out_b[2]))
        value = abs(sum(s*c for s,c in zip((1, 1, 1, -1), correlations)))
        assert value == 2
        tables.append({"common_memory": [m_a, m_b], "correlations": correlations, "CHSH": value})
    return {"exact_response_tables": tables, "stochastic_mean_models": len(means)**4,
            "maximum_CHSH": str(maximum), "all_setting_pairs_retained": True,
            "setting_independent_common_measure_required": True,
            "interpretation": "Local response tables of the audited gate; no late-choice, spacelike, entangled Engine experiment supplied.",
            "physical_Bell_violation": "not_tested"}


def verify_saved(path, tensors):
    from universe24.tests.test_migration import scalar_step
    seen, counts, previous = set(), Counter(), {}
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = exact_json.loads(line); record = row["transition"]
            identity = (record["run_id"], record["step"])
            if identity in seen:
                raise ValueError("duplicate trial transition")
            seen.add(identity)
            family = record["run_id"].split(":", 1)[0]
            if family not in ("gate", "pointer") or row["family"] != family:
                raise ValueError("wrong declared trial family")
            old = previous.get(record["run_id"])
            if old is None:
                if record["step"] != 1:
                    raise ValueError("trial must start at its first transition")
            elif record["step"] != old[0]+1 or record["before"] != old[1]:
                raise ValueError("saved trial chain is missing, reordered or disconnected")
            tensor = tensors[record["tensor_hash"]]
            before, after = (State.from_dict(record[k]) for k in ("before", "after"))
            if not scalar_step(tensor, before).same_as(after):
                raise ValueError("saved transition failed independent scalar oracle")
            if not Engine(tensor).inverse_step(after).same_as(before):
                raise ValueError("saved transition failed inverse")
            if decode_transition(record, tensor) != row["events"]:
                raise ValueError("saved canonical records mismatch")
            previous[record["run_id"]] = (record["step"], record["after"])
            counts[row["family"]] += 1
    expected = {("gate:%d:%d" % (carry, index), 1) for carry in range(6) for index in range(512)}
    expected.update(("pointer:%d:%d" % (carry, index), step)
                    for carry in range(6) for index in range(28) for step in range(1, 7))
    if seen != expected:
        raise ValueError("saved trials incomplete or undeclared")
    if counts != {"gate": 3072, "pointer": 1008}:
        raise ValueError("saved family counts disagree with the declared protocol")
    return {"transitions": len(seen), "by_family": dict(counts),
            "independent_scalar_replay": True, "complete_inverse": True, "canonical_records_equal": True,
            "complete_contiguous_trial_chains": True}


def audit(out):
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("fresh Born-audit output directory required")
    out.mkdir(parents=True, exist_ok=True)
    tensors = {t.fingerprint: t for t in (build_native_gate(SORT_GATE), native_control(side=5).tensor)}
    with gzip.open(out / "transitions.jsonl.gz", "wt", encoding="utf-8") as stream:
        sink = lambda row: stream.write(exact_json.dumps(row)+"\n")
        gate, pointer = gate_audit(sink=sink), pointer_audit(sink=sink)
    saved = verify_saved(out / "transitions.jsonl.gz", tensors)
    (out / "tensors.json").write_text(exact_json.dumps({key:t.to_dict() for key,t in tensors.items()})+"\n")
    root = Path(__file__).resolve().parents[2]
    paths = ["validation/selection/"+name+".py" for name in ("born", "clocks", "complexity", "pointer")]
    paths += ["universe24/core/engine.py", "universe24/core/tensor.py", "universe24/system/decoder.py",
              "universe24/tests/test_migration.py"]
    report = {"schema": "universe24/selection-born-audit/1", "gate": gate, "pointer": pointer,
              "bell": bell_control(), "saved_replay": saved,
              "source_sha256": {p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths},
              "artifact_sha256": {p:hashlib.sha256((out/p).read_bytes()).hexdigest()
                                  for p in ("transitions.jsonl.gz", "tensors.json")},
              "positive_result": "Exact conditional exclusive routing with retained provenance and a declared ready sector.",
              "open_gate": "Neither uniform stationary counting nor a shared clock uniquely derives a physical Born preparation measure.",
              "physical45_integration": "not_implemented by this native-sector audit"}
    (out / "born.json").write_text(exact_json.dumps(report, sort_keys=True)+"\n")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/selection/born"))
    result = audit(parser.parse_args(argv).out)
    print(exact_json.dumps({"saved_replay": result["saved_replay"],
          "positive_result": result["positive_result"], "open_gate": result["open_gate"]}))


if __name__ == "__main__":
    main()
