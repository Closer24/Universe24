"""cs6's second copy (src_cs6b from src_cs6, every flag kept): CS6_NO_CREDIT=1, a READER'S CONTROL and no proposal: the bodies' closing takes nothing on any record (no credit), so a board's course is read with the births' takes alone; unset, the copy is src_cs6.
Usage: python make_copy_cs6b.py"""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "src_cs6", "event_universe")
root = os.path.join(here, "src_cs6b")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(dst, "bodies.py")
s = open(p).read()
old = """    for rec, row in enumerate(node.records()):
        if os.environ.get("CS4_LIGHT_NO_BODY", "") == "1" and row.gap == 0:  # cs4's flag: the light at the gap 0 is no body
            continue
"""
new = """    for rec, row in enumerate(node.records()):
        if os.environ.get("CS6_NO_CREDIT", "") == "1":  # cs6's control: no credit on any record
            continue
        if os.environ.get("CS4_LIGHT_NO_BODY", "") == "1" and row.gap == 0:  # cs4's flag: the light at the gap 0 is no body
            continue
"""
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
print("copy written:", dst, "flag: CS6_NO_CREDIT (bodies.py)")
