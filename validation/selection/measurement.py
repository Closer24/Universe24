"""Exact instrument contracts and a finite relational-clock reference.

This is validation, not an Engine sampler. The rational quantum reference
assumes a Hilbert-space norm and never feeds outcomes into Rule3. Its purpose
is to make clock ordering, retained record, coherence and selection distinct.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path


LABELS = ("left", "right")


def assess_trials(trials, *, declared_ids, decision_tick, persistence_ticks,
                  labels=LABELS, weights=None):
    """Assess all declared outcome traces without selecting/resampling them.

    Each trial is {id: str, outcomes: list[list[str]], expected: optional str}.
    Index zero is the observed ready window; tick indexing is static protocol,
    not a hidden evolution input. Each output list contains all active outcomes.
    The caller supplies any ensemble weights explicitly; they are not derived.
    """
    if (type(decision_tick) is not int or decision_tick < 1
            or type(persistence_ticks) is not int or persistence_ticks < 1):
        raise ValueError("positive declared decision and persistence ticks required")
    if not labels or len(set(labels)) != len(labels):
        raise ValueError("distinct outcome labels required")
    if any(type(label) is not str or not label for label in labels):
        raise ValueError("nonempty string labels required")
    if set(labels) & {"none", "multiple"}:
        raise ValueError("outcome labels cannot use reserved diagnostic categories")
    ids = tuple(declared_ids)
    if not ids or len(set(ids)) != len(ids) or any(type(i) is not str or not i for i in ids):
        raise ValueError("nonempty unique trial identities required")
    rows = list(trials)
    if any(type(row) is not dict for row in rows):
        raise ValueError("trial rows must be dictionaries")
    if len(rows) != len(ids) or {row.get("id") for row in rows} != set(ids):
        raise ValueError("every declared trial must occur exactly once")
    if weights is None:
        measure = {identity: Fraction(1, len(ids)) for identity in ids}
        measure_role = "explicit uniform counting measure on declared trials; not a physical derivation"
    else:
        if set(weights) != set(ids):
            raise ValueError("weights must cover every trial")
        if any(type(value) not in (int, Fraction) for value in weights.values()):
            raise ValueError("weights must be exact integers or Fractions")
        measure = {identity: Fraction(value) for identity, value in weights.items()}
        if any(value < 0 for value in measure.values()) or sum(measure.values()) != 1:
            raise ValueError("weights must be nonnegative and normalized")
        measure_role = "caller-supplied exact measure; not a physical derivation"
    horizon = decision_tick + persistence_ticks
    counts = Counter({"none": 0, "single": 0, "multiple": 0,
                      "unstable_single": 0, "stable_single": 0})
    mass = {label: Fraction(0) for label in (*labels, "none", "multiple")}
    ready, calibration, calibrated = True, True, 0
    details = []
    for row in rows:
        trace = row.get("outcomes")
        if type(trace) is not list or len(trace) < horizon:
            raise ValueError("incomplete declared observation horizon")
        for outcomes in trace:
            if (type(outcomes) is not list or len(set(outcomes)) != len(outcomes)
                    or any(label not in labels for label in outcomes)):
                raise ValueError("invalid or duplicate outcome in trace")
        ready &= not trace[0]
        outcome = trace[decision_tick]
        category = "none" if not outcome else "single" if len(outcome) == 1 else "multiple"
        counts[category] += 1
        mass[outcome[0] if category == "single" else category] += measure[row["id"]]
        stable = category == "single" and all(
            tick == outcome for tick in trace[decision_tick:horizon])
        if category == "single":
            counts["stable_single" if stable else "unstable_single"] += 1
        if "expected" in row:
            if row["expected"] not in labels:
                raise ValueError("unknown calibration outcome")
            calibrated += 1
            calibration &= outcome == [row["expected"]]
        details.append({"id": row["id"], "category": category,
                        "persistent": stable, "outcomes_at_decision": outcome})
    assert sum(mass.values()) == 1
    return {"schema": "universe24/instrument-observation-contract/1",
            "trial_count": len(ids), "all_declared_trials_retained": True,
            "decision_tick": decision_tick, "persistence_ticks": persistence_ticks,
            "counts": dict(counts), "observed_ready_window_empty": ready,
            "exclusive_at_decision": counts["single"] == len(ids),
            "persistent_exclusive_record": counts["stable_single"] == len(ids),
            "calibration": "not_tested" if not calibrated else "passed" if calibration else "failed",
            "outcome_mass_all_trials": {key: str(value) for key, value in mass.items()},
            "measure_role": measure_role, "details": details,
            "not_certified_by_this_reader": ["retained physical ready domain", "source interaction",
                "full-state reversibility", "causal feedback", "repeatability with fresh apparatus",
                "Born measure", "material proper time"]}


def _swap_ready(pointer, source):
    target = source + 1
    return target if pointer == 0 else 0 if pointer == target else pointer


def clock_gate(tick, basis):
    """Fixed controlled permutation: source bit, two ternary pointer registers."""
    source, first, fresh = basis
    if tick in (0, 3):
        first = _swap_ready(first, source)
    if tick in (1, 3):
        fresh = _swap_ready(fresh, source)
    return source, first, fresh


def global_step(basis):
    tick, *data = basis
    return ((tick + 1) % 4, *clock_gate(tick, tuple(data)))


def _apply(state, transform):
    result = {}
    for basis, amplitude in state.items():
        other = transform(basis)
        result[other] = result.get(other, Fraction(0)) + amplitude
    return {basis: amplitude for basis, amplitude in result.items() if amplitude}


def _norm(state):
    return sum(amplitude ** 2 for amplitude in state.values())


def relational_reference():
    """Construct a stationary four-tick history with exact retained memories."""
    bases = tuple(product(range(4), range(2), range(3), range(3)))
    images = [global_step(basis) for basis in bases]
    assert len(set(images)) == len(bases) == 72
    inverse = {image: basis for basis, image in zip(bases, images)}
    assert all(inverse[global_step(basis)] == basis for basis in bases)
    initial = {(0, 0, 0): Fraction(3, 5), (1, 0, 0): Fraction(4, 5)}
    slices = [initial]
    for tick in range(4):
        slices.append(_apply(slices[-1], lambda basis, tick=tick: clock_gate(tick, basis)))
    assert slices[4] == initial
    assert all(_norm(state) == 1 for state in slices)
    history = {(tick, *basis): amplitude / 2
               for tick, state in enumerate(slices[:4]) for basis, amplitude in state.items()}
    assert _norm(history) == 1 and _apply(history, global_step) == history
    assert _apply(_apply(history, global_step), lambda basis: inverse[basis]) == history
    for tick in range(4):
        conditioned = {basis[1:]: value * 2 for basis, value in history.items() if basis[0] == tick}
        assert conditioned == slices[tick]
    # Tracing the source/fresh register suppresses first-pointer off diagonals.
    rho = [[Fraction(0) for _ in range(3)] for _ in range(3)]
    for (source, first, fresh), a in slices[2].items():
        for (other_source, other_first, other_fresh), b in slices[2].items():
            if source == other_source and fresh == other_fresh:
                rho[first][other_first] += a * b
    assert rho == [[0, 0, 0], [0, Fraction(9, 25), 0], [0, 0, Fraction(16, 25)]]
    coherence = slices[2][(0, 1, 1)] * slices[2][(1, 2, 2)]
    assert coherence == Fraction(12, 25)
    basis_trials, repeatability = [], []
    for source in (0, 1):
        state, outcomes = (source, 0, 0), [[]]
        for tick in range(4):
            state = clock_gate(tick, state)
            outcomes.append([] if state[1] == 0 else [LABELS[state[1] - 1]])
            if tick == 1:
                repeatability.append(state[1] == state[2] == source + 1)
        basis_trials.append({"id": f"basis-{source}", "outcomes": outcomes,
                             "expected": LABELS[source]})
    short = assess_trials(basis_trials, declared_ids=("basis-0", "basis-1"),
                          decision_tick=1, persistence_ticks=3)
    long = assess_trials(basis_trials, declared_ids=("basis-0", "basis-1"),
                         decision_tick=1, persistence_ticks=4)
    assert short["persistent_exclusive_record"] and all(repeatability)
    assert not long["persistent_exclusive_record"]
    return {"role": "exact finite quantum-circuit reference, not a Rule3 model or sampler",
            "basis_dimension": 72, "clock_readings": 4,
            "retained_subsystems": "clock, source, ternary pointer, fresh ternary probe",
            "global_permutation_bijection": True, "stationary_history_exact": True,
            "clock_conditioning_recovers_each_slice": True,
            "fresh_probe_repeatability_on_basis_inputs": all(repeatability),
            "short_window_contract": short, "cyclic_uncomputation_control": long,
            "pointer_reduced_density_matrix": [[str(x) for x in row] for row in rho],
            "full_state_off_diagonal_coherence": str(coherence),
            "coherent_outcome_branches_retained": len(slices[2]),
            "single_branch_dynamically_selected": False,
            "probability_role": "9/25 and 16/25 use the assumed quantum squared-norm rule; not derived from clock conditioning",
            "random_draws": 0}


def contract_controls():
    cases = [
        {"id": "good", "outcomes": [[], ["left"], ["left"], ["left"]]},
        {"id": "none", "outcomes": [[], [], [], []]},
        {"id": "double", "outcomes": [[], ["left", "right"], ["left", "right"], ["left", "right"]]},
        {"id": "unstable", "outcomes": [[], ["right"], ["left"], ["right"]]},
    ]
    result = assess_trials(cases, declared_ids=[case["id"] for case in cases],
                           decision_tick=1, persistence_ticks=3)
    assert result["counts"] == {"none": 1, "single": 2, "multiple": 1,
                                 "unstable_single": 1, "stable_single": 1}
    rejections = []
    for label, wrong in (("missing", cases[:-1]), ("duplicate", cases[:-1] + [cases[0]])):
        try:
            assess_trials(wrong, declared_ids=[case["id"] for case in cases],
                          decision_tick=1, persistence_ticks=3)
        except ValueError:
            rejections.append(label)
        else:
            raise AssertionError("incomplete trial stream was accepted")
    # Exclusive deterministic outcomes alone do not specify a probability law.
    calibrated = [{"id": "a", "outcomes": [[], ["left"], ["left"]]},
                  {"id": "b", "outcomes": [[], ["right"], ["right"]]}]
    measures = []
    for weight in (Fraction(1, 2), Fraction(9, 10)):
        row = assess_trials(calibrated, declared_ids=("a", "b"), decision_tick=1,
                            persistence_ticks=2, weights={"a": weight, "b": 1-weight})
        assert row["persistent_exclusive_record"]
        measures.append(row["outcome_mass_all_trials"])
    assert measures[0] != measures[1]
    # Same initial rational state; actual unitary rotation can change amplitudes.
    amplitude = (Fraction(3, 5), Fraction(4, 5))
    rotated = ((3*amplitude[0] - 4*amplitude[1])/5,
               (4*amplitude[0] + 3*amplitude[1])/5)
    assert sum(x*x for x in rotated) == 1
    before = [x*x for x in amplitude]
    after = [x*x for x in rotated]
    postweighted = [2*before[0]/(2*before[0]+before[1]),
                   before[1]/(2*before[0]+before[1])]
    assert before != after and postweighted != before
    return {"complete_window_failure_controls": result, "malformed_streams_rejected": rejections,
            "same_dynamics_different_measures": measures,
            "premeasurement_unitary_rotation": {"before": list(map(str, before)),
                                                 "after": list(map(str, after))},
            "postmeasurement_outcome_bias": {"multipliers": [2, 1],
                                               "result": list(map(str, postweighted))},
            "scope": "Changing amplitudes through dynamics and reweighting fixed outcomes are different operations; neither example derives a complexity law."}


def native_pointer_contract(path):
    """Read the native lane's declared finite window without filtering controls."""
    data = json.loads(path.read_text())
    rows = data["trials"]
    report = assess_trials(rows, declared_ids=[row["id"] for row in rows],
                           decision_tick=data["decision_index"],
                           persistence_ticks=data["persistence_ticks"],
                           labels=tuple(data["allowed_outcomes"]))
    return {"source_path": str(path),
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "role": "pooled engineering controls, not an identically prepared physical ensemble",
            "contract": report,
            "interpretation": "Persistent pulse records are demonstrated by individual controls; none, double and prefilled records remain visible. This is not an outcome-selector certificate."}


def audit(pointer_trials=None):
    report = {"schema": "universe24/selection/measurement/1",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "relational_clock_reference": relational_reference(),
            "instrument_contract_controls": contract_controls(),
            "engine_feedback_derived_here": False, "engine_Born_derived_here": False,
            "gate_handoff": ["retained ready sector", "causal interaction", "exclusive persistent record",
                "fresh-probe repeatability", "local feedback", "complete preparation measure",
                "held-out Born comparison", "structural growth with disconnected controls"]}
    if pointer_trials is not None:
        report["native_pointer_observation"] = native_pointer_contract(pointer_trials)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/selection/measurement"))
    parser.add_argument("--pointer-trials", type=Path,
                        help="explicit native observer lane trace file, all declared controls retained")
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    report = audit(args.pointer_trials)
    (args.out / "measurement.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"stationary_history": True, "basis_calibration_repeatability": True,
                      "cyclic_pointer_persistence": "failed", "derived_Born": False}))


if __name__ == "__main__":
    main()
