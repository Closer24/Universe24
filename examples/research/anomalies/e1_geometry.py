"""E1 (geometry): does the transport delay change the dilution or the angular size?

A periodic cube with a uniform static `computation` load (baseline B0 at every
Node, no emission: the hop time k = ceil(B0 / budget) is the same everywhere and
for ever, so there is no stretch) or none. Two lamps 4 links apart along z, each
emitting one ray field over 512 golden-spiral headings (64 rays of 1 quantum per
tick, an 8-tick sweep). Eight eyes in the lamps' mid-plane at distances 3..16 in
four directions absorb both fields into separate stocks and separate momentum
registers (share x heading), so each eye reads the number of rays it received
from each lamp over a window of three full sweeps and the mean heading of each.
The dilution exponent is the log-log slope of count against distance, and the
angular size is the angle between the two mean headings against 2 atan(2 / D).
Run with and without the load; the geometry must not change.

usage: PYTHONPATH=src python examples/research/anomalies/e1_geometry.py --output DIR --baseline 0|3000
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
from run_experiments import golden_headings  # noqa: E402

sys.argv = _argv
from event_universe import Simulation  # noqa: E402
from event_universe.core.disturbance_state import OPERATIONS  # noqa: E402
from event_universe.initialization import parse_initial_state  # noqa: E402
from event_universe.runner import source_fingerprint  # noqa: E402

SIDE = 141
HEADINGS, PER_TICK, SCALE = 4096, 64, 24
SWEEP = HEADINGS // PER_TICK
HALF_SEP = 2  # lamps at z = c +/- 2
# Generic integer offsets in the mid-plane (no eye on a lattice axis or diagonal).
EYE_OFFSETS = ((3, 1), (-4, 2), (-5, -3), (7, -2), (9, 4), (-11, 5), (-13, -8), (17, -6))
BUDGET = 1000


def document(baseline: int, ticks: int) -> dict:
    c = SIDE // 2
    fields = [
        {
            "name": "strength",
            "components": 1,
            "units": "u",
            "signed": False,
            "conserved": True,
            "extensive": True,
        },
        {
            "name": "computation",
            "components": 1,
            "units": "load unit",
            "signed": False,
            "conserved": True,
            "extensive": True,
        },
    ]
    spatial = [{"field": "computation", "baseline": baseline, "transport": "outward"}]
    types = []
    emissions = []
    couplings = []
    eye_fields = []
    for lamp in ("a", "b"):
        fields += [
            {
                "name": f"light_{lamp}",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": f"mom_{lamp}",
                "components": 3,
                "units": "quantum x heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
        ]
        spatial.append(
            {
                "field": f"light_{lamp}",
                "baseline": 0,
                "transport": "ray",
                "headings": golden_headings(HEADINGS, SCALE),
                "rays_per_tick": PER_TICK,
                "ray_slots": 1024,
            }
        )
        types.append(
            {
                "name": f"lamp_{lamp}",
                "fields": ["strength"],
                "defaults": {"strength": PER_TICK},
                "transport": {"mode": "hold"},
            }
        )
        emissions.append(
            {
                "type": f"lamp_{lamp}",
                "field": f"light_{lamp}",
                "amount": {"field": "strength"},
                "denominator": 1,
                "source": True,
            }
        )
        couplings.append(
            {
                "name": f"eye_absorbs_{lamp}",
                "type": "eye",
                "field": f"light_{lamp}",
                "mode": "absorb",
                "momentum_field": f"mom_{lamp}",
            }
        )
        eye_fields += [f"light_{lamp}", f"mom_{lamp}"]
    types.append(
        {
            "name": "eye",
            "fields": eye_fields,
            "defaults": {f: (0 if f.startswith("light") else [0, 0, 0]) for f in eye_fields},
            "transport": {"mode": "hold"},
        }
    )
    seeds = [
        {"position": [c, c, c + HALF_SEP], "type": "lamp_a"},
        {"position": [c, c, c - HALF_SEP], "type": "lamp_b"},
    ]
    for dx, dy in EYE_OFFSETS:
        seeds.append({"position": [c + dx, c + dy, c], "type": "eye"})
    return {
        "schema_version": 1,
        "model_id": "dilution-and-angle-under-load-v1",
        "boundary": "periodic",
        "shape": [SIDE, SIDE, SIDE],
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": BUDGET,
        "ticks": ticks,
        **(
            {"computation_field": "computation", "delay_direction": "along", "ray_delay": True}
            if baseline
            else {}
        ),
        "operation_costs": {n: 1 for n in OPERATIONS},
        "fields": fields,
        "disturbance_types": types,
        "spatial_fields": spatial,
        "emissions": emissions,
        "spatial_couplings": couplings,
        "seeds": seeds,
    }


def eyes(world: Simulation, type_index: int) -> dict[tuple[int, int, int], dict]:
    return {
        pos: world.record_values(r)
        for pos, node in world.nodes.items()
        for r in node.records
        if r is not None and r.type_index == type_index
    }


def angle(u: tuple[float, ...], v: tuple[float, ...]) -> float:
    nu, nv = math.sqrt(sum(x * x for x in u)), math.sqrt(sum(x * x for x in v))
    if nu == 0 or nv == 0:
        return float("nan")
    return math.degrees(
        math.acos(max(-1.0, min(1.0, sum(a * b for a, b in zip(u, v, strict=True)) / (nu * nv))))
    )


def loglog(points: list[tuple[float, float]]) -> dict | None:
    usable = [(math.log(x), math.log(y)) for x, y in points if x > 0 and y > 0]
    if len(usable) < 3:
        return None
    n = len(usable)
    mx = sum(x for x, _ in usable) / n
    my = sum(y for _, y in usable) / n
    sxx = sum((x - mx) ** 2 for x, _ in usable)
    slope = sum((x - mx) * (y - my) for x, y in usable) / sxx
    resid = [y - (my + slope * (x - mx)) for x, y in usable]
    se = math.sqrt(sum(r * r for r in resid) / (n - 2) / sxx)
    return {"slope": round(slope, 3), "se": round(se, 3), "n": n}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--baseline", type=int, default=0)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    k = max(1, -(-args.baseline // BUDGET))
    far = max(abs(dx) + abs(dy) for dx, dy in EYE_OFFSETS)
    warm = k * (far + HALF_SEP + 2)
    window = SWEEP
    ticks = warm + window
    image_distance = SIDE - max(max(abs(dx), abs(dy)) for dx, dy in EYE_OFFSETS)
    raw = document(args.baseline, ticks)
    c = SIDE // 2
    t0 = time.time()
    world = Simulation(parse_initial_state(raw))
    type_index = [t["name"] for t in raw["disturbance_types"]].index("eye")
    for _ in range(warm):
        world.step()
    before = eyes(world, type_index)
    for _ in range(window):
        world.step()
    after = eyes(world, type_index)
    host = round(time.time() - t0, 1)
    rows = []
    for pos, v1 in after.items():
        v0 = before[pos]
        d = math.sqrt((pos[0] - c) ** 2 + (pos[1] - c) ** 2)
        r_lamp = math.sqrt(d * d + HALF_SEP**2)
        counts = {lamp: v1[f"light_{lamp}"][0] - v0[f"light_{lamp}"][0] for lamp in ("a", "b")}
        moms = {
            lamp: tuple(a - b for a, b in zip(v1[f"mom_{lamp}"], v0[f"mom_{lamp}"], strict=True))
            for lamp in ("a", "b")
        }
        rows.append(
            {
                "position": list(pos),
                "D_in_plane": d,
                "r_to_each_lamp": round(r_lamp, 3),
                "count_a": counts["a"],
                "count_b": counts["b"],
                "count_mean": (counts["a"] + counts["b"]) / 2,
                "mean_heading_a": [
                    round(m / counts["a"], 2) if counts["a"] else None for m in moms["a"]
                ],
                "mean_heading_b": [
                    round(m / counts["b"], 2) if counts["b"] else None for m in moms["b"]
                ],
                "angle_between_lamps_deg": round(angle(moms["a"], moms["b"]), 3),
                "angle_expected_static_deg": round(math.degrees(2 * math.atan(HALF_SEP / d)), 3),
            }
        )
    rows.sort(key=lambda r: r["D_in_plane"])
    report = {
        "source_sha256": source_fingerprint(),
        "baseline": args.baseline,
        "hop_time_k": k,
        "side": SIDE,
        "headings": HEADINGS,
        "rays_per_tick": PER_TICK,
        "warm": warm,
        "window_ticks": window,
        "sweeps_in_window": 1,
        "image_distance_links": image_distance,
        "image_arrival_tick_at_least": image_distance * k,
        "window_free_of_images": image_distance * k > ticks,
        "rows": rows,
        "dilution_fit_count_vs_r": loglog([(r["r_to_each_lamp"], r["count_mean"]) for r in rows]),
        "angle_fit_vs_D": loglog(
            [
                (r["D_in_plane"], r["angle_between_lamps_deg"])
                for r in rows
                if r["angle_between_lamps_deg"] == r["angle_between_lamps_deg"]
            ]
        ),
        "angle_ratio_measured_over_static": [
            round(r["angle_between_lamps_deg"] / r["angle_expected_static_deg"], 3)
            for r in rows
            if r["angle_between_lamps_deg"] == r["angle_between_lamps_deg"]
        ],
        "quanta_closed": all(
            world.totals()[f"light_{lamp}"][0] == PER_TICK * ticks for lamp in ("a", "b")
        ),
        "host_seconds": host,
    }
    (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"baseline {args.baseline} (k = {k}): window {warm + 1}..{ticks}, images free {report['window_free_of_images']}, closed {report['quanta_closed']}, host {host} s"
    )
    for r in rows:
        print(
            f"  D {r['D_in_plane']:5.1f} r {r['r_to_each_lamp']:6.2f}: counts {r['count_a']:4d} {r['count_b']:4d}; angle {r['angle_between_lamps_deg']:7.3f} vs static {r['angle_expected_static_deg']:7.3f}"
        )
    print(
        "  dilution",
        report["dilution_fit_count_vs_r"],
        "angle",
        report["angle_fit_vs_D"],
        "angle ratios",
        report["angle_ratio_measured_over_static"],
    )


if __name__ == "__main__":
    main()
