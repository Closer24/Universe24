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
    ("single source, row 48", 48, EMISSION, BUDGET, BASELINE, 1600, None, True),
    ("single source, wave, phase per link", 48, EMISSION, BUDGET, BASELINE, 1600, "link", True),
    ("single source, no emission", 48, 0, BUDGET, BASELINE, 700, None, True),
    # Convergence of the wave reading: finer phase steps, and a finer tick resolution of
    # the gaps (a launch hop of 16, so the source's interval is 48 ticks).
    (
        "single source, wave, phase per link, 256 steps",
        48,
        EMISSION,
        BUDGET,
        BASELINE,
        1600,
        "link",
        True,
        256,
    ),
    (
        "single source, wave, phase per link, launch at k = 16",
        48,
        EMISSION,
        BUDGET,
        15000,
        3400,
        "link",
        True,
    ),
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
SINGLE_SPACING = 3  # a single source emits every three launch hops of its own clock


def document(
    length: int,
    emission: int,
    budget: int,
    baseline: int,
    ticks: int,
    wave: str | None = None,
    single: bool = False,
    phase_steps: int = PHASE_STEPS,
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
    # A single source: twelve lamps at x = 0, each emitting once, the i-th on its own
    # clock's tick i * SINGLE_SPACING * k_e, so the rays leave from one place at a fixed
    # interval of the source's clock and all cross the same distance to the eye. The
    # interval is three launch hops because the rule holds one wait register per Node:
    # a ray arriving while another is held leaves with it, so rays closer in time than
    # the hop time would bunch; three hops keeps them apart while k stays below 3 k_e.
    launch_hop = -(-(baseline + emission + 1) // budget) if single else None
    raw = {
        "schema_version": 1,
        "model_id": "redshift-closed-row-ray-delay-v1",
        "boundary": "periodic",
        "shape": [length, 1, 1],
        # A single source puts twelve lamps and the mass body on one Node.
        "slots_per_node": 14 if single else 4,
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
                    {"kerengonen": {"phase_steps": phase_steps, "phase_advance": 1, "capture": "share"}}
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
    if wave or single:
        # One lamp type per lamp: emission phases and timings are per rule, not per record.
        lamp = next(k for k in raw["disturbance_types"] if k["name"] == "lamp")
        rule = next(r for r in raw["emissions"] if r["type"] == "lamp")
        raw["disturbance_types"] = [k for k in raw["disturbance_types"] if k["name"] != "lamp"] + [
            {
                **lamp,
                "name": f"lamp_{i}",
                "fields": ["light", "train", "clock"],
                "defaults": {"light": 1, "train": TRAIN - i, "clock": 0},
                "updates": [{"field": "clock", "expression": op("add", {"field": "clock"}, 1)}],
            }
            for i in range(TRAIN)
        ]
        raw["emissions"] = [r for r in raw["emissions"] if r["type"] != "lamp"] + [
            {
                **rule,
                "type": f"lamp_{i}",
                # The lamps launch a quarter turn apart whatever the step count.
                **({"kerengonen_phase": (i * (phase_steps // 4)) % phase_steps} if wave else {}),
                # A single source emits its i-th ray when its own clock reads i hops.
                **(
                    {
                        "amount": op(
                            "eq", {"field": "clock"}, (TRAIN - 1 - i) * SINGLE_SPACING * launch_hop
                        )
                    }
                    if single
                    else {}
                ),
            }
            for i in range(TRAIN)
        ]
        raw["seeds"] = [s for s in raw["seeds"] if s["type"] != "lamp"] + [
            {"position": [0 if single else i, 0, 0], "type": f"lamp_{i}"} for i in range(TRAIN)
        ]
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


def hop_time_at(schedule: list[tuple[int, int]], tick: int) -> int | None:
    """The hop time in force at a tick: the duration of the last hop begun at or before it."""
    current = None
    for start, duration in schedule:
        if start > tick:
            break
        current = duration
    return current


def frequency_at(seen: dict, x: int, phase_steps: int = PHASE_STEPS) -> float | None:
    """Phase steps per tick of the passing train at Node x: the wave's frequency there."""
    rows = sorted(
        (seen["first_seen"][(train, x)], seen["phases"][(train, x)])
        for train in range(1, TRAIN + 1)
        if (train, x) in seen["phases"]
    )
    if len(rows) < 2:
        return None
    rates: list[float] = []
    for (t0, p0), (t1, p1) in zip(rows, rows[1:], strict=False):
        if t1 == t0:
            continue  # two rays resident together: no interval to read a rate over
        step = (p1 - p0 + phase_steps // 2) % phase_steps - phase_steps // 2
        rates.append(step / (t1 - t0))
    return sum(rates) / len(rates) if rates else None


def mean_gap_at(seen: dict, x: int) -> float | None:
    """The mean interval between consecutive rays passing Node x, in ticks."""
    ticks = sorted(
        seen["first_seen"][(train, x)]
        for train in range(1, TRAIN + 1)
        if (train, x) in seen["first_seen"]
    )
    if len(ticks) < 2:
        return None
    return (ticks[-1] - ticks[0]) / (len(ticks) - 1)


def measure(
    label: str,
    length: int,
    emission: int,
    budget: int,
    baseline: int,
    ticks: int,
    wave: str | None = None,
    single: bool = False,
    phase_steps: int = PHASE_STEPS,
) -> dict:
    raw = document(length, emission, budget, baseline, ticks, wave, single, phase_steps)
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
    # Lamp i sits at x = i and its ray crosses (length - 1 - i) links to the eye; a
    # single source sits at x = 0 and every ray crosses length - 1 links.
    distance = (length - 1) if single else sum(length - 1 - i for i in range(TRAIN)) / TRAIN
    result: dict = {
        "label": label,
        "single_source": single,
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
        # The frequency is read one link past the lamps (past the last lamp of the train,
        # past the single source's Node) and at the eye, and the law is applied over that
        # same span: the gap ratio between those two Nodes, not the run's z, is what the
        # wave's frequency ratio is compared with.
        source_x = 1 if single else TRAIN
        source = frequency_at(seen, source_x, phase_steps)
        eye = frequency_at(seen, length - 1, phase_steps)
        gap_source, gap_eye = mean_gap_at(seen, source_x), mean_gap_at(seen, length - 1)
        span_stretch = gap_eye / gap_source if gap_source and gap_eye else None
        result.update(
            {
                "wave": wave,
                "phase_steps": phase_steps,
                "frequency_read_at_links": [source_x, length - 1],
                "gap_ratio_over_the_frequency_span": round(span_stretch, 4) if span_stretch else None,
                "frequency_at_the_source": round(source, 4) if source is not None else None,
                "frequency_at_the_eye": round(eye, 4) if eye is not None else None,
                "frequency_ratio": round(eye / source, 4) if source and eye is not None else None,
            }
        )
    if len(absorbed) == TRAIN and k_launch:
        mean_gap = sum(gaps_clock) / len(gaps_clock)
        # The train leaves one hop apart; a single source emits every SINGLE_SPACING
        # launch hops of its own clock, an interval fixed by the configuration, so the
        # control without emission (whose first hop is shorter) is read against it too.
        emitted_gap = SINGLE_SPACING * -(-(baseline + emission + 1) // budget) if single else k_launch
        z = mean_gap / emitted_gap - 1
        k_reception = sum(last_hops) / len(last_hops) if last_hops else None
        if single:
            # From one source the launch hop rises during the emission, so the law is read
            # ray by ray: the last hop of each ray over the hop time in force when it left.
            launches = sorted(tick for (train, x), tick in seen["first_seen"].items() if x == 1)
            ratios = []
            for t0, t1, hop0, hop1 in zip(
                launches, launches[1:], last_hops, last_hops[1:], strict=False
            ):
                k_e0 = hop_time_at(schedule, t0) or k_launch
                k_e1 = hop_time_at(schedule, t1) or k_launch
                ratios.append(((hop1 + hop0) / 2) / ((k_e0 + k_e1) / 2))
            k_reception = k_launch * sum(ratios) / len(ratios) if ratios else k_reception
        result.update(
            {
                "z": round(z, 4),
                "duration_ratio": round(
                    (absorbed[-1][1] - absorbed[0][1]) / (emitted_gap * (TRAIN - 1)), 4
                ),
                "hop_time_at_reception": round(k_reception, 4) if k_reception else None,
                "predicted_1_plus_z": round(k_reception / k_launch, 4) if k_reception else None,
                "alpha_measured": round(math.log(1 + z) / distance, 6) if z > 0 else None,
            }
        )
        if wave and result.get("frequency_at_the_source") and span_stretch:
            # Phase per link: the phase difference between rays is conserved along the path
            # (every ray crosses the same links), so the frequency ratio is the inverse of
            # the gap ratio over the span by construction; the measurement checks the phase
            # bookkeeping and its wrap, not an independent stretch. Phase per interval: the
            # advance rate a is added per tick, so only the excess over a follows the gaps.
            advance = 1
            source = result["frequency_at_the_source"]
            result["frequency_ratio_predicted"] = round(
                1 / span_stretch
                if wave == "link"
                else (advance + (source - advance) / span_stretch) / source,
                4,
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
