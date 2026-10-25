"""Hand r5: run twin.py on the boards under the ride (3) and the branch (0), each to its own .log (no shell loop)."""

import os
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), TMPDIR="/dev/shm/tmp")
for flag, board in (("3", "open"), ("3", "standing"), ("3", "hole"), ("3", "sea"), ("0", "open"), ("0", "standing")):
    log = HERE / f"twin_{flag}_{board}.log"
    with log.open("w", encoding="utf-8") as out:
        subprocess.run(["/home/user/Universe24/venv314/bin/python", str(HERE / "twin.py"), board, flag], cwd=ROOT, env=env, stdout=out, stderr=subprocess.STDOUT, check=False)
    print(flag, board, log.read_text(encoding="utf-8")[-1500:], flush=True)
