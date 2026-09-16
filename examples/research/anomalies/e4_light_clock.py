"""E4: a clock built from the model's own moving parts, read under a growing load.

A [L, 5, 1] periodic lattice whose load grows uniformly (a mass body at every
Node emits `computation` each cycle, as in the redshift sweep). Two light
clocks: a `light` ray bouncing along y between a bottom mirror at y = 0 and a
top mirror at y = 4 (4 links per leg), one clock in column x = 0 (the source)
and one in column x = L - 1 (the eye). Every time the source's bottom mirror
catches its clock ray it also fires one `signal` quantum down +x: an
oscillating source whose frequency is carried by a physical process. The eye
absorbs the signals and runs, in the same record, the paper's bare-rate
counter (`clock`). Every Node has one wait register under `ray_delay`, so the
signal and the bounced ray leave the source together and part at the top
mirror; signals never enter the eye's clock column except at the eye itself,
where they are absorbed on arrival.

Read-only inventory audit; no unit is identified.

usage: PYTHONPATH=src python examples/research/anomalies/e4_light_clock.py --output DIR [--emission 16]
       [--baseline 3000] [--ticks 4000] [--length 32] [--direction along|none]
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS, unpack
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

FIELDS = ("mass", "clock", "light", "signal", "computation")
SPATIAL = ("computation", "light", "signal")  # spatial field order: node.rays index
LEG = 4  # links per leg: mirrors at y = 0 and y = LEG on a lattice of extent LEG + 1


def op(name: str, *args: object) -> dict:
    return {"op": name, "args": list(args)}


def document(length: int, emission: int, budget: int, baseline: int, ticks: int, direction: str) -> dict:
    counter = {"field": "clock", "expression": op("add", {"field": "clock"}, 1)}
    raw = {
        "schema_version": 1,
        "model_id": "light-clock-under-load-v1",
        "boundary": "periodic",
        "shape": [length, LEG + 1, 1],
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": budget,
        "ticks": ticks,
        "computation_field": "computation",
        **({"delay_direction": "along"} if direction == "along" else {}),
        "ray_delay": True,
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
                "name": "light",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "signal",
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
            # The source: bottom mirror of the source clock, a counter, and a stock of signals.
            {
                "name": "source",
                "fields": ["light", "signal", "clock"],
                "defaults": {"light": 1, "signal": ticks, "clock": 0},
                "updates": [counter],
                "transport": {"mode": "hold"},
            },
            {
                "name": "top",
                "fields": ["light", "clock"],
                "defaults": {"light": 0, "clock": 0},
                "updates": [counter],
                "transport": {"mode": "hold"},
            },
            # The eye: bottom mirror of the eye clock, absorbs signals, and a counter.
            {
                "name": "eye",
                "fields": ["light", "signal", "clock"],
                "defaults": {"light": 1, "signal": 0, "clock": 0},
                "updates": [counter],
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [
            {"field": "computation", "baseline": baseline, "transport": "outward"},
            {
                "field": "light",
                "baseline": 0,
                "transport": "ray",
                "headings": [[0, 1, 0], [0, -1, 0]],
                "rays_per_tick": 1,
                "ray_slots": 8,
            },
            {
                "field": "signal",
                "baseline": 0,
                "transport": "ray",
                "headings": [[1, 0, 0]],
                "rays_per_tick": 1,
                "ray_slots": 64,
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
            # Bottom mirrors re-emit their whole light stock upward; the source also fires
            # one signal per caught ray (its amount reads the light stock it just caught).
            # The signal rule is listed first: funded rules debit the stock they read in
            # order, so listed after the bounce it would read a light stock of zero.
            {
                "type": "source",
                "field": "signal",
                "amount": {"field": "light"},
                "denominator": 1,
                "source": False,
                "heading": [1, 0, 0],
            },
            {
                "type": "source",
                "field": "light",
                "amount": {"field": "light"},
                "denominator": 1,
                "source": False,
                "heading": [0, 1, 0],
            },
            {
                "type": "eye",
                "field": "light",
                "amount": {"field": "light"},
                "denominator": 1,
                "source": False,
                "heading": [0, 1, 0],
            },
            {
                "type": "top",
                "field": "light",
                "amount": {"field": "light"},
                "denominator": 1,
                "source": False,
                "heading": [0, -1, 0],
            },
        ],
        "spatial_couplings": [
            {"name": "source_catches", "type": "source", "field": "light", "mode": "absorb"},
            {"name": "eye_catches", "type": "eye", "field": "light", "mode": "absorb"},
            {"name": "top_catches", "type": "top", "field": "light", "mode": "absorb"},
            {"name": "eye_counts", "type": "eye", "field": "signal", "mode": "absorb"},
        ],
        "seeds": [
            {"position": [x, y, 0], "type": "mass body"} for x in range(length) for y in range(LEG + 1)
        ]
        + [
            {"position": [0, 0, 0], "type": "source"},
            {"position": [0, LEG, 0], "type": "top"},
            {"position": [length - 1, 0, 0], "type": "eye"},
            {"position": [length - 1, LEG, 0], "type": "top"},
        ],
    }
    return raw


def observe(raw: dict) -> dict:
    world = Simulation(parse_initial_state(raw))
    names = [kind["name"] for kind in raw["disturbance_types"]]
    length = raw["shape"][0]
    i_light, i_signal = SPATIAL.index("light"), SPATIAL.index("signal")
    f_clock, f_signal = FIELDS.index("clock"), FIELDS.index("signal")
    # Residency of light rays: (column, y) -> list of ticks a light ray is resident there.
    resident: dict[tuple[int, int], list[int]] = {}
    # Signal rays: (x) -> first tick seen, per signal ray identity we cannot label; record
    # every (tick, x) residency instead and derive arrivals at the eye from its stock.
    signal_at_x1: list[int] = []  # ticks a signal ray is resident one link past the source
    eye_series: list[tuple[int, int, int]] = []  # (tick, eye counter, signals absorbed)
    source_counter: list[tuple[int, int]] = []
    loads: list[tuple[int, int]] = []  # (tick, computation stock at the eye's Node)
    lost_light: list[int] = []
    t0 = time.time()
    for tick in range(1, raw["ticks"] + 1):
        world.step()
        view = world.inventory_view()
        light_rays = 0
        for node in view.nodes:
            x, y, _ = node.position
            if node.rays:
                for ray in node.rays[i_light]:
                    resident.setdefault((x, y), []).append(tick)
                    light_rays += ray.amount
                if x == 1 and y == 0:
                    for _ray in node.rays[i_signal]:
                        signal_at_x1.append(tick)
            for record in node.records:
                if record is None:
                    continue
                kind = names[record.type_index]
                if kind == "eye":
                    eye_series.append(
                        (tick, unpack(record.values[f_clock])[0], unpack(record.values[f_signal])[0])
                    )
                elif kind == "source":
                    source_counter.append((tick, unpack(record.values[f_clock])[0]))
            if (x, y) == (length - 1, 0):
                loads.append((tick, world.spatial_values((x, y, 0))["computation"]["value"][0]))
        # Rays in flight are packets; count them too so that a lost ray is detected.
        for packet in view.packets:
            if packet.rays:
                light_rays += sum(r.amount for r in packet.rays[i_light])
        totals = world.totals()
        if totals["light"][0] != 2:
            lost_light.append(tick)
    return {
        "resident": {f"{x},{y}": ticks for (x, y), ticks in resident.items()},
        "signal_at_x1": signal_at_x1,
        "eye": eye_series,
        "source_counter": source_counter,
        "loads": loads,
        "light_total_ok": not lost_light,
        "first_light_loss_tick": lost_light[0] if lost_light else None,
        "signal_total": world.totals()["signal"][0],
        "host_seconds": round(time.time() - t0, 1),
    }


def arrivals(ticks: list[int]) -> list[int]:
    """Start tick of every residency run in a sorted tick list."""
    out = []
    prev = None
    for t in ticks:
        if prev is None or t != prev + 1:
            out.append(t)
        prev = t
    return out


def fit_loglog(points: list[tuple[float, float]]) -> tuple[float, float, int]:
    xs = [math.log(x) for x, _ in points]
    ys = [math.log(y) for _, y in points]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return float("nan"), float("nan"), n
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True)) / sxx
    resid = [y - (my + slope * (x - mx)) for x, y in zip(xs, ys, strict=True)]
    se = math.sqrt(sum(r * r for r in resid) / max(1, n - 2) / sxx)
    return slope, se, n


def analyse(raw: dict, seen: dict) -> dict:
    length = raw["shape"][0]
    budget = raw["normal_budget"]
    loads = dict(seen["loads"])

    def k_at(tick: int) -> int:
        # hop time in force: ceil(load / budget) with the load read at the eye's column
        load = loads.get(tick, loads[max(loads)])
        return max(1, -(-load // budget))

    result: dict = {
        "length": length,
        "emission": raw["emissions"][0]["amount"],
        "baseline": raw["spatial_fields"][0]["baseline"],
        "budget": budget,
        "ticks": raw["ticks"],
        "direction": raw.get("delay_direction", "none"),
    }
    clocks = {}
    for name, col in (("source", 0), ("eye", length - 1)):
        bottom = arrivals(seen["resident"].get(f"{col},0", []))
        periods = [b - a for a, b in zip(bottom, bottom[1:], strict=False)]
        # Pair each period with the hop time in force at its midpoint.
        pairs = [(k_at((a + b) // 2), b - a) for a, b in zip(bottom, bottom[1:], strict=False)]
        fit = fit_loglog([(k, p) for k, p in pairs if k > 0 and p > 0]) if len(pairs) > 2 else None
        # Also the overhead model P = 2 LEG k + c: least squares for c with slope fixed at 2 LEG.
        c = sum(p - 2 * LEG * k for k, p in pairs) / len(pairs) if pairs else None
        clocks[name] = {
            "arrivals_at_bottom_mirror": bottom,
            "periods": periods,
            "k_at_each_period": [k for k, _ in pairs],
            "loglog_slope_P_vs_k": None if fit is None or fit[0] != fit[0] else round(fit[0], 4),
            "loglog_slope_se": None if fit is None or fit[1] != fit[1] else round(fit[1], 4),
            "n_periods": len(periods),
            "k_range": [min(k for k, _ in pairs), max(k for k, _ in pairs)] if pairs else None,
            "mirror_overhead_c_in_P_eq_8k_plus_c": None if c is None else round(c, 3),
        }
    result["clocks"] = clocks
    # Signals: emission ticks (residency one link past the source) and absorption ticks.
    emitted = arrivals(seen["signal_at_x1"])
    eye = seen["eye"]
    absorbed = [t for (t, _, s), (_, _, s0) in zip(eye[1:], eye, strict=False) if s != s0]
    counter_at = {t: c for t, c, _ in eye}
    result["signals"] = {
        "emitted_ticks_seen_at_x1": emitted,
        "absorbed_ticks": absorbed,
        "eye_counter_at_absorption": [counter_at[t] for t in absorbed],
        "eye_counter_equals_ticks": all(counter_at[t] == t for t in absorbed),
        "signal_total_conserved": seen["signal_total"] == raw["ticks"],
    }
    gaps_e = [b - a for a, b in zip(emitted, emitted[1:], strict=False)]
    gaps_o = [b - a for a, b in zip(absorbed, absorbed[1:], strict=False)]
    n = min(len(gaps_e), len(gaps_o))
    if n >= 2:
        # Stretch read by the bare counter: absorbed gap over the emitted gap of the same
        # pair of signals (the i-th and (i+1)-th signal), on the eye's counter.
        clock_gaps_o = [
            counter_at[b] - counter_at[a] for a, b in zip(absorbed, absorbed[1:], strict=False)
        ]
        z_counter = [co / ge - 1 for co, ge in zip(clock_gaps_o[:n], gaps_e[:n], strict=True)]
        # Stretch read by the eye's light clock: the absorbed gap in units of the eye
        # clock's period in force at that time, over the emitted gap in units of the source
        # clock's period at emission (which is 1 by construction: one signal per period).
        eye_bottom = clocks["eye"]["arrivals_at_bottom_mirror"]

        def cycles_between(t0: int, t1: int) -> float:
            # fractional light-clock cycles of the eye between two ticks
            def phase(t: int) -> float:
                i = (
                    max(j for j, a in enumerate(eye_bottom) if a <= t)
                    if any(a <= t for a in eye_bottom)
                    else 0
                )
                a = eye_bottom[i]
                b = eye_bottom[i + 1] if i + 1 < len(eye_bottom) else a + (a - eye_bottom[i - 1])
                return i + (t - a) / (b - a)

            return phase(t1) - phase(t0)

        z_light = [
            cycles_between(a, b) - 1
            for a, b in zip(absorbed[: n + 1], absorbed[1 : n + 1], strict=False)
        ]
        result["redshift"] = {
            "pairs": n,
            "emitted_gaps_ticks": gaps_e[:n],
            "absorbed_gaps_ticks": gaps_o[:n],
            "z_by_bare_counter": [round(z, 4) for z in z_counter],
            "z_by_bare_counter_mean": round(sum(z_counter) / n, 4),
            "z_by_bare_counter_sd": round(
                math.sqrt(sum((z - sum(z_counter) / n) ** 2 for z in z_counter) / max(1, n - 1)), 4
            ),
            "z_by_light_clock": [round(z, 4) for z in z_light],
            "z_by_light_clock_mean": round(sum(z_light) / len(z_light), 4),
            "z_by_light_clock_sd": round(
                math.sqrt(
                    sum((z - sum(z_light) / len(z_light)) ** 2 for z in z_light)
                    / max(1, len(z_light) - 1)
                ),
                4,
            ),
        }
    result["light_conserved_throughout"] = seen["light_total_ok"]
    result["first_light_loss_tick"] = seen["first_light_loss_tick"]
    result["host_seconds"] = seen["host_seconds"]
    result["load_at_eye_column_checkpoints"] = seen["loads"][:: max(1, len(seen["loads"]) // 8)]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--length", type=int, default=32)
    parser.add_argument("--emission", type=int, default=16)
    parser.add_argument("--budget", type=int, default=1000)
    parser.add_argument("--baseline", type=int, default=3000)
    parser.add_argument("--ticks", type=int, default=4000)
    parser.add_argument("--direction", default="along", choices=["along", "none"])
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    raw = document(args.length, args.emission, args.budget, args.baseline, args.ticks, args.direction)
    (args.output / "initialization.json").write_text(json.dumps(raw, indent=1))
    seen = observe(raw)
    (args.output / "raw_observation.json").write_text(json.dumps(seen))
    result = analyse(raw, seen)
    result["source_sha256"] = source_fingerprint()
    (args.output / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    (args.output / "raw_observation.json").write_text(json.dumps(seen))
    for name, clock in result["clocks"].items():
        print(
            f"{name} clock: {clock['n_periods']} periods, k {clock['k_range']}, "
            f"P vs k slope {clock['loglog_slope_P_vs_k']} +/- {clock['loglog_slope_se']}, "
            f"overhead c {clock['mirror_overhead_c_in_P_eq_8k_plus_c']}; first periods {clock['periods'][:6]}"
        )
    print(
        "signals emitted",
        len(result["signals"]["emitted_ticks_seen_at_x1"]),
        "absorbed",
        len(result["signals"]["absorbed_ticks"]),
        "counter=ticks",
        result["signals"]["eye_counter_equals_ticks"],
    )
    if "redshift" in result:
        r = result["redshift"]
        print(
            f"z by bare counter {r['z_by_bare_counter_mean']} +/- {r['z_by_bare_counter_sd']} (n={r['pairs']}); "
            f"z by light clock {r['z_by_light_clock_mean']} +/- {r['z_by_light_clock_sd']}"
        )
    print("light conserved", result["light_conserved_throughout"], "host s", result["host_seconds"])


if __name__ == "__main__":
    main()
