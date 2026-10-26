"""ca2's flagged COPY of the engine's src (the kit's maker pattern): /dev/shm/tmp/ca2/src_ca2 written from the worktree's src by exact text
replacements, each matching once, else refused. The flag CA2_EVEN_LAY (an environment key of this copy alone, never of the engine): with it
set, the children's lay has no direction, the same quantum on both slots (re_now = re_before = A, im_now = im_before = sense B), the
undo the same lay negated; empty, the head's path bit for bit. The control of Q4: which conservation goes when the click has no direction."""
import os, shutil, sys
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
SRC, DST = os.path.join(W, "src"), "/dev/shm/tmp/ca2/src_ca2"
if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(DST, "event_universe", "close.py")
s = open(p).read()
reps = [
    ("from typing import TYPE_CHECKING, Any, NamedTuple\n", "import os\nfrom typing import TYPE_CHECKING, Any, NamedTuple\n"),
    ("    lay(node, s, where, (node.A, 0, 0, sense * node.B), sign)\n",
     "    lay(node, s, where, even_lay(node.A, sense * node.B) if os.environ.get(\"CA2_EVEN_LAY\") else (node.A, 0, 0, sense * node.B), sign)\n"),
    ("            lay(node, s, tuple(entry[\"minus\"]), (a, 0, 0, -b), -1)\n            lay(node, s, tuple(entry[\"plus\"]), (a, 0, 0, b), -1)\n",
     "            lay(node, s, tuple(entry[\"minus\"]), even_lay(a, -b) if os.environ.get(\"CA2_EVEN_LAY\") else (a, 0, 0, -b), -1)\n            lay(node, s, tuple(entry[\"plus\"]), even_lay(a, b) if os.environ.get(\"CA2_EVEN_LAY\") else (a, 0, 0, b), -1)\n"),
    ("def child_laid(", "def even_lay(a: int, b: int) -> tuple[int, int, int, int]:\n    \"\"\"ca2's control: the lay with no direction, the same quantum on the two slots of each line.\"\"\"\n    return (a, a, b, b)\n\n\ndef child_laid("),
]
for old, new in reps:
    if s.count(old) != 1:
        sys.exit(f"refused: {s.count(old)} matches for {old[:60]!r}")
    s = s.replace(old, new)
open(p, "w").write(s)
print("written", DST, len(reps), "replacements")
