"""cs5's third copy (src_cs5c from src_cs5b, the flags kept): a READER'S CONTROL and no proposal, CS5_BIRTHS_UNTIL=<i>: from the interval i + 1 on every meeting that reaches the lay is refused by name as `lay` with the key control 2, so a bang's births stand alone on the board and the course after one bang is read with no later birth; unset, the copy is src_cs5b.
Usage: python make_copy_cs5c.py"""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "src_cs5b", "event_universe")
root = os.path.join(here, "src_cs5c")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(dst, "close.py")
s = open(p).read()
old = """        if os.environ.get("CS4_NO_BIRTH", "") == "1":  # cs4's control: no child on the board
            refused(node, at, "lay", control=1, row=rec)
            continue
"""
new = old + """        until = os.environ.get("CS5_BIRTHS_UNTIL", "")
        if until != "" and node.interval > int(until):  # cs5's control: no birth after the named interval
            refused(node, at, "lay", control=2, row=rec)
            continue
"""
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
print("copy written:", dst, "flag: CS5_BIRTHS_UNTIL (close.py)")
