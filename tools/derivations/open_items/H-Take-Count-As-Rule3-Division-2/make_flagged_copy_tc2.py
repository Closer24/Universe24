"""tc2's flagged COPY of the engine's src (the kit's maker pattern): /dev/shm/tmp/tc2/src_tc2 written from the worktree's src by exact
text replacements, each matching once, else refused. The flag TC2_CHORD_COUNT (an environment key of this copy alone, never of the
engine): with it set, the exact take's count is one carried division at the direction -1 and no root: the walls owed times the full
move, divided by the full move's fall (the share's fall to the line now == before), the quotient rounded up by the remainder's mirror;
the fall is concave in the count, so the chord pays the walls at every take, the surplus the take's remainder (EX-S1). Empty, the
head's path bit for bit."""
import os, shutil, sys
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
SRC, DST = os.path.join(W, "src"), "/dev/shm/tmp/tc2/src_tc2"
if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(DST, "event_universe", "take.py")
s = open(p).read()
reps = [
    ("from typing import TYPE_CHECKING, Any\n", "import os\nfrom typing import TYPE_CHECKING, Any\n"),
    ("    if full < walls:\n        return None, full, k\n    for s in rule3.least_root(",
     "    if full < walls:\n        return None, full, k\n    if os.environ.get(\"TC2_CHORD_COUNT\"):\n"
     "        chord = rule3.carried_division(walls * dist, full, 0, -1)[0]\n"
     "        return chord, fall(chord), k\n    for s in rule3.least_root("),
]
for old, new in reps:
    if s.count(old) != 1:
        sys.exit(f"refused: {s.count(old)} matches for {old[:60]!r}")
    s = s.replace(old, new)
open(p, "w").write(s)
print("written", DST, len(reps), "replacements")
