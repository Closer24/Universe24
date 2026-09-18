"""Read the runs of A5s repeated under the law of the bit (docs/EXPERIMENTS.md).

From `run.json` of every world of the series (a Recorder in the sense of
Highlights 3.29): the books per bit at every completed tick (`audit`), the two
bodies' momentum lines per tick (`momentum`, thing id to vector: the bodies
are things 2 and 3, after the one unseeded type), the push per interval on
each (the increments), the bodies' positions per tick (both at rest), the
shadows' total and the escapes, the runner's standing-set report; and the
momentum in flight on the shadows, the ledger's current momentum less the
things' (the world's momentum line is its initial, zero, at every tick when
the books close, so what the things gained the shadows carry). Every world is
closed (the model owner, 2026-09-18: only closed worlds are tested). The push
on B along the line from A to B per interval, averaged over windows of twenty
intervals, its settled value (the mean over ticks 101 to 120, with its
standard error and the settling tick, the first from which every later
window of twenty stays within 10 % of the last), gives the scaling with d
over the axis worlds (log-log least squares over d = 4, 6, 8, 12) and the
anisotropy (the (110) and (111) worlds against the axis fit at the same
Euclidean distance); the three pairs of contents at d = 8 give the product
law (the settled push on each body against the product of the whole charges,
and against each body's own and the other's charge).

With `--replay NAME` (or `--replay-all`) a world is also replayed through the
Simulation API and the momentum in flight is read per tick from the engine's
arrays and Nodes (every shadow's `momentum`, on its way and parked; with
`--inventory` the inventory view is summed as well and checked equal), and
the bodies' momenta plus the momentum in flight plus the escaped are checked
to sum to zero at every tick (the runner's ledger line of the momentum field
does not sum the momentum carried on rays, so the world's zero is read here);
the replay's momentum lines are checked against the record's.

Run:  PYTHONPATH=src python examples/nature/a5s_law/analyze.py RUNS_DIR [--closed CLOSED_RUNS_DIR] [--record record.json] [--tables tables.md] [--replay pq_d8_closed]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from make_worlds import AXIS_DISTANCES, OFF_AXIS, PAIRS, cases  # noqa: E402

THING_A = 2
THING_B = 3
CLOSED_WINDOWS = tuple((a, a + 19) for a in range(1, 120, 20))


def load_record(runs, name):
    path = Path(runs) / name / "run" / "run.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def unit(vector):
    norm = math.sqrt(sum(c * c for c in vector))
    return tuple(c / norm for c in vector)


def read_world(run, offset, amount_a, amount_b):
    line = unit(offset)
    rows = []
    previous = {THING_A: [0, 0, 0], THING_B: [0, 0, 0]}
    for tick, (momenta, entry) in enumerate(zip(run["momentum"], run["audit"], strict=True), start=1):
        row = {"tick": tick}
        for thing, key in ((THING_A, "a"), (THING_B, "b")):
            vector = list(momenta.get(str(thing), [0, 0, 0]))
            push = [vector[k] - previous[thing][k] for k in range(3)]
            previous[thing] = vector
            row[f"p_{key}"] = vector
            row[f"push_{key}"] = push
            row[f"push_{key}_line"] = sum(push[k] * line[k] for k in range(3))
            row[f"p_{key}_line"] = sum(vector[k] * line[k] for k in range(3))
        things = [row["p_a"][k] + row["p_b"][k] for k in range(3)]
        ledger = entry["fields"]["momentum"]
        row["things_sum"] = things
        # The runner's ledger line of the momentum field does not sum the
        # momentum carried on rays: the momentum in flight is read by the
        # replay (`--replay`), and the world's zero there.
        row["ledger_momentum"] = {"current": list(ledger["current"]), "returned": list(ledger["returned"]), "escaped": list(ledger["escaped"])}
        row["momentum_escaped"] = list(ledger["escaped"])
        row["balanced"] = bool(entry["balanced"])
        row["real_balanced"] = all(x["balanced"] for x in entry["real"].values())
        row["shadow_balanced"] = all(x["balanced"] for x in entry["shadow"].values())
        row["real_conserved"] = bool(entry.get("real_conserved", False))
        row["bodies_line"] = list(entry["bodies"]["momentum"])
        rows.append(row)
    windows = {}
    for a, b in CLOSED_WINDOWS:
        sel = [r for r in rows if a <= r["tick"] <= b]
        if not sel:
            continue
        windows[f"{a}-{b}"] = {
            "push_b": sum(r["push_b_line"] for r in sel) / len(sel),
            "push_a": sum(r["push_a_line"] for r in sel) / len(sel),
        }
    positions = run["external_bodies"]
    last = rows[-20:]
    before = rows[-40:-20]
    return {
        "settling_tick_b": settling_tick(rows, "push_b_line"),
        "settling_tick_a": settling_tick(rows, "push_a_line"),
        "standing_field": {k: run.get(k) for k in ("standing_field", "standing_field_iterations", "standing_field_period", "standing_field_residual", "standing_field_ticks", "standing_field_fallback", "standing_field_max_iterations")} if "standing_field" in run else None,
        "settled_push_b": sum(r["push_b_line"] for r in last) / len(last),
        "settled_push_b_error": standard_error([r["push_b_line"] for r in last]),
        "settled_push_b_before": sum(r["push_b_line"] for r in before) / len(before) if before else None,
        "settled_push_a": sum(r["push_a_line"] for r in last) / len(last),
        "settled_push_a_before": sum(r["push_a_line"] for r in before) / len(before) if before else None,
        "p_b_line_at_end": rows[-1]["p_b_line"],
        "p_a_line_at_end": rows[-1]["p_a_line"],
        "bodies_sum_at_end": rows[-1]["things_sum"],
        "in_flight_at_end": None,
        "world_zero_every_tick": None,
        "offset": list(offset),
        "distance": math.sqrt(sum(c * c for c in offset)),
        "amount_a": amount_a,
        "amount_b": amount_b,
        "charge_a": 3 * amount_a,
        "charge_b": 3 * amount_b,
        "status": run["status"],
        "completed_ticks": run["completed_ticks"],
        "source_sha256": run["source_sha256"],
        "initialization_sha256": run["initialization_sha256"],
        "elapsed_seconds": run["elapsed_seconds"],
        "shadows_initial": run["shadow_content"][0],
        "shadows_final": run["shadow_content"][-1],
        "escaped": run["escaped_totals"]["proton"][0],
        "bodies_at_rest": all(
            p[1:] == body["positions"][0][1:] for body in positions for p in body["positions"]
        ),
        "ticks": rows,
        "windows": windows,
        "first_push_tick_b": next((r["tick"] for r in rows if any(r["push_b"])), None),
        "max_push_b": max(r["push_b_line"] for r in rows),
        "min_push_b": min(r["push_b_line"] for r in rows),
        "sign_changes_b": sum(
            1 for x, y in zip(rows, rows[1:], strict=False) if x["push_b_line"] * y["push_b_line"] < 0
        ),
        "books_every_tick": all(r["balanced"] and r["real_balanced"] and r["shadow_balanced"] and r["real_conserved"] for r in rows),
        "bodies_line_matches": all(r["bodies_line"] == r["things_sum"] for r in rows),
        "escaped_momentum_at_end": rows[-1]["momentum_escaped"],
        "ledger_momentum_at_end": rows[-1]["ledger_momentum"],
    }


def standard_error(values):
    """The standard error of the mean of `values` (the sample deviation over root n)."""
    n = len(values)
    if n < 2:
        return None
    mean = sum(values) / n
    return math.sqrt(sum((v - mean) ** 2 for v in values) / (n - 1) / n)


def settling_tick(rows, key, window=20, tolerance=0.10):
    """The first tick from which every mean of `key` over a window of twenty
    stays within 10 % of the mean over the last window (the settled value);
    None when the two last windows disagree."""
    values = [row[key] for row in rows]
    n = len(values)
    if n < 2 * window:
        return None
    final = sum(values[n - window :]) / window
    scale = abs(final) if final else 1.0
    ok = [abs(sum(values[s : s + window]) / window - final) <= tolerance * scale for s in range(0, n - window + 1)]
    t = n - window
    while t > 0 and ok[t - 1]:
        t -= 1
    return t + 1 if t <= n - 2 * window else None


def fit_slope(points):
    xs = [math.log(r) for r, y in points if y]
    ys = [math.log(abs(y)) for r, y in points if y]
    if len(xs) < 2:
        return None
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    slope = sxy / sxx
    intercept = my - slope * mx
    residual = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys, strict=True))
    error = math.sqrt(residual / (n - 2) / sxx) if n > 2 else None
    return {"slope": slope, "intercept": intercept, "error": error, "points": n}


def fit_value(fit, r):
    return math.exp(fit["intercept"] + fit["slope"] * math.log(r)) if fit else None


def shadow_momentum(world, index=0):
    """The momentum in flight on the shadows after a tick: the layer's arrays
    (arrivals, departures, parked ninths), the whole rays beside them and the
    engine's Nodes' shadows; equal to the inventory view's sum (checked on a
    small closed world, and on `pq_d8_closed` with `--inventory`)."""
    import numpy as np

    spatial = world._spatial
    family = spatial.dense.families[index]
    axes = tuple(range(family.arr_mom.ndim - 1))
    total = (
        family.arr_mom.astype(np.int64).sum(axis=axes)
        + family.fly_mom.astype(np.int64).sum(axis=axes)
        + family.reg_mom.astype(np.int64).sum(axis=tuple(range(family.reg_mom.ndim - 1)))
    )
    total = [int(c) for c in total]
    for rays in family.overflow.values():
        for ray in rays:
            if ray.momentum is not None:
                for k in range(3):
                    total[k] += ray.momentum[k]
    for node in spatial.nodes.values():
        if not node.rays:
            continue
        for ray in node.rays[index]:
            if ray.detector == 0 and ray.momentum is not None:
                for k in range(3):
                    total[k] += ray.momentum[k]
    return total


def replay_in_flight(document, ticks, log=print, inventory=False):
    """The momentum in flight on the shadows per tick, read from the engine's
    arrays and Nodes (and, with `inventory`, from the inventory view as well,
    the two checked equal), beside the bodies' momenta and the ledger's lines."""
    from event_universe import Simulation
    from event_universe.initialization import parse_initial_state

    rows = []
    with Simulation(parse_initial_state(document)) as world:
        for tick in range(1, ticks + 1):
            world.step()
            in_flight = shadow_momentum(world)
            if inventory:
                from_inventory = [0, 0, 0]
                for node in world.inventory_view().nodes:
                    for rays in list(node.rays) + list(node.parked):
                        for ray in rays:
                            if ray.detector == 0 and ray.momentum is not None:
                                for k in range(3):
                                    from_inventory[k] += ray.momentum[k]
                if from_inventory != in_flight:
                    raise AssertionError(f"tick {tick}: the arrays read {in_flight}, the inventory {from_inventory}")
            bodies = [list(b["momentum"]) for b in world.external_bodies()]
            ledger = world.audit()
            rows.append(
                {
                    "tick": tick,
                    "bodies": bodies,
                    "in_flight_inventory": in_flight,
                    "sum": [bodies[0][k] + bodies[1][k] + in_flight[k] for k in range(3)],
                    "ledger_current": list(ledger["fields"]["momentum"]["current"]),
                    "ledger_escaped": list(ledger["fields"]["momentum"]["escaped"]),
                }
            )
            log(f"  tick {tick} bodies {bodies} in flight {in_flight} escaped {rows[-1]['ledger_escaped']}")
    return rows


def replay_job(job):
    """One replay (a worker of the pool): the world's name, its file, its ticks."""
    name, world_path, ticks, inventory = job
    document = json.loads(Path(world_path).read_text(encoding="utf-8"))
    return name, replay_in_flight(document, ticks, log=lambda _: None, inventory=inventory)


def fmt(value, digits=1):
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def tables(record):
    w = record["worlds"]
    lines = ["### The books per bit, the rest and the momentum in flight\n"]
    lines.append("| World | r | Contents A, B | Ticks | Books per bit balanced | Bodies + shadows in flight = 0 every tick (replay) | Bodies at rest | Shadows at start / at the end | Escaped | First push on B | Runner s |")
    lines.append("| --- | ---: | --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: |")
    for name, r in w.items():
        lines.append(
            f"| `{name}` | {r['distance']:.2f} | 2^{int(math.log2(r['amount_a']))}, 2^{int(math.log2(r['amount_b']))} | {r['completed_ticks']} | "
            f"{'every tick' if r['books_every_tick'] else 'NO'} | {'every tick' if r['world_zero_every_tick'] else ('NO' if r['world_zero_every_tick'] is False else 'not replayed')} | {'yes' if r['bodies_at_rest'] else 'NO'} | "
            f"{r['shadows_initial']} / {r['shadows_final']} | {r['escaped']} | {fmt(r['first_push_tick_b'])} | {fmt(r['elapsed_seconds'])} |"
        )
    closed = w
    if closed:
        lines.append("\n### The push per interval on B along the line from A, per window of twenty, the settled push and the standing-set search (every world closed: `boundary` periodic, 120 ticks, `standing_field` on)\n")
        lines.append("| World | r | Contents A, B | Books per bit | Things + in flight + escaped = 0 | At rest | Standing set found | Iterations | Period | Residual (cells, amount) | Push on B, ticks 1-20 | 21-40 | 41-60 | 61-80 | 81-100 | 101-120 (+- its standard error) | Settled from tick | Push on A, 101-120 | Sign changes | p_B at 120 | p_A at 120 | p_A + p_B at 120 | In flight on the shadows at 120 (replay) | Runner s |")
        lines.append("| --- | ---: | --- | --- | --- | --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |")
        for name, r in closed.items():
            sf = r.get("standing_field") or {}
            win = r["windows"]
            cells = " | ".join(f"{win[k]['push_b']:.0f}" if k in win else "-" for k in ("1-20", "21-40", "41-60", "61-80", "81-100", "101-120"))
            res = sf.get("standing_field_residual") or {}
            lines.append(
                f"| `{name}` | {r['distance']:.2f} | 2^{int(math.log2(r['amount_a']))}, 2^{int(math.log2(r['amount_b']))} | {'every tick' if r['books_every_tick'] else 'NO'} | {'every tick' if r['world_zero_every_tick'] else ('NO' if r['world_zero_every_tick'] is False else 'not replayed')} | {'yes' if r['bodies_at_rest'] else 'NO'} | "
                f"{sf.get('standing_field')} | {fmt(sf.get('standing_field_iterations'))} | {fmt(sf.get('standing_field_period'))} | {res.get('cells', '-')}, {res.get('amount', '-')} | {cells} +- {r['settled_push_b_error']:.0f} | {fmt(r['settling_tick_b'])} | {r['settled_push_a']:.0f} | {r['sign_changes_b']} | "
                f"{r['p_b_line_at_end']:.0f} | {r['p_a_line_at_end']:.0f} | {r['bodies_sum_at_end']} | {r['in_flight_at_end']} | {fmt(r['elapsed_seconds'])} |"
            )
        lines.append("\n### The scaling with d (the axis worlds, like contents 2^28), the anisotropy and the product law\n")
        lines.append("| Quantity (the axis worlds) | Slope (log-log over d = 4, 6, 8, 12) | Standard error | Fit at d = 8 | Fit at d = 11.31 | Fit at d = 13.86 |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
        for quantity, fit in record.get("closed_fits", {}).items():
            if fit:
                lines.append(f"| {quantity} | {fit['slope']:.2f} | {fmt(fit['error'], 2)} | {fit_value(fit, 8):.0f} | {fit_value(fit, math.sqrt(128)):.0f} | {fit_value(fit, math.sqrt(192)):.0f} |")
        if record.get("closed_anisotropy"):
            lines.append("\n| World | r | Quantity | Measured | Axis fit | Ratio |")
            lines.append("| --- | ---: | --- | ---: | ---: | ---: |")
            for name, entry in record["closed_anisotropy"].items():
                for quantity, a in entry.items():
                    lines.append(f"| `{name}` | {a['r']:.2f} | {quantity} | {a['measured']:.0f} | {fmt(a['fit'], 0)} | {fmt(a['ratio'], 3)} |")
        if record.get("closed_product_law"):
            lines.append("\n| World (d = 8) | q_A, q_B | q_A q_B / (3 2^28)^2 | Settled push on B, 101-120 | Ratio to `pp_d8_closed` | 81-100 | Settled push on A, 101-120 | Ratio | Push on A + push on B | p_B at 120 | p_A at 120 |")
            lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
            for name, pr in record["closed_product_law"].items():
                lines.append(
                    f"| `{name}` | 3 x 2^{int(math.log2(pr['amount_a']))}, 3 x 2^{int(math.log2(pr['amount_b']))} | {pr['charge_product_ratio']:.4f} | {pr['push_b']:.0f} | {fmt(pr['push_b_ratio'], 3)} | "
                    f"{fmt(pr['push_b_before'], 0)} | {pr['push_a']:.0f} | {fmt(pr['push_a_ratio'], 3)} | {pr['sum']:.0f} | {pr['p_b_120']:.0f} | {pr['p_a_120']:.0f} |"
                )
    for rp in (record.get("replays") or {}).values():
        n = len(rp["rows"])
        shown = (1, 2, 3, 4, 5, 8, 10, 15, 20, 25, 30, 35, 40) if n <= 40 else (1, 2, 3, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120)
        lines.append(f"\n### The recoil through the field: `{rp['world']}` replayed, the momentum in flight from the inventory\n")
        lines.append("| Tick | p_A | p_B | In flight on the shadows | Ledger current | Escaped | Sum |")
        lines.append("| ---: | --- | --- | --- | --- | --- | --- |")
        for row in rp["rows"]:
            if row["tick"] in shown:
                total = [row["bodies"][0][k] + row["bodies"][1][k] + row["in_flight_inventory"][k] + row["ledger_escaped"][k] for k in range(3)]
                lines.append(f"| {row['tick']} | {row['bodies'][0]} | {row['bodies'][1]} | {row['in_flight_inventory']} | {row['ledger_current']} | {row['ledger_escaped']} | {total} |")
        lines.append(f"\nThe replay's momentum lines equal the record's: {rp['matches_record']}; the two things' momenta plus the momentum in flight on the shadows plus the escaped sum to zero at every tick: {rp.get('sum_zero_every_tick')}.\n")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("runs", type=Path)
    parser.add_argument("--worlds", type=Path, default=HERE)
    parser.add_argument("--record", type=Path, default=HERE / "record.json")
    parser.add_argument("--tables", type=Path, default=HERE / "tables.md")
    parser.add_argument("--replay", action="append", default=[], help="a world to replay in-process for the momentum in flight (repeatable)")
    parser.add_argument("--replay-all", action="store_true", help="replay every world of the series")
    parser.add_argument("--replay-jobs", type=int, default=1, help="replays at once (processes)")
    parser.add_argument("--inventory", action="store_true", help="read the momentum in flight from the inventory view as well and check it equal (slow)")
    parser.add_argument("--closed", type=Path, default=None, help="the runs directory (kept for the earlier form of the command; RUNS_DIR is read when absent)")
    args = parser.parse_args(argv)
    documents = dict(cases())
    record = {
        "experiment": "A5s repeated under the law of the bit (2026-09-18)",
        "worlds": {},
        "replays": {},
        "closed_fits": {},
        "closed_anisotropy": {},
        "closed_product_law": {},
    }
    if args.record.exists():
        # Keep an earlier analysis's replays (the engine is deterministic).
        earlier = json.loads(args.record.read_text(encoding="utf-8"))
        record["replays"] = earlier.get("replays") or {}
        for rp in record["replays"].values():
            # The checks are re-read from the rows (the ledger's `current` is the
            # shadows' momentum; the bodies' is the `returned` line).
            rp["sum_zero_every_tick"] = all(
                all(row["bodies"][0][k] + row["bodies"][1][k] + row["in_flight_inventory"][k] + row["ledger_escaped"][k] == 0 for k in range(3))
                for row in rp["rows"]
            )
    for name, document in documents.items():
        run = load_record(args.closed if args.closed else args.runs, name)
        if run is None:
            print(f"{name}: no record")
            continue
        a, b = document["external_bodies"]
        offset = tuple(b["position"][k] - a["position"][k] for k in range(3))
        record["worlds"][name] = read_world(run, offset, a["amount"], b["amount"])
        r = record["worlds"][name]
        print(f"{name}: {r['status']} {r['completed_ticks']} ticks, books {r['books_every_tick']}, at rest {r['bodies_at_rest']}, settled push on B {r['settled_push_b']:.0f}")
    closed_axis = [(d, record["worlds"].get(f"pp_d{d}_closed")) for d in AXIS_DISTANCES]
    closed_axis = [(d, r) for d, r in closed_axis if r]
    closed_quantities = {
        "settled push on B, ticks 101-120": lambda r: r["settled_push_b"],
        "push on B, ticks 81-100": lambda r: r["settled_push_b_before"],
        "settled push on A, ticks 101-120": lambda r: r["settled_push_a"],
        "p_B at 120": lambda r: r["p_b_line_at_end"],
    }
    for quantity, read in closed_quantities.items():
        record["closed_fits"][quantity] = fit_slope([(d, read(r)) for d, r in closed_axis]) if closed_axis else None
    for direction in OFF_AXIS:
        name = f"pp_d8_{direction}_closed"
        if name not in record["worlds"]:
            continue
        r = record["worlds"][name]
        record["closed_anisotropy"][name] = {}
        for quantity, read in closed_quantities.items():
            fit = record["closed_fits"][quantity]
            value = fit_value(fit, r["distance"])
            measured = read(r)
            record["closed_anisotropy"][name][quantity] = {"r": r["distance"], "measured": measured, "fit": value, "ratio": measured / value if value else None}
    base = record["worlds"].get("pp_d8_closed")
    for name in ("pp_d8_closed", *(f"{tag}_d8_closed" for tag in PAIRS)):
        r = record["worlds"].get(name)
        if r is None or base is None:
            continue
        record["closed_product_law"][name] = {
            "amount_a": r["amount_a"],
            "amount_b": r["amount_b"],
            "charge_product_ratio": (r["charge_a"] * r["charge_b"]) / (base["charge_a"] * base["charge_b"]),
            "push_b": r["settled_push_b"],
            "push_b_ratio": r["settled_push_b"] / base["settled_push_b"] if base["settled_push_b"] else None,
            "push_a": r["settled_push_a"],
            "push_a_ratio": r["settled_push_a"] / base["settled_push_a"] if base["settled_push_a"] else None,
            "push_b_before": r["settled_push_b_before"],
            "push_a_before": r["settled_push_a_before"] if "settled_push_a_before" in r else None,
            "sum": r["settled_push_a"] + r["settled_push_b"],
            "p_b_120": r["p_b_line_at_end"],
            "p_a_120": r["p_a_line_at_end"],
        }
    names = [n for n in (list(record["worlds"]) if args.replay_all else args.replay) if n in record["worlds"] and n not in record["replays"]]
    jobs = [(name, str(args.worlds / f"{name}.json"), record["worlds"][name]["completed_ticks"], args.inventory) for name in names]
    if jobs:
        print(f"replaying {[j[0] for j in jobs]} in-process for the momentum in flight, {args.replay_jobs} at once")
    if args.replay_jobs > 1 and len(jobs) > 1:
        import multiprocessing

        with multiprocessing.get_context("spawn").Pool(args.replay_jobs) as pool:
            results = dict(pool.imap_unordered(replay_job, jobs))
    else:
        results = dict(replay_job(job) for job in jobs)
    for name in names:
        rows = results[name]
        recorded = record["worlds"][name]["ticks"]
        record["replays"][name] = {
            "world": name,
            "rows": rows,
            "matches_record": all(row["bodies"] == [rec["p_a"], rec["p_b"]] for row, rec in zip(rows, recorded, strict=True)),
            "sum_zero_every_tick": all(
                all(row["bodies"][0][k] + row["bodies"][1][k] + row["in_flight_inventory"][k] + row["ledger_escaped"][k] == 0 for k in range(3))
                for row in rows
            ),
        }
    for name, rp in record["replays"].items():
        if name in record["worlds"]:
            record["worlds"][name]["in_flight_at_end"] = rp["rows"][-1]["in_flight_inventory"]
            record["worlds"][name]["world_zero_every_tick"] = rp["sum_zero_every_tick"]
    args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    text = tables(record)
    args.tables.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
