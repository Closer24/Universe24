"""The echo's check (C-a's rule on the click lines, the owner's ask of 07:1x UTC): on the mesh world's ring, the wave
leaves its laid bump at round 0 both ways; the two halves meet on the far side and come back to the bump. Read from
the wave's clicks across the Meshes alone: the round where the far side clicks most (the meeting), the round where
the bump's own Node-clocks click most after the light has left them (the return), and Einstein's rule: the meeting
should sit at the midpoint of the laying and the return. Also the leading front's law, first click at distance d.
Rounds as order and as a stand-in for a clock's own count (FACE2 not in the record); whole numbers alone.

Usage: python3 -I echo.py <src> <record.jsonl> <ring> <centre> <rounds after which the return is sought>
"""
import json
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

record, ring, centre, after = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
half, _ = carry(ring, 2, 0)


def dist(s):
    _, r = carry(s - centre + half, ring, 0)
    return r - half


first, size_at = {}, {}
for line in open(record):
    d = json.loads(line)
    if d["kind"] != "click" or d["train"] != 0 or not d.get("across"):
        continue
    t, dd = d["round"], dist(d["site"])
    first.setdefault(dd, t)
    size_at[(t, dd)] = size_at.get((t, dd), 0) + sum(abs(a[2]) for a in d["across"])
rounds = max(t for t, _ in size_at)


def band(lo, hi):
    out = {}
    for (t, dd), v in size_at.items():
        if lo <= abs(dd) <= hi:
            out[t] = out.get(t, 0) + v
    return out


bump, far, mid = band(0, 3), band(half - 3, half), band(43, 47)
t_far = max(far, key=lambda t: far[t])
late = {t: v for t, v in bump.items() if t > after}
t_ret = max(late, key=lambda t: late[t])
t_mid = max(mid, key=lambda t: mid[t])
ok = [dd for dd in range(12, half - 2) if first.get(dd) == 2 * dd and first.get(-dd) == 2 * dd]
print(f"{record}: {rounds} rounds")
print(f"the leading front: the first click at distance d is at round 2 d, both ways, for {len(ok)} of the"
      f" {half - 2 - 12} distances 12 to {half - 3}")
print(f"halfway out (distance 43 to 47) the light clicks most at round {t_mid}: {mid[t_mid]}")
print(f"the far side (distance {half - 3} to {half}) clicks most at round {t_far}: {far[t_far]}")
print(f"the bump's own Node-clocks, after round {after}, click most at round {t_ret}: {late[t_ret]}"
      f" (before round {after} at most {max(v for t, v in bump.items() if t <= after)})")
two_mid = 0 + t_ret
print(f"Einstein's rule: laid at round 0, back at round {t_ret}, so the far event at round {two_mid} / 2;"
      f" the far side's own peak is at round {t_far}, so 2 x {t_far} = {2 * t_far} against {two_mid}")
