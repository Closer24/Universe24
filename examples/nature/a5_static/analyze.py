"""Read the records of experiment A5s (docs/EXPERIMENTS.md) and evaluate its
criterion clause by clause: each body's momentum register per tick (from the
`external_body_absorbed` records), the push per interval, the steady-state push
F(r) as the mean over the last 32 ticks, the log-log least-squares exponent of
F(r) over the axis distances with its standard error, the ledger, the control,
the equal and opposite registers, the sign of the push and the diagonal series
against the axis fit. A Renderer of records in the sense of Highlights 3.29: it
reads only what the runner wrote (``run.json``, ``events.jsonl``,
``initialization.json``) and never the engine.

Run:  python examples/nature/a5_static/analyze.py RUN [RUN ...] [--out summary.json] [--record record.json]
where RUN is a run directory (``run.json`` beside ``events.jsonl``) of one world
of ``make_worlds.py``. The per-tick table of every run and the clause table are
printed; ``--out`` writes the full summary and ``--record`` the small committed
record the test reads.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

WINDOW = 32
BAND = (-2.2, -1.8)


def add(u, v):
    return tuple(a + b for a, b in zip(u, v, strict=True))


def sub(u, v):
    return tuple(a - b for a, b in zip(u, v, strict=True))


def load(run):
    directory = Path(run)
    metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    world = json.loads((directory / "initialization.json").read_text(encoding="utf-8"))
    return directory, metadata, world


def geometry(world):
    """The bodies, their families, charges and tables, and the offset of B from A."""
    bodies = []
    charges = {entry["field"]: entry.get("charge", 0) for entry in world["spatial_fields"]}
    fields = {
        entry["field_of"]: entry["field"] for entry in world["spatial_fields"] if "field_of" in entry
    }
    for body in world["external_bodies"]:
        bodies.append(
            {
                "family": body["family"],
                "charge": body["charge"],
                "position": tuple(body["position"]),
                "amount": body["amount"],
                "table": body["momentum_table"],
                "light": fields[body["family"]],
            }
        )
    offset = (0, 0, 0)
    if len(bodies) == 2:
        offset = sub(bodies[1]["position"], bodies[0]["position"])
    manhattan = sum(abs(c) for c in offset)
    return {
        "bodies": bodies,
        "charges": charges,
        "offset": offset,
        "manhattan": manhattan,
        "euclidean": math.sqrt(sum(c * c for c in offset)),
        "diagonal": offset[1] != 0,
        "control": len(bodies) == 1,
        "like": len(bodies) == 2 and bodies[0]["charge"] * bodies[1]["charge"] > 0,
    }


def analyze(run):
    directory, metadata, world = load(run)
    geo = geometry(world)
    ticks = int(metadata["completed_ticks"])
    count = len(geo["bodies"])
    # The register of each body after each tick: the momentum the last absorption
    # of the tick left it with, unchanged on a tick without one.
    last = {index: {} for index in range(count)}
    absorbed = {index: 0 for index in range(count)}
    with (directory / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            if '"external_body_absorbed"' not in line:
                continue
            event = json.loads(line)
            if event.get("event") != "external_body_absorbed":
                continue
            last[event["body"]][event["tick"]] = tuple(event["momentum"])
            absorbed[event["body"]] += 1
    registers = {index: [] for index in range(count)}
    for index in range(count):
        current = (0, 0, 0)
        for t in range(1, ticks + 1):
            current = last[index].get(t, current)
            registers[index].append(current)
    pushes = {
        index: [
            sub(registers[index][t], registers[index][t - 1] if t else (0, 0, 0)) for t in range(ticks)
        ]
        for index in range(count)
    }
    audit = {entry["tick"]: entry for entry in metadata["audit"]}
    rows = []
    for t in range(1, ticks + 1):
        line = audit[t]
        rows.append(
            {
                "tick": t,
                "registers": [list(registers[index][t - 1]) for index in range(count)],
                "pushes": [list(pushes[index][t - 1]) for index in range(count)],
                "balanced": line["balanced"],
                "bodies_momentum": list(line["bodies"]["momentum"]),
                "momentum_line": {
                    key: list(line["fields"]["momentum"][key])
                    for key in ("sourced", "current", "escaped", "absorbed")
                },
                "light_current": [line["fields"][body["light"]]["current"][0] for body in geo["bodies"]],
                "light_escaped": [line["fields"][body["light"]]["escaped"][0] for body in geo["bodies"]],
            }
        )
    first_push = {
        index: next((t + 1 for t, push in enumerate(pushes[index]) if any(push)), None)
        for index in range(count)
    }
    window = min(WINDOW, ticks)
    steady = {}
    for index in range(count):
        end = registers[index][ticks - 1]
        start = registers[index][ticks - 1 - window] if ticks > window else (0, 0, 0)
        total = sub(end, start)
        previous_total = None
        if ticks > 2 * window:
            previous_total = sub(
                registers[index][ticks - 1 - window], registers[index][ticks - 1 - 2 * window]
            )
        steady[index] = {
            "window": window,
            "sum": list(total),
            "mean": [c / window for c in total],
            "previous_sum": list(previous_total) if previous_total is not None else None,
            "previous_mean": [c / window for c in previous_total]
            if previous_total is not None
            else None,
        }
    positions_fixed = all(
        all(entry[1:] == list(body["position"]) for entry in record["positions"])
        for body, record in zip(geo["bodies"], metadata["external_bodies"], strict=True)
    )
    equal_opposite = count == 2 and all(
        add(registers[0][t], registers[1][t]) == (0, 0, 0) for t in range(ticks)
    )
    control_zero = count == 1 and all(registers[0][t] == (0, 0, 0) for t in range(ticks))
    return {
        "run": str(directory),
        "model": metadata["model"],
        "status": metadata["status"],
        "error": metadata.get("error"),
        "source_sha256": metadata["source_sha256"],
        "initialization_sha256": metadata["initialization_sha256"],
        "elapsed_seconds": metadata["elapsed_seconds"],
        "ticks": ticks,
        "shape": world["shape"],
        "control": geo["control"],
        "diagonal": geo["diagonal"],
        "like": geo["like"],
        "offset": list(geo["offset"]),
        "manhattan": geo["manhattan"],
        "euclidean": geo["euclidean"],
        "bodies": [
            {k: (list(v) if isinstance(v, tuple) else v) for k, v in body.items()}
            for body in geo["bodies"]
        ],
        "absorptions": absorbed,
        "first_push": first_push,
        "final_registers": [list(registers[index][ticks - 1]) for index in range(count)],
        "steady": steady,
        "positions_fixed": positions_fixed,
        "equal_opposite": equal_opposite,
        "control_zero": control_zero,
        "all_balanced": all(row["balanced"] for row in rows),
        "conserved_at_every_completed_tick": metadata["conserved_at_every_completed_tick"],
        "bodies_momentum_zero": all(row["bodies_momentum"] == [0, 0, 0] for row in rows),
        "momentum_line_zero": all(
            all(v == [0, 0, 0] for v in row["momentum_line"].values()) for row in rows
        ),
        "final_totals": metadata["final_totals"],
        "escaped_totals": metadata["escaped_totals"],
        "sink_totals": metadata["external_body_totals"],
        "register_series": {str(index): [list(r) for r in registers[index]] for index in range(count)},
        "rows": rows,
    }


def fit(points):
    """Least-squares slope of ln F over ln r with its standard error; None when an
    F is 0 (no logarithm) or fewer than three points remain."""
    usable = [(r, v) for r, v in points if v > 0]
    n = len(usable)
    if n < 3 or n != len(points):
        return {
            "exponent": None,
            "standard_error": None,
            "intercept": None,
            "points": n,
            "zeros": len(points) - n,
        }
    xs = [math.log(r) for r, _ in usable]
    ys = [math.log(v) for _, v in usable]
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    slope = sxy / sxx
    intercept = my - slope * mx
    residual = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys, strict=True))
    se = math.sqrt(residual / (n - 2) / sxx) if n > 2 else None
    return {"exponent": slope, "standard_error": se, "intercept": intercept, "points": n, "zeros": 0}


def force(result, index):
    """The steady push per interval on body `index`: the mean over the last window."""
    return result["steady"][index]["mean"]


def case_of(result):
    return (
        "control"
        if result["control"]
        else ("diagonal" if result["diagonal"] else ("pp" if result["like"] else "pe"))
    )


def clauses(results):
    """The criterion of A5s, each clause with its verdict and its numbers."""
    by_case = {}
    for r in results:
        by_case.setdefault(case_of(r), []).append(r)
    axis = {case: sorted(by_case.get(case, []), key=lambda r: r["manhattan"]) for case in ("pp", "pe")}
    table = []
    # 1. Every ledger line balanced, conserved_at_every_completed_tick, at every tick of every world.
    ledger = {
        r["model"]: {
            "all_balanced": r["all_balanced"],
            "conserved": r["conserved_at_every_completed_tick"],
            "status": r["status"],
        }
        for r in results
    }
    table.append(
        {
            "clause": "ledger balanced and conserved at every tick of every world",
            "pass": bool(results)
            and all(
                v["all_balanced"] and v["conserved"] and v["status"] == "completed"
                for v in ledger.values()
            ),
            "numbers": ledger,
        }
    )
    # 2. The control's register (0, 0, 0) at every tick.
    control = {
        r["model"]: {
            "zero_every_tick": r["control_zero"],
            "final": r["final_registers"],
            "absorptions": r["absorptions"],
        }
        for r in by_case.get("control", [])
    }
    table.append(
        {
            "clause": "control register (0, 0, 0) at every tick",
            "pass": bool(control) and all(v["zero_every_tick"] for v in control.values()),
            "numbers": control,
        }
    )
    # 3. In every two-body world the two registers are equal and opposite at every tick.
    opposite = {
        r["model"]: {"equal_opposite_every_tick": r["equal_opposite"], "final": r["final_registers"]}
        for r in results
        if not r["control"]
    }
    table.append(
        {
            "clause": "registers equal and opposite at every tick",
            "pass": bool(opposite) and all(v["equal_opposite_every_tick"] for v in opposite.values()),
            "numbers": opposite,
        }
    )
    # 4. The log-log exponent of F(r) over the five axis r is -2.0 +- 0.2.
    fits = {}
    for case, rs in axis.items():
        if not rs:
            continue
        points = [(r["manhattan"], abs(force(r, 1)[0])) for r in rs]
        fits[case] = {"points": points, **fit(points)}
    table.append(
        {
            "clause": "log-log exponent of F(r) over the axis r is -2.0 +- 0.2",
            "pass": bool(fits)
            and all(
                f["exponent"] is not None and BAND[0] <= f["exponent"] <= BAND[1] for f in fits.values()
            ),
            "numbers": fits,
        }
    )
    # 5. Like charges pushed apart (A -X, B +X), opposite together, the same magnitudes.
    signs = {}
    for rs in axis.values():
        for r in rs:
            fa, fb = force(r, 0), force(r, 1)
            apart = fa[0] < 0 < fb[0]
            together = fb[0] < 0 < fa[0]
            signs[r["model"]] = {
                "like": r["like"],
                "F": [fa, fb],
                "pass": apart if r["like"] else together,
            }
    magnitudes = {}
    for pp in axis["pp"]:
        pe = next((r for r in axis["pe"] if r["manhattan"] == pp["manhattan"]), None)
        if pe is None:
            continue
        magnitudes[pp["manhattan"]] = {
            "pp_series_is_minus_pe_series": pp["register_series"]
            == {k: [[-c for c in v] for v in series] for k, series in pe["register_series"].items()},
            "F_pp": force(pp, 1),
            "F_pe": force(pe, 1),
        }
    table.append(
        {
            "clause": "like charges apart, opposite together, the same magnitudes",
            "pass": bool(signs)
            and all(v["pass"] for v in signs.values())
            and bool(magnitudes)
            and all(v["pp_series_is_minus_pe_series"] for v in magnitudes.values()),
            "numbers": {"signs": signs, "magnitudes": magnitudes},
        }
    )
    # 6. The diagonal series against the axis fit at the same Euclidean distance:
    # the ratio per point and the direction, reported, no pass/fail.
    diagonal = {}
    reference = fits.get("pp")
    for r in sorted(by_case.get("diagonal", []), key=lambda r: r["manhattan"]):
        fb = force(r, 1)
        magnitude = math.sqrt(sum(c * c for c in fb))
        predicted = None
        if reference and reference["exponent"] is not None:
            predicted = math.exp(
                reference["intercept"] + reference["exponent"] * math.log(r["euclidean"])
            )
        diagonal[r["model"]] = {
            "offset": r["offset"],
            "euclidean": r["euclidean"],
            "F_b": fb,
            "F_a": force(r, 0),
            "magnitude": magnitude,
            "axis_fit_at_same_distance": predicted,
            "ratio": (magnitude / predicted) if predicted else None,
            "along_diagonal": r["steady"][1]["sum"][0] == r["steady"][1]["sum"][1]
            and r["steady"][1]["sum"][2] == 0,
            "sum_window": r["steady"][1]["sum"],
        }
    table.append(
        {
            "clause": "diagonal series against the axis fit (reported, no pass/fail)",
            "pass": None,
            "numbers": diagonal,
        }
    )
    return table


def print_run(r):
    print(
        f"== {r['model']}  offset={r['offset']} manhattan={r['manhattan']} euclid={r['euclidean']:.2f}"
        f" shape={r['shape']} ticks={r['ticks']} status={r['status']} elapsed={r['elapsed_seconds']:.0f}s"
    )
    print(f"   source {r['source_sha256']}  init {r['initialization_sha256']}")
    for index, body in enumerate(r["bodies"]):
        s = r["steady"][index]
        print(
            f"   body {index} {body['family']} charge {body['charge']} at {body['position']} table {body['table']}:"
            f" first push tick {r['first_push'][index]}, final register {r['final_registers'][index]},"
            f" F (last {s['window']}) {[round(c, 3) for c in s['mean']]}"
            + (
                f", previous window {[round(c, 3) for c in s['previous_mean']]}"
                if s["previous_mean"]
                else ""
            )
        )
    print(
        f"   balanced {r['all_balanced']} conserved {r['conserved_at_every_completed_tick']}"
        f" positions fixed {r['positions_fixed']} equal+opposite {r['equal_opposite']} control zero {r['control_zero']}"
        f" bodies' momentum line zero {r['bodies_momentum_zero']} momentum ledger zero {r['momentum_line_zero']}"
    )
    print(
        "   tick  "
        + "  ".join(f"{'reg_' + str(i):18s} {'push_' + str(i):15s}" for i in range(len(r["bodies"])))
        + " light_current"
    )
    for row in r["rows"]:
        cells = "  ".join(
            f"{str(row['registers'][i]):18s} {str(row['pushes'][i]):15s}"
            for i in range(len(r["bodies"]))
        )
        print(f"   {row['tick']:4d}  {cells} {row['light_current']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    results = [analyze(run) for run in args.runs]
    for r in results:
        print_run(r)
    table = clauses(results)
    print("\n== Criterion of A5s, clause by clause")
    for entry in table:
        verdict = "----" if entry["pass"] is None else ("PASS" if entry["pass"] else "FAIL")
        print(f"   {verdict}  {entry['clause']}")
        print("         " + json.dumps(entry["numbers"], default=str)[:1500])
    if args.out:
        args.out.write_text(
            json.dumps({"runs": results, "clauses": table}, indent=1) + "\n", encoding="utf-8"
        )
    if args.record:
        record = {
            "runs": [{k: r[k] for k in r if k not in ("rows", "run")} for r in results],
            "clauses": table,
        }
        args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
