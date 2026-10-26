"""The three records regenerated from the seed alone: each committed record's own `world` dict written out beside its universe file and run through event_universe.run.main, the run back as the record names it."""
import json, subprocess, sys, time
from pathlib import Path
W, OUT = Path(sys.argv[1]), Path("/dev/shm/tmp/cb26/records")
P = "/home/user/Universe24/venv314/bin/python"
for name in ("hole", "chiral", "bodies"):
    rec = json.loads((W / "examples/records" / (name + ".json")).read_text())
    (OUT / (name + ".world.json")).write_text(json.dumps(rec["world"]))
    back = str(rec["run_back"]["intervals"])
    t = time.time()
    found = subprocess.run(
        ["nice", "-n", "19", P, "-m", "event_universe.run", str(OUT / (name + ".world.json")), str(OUT / (name + ".json")), "back", back],
        capture_output=True, text=True, cwd=str(W), env={"PYTHONPATH": str(W / "src"), "TMPDIR": "/dev/shm/tmp/cb26", "PATH": "/usr/bin:/bin"},
    )
    print(name, "exit", found.returncode, "seconds", round(time.time() - t, 1), found.stderr.strip()[-200:], flush=True)
