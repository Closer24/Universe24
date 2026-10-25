"""ol1's control: the flags absent are David's path bit for bit: a world run n intervals under src and under src_ol1 (no flag), the state hash, the counts and the census compared. Usage: check_flag_absent.py <world> <n> [lay.json]"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CODE = r'''
import json, sys
sys.set_int_max_str_digits(0)
sys.path.insert(0, sys.argv[3])
from event_universe.loader.world import load_world
from event_universe.node import Node
universe, world = load_world(sys.argv[1])
node = Node(universe, world)
if len(sys.argv) > 4:
    import ol1_run, cs5_run
    spec = json.load(open(sys.argv[4]))
    if "beam" in spec:
        ol1_run.lay_beam(node, spec["beam"])
    else:
        cs5_run.lay_pattern(node, spec)
for _ in range(int(sys.argv[2])):
    node.step()
print(json.dumps({"hash": node.state_hash(), "counts": node.counts, "census": node.census()}))
'''
def run(src):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("OL1_", "CS7_", "CS4_"))}
    env.update(PYTHONPATH=src, TMPDIR="/dev/shm/tmp")
    args = [sys.executable, "-c", CODE, sys.argv[1], sys.argv[2], HERE] + sys.argv[3:4]
    return json.loads(subprocess.run(args, env=env, capture_output=True, text=True, check=True).stdout)
a, b = run(os.path.join(WORKTREE, "src")), run(os.path.join(HERE, "src_ol1"))
print(json.dumps({"world": sys.argv[1], "n": sys.argv[2], "src": a, "src_ol1 (no flag)": b, "EQUAL": a == b}))
