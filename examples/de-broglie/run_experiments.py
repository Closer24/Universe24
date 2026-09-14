"""De Broglie on matter rays: a beam's fringe spacing must shrink as its momentum grows.

A held beam source of momentum p emits rays on a Kerengonen field of 64 phase
steps whose advance per link is `|p| / 4`, its own de Broglie rule. An
absorbing wall with two re-emitting slits at y = -6 and y = +6 stands eight
links downstream, the screen twelve links beyond it. On this lattice the path
difference between the slits and a screen Node at offset y is `2 y` links for
`|y| <= 6`, so the phase difference is `2 y x advance` steps and the first
dark fringe sits at `y = 16 / advance`: 4, 2 and 1 for momenta 16, 32 and 64.
Each momentum is also run with one slit at a time and on the plain field, so
the fringe is read as the two-slit profile over the sum of the single slits.
Every number is a read-only world/event audit at host lattice coordinates; no
mass, constant or wavelength unit is identified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

SIZE = 31
CENTER = SIZE // 2
SOURCE_X = CENTER - 13
WALL_X = CENTER - 4
SCREEN_X = CENTER + 8
SLIT_HALF = 6
SCREEN_HALF = 12
PHASE_STEPS = 64
ADVANCE_DENOMINATOR = 4
MOMENTA = (16, 32, 64)
HEADINGS = 256
HEADING_SCALE = 64
PER_RAY = 64
TICKS = 64
COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}


def cone_headings(count: int, scale: int) -> list[list[int]]:
    """Distinct integer headings within 45 degrees of +x, in the wall plane."""
    result: list[list[int]] = []
    for i in range(count):
        angle = -math.pi / 4 + math.pi / 2 * (i + 0.5) / count
        heading = [round(scale * math.cos(angle)), round(scale * math.sin(angle)), 0]
        if heading[0] > 0 and heading not in result:
            result.append(heading)
    return result


def document(
    momentum: int,
    headings: list[list[int]],
    ticks: int = TICKS,
    slits: tuple[int, ...] = (-SLIT_HALF, SLIT_HALF),
    phased: bool = True,
) -> dict:
    count = len(headings)
    field: dict = {
        "field": "matter",
        "baseline": 0,
        "transport": "ray",
        "headings": headings,
        "rays_per_tick": count,
        "ray_slots": 2048,
    }
    if phased:
        field["kerengonen"] = {"phase_steps": PHASE_STEPS, "phase_advance": 0}
    # The de Broglie advance reads the momentum the emitter set out with; the
    # momentum field itself takes the recoil of every emitted ray.
    wavenumber = {"field": "wavenumber"}
    beam_emission: dict = {
        "type": "beam",
        "field": "matter",
        "amount": PER_RAY * count,
        "denominator": 1,
        "source": False,
        "recoil_field": "momentum",
    }
    slit_emission: dict = {
        "type": "slit",
        "field": "matter",
        "amount": {"field": "matter"},
        "denominator": 1,
        "source": False,
        "recoil_field": "momentum",
    }
    if phased:
        beam_emission["kerengonen_advance"] = {"amount": wavenumber, "denominator": ADVANCE_DENOMINATOR}
        slit_emission["kerengonen_phase"] = "carried"
    body = {
        "fields": ["matter", "momentum"],
        "defaults": {"matter": 0, "momentum": [0, 0, 0]},
        "transport": {"mode": "hold"},
    }
    return {
        "schema_version": 1,
        "model_id": "de-broglie-matter-ray-probe-v1",
        "shape": [SIZE, SIZE, 3],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": COSTS,
        "fields": [
            {
                "name": "matter",
                "components": 1,
                "units": "matter quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "matter quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "wavenumber",
                "components": 1,
                "units": "matter quantum times heading",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
        ],
        "disturbance_types": [
            {
                "name": "beam",
                "fields": ["matter", "momentum", "wavenumber"],
                "defaults": {
                    "matter": PER_RAY * count * ticks,
                    "momentum": [momentum, 0, 0],
                    "wavenumber": momentum,
                },
                "transport": {"mode": "hold"},
            },
            {"name": "wall", **body},
            {"name": "slit", **body},
            {"name": "screen", **body},
        ],
        "spatial_fields": [field],
        "emissions": [beam_emission, slit_emission],
        "spatial_couplings": [
            {
                "name": f"{name}_absorbs",
                "type": name,
                "field": "matter",
                "mode": "absorb",
                "momentum_field": "momentum",
            }
            for name in ("wall", "slit", "screen")
        ],
        "seeds": [{"position": [SOURCE_X, CENTER, 1], "type": "beam"}]
        + [
            {"position": [WALL_X, CENTER + y, 1], "type": "slit" if y in slits else "wall"}
            for y in range(-(SIZE // 2), SIZE // 2 + 1)
        ]
        + [
            {"position": [SCREEN_X, CENTER + y, 1], "type": "screen"}
            for y in range(-SCREEN_HALF, SCREEN_HALF + 1)
        ],
    }


def run(raw: dict) -> dict:
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["matter"][0]
    for _ in range(raw["ticks"]):
        world.step()
    totals, escaped = world.totals(), world.escaped_totals()
    names = [kind["name"] for kind in raw["disturbance_types"]]
    profile: dict[int, int] = {}
    for position, node in world.nodes.items():
        for record in node.records:
            if record is not None and names[record.type_index] == "screen":
                profile[position[1] - CENTER] = world.record_values(record)["matter"][0]
    return {
        "profile": dict(sorted(profile.items())),
        "absorbed_total": sum(profile.values()),
        "matter_closed": totals["matter"][0] + escaped["matter"][0] == initial,
    }


def fringe(momentum: int, headings: list[list[int]]) -> dict:
    two = run(document(momentum, headings))
    a = run(document(momentum, headings, slits=(-SLIT_HALF,)))
    b = run(document(momentum, headings, slits=(SLIT_HALF,)))
    plain = run(document(momentum, headings, phased=False))
    advance = momentum // ADVANCE_DENOMINATOR
    rows = []
    for y in range(-SCREEN_HALF, SCREEN_HALF + 1):
        incoherent = a["profile"].get(y, 0) + b["profile"].get(y, 0)
        rows.append(
            {
                "y": y,
                "phase_difference": (2 * min(abs(y), SLIT_HALF) * advance) % PHASE_STEPS,
                "two_slits": two["profile"].get(y, 0),
                "sum_of_single_slits": incoherent,
                "plain": plain["profile"].get(y, 0),
                "ratio": round(two["profile"].get(y, 0) / incoherent, 3) if incoherent else None,
            }
        )
    inner = [row for row in rows if 0 < row["y"] <= SLIT_HALF and row["ratio"] is not None]
    first_dark = min(inner, key=lambda row: row["ratio"])["y"] if inner else None
    return {
        "momentum": momentum,
        "advance": advance,
        "predicted_first_dark": PHASE_STEPS // 2 // (2 * advance) if advance else None,
        "measured_first_dark": first_dark,
        "plain_equals_sum": all(row["plain"] == row["sum_of_single_slits"] for row in rows),
        "closed": two["matter_closed"]
        and a["matter_closed"]
        and b["matter_closed"]
        and plain["matter_closed"],
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    headings = cone_headings(HEADINGS, HEADING_SCALE)
    results = [fringe(momentum, headings) for momentum in MOMENTA]
    report = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only world/event audit",
        "headings": len(headings),
        "phase_steps": PHASE_STEPS,
        "advance_denominator": ADVANCE_DENOMINATOR,
        "ticks": TICKS,
        "fringes": results,
    }
    (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    for result in results:
        print(
            "momentum",
            result["momentum"],
            "advance",
            result["advance"],
            "first dark predicted",
            result["predicted_first_dark"],
            "measured",
            result["measured_first_dark"],
            "plain = sum",
            result["plain_equals_sum"],
            "closed",
            result["closed"],
        )
        print("  ratios", [(row["y"], row["ratio"]) for row in result["rows"] if abs(row["y"]) <= 8])
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
