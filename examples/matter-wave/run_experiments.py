"""A particle in flight dissolves into a matter wave and lands on a screen as a fringe.

Configuration only, on rules that already exist. A particle record of matter M
and momentum p moves along its heading at an eighth of a link per tick. Its funded
emission carries the engine's `dissolve` schedule: nothing for four cycles,
then its initial matter over sixteen cycles as Kerengonen rays over a forward
cone, each ray advancing `|p| / 4` phase steps per link. The particle keeps
flying while it holds matter and stops when it is empty. Sixteen ticks is
longer than any path difference to the screen, so the two slits' contributions
overlap at every screen Node; a one-tick pulse would meet itself only where
the paths are equal. The
wave meets an absorbing wall with two Huygens slits and a screen twelve links
beyond, exactly as in the de Broglie probe. What the screen collects is the
matter of one particle, spread as its wave; the fringe period must follow the
momentum the particle had. Every number is a read-only world/event audit at
host lattice coordinates; no mass, constant or wavelength unit is identified.
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
START_X = CENTER - 15
WALL_X = CENTER - 4
SCREEN_X = CENTER + 8
SLIT_HALF = 6
SCREEN_HALF = 12
PHASE_STEPS = 64
ADVANCE_DENOMINATOR = 4
MOMENTA = (32, 64)
HEADINGS = 256
HEADING_SCALE = 64
PER_RAY = 4096  # a single particle of 479,232 quanta: enough that each slit re-emits over every heading every tick
DISSOLVE_TICK = 4  # the particle flies two links before its train starts
TRAIN_TICKS = (
    16  # it pays out its matter over sixteen ticks: a wave train longer than any path difference
)
SPEED_NUMERATOR = 8  # hops per tick = 8 / 64 while it holds matter, then 0: it stays far from the wall
SPEED_DENOMINATOR = 64
TICKS = 84
COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}


def cone_headings(count: int, scale: int) -> list[list[int]]:
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
    dissolve_tick: int = DISSOLVE_TICK,
) -> dict:
    count = len(headings)
    matter = PER_RAY * count
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
    # The engine's dissolution schedule: nothing for dissolve_tick cycles, then the
    # initial matter over TRAIN_TICKS cycles, never more than is left.
    dissolve: dict = {
        "type": "particle",
        "field": "matter",
        "dissolve": {"after_ticks": dissolve_tick, "over_ticks": TRAIN_TICKS},
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
        dissolve["kerengonen_advance"] = {"amount": wavenumber, "denominator": ADVANCE_DENOMINATOR}
        slit_emission["kerengonen_phase"] = "carried"
    body = {
        "fields": ["matter", "momentum"],
        "defaults": {"matter": 0, "momentum": [0, 0, 0]},
        "transport": {"mode": "hold"},
    }
    return {
        "schema_version": 1,
        "model_id": "matter-wave-particle-in-flight-probe-v1",
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
            {
                "name": "heading",
                "components": 3,
                "units": "direction",
                "signed": True,
                "conserved": False,
                "extensive": False,
            },
        ],
        "disturbance_types": [
            {
                "name": "particle",
                "fields": ["matter", "momentum", "heading", "wavenumber"],
                "defaults": {
                    "matter": matter,
                    "momentum": [momentum, 0, 0],
                    "heading": [1, 0, 0],
                    "wavenumber": momentum,
                },
                "transport": {
                    "mode": "move",
                    "direction_field": "heading",
                    "rate": {
                        "op": "mul",
                        "args": [SPEED_NUMERATOR, {"op": "gt", "args": [{"field": "matter"}, 0]}],
                    },
                    "rate_denominator": SPEED_DENOMINATOR,
                },
            },
            {"name": "wall", **body},
            {"name": "slit", **body},
            {"name": "screen", **body},
        ],
        "spatial_fields": [field],
        "emissions": [dissolve, slit_emission],
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
        "seeds": [{"position": [START_X, CENTER, 1], "type": "particle"}]
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
    names = [kind["name"] for kind in raw["disturbance_types"]]
    path = []
    for tick in range(1, raw["ticks"] + 1):
        world.step()
        for position, node in world.nodes.items():
            for record in node.records:
                if record is not None and names[record.type_index] == "particle":
                    values = world.record_values(record)
                    path.append(
                        {
                            "tick": tick,
                            "x": position[0] - CENTER,
                            "matter": values["matter"][0],
                            "momentum": list(values["momentum"]),
                        }
                    )
    totals, escaped = world.totals(), world.escaped_totals()
    profile: dict[int, int] = {}
    for position, node in world.nodes.items():
        for record in node.records:
            if record is not None and names[record.type_index] == "screen":
                profile[position[1] - CENTER] = world.record_values(record)["matter"][0]
    return {
        "profile": dict(sorted(profile.items())),
        "absorbed_total": sum(profile.values()),
        "particle_path": path[::2],
        "husk": path[-1] if path else None,
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
                "two_slits": two["profile"].get(y, 0),
                "sum_of_single_slits": incoherent,
                "plain": plain["profile"].get(y, 0),
                "ratio": round(two["profile"].get(y, 0) / incoherent, 3) if incoherent else None,
            }
        )
    inner = [row for row in rows if 0 < row["y"] <= SLIT_HALF and row["ratio"] is not None]
    return {
        "momentum": momentum,
        "advance": advance,
        "predicted_first_dark": PHASE_STEPS // 2 // (2 * advance),
        "measured_first_dark": min(inner, key=lambda row: row["ratio"])["y"] if inner else None,
        "plain_equals_sum": all(row["plain"] == row["sum_of_single_slits"] for row in rows),
        "closed": all(w["matter_closed"] for w in (two, a, b, plain)),
        "particle_path": two["particle_path"],
        "husk": two["husk"],
        "absorbed": {"two_slits": two["absorbed_total"], "plain": plain["absorbed_total"]},
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
        "matter": PER_RAY * len(headings),
        "dissolve_tick": DISSOLVE_TICK,
        "fringes": results,
    }
    (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    for result in results:
        print(
            "momentum",
            result["momentum"],
            "first dark predicted",
            result["predicted_first_dark"],
            "measured",
            result["measured_first_dark"],
            "plain = sum",
            result["plain_equals_sum"],
            "closed",
            result["closed"],
            "husk",
            result["husk"],
        )
        print("  path", result["particle_path"][:4])
        print("  ratios", [(row["y"], row["ratio"]) for row in result["rows"] if abs(row["y"]) <= 6])
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
