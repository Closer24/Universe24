"""The records of H-Setting-From-The-Frame-2, run one at a time under nice 19 (the load rule: the kit's wait_load before every run above a minute): the hole 60, the chiral 60, the chiral 300 on the 5-cube, the chiral 300 on the 3-cube (the seed's centres read mod 3 as the kit's 48 tool reads them), ga2 450. Usage: python run_records.py <worlds dir> <records dir> <kit dir>"""
import subprocess
import sys
import time

P = sys.executable
worlds, records, kit = sys.argv[1:4]
RUNS = [
    ("world_hole.json", "hole_60.json", False),
    ("world_nature.json", "chiral_60.json", False),
    ("world_chiral_300.json", "chiral_300.json", True),
    ("world_chiral3_300.json", "chiral3_300.json", True),
    ("world_ga2_450.json", "ga2_450.json", True),
]
for world, out, long in RUNS:
    if long:
        subprocess.run([P, f"{kit}/wait_load.py", "3"], check=True)
    t0 = time.monotonic()
    cmd = ["nice", "-n", "19", P, "-m", "event_universe.run", f"{worlds}/{world}", f"{records}/{out}", "back", "20"]
    with open(f"{records}/{out}.log", "w") as log:
        subprocess.run(cmd, check=True, stdout=log, stderr=subprocess.STDOUT)
    print(out, "seconds", int(time.monotonic() - t0), flush=True)
print("done", flush=True)
