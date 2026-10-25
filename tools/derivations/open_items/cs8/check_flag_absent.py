"""cs8: the flag absent is David's path bit for bit: the hole seed on the 3-cube (tests/worlds/world_node.json) run 20 intervals under src and under src_cs8 (every flag absent) in two processes, the state hashes and the counts compared (cs7's check rebuilt at this folder)."""
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
for name, src in (("src", os.path.join(WORKTREE, "src")), ("src_cs8 absent", os.path.join(HERE, "src_cs8"))):
    env = dict(os.environ, PYTHONPATH=src, TMPDIR="/dev/shm/tmp")
    for k in ("CS7_EQ", "CS4_TAKE_FARTHEST", "CS8_REST", "CS5_CROWD_OFF", "CS6_SL_S3", "CS6_LIGHT_ON_LIGHT"):
        env.pop(k, None)
    out = subprocess.run([PY, "-c", CODE, world], env=env, capture_output=True, text=True, check=True)
    found[name] = json.loads(out.stdout)
    print(name, found[name]["hash"][:16], found[name]["counts"]["body_clicks"], found[name]["counts"]["births"], found[name]["census"])
print("flag absent bit for bit:", found["src"]["hash"] == found["src_cs8 absent"]["hash"] and found["src"]["counts"] == found["src_cs8 absent"]["counts"])
