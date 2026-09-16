"""E3: the force-law exponent of a 1/r^2 ray source when one dimension is closed and short.

The gravity probe's held-body configuration (examples/gravity-probe): a source at
the centre emits `radiation` rays over golden-spiral headings, and a held body of
mass 1 gains momentum -(mass x flux) / D toward the source for every ray that
crosses its Node (exchange coupling; rays pass through, so bodies do not shadow
each other). Bodies sit in the source's plane at several radii on the four axes
and the four diagonals. Boxes: a periodic slab [S, S, depth] (closed short third
dimension, S wide enough that no ray laps within the window), an open cube (the
three-dimensional control), and an open slab (rays leak through the faces).
The pull per tick over one full heading sweep after the front has passed every
body is fitted as pull ~ r^p per box. Read-only inventory audit.

usage: PYTHONPATH=src python examples/research/anomalies/e3_rotation.py --output DIR --box periodic-slab|open-cube|open-slab [--depth 3] [--side 201]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "examples" / "gravity-probe"))
_argv, sys.argv = sys.argv, sys.argv[:1]
from run_experiments import HEADING_SCALE, STRENGTH, attraction, golden_headings  # noqa: E402

sys.argv = _argv
from event_universe import Simulation  # noqa: E402
from event_universe.initialization import parse_initial_state  # noqa: E402
from event_universe.runner import source_fingerprint  # noqa: E402

HEADINGS = 4096
RAYS_PER_TICK = 64
SWEEP = HEADINGS // RAYS_PER_TICK  # 64 ticks
AXIS_RADII = (3, 4, 6, 8, 12, 16, 24)
DIAGONAL_STEPS = (2, 3, 4, 6, 8, 12, 17)  # r = step * sqrt(2): 2.8 .. 24.0
AXES = ((1, 0), (-1, 0), (0, 1), (0, -1))
DIAGONALS = ((1, 1), (1, -1), (-1, 1), (-1, -1))


def document(box: str, side: int, depth: int, ticks: int) -> dict:
    shape = [side, side, side] if box == "open-cube" else [side, side, depth]
    boundary = "periodic" if box == "periodic-slab" else "open"
    c = [s // 2 for s in shape]
    raw = {
        "schema_version": 1,
        "model_id": f"ray-gravity-{box}-v1",
        "shape": shape,
        "boundary": boundary,
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": {
            n: 1
            for n in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            {
                "name": "strength",
                "components": 1,
                "units": "source units per tick",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "radiation",
                "components": 1,
                "units": "ray unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "mass",
                "components": 1,
                "units": "mass unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "momentum unit",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "source",
                "fields": ["strength"],
                "defaults": {"strength": STRENGTH},
                "transport": {"mode": "hold"},
            },
            {
                "name": "held_body",
                "fields": ["mass", "momentum"],
                "defaults": {"mass": 1, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [
            {
                "field": "radiation",
                "baseline": 0,
                "transport": "ray",
                "headings": golden_headings(HEADINGS, HEADING_SCALE),
                "rays_per_tick": RAYS_PER_TICK,
                "ray_slots": 4096,
            },
            {"field": "momentum", "baseline": [0, 0, 0], "transport": "local"},
        ],
        "emissions": [
            {
                "type": "source",
                "field": "radiation",
                "amount": {"field": "strength"},
                "denominator": 1,
                "source": True,
            }
        ],
        "spatial_couplings": [attraction("held_body")],
        "seeds": [{"position": c, "type": "source"}],
    }
    for r in AXIS_RADII:
        for ax, ay in AXES:
            raw["seeds"].append({"position": [c[0] + ax * r, c[1] + ay * r, c[2]], "type": "held_body"})
    for s in DIAGONAL_STEPS:
        for dx, dy in DIAGONALS:
            raw["seeds"].append({"position": [c[0] + dx * s, c[1] + dy * s, c[2]], "type": "held_body"})
    return raw


def bodies(world: Simulation, type_index: int) -> dict[tuple[int, int, int], tuple[int, ...]]:
    found = {}
    for position, node in world.nodes.items():
        for record in node.records:
            if record is not None and record.type_index == type_index:
                found[position] = tuple(world.record_values(record)["momentum"])
    return found


def fit_exponent(points: list[tuple[float, float]]) -> dict | None:
    usable = [(math.log(r), math.log(v)) for r, v in points if v > 0 and r > 0]
    if len(usable) < 3:
        return None
    n = len(usable)
    mx = sum(x for x, _ in usable) / n
    my = sum(y for _, y in usable) / n
    sxx = sum((x - mx) ** 2 for x, _ in usable)
    sxy = sum((x - mx) * (y - my) for x, y in usable)
    slope = sxy / sxx
    resid = [y - (my + slope * (x - mx)) for x, y in usable]
    se = math.sqrt(sum(r * r for r in resid) / (n - 2) / sxx)
    return {
        "p": round(slope, 3),
        "se": round(se, 3),
        "n": n,
        "r_range": [
            round(math.exp(min(x for x, _ in usable)), 2),
            round(math.exp(max(x for x, _ in usable)), 2),
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--box", choices=["periodic-slab", "open-cube", "open-slab"], required=True)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--side", type=int, default=201)
    parser.add_argument(
        "--warm",
        type=int,
        default=SWEEP + 26,
        help="ticks before the window (front past r = 24 + one sweep)",
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    ticks = args.warm + SWEEP
    raw = document(args.box, args.side, args.depth, ticks)
    c = [s // 2 for s in raw["shape"]]
    # No ray may lap the box within the window: the nearest image of the source is side - r away.
    lap_safe = raw["boundary"] == "open" or (args.side - max(AXIS_RADII)) > ticks
    t0 = time.time()
    world = Simulation(parse_initial_state(raw))
    for _ in range(args.warm):
        world.step()
    before = bodies(world, 1)
    for _ in range(SWEEP):
        world.step()
    after = bodies(world, 1)
    host = round(time.time() - t0, 1)
    rows = []
    for position, m1 in after.items():
        m0 = before[position]
        gained = tuple(a - b for a, b in zip(m1, m0, strict=True))
        offset = tuple(v - cc for v, cc in zip(position, c, strict=True))
        r = math.sqrt(sum(o * o for o in offset))
        radial = sum(g * o for g, o in zip(gained, offset, strict=True)) / r
        kind = "axis" if 0 in offset[:2] else "diagonal"
        rows.append(
            {
                "position": list(position),
                "kind": kind,
                "r": round(r, 3),
                "momentum_gained": gained,
                "pull_per_tick_toward_source": round(-radial / SWEEP, 4),
            }
        )
    rows.sort(key=lambda row: (row["kind"], row["r"]))
    # Average the four directions at each radius; error = standard error over directions.
    grouped: dict[tuple[str, float], list[float]] = {}
    for row in rows:
        grouped.setdefault((row["kind"], row["r"]), []).append(row["pull_per_tick_toward_source"])
    table = []
    for (kind, r), pulls in sorted(grouped.items()):
        m = sum(pulls) / len(pulls)
        se = (
            math.sqrt(sum((p - m) ** 2 for p in pulls) / (len(pulls) - 1) / len(pulls))
            if len(pulls) > 1
            else None
        )
        table.append(
            {
                "kind": kind,
                "r": r,
                "n_directions": len(pulls),
                "pull_mean": round(m, 4),
                "pull_se": None if se is None else round(se, 4),
                "pulls": pulls,
            }
        )
    fits = {
        "axis_all": fit_exponent([(t["r"], t["pull_mean"]) for t in table if t["kind"] == "axis"]),
        "diagonal_all": fit_exponent(
            [(t["r"], t["pull_mean"]) for t in table if t["kind"] == "diagonal"]
        ),
        "pooled_r_ge_4": fit_exponent([(t["r"], t["pull_mean"]) for t in table if t["r"] >= 4]),
        "pooled_r_lt_depth": fit_exponent(
            [(t["r"], t["pull_mean"]) for t in table if t["r"] < args.depth]
        )
        if args.box != "open-cube"
        else None,
        "pooled_r_gt_depth": fit_exponent(
            [(t["r"], t["pull_mean"]) for t in table if t["r"] > args.depth]
        )
        if args.box != "open-cube"
        else None,
    }
    totals = world.totals()["momentum"]
    report = {
        "source_sha256": source_fingerprint(),
        "box": args.box,
        "shape": raw["shape"],
        "boundary": raw["boundary"],
        "depth": args.depth,
        "headings": HEADINGS,
        "rays_per_tick": RAYS_PER_TICK,
        "sweep_ticks": SWEEP,
        "warm_ticks": args.warm,
        "window": [args.warm + 1, ticks],
        "no_ray_laps_in_window": lap_safe,
        "momentum_closed": totals == (0, 0, 0),
        "momentum_total": totals,
        "all_pulls_toward_source": all(row["pull_per_tick_toward_source"] > 0 for row in rows),
        "table": table,
        "fits": fits,
        "rows": rows,
        "host_seconds": host,
    }
    (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"{args.box} depth {args.depth} side {args.side}: window {report['window']}, lap-safe {lap_safe}, closed {report['momentum_closed']}, host {host} s"
    )
    for t in table:
        print(
            f"  {t['kind']:8s} r {t['r']:6.2f}: pull {t['pull_mean']:8.3f} +/- {t['pull_se']}  {t['pulls']}"
        )
    for name, fit in fits.items():
        print("  fit", name, fit)


if __name__ == "__main__":
    main()
