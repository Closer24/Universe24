"""The lottery aside, and back in time: one number, replay to any point, and reversal.

Part 1, the lottery ledger. The seeded quantum world (examples/quantum/native_quantum.json,
seed 17) draws its tickets from one integer. Every ticket drawn is logged aside;
the world is then run again from the logged tickets instead of the seed, and
again from the seed alone, and the complete snapshot is compared tick by tick.
Any earlier point of the history is reached by running the one number forward
to that tick: the snapshot is the same. A different seed diverges at the first
draw.

Part 2, time reversal of the mechanical law. Two equal masses collide
elastically (examples/collisions/01, at link speed). After T ticks every
momentum is negated and the world runs T ticks more: the bodies retrace their
paths, swap back at the same Node, and arrive at their initial positions with
their initial momenta reversed. The collision and transport laws are time
symmetric; nothing else is asserted (outward fields have no inward law, and a
truncated absorption is not a bijection).

usage: python examples/relativity-probes/time_symmetry.py
"""

import hashlib
import json
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[2]


def digest(snapshot) -> str:
    return hashlib.sha256(json.dumps(snapshot, sort_keys=True, default=list).encode()).hexdigest()[:12]


def run_quantum(doc, ticks, log=None):
    world = Simulation(parse_initial_state(doc))
    if log is not None:
        original = world._resolver._sample

        def logged(total):
            ticket = original(total)
            log.append(ticket)
            return ticket

        world._resolver._sample = logged
    hashes = []
    for _ in range(ticks):
        world.step()
        hashes.append(digest(world.snapshot()))
    return hashes, world._resolver.report()["random_draws"]


def part_one():
    doc = json.loads((ROOT / "examples/quantum/native_quantum.json").read_text(encoding="utf-8"))
    ticks = doc["ticks"]
    tickets: list[int] = []
    seeded, draws = run_quantum(doc, ticks, tickets)
    replayed_doc = json.loads(json.dumps(doc))
    replayed_doc["event_program"].pop("seed", None)
    replayed_doc["event_program"]["tickets"] = tickets
    replayed, _ = run_quantum(replayed_doc, ticks)
    again, _ = run_quantum(doc, ticks)
    other_doc = json.loads(json.dumps(doc))
    other_doc["event_program"]["seed"] = 18
    other, _ = run_quantum(other_doc, ticks)
    print("=== Part 1: the lottery ledger of the seeded quantum world (seed 17) ===")
    print(f"  tickets drawn ({draws}): {tickets}")
    print(f"  snapshot digests per tick, seed 17: {seeded}")
    print(
        f"  replayed from the logged tickets:  {'identical at every tick' if replayed == seeded else replayed}"
    )
    print(
        f"  run again from the seed alone:     {'identical at every tick' if again == seeded else again}"
    )
    diverge = next((t + 1 for t, (a, b) in enumerate(zip(seeded, other, strict=True)) if a != b), None)
    print(
        f"  seed 18: {'diverges at tick ' + str(diverge) if diverge else 'identical (no draw differed)'}"
    )
    for point in (2, 4, 6):
        partial, _ = run_quantum(doc, point)
        print(
            f"  back to tick {point} by running the one number forward: "
            f"{'same point' if partial[-1] == seeded[point - 1] else 'DIFFERENT'}"
        )


def residents(world):
    """(body, x, momentum) of every resident body; a link-speed body is resident after each step."""
    return sorted(
        (record["type"], node["position"][0], record["values"]["momentum"][0])
        for node in world.snapshot()["nodes"]
        for record in node["disturbances"]
    )


def part_two():
    doc = json.loads(
        (ROOT / "examples/collisions/01-equal-mass-head-on.json").read_text(encoding="utf-8")
    )
    for kind, momentum in zip(doc["disturbance_types"], (120, -120), strict=True):
        kind["defaults"]["momentum"] = [momentum, 0, 0]
    doc["seeds"] = [
        {"position": [5, 3, 3], "type": "Body A"},
        {"position": [15, 3, 3], "type": "Body B"},
    ]
    forward_ticks = 12
    doc["ticks"] = forward_ticks
    world = Simulation(parse_initial_state(doc))
    trail = []
    for _ in range(forward_ticks):
        world.step()
        trail.append(residents(world))
    final = residents(world)
    reversed_doc = json.loads(json.dumps(doc))
    reversed_doc["seeds"] = [
        {"position": [x, 3, 3], "type": kind, "values": {"mass": 1, "momentum": [-momentum, 0, 0]}}
        for kind, x, momentum in final
    ]
    back = Simulation(parse_initial_state(reversed_doc))
    for _ in range(forward_ticks):
        back.step()
    returned = residents(back)
    initial = sorted(
        (s["type"], s["position"][0], -m) for s, m in zip(doc["seeds"], (120, -120), strict=True)
    )
    print("\n=== Part 2: time reversal of the elastic collision (momentum scale 120 = link speed) ===")
    print("  forward, (body, x, momentum) per tick:")
    for tick, row in enumerate(trail, start=1):
        print(f"    tick {tick:>2}: {row}")
    print(
        f"  at tick {forward_ticks} every momentum is negated and the world runs {forward_ticks} ticks back"
    )
    print(f"  arriving at: {returned}")
    print(f"  initial positions with momenta reversed: {initial}")
    print(f"  {'RETURNED to the initial point' if returned == initial else 'did not return'}")


if __name__ == "__main__":
    part_one()
    part_two()
