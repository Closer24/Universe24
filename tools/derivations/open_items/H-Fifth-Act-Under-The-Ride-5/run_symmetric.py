"""Hand r5: the symmetric-ride toy at three gains, each to its own .log (no shell loop)."""

import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
for gain in ("1", "3", "30"):
    log = HERE / f"symmetric_ride_g{gain}.log"
    with log.open("w", encoding="utf-8") as out:
        subprocess.run(["/home/user/Universe24/venv314/bin/python", str(HERE / "symmetric_ride.py"), gain], stdout=out, stderr=subprocess.STDOUT, check=False)
    print(gain, "done", flush=True)
