"""cs4's flagged copy of the engine: src/event_universe copied whole to src_cs4/event_universe with two flags in close.py, each unset bit for bit David's path (the control: 50 intervals equal in every Node's X and every count):
  CK1_CROSS=1 (ck1's text at this head's indentation): the record's re line's zero crossing read in either direction in close.bodies (CK-S1);
  CS4_LIGHT_NO_BODY=1: the plane at the gap 0 never credited as a body (close.bodies skips the gap-0 record: the Boss's reading of the owner's word, nature's light at rest no body); its standing, crossings and beats counters left at 0.
Usage: python make_copy_cs4.py (writes src_cs4/ beside this file)."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "src", "event_universe")
root = os.path.join(here, "src_cs4")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(dst, "close.py")
s = open(p).read()
old_up = """            upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(
                re.before, re.now
            )
"""
new_up = """            if os.environ.get("CK1_CROSS", "") == "1":  # ck1's flag: the zero crossing in either direction, even under the line's negation
                upward = np.vectorize(
                    lambda b, n: 1 if (int(b) < 0 <= int(n) or int(n) < 0 <= int(b)) else 0, otypes=[object]
                )(re.before, re.now)
            else:
                upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(
                    re.before, re.now
                )
"""
assert s.count(old_up) == 1, "the crossing site is not unique (close.py)"
s = s.replace(old_up, new_up)
old_loop = """    for rec, row in enumerate(node.records()):
        standing_now = np.vectorize("""
new_loop = """    for rec, row in enumerate(node.records()):
        if os.environ.get("CS4_LIGHT_NO_BODY", "") == "1" and row.gap == 0:  # cs4's flag: the light at the gap 0 is no body, never credited
            continue
        standing_now = np.vectorize("""
assert s.count(old_loop) == 1, "the bodies' loop is not unique (close.py)"
s = s.replace(old_loop, new_loop)
s = s.replace("import numpy as np\n", "import numpy as np\nimport os\n", 1)
open(p, "w").write(s)
print("copy written:", dst, "flags: CK1_CROSS, CS4_LIGHT_NO_BODY (close.py); unset = David's path")
