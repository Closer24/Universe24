"""tw3's FLAGGED COPY of src/event_universe (toys-5's head d9d7914ff), written by this script and never by hand, as tw1's was:
src_tw3/event_universe is src/event_universe with ONE change: rows.py's literal TRACE = 54 reads the environment flag
TW3_TRACE=<integer>; with the flag absent the copy holds 54 and runs the head bit for bit (shown on the hole 60's record hash,
run_tw3.py against the record cache). src_tw3_rev/event_universe is the same copy with A48-S1's read (commit 05cca5015,
src/event_universe/take.py alone) reverted by `patch -R` of that commit's diff: the former read of the remainder as it stood.
Run: python make_copy_tw3.py  (writes src_tw3/ and src_tw3_rev/ beside it)."""

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SRC = os.path.join(ROOT, "src", "event_universe")


def replace(dst: str, name: str, old: str, new: str) -> None:
    """One named replacement in the copy's file `name`, the old text matched exactly once."""
    path = os.path.join(dst, name)
    text = open(path, encoding="utf-8").read()
    if text.count(old) != 1:
        print("REFUSED", name, repr(old[:80]), "matches", text.count(old))
        sys.exit(1)
    open(path, "w", encoding="utf-8").write(text.replace(old, new))


def build(tag: str, revert: bool) -> None:
    dst_root = os.path.join(HERE, tag)
    dst = os.path.join(dst_root, "event_universe")
    if os.path.isdir(dst_root):
        shutil.rmtree(dst_root)
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    replace(dst, "rows.py", "from typing import Any\n\nimport numpy as np\n", "import os\nfrom typing import Any\n\nimport numpy as np\n")
    replace(
        dst,
        "rows.py",
        "TRACE = 54  # the trace's weight of the held walls and the carrier's write, 2 x 27 (ALGEBRA.md, the held write)\n",
        "TRACE = int(os.environ.get(\"TW3_TRACE\", \"54\"))  # tw3's flag on the trace's weight; 54 (the head) with the flag absent\n",
    )
    if revert:
        diff = subprocess.run(["git", "-C", ROOT, "show", "05cca5015", "--", "src/event_universe/take.py"], check=True, capture_output=True, text=True).stdout
        done = subprocess.run(["patch", "-R", "-p3", "-d", dst], input=diff, capture_output=True, text=True)
        print(done.stdout.strip(), done.stderr.strip())
        if done.returncode != 0:
            print("REFUSED: the revert of 05cca5015 does not apply to take.py")
            sys.exit(1)
    print("written", dst)


build("src_tw3", False)
build("src_tw3_rev", True)
