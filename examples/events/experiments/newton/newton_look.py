"""Scratch GAMEBOARD watch of two whole bodies: per interval each body's count-weighted centroid along x (the count's line), its total count, its record's peak; the gap between the bodies' faces; the refusal named. Usage: watch_two.py <world.json> <ticks> [every]"""

import json
import sys
from pathlib import Path

import numpy as np

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world

path = Path(sys.argv[1])
world = load_world(path)
sim = DetectorLawSimulation(world)
ticks = int(sys.argv[2])
every = int(sys.argv[3]) if len(sys.argv) > 3 else 10
bodies = [sim.blocks[0], sim.blocks[1]]
blind_path = path.with_suffix(".expectation.json")
blind = json.loads(blind_path.read_text()) if blind_path.exists() else {}


def centroid(arr):
    a = np.asarray(arr, dtype=float)
    wx = a.sum(axis=(1, 2))
    return float((np.arange(a.shape[0]) * wx).sum() / wx.sum()) if wx.sum() > 0 else float("nan")


def faces(arr):
    a = np.asarray(arr)
    xs = np.nonzero(a.sum(axis=(1, 2)))[0]
    return (int(xs.min()), int(xs.max())) if len(xs) else (-1, -1)


start = None
for _ in range(ticks):
    try:
        sim.step()
    except Exception as stop:
        print(f"REFUSED at interval {sim.tick + 1}: {str(stop)[:300]}", flush=True)
        break
    if start is None:
        start = [centroid(b.counts) for b in bodies]
        print(
            f"t=   1 centroids {start[0]:7.3f} {start[1]:7.3f} totals {[int(np.asarray(b.counts).sum()) for b in bodies]} faces {[faces(b.counts) for b in bodies]}",
            flush=True,
        )
    if sim.tick % every == 0 or sim.tick < 3:
        cs = [centroid(b.counts) for b in bodies]
        gap = faces(bodies[1].counts)[0] - faces(bodies[0].counts)[1] - 1
        exp = blind.get("closing_links_at_intervals", {}).get(str(sim.tick), "-")
        peaks = [int(np.abs(np.asarray(b.own.now)).max()) if b.own is not None else -1 for b in bodies]
        print(
            f"t={sim.tick:4d} centroids {cs[0]:7.3f} {cs[1]:7.3f} moved {cs[0] - start[0]:+7.3f} {cs[1] - start[1]:+7.3f} closing {(start[1] - start[0]) - (cs[1] - cs[0]):6.3f} blind {exp} | totals {[int(np.asarray(b.counts).sum()) for b in bodies]} gap {gap} peaks {peaks}",
            flush=True,
        )
