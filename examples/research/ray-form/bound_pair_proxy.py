"""PROXY for HYPOTHESES 8 'the first thing to check': can a pair of counter-heading rays stay bound?

The engine has no rule by which two rays reflect each other at a Node (rays only
merge, are absorbed by records, gathered by claims, or answered by the bond
registry). The closest legal configuration is a cavity: two MIRROR RECORDS
(transport hold, absorb + kerengonen_mirror re-emission) facing each other, one
8-quantum Kerengonen ray bouncing each way. The pair is therefore bound by a
configured record rule, and every reflection passes through a record for one
tick. Everything measured here is a read-only inventory audit.

Run:  PYTHONPATH=src python examples/research/ray-form/bound_pair_proxy.py --output DIR [--ticks 600]

Geometries: 'adjacent' (mirrors at x=0 and x=1, d=1) and 'cavity' (mirrors at
x=0 and x=2, lamp at x=1, d=2; the center Node has no absorber, so a load there
delays the rays under `ray_delay`). Loads: none, fixed k via the computation
baseline, and the redshift_sweep growing profile (baseline 7000, emission 16,
budget 1000). Negative control: same rays, no mirrors, open row.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS, unpack
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

P = 64  # phase steps
A = 4  # advance per link
PARCEL = 8  # quanta per ray
BUDGET = 1000
TICKS = 600
ROW = 8  # periodic row length for the bound runs
OPEN_ROW = 65  # open row for the negative control


def document(
    geometry: str,
    *,
    mirrors: bool = True,
    computation: bool = False,
    baseline: int = 0,
    emission: int = 0,
    phase_per_tick: bool = False,
    delay_direction: str | None = "along",
    ticks: int = TICKS,
) -> dict:
    boundary = "periodic" if mirrors else "open"
    length = ROW if mirrors else OPEN_ROW
    origin = 0 if mirrors else OPEN_ROW // 2
    if geometry == "adjacent":
        left, right = origin, origin + 1
        lamps = [
            {"position": [left, 0, 0], "type": "lamp_r"},
            {"position": [right, 0, 0], "type": "lamp_l"},
        ]
    elif geometry == "cavity":
        left, right = origin, origin + 2
        lamps = [{"position": [origin + 1, 0, 0], "type": "lamp_c"}]
    else:
        raise ValueError(geometry)
    fields = [
        {
            "name": "quanta",
            "components": 1,
            "units": "quantum",
            "signed": False,
            "conserved": True,
            "extensive": True,
        },
        {
            "name": "momentum",
            "components": 3,
            "units": "quantum times heading",
            "signed": True,
            "conserved": True,
            "extensive": True,
        },
    ]
    types = [
        {
            "name": "lamp_r",
            "fields": ["quanta", "momentum"],
            "defaults": {"quanta": PARCEL, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        },
        {
            "name": "lamp_l",
            "fields": ["quanta", "momentum"],
            "defaults": {"quanta": PARCEL, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        },
        {
            "name": "lamp_c",
            "fields": ["quanta", "momentum"],
            "defaults": {"quanta": 2 * PARCEL, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        },
        {
            "name": "mirror",
            "fields": ["quanta", "momentum"],
            "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        },
    ]
    emissions = [
        {
            "type": "lamp_r",
            "field": "quanta",
            "amount": PARCEL,
            "denominator": 1,
            "source": False,
            "recoil_field": "momentum",
            "heading": [1, 0, 0],
        },
        {
            "type": "lamp_l",
            "field": "quanta",
            "amount": PARCEL,
            "denominator": 1,
            "source": False,
            "recoil_field": "momentum",
            "heading": [-1, 0, 0],
        },
        {
            "type": "lamp_c",
            "field": "quanta",
            "amount": 2 * PARCEL,
            "denominator": 1,
            "source": False,
            "recoil_field": "momentum",
        },
    ]
    couplings = []
    seeds = list(lamps)
    if mirrors:
        emissions.append(
            {
                "type": "mirror",
                "field": "quanta",
                "amount": {"field": "quanta"},
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": "carried",
                "kerengonen_mirror": "x",
            }
        )
        couplings.append(
            {
                "name": "mirror_absorbs",
                "type": "mirror",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
            }
        )
        seeds += [
            {"position": [left, 0, 0], "type": "mirror"},
            {"position": [right, 0, 0], "type": "mirror"},
        ]
    spatial_fields = [
        {
            "field": "quanta",
            "baseline": 0,
            "transport": "ray",
            "headings": [[1, 0, 0], [-1, 0, 0]],
            "rays_per_tick": 2,
            "ray_slots": 16,
            "kerengonen": {"phase_steps": P, "phase_advance": A},
        },
    ]
    raw = {
        "schema_version": 1,
        "model_id": "bound-pair-proxy-cavity-v1",
        "boundary": boundary,
        "shape": [length, 1, 1],
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": BUDGET,
        "ticks": ticks,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": fields,
        "disturbance_types": types,
        "spatial_fields": spatial_fields,
        "emissions": emissions,
        "spatial_couplings": couplings,
        "seeds": seeds,
    }
    if computation:
        fields.append(
            {"name": "mass", "components": 1, "units": "unit", "signed": False, "conserved": True}
        )
        fields.append(
            {
                "name": "computation",
                "components": 1,
                "units": "load unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            }
        )
        types.append(
            {
                "name": "mass body",
                "fields": ["mass"],
                "defaults": {"mass": 1},
                "transport": {"mode": "hold"},
            }
        )
        spatial_fields.append({"field": "computation", "baseline": baseline, "transport": "outward"})
        if emission:
            emissions.append(
                {
                    "type": "mass body",
                    "field": "computation",
                    "amount": emission,
                    "denominator": 1,
                    "source": True,
                }
            )
            seeds += [{"position": [x, 0, 0], "type": "mass body"} for x in range(length)]
        raw["computation_field"] = "computation"
        raw["ray_delay"] = True
        raw["ray_phase_per_tick"] = phase_per_tick
        if delay_direction is not None:
            raw["delay_direction"] = delay_direction
    return raw


def observe(world: Simulation, raw: dict) -> dict:
    """Located parcels (resident rays or mirror stock), their phases, and the load per Node."""
    type_index = {t["name"]: i for i, t in enumerate(raw["disturbance_types"])}
    mirror = type_index["mirror"]
    comp_index = next(
        (i for i, f in enumerate(raw["spatial_fields"]) if f["field"] == "computation"), None
    )
    parcels = []  # (x, kind, phase, amount)
    loads = {}
    for node in world.inventory_view().nodes:
        x = node.position[0]
        for ray in node.rays[0] if node.rays else ():
            parcels.append((x, "ray", ray.phase, ray.amount, ray.heading))
        for record in node.records:
            if record is not None and record.type_index == mirror:
                stock = world.record_values(record)["quanta"][0]
                if stock:
                    phase = unpack(record.absorbed_phases[0])[0] if record.absorbed_phases else None
                    parcels.append((x, "mirror", phase, stock, None))
        if comp_index is not None and node.spatial:
            loads[x] = sum(unpack(p)[0] for p in node.spatial[comp_index].populations)
    return {"parcels": parcels, "loads": loads}


def k_of(load: int) -> int:
    return max(1, -(-load // BUDGET))


def run(raw: dict, label: str, d: int, mirrors: bool) -> dict:
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["quanta"][0]
    baseline = next((f["baseline"] for f in raw["spatial_fields"] if f["field"] == "computation"), None)
    phase_track: list[int] = []  # unwrapped cumulative phase of the parcels
    tick_of_phase: list[int] = []
    max_sep = 0
    separations: list[tuple[int, int]] = []  # (tick, separation) for the negative control
    center_k: list[tuple[int, int]] = []  # (tick, k at the center Node) from the load
    symmetric = True
    both_visible = 0
    last_phase = None
    cumulative = 0
    center_x = (0 if mirrors else OPEN_ROW // 2) + 1
    started = time.perf_counter()
    for tick in range(1, raw["ticks"] + 1):
        world.step()
        obs = observe(world, raw)
        parcels = obs["parcels"]
        xs = [x for x, _, _, amount, _ in parcels for _ in range(1) if amount]
        if len(parcels) >= 2:
            both_visible += 1
            sep = max(xs) - min(xs)
            max_sep = max(max_sep, sep)
            separations.append((tick, sep))
        phases = sorted({ph for _, _, ph, amount, _ in parcels if ph is not None and amount})
        if len(phases) > 1:
            symmetric = False
        if phases:
            ph = phases[0]
            if last_phase is None:
                cumulative = ph
            else:
                delta = (ph - last_phase) % P
                if delta > 3 * A:
                    raise RuntimeError(
                        f"{label}: phase jump {delta} at tick {tick} breaks the unwrap rule"
                    )
                cumulative += delta
            last_phase = ph
            phase_track.append(cumulative)
            tick_of_phase.append(tick)
        if baseline is not None:
            center_k.append((tick, k_of(baseline + obs["loads"].get(center_x, 0))))
    wall = time.perf_counter() - started
    totals, escaped = world.totals(), world.escaped_totals()
    closed = totals["quanta"][0] + escaped["quanta"][0] == initial
    result = {
        "label": label,
        "d": d,
        "ticks": raw["ticks"],
        "wall_seconds": round(wall, 2),
        "observations_with_both_parcels": both_visible,
        "max_separation": max_sep,
        "bound": mirrors and max_sep <= d and both_visible == raw["ticks"],
        "phases_symmetric": symmetric,
        "quanta_closed": closed,
        "quanta_in_world": totals["quanta"][0],
        "quanta_escaped": escaped["quanta"][0],
    }
    if len(phase_track) >= 2:
        # Clock rate over the whole run (after the first observation) and per phase cycle.
        dphi = phase_track[-1] - phase_track[0]
        dt = tick_of_phase[-1] - tick_of_phase[0]
        result["phase_steps_advanced"] = dphi
        result["ticks_spanned"] = dt
        result["ticks_per_cycle"] = round(P * dt / dphi, 3) if dphi else None
        result["cycles_per_tick"] = round(dphi / (P * dt), 5) if dt else None
        # Per-cycle table: tick at which each multiple of P is first reached.
        cycles = []
        target = phase_track[0] + P
        last_tick = tick_of_phase[0]
        for phi, t in zip(phase_track, tick_of_phase, strict=False):
            if phi >= target:
                k_here = next((k for tk, k in reversed(center_k) if tk <= t), None)
                cycles.append({"cycle_end_tick": t, "ticks": t - last_tick, "k_center": k_here})
                last_tick = t
                target += P
        result["cycles"] = cycles
        result["cycle_count"] = len(cycles)
        if cycles:
            ts = [c["ticks"] for c in cycles]
            mean = sum(ts) / len(ts)
            var = sum((t - mean) ** 2 for t in ts) / max(1, len(ts) - 1)
            result["ticks_per_cycle_mean"] = round(mean, 3)
            result["ticks_per_cycle_sd"] = round(var**0.5, 3)
            result["ticks_per_cycle_sem"] = round((var / len(ts)) ** 0.5, 3)
    if center_k:
        result["k_center_first"] = center_k[0][1]
        result["k_center_last"] = center_k[-1][1]
    if not mirrors:
        # Separation growth per tick while both parcels are resident.
        steps = [
            (t2 - t1, s2 - s1) for (t1, s1), (t2, s2) in zip(separations, separations[1:], strict=False)
        ]
        result["separation_trace"] = separations[:24]
        result["mean_links_per_tick"] = (
            round(sum(ds for _, ds in steps) / max(1, sum(dt for dt, _ in steps)), 4) if steps else None
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ticks", type=int, default=TICKS)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    loads = [
        ("no-field", dict(computation=False)),
        ("k1", dict(computation=True, baseline=0)),
        ("k2", dict(computation=True, baseline=BUDGET + 1)),
        ("k4", dict(computation=True, baseline=3 * BUDGET + 1)),
        ("k8", dict(computation=True, baseline=7 * BUDGET + 1)),
        ("growing", dict(computation=True, baseline=7000, emission=16)),
    ]
    results = []
    failures = []
    for geometry, d in (("adjacent", 1), ("cavity", 2)):
        for load_label, load in loads:
            for ppt in (False, True):
                if not load["computation"] and ppt:
                    continue
                label = f"{geometry}/{load_label}/ppt={ppt}"
                raw = document(geometry, phase_per_tick=ppt, ticks=args.ticks, **load)
                try:
                    results.append(run(raw, label, d, True))
                    r = results[-1]
                    print(
                        f"{label:34s} bound={r['bound']} maxsep={r['max_separation']} T/cycle={r.get('ticks_per_cycle_mean')}"
                        f" +-{r.get('ticks_per_cycle_sem')} (N={r.get('cycle_count')}) k={r.get('k_center_first')}->{r.get('k_center_last')}"
                        f" closed={r['quanta_closed']} sym={r['phases_symmetric']} {r['wall_seconds']}s"
                    )
                except Exception as error:  # report, do not hide
                    failures.append({"label": label, "error": f"{type(error).__name__}: {error}"})
                    print(f"{label:34s} FAILED {type(error).__name__}: {error}")
    # Negative controls: no mirrors, open row.
    for load_label, load in (
        ("no-field", dict(computation=False)),
        ("k4", dict(computation=True, baseline=3 * BUDGET + 1)),
    ):
        label = f"control-no-mirrors/cavity/{load_label}"
        raw = document("cavity", mirrors=False, ticks=min(args.ticks, 120), **load)
        try:
            results.append(run(raw, label, 2, False))
            r = results[-1]
            print(
                f"{label:34s} maxsep={r['max_separation']} links/tick={r['mean_links_per_tick']} escaped={r['quanta_escaped']} closed={r['quanta_closed']}"
            )
        except Exception as error:
            failures.append({"label": label, "error": f"{type(error).__name__}: {error}"})
            print(f"{label:34s} FAILED {type(error).__name__}: {error}")
    # Expected failure: isotropic delay with a loaded mirror Node.
    label = "cavity/k4/isotropic-delay (expected failure)"
    raw = document("cavity", computation=True, baseline=3 * BUDGET + 1, delay_direction=None, ticks=40)
    try:
        results.append(run(raw, label, 2, True))
        print(f"{label:34s} RAN (unexpected): {results[-1]}")
    except Exception as error:
        failures.append({"label": label, "error": f"{type(error).__name__}: {error}", "expected": True})
        print(f"{label:34s} failed as expected: {type(error).__name__}: {error}")
    report = {
        "source_sha256": source_fingerprint(),
        "python": sys.version,
        "phase_steps": P,
        "advance": A,
        "budget": BUDGET,
        "ticks": args.ticks,
        "results": results,
        "failures": failures,
    }
    (args.output / "summary.json").write_text(json.dumps(report, indent=1) + "\n")
    print("wrote", args.output / "summary.json")


if __name__ == "__main__":
    main()
