"""The flag absent is David's path bit for bit: the hole seed on the 3-cube (tests/worlds/world_node.json) run 20 intervals under src and under src_eq2 (the flag absent) in two processes, the state hashes and the counts compared; and the same world under each flag, the hash printed (a reading)."""
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
for name, src, flag in (
    ("src", os.path.join(WORKTREE, "src"), None),
    ("src_eq2 absent", os.path.join(HERE, "src_eq2"), None),
    ("src_eq2 a", os.path.join(HERE, "src_eq2"), "a"),
    ("src_eq2 b", os.path.join(HERE, "src_eq2"), "b"),
    ("src_eq2 c", os.path.join(HERE, "src_eq2"), "c"),
):
    env = dict(os.environ, PYTHONPATH=src, TMPDIR="/dev/shm/tmp")
    env.pop("EQ2_CLICK", None)
    if flag:
        env["EQ2_CLICK"] = flag
    out = subprocess.run([PY, "-c", CODE, world], env=env, capture_output=True, text=True, check=True)
    found[name] = json.loads(out.stdout)
    print(name, found[name]["hash"][:16], found[name]["counts"]["body_clicks"], found[name]["counts"]["births"], found[name]["census"])
print("flag absent bit for bit:", found["src"]["hash"] == found["src_eq2 absent"]["hash"] and found["src"]["counts"] == found["src_eq2 absent"]["counts"])
