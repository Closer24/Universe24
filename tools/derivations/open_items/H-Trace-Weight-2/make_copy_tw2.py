"""tw2's flagged COPY of the engine (src/event_universe at the head), written by this script and never by hand:
the copy is src_tw2/event_universe under this folder with ONE flag, the environment variable TW2_TRACE=<integer>,
read once at the import into rows.TRACE; the flag absent, TRACE is the head's literal 54 and the copy is the head
bit for bit (shown on the hole 60 record's hash). Every replacement must match the engine's text exactly once,
else the script refuses. Run: python make_copy_tw2.py"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "..", "src", "event_universe")
DST = os.path.join(HERE, "src_tw2", "event_universe")

if os.path.exists(os.path.join(HERE, "src_tw2")):
    shutil.rmtree(os.path.join(HERE, "src_tw2"))
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))

edits = {
    "rows.py": [
        (
            "from typing import Any\n",
            "import os\nfrom typing import Any\n",
        ),
        (
            "TRACE = 54  # the trace's weight of the held walls and the carrier's write, 2 x 27 (ALGEBRA.md, the held write)\n",
            "TRACE = int(os.environ.get(\"TW2_TRACE\", \"54\"))  # tw2's flag (2026-10-25): the trace's weight, the head's 54 when the flag is absent\n",
        ),
    ],
}
for name, pairs in edits.items():
    path = os.path.join(DST, name)
    text = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if text.count(old) != 1:
            print("REFUSED", name, repr(old[:60]), text.count(old))
            sys.exit(1)
        text = text.replace(old, new)
    open(path, "w", encoding="utf-8").write(text)
print("copy written", DST, "edits", sum(len(p) for p in edits.values()))
