"""cs4's second copy, a reader's control and no proposal: src_cs4 copied to src_cs4b with a third flag, CS4_NO_BIRTH=1, under which close.refuse keeps no birth (every meeting that reaches the lay refused by name as `lay` with the key control 1), so the light's own course at an amplitude is read with no child on the board; unset, the copy is src_cs4 (the two flags of make_copy_cs4.py, unset David's path bit for bit).
Usage: python make_copy_cs4b.py"""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "src_cs4", "event_universe")
root = os.path.join(here, "src_cs4b")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(dst, "close.py")
s = open(p).read()
old = """    kept = []
    for at, s, minus, plus, room, rec in born:
        if int(owns[s][minus]) > 0 or int(owns[s][plus]) > 0:"""
new = """    kept = []
    for at, s, minus, plus, room, rec in born:
        if os.environ.get("CS4_NO_BIRTH", "") == "1":  # cs4's control: no child on the board, the course of the light alone
            refused(node, at, "lay", control=1, row=rec)
            continue
        if int(owns[s][minus]) > 0 or int(owns[s][plus]) > 0:"""
assert s.count(old) == 1
s = s.replace(old, new)
open(p, "w").write(s)
print("copy written:", dst, "flag: CS4_NO_BIRTH (close.py)")
