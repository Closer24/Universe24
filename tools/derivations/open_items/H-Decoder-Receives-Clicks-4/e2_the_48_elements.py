"""(e, the 48) Which of the 48 cube elements about the origin keep the credits' multiset, and under one reflection the first signatures that differ (the key that breaks it).
Command: cd <worktree> && PYTHONPATH=src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/open_items/H-Decoder-Receives-Clicks-4/e2_the_48_elements.py 120"""
from __future__ import annotations
import json, sys
from itertools import permutations, product
from d4lib import HERE, dump
N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
L = 3
lines = [json.loads(x) for x in (HERE / f"hole_{N}.lines.jsonl").read_text(encoding="utf-8").splitlines()]
credits = [l for l in lines if l["event"] == "credit"]
def image_node(n, perm, signs):
    return [(signs[i] * n[perm[i]]) % L for i in range(3)]
def image_axis(axis, sign):
    if axis is None:
        return None
    if isinstance(axis[0], int):  # [sign_a, num_a, den_a], or [sign_a, [pair], [pair]] on a record of two lines
        return [sign * axis[0], *axis[1:]]
    return axis
def image_momentum(m, perm, signs):
    return None if m is None else [image_axis(m[perm[i]], signs[i]) for i in range(3)]
KEYS = ("point", "kind", "sense", "beat", "proper", "windows", "support", "momentum")
def sig(c, perm, signs, keys):
    row = {"interval": c["interval"], "family": c["identity"][0]}
    for k in keys:
        if k == "support":
            row[k] = image_node(c["support"], perm, signs)
        elif k == "momentum":
            row[k] = image_momentum(c["momentum"], perm, signs)
        else:
            row[k] = c[k]
    return json.dumps(row, sort_keys=True)
def multiset(perm, signs, keys):
    found = {}
    for c in credits:
        s = sig(c, perm, signs, keys)
        found[s] = found.get(s, 0) + 1
    return found
elements = [(p, s) for p in permutations(range(3)) for s in product((1, -1), repeat=3)]
base = multiset((0, 1, 2), (1, 1, 1), KEYS)
kept = [[list(p), list(s)] for p, s in elements if multiset(p, s, KEYS) == base]
# drop one key at a time: how many elements keep the multiset without it
without = {}
for drop in KEYS:
    keys = tuple(k for k in KEYS if k != drop)
    b = multiset((0, 1, 2), (1, 1, 1), keys)
    without[drop] = sum(1 for p, s in elements if multiset(p, s, keys) == b)
refl = multiset((0, 1, 2), (1, 1, -1), KEYS)
diff_base = sorted(set(base) - set(refl))[:3]
diff_refl = sorted(set(refl) - set(base))[:3]
result = {"elements_keeping_all_keys": kept, "count": len(kept), "elements_keeping_without_one_key": without, "reflection_z_first_differences_base": diff_base, "reflection_z_first_differences_image": diff_refl}
dump(HERE / f"e2_the_48_elements_{N}.json", result)
print(json.dumps(result, indent=1))
