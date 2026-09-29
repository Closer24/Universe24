"""ONE BODY IN THREE DIMENSIONS at Gamma 6000: 600 quanta on the centre Node of a periodic cube, laid by the pixel tool; its Nodes and extent. Usage: body_3d.py <side> <quanta>."""

import json
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "src")
import event_universe.world_files as wf
from tests.laws import load_file

ROOT = Path(".")
TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
side, quanta = int(sys.argv[1]), int(sys.argv[2])
d = Path(tempfile.mkdtemp())
wf.REPOSITORY_ROOT = d
events = ROOT / "examples" / "events"
universe = json.loads((events / "planck_6000.json").read_text())
for family in universe["families"]:
    if family.get("name") == "gravity":
        family["held"]["divisor"] = 10_000
(d / "u.json").write_text(json.dumps(universe))
(d / "e.json").write_bytes((events / "engine_start.json").read_bytes())
c = side // 2
body = dict(
    family="matter",
    nodes=[dict(node=[c, c, c], count=quanta)],
    momentum=[0, 0, 0],
    momentum_before=[0, 0, 0],
    phase_denominator=1024,
)
document = dict(
    shape=[side, side, side],
    boundary=dict(x="open", y="open", z="open"),
    detectors=[],
    ticks=100,
    N=65536,
    face_depth=1,
    universe="u.json",
    engine="e.json",
    measured=[body],
)
world = d / "cube.json"
world.write_text(json.dumps(document))
t0 = time.time()
TOOL.main(["--input", str(world)])
nodes = json.loads(world.read_text())["measured"][0]["nodes"]
xs = sorted(set(n["node"][0] for n in nodes))
print(
    f"laid in {time.time() - t0:.0f} s: {len(nodes)} Nodes, x from {xs[0]} to {xs[-1]}, counts at the centre line: {[n['count'] for n in nodes if n['node'][1] == c and n['node'][2] == c]}"
)
print(f"world {world}")
