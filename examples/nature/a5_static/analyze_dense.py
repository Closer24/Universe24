"""Read the records of Run 2 of experiment A5s (docs/EXPERIMENTS.md, "Run 2, to
the steady state (dense mode)") and evaluate its pre-registered criterion clause
by clause against the mean field's predictions written before the run
(predictions.json, by predict_dense.py): (1) every ledger line balanced and
`conserved_at_every_completed_tick` at every tick; (2) the registers equal and
opposite at every tick, the control zero; (3) the engine's steady-state push
F(r), the mean over the last 32 ticks, within 3 % of the prediction for the
same box and ticks at every r; (4) the log-log exponent over the r run equal to
the mean field's over the same points within 0.1, the asymptote stated beside
it; (5) the opposite-charge series the exact negation of the like-charge series
at r = 16. The per-run reading is analyze.py's (the registers from the
`external_body_absorbed` records, the ledger from `run.json`); nothing here
reads the engine. A run directory that does not exist yet is reported as
missing and its clauses evaluate over what exists.

Run:  python examples/nature/a5_static/analyze_dense.py RUN [RUN ...] [--predictions predictions.json] [--out summary.json] [--record record_dense.json]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUSH_TOLERANCE = 0.03
EXPONENT_TOLERANCE = 0.1
NEGATION_DISTANCE = 16


def load_analyze():
    spec = importlib.util.spec_from_file_location("a5_static_analyze", HERE / "analyze.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_predictions(path):
    predictions = json.loads(Path(path).read_text(encoding="utf-8"))
    return {row["r"]: row for row in predictions["rows"]}, predictions


def analyze_run(analyze, run):
    directory = Path(run)
    if not (directory / "run.json").exists():
        return {"run": str(directory), "missing": True}
    result = analyze.analyze(directory)
    metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    result["missing"] = False
    result["dense_field"] = metadata.get("dense_field")
    result["completed_ticks"] = metadata["completed_ticks"]
    result["planned_ticks"] = result["ticks"]
    return result


def case_of(r):
    return "control" if r["control"] else ("pp" if r["like"] else "pe")


def force_x(r):
    """The steady push per interval on B along x (on A for the control)."""
    index = 0 if r["control"] else 1
    return r["steady"][index]["mean"][0]


def clauses(analyze, results, predictions, fits_predicted):
    present = [r for r in results if not r["missing"]]
    by_case = {}
    for r in present:
        by_case.setdefault(case_of(r), []).append(r)
    pp = sorted(by_case.get("pp", []), key=lambda r: r["manhattan"])
    pe = sorted(by_case.get("pe", []), key=lambda r: r["manhattan"])
    table = []
    # 1. Every ledger line balanced and conserved at every tick of every world.
    ledger = {
        r["model"]: {
            "all_balanced": r["all_balanced"],
            "conserved": r["conserved_at_every_completed_tick"],
            "status": r["status"],
            "completed_ticks": r["completed_ticks"],
            "dense_field": r["dense_field"],
        }
        for r in present
    }
    table.append(
        {
            "clause": "ledger balanced and conserved at every tick of every world",
            "pass": bool(ledger)
            and all(
                v["all_balanced"] and v["conserved"] and v["status"] == "completed"
                for v in ledger.values()
            ),
            "numbers": ledger,
        }
    )
    # 2. Registers equal and opposite at every tick; the control (0, 0, 0).
    registers = {
        r["model"]: (
            {"control_zero_every_tick": r["control_zero"], "absorptions": r["absorptions"]}
            if r["control"]
            else {"equal_opposite_every_tick": r["equal_opposite"], "final": r["final_registers"]}
        )
        for r in present
    }
    table.append(
        {
            "clause": "registers equal and opposite at every tick, the control zero",
            "pass": bool(registers)
            and any(r["control"] for r in present)
            and all((r["control_zero"] if r["control"] else r["equal_opposite"]) for r in present),
            "numbers": registers,
        }
    )
    # 3. F(r) within 3 % of the mean field's prediction for the same box and ticks.
    pushes = {}
    for r in pp + pe:
        prediction = predictions.get(r["manhattan"])
        if prediction is None:
            continue
        sign = 1 if r["like"] else -1
        predicted = sign * prediction["predicted_push"]
        measured = force_x(r)
        pushes[r["model"]] = {
            "r": r["manhattan"],
            "ticks": r["ticks"],
            "predicted_ticks": prediction["ticks"],
            "F": measured,
            "window_sum": r["steady"][1]["sum"],
            "previous_window_mean": r["steady"][1]["previous_mean"],
            "predicted": predicted,
            "steady_state": sign * prediction["steady_push"],
            "relative_deviation": (measured - predicted) / predicted,
            "within_3_percent": abs(measured - predicted) <= PUSH_TOLERANCE * abs(predicted),
            "first_push": r["first_push"]["1"] if "1" in r["first_push"] else r["first_push"][1],
            "predicted_first_push": prediction["first_push_tick"],
        }
    table.append(
        {
            "clause": "F(r) within 3 % of the mean field's prediction at every r",
            "pass": bool(pushes)
            and all(v["within_3_percent"] for v in pushes.values())
            and all(v["ticks"] == v["predicted_ticks"] for v in pushes.values()),
            "numbers": pushes,
        }
    )
    # 4. The log-log exponent over the r run against the mean field's over the same points.
    points = [(r["manhattan"], abs(force_x(r))) for r in pp]
    engine_fit = analyze.fit(points)
    same = [(r, predictions[r]["predicted_push"]) for r, _ in points if r in predictions]
    mean_fit = analyze.fit(same)
    steady_fit = analyze.fit([(r, predictions[r]["steady_push"]) for r, _ in same])
    difference = (
        engine_fit["exponent"] - mean_fit["exponent"]
        if engine_fit["exponent"] is not None and mean_fit["exponent"] is not None
        else None
    )
    table.append(
        {
            "clause": "log-log exponent over the r run equals the mean field's within 0.1",
            "pass": difference is not None and abs(difference) <= EXPONENT_TOLERANCE,
            "numbers": {
                "engine": {"series": points, **engine_fit},
                "mean_field_same_points": {"series": same, **mean_fit},
                "mean_field_steady_state_same_points": steady_fit,
                "difference": difference,
                "asymptote": fits_predicted,
            },
        }
    )
    # 5. pe = -pp at r = 16, tick by tick.
    negation = {}
    like = next((r for r in pp if r["manhattan"] == NEGATION_DISTANCE), None)
    opposite = next((r for r in pe if r["manhattan"] == NEGATION_DISTANCE), None)
    if like is not None and opposite is not None:
        negation = {
            "r": NEGATION_DISTANCE,
            "pe_series_is_minus_pp_series": opposite["register_series"]
            == {k: [[-c for c in v] for v in s] for k, s in like["register_series"].items()},
            "F_pp": force_x(like),
            "F_pe": force_x(opposite),
            "window_sum_pp": like["steady"][1]["sum"],
            "window_sum_pe": opposite["steady"][1]["sum"],
        }
    table.append(
        {
            "clause": "opposite charges the exact negation of like charges at r = 16",
            "pass": bool(negation) and negation["pe_series_is_minus_pp_series"],
            "numbers": negation,
        }
    )
    return table


def print_run(r):
    if r["missing"]:
        print(f"== {r['run']}: no record yet")
        return
    print(
        f"== {r['model']}  offset={r['offset']} r={r['manhattan']} shape={r['shape']}"
        f" ticks={r['ticks']} status={r['status']} dense_field={r['dense_field']}"
        f" elapsed={r['elapsed_seconds']:.0f}s"
    )
    print(f"   source {r['source_sha256']}  init {r['initialization_sha256']}")
    for index, body in enumerate(r["bodies"]):
        s = r["steady"][index]
        print(
            f"   body {index} {body['family']} at {body['position']}: first push tick"
            f" {r['first_push'][index]}, final register {r['final_registers'][index]},"
            f" F (last {s['window']}) {[round(c, 4) for c in s['mean']]}"
            + (
                f", the window before {[round(c, 4) for c in s['previous_mean']]}"
                if s["previous_mean"]
                else ""
            )
        )
    print(
        f"   balanced {r['all_balanced']} conserved {r['conserved_at_every_completed_tick']}"
        f" positions fixed {r['positions_fixed']} equal+opposite {r['equal_opposite']}"
        f" control zero {r['control_zero']} momentum ledger zero {r['momentum_line_zero']}"
    )
    # The register of B (of A for the control) every 32 ticks and at the end.
    index = "0" if r["control"] else "1"
    series = r["register_series"][index]
    marks = list(range(31, len(series), 32))
    if not marks or marks[-1] != len(series) - 1:
        marks.append(len(series) - 1)
    print("   register at tick: " + ", ".join(f"{t + 1}: {series[t][0]}" for t in marks))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--predictions", type=Path, default=HERE / "predictions.json")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    analyze = load_analyze()
    predictions, document = read_predictions(args.predictions)
    results = [analyze_run(analyze, run) for run in args.runs]
    for r in results:
        print_run(r)
    table = clauses(analyze, results, predictions, {**document["fits"], **document["asymptote"]})
    print("\n== Criterion of A5s, Run 2, clause by clause")
    for entry in table:
        verdict = "----" if entry["pass"] is None else ("PASS" if entry["pass"] else "FAIL")
        print(f"   {verdict}  {entry['clause']}")
        print("         " + json.dumps(entry["numbers"], default=str)[:2000])
    if args.out:
        args.out.write_text(
            json.dumps({"runs": results, "clauses": table}, indent=1) + "\n", encoding="utf-8"
        )
    if args.record:
        record = {
            "predictions": str(args.predictions),
            "runs": [
                {k: r[k] for k in r if k not in ("rows", "run")} for r in results if not r["missing"]
            ],
            "clauses": table,
        }
        args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
