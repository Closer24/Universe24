"""Claim and gather: a wave that was captured at one Node arrives there whole, later.

A particle dissolves into a matter wave of rays slower than link speed. When a
record takes any of that train, it opens a claim: a flood of knowledge that
passes Node to Node at link speed, each Node remembering the port it came from
as the way home. Every free ray of the train that a claiming Node meets turns
homeward and follows those ports back; the claiming record takes it whole.
Where two claims for one train meet, the earlier capture wins and the later
root yields, keeping only the piece it took. Two probes: an isotropic wave in
the open, gathered by one screen and contested by two; and the double slit,
where a line of screen Nodes draws single-quantum lottery clicks and the first
click gathers the particle, over an ensemble of capture seeds, so the landing
position of a whole particle is compared with the fringe of its wave. Every
number is a read-only world/event audit at host lattice coordinates; no unit
or constant is identified.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

ROOT = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "matter_wave_probe", ROOT / "examples/matter-wave/run_experiments.py"
)
assert _SPEC is not None and _SPEC.loader is not None
MATTER_WAVE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(MATTER_WAVE)

SIZE = 25
CENTER = SIZE // 2
SCREEN_X = 6
RIVAL_X = -4
MATTER = 64
PACE = (1, 4)
GATHER_TICKS = 80
PLANAR_HEADINGS = [
    [1, 0, 0],
    [-1, 0, 0],
    [0, 1, 0],
    [0, -1, 0],
    [1, 1, 0],
    [-1, 1, 0],
    [1, -1, 0],
    [-1, -1, 0],
]
CLAIM_TICKS = 1000
CLAIM_SLOTS = 4
LANDING_PACE = (1, 2)
LANDING_TICKS = 220
CLICK_DENOMINATOR = 256
SEEDS = 48
MOMENTUM = 64
COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}


def gather_document(
    ticks: int = GATHER_TICKS, claim: bool = True, rival: bool = False, matter: int = MATTER
) -> dict:
    return {
        "schema_version": 1,
        "model_id": "claim-gather-isotropic-probe-v1",
        "shape": [SIZE, SIZE, 3],
        "boundary": "open",
        "slots_per_node": 1,
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
                "name": "train",
                "components": 1,
                "units": "label",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
        ],
        "disturbance_types": [
            {
                "name": "particle",
                "fields": ["matter", "momentum", "train"],
                "defaults": {"matter": matter, "momentum": [0, 0, 0], "train": 7},
                "transport": {"mode": "hold"},
            },
            {
                "name": "screen",
                "fields": ["matter", "momentum"],
                "defaults": {"matter": 0, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [
            {
                "field": "matter",
                "baseline": 0,
                "transport": "ray",
                "headings": PLANAR_HEADINGS,
                "rays_per_tick": len(PLANAR_HEADINGS),
                "ray_slots": 256,
                "pace": list(PACE),
                "claim": {"ticks": CLAIM_TICKS, "slots": CLAIM_SLOTS},
            }
        ],
        "emissions": [
            {
                "type": "particle",
                "field": "matter",
                "source": False,
                "recoil_field": "momentum",
                "dissolve": {"after_ticks": 2, "over_ticks": 8},
                "train_field": "train",
            }
        ],
        "spatial_couplings": [
            {
                "name": "screen_absorbs",
                "type": "screen",
                "field": "matter",
                "mode": "absorb",
                "momentum_field": "momentum",
                "claim": claim,
            }
        ],
        "seeds": [
            {"position": [CENTER, CENTER, 1], "type": "particle"},
            {"position": [CENTER + SCREEN_X, CENTER, 1], "type": "screen"},
        ]
        + ([{"position": [CENTER + RIVAL_X, CENTER, 1], "type": "screen"}] if rival else []),
    }


def gather(raw: dict) -> dict:
    """Per tick: matter free, homing, at each screen, and claims; then the outcome."""
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["matter"][0]
    names = [kind["name"] for kind in raw["disturbance_types"]]
    timeline = []
    closed = True
    for tick in range(1, raw["ticks"] + 1):
        world.step()
        view = world.inventory_view()
        screens: dict[int, int] = {}
        free = homing = claims = 0
        for node in view.nodes:
            for record in node.records:
                if record is not None and names[record.type_index] == "screen":
                    screens[node.position[0] - CENTER] = world.record_values(record)["matter"][0]
            claims += len(node.claims[0]) if node.claims else 0
            for ray in node.rays[0] if node.rays else ():
                if ray.homing:
                    homing += ray.amount
                else:
                    free += ray.amount
        escaped = world.escaped_totals()["matter"][0]
        closed = closed and world.totals()["matter"][0] + escaped == initial
        timeline.append(
            {
                "tick": tick,
                "free": free,
                "homing": homing,
                "claims": claims,
                "screens": screens,
                "escaped": escaped,
            }
        )
    view = world.inventory_view()
    roots = [
        {"position": [node.position[0] - CENTER, node.position[1] - CENTER], "since": claim.since}
        for node in view.nodes
        for claim in (node.claims[0] if node.claims else ())
        if claim.parent < 0
    ]
    momenta = {
        node.position[0] - CENTER: list(world.record_values(record)["momentum"])
        for node in view.nodes
        for record in node.records
        if record is not None and names[record.type_index] == "screen"
    }
    first_claim = next((row["tick"] for row in timeline if row["claims"]), None)
    gathered = [
        row["tick"]
        for row in timeline
        if first_claim is not None
        and row["tick"] > first_claim
        and row["free"] == 0
        and row["homing"] == 0
    ]
    return {
        "matter": initial,
        "screens": timeline[-1]["screens"],
        "screen_momenta": momenta,
        "roots": roots,
        "first_claim_tick": first_claim,
        "gathered_tick": gathered[0] if gathered else None,
        "nodes_claimed": timeline[-1]["claims"],
        "escaped": timeline[-1]["escaped"],
        "matter_closed": closed,
        "timeline": timeline[::4],
    }


def landing_document(
    seed: int, ticks: int = LANDING_TICKS, phased: bool = True, capture: bool = True
) -> dict:
    """The matter-wave double slit with claiming screen Nodes drawing lottery clicks.

    On the Euclidean metric so that the wave reaches the whole screen line at
    about the same tick; without capture the screen takes the coherent share and
    no claim, which reads the fringe of the same wave.
    """
    headings = MATTER_WAVE.cone_headings(MATTER_WAVE.HEADINGS, MATTER_WAVE.HEADING_SCALE)
    raw = MATTER_WAVE.document(MOMENTUM, headings, ticks=ticks, phased=phased)
    raw["model_id"] = "claim-gather-double-slit-landing-probe-v1"
    raw["sampling_profile"] = "historical-autonomous-v1"
    field = raw["spatial_fields"][0]
    field["metric"] = "euclidean"
    field["pace"] = list(LANDING_PACE)
    field["claim"] = {"ticks": CLAIM_TICKS, "slots": CLAIM_SLOTS}
    field["ray_slots"] = 4096
    if phased and capture:
        field["kerengonen"].update({"capture": "lottery", "capture_seed": seed})
    raw["fields"].append(
        {
            "name": "train",
            "components": 1,
            "units": "label",
            "signed": False,
            "conserved": False,
            "extensive": False,
        }
    )
    particle = raw["disturbance_types"][0]
    particle["fields"].append("train")
    particle["defaults"]["train"] = 1
    dissolve, slit_emission = raw["emissions"]
    dissolve["train_field"] = "train"
    if phased:
        # The phase advances once per tick; at half pace that is twice per link, so
        # the wavelength in links is kept by halving the advance.
        dissolve["kerengonen_advance"]["denominator"] = MATTER_WAVE.ADVANCE_DENOMINATOR * 2
    slit_emission["train_field"] = "carried"
    for rule in raw["spatial_couplings"]:
        if rule["type"] == "screen" and capture:
            rule.update({"claim": True, "fraction": 1, "fraction_denominator": CLICK_DENOMINATOR})
    return raw


def landing(raw: dict) -> dict:
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["matter"][0]
    names = [kind["name"] for kind in raw["disturbance_types"]]
    for _ in range(raw["ticks"]):
        world.step()
    view = world.inventory_view()
    screen: dict[int, int] = {}
    wall = 0
    for node in view.nodes:
        for record in node.records:
            if record is None:
                continue
            values = world.record_values(record)
            if names[record.type_index] == "screen":
                screen[node.position[1] - MATTER_WAVE.CENTER] = values["matter"][0]
            elif names[record.type_index] in ("wall", "slit"):
                wall += values["matter"][0]
    roots = [
        node.position[1] - MATTER_WAVE.CENTER
        for node in view.nodes
        for claim in (node.claims[0] if node.claims else ())
        if claim.parent < 0
    ]
    winner = max(screen, key=lambda y: screen[y]) if any(screen.values()) else None
    escaped = world.escaped_totals()["matter"][0]
    in_flight = sum(ray.amount for node in view.nodes for rays in node.rays for ray in rays)
    return {
        "winner": winner,
        "winner_matter": screen.get(winner, 0) if winner is not None else 0,
        "screen_total": sum(screen.values()),
        "other_screens": sum(screen.values()) - (screen.get(winner, 0) if winner is not None else 0),
        "wall": wall,
        "escaped": escaped,
        "in_flight": in_flight,
        "roots": roots,
        "matter_closed": world.totals()["matter"][0] + escaped == initial,
        "profile": dict(sorted(screen.items())),
    }


def ensemble(seeds: int = SEEDS) -> dict:
    runs = [landing(landing_document(seed)) for seed in range(1, seeds + 1)]
    histogram: dict[int, int] = {}
    for run in runs:
        if run["winner"] is not None:
            histogram[run["winner"]] = histogram.get(run["winner"], 0) + 1
    fringe = landing(landing_document(0, capture=False))
    return {
        "seeds": seeds,
        "landings": dict(sorted(histogram.items())),
        "landed": sum(histogram.values()),
        "winner_share": [
            round(run["winner_matter"] / run["screen_total"], 3) for run in runs if run["screen_total"]
        ],
        "closed": all(run["matter_closed"] for run in runs),
        "wave_fringe": fringe["profile"],
        "wave_reached_screen": fringe["screen_total"],
        "runs": runs,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, default=SEEDS)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    gathered = gather(gather_document())
    free = gather(gather_document(claim=False))
    contested = gather(gather_document(rival=True))
    landings = ensemble(args.seeds)
    report = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only world/event audit",
        "gathered": gathered,
        "without_claim": free,
        "contested": contested,
        "landings": landings,
    }
    (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    for name, result in (("gathered", gathered), ("without claim", free), ("contested", contested)):
        print(
            name,
            "screens",
            result["screens"],
            "momenta",
            result["screen_momenta"],
            "first claim",
            result["first_claim_tick"],
            "gathered by",
            result["gathered_tick"],
            "nodes claimed",
            result["nodes_claimed"],
            "escaped",
            result["escaped"],
            "closed",
            result["matter_closed"],
        )
    print("landings", landings["landings"], "landed", landings["landed"], "of", landings["seeds"])
    print("winner share", landings["winner_share"])
    print("wave fringe", landings["wave_fringe"], "closed", landings["closed"])
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
