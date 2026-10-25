"""pl2: the flags absent are David's path bit for bit: tests/worlds/world_node.json (the hole seed on the 3-cube) and world_plasma_3.json run 20 intervals under src and under src_pl2 with every flag absent, the state hashes, the counts and the census compared."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PY = sys.executable
CODE = r'''
import json, sys
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node
universe, world = load_world(sys.argv[1])
node = Node(universe, dict(world, intervals=20))
for _ in range(20):
    node.step()
print(json.dumps({"hash": node.state_hash(), "counts": node.counts, "census": node.census()}))
'''
ok = True
for name in ("world_node.json", "world_plasma_3.json", "world_chiral.json"):
    pass
for name in ("world_node.json", "world_plasma_3.json", "world_chiral.json"):
    world = os.path.join(WORKTREE, "tests", "worlds", name)
    found = {}
    for label, src in (("src", os.path.join(WORKTREE, "src")), ("src_pl2 absent", os.path.join(HERE, "src_pl2")), ("src_pl2b absent", os.path.join(HERE, "src_pl2b"))):
        env = {k: v for k, v in os.environ.items() if not k.startswith(("PL2_", "CS7_"))}
        env.update(PYTHONPATH=src, TMPDIR="/dev/shm/tmp")
        out = subprocess.run([PY, "-c", CODE, world], env=env, capture_output=True, text=True, check=True)
        found[label] = json.loads(out.stdout)
    same = found["src"] == found["src_pl2 absent"] == found["src_pl2b absent"]
    ok = ok and same
    print(name, "bit for bit:", same, found["src"]["hash"][:16], found["src"]["counts"]["body_clicks"], found["src"]["counts"]["births"], found["src"]["census"])
print("every flag absent is David's path bit for bit:", ok)
