"""Read the runs of E11 repeated under the law of the bit (docs/EXPERIMENTS.md).

Two readings, both Recorders in the sense of Highlights 3.29 (they read the
record a run left, or replay its world through the Simulation API and check
the replay against the record; they never change the engine):

1. From `run.json` of every world of the series (the runner's record): the
   books per bit at every completed tick (`audit`: the world line, the real
   line and the shadow line balanced, `real_conserved`), the shadows' total
   per tick, the escapes, and for the probe worlds the test thing's momentum
   line per tick (the runner's `momentum`, thing id to vector; the test thing
   is type 2 and the body is thing 3), whose increments are the pushed amount
   per interval, and the body's momentum line, the recoil that came home
   through the field.

2. In-process, for `pulse.json` and `standing.json` (no test thing; the dense
   layer holds every shadow and publishes no per-Node event, so the shells are
   read from the engine): the world is replayed for its ticks and after every
   tick the inventory view gives, per Node, the body's shadows on their way
   (outgoing, returning), their signed radial flux J_r = sum over shadows of
   +-amount x (heading . r) / |r| (the sign of a returning share negative,
   what a thing reads) and the parked shares; from these, per L1 shell
   (|dx| + |dy| + |dz| = k) and per Euclidean shell (round |r| = k): the
   Nodes, the content, the content per Node, J_r per shell and per Node; the
   content on the axes, on the coordinate planes off the axes, and off the
   planes (all three coordinates nonzero), as fractions of the content on the
   board; and the content and J at the nine read Nodes of the probe worlds. The
   replay's ledger per tick is checked equal to the record's `audit`, so the
   reading belongs to the fingerprinted run.

The front's arrival per direction (the pulse): at the read Nodes (r, 0, 0),
(m, m, 0), (m, m, m) for the three radii of each direction, the first tick at
which the Node's content reaches 1 % of its peak over the run, and the tick of
the peak; DERIVATIONS.md section 27 (iii) predicts the peak at sqrt 3 r.

The 1/r^2 fit (the probes): per direction, the pushed amount at the three
radii is the test thing's momentum along the radial direction, cumulative at
tick 40 (the momentum line less the thing's own amount x heading; for a wave
train that passes, the time-integrated push is the content that crossed the
shell over its area, Gauss for a pulse) and its mean per interval over ticks
2 to 21 (the first twenty read intervals), and the log-log least-squares
slope over the three radii; the anisotropy is the axis fit's value over the
(111) fit's value at r = 8 (and at r = 12), DERIVATIONS.md section 27 (v)
predicting 1 - 1.25 omega^2 for a clocked source and no far field at all for
a clockless one.

Run:  PYTHONPATH=src python examples/nature/e11_law/analyze.py RUNS_DIR [--worlds DIR] [--record record.json] [--tables tables.md] [--no-replay]
      (RUNS_DIR holds <name>/run/run.json for every world written by make_worlds.py)
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from make_worlds import HALF, PROBES, PULSE_HALF, TICKS, cases  # noqa: E402

PORTS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
PROBE_THING = 2
BODY_THING = 3
EARLY = (2, 21)
FRONT_THRESHOLD = 0.01


def load_record(runs, name):
    path = Path(runs) / name / "run" / "run.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def books(record):
    """The books per bit at every completed tick, from the record's audit."""
    rows = []
    for entry in record["audit"]:
        rows.append(
            {
                "tick": entry["tick"],
                "balanced": bool(entry["balanced"]),
                "real_balanced": all(line["balanced"] for line in entry["real"].values()),
                "shadow_balanced": all(line["balanced"] for line in entry["shadow"].values()),
                "real_conserved": bool(entry.get("real_conserved", False)),
                "momentum_current": list(entry["fields"]["momentum"]["current"]),
                "momentum_escaped": list(entry["fields"]["momentum"]["escaped"]),
                "bodies_momentum": list(entry["bodies"]["momentum"]),
            }
        )
    return rows


def unit(vector):
    norm = math.sqrt(sum(c * c for c in vector))
    return tuple(c / norm for c in vector)


def probe_reading(record, offset, heading):
    """The test thing's momentum line per tick, its push per interval (the
    increments of the line less its own amount x heading), the cumulative push
    and its radial component."""
    radial = unit(offset)
    own = None
    rows = []
    previous = [0, 0, 0]
    for tick, line in enumerate(record["momentum"], start=1):
        vector = list(line.get(str(PROBE_THING), [0, 0, 0]))
        body_vector = list(line.get(str(BODY_THING), [0, 0, 0]))
        if own is None:
            # The thing's own amount x heading, read from the first tick (no
            # push before the thing stands at its Node).
            own = [c * 1 for c in heading]
        carried = [vector[k] - own[k] for k in range(3)]
        push = [carried[k] - previous[k] for k in range(3)]
        previous = carried
        rows.append(
            {
                "tick": tick,
                "momentum": vector,
                "carried": carried,
                "push": push,
                "push_radial": sum(push[k] * radial[k] for k in range(3)),
                "cumulative_radial": sum(carried[k] * radial[k] for k in range(3)),
                "body_momentum": body_vector,
                "computation": record["computation_per_tick"][tick - 1],
            }
        )
    early = [row["push_radial"] for row in rows if EARLY[0] <= row["tick"] <= EARLY[1]]
    return {
        "offset": list(offset),
        "heading": list(heading),
        "radius": math.sqrt(sum(c * c for c in offset)),
        "ticks": rows,
        "cumulative_radial_at_end": rows[-1]["cumulative_radial"],
        "cumulative_radial_at_30": next(r["cumulative_radial"] for r in rows if r["tick"] == 30),
        "early_mean_radial": sum(early) / len(early) if early else 0.0,
        "window_means": {
            f"{a}-{b}": sum(r["push_radial"] for r in rows if a <= r["tick"] <= b) / (b - a + 1)
            for a, b in ((2, 11), (12, 21), (22, 31), (32, 40))
        },
        "body_momentum_at_end": rows[-1]["body_momentum"],
        "waited_intervals": sum(1 for r in rows if r["computation"] == 0 and r["tick"] >= 2),
    }


def fit_slope(points):
    """Log-log least squares of |y| against r over (r, y) with y != 0."""
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


# ----------------------------------------------------------- the replay


def read_board(world, index, shape):
    """The body's shadows per Node and Port heading after a tick: outgoing and
    returning shares on their way, and the parked shares in whole quanta. The
    dense region's arrays (arrivals and departures per Node, owner, sign, Port
    and layer; the parked ninths per Node, owner, sign and Port) hold every
    plain outgoing share, and the engine's Nodes hold the rest (a returning
    share, a share carrying momentum, the body's own Node); the reading equals
    the inventory view's, checked on a small world before the run."""
    spatial = world._spatial
    family = spatial.dense.families[index]
    definition = world.initial.spatial_fields[index]
    ports = [PORTS.index(tuple(h)) for h in definition.headings]
    out = np.ascontiguousarray(
        np.transpose(family.arr_amt.sum(axis=(3, 4, 6)) + family.fly_amt.sum(axis=(3, 4, 6)), (3, 0, 1, 2))
    ).astype(np.int64)
    ret = np.zeros((6, *shape), dtype=np.int64)
    park_ninths = family.reg.sum(axis=(3, 4, 5)).astype(np.int64)
    for position, rays in family.overflow.items():
        for ray in rays:
            out[(ports[ray.heading], *position)] += ray.amount
    for position, node in spatial.nodes.items():
        if not node.rays:
            continue
        for ray in node.rays[index]:
            if ray.detector != 0:
                continue
            if ray.parked:
                park_ninths[position] += ray.amount
                continue
            (out if ray.outbound else ret)[(ports[ray.heading], *position)] += ray.amount
    return out, ret, park_ninths // family.total


def replay(document, ticks, read_nodes, log=print):
    """The world through the Simulation API: per tick the shells and the
    fractions, the content and J at the read Nodes, and the ledger."""
    from event_universe import Simulation
    from event_universe.initialization import parse_initial_state

    shape = tuple(int(n) for n in document["shape"])
    centre = tuple(int(c) for c in document["external_bodies"][0]["position"])
    grid = np.indices(shape, dtype=np.int64) - np.array(centre, dtype=np.int64)[:, None, None, None]
    l1 = np.abs(grid).sum(axis=0)
    radius = np.sqrt((grid * grid).sum(axis=0).astype(float))
    euclid = np.rint(radius).astype(np.int64)
    nonzero = (grid != 0).sum(axis=0)
    unit_r = np.where(radius > 0, grid / np.maximum(radius, 1e-9), 0.0)
    kmax = max(shape) // 2
    headings = np.array(PORTS, dtype=np.int64)
    per_tick = []
    ledgers = []
    with Simulation(parse_initial_state(document)) as world:
        index = 0
        for tick in range(1, ticks + 1):
            started = time.perf_counter()
            world.step()
            stepped = time.perf_counter() - started
            out, ret, park = read_board(world, index, shape)
            signed = out - ret
            jvec = np.einsum("pxyz,pk->kxyz", signed, headings)
            jr = (jvec * unit_r).sum(axis=0)
            out_total, ret_total, park_total = out.sum(axis=0), ret.sum(axis=0), park
            total = int(out_total.sum() + ret_total.sum() + park_total.sum())
            row = {"tick": tick, "seconds": round(stepped, 3), "on_board": total}
            for kind, level in (("l1", l1), ("euclid", euclid)):
                shells = []
                for k in range(0, kmax + 1):
                    mask = level == k
                    n = int(mask.sum())
                    if n == 0:
                        continue
                    content = int(out_total[mask].sum() + ret_total[mask].sum() + park_total[mask].sum())
                    shells.append(
                        {
                            "k": k,
                            "nodes": n,
                            "out": int(out_total[mask].sum()),
                            "ret": int(ret_total[mask].sum()),
                            "parked": int(park_total[mask].sum()),
                            "content": content,
                            "per_node": content / n,
                            "jr": float(jr[mask].sum()),
                            "jr_per_node": float(jr[mask].sum()) / n,
                        }
                    )
                row[kind] = shells
            moving = out_total + ret_total
            row["fractions"] = {
                "axes": float(moving[nonzero <= 1].sum()) / total if total else 0.0,
                "planes_off_axes": float(moving[nonzero == 2].sum()) / total if total else 0.0,
                "off_planes": float(moving[nonzero == 3].sum()) / total if total else 0.0,
                "parked": float(park_total.sum()) / total if total else 0.0,
            }
            row["read_nodes"] = {}
            for label, offset in read_nodes.items():
                position = tuple(centre[k] + offset[k] for k in range(3))
                radial = unit(offset)
                j = [int(jvec[k][position]) for k in range(3)]
                row["read_nodes"][label] = {
                    "content": int(out_total[position] + ret_total[position] + park_total[position]),
                    "out": int(out_total[position]),
                    "ret": int(ret_total[position]),
                    "parked": int(park_total[position]),
                    "j": j,
                    "j_radial": sum(j[k] * radial[k] for k in range(3)),
                }
            row["escaped"] = int(world.escaped_totals()["proton"][0])
            ledger = world.audit()
            ledgers.append(ledger)
            row["balanced"] = bool(ledger["balanced"]) and bool(ledger.get("real_conserved", True))
            row["body_momentum"] = [list(b["momentum"]) for b in world.external_bodies()]
            per_tick.append(row)
            log(
                f"  tick {tick} {stepped:.2f}s on board {total} escaped {row['escaped']} "
                f"off planes {row['fractions']['off_planes']:.3f} balanced {row['balanced']}"
            )
    return per_tick, ledgers


def front(per_tick, label):
    """The first tick at which the read Node's content reaches 1 % of its peak, and the peak's tick."""
    series = [row["read_nodes"][label]["content"] for row in per_tick]
    peak = max(series)
    if peak <= 0:
        return {"first": None, "peak_tick": None, "peak": 0}
    first = next(t for t, c in enumerate(series, start=1) if c >= FRONT_THRESHOLD * peak)
    return {"first": first, "peak_tick": series.index(peak) + 1, "peak": peak}


def read_node_labels():
    labels = {}
    for direction, (offsets, _, letter) in PROBES.items():
        for offset in offsets:
            labels[f"{direction}_{letter}{offset[0]}"] = offset
    return labels


# ------------------------------------------------------------- the tables


def fmt(value, digits=1):
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def tables(record):
    lines = []
    lines.append("### The books per bit\n")
    lines.append("| World | Ticks | World line balanced | Real line | Shadow line | `real_conserved` | Shadows at start | At tick 40 | Escaped | Runner s |")
    lines.append("| --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: |")
    for name, row in record["worlds"].items():
        b = row["books"]
        lines.append(
            f"| `{name}` | {row['completed_ticks']} | {'every tick' if all(x['balanced'] for x in b) else 'NO'} | "
            f"{'every tick' if all(x['real_balanced'] for x in b) else 'NO'} | {'every tick' if all(x['shadow_balanced'] for x in b) else 'NO'} | "
            f"{'every tick' if all(x['real_conserved'] for x in b) else 'NO'} | {row['shadows_initial']} | {row['shadows_final']} | {row['escaped']} | {fmt(row['elapsed_seconds'])} |"
        )
    if "pulse" in record["replays"]:
        p = record["replays"]["pulse"]
        lines.append("\n### The pulse: the front per direction and the release off the planes\n")
        lines.append("| Read Node | r | sqrt 3 r | First arrival (tick) | Peak (tick) | Peak content |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
        for label, f in p["fronts"].items():
            r = record["read_nodes"][label]["radius"]
            lines.append(f"| {label} | {r:.2f} | {math.sqrt(3) * r:.1f} | {fmt(f['first'])} | {fmt(f['peak_tick'])} | {f['peak']} |")
        lines.append("\n| t | On the board | Escaped | On the axes | On the planes off the axes | Off the planes | Parked |")
        lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for row in p["per_tick"]:
            if row["tick"] in (1, 2, 3, 5, 10, 20, 30, 40):
                f = row["fractions"]
                lines.append(f"| {row['tick']} | {row['on_board']} | {row['escaped']} | {f['axes']:.3f} | {f['planes_off_axes']:.3f} | {f['off_planes']:.3f} | {f['parked']:.3f} |")
    if "standing" in record["replays"]:
        s = record["replays"]["standing"]
        lines.append("\n### The field of the thing at rest, shell by shell (L1 shells; content per Node and J_r per Node)\n")
        ticks_shown = (1, 5, 10, 20, 30, 40)
        header = "| k | Nodes | " + " | ".join(f"t = {t}" for t in ticks_shown) + " |"
        lines.append(header)
        lines.append("| ---: | ---: | " + " | ".join("---:" for _ in ticks_shown) + " |")
        by_tick = {row["tick"]: row for row in s["per_tick"]}
        for k in range(0, HALF + 1):
            cells = []
            nodes = None
            for t in ticks_shown:
                shell = next((x for x in by_tick[t]["l1"] if x["k"] == k), None)
                if shell is None:
                    cells.append("-")
                    continue
                nodes = shell["nodes"]
                cells.append(f"{shell['per_node']:.0f} / {shell['jr_per_node']:.0f}")
            lines.append(f"| {k} | {nodes} | " + " | ".join(cells) + " |")
        lines.append("\n| t | On the board | Escaped | J_r per Node at k = 4 | 8 | 12 | Off the planes |")
        lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for row in s["per_tick"]:
            if row["tick"] in (1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40):
                j = {x["k"]: x["jr_per_node"] for x in row["l1"]}
                lines.append(f"| {row['tick']} | {row['on_board']} | {row['escaped']} | {j.get(4, 0):.0f} | {j.get(8, 0):.0f} | {j.get(12, 0):.0f} | {row['fractions']['off_planes']:.3f} |")
    if "standing_closed" in record["replays"]:
        c = record["replays"]["standing_closed"]
        w = record["worlds"]["standing_closed"]
        sf = w.get("standing_field") or {}
        lines.append("\n### The closed board: the standing world with `boundary` periodic, 120 ticks, `standing_field` on\n")
        lines.append(f"The runner's standing-set search: fixed point found {sf.get('standing_field')}, iterations {sf.get('standing_field_iterations')}, period {sf.get('standing_field_period')}, residual {sf.get('standing_field_residual')}, ticks kept fixed {sf.get('standing_field_ticks')}, fallback {sf.get('standing_field_fallback')}. Shadows on the board at every tick: {w['shadows_initial']} (escaped {w['escaped']}). Off the planes, mean of the last twenty ticks: {c['off_planes_last_20']:.3f}.\n")
        lines.append("| k (L1) | Nodes | Content per Node, ticks 81-100 | 101-120 | J_r per Node, 81-100 | 101-120 |")
        lines.append("| ---: | ---: | ---: | ---: | ---: | ---: |")
        nodes_of = {x["k"]: x["nodes"] for x in c["per_tick"][-1]["l1"]}
        for k, v in c["settled"].items():
            if v["per_node"] is None:
                continue
            lines.append(f"| {k} | {nodes_of.get(int(k), '-')} | {v['per_node_before']:.0f} | {v['per_node']:.0f} | {v['jr_per_node_before']:.0f} | {v['jr_per_node']:.0f} |")
        lines.append("\n| Read Node | r | Content, ticks 81-100 | 101-120 | J_r, 81-100 | 101-120 |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
        for label, v in c["settled_read_nodes"].items():
            r = record["read_nodes"][label]["radius"]
            lines.append(f"| {label} | {r:.2f} | {v['content_before']:.0f} | {v['content']:.0f} | {v['j_radial_before']:.1f} | {v['j_radial']:.1f} |")
        lines.append("\n| t | On the board | J_r per Node at k = 4 | 8 | 12 | Off the planes | Step s |")
        lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for row in c["per_tick"]:
            if row["tick"] in (1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120):
                j = {x["k"]: x["jr_per_node"] for x in row["l1"]}
                lines.append(f"| {row['tick']} | {row['on_board']} | {j.get(4, 0):.0f} | {j.get(8, 0):.0f} | {j.get(12, 0):.0f} | {row['fractions']['off_planes']:.3f} | {row['seconds']} |")
    lines.append("\n### The test things: the pushed amount per interval and the inventory's J at the same Node\n")
    lines.append("| Probe | r | Cumulative radial push at 40 | At 30 | Mean per interval, ticks 2-21 | 2-11 | 12-21 | 22-31 | 32-40 | Inventory J_r, mean 2-21 (`standing`) | Content per Node at 2 / 21 / 40 | Intervals waited | Body's momentum at 40 |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- |")
    for label, probe in record["probes"].items():
        inv = record["inventory_at_read_nodes"].get(label, {})
        w = probe["window_means"]
        lines.append(
            f"| `{label}` | {probe['radius']:.2f} | {probe['cumulative_radial_at_end']:.0f} | {probe['cumulative_radial_at_30']:.0f} | "
            f"{probe['early_mean_radial']:.1f} | {w['2-11']:.1f} | {w['12-21']:.1f} | {w['22-31']:.1f} | {w['32-40']:.1f} | "
            f"{fmt(inv.get('j_radial_mean_2_21'))} | {inv.get('content_2', '-')} / {inv.get('content_21', '-')} / {inv.get('content_40', '-')} | {probe['waited_intervals']} | {probe['body_momentum_at_end']} |"
        )
    lines.append("\n### The 1/r^2 fit per direction and the anisotropy\n")
    lines.append("| Direction | Quantity | Slope (log-log over three radii) | Standard error | Value at r = 8 | At r = 12 |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: |")
    for direction, fits in record["fits"].items():
        for quantity, fit in fits.items():
            if fit:
                lines.append(f"| {direction} | {quantity} | {fit['slope']:.2f} | {fmt(fit['error'], 2)} | {fit_value(fit, 8):.1f} | {fit_value(fit, 12):.1f} |")
    lines.append("\n| Quantity | Axis / (111) at r = 8 | At r = 12 | Axis / (110) at r = 8 | At r = 12 |")
    lines.append("| --- | ---: | ---: | ---: | ---: |")
    for quantity, a in record["anisotropy"].items():
        lines.append(f"| {quantity} | {fmt(a.get('axis_over_111_at_8'), 3)} | {fmt(a.get('axis_over_111_at_12'), 3)} | {fmt(a.get('axis_over_110_at_8'), 3)} | {fmt(a.get('axis_over_110_at_12'), 3)} |")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("runs", type=Path)
    parser.add_argument("--worlds", type=Path, default=HERE)
    parser.add_argument("--record", type=Path, default=HERE / "record.json")
    parser.add_argument("--tables", type=Path, default=HERE / "tables.md")
    parser.add_argument("--no-replay", action="store_true")
    parser.add_argument("--closed", type=Path, default=None, help="the runs directory of standing_closed")
    args = parser.parse_args(argv)
    labels = read_node_labels()
    record = {
        "experiment": "E11 repeated under the law of the bit (2026-09-18)",
        "read_nodes": {label: {"offset": list(o), "radius": math.sqrt(sum(c * c for c in o))} for label, o in labels.items()},
        "worlds": {},
        "probes": {},
        "replays": {},
        "inventory_at_read_nodes": {},
        "fits": {},
        "anisotropy": {},
    }
    documents = dict(cases())
    runs_of = {name: (args.closed if name.endswith("_closed") and args.closed else args.runs) for name in documents}
    for name in documents:
        run = load_record(runs_of[name], name)
        if run is None:
            print(f"{name}: no record")
            continue
        b = books(run)
        record["worlds"][name] = {
            "status": run["status"],
            "completed_ticks": run["completed_ticks"],
            "source_sha256": run["source_sha256"],
            "initialization_sha256": run["initialization_sha256"],
            "elapsed_seconds": run["elapsed_seconds"],
            "books": b,
            "shadows_initial": run["shadow_content"][0] if run["shadow_content"] else None,
            "shadows_final": run["shadow_content"][-1] if run["shadow_content"] else None,
            "escaped": run["escaped_totals"]["proton"][0],
            "body_positions_fixed": all(p[1:] == run["external_bodies"][0]["positions"][0][1:] for p in run["external_bodies"][0]["positions"]),
            "boundary": documents[name]["boundary"],
            "standing_field": {k: run.get(k) for k in ("standing_field", "standing_field_iterations", "standing_field_period", "standing_field_residual", "standing_field_ticks", "standing_field_fallback", "standing_field_max_iterations")} if "standing_field" in run else None,
        }
        if name.startswith("probe_"):
            direction, tag = name.split("_")[1], name.split("_")[2]
            offsets, heading, letter = PROBES[direction]
            offset = next(o for o in offsets if f"{letter}{o[0]}" == tag)
            record["probes"][f"{direction}_{tag}"] = probe_reading(run, offset, heading)
        print(f"{name}: {run['status']} {run['completed_ticks']} ticks, books balanced at every tick: {all(x['balanced'] for x in b)}")
    if not args.no_replay:
        for name in ("pulse", "standing", "standing_closed"):
            if name not in record["worlds"]:
                continue
            document = json.loads((args.worlds / f"{name}.json").read_text(encoding="utf-8"))
            run = load_record(runs_of[name], name)
            cache = runs_of[name] / name / "replay.json"
            if cache.exists():
                # A replay made earlier beside the record (the same integers:
                # the engine is deterministic), kept with its identity check.
                cached = json.loads(cache.read_text(encoding="utf-8"))
                per_tick, identical = cached["per_tick"], cached["ledger_identical_to_record"]
                print(f"reading the replay of {name} from {cache}")
            else:
                print(f"replaying {name} in-process for the shells")
                per_tick, ledgers = replay(document, record["worlds"][name]["completed_ticks"], labels)
                identical = [l["fields"] for l in ledgers] == [l["fields"] for l in run["audit"]]
                cache.write_text(json.dumps({"per_tick": per_tick, "ledger_identical_to_record": identical}), encoding="utf-8")
            entry = {"per_tick": per_tick, "ledger_identical_to_record": identical}
            if name == "pulse":
                entry["fronts"] = {label: front(per_tick, label) for label in labels}
                entry["release"] = 6 * (document["external_bodies"][0]["amount"] // document["spatial_fields"][0]["release"][1])
            record["replays"][name] = entry
            print(f"  ledger identical to the record: {identical}")
            if name == "standing_closed":
                # The settled state: the mean over the last twenty ticks of the
                # content per Node and J_r per Node per L1 shell, and the change
                # between the last two windows of twenty.
                last = [row for row in per_tick if row["tick"] > len(per_tick) - 20]
                before = [row for row in per_tick if len(per_tick) - 40 < row["tick"] <= len(per_tick) - 20]
                settled = {}
                for k in range(0, HALF + 1):
                    def mean_of(rows, key):
                        values = [next((x[key] for x in row["l1"] if x["k"] == k), None) for row in rows]
                        values = [v for v in values if v is not None]
                        return sum(values) / len(values) if values else None
                    settled[k] = {
                        "per_node": mean_of(last, "per_node"),
                        "per_node_before": mean_of(before, "per_node"),
                        "jr_per_node": mean_of(last, "jr_per_node"),
                        "jr_per_node_before": mean_of(before, "jr_per_node"),
                    }
                entry["settled"] = settled
                entry["settled_read_nodes"] = {
                    label: {
                        "content": sum(row["read_nodes"][label]["content"] for row in last) / len(last),
                        "j_radial": sum(row["read_nodes"][label]["j_radial"] for row in last) / len(last),
                        "content_before": sum(row["read_nodes"][label]["content"] for row in before) / len(before),
                        "j_radial_before": sum(row["read_nodes"][label]["j_radial"] for row in before) / len(before),
                    }
                    for label in labels
                }
                entry["off_planes_last_20"] = sum(row["fractions"]["off_planes"] for row in last) / len(last)
            if name == "standing":
                for label in labels:
                    series = [row["read_nodes"][label] for row in per_tick]
                    early = [s["j_radial"] for s, row in zip(series, per_tick, strict=True) if EARLY[0] <= row["tick"] <= EARLY[1]]
                    record["inventory_at_read_nodes"][label] = {
                        "j_radial_mean_2_21": sum(early) / len(early) if early else None,
                        "j_radial_cumulative_2_40": sum(s["j_radial"] for s, row in zip(series, per_tick, strict=True) if row["tick"] >= 2),
                        "content_2": series[1]["content"],
                        "content_21": series[20]["content"],
                        "content_40": series[-1]["content"],
                        "min_content_2_40": min(s["content"] for s in series[1:]),
                    }
    for direction in PROBES:
        points_end = [(p["radius"], p["cumulative_radial_at_end"]) for label, p in record["probes"].items() if label.startswith(direction + "_")]
        points_early = [(p["radius"], p["early_mean_radial"]) for label, p in record["probes"].items() if label.startswith(direction + "_")]
        points_inv = [
            (record["read_nodes"][label]["radius"], inv["j_radial_mean_2_21"])
            for label, inv in record["inventory_at_read_nodes"].items()
            if label.startswith(direction + "_") and inv["j_radial_mean_2_21"]
        ]
        record["fits"][direction] = {
            "cumulative_push_at_40": fit_slope(points_end),
            "mean_push_2_21": fit_slope(points_early),
            "inventory_j_2_21": fit_slope(points_inv),
        }
    for quantity in ("cumulative_push_at_40", "mean_push_2_21", "inventory_j_2_21"):
        a = {}
        for other in ("111", "110"):
            for r in (8, 12):
                fa, fo = record["fits"]["axis"].get(quantity), record["fits"][other].get(quantity)
                va, vo = fit_value(fa, r), fit_value(fo, r)
                a[f"axis_over_{other}_at_{r}"] = va / vo if va and vo else None
        record["anisotropy"][quantity] = a
    args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    text = tables(record)
    args.tables.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
