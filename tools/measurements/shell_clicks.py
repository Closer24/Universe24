"""THE SHELL CLICKS: the chain body of Gamma 6000 laid by the pixel tool; per interval the counts at its two shell Nodes and at the two Nodes just beyond, a click being a whole quantum moving across a Link (the count's line); the clicks through the shell's outer Ports counted inward and outward over 100 intervals."""

import json
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "src")
import event_universe.world_files as wf
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world
from tests.laws import chain_body_world, load_file

TOOL = load_file("pixel_mode", Path("tools/pixel_mode.py"))
d = Path(tempfile.mkdtemp())
wf.REPOSITORY_ROOT = d
world = chain_body_world(d, TOOL)
nodes = sorted(n["node"][0] for n in json.loads(world.read_text())["measured"][0]["nodes"])
sim = DetectorLawSimulation(load_world(world))
block = sim.blocks[0]
lo, hi = nodes[0], nodes[-1]
sim.step()
inset = np.zeros(sim.shape, dtype=bool)
inset[lo : hi + 1] = True
prev = block.counts.copy()
outward = inward = shell_events = 0
print(f"the body's set x = {lo}..{hi}; shell Nodes {lo} and {hi}; beyond them {lo - 1} and {hi + 1}")
print("t | count at lo-1, lo | hi, hi+1 | in the set | beyond the set")
for t in range(2, 102):
    sim.step()
    c = block.counts
    for shell, beyond in ((lo, lo - 1), (hi, hi + 1)):
        moved = int(
            c[beyond, 0, 0] - prev[beyond, 0, 0]
        )  # the quanta that crossed the shell's outer Link this interval
        if moved > 0:
            outward += moved
        if moved < 0:
            inward -= moved
        if int(c[shell, 0, 0]) != int(prev[shell, 0, 0]):
            shell_events += 1
    if t <= 12 or t % 10 == 0:
        print(
            f"{t:3d} | {int(c[lo - 1, 0, 0]):3d} {int(c[lo, 0, 0]):3d} | {int(c[hi, 0, 0]):3d} {int(c[hi + 1, 0, 0]):3d} | {int(c[inset].sum()):4d} | {int(c[~inset].sum()):3d}"
        )
    prev = c.copy()
print(
    f"over 100 intervals: the shell's counts changed {shell_events} times (clicks at the shell); through the shell's outer Ports {outward} quanta out, {inward} quanta back in; total in the set {int(block.counts[inset].sum())} of {int(block.counts.sum())} laid"
)
