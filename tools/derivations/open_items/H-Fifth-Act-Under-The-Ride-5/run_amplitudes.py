"""Hand r5: the closed standing board under the mended fifth act (U24_RIDES=3) at smaller amplitudes, the seed's births (no shell loop)."""

import os
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for amplitude in ("320", "260", "200"):
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), TMPDIR="/dev/shm/tmp", R5_AMPLITUDE=amplitude)
    log = HERE / f"top_local_3_standing_A{amplitude}.log"
    with log.open("w", encoding="utf-8") as out:
        subprocess.run(["/home/user/Universe24/venv314/bin/python", str(HERE / "top_local.py"), "3", "standing"], cwd=ROOT, env=env, stdout=out, stderr=subprocess.STDOUT, check=False)
    print(amplitude, log.read_text(encoding="utf-8")[-600:], flush=True)
