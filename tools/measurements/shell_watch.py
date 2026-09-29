"""THE SHELL WATCH (GAMEBOARD, the owner's word of 2026-09-29: the engine alone, no world of record): one bound body at rest,
stepped by the engine; per interval the Nodes whose count changed, each classed INTERIOR (all six neighbours in the body's
declared set), SHELL (in the set with a neighbour outside) or BEYOND (outside the set); the quanta moved per class, the count
beyond the set, the holes (negative counts) and the body's total. Usage: python shell_watch.py <world.json> <ticks> <every>."""

import json
import sys
from pathlib import Path

import numpy as np

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world

path = Path(sys.argv[1])
ticks = int(sys.argv[2])
every = int(sys.argv[3]) if len(sys.argv) > 3 else 20
world = load_world(path)
sim = DetectorLawSimulation(world)
block = sim.blocks[0]
document = json.loads(path.read_text())
shape = tuple(document["shape"])
inset = np.zeros(shape, dtype=bool)
for node in document["measured"][0]["nodes"]:
    inset[tuple(node["node"])] = True
interior = inset.copy()
for axis in range(3):
    if shape[axis] == 1:
        continue  # a folded axis: the neighbour is the Node itself
    for sign in (1, -1):
        shifted = np.roll(inset, sign, axis=axis)
        # an open face counts as outside
        index = [slice(None)] * 3
        index[axis] = 0 if sign == 1 else -1
        shifted[tuple(index)] = False
        interior &= shifted
shell = inset & ~interior
beyond = ~inset
print(
    f"the set {int(inset.sum())} Nodes: interior {int(interior.sum())}, shell {int(shell.sum())}",
    flush=True,
)

previous = None
moved = {"INTERIOR": 0, "SHELL": 0, "BEYOND": 0}
changed_nodes = {"INTERIOR": set(), "SHELL": set(), "BEYOND": set()}
for t in range(1, ticks + 1):
    try:
        sim.step()
    except Exception as stop:
        print(f"REFUSED at interval {sim.tick + 1}: {str(stop)[:300]}", flush=True)
        break
    counts = np.asarray(block.counts, dtype=np.int64)
    if previous is not None:
        diff = counts - previous
        for name, mask in (("INTERIOR", interior), ("SHELL", shell), ("BEYOND", beyond)):
            d = diff[mask]
            moved[name] += int(np.abs(d).sum())
            for idx in zip(*np.nonzero(mask & (diff != 0)), strict=True):
                changed_nodes[name].add(idx)
    previous = counts.copy()
    if t == 1:
        print(
            f"the count's wall T (derived by the engine from the record's form per quantum) {sim.world.quantum_action} (the universe's T)",
            flush=True,
        )
    if t % every == 0 or t <= 2:
        peak = int(np.abs(np.asarray(block.own.now)).max()) if block.own is not None else -1
        print(
            f"t={t:5d} total {int(counts.sum()):6d} beyond {int(counts[beyond].sum()):4d} holes {int(counts.min()):3d} | quanta moved so far: interior {moved['INTERIOR']:6d} shell {moved['SHELL']:6d} beyond {moved['BEYOND']:6d} | Nodes touched: interior {len(changed_nodes['INTERIOR'])} shell {len(changed_nodes['SHELL'])} beyond {len(changed_nodes['BEYOND'])} | peak {peak}",
            flush=True,
        )
