"""Complete-trial calibration of the retained clock-link apparatus.

The CLI requires the pinned base bundle. No probability sampler supplies Engine
outcomes. All preparations are declared arrival-surface controls; they are not
constraint-satisfying source/transport experiments or a quantum Bell apparatus.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
from itertools import product
from pathlib import Path

from universe24.core import Engine, State
from universe24.core import exact_json as json
from universe24.system.bundle import canonical_bytes, load_bundle, save_bundle
from universe24.system.decoder import decode_transition, make_transition
from validation.clock_links.model import append_phase_observers, CARRIER_NAMES, OBSERVER_NAMES


def norm2(z):
    return sum(value * value for value in z)


def normalized(values):
    total = sum(values)
    return [str(Fraction(value, total)) for value in values] if total else None


def state_hash(state):
    return hashlib.sha256(canonical_bytes(state.to_dict())).hexdigest()


def local_chsh_bound():
    """Exact finite certificate; the continuous proof is given in the report."""
    means = tuple(Fraction(k, 4) for k in range(-4, 5))
    maximum = max(abs(a0 * (b0 + b1) + a1 * (b0 - b1))
                  for a0, a1, b0, b1 in product(means, repeat=4))
    assert maximum == 2
    return {"local_response_mean_grid": list(map(str, means)),
            "models_checked": len(means) ** 4, "maximum_CHSH": str(maximum),
            "assumptions": ["same setting-independent distribution of the complete common-past state",
                            "conditional local response factorization",
                            "all predefined trials retained with fixed outcomes in [-1,1]"],
            "engine_Bell_experiment": "not_tested: no entangled preparation or two-setting analyzer is supplied",
            "whole_board_clock_exemption": False}


def complexity_reweighting():
    """A compatibility condition, not an Engine probability or selection law."""
    checked = 0
    for i0, i1, c0, c1 in product(range(1, 7), repeat=4):
        same = Fraction(i0 * c0, i0 * c0 + i1 * c1) == Fraction(i0, i0 + i1)
        assert same == (c0 == c1)
        checked += 1
    return {"positive_integer_cases": checked,
            "identity": "I0*c0/(I0*c0+I1*c1)=I0/(I0+I1) iff c0=c1 for positive I0,I1,c0,c1",
            "example": {"intensities": [9, 1], "complexity_multipliers": [2, 1],
                        "Born_reference": ["9/10", "1/10"], "postweighted": ["18/19", "1/19"]},
            "interpretation": "Outcome-dependent complexity postweighting generally changes Born ratios; a common multiplier cancels. This does not exclude complexity changing amplitudes before measurement."}


CALIBRATIONS = (
    ("zero_source", ((0, 0), (0, 0)), False),
    ("unequal_9_1", ((3, 0), (1, 0)), False),
    ("unequal_scaled_36_4", ((6, 0), (2, 0)), False),
    ("balanced", ((1, 0), (0, 1)), False),
    ("one_dark", ((2, 0), (0, 0)), False),
    ("common_quarter_turn", ((0, 3), (0, 1)), False),
    ("stationary_nonzero", ((1, 1), (1, 1)), True),
)


def _prepared_seed(extended, amplitudes, remainders, stationary):
    seed = extended.seed
    carrier = [extended.tensor.gear_index(name) for name in CARRIER_NAMES]
    detector = extended.tensor.gear_index(OBSERVER_NAMES[0])
    nodes = (seed.lattice.index(0, 0, 0), seed.lattice.index(1, 1, 1))
    for g in carrier:
        seed.a[g, :] = 0
        seed.b[g, :] = 0
    for node, amplitude, remainder in zip(nodes, amplitudes, remainders):
        for g, value in zip(carrier, amplitude):
            seed.b[g, node] = value
        seed.r[detector, node] = remainder
        if stationary:
            intensity = norm2(amplitude)
            if intensity % 2:
                raise ValueError("stationary calibration needs even intensity")
            seed.a[detector, node] = seed.b[detector, node] = intensity // 2
    return seed, nodes, detector


def receiver_indistinguishability(extended, *, record_sink=None):
    """Two positive, unequal ratios have identical four-receiver records.

    Scope is one complete predeclared observation window and receiver records
    only. Base carrier records or hidden state are not part of that interface.
    This is an exact obstruction for *all admitted apparatus seeds*, not a
    no-go theorem for another interacting detector/preparation domain.
    """
    tensor, engine = extended.tensor, Engine(extended.tensor)
    carrier = [tensor.gear_index(name) for name in CARRIER_NAMES]
    observers = [tensor.gear_index(name) for name in OBSERVER_NAMES]
    rows = []
    for label, amplitudes in (("ratio_5_1", ((3, 1), (1, 1))),
                              ("ratio_1_5", ((1, 1), (3, 1)))):
        seed, nodes, _ = _prepared_seed(extended, amplitudes, (0, 0), False)
        re, im = seed.b[carrier[0]], seed.b[carrier[1]]
        for slot, observer in enumerate(observers):
            for node in range(seed.N):
                if slot == 0:
                    real, imaginary = int(re[node]), int(im[node])
                else:
                    offset = tuple(1 if k == slot - 1 else 0 for k in range(3))
                    neighbour = int(seed.lattice.shift_index(offset)[node])
                    real, imaginary = int(re[node] + re[neighbour]), int(im[node] + im[neighbour])
                intensity = real * real + imaginary * imaginary
                assert intensity % 2 == 0
                seed.a[observer, node] = seed.b[observer, node] = intensity // 2
        after = engine.step(seed)
        run_id = "receiver-indistinguishability:" + label
        transition = make_transition(tensor, seed, after, run_id=run_id, step=1)
        records = decode_transition(transition, tensor, run_id=run_id)
        receiver_records = [row for row in records if row["channel"] in observers]
        assert receiver_records == []
        assert engine.inverse_step(after).same_as(seed)
        row = {"case": label, "intensities": list(map(norm2, amplitudes)),
               "Born_ratio_reference": normalized(list(map(norm2, amplitudes))),
               "four_receiver_records": receiver_records, "complete_rewind": True,
               "seed_sha256": state_hash(seed), "final_sha256": state_hash(after)}
        rows.append(row)
        if record_sink is not None:
            record_sink({**row, "transition": transition, "canonical_clicks": records})
    assert rows[0]["Born_ratio_reference"] != rows[1]["Born_ratio_reference"]
    return {"cases": rows, "identical_receiver_records": True,
            "different_positive_Born_ratios": True,
            "result": "No decoder using only these four receiver record streams can recover the required Born ratios for every admitted apparatus seed in this one-update window.",
            "scope_limit": "This is not an impossibility proof for restricted preparations, longer windows, another interacting apparatus, or access to other channels."}


def audit(base, *, record_sink=None):
    extended = append_phase_observers(base)
    tensor, engine = extended.tensor, Engine(extended.tensor)
    cases, trials = [], []
    for label, amplitudes, stationary in CALIBRATIONS:
        intensities = list(map(norm2, amplitudes))
        counts, weights, classes = [0, 0], [0, 0], Counter()
        outcomes = Counter({"none": 0, "single": 0, "multiple": 0})
        for carry_pair in product(range(6), repeat=2):
            seed, nodes, detector = _prepared_seed(extended, amplitudes, carry_pair, stationary)
            after = engine.step(seed)
            assert engine.inverse_step(after).same_as(seed)
            run_id = f"born-calibration:{label}:{carry_pair[0]}:{carry_pair[1]}"
            transition = make_transition(tensor, seed, after, run_id=run_id, step=1)
            records = decode_transition(transition, tensor, run_id=run_id)
            selected = {(event["node"]): event for event in records
                        if event["channel"] == detector and event["node"] in nodes}
            hit = []
            quotients = []
            for side, node in enumerate(nodes):
                quotient = int(after.b[detector, node] + seed.a[detector, node])
                assert quotient == intensities[side]
                assert int(after.r[detector, node]) == carry_pair[side]
                event = selected.get(node)
                expected_hit = intensities[side] > 0 and not stationary
                assert (event is not None) == expected_hit
                hit.append(event is not None)
                quotients.append(quotient)
                if event is not None:
                    assert event["kind"] == "C0"
                    counts[side] += 1
                    weights[side] += event["quotient"]
                    classes[event["kind"]] += 1
            outcome = ("none", "single", "multiple")[sum(hit)]
            outcomes[outcome] += 1
            row = {"trial_id": run_id, "case": label, "initial_remainders": list(carry_pair),
                   "detector_nodes": list(nodes), "observed_clicks": hit,
                   "full_state_quotients": quotients, "outcome": outcome,
                   "seed_sha256": state_hash(seed), "final_sha256": state_hash(after),
                   "complete_rewind": True}
            trials.append(row)
            if record_sink is not None:
                record_sink({**row, "transition": transition, "canonical_clicks": records})
        cases.append({"case": label, "amplitudes": [list(z) for z in amplitudes],
                      "intensities": intensities, "stationary_apparatus": stationary,
                      "trials": 36, "outcomes": dict(outcomes), "binary_counts": counts,
                      "clicks_per_trial": [str(Fraction(c, 36)) for c in counts],
                      "share_of_binary_events": normalized(counts),
                      "observed_quotient_weights": weights,
                      "share_of_quotient_weights": normalized(weights),
                      "Born_ratio_reference": normalized(intensities),
                      "classes": dict(classes), "C2_selected_trials": 0})
    phase_rows = []
    link = tensor.gear_index(OBSERVER_NAMES[1])
    carrier = [tensor.gear_index(name) for name in CARRIER_NAMES]
    for label, left, right in (("constructive", (1, 0), (1, 0)),
                               ("destructive", (1, 0), (-1, 0)),
                               ("quadrature", (1, 0), (0, 1)),
                               ("common_rotation", (0, 1), (0, 1))):
        seed = extended.seed
        node = seed.lattice.index(0, 0, 0)
        neighbour = int(seed.lattice.shift_index((1, 0, 0))[node])
        for g in carrier:
            seed.a[g, :] = seed.b[g, :] = 0
        for g, x, y in zip(carrier, left, right):
            seed.b[g, node], seed.b[g, neighbour] = x, y
        after = engine.step(seed)
        expected = norm2(tuple(x + y for x, y in zip(left, right)))
        actual = int(after.b[link, node] + seed.a[link, node])
        assert actual == expected and engine.inverse_step(after).same_as(seed)
        phase_rows.append({"case": label, "coherent_intensity": actual,
                           "seed_sha256": state_hash(seed), "rewind_exact": True})
        if record_sink is not None:
            run_id = "phase-control:" + label
            transition = make_transition(tensor, seed, after, run_id=run_id, step=1)
            record_sink({"case": run_id, "transition": transition,
                         "canonical_clicks": decode_transition(transition, tensor, run_id=run_id)})
    report = {"schema": "universe24/validation/clock-link-born-bell/1",
              "base_bundle_id": base.bundle_id, "base_tensor_hash": base.tensor.fingerprint,
              "tensor_hash": tensor.fingerprint, "channels_per_node": tensor.G,
              "retained_integers_per_node": 3 * tensor.G,
              "preparation": "One-update arrival-surface calibration. Both carrier a/b fields are cleared; the stated b amplitudes and all 36 detector carry pairs are prepared. Other base state is retained. This is not a constrained Einstein or transported emission fixture.",
              "ensemble": "Each carry pair in 0..5 squared has equal assigned weight; no physical measure is derived. Every trial is kept.",
              "one_update_trials": len(trials), "cases": cases, "phase_controls": phase_rows,
              "all_rewinds_exact": True, "coherent_intensity_identity": "passed",
              "one_outcome_per_trial": "failed", "Born_binary_frequencies": "failed",
              "Bell_violation_from_Engine": "not_tested",
              "local_CHSH": local_chsh_bound(), "complexity_postweighting": complexity_reweighting(),
              "receiver_indistinguishability": receiver_indistinguishability(extended, record_sink=record_sink),
              "probability_sampling_feeds_Engine": False,
              "conclusion": "The retained apparatus records coherent intensity, not a normalized one-winner Born measurement. The missing mechanism is demonstrated on the actual tensor, not repaired by resampling its clicks."}
    return report, trials


def verify_saved_trials(path, tensor):
    """Reread every raw record and use the independent scalar update oracle."""
    from validation.clock_links.acceptance_audit import scalar_step
    expected = {f"born-calibration:{label}:{a}:{b}" for label, _, _ in CALIBRATIONS
                for a, b in product(range(6), repeat=2)}
    expected.update("phase-control:" + label for label in
                    ("constructive", "destructive", "quadrature", "common_rotation"))
    expected.update("receiver-indistinguishability:" + label for label in ("ratio_5_1", "ratio_1_5"))
    seen = set()
    engine = Engine(tensor)
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            transition = row["transition"]
            identity = transition["run_id"]
            if identity not in expected or identity in seen:
                raise ValueError("unknown or duplicate saved trial")
            seen.add(identity)
            before, after = (State.from_dict(transition[field]) for field in ("before", "after"))
            if not scalar_step(tensor, before).same_as(after):
                raise ValueError("saved trial disagrees with independent scalar oracle")
            if not engine.inverse_step(after).same_as(before):
                raise ValueError("saved trial fails complete inverse")
            if decode_transition(transition, tensor, run_id=identity) != row["canonical_clicks"]:
                raise ValueError("saved trial click stream disagrees with canonical decoder")
            for field, state in (("seed_sha256", before), ("final_sha256", after)):
                if field in row and row[field] != state_hash(state):
                    raise ValueError("saved trial state hash mismatch")
    if seen != expected:
        raise ValueError("saved trial file is incomplete")
    return {"saved_transitions_verified": len(seen), "independent_scalar_oracle": True,
            "all_complete_rewinds": True, "canonical_stream_parity": True,
            "unique_complete_declared_trials": True}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-bundle", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("runs/clock_links/born"))
    args = parser.parse_args(argv)
    base = load_bundle(args.base_bundle)
    if base.tensor.G != 44:
        raise ValueError("published integration report requires the declared 44-channel base")
    args.out.mkdir(parents=True, exist_ok=True)
    save_bundle(base, args.out / "input_bundle")
    with gzip.open(args.out / "complete_trials.jsonl.gz", "wt", encoding="utf-8") as stream:
        report, trials = audit(base, record_sink=lambda row: stream.write(json.dumps(row) + "\n"))
    report["saved_replay"] = verify_saved_trials(args.out / "complete_trials.jsonl.gz",
                                                 append_phase_observers(base).tensor)
    root = Path(__file__).resolve().parents[2]
    paths = ["validation/clock_links/born_bell_audit.py", "validation/clock_links/model.py",
             "validation/clock_links/acceptance_audit.py",
             "universe24/core/engine.py", "universe24/system/decoder.py"]
    report["source_sha256"] = {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                               for name in paths}
    report["complete_trials_sha256"] = hashlib.sha256((args.out / "complete_trials.jsonl.gz").read_bytes()).hexdigest()
    (args.out / "trials.json").write_text(json.dumps(trials) + "\n")
    (args.out / "report.json").write_text(json.dumps(report) + "\n")
    print(json.dumps({"channels": report["channels_per_node"], "trials": len(trials),
                      "Born_binary_frequencies": report["Born_binary_frequencies"],
                      "local_CHSH_bound": report["local_CHSH"]["maximum_CHSH"]}))


if __name__ == "__main__":
    main()
