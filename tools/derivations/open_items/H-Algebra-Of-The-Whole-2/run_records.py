"""Run the records the brief names with the engine's writer and the gates, each world once, timed (integers: milliseconds)."""
import subprocess
import sys
import time
import os

PY = "/home/user/Universe24/venv314/bin/python"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "records")
os.makedirs(OUT, exist_ok=True)
env = dict(os.environ, PYTHONPATH=os.path.join(ROOT, "src"), TMPDIR="/dev/shm/tmp")
worlds = sys.argv[1:]
for w in worlds:
    name = os.path.splitext(os.path.basename(w))[0]
    out = os.path.join("/dev/shm/tmp", "ag2_" + name + ".json")
    t0 = time.monotonic_ns()
    with open(os.path.join(OUT, name + ".run.txt"), "w") as f:
        subprocess.run(["nice", "-n", "19", PY, "-m", "event_universe.run", w, out, "back", "10"], env=env, stdout=f, stderr=subprocess.STDOUT, cwd=ROOT)
    t1 = time.monotonic_ns()
    with open(os.path.join(OUT, name + ".gates.txt"), "w") as f:
        subprocess.run(["nice", "-n", "19", PY, "-m", "event_universe.gates", out], env=env, stdout=f, stderr=subprocess.STDOUT, cwd=ROOT)
    t2 = time.monotonic_ns()
    print(name, "run ms", (t1 - t0) // 1000000, "gates ms", (t2 - t1) // 1000000, flush=True)
