"""a484: the credits (body clicks) at one interval in the base and one reflection, read side by side at the image Node. Usage: locate_credit.py <src> <worktree> <image index> <interval>"""
import json
import sys

sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2] + "/tools/derivations/open_items/H-48-In-The-Clicks-2")
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
import a48b_48 as A  # noqa: E402

root, k_img, at_i = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
universe, world = load_world(root + "/tests/worlds/world_node.json")
centres = ([1, 0, 0], [0, 2, 1], [2, 1, 0])
lays = [{"lay": "sea", "row": 0}, {"lay": "hole", "at": [0, 0, 0]}]
lays += [{"lay": "at", "row": 0, "centre": c, "quanta": 1} for c in centres]
world = dict(world, shape=[3, 3, 3], intervals=at_i, seed=lays)
m = A.signed_permutations()[k_img]
base, img = Node(universe, world), Node(universe, A.world_image(world, m, 3))
for t in range(at_i):
    base.step(); img.step()
keys = ("node", "line", "sense", "beat", "levels", "taken_now_was", "taker", "walls", "fall", "taken_line", "taken_row")
cb = [e for e in base.log if e["event"] == "credit" and e["i"] == at_i]
ci = {tuple(e["node"]): e for e in img.log if e["event"] == "credit" and e["i"] == at_i}
print("credits at", at_i, "base", len(cb), "image", len(ci))
for e in cb:
    f = ci.get(tuple(A.image(m, tuple(e["node"]), 3)))
    a = {k: e.get(k) for k in keys if k in e}
    b = None if f is None else {k: f.get(k) for k in keys if k in f}
    flag = "" if (b is not None and all(a.get(k) == b.get(k) for k in a if k not in ("node", "sense"))) else "  <<<"
    print("base", json.dumps(a, default=str)[:300], "| image", json.dumps(b, default=str)[:300], flag)
