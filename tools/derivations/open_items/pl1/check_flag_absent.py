"""The flag absent is the head's path bit for bit: the hole seed on the 3-cube (tests/worlds/world_node.json) run 20 intervals under src and under src_pl1 with every flag absent, the state hashes, the counts and the census compared; then the same under each flag (a reading of what each flag moves on a record where light flows)."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PY = sys.executable
CODE = r'''
import json, sys
from event_universe.loader.world import load_world
from event_universe.node import Node
universe, world = load_world(sys.argv[1])
node = Node(universe, dict(world, intervals=20))
for _ in range(20):
    node.step()
print(json.dumps({"hash": node.state_hash(), "counts": node.counts, "census": node.census()}))
'''
world = os.path.join(WORKTREE, "tests", "worlds", "world_node.json")
found = {}
for name, src, flags in (
    ("src", os.path.join(WORKTREE, "src"), {}),
    ("src_pl1 absent", os.path.join(HERE, "src_pl1"), {}),
    ("src_pl1 sym", os.path.join(HERE, "src_pl1"), {"PL1_SIGN": "sym"}),
    ("src_pl1 odd", os.path.join(HERE, "src_pl1"), {"PL1_SIGN": "odd"}),
    ("src_pl1 none", os.path.join(HERE, "src_pl1"), {"PL1_SIGN": "none"}),
    ("src_pl1 click b", os.path.join(HERE, "src_pl1"), {"EQ2_CLICK": "b"}),
):
    env = dict(os.environ, PYTHONPATH=src, TMPDIR="/dev/shm/tmp")
    env.pop("EQ2_CLICK", None)
    env.pop("PL1_SIGN", None)
    env.update(flags)
    out = subprocess.run([PY, "-c", CODE, world], env=env, capture_output=True, text=True, check=True)
    found[name] = json.loads(out.stdout)
    print(name, found[name]["hash"][:16], "clicks", found[name]["counts"]["body_clicks"], "births", found[name]["counts"]["births"], "census", found[name]["census"])
print("flag absent bit for bit:", found["src"]["hash"] == found["src_pl1 absent"]["hash"] and found["src"]["counts"] == found["src_pl1 absent"]["counts"])
