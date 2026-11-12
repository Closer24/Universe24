"""Complete-trial quantum claim guards; no alternative dynamics or sampler.

The exact controls here test a reader and the local-model CHSH algebra. They
are not Engine evidence for quantum theory. Run with ``python -m
validation.geodesic_board.quantum_audit``; all arithmetic is exact.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


@dataclass(frozen=True)
class Trial:
    trial_id: str
    settings: tuple[int, int]
    left: tuple[int, ...]
    right: tuple[int, ...]


def _fraction(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def complete_trial_summary(trials: list[Trial],
                           manifest: dict[str, tuple[int, int]]) -> dict:
    """Read every predeclared trial; no-click is 0, multi-click is invalid.

    This exact empirical CHSH estimate alone is not a significance test. The
    local bound is a population/complete common-ensemble result; finite random
    samples can exceed it. Setting independence and spacelike separation need
    separately established preparation/causal provenance.
    """
    if not manifest:
        raise ValueError("a nonempty predeclared emission manifest is required")
    valid_settings = set(product((0, 1), repeat=2))
    for trial_id, settings in manifest.items():
        if not isinstance(trial_id, str) or not trial_id:
            raise ValueError("invalid trial id")
        if (type(settings) is not tuple or len(settings) != 2
                or any(type(x) is not int for x in settings)
                or settings not in valid_settings):
            raise ValueError("manifest settings must be two integer bits")
    seen = set()
    counts = {xy: 0 for xy in valid_settings}
    sums = {xy: 0 for xy in valid_settings}
    missing_sides = double_sides = coincident = 0
    for trial in trials:
        if trial.trial_id in seen or trial.trial_id not in manifest:
            raise ValueError("duplicate or unknown trial")
        seen.add(trial.trial_id)
        if (type(trial.settings) is not tuple or len(trial.settings) != 2
                or any(type(x) is not int for x in trial.settings)
                or trial.settings != manifest[trial.trial_id]):
            raise ValueError("settings disagree with predeclared manifest")
        for outcomes in (trial.left, trial.right):
            if (type(outcomes) is not tuple
                    or any(type(x) is not int or x not in (-1, 1) for x in outcomes)):
                raise ValueError("outcomes must be tuples of integer +/-1 records")
            missing_sides += len(outcomes) == 0
            double_sides += len(outcomes) > 1
        counts[trial.settings] += 1
        if len(trial.left) <= 1 and len(trial.right) <= 1:
            a = trial.left[0] if trial.left else 0
            b = trial.right[0] if trial.right else 0
            sums[trial.settings] += a*b
            coincident += bool(trial.left and trial.right)
    if seen != set(manifest):
        raise ValueError("missing emission trials, including possible nondetections")
    if any(n == 0 for n in counts.values()):
        raise ValueError("all four settings require predeclared trials")
    correlations = {xy: Fraction(sums[xy], counts[xy]) for xy in valid_settings}
    score = abs(correlations[0, 0] + correlations[0, 1]
                + correlations[1, 0] - correlations[1, 1])
    return {
        "emissions": len(trials), "nondetection_sides": missing_sides,
        "multiple_record_sides": double_sides, "coincident_trials": coincident,
        "exclusive_outcome_contract": double_sides == 0,
        "nondetection_policy": "include every emission; assign no-click outcome 0",
        "settings_counts": {str(xy): counts[xy] for xy in sorted(counts)},
        "correlations": ({str(xy): _fraction(correlations[xy])
                           for xy in sorted(correlations)} if not double_sides else None),
        "chsh": _fraction(score) if not double_sides else None,
        "significance_test": "not_performed",
        "measurement_independence": "requires_external_preparation_evidence",
        "metric_spacelike_separation": "requires_same_run_geometry_evidence",
    }


def _local_bound_control() -> dict:
    # Every extremal local deterministic response, including no-click=0.
    values = []
    for a0, a1, b0, b1 in product((-1, 0, 1), repeat=4):
        value = a0*b0 + a0*b1 + a1*b0 - a1*b1
        assert abs(value) <= 2
        values.append(value)
    # A common nonnegative normalized mixture cannot exceed its vertices.
    mixture = sum(Fraction(i+1, sum(range(1, 82)))*v
                  for i, v in enumerate(values))
    assert abs(mixture) <= 2
    return {"local_vertices_checked": len(values), "maximum_absolute_chsh": 2,
            "exact_common_weight_mixture": _fraction(mixture),
            "assumptions": ["local response A(x,lambda), B(y,lambda)",
                            "one setting-independent distribution of lambda",
                            "bounded outcomes and complete predeclared trials"],
            "scope": "exact algebra control, not a finite-sample p-value"}


def _selection_control() -> tuple[dict, list[Trial], dict]:
    # lambda=(i,j,s) is sampled identically for all four setting pairs.
    # Each detector's acceptance uses only its own setting and lambda.
    trials, manifest = [], {}
    selected_sums = {(x, y): 0 for x, y in product((0, 1), repeat=2)}
    selected_counts = dict.fromkeys(selected_sums, 0)
    for i, j, s in product((0, 1), (0, 1), (-1, 1)):
        for x, y in product((0, 1), repeat=2):
            trial_id = f"{i}:{j}:{s}:{x}:{y}"
            a = (s,) if x == i else ()
            b = (s*(-1)**(i*j),) if y == j else ()
            trials.append(Trial(trial_id, (x, y), a, b))
            manifest[trial_id] = (x, y)
            if a and b:
                selected_sums[x, y] += a[0]*b[0]
                selected_counts[x, y] += 1
    complete = complete_trial_summary(trials, manifest)
    e = {xy: Fraction(selected_sums[xy], selected_counts[xy]) for xy in selected_sums}
    selected = abs(e[0, 0]+e[0, 1]+e[1, 0]-e[1, 1])
    assert selected == 4 and complete["chsh"] == _fraction(Fraction(1))
    return ({"complete": complete, "coincidence_selected_chsh": _fraction(selected),
             "selected_claim_rejected": True,
             "explanation": "local detection selects different lambda ensembles at each setting"},
            trials, manifest)


def audit() -> dict:
    selection, trials, manifest = _selection_control()
    rejected = []
    bad_cases = {
        "omitted_nondetection": trials[:-1],
        "duplicate": trials+[trials[0]],
        "unknown": trials+[Trial("unknown", (0, 0), (), ())],
        "changed_settings": [Trial(trials[0].trial_id, (1, 1), (), ())]+trials[1:],
        "noninteger_outcome": [Trial(trials[0].trial_id, (0, 0), (True,), ())]+trials[1:],
    }
    for name, rows in bad_cases.items():
        try:
            complete_trial_summary(rows, manifest)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(f"accepted invalid control: {name}")
    doubled = [Trial(t.trial_id, t.settings, (1, -1), (1,)) for t in trials]
    doubles = complete_trial_summary(doubled, manifest)
    assert not doubles["exclusive_outcome_contract"] and doubles["chsh"] is None
    # Intensity weights alone do not implement an exclusive categorical outcome.
    # This is a synthetic regression for the published #49 failure, not a rerun.
    weights, binary_counts = (324, 36), (36, 36)
    weighted = Fraction(weights[0], sum(weights))
    counted = Fraction(binary_counts[0], sum(binary_counts))
    assert weighted == Fraction(9, 10) and counted == Fraction(1, 2)
    return {
        "schema": "universe24.quantum_claim_audit.v1",
        "scope": "passive exact protocol controls; no Engine quantum apparatus is added",
        "software_controls": "passed", "extra_retained_channels": 0,
        "local_chsh": _local_bound_control(), "selection_negative_control": selection,
        "invalid_records_rejected": rejected, "multiple_record_control": doubles,
        "intensity_is_not_binary_born": {"weighted_fraction": _fraction(weighted),
            "binary_fraction": _fraction(counted), "exclusive_outcomes": False,
            "scope": "synthetic arithmetic illustration of published PR49 finding"},
        "physical_gates": {
            "unitary_or_equivalent_operational_state_space": "not_established",
            "exclusive_born_outcomes_from_engine": "not_established",
            "engine_bell_apparatus": "not_implemented",
            "bell_violation_under_stated_local_model_assumptions": "excluded_by_bound",
            "shared_metric_quantum_apparatus": "not_implemented",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/geodesic_board/quantum.json"))
    args = parser.parse_args()
    result = audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"output": str(args.out), "software_controls": "passed",
                      "physical_gates": result["physical_gates"]}, indent=2))


if __name__ == "__main__":
    main()
