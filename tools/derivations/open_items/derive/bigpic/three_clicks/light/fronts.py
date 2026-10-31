"""Light and its echo read from the click lines alone (Big Pic, the owner's ask of 07:1x UTC): on the mesh world (a
ring of Node-clocks, one bump of the wave laid at rest), the wave's clicks across the Meshes (the record's across
lines of train 0) are read for (a) the round of each Node-clock's first such click, against its ring distance from
the laid bump: the fronts; (b) the clicks at the bump's own Node-clocks, round by round: the light leaving, a quiet
span, and its return around the ring: the echo; (c) the far side of the ring, where the two fronts meet. Rounds are
read only as order here, and as a stand-in for a clock's own count, which the record does not hold (FACE2): on this
world every clock is laid alike. Whole numbers and Rule3's carry alone.

Usage: python3 -I fronts.py <src> <record.jsonl> <ring size> <the bump's centre site> [rounds per printed row]
"""
import json
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

record, ring, centre = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
step = int(sys.argv[5]) if len(sys.argv) > 5 else 20
half, _ = carry(ring, 2, 0)


def dist(s):
    _, r = carry(s - centre + half, ring, 0)
    return r - half


first, at_bump, far, rounds = {}, {}, {}, 0
for line in open(record):
    d = json.loads(line)
    if d["kind"] == "end":
        rounds = d["rounds"]
    if d["kind"] != "click" or d["train"] != 0 or not d.get("across"):
        continue
    t, s = d["round"], d["site"]
    size = sum(abs(a[2]) for a in d["across"])
    first.setdefault(s, t)
    if abs(dist(s)) <= 3:
        at_bump[t] = at_bump.get(t, 0) + size
    if abs(dist(s)) >= half - 3:
        far[t] = far.get(t, 0) + size

print(f"record {record}: {rounds} rounds, ring of {ring} Node-clocks, the bump at {centre}")
print("(a) the fronts: the first click across a Mesh at each ring distance, both ways")
by_d = {}
for s, t in first.items():
    by_d.setdefault(dist(s), t)
for dd in range(0, half + 1, 10):
    print(f"   distance {dd:3d}: first click at round {by_d.get(dd, '-')} going one way, {by_d.get(-dd, '-')} the other")
d1, d2 = 10, half - 10
if d1 in by_d and d2 in by_d:
    num, den = d2 - d1, by_d[d2] - by_d[d1]
    milli, _ = carry(1000 * num, den, 0)
    print(f"   the front's pace from distance {d1} to {d2}: {num} Meshes in {den} rounds, {milli} per mille of a Mesh a round"
          f" (the board's cone: 1,000)")
print("(b) the clicks at the bump's own Node-clocks (within 3 of it), summed size, every", step, "rounds")
for t0 in range(1, rounds + 1, step):
    tot = sum(at_bump.get(t, 0) for t in range(t0, t0 + step))
    print(f"   rounds {t0:3d} to {t0 + step - 1:3d}: {tot}")
print("(c) the far side of the ring (within 3 of the antipode): its first click, and the summed size every", step,
      "rounds")
print(f"   first click there at round {min(far) if far else '-'}")
for t0 in range(1, rounds + 1, step):
    tot = sum(far.get(t, 0) for t in range(t0, t0 + step))
    if tot:
        print(f"   rounds {t0:3d} to {t0 + step - 1:3d}: {tot}")
