"""bb2: the flagged copy of src/event_universe under tools/derivations/open_items/H-Uniform-Board-Returns-2/engine/, written from David's files by one exact text replacement, named here; the flag the environment variable BB2_SWAP=7; absent, the copy is David's path bit for bit (the swap's trigger as written).

The one replacement (node.py, Node.swap): under the flag the weak maximum is read on the Node's one-Link form, the sum of the Node's level with its six neighbours' through the six Links (the three levels x0, x1, x2 each summed over the seven), the floor on the Node's own two levels as written.
"""
import os
import shutil
import sys

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "src", "event_universe")
dst = os.path.join(here, "engine", "event_universe")
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))

OLD = """        x0, x1, x2 = held[k][0].before, held[k][0].now, self.row(CARRIER).lines[0].now
        peak = np.vectorize("""
NEW = """        x0, x1, x2 = held[k][0].before, held[k][0].now, self.row(CARRIER).lines[0].now
        s0, s1, s2 = x0, x1, x2
        if __import__("os").environ.get("BB2_SWAP") == "7":
            from event_universe.core.ports import across as _across

            def _seven(x):
                s = x
                for port in range(6):
                    s = s + _across(x, port)
                return s

            s0, s1, s2 = _seven(x0), _seven(x1), _seven(x2)
        peak = np.vectorize("""
OLD2 = "        top = peak(x0, x1, x2) | below(x0, x2)"
NEW2 = "        top = peak(s0, s1, s2) | below(x0, x2)"
p = os.path.join(dst, "node.py")
s = open(p).read()
assert s.count(OLD) == 1 and s.count(OLD2) == 1
s = s.replace(OLD, NEW).replace(OLD2, NEW2)
open(p, "w").write(s)
print("copy written; replacements 2; flag BB2_SWAP=7")
