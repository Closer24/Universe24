"""cc1's flagged COPY of the engine's src (the kit's maker pattern): /dev/shm/tmp/cc1/src_cc1 written from the worktree's src by exact
text replacements, each matching once, else refused. The flag CC1_LIGHT_EXACT (an environment key of this copy alone, never of the
engine): with it set, merger.rise_of names no line as having no direction: the exact take at -1 is laid at every merger end, the tie
now == before resolved by the letter's own u (-1, as fall_of's t resolves it), so the merger's light is laid on one line (its own
Wronskian 0) at both ends and never as the charged child's lay; empty, the head's path bit for bit."""
import os, shutil, sys
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
SRC, DST = os.path.join(W, "src"), "/dev/shm/tmp/cc1/src_cc1"
if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(DST, "event_universe", "merger.py")
s = open(p).read()
reps = [
    ("from collections.abc import Callable\n", "import os\nfrom collections.abc import Callable\n"),
    ("    now, before = int(line.now[where]), int(line.before[where])\n    if now == before:\n        return k, 0, 0\n",
     "    now, before = int(line.now[where]), int(line.before[where])\n    if now == before and not os.environ.get(\"CC1_LIGHT_EXACT\"):\n        return k, 0, 0\n"),
]
for old, new in reps:
    if s.count(old) != 1:
        sys.exit(f"refused: {s.count(old)} matches for {old[:60]!r}")
    s = s.replace(old, new)
open(p, "w").write(s)
print("written", DST, len(reps), "replacements")
