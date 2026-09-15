"""Redshift from delay growth on a closed row: the law read by a local clock, and a size sweep.

A closed row of Nodes (periodic in x, one Node across) holds a mass body at
every Node, each emitting a constant amount of the `computation` field per
cycle, so the field's total grows linearly with age and, by symmetry, the load
at every Node grows alike: a closed universe filling uniformly with field.
Light is a train of twelve single-quantum rays, one link apart, launched at
tick 1 by twelve lamps and absorbed by an eye at the far end of the row.
`ray_delay` makes a ray wait `k - 1 = ceil(load / budget) - 1` extra field
cycles at every Node it crosses, so a hop takes k ticks and k rises with age;
`delay_direction: "along"` keeps every local cycle at the bare cycle time,
and the eye counts its own cycles as its clock. The rays leave one hop apart,
k_e ticks, and reach the eye k_o ticks apart, so the stretch the eye reads on
its own clock is 1 + z = k_o / k_e, the ratio of the hop time at reception to
the hop time at launch; the train's duration stretches by the same ratio.
Distance enters through the travel time: with k linear in age,
D = (B / lambda) ln(k_o / k_e) for a load growing by lambda per tick, so
1 + z = exp(alpha D) with alpha = lambda / B per hop, the rate at which the hop
time rises: an exponential distance-redshift law with no recession.

The sweep varies the row's length (the distance from the lamps to the eye),
the emission (alpha must scale with it) and the baseline (the hop time at
launch, which sets the resolution of z: with k_e = 1 the stretch takes
whole-number values only). Every number is a read-only inventory audit at
host lattice coordinates; no angle, length or time unit is identified.

Moving bodies were the first choice of light and are not used: a Node starts
no new cycle until its delayed departure has arrived, so a train of bodies
stalls the clocks of the Nodes it waits at (the emitters of a 24-row
completed 320 to 436 cycles in 700 ticks with the train and 700 without);
rays wait without stalling anyone, and the eye's clock keeps the bare rate.

usage: python examples/relativity-probes/redshift_sweep.py --output DIR [--quick] [--labels ...]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS, unpack
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

TRAIN = 12
EMISSION, BUDGET, BASELINE = 16, 1000, 7000
# The sweep: (label, length, emission, budget, baseline, ticks).
SWEEP = (
    ("row 16", 16, EMISSION, BUDGET, BASELINE, 400),
    ("row 24", 24, EMISSION, BUDGET, BASELINE, 500),
    ("row 32", 32, EMISSION, BUDGET, BASELINE, 700),
    ("row 48", 48, EMISSION, BUDGET, BASELINE, 1000),
    ("row 64", 64, EMISSION, BUDGET, BASELINE, 1600),
    ("row 96", 96, EMISSION, BUDGET, BASELINE, 2600),
    ("control, no emission", 48, 0, BUDGET, BASELINE, 500),
    ("half the emission", 48, 8, BUDGET, BASELINE, 1000),
    ("double the emission", 48, 32, BUDGET, BASELINE, 1000),
    ("launch at k = 1", 48, EMISSION, BUDGET, 900, 600),
    ("launch at k = 4", 48, EMISSION, BUDGET, 3000, 600),
    ("launch at k = 16", 48, EMISSION, BUDGET, 15000, 2000),
    ("wave, phase per link", 48, EMISSION, BUDGET, BASELINE, 1000, "link"),
    ("wave, phase per interval", 48, EMISSION, BUDGET, BASELINE, 1000, "interval"),
    ("wave, phase per link, no emission", 48, 0, BUDGET, BASELINE, 500, "link"),
)
QUICK = (
    ("row 16", 16, 32, BUDGET, BASELINE, 400),
    ("control, no emission", 16, 0, BUDGET, BASELINE, 200),
)
# Global field order of the document: the eye's light and clock are read by these indices.
FIELDS = ("mass", "clock", "train", "light", "computation")


def op(name: str, *args: object) -> dict:
    return {"op": name, "args": list(args)}


PHASE_STEPS = 64
WAVE_STEP = 16  # phase steps between consecutive lamps: the emitted wave's phase per hop


def document(
    length: int, emission: int, budget: int, baseline: int, ticks: int, wave: str | None = None
) -> dict:
    """The closed row; with `wave` the light is a Kerengonen field whose rays carry a phase.

    `wave = "link"` advances the phase once per link; `wave = "interval"` advances it on
    every waiting interval as well (`ray_phase_per_tick`). Consecutive lamps launch rays
    WAVE_STEP phase steps apart, so the train is a wave of WAVE_STEP steps per hop at the
    source; the eye reads the phase of every ray it absorbs and the frequency it sees is
    the phase difference between consecutive absorptions over the gap on its clock.
    """
    if length <= TRAIN:
        raise ValueError("the row must be longer than the train so the eye is ahead of it")
    raw = {
        "schema_version": 1,
        "model_id": "redshift-closed-row-ray-delay-v1",
        "boundary": "periodic",
        "shape": [length, 1, 1],
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": budget,
        "ticks": ticks,
        "computation_field": "computation",
        "delay_direction": "along",
        "ray_delay": True,
        **({"ray_phase_per_tick": True} if wave == "interval" else {}),
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "mass", "components": 1, "units": "unit", "signed": False, "conserved": True},
            {
                "name": "clock",
                "components": 1,
                "units": "completed cycles",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
            {
                "name": "train",
                "components": 1,
                "units": "label",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
            {
                "name": "light",
                "components": 1,
                "units": "quantum",
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
        ],
        "disturbance_types": [
            {
                "name": "mass body",
                "fields": ["mass"],
                "defaults": {"mass": 1},
                "transport": {"mode": "hold"},
            },
            {
                "name": "lamp",
                "fields": ["light", "train"],
                "defaults": {"light": 1, "train": 0},
                "transport": {"mode": "hold"},
            },
            {
                "name": "eye",
                "fields": ["light", "clock"],
                "defaults": {"light": 0, "clock": 0},
                "updates": [{"field": "clock", "expression": op("add", {"field": "clock"}, 1)}],
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [
            {"field": "computation", "baseline": baseline, "transport": "outward"},
            {
                "field": "light",
                "baseline": 0,
                "transport": "ray",
                "headings": [[1, 0, 0]],
                "rays_per_tick": 1,
                "ray_slots": 16,
                # Claims let every ray carry its lamp's train label, so rays never merge.
                "claim": {"ticks": 4 * ticks, "slots": 4},
                **(
                    {"kerengonen": {"phase_steps": PHASE_STEPS, "phase_advance": 1, "capture": "share"}}
                    if wave
                    else {}
                ),
            },
        ],
        "emissions": [
            {
                "type": "mass body",
                "field": "computation",
                "amount": emission,
                "denominator": 1,
                "source": True,
            },
            {
                "type": "lamp",
                "field": "light",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "train_field": "train",
                "heading": [1, 0, 0],
            },
        ],
        "spatial_couplings": [
            {"name": "eye_absorbs", "field": "light", "mode": "absorb", "claim": True, "type": "eye"}
        ],
        "seeds": [{"position": [x, 0, 0], "type": "mass body"} for x in range(length)]
        + [{"position": [i, 0, 0], "type": "lamp", "values": {"train": TRAIN - i}} for i in range(TRAIN)]
        + [{"position": [length - 1, 0, 0], "type": "eye"}],
    }
    if wave:
        # One lamp type per lamp, each emitting at its own phase: emission phases are per rule.
        lamp = next(k for k in raw["disturbance_types"] if k["name"] == "lamp")
        rule = next(r for r in raw["emissions"] if r["type"] == "lamp")
        raw["disturbance_types"] = [k for k in raw["disturbance_types"] if k["name"] != "lamp"] + [
            {**lamp, "name": f"lamp_{i}", "defaults": {"light": 1, "train": TRAIN - i}}
            for i in range(TRAIN)
        ]
        raw["emissions"] = [r for r in raw["emissions"] if r["type"] != "lamp"] + [
            {**rule, "type": f"lamp_{i}", "kerengonen_phase": (i * WAVE_STEP) % PHASE_STEPS}
            for i in range(TRAIN)
        ]
        raw["seeds"] = [
            {**s, "type": f"lamp_{s['position'][0]}"} if s["type"] == "lamp" else s for s in raw["seeds"]
        ]
        for s in raw["seeds"]:
            s.pop("values", None) if s["type"].startswith("lamp_") else None
    return raw


def observe(raw: dict) -> dict:
    """The eye's absorptions on its own clock, the leading ray's hops, and the field's growth."""
    world = Simulation(parse_initial_state(raw))
    names = [kind["name"] for kind in raw["disturbance_types"]]
    light, clock = FIELDS.index("light"), FIELDS.index("clock")
    length = raw["shape"][0]
    first_seen: dict[tuple[int, int], int] = {}
    phases: dict[tuple[int, int], int] = {}
    absorptions: list[tuple[int, int, int]] = []  # (tick, eye clock, light absorbed so far)
    last_light = 0
    checkpoints: list[tuple[int, int]] = []
    for tick in range(1, raw["ticks"] + 1):
        world.step()
        view = world.inventory_view()
        for node in view.nodes:
            if node.rays:
                for ray in node.rays[1]:
                    if (ray.train, node.position[0]) not in first_seen:
                        first_seen[(ray.train, node.position[0])] = tick
                        phases[(ray.train, node.position[0])] = ray.phase
            if node.position[0] == length - 1:
                for record in node.records:
                    if record is not None and names[record.type_index] == "eye":
                        got = unpack(record.values[light])[0]
                        if got != last_light:
                            absorptions.append((tick, unpack(record.values[clock])[0], got))
                            last_light = got
        if tick % max(1, raw["ticks"] // 4) == 0:
            checkpoints.append((tick, world.totals()["computation"][0]))
    increments = [b[1] - a[1] for a, b in zip(checkpoints, checkpoints[1:], strict=False)]
    return {
        "first_seen": first_seen,
        "phases": phases,
        "absorptions": absorptions,
        "light_total": world.totals()["light"][0],
        "closure": {
            "computation_checkpoints": checkpoints,
            "increments": increments,
            "linear_in_age": len(set(increments)) == 1,
            "light_conserved": world.totals()["light"][0] == TRAIN,
        },
    }


def frequency_at(seen: dict, x: int) -> float | None:
    """Phase steps per tick of the passing train at Node x: the wave's frequency there."""
    rows = sorted(
        (seen["first_seen"][(train, x)], seen["phases"][(train, x)])
        for train in range(1, TRAIN + 1)
        if (train, x) in seen["phases"]
    )
    if len(rows) < 2:
        return None
    rates = []
    for (t0, p0), (t1, p1) in zip(rows, rows[1:], strict=False):
        step = (p1 - p0 + PHASE_STEPS // 2) % PHASE_STEPS - PHASE_STEPS // 2
        rates.append(step / (t1 - t0))
    return sum(rates) / len(rates)


def measure(
    label: str,
    length: int,
    emission: int,
    budget: int,
    baseline: int,
    ticks: int,
    wave: str | None = None,
) -> dict:
    raw = document(length, emission, budget, baseline, ticks, wave)
    seen = observe(raw)
    # Every ray's hop schedule, (tick the hop began, its duration): the load is uniform, so
    # any ray's hop measures the hop time k in force at that tick.
    schedule: list[tuple[int, int]] = []
    for train in range(1, TRAIN + 1):
        track = sorted((tick, x) for (t, x), tick in seen["first_seen"].items() if t == train)
        schedule.extend((a[0], b[0] - a[0]) for a, b in zip(track, track[1:], strict=False))
    schedule.sort()
    leading = sorted((tick, x) for (t, x), tick in seen["first_seen"].items() if t == 1)
    k_launch = leading[1][0] - leading[0][0] if len(leading) > 1 else None
    # The hop time in force against age, from every ray's hops: the least-squares slope of
    # duration against the tick a hop began is the rate at which k rises, alpha per hop.
    if len(schedule) > 1:
        n = len(schedule)
        mean_t = sum(s for s, _ in schedule) / n
        mean_k = sum(d for _, d in schedule) / n
        sxx = sum((s - mean_t) ** 2 for s, _ in schedule)
        alpha_schedule = sum((s - mean_t) * (d - mean_k) for s, d in schedule) / sxx if sxx else None
    else:
        alpha_schedule = None
    # The hop time at reception: each ray's last hop, into the eye's Node, whose durations
    # the gaps between absorptions repeat (a ray is absorbed on the cycle after it arrives).
    last_hops = []
    for train in range(1, TRAIN + 1):
        track = sorted((tick, x) for (t, x), tick in seen["first_seen"].items() if t == train)
        if len(track) > 1 and track[-1][1] == length - 1:
            last_hops.append(track[-1][0] - track[-2][0])
    absorbed = seen["absorptions"]
    gaps_ticks = [b[0] - a[0] for a, b in zip(absorbed, absorbed[1:], strict=False)]
    gaps_clock = [b[1] - a[1] for a, b in zip(absorbed, absorbed[1:], strict=False)]
    # Lamp i sits at x = i and its ray crosses (length - 1 - i) links to the eye.
    distance = sum(length - 1 - i for i in range(TRAIN)) / TRAIN
    result: dict = {
        "label": label,
        "length": length,
        "emission": emission,
        "budget": budget,
        "baseline": baseline,
        "ticks": ticks,
        "distance": distance,
        "hop_time_at_launch": k_launch,
        "alpha_from_schedule": round(alpha_schedule, 6) if alpha_schedule else None,
        "last_hops_into_the_eye": last_hops,
        "hop_times_of_the_leading_ray": [
            b[0] - a[0] for a, b in zip(leading, leading[1:], strict=False)
        ],
        "absorbed": len(absorbed),
        "first_absorption_tick": absorbed[0][0] if absorbed else None,
        "gaps_on_the_eye_clock": gaps_clock,
        "gaps_in_ticks": gaps_ticks,
        "eye_clock_equals_ticks": all(a[0] == a[1] for a in absorbed),
        "closure": seen["closure"],
    }
    if wave:
        # The wave's frequency one link past the lamps and at the eye, and the ratio the
        # law predicts: the whole frequency redshifts when the phase advances per link,
        # only its excess over the advance rate when it advances per interval as well.
        source = frequency_at(seen, TRAIN)
        eye = frequency_at(seen, length - 1)
        result.update(
            {
                "wave": wave,
                "frequency_at_the_source": round(source, 4) if source is not None else None,
                "frequency_at_the_eye": round(eye, 4) if eye is not None else None,
                "frequency_ratio": round(eye / source, 4) if source and eye is not None else None,
            }
        )
    if len(absorbed) == TRAIN and k_launch:
        mean_gap = sum(gaps_clock) / len(gaps_clock)
        z = mean_gap / k_launch - 1
        k_reception = sum(last_hops) / len(last_hops) if last_hops else None
        result.update(
            {
                "z": round(z, 4),
                "duration_ratio": round(
                    (absorbed[-1][1] - absorbed[0][1]) / (k_launch * (TRAIN - 1)), 4
                ),
                "hop_time_at_reception": round(k_reception, 4) if k_reception else None,
                "predicted_1_plus_z": round(k_reception / k_launch, 4) if k_reception else None,
                "alpha_measured": round(math.log(1 + z) / distance, 6) if z > 0 else None,
            }
        )
        if wave and result.get("frequency_at_the_source"):
            advance = 1
            source = result["frequency_at_the_source"]
            result["frequency_ratio_predicted"] = round(
                1 / (1 + z) if wave == "link" else (advance + (source - advance) / (1 + z)) / source, 4
            )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--quick", action="store_true", help="two short runs for a smoke test")
    parser.add_argument(
        "--labels", nargs="*", default=None, help="run only the sweep rows whose label contains one"
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    rows = QUICK if args.quick else SWEEP
    if args.labels:
        rows = tuple(row for row in rows if any(label in row[0] for label in args.labels))
    runs = [measure(*row) for row in rows]
    report = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only inventory audit",
        "train": TRAIN,
        "runs": runs,
    }
    (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    for run in runs:
        print(
            f"{run['label']}: row {run['length']}, emission {run['emission']}, budget {run['budget']},"
            f" baseline {run['baseline']}; D {run['distance']}, k at launch {run['hop_time_at_launch']},"
            f" absorbed {run['absorbed']} of {TRAIN}, z {run.get('z')}, k_o/k_e {run.get('predicted_1_plus_z')},"
            f" duration ratio {run.get('duration_ratio')}, alpha measured {run.get('alpha_measured')}"
            f" from the schedule {run.get('alpha_from_schedule')}; eye clock = ticks"
            f" {run['eye_clock_equals_ticks']};"
            f" gaps {run['gaps_on_the_eye_clock']}; field linear {run['closure']['linear_in_age']},"
            f" light conserved {run['closure']['light_conserved']}"
            + (
                f"; wave {run['wave']}: frequency {run['frequency_at_the_source']} at the source,"
                f" {run['frequency_at_the_eye']} at the eye, ratio {run['frequency_ratio']}"
                f" (predicted {run.get('frequency_ratio_predicted')})"
                if run.get("wave")
                else ""
            )
        )
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
