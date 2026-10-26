"""The kit's bodies 120 (the 7-cube on the middle universe) under MB_S1 and with the flag empty, one at a time under nice 19."""
import os, subprocess, time
P = "/home/user/Universe24/venv314/bin/python"
W = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mb1"
F = W + "/tools/derivations/open_items/H-Moving-Born-Pair-1"
D = "/dev/shm/tmp/mb1"
log = open(D + "/chain2.log", "a")
for name, flag in (("bodies120k_mb", "1"), ("bodies120k_off", "")):
    e = dict(os.environ, PYTHONPATH=D + "/src_mb1", TMPDIR="/dev/shm/tmp", MB_S1=flag, HQ_S1="")
    t = time.time()
    with open(D + "/" + name + ".out", "w") as o:
        r = subprocess.run(["nice", "-n", "19", P, "-m", "event_universe.run", F + "/worlds/world_bodies_120.json", D + "/" + name + ".json", "back", "20"], env=e, cwd=D, stdout=o, stderr=subprocess.STDOUT)
    print(time.strftime("%H:%M:%S"), name, "rc", r.returncode, "s", int(time.time() - t), file=log, flush=True)
print("chain2 done", file=log, flush=True)
