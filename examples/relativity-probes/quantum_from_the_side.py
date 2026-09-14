"""The quantum chain probe read by a local observer sitting at the detector node.

The observer at x=7 on the chain row knows only its own node: the tick at which
a localized charge first appears in its own records (the click) and the tick at
which the classical runner, launched on the same row one link before the source,
is received there. Nothing from the resolver's host report is used.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from quantum_gravity import LENGTH, document  # noqa: E402

from event_universe import Simulation  # noqa: E402
from event_universe.initialization import parse_initial_state  # noqa: E402

EYE = (LENGTH, 1, 1)


def observe(emission):
    doc = document(emission)
    for seed in doc["seeds"]:
        if seed["type"] == "runner":
            seed["position"] = [0, 1, 1]  # same row as the chain, one link before the source
    events = []
    world = Simulation(parse_initial_state(doc), observer=events.append)
    click = None
    for tick in range(1, 41):
        world.step()
        names = [
            doc["disturbance_types"][r.type_index]["name"]
            for r in world.nodes[EYE].records
            if r is not None
        ]
        if click is None and "localized_charge" in names:
            click = tick
    runner = next(
        (
            e["tick"]
            for e in events
            if e.get("event") == "received"
            and e.get("disturbance") == "runner"
            and tuple(e["position"]) == EYE
        ),
        None,
    )
    print(f"\n=== observer at {EYE}, mass emission {emission} ===")
    print(f"  first tick a localized charge sits in my own node (the click): {click}")
    print(f"  tick the classical runner is received at my node:            {runner}")


for emission in (0, 6000):
    observe(emission)
