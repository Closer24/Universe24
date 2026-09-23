"""The count of events against intervals x active Nodes on five registered
worlds (read-only, the derivation mathematician, 2026-09-21;
DERIVATIONS_BEAM.md section 11): each world is run in-process for its own
ticks (a reproduction of registered integers, no engine change), and per
interval the host counts the carries of the state: the Links of rows (the
flight table's step at their age, read before the interval), the Links of
bodies, the clicks (every end: a set, a face, the border), the rows born
(rows of age 0 after the interval), the pushes taken (bodies whose momentum
changed), the turns (bodies whose phase turned), the counts owed that began;
and the Nodes active (holding a row or a body) after the interval. Merges
and collisions are not counted (the store reports neither); both happen
only at a Link or a birth, so the count of events is a lower bound by the
merges alone.

Run from the repository root with PYTHONPATH=src:

    python docs/designs/derivations_beam/event_count.py > docs/designs/derivations_beam/event_count.out
"""

from __future__ import annotations

import math
import time
from collections import Counter
from pathlib import Path

from event_universe.events.engine import NatureBeamSimulation
from event_universe.events.nature_beam import REST_DIRECTIONS
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[3] / "examples" / "events"
WORLDS = [
    ("slits_low (L2)", "amplitude/slits_low.json"),
    ("bell_16_24 (L3)", "amplitude/bell_16_24.json"),
    ("cone_links (L7)", "amplitude/cone_links.json"),
    ("deuteron_1_kick (I2b)", "nucleus/deuteron_1_kick.json"),
    ("coasting_none (G2)", "hubble_stars/coasting_none.json"),
]
BUDGET_SECONDS = 420


def run(name: str, relative: str):
    path = ROOT / relative
    loaded = load_world(path.read_bytes(), base_dir=path.parent)
    world = loaded.world
    events: list[dict] = []
    # The count is of every line, the per-row clicks among them.
    sim = NatureBeamSimulation(world, observer=events.append, keep_row_clicks=True)
    flight = sim.tables.flight
    totals: Counter = Counter()
    active_sum = 0
    all_nodes = world.shape[0] * world.shape[1] * world.shape[2]
    started = time.perf_counter()
    ticks_run = 0
    momentum_before = {n: list(e.momentum) for n, e in sim.measured.items()}
    steps_before = {n: e.steps - sum(e.contacts) for n, e in sim.measured.items()}
    momentum_initial = {n: list(e.momentum) for n, e in sim.measured.items()}
    owed_before = {n: e.owed for n, e in sim.measured.items()}
    quiet = 0
    last_events = 0
    strides = sim.stores[0].strides
    for _ in range(world.ticks):
        for store in sim.stores:
            if store.size:
                step = flight.steps[store.direction, store.age % flight.period[store.direction]]
                totals["links_rows"] += int(step.any(axis=1).sum())
        clicks_before = sum(1 for e in events if e["event"] == "click")
        sim.step()
        ticks_run += 1
        totals["clicks"] += sum(1 for e in events if e["event"] == "click") - clicks_before
        nodes: set[int] = set()
        for store in sim.stores:
            if store.size:
                nodes.update(store.node.tolist())
                moving = store.direction >= REST_DIRECTIONS
                totals["births"] += int(((store.age == 0) & moving).sum())
        for n, e in sim.measured.items():
            nodes.add(sum(int(p) * int(st) for p, st in zip(e.position, strides, strict=True)))
            if list(e.momentum) != momentum_before.get(n):
                totals["pushes"] += 1
            momentum_before[n] = list(e.momentum)
            # A fire of the drive refused by an occupant is a contact, not a Link.
            made = e.steps - sum(e.contacts)
            totals["links_bodies"] += made - steps_before.get(n, 0)
            steps_before[n] = made
            if e.turn > 0:
                totals["turns"] += 1
            if e.owed > 0 and owed_before.get(n, 0) == 0:
                totals["owed_starts"] += 1
            owed_before[n] = e.owed
        active_sum += len(nodes)
        interval_events = (
            totals["links_rows"]
            + totals["links_bodies"]
            + totals["clicks"]
            + totals["births"]
            + totals["pushes"]
        )
        if interval_events == last_events:
            quiet += 1
        last_events = interval_events
        if time.perf_counter() - started > BUDGET_SECONDS:
            break
    elapsed = time.perf_counter() - started
    carries = totals["links_rows"] + totals["links_bodies"] + totals["clicks"] + totals["births"]
    interactions = totals["clicks"] + totals["births"] + totals["pushes"]
    kinds = Counter(e["event"] for e in events)
    print(
        f"\n{name}: shape {list(world.shape)} ({all_nodes} Nodes), {ticks_run} of {world.ticks} intervals run in {elapsed:.0f} s"
    )
    print(
        f"  per interval: rows' Links {totals['links_rows'] / ticks_run:.1f}, bodies' Links {totals['links_bodies'] / ticks_run:.3f}, clicks {totals['clicks'] / ticks_run:.2f}, births {totals['births'] / ticks_run:.2f}, momentum changes (pushes, recoils) {totals['pushes'] / ticks_run:.2f}, turns {totals['turns'] / ticks_run:.2f}, waits begun {totals['owed_starts'] / ticks_run:.3f}"
    )
    print(
        f"  active Nodes per interval {active_sum / ticks_run:.1f} of {all_nodes}; intervals with no Link, click, birth or push: {quiet} of {ticks_run}"
    )
    print(
        f"  events (Links + clicks + births) {carries} against intervals x active Nodes {active_sum}: ratio {carries / max(active_sum, 1):.3f}; against intervals x all Nodes {ticks_run * all_nodes}: {carries / (ticks_run * all_nodes):.2e}"
    )
    print(
        f"  interactions (clicks + births + pushes) {interactions}: {interactions / max(active_sum, 1):.3f} per active Node-interval; the record's events {dict(kinds)}"
    )
    return sim, events, momentum_initial


if __name__ == "__main__":
    print(
        "EVENTS AGAINST INTERVALS x ACTIVE NODES on five registered worlds (host count, the engine's own run)"
    )
    import json

    expectations = json.loads((ROOT / "amplitude" / "expectations.json").read_text())
    for name, relative in WORLDS:
        sim, events, momentum_initial = run(name, relative)
        # The register reads the first 64 births (u spanning the circle once; the lamps stall once).
        gathers = sorted((e for e in events if e["event"] == "gather"), key=lambda e: e["born"])[:64]
        if relative.endswith("cone_links.json"):
            ages = sorted({e["arrived"] - e["born"] for e in gathers})
            print(
                f"  registered check: every record clicks at the age {ages} (the register: 29 on the axis and on the staircase)"
            )
        if relative.endswith("bell_16_24.json"):
            cells = Counter("".join(c[2] for c in e["chosen"]) for e in gathers if e["chosen"])
            print(
                f"  registered check: the cells {dict(cells)} (the register: {expectations['pair']['chsh']['16_24']['counts']})"
            )
        if relative.endswith("slits_low.json"):
            kinds = Counter(
                (
                    "wall"
                    if c[0].startswith("measured")
                    else "screen"
                    if c[0].startswith("screen")
                    else "faces"
                )
                for e in gathers
                if e["chosen"]
                for c in e["chosen"][:1]
            )
            print(
                f"  registered check: the 64 clicks by kind {dict(kinds)} (the register: {expectations['two_slits']['clicks_by_kind']})"
            )
        if relative.endswith("deuteron_1_kick.json"):
            fires = [e.steps for e in sim.measured.values()]
            contacts = sum(sum(e.contacts) for e in sim.measured.values())
            print(
                f"  registered check: the drive fired {fires} times, {sum(fires)} in all, and {contacts} contacts were booked on the occupants: every fire refused, no Link (the register: no step, the first refused step of each body toward the other)"
            )
        if relative.endswith("coasting_none.json"):
            ratios = [
                math.sqrt(sum(v * v for v in e.momentum))
                / math.sqrt(sum(v * v for v in momentum_initial[n]))
                for n, e in sim.measured.items()
                if any(momentum_initial[n])
            ]
            print(
                f"  registered check: {len(sim.measured)} bodies; |p(end)| / |p(0)| from {min(ratios):.4f} to {max(ratios):.4f} on the {len(ratios)} thrown stars (the README's p(end) / p(0) = 1.000 on the coasting control)"
            )
