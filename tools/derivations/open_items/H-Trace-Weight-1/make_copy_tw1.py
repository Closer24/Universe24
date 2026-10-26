"""tw1's FLAGGED COPY of src/event_universe (the head 435af1631), written by this script and never by hand:
src_tw1/event_universe is src/event_universe with ONE change: rows.py's literal TRACE = 54 reads the environment flag
TW1_TRACE=<integer>; with the flag absent the copy holds 54 and runs the head bit for bit (shown on the hole 60's record hash,
run_tw1.py). Run: python make_copy_tw1.py  (writes src_tw1/ beside it)."""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "..", "src", "event_universe")
DST_ROOT = os.path.join(HERE, "src_tw1")
DST = os.path.join(DST_ROOT, "event_universe")

if os.path.isdir(DST_ROOT):
    shutil.rmtree(DST_ROOT)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))


def replace(name: str, old: str, new: str) -> None:
    """One named replacement in the copy's file `name`, the old text matched exactly once."""
    path = os.path.join(DST, name)
    text = open(path, encoding="utf-8").read()
    if text.count(old) != 1:
        print("REFUSED", name, repr(old[:80]), "matches", text.count(old))
        sys.exit(1)
    open(path, "w", encoding="utf-8").write(text.replace(old, new))


replace(
    "rows.py",
    "from typing import Any\n\nimport numpy as np\n",
    "import os\nfrom typing import Any\n\nimport numpy as np\n",
)
replace(
    "rows.py",
    "TRACE = 54  # the trace's weight of the held walls and the carrier's write, 2 x 27 (ALGEBRA.md, the held write)\n",
    "TRACE = int(os.environ.get(\"TW1_TRACE\", \"54\"))  # tw1's flag on the trace's weight; 54 (the head) with the flag absent\n",
)
print("written", DST)
