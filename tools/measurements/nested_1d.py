"""A BOUND BODY INSIDE A BOUND BODY on the chain: the outer body of 600 quanta on the middle Node, the inner of 60 quanta three Nodes beside it, both laid by the pixel tool; the tool's and the loader's word on two bodies sharing Nodes."""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "src")
import event_universe.world_files as wf
from tests.laws import load_file

ROOT = Path(".")
TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
d = Path(tempfile.mkdtemp())
wf.REPOSITORY_ROOT = d
events = ROOT / "examples" / "events"
universe = json.loads((events / "planck_6000.json").read_text())
for family in universe["families"]:
    if family.get("name") == "gravity":
        family["held"]["divisor"] = 10_000
(d / "u.json").write_text(json.dumps(universe))
(d / "e.json").write_bytes((events / "engine_start.json").read_bytes())


def body(x, count):
    return dict(
        family="matter",
        nodes=[dict(node=[x, 0, 0], count=count)],
        momentum=[0, 0, 0],
        momentum_before=[0, 0, 0],
        phase_denominator=1024,
    )


document = dict(
    shape=[240, 1, 1],
    boundary=dict(x="open", y="periodic", z="periodic"),
    detectors=[],
    ticks=400,
    N=65536,
    face_depth=1,
    universe="u.json",
    engine="e.json",
    measured=[body(120, 600), body(int(sys.argv[1]), int(sys.argv[2]))],
)
world = d / "nested.json"
world.write_text(json.dumps(document))
try:
    TOOL.main(["--input", str(world)])
except Exception as stop:
    print(f"THE TOOL REFUSED: {str(stop)[:500]}")
else:
    for entry in json.loads(world.read_text())["measured"]:
        xs = [n["node"][0] for n in entry["nodes"]]
        print(
            f"a body laid at x {min(xs)}..{max(xs)} with {sum(n['count'] for n in entry['nodes'])} quanta"
        )
    print(f"world {world}")
