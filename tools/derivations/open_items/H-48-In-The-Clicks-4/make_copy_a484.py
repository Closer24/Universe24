"""a484's flagged copy of the engine: src/event_universe copied whole to src_a484/event_universe with one text replacement in take.py (read_number's fold and origin) behind the environment flag A484_READ: unset or empty, the head's path bit for bit; "1" the fold by the one rule of the remainder (the ones' complement, min(rho, wl - 1 - rho), rule3.mirrored once) and the origin the exact half alone (folded == half(wl)). Measured, not proposed: the derivation (REPORT.md, step 1) says this fold is not covariant with the state's own carry of a negated division (the two's complement), and the measurement is the integer that shows it."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "..", "src", "event_universe")
dst = os.path.join(here, "src_a484", "event_universe")
if os.path.exists(os.path.join(here, "src_a484")):
    shutil.rmtree(os.path.join(here, "src_a484"))
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
path = os.path.join(dst, "take.py")
text = open(path).read()
old = """            folded = min(rho, remainder(wl - rho, wl))
            origin = origin and folded in (half(wl), mirrored(half(wl), wl, 1))
"""
new = """            if A484_READ:  # a484: the fold by the one rule (the ones' complement), the origin the exact half alone
                folded = min(rho, mirrored(rho, wl, 1))
                origin = origin and folded == half(wl)
            else:
                folded = min(rho, remainder(wl - rho, wl))
                origin = origin and folded in (half(wl), mirrored(half(wl), wl, 1))
"""
assert text.count(old) == 1, "the replacement site is not unique"
text = text.replace(old, new)
text = text.replace("import numpy as np\n", "import numpy as np\nimport os\n\nA484_READ = os.environ.get(\"A484_READ\", \"\") == \"1\"  # a484's flag: unset is the head bit for bit\n", 1)
open(path, "w").write(text)
print("copy written:", dst)
