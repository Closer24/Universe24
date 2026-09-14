"""A Kerengonen two-lamp interferometer with a mass beside one arm: does gravity leave a phase?

The double-slit configuration (two funded lamps in phase, a screen of absorbers)
with a mass that emits an outward `computation` field next to lamp B's arm.
Four worlds, same lamps, same screen:

  none    no mass
  A       mass; rays on the fixed field clock (the rules as they stand)
  B       mass; `ray_delay`: rays wait at loaded Nodes, phase per link only
  C       mass; `ray_delay` and `ray_phase_per_tick`: waiting also advances the phase

The screen's lower wing is lit by rays that never pass the mass and is the
control; the upper wing's lamp-B rays cross the loaded region. Prediction:
A identical to none; B loses contrast in the upper wing (delayed rays miss
their partners in time); C shifts the upper fringe by the waits, in whole steps.

usage: python examples/relativity-probes/kerengonen_interferometer.py [mass emission]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "kerengonen-double-slit"))
from run_experiments import (  # noqa: E402
    CENTER,
    HEADING_SCALE,
    HEADINGS,
    LAMP_X,
    SCREEN_X,
    TICKS,
    document,
    planar_headings,
)

from event_universe import Simulation  # noqa: E402
from event_universe.initialization import parse_initial_state  # noqa: E402

EMISSION = int(sys.argv[1]) if len(sys.argv) > 1 else 6_000_000
MASS = (CENTER - 2, CENTER + 9, 1)  # beside lamp B's rays to the upper screen


def world_document(mass, ray_delay, phase_per_tick):
    raw = document(TICKS, planar_headings(HEADINGS, HEADING_SCALE))
    raw["model_id"] = "kerengonen-interferometer-beside-a-mass-v1"
    if not mass:
        return raw
    raw["fields"].append(
        {
            "name": "computation",
            "components": 1,
            "units": "load unit",
            "signed": False,
            "conserved": True,
            "extensive": True,
        }
    )
    raw["disturbance_types"].append(
        {
            "name": "mass body",
            "fields": ["quanta", "momentum"],
            "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        }
    )
    raw["spatial_fields"].append({"field": "computation", "baseline": 0, "transport": "outward"})
    raw["emissions"].append(
        {
            "type": "mass body",
            "field": "computation",
            "amount": EMISSION,
            "denominator": 1,
            "source": True,
        }
    )
    raw["seeds"].append({"position": list(MASS), "type": "mass body"})
    raw["computation_field"] = "computation"
    raw["delay_direction"] = "along"  # held lamps and screen keep their fixed cycle
    raw["ray_delay"] = ray_delay
    raw["ray_phase_per_tick"] = phase_per_tick
    return raw


def profile(raw):
    world = Simulation(parse_initial_state(raw))
    for _ in range(raw["ticks"]):
        world.step()
    names = [kind["name"] for kind in raw["disturbance_types"]]
    result = {}
    for position, node in world.nodes.items():
        for record in node.records:
            if record is not None and names[record.type_index] == "screen":
                result[position[1] - CENTER] = world.record_values(record)["quanta"][0]
    return dict(sorted(result.items()))


WORLDS = {
    "none": (False, False, False),
    "A fixed clock": (True, False, False),
    "B ray_delay": (True, True, False),
    "C phase per tick": (True, True, True),
}

if __name__ == "__main__":
    profiles = {name: profile(world_document(*flags)) for name, flags in WORLDS.items()}
    print(
        f"lamps at x={LAMP_X}, y={CENTER}+-3; screen at x={SCREEN_X}; mass at {MASS} emitting "
        f"{EMISSION} per tick; {TICKS} ticks"
    )
    header = "screen y | " + " | ".join(f"{name:>16}" for name in WORLDS)
    print(header)
    for y in sorted(profiles["none"]):
        print(f"{y:>8} | " + " | ".join(f"{profiles[name].get(y, 0):>16}" for name in WORLDS))
    for wing, rows in (
        ("lower wing (control)", range(-12, 0)),
        ("upper wing (past the mass)", range(1, 13)),
    ):
        print(wing + ":")
        for name in WORLDS:
            print(f"   {name:<18} total {sum(profiles[name].get(y, 0) for y in rows)}")
