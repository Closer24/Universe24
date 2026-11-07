"""Prospective two-site cooperation study using data-only component assembly.

The score is frozen before joint cases. The sole forward operation is the
unchanged Engine.advance. Every complete state is retained, including failures.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import time

from research.components import BoardSpec, PairedArm, SignalSource, TensorSpec, finalize, place, plain
from universe24.experiments.config import checkpoint_data
from universe24.observation.clicks import classify


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PAIRS = {"O": (4, 0), "N": (2, 2), "R": (0, 4)}
SIDES = ((-1, "L"), (1, "R"))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        handle.write(canonical(value) + "\n")


def isolated_id(phase_index, side, pattern, suffix="base"):
    return f"iso-p{phase_index}-{'L' if side == -1 else 'R'}-{pattern}-{suffix}"


def joint_id(phase_index, left, right):
    return f"joint-p{phase_index}-{left}-{right}"


def make_cases(protocol):
    patterns = protocol["family"]["ordered_patterns"]
    phases = protocol["family"]["source_phases"]
    common = {"side": protocol["geometry"]["side"], "arm_length": 6,
              "steps": 40, "window": [6, 40], "body_signs": [1, 1, 1]}
    calibration, later = [], []
    for phase_index, phase in enumerate(phases):
        for side, _ in SIDES:
            for pattern in patterns:
                variants = ["OO", "OO"]
                variants[0 if side == -1 else 1] = pattern
                case = {**common, "id": isolated_id(phase_index, side, pattern),
                        "kind": "isolated", "phase_index": phase_index,
                        "phase": phase, "patterns": variants, "pattern": pattern,
                        "isolated_side": side, "source_present": True,
                        "perturb_sites": []}
                (calibration if phase_index == 0 else later).append(case)
    for side, _ in SIDES:
        for pattern in patterns:
            variants = ["OO", "OO"]
            variants[0 if side == -1 else 1] = pattern
            for suffix, flips in (("i", [2]), ("j", [3]), ("ij", [2, 3])):
                calibration.append({**common, "steps": 15, "window": [6, 15],
                    "id": isolated_id(0, side, pattern, suffix), "kind": "calibration",
                    "phase_index": 0, "phase": phases[0], "patterns": variants,
                    "pattern": pattern, "isolated_side": side, "source_present": True,
                    "perturb_sites": flips})
    for left, right in itertools.product(patterns, repeat=2):
        later.append({**common, "id": f"null-{left}-{right}", "kind": "no_source",
            "phase_index": 0, "phase": phases[0], "patterns": [left, right],
            "source_present": False, "perturb_sites": []})
    for phase_index, phase in enumerate(phases):
        for left, right in itertools.product(patterns, repeat=2):
            later.append({**common, "id": joint_id(phase_index, left, right),
                "kind": "joint", "phase_index": phase_index, "phase": phase,
                "patterns": [left, right], "source_present": True, "perturb_sites": []})
    if len(calibration) + len(later) != protocol["family"]["registered_trajectories"]:
        raise ValueError("Frozen trajectory count differs from generated manifest")
    return calibration, later


def prepare_case(case):
    """One-time generic assembly. No callback or state-changing observer."""
    tensor = TensorSpec.from_signs(tuple(case["body_signs"]))
    origin = (case["side"] // 2,) * 3
    a, b = case["phase"]
    placements = [place(SignalSource(a=a, b=b, present=case["source_present"], tensor=tensor),
                        at=origin, name="source")]
    for side, label in SIDES:
        if case.get("isolated_side") is not None and side != case["isolated_side"]:
            continue
        pattern = case["patterns"][0 if side == -1 else 1]
        pairs = [PAIRS[letter] for letter in pattern]
        for index, site in enumerate((2, 3)):
            if site in case.get("perturb_sites", []):
                remainder = (pairs[index][0] + 2) % 6
                pairs[index] = (remainder, 4 - remainder)
        arm = PairedArm(direction=side, gate_pairs=tuple(pairs), tensor=tensor)
        placements.append(place(arm, at=origin, name=label))
    prepared = finalize(BoardSpec(case["side"], tensor=tensor), placements)
    expected = {}
    # Independent preparation-value audit; this does not evolve an alternate board.
    for side, _ in SIDES:
        if case.get("isolated_side") is not None and side != case["isolated_side"]:
            continue
        pattern = case["patterns"][0 if side == -1 else 1]
        for j in range(1, 7):
            pair = PAIRS[pattern[j - 2]] if j in (2, 3) else PAIRS["O"]
            if j in case.get("perturb_sites", []):
                rr = (pair[0] + 2) % 6
                pair = (rr, 4 - rr)
            for channel, remainder in zip((0, 14), pair):
                if remainder != 2:
                    expected[(origin[0] + side * j, origin[1], origin[2], channel)] = (0, 0, remainder)
    if case["source_present"]:
        expected[(*origin, 0)] = (a, b, 2)
        expected[(*origin, 14)] = (-a, -b, 2)
    if {address: tuple(value) for address, value in prepared.initial.cells.items()} != expected:
        raise AssertionError("Generic assembly differs from the declared preparation")
    return prepared


class Budget:
    def __init__(self, protocol):
        self.started_cpu = time.process_time()
        self.started_wall = time.monotonic()
        self.cpu_seconds = protocol["budget"]["cpu_seconds"]
        self.wall_seconds = protocol["budget"]["wall_seconds"]
        self.max_cells = protocol["budget"]["maximum_stored_channels"]

    def check(self, state=None):
        if time.process_time() - self.started_cpu > self.cpu_seconds:
            raise TimeoutError("Frozen selection CPU budget exhausted")
        if time.monotonic() - self.started_wall > self.wall_seconds:
            raise TimeoutError("Frozen selection wall budget exhausted")
        if state is not None and len(state.cells) > self.max_cells:
            raise MemoryError("Frozen selection retained-channel cap exceeded")


def outlet_summary(initial, positions):
    return {str(side): {"position": list(position), "first_full_change": None,
            "first_b": None, "first_C": None, "b_transmission": False,
            "strong_quiet": True, "C_events": [], "C_bank_times": [],
            "calibration_vector": [], "remainder_change_times": [],
            "baseline": [list(initial.at((*position, g))) for g in range(48)]}
            for side, position in positions.items()}


def record_case(case, folder, budget):
    started = time.process_time()
    folder.mkdir(parents=True, exist_ok=False)
    prepared = prepare_case(case)
    engine, initial = prepared.engine, prepared.initial
    save(folder / "assembly.json", plain(prepared.manifest))
    save(folder / "case.json", case)
    origin = (case["side"] // 2,) * 3
    positions = {side: (origin[0] + side * 6, origin[1], origin[2]) for side, _ in SIDES}
    summaries = outlet_summary(initial, positions)
    trace_path = folder / "states.jsonl.gz"
    frame_hashes, state, previous = [], initial, None
    stationary, max_cells = True, 0
    before_margin = min(min(v, case["side"] - 1 - v) for a in initial.cells for v in a[:3])
    if before_margin <= case["steps"]:
        raise ValueError("Initial support does not have the declared nonwrapping margin")
    with gzip.open(trace_path, "xt", encoding="utf-8", compresslevel=6) as trace:
        for t in range(case["steps"] + 1):
            budget.check(state)
            max_cells = max(max_cells, len(state.cells))
            stationary = stationary and state == initial
            frame = canonical(checkpoint_data(state, engine, t))
            frame_hashes.append(hashlib.sha256(frame.encode()).hexdigest())
            trace.write(frame + "\n")
            for side, position in positions.items():
                out = summaries[str(side)]
                values = [state.at((*position, g)) for g in range(48)]
                baseline = out["baseline"]
                changed = any(list(value) != baseline[g] for g, value in enumerate(values))
                nonzero_b = any(value.b != baseline[g][1] for g, value in enumerate(values))
                if t and changed and out["first_full_change"] is None:
                    out["first_full_change"] = t
                if t and nonzero_b and out["first_b"] is None:
                    out["first_b"] = t
                if case["window"][0] <= t <= case["window"][1]:
                    out["strong_quiet"] = out["strong_quiet"] and not changed
                    out["b_transmission"] = out["b_transmission"] or nonzero_b
                if 6 <= t <= 15:
                    out["calibration_vector"].extend(value.b for value in values)
                if previous is not None:
                    events = []
                    old_values = [previous.at((*position, g)) for g in range(48)]
                    if any(old.r != new.r for old, new in zip(old_values, values)):
                        out["remainder_change_times"].append(t)
                    for g, (old, new) in enumerate(zip(old_values, values)):
                        event = classify(old, new)
                        if event is not None:
                            kind, quotient = event
                            events.append({"step": t, "address": [*position, g],
                                           "kind": kind, "quotient": quotient,
                                           "before": list(old), "after": list(new)})
                    if events:
                        out["C_events"].extend(events)
                        out["C_bank_times"].append(t)
                        if out["first_C"] is None:
                            out["first_C"] = t
            if t < case["steps"]:
                previous = state
                state = engine.advance(previous)
                if engine.rewind(state) != previous:
                    raise AssertionError("One-step complete-state inverse failed")
    rewound = state
    for _ in range(case["steps"]):
        budget.check(rewound)
        rewound = engine.rewind(rewound)
    if rewound != initial:
        raise AssertionError("Complete rewind failed")
    for out in summaries.values():
        out["arrival_tuple"] = [out["first_full_change"], out["first_b"], out["first_C"]]
        out["C_in_window"] = any(case["window"][0] <= t <= case["window"][1] for t in out["C_bank_times"])
        out["functional"] = out["b_transmission"] and out["C_in_window"]
    result = {"case": case, "outlets": summaries, "full_one_step_inverses": True,
              "complete_rewind": True, "entire_board_stationary": stationary,
              "frames": case["steps"] + 1, "frame_sha256": frame_hashes,
              "trace_sha256": digest(trace_path), "trace": "states.jsonl.gz",
              "max_stored_channels": max_cells, "initial_boundary_margin": before_margin,
              "assembly_sha256": digest(folder / "assembly.json"),
              "coupling_fingerprint": engine.coupling.fingerprint,
              "cpu_seconds": time.process_time() - started}
    save(folder / "result.json", result)
    return result


def calculate_scores(records, patterns):
    scores = {}
    for side, _ in SIDES:
        for pattern in patterns:
            vectors = {suffix: records[isolated_id(0, side, pattern, suffix)]["outlets"][str(side)]["calibration_vector"]
                       for suffix in ("base", "i", "j", "ij")}
            if any(len(v) != 480 for v in vectors.values()):
                raise ValueError("Calibration vectors must have all480 coordinates")
            mixed = [ij - i - j + base for ij, i, j, base in
                     zip(vectors["ij"], vectors["i"], vectors["j"], vectors["base"])]
            count = sum(value != 0 for value in mixed)
            score = Fraction(count, 480)
            scores[f"{side},{pattern}"] = {"score": str(score), "nonzero_coordinates": count,
                "vector_length": 480, "binary_K_diagnostic": int(count != 0),
                "mixed_vector": mixed, "calibration_vectors": vectors}
    return scores


def comparisons(records, scores, patterns, phase_count):
    rows = []
    for p in range(phase_count):
        for left, right in itertools.product(patterns, repeat=2):
            identifier = joint_id(p, left, right)
            if identifier not in records:
                continue
            joint = records[identifier]
            isolated = {str(side): records[isolated_id(p, side, pattern)]["outlets"][str(side)]
                        for side, pattern in ((-1, left), (1, right))}
            values = [Fraction(scores[f"-1,{left}"]["score"]), Fraction(scores[f"1,{right}"]["score"])]
            both_functional = all(out["functional"] for out in isolated.values())
            matched = isolated["-1"]["arrival_tuple"] == isolated["1"]["arrival_tuple"]
            unequal = values[0] != values[1]
            high = -1 if values[0] > values[1] else 1
            out = joint["outlets"]
            sole = [side for side, _ in SIDES if out[str(side)]["functional"] and out[str(-side)]["strong_quiet"]]
            unique = len(sole) == 1
            eligible = both_functional and matched and unequal
            rows.append({"id": identifier, "phase_index": p, "patterns": [left, right],
                "scores": [str(v) for v in values], "both_isolated_functional": both_functional,
                "isolated_arrival_tuples": [isolated["-1"]["arrival_tuple"], isolated["1"]["arrival_tuple"]],
                "matched_arrivals": matched, "unequal_scores": unequal, "primary_eligible": eligible,
                "higher_side": high if unequal else None,
                "unique_outlet_side": sole[0] if unique else None,
                "higher_only": unequal and unique and sole[0] == high,
                "competitive_component": both_functional and unique,
                "category": ("left_only" if sole == [-1] else "right_only" if sole == [1]
                    else "both_functional" if all(out[str(s)]["functional"] for s, _ in SIDES)
                    else "both_quiet" if all(out[str(s)]["strong_quiet"] for s, _ in SIDES)
                    else "partial_or_remainder_only"),
                "null_stationary": records[f"null-{left}-{right}"]["entire_board_stationary"]})
    by_id = {row["id"]: row for row in rows}
    strong, competitive = None, None
    for left, right in itertools.combinations(patterns, 2):
        ids = [joint_id(p, l, r) for p in range(phase_count) for l, r in ((left, right), (right, left))]
        if not all(identifier in by_id for identifier in ids):
            continue
        group = [by_id[identifier] for identifier in ids]
        if strong is None and all(row["primary_eligible"] and row["higher_only"] for row in group):
            strong = {"patterns": [left, right], "joint_ids": ids}
        if competitive is None and all(row["competitive_component"] for row in group):
            competitive = {"patterns": [left, right], "joint_ids": ids}
    eligible = [row for row in rows if row["primary_eligible"]]
    summary = {"comparisons": len(rows), "eligible_comparisons": len(eligible),
               "eligible_higher_only": sum(row["higher_only"] for row in eligible),
               "eligible_counterexamples": sum(not row["higher_only"] for row in eligible),
               "unmatched_functional_unequal": sum(row["both_isolated_functional"] and row["unequal_scores"] and not row["matched_arrivals"] for row in rows),
               "functional_ties": sum(row["both_isolated_functional"] and not row["unequal_scores"] for row in rows),
               "competitive_comparisons": sum(row["competitive_component"] for row in rows),
               "strong_candidate": strong, "competitive_candidate": competitive,
               "selected_for_holdout": strong or competitive,
               "selected_claim": "arrival_matched_cooperation_candidate" if strong else "prepared_competition_only" if competitive else None,
               "primary_prediction_status": ("inconclusive_no_eligible_comparisons" if not eligible else
                    "finite_prediction_passed" if all(row["higher_only"] for row in eligible) else "finite_prediction_refuted")}
    return rows, summary


def main(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    protocol_path = HERE / "selection_protocol.json"
    protocol_bytes = protocol_path.read_bytes()
    protocol = json.loads(protocol_bytes)
    calibration, later = make_cases(protocol)
    (output / "protocol.json").write_bytes(protocol_bytes)
    save(output / "candidate_manifest.json", {"calibration": calibration, "later": later})
    files = sorted(set(ROOT.glob("universe24/**/*.py")) | set(ROOT.glob("research/components/*.py")) |
                   {Path(__file__), protocol_path})
    sources = {str(path.relative_to(ROOT)): digest(path) for path in files}
    for path in files:
        target = output / "source" / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    save(output / "source_manifest.json", {"git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
         "sources": sources, "seed": None, "enumeration": "Complete deterministic frozen family"})
    budget = Budget(protocol)
    records, scores, failure = {}, None, None
    for stage, cases in (("calibration", calibration), ("joint_and_controls", later)):
        for case in cases:
            try:
                records[case["id"]] = record_case(case, output / "cases" / case["id"], budget)
                if len(records) % 20 == 0:
                    print(canonical({"completed": len(records), "registered": len(calibration) + len(later),
                                     "stage": stage, "cpu_seconds": round(time.process_time() - budget.started_cpu, 3)}), flush=True)
            except (TimeoutError, MemoryError, AssertionError, ValueError) as exc:
                failure = {"case": case["id"], "stage": stage, "type": type(exc).__name__, "message": str(exc)}
                break
        if failure:
            break
        if stage == "calibration":
            scores = calculate_scores(records, protocol["family"]["ordered_patterns"])
            save(output / "calibration_scores.json", scores)
            print(canonical({"stage": "scores_frozen_before_joint_runs", "scores_sha256": digest(output / "calibration_scores.json")}), flush=True)
    rows, summary = (comparisons(records, scores, protocol["family"]["ordered_patterns"],
                               len(protocol["family"]["source_phases"])) if scores is not None
                     else ([], {"primary_prediction_status": "inconclusive_incomplete_calibration"}))
    if failure:
        summary["primary_prediction_status"] = "inconclusive_incomplete_execution"
    summary.update({"execution_status": "completed" if failure is None else "inconclusive",
                    "failure": failure, "runs_completed": len(records), "runs_registered": len(calibration) + len(later),
                    "forward_steps": sum(record["case"]["steps"] for record in records.values()),
                    "cpu_seconds": time.process_time() - budget.started_cpu,
                    "wall_seconds": time.monotonic() - budget.started_wall,
                    "all_full_inverses": all(r["full_one_step_inverses"] and r["complete_rewind"] for r in records.values()),
                    "all_null_stationary": all(r["entire_board_stationary"] for r in records.values() if r["case"]["kind"] == "no_source"),
                    "sources_unchanged": sources == {str(path.relative_to(ROOT)): digest(path) for path in files},
                    "generic_component_preparations": True, "old_K_failure_changed": False,
                    "physical_complexity_law_claim": False, "joined_confirmation_claim": False})
    save(output / "result.json", {"summary": summary, "comparisons": rows,
          "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
          "calibration_scores_sha256": digest(output / "calibration_scores.json") if scores is not None else None,
          "cases": {identifier: {"result": f"cases/{identifier}/result.json", "trace": f"cases/{identifier}/states.jsonl.gz",
                                 "result_sha256": digest(output / "cases" / identifier / "result.json"),
                                 "trace_sha256": record["trace_sha256"]}
                    for identifier, record in records.items()}})
    print(canonical(summary), flush=True)
    return 0 if failure is None else 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    raise SystemExit(main(parser.parse_args().output))
