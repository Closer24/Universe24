"""tc1's flagged COPY of the engine's src (the kit's maker pattern): /dev/shm/tmp/tc1/src_tc1 written from the worktree's src by exact
text replacements, each matching once, else refused. The flag TC1_DIVISION_COUNT (an environment key of this copy alone, never of the
engine): with it set, the take's count at the gap-0 row is one carried division (take.division_count) in place of the share's root,
the second key TC1_DIVISION_GUARD adding the exact guard at the quotient; both empty, the head's path bit for bit. David's src is untouched."""
import os, shutil, sys
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
SRC, DST = os.path.join(W, "src"), "/dev/shm/tmp/tc1/src_tc1"
if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(DST, "event_universe", "take.py")
s = open(p).read()
reps = [
    ("from __future__ import annotations\n\nfrom typing import TYPE_CHECKING, Any\n",
     "from __future__ import annotations\n\nimport os\nfrom typing import TYPE_CHECKING, Any\n"),
    ("    full = fall(dist := abs(now - before))\n    if full < walls:\n        return None, full, k\n",
     "    if os.environ.get(\"TC1_DIVISION_COUNT\"):\n        return division_count(now, before, t, w, pull, x, weight, walls, fall, k)\n"
     "    full = fall(dist := abs(now - before))\n    if full < walls:\n        return None, full, k\n"),
    ("def lay(node: Node, rec: int, where: Any, levels: Any, sign: int = 1) -> None:\n",
     "def division_count(\n    now: int, before: int, t: int, w: int, pull: int, x: int, weight: int, walls: int, fall: Any, k: int\n) -> tuple[int | None, int, int]:\n"
     "    \"\"\"tc1's form behind the flag TC1_DIVISION_COUNT: the take's count as one carried division of the walls owed, in the share's unit, by the price of one level at the start of the move, X times Rule3's backward numerator read at the now slot, -t (2 w now + pull); the least count whose linear price covers the walls (the ceiling as the floor's mirror); the moved levels' own square, the fall's shortfall under the walls, is left to the Node's take remainder as a debt (EX-S1's remainder signed), or, with the key TC1_DIVISION_GUARD, paid by the exact guard the letter holds (the head's refusal where the full move cannot pay, then the fall at the count read against the walls and, where short, the shortfall divided by the price of the next level, price less 2 X w s, the same carried division iterated from below to its fixed count; no root); refused where the line has no price to give or the count passes the line's own move.\"\"\"\n"
     "    price = -t * ((w + w) * now + pull) * x\n"
     "    dist = abs(now - before)\n"
     "    if price <= 0:\n        return None, fall(dist), k\n"
     "    s = -quotient(-walls * weight, price)\n"
     "    if os.environ.get(\"TC1_DIVISION_GUARD\") and fall(dist) < walls:\n        return None, fall(dist), k\n"
     "    while os.environ.get(\"TC1_DIVISION_GUARD\") and s <= dist and fall(s) < walls:\n"
     "        s += -quotient(-(walls * weight - s * (price - x * w * s)), price - x * w * (s + s))\n"
     "    if s > dist:\n        return None, fall(dist), k\n"
     "    return s, fall(s), k\n\n\n"
     "def lay(node: Node, rec: int, where: Any, levels: Any, sign: int = 1) -> None:\n"),
]
for old, new in reps:
    if s.count(old) != 1:
        sys.exit(f"refused: {s.count(old)} matches for {old[:60]!r}")
    s = s.replace(old, new)
open(p, "w").write(s)
print("written", DST, len(reps), "replacements")
