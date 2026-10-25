"""Hand r5: run top_local.py on every (flag, board) of the brief, each to its own .log beside it (no shell loop)."""

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PYTHON = "/home/user/Universe24/venv314/bin/python"
RUNS = [(f, b) for b in ("open", "hole", "sea", "standing") for f in ("3", "2", "0")]
if len(sys.argv) > 1:
    RUNS = [tuple(a.split(":")) for a in sys.argv[1:]]
env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), TMPDIR="/dev/shm/tmp")
for flag, board in RUNS:
    extra = [] if len(board.split(",")) == 1 else board.split(",")[1:]
    name = board.split(",")[0]
    log = HERE / f"top_local_{flag}_{name}{''.join('_' + e for e in extra)}.log"
    with log.open("w", encoding="utf-8") as out:
        subprocess.run([PYTHON, str(HERE / "top_local.py"), flag, name, *extra], cwd=ROOT, env=env, stdout=out, stderr=subprocess.STDOUT, check=False)
    print(flag, name, log.read_text(encoding="utf-8").strip().splitlines()[-1][:400], flush=True)
