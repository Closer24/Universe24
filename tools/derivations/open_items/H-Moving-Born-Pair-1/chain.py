"""The chain of this hand's runs, one at a time under nice 19 (the kit's wait_load before every run above a minute): the quartet worlds at the third lift under HQ_S1 and MB_S1, the three plane records under MB_S1 alone, the measurement 5-cube, the kit's conservation check on one flagged record, then the kit's 48 on the chiral 3-cube under the flags. Every record under /dev/shm/tmp/mb1/; the log of the chain beside them."""
import os, subprocess, sys, time

P = "/home/user/Universe24/venv314/bin/python"
W = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mb1"
F = W + "/tools/derivations/open_items/H-Moving-Born-Pair-1"
K = W + "/tools/derivations/open_items/H-Kit-48-Re-Cut-1"
S = "/dev/shm/tmp/mb1/src_mb1"
D = "/dev/shm/tmp/mb1"
log = open(D + "/chain.log", "a")

def say(*a):
    print(time.strftime("%H:%M:%S"), *a, file=log, flush=True)

def env(flags):
    e = dict(os.environ)
    e["PYTHONPATH"] = S
    e["TMPDIR"] = "/dev/shm/tmp"
    for k in ("HQ_S1", "MB_S1"):
        e[k] = "1" if k in flags else ""
    return e

def run(name, world, flags, back="20", wait=False):
    if wait:
        subprocess.run([P, K + "/wait_load.py", "3"], env=env(()), cwd=D)
    out = D + "/" + name + ".json"
    say("start", name, flags)
    t = time.time()
    with open(D + "/" + name + ".out", "w") as o:
        r = subprocess.run(["nice", "-n", "19", P, "-m", "event_universe.run", world, out, "back", back], env=env(flags), cwd=D, stdout=o, stderr=subprocess.STDOUT)
    say("done", name, "rc", r.returncode, "s", int(time.time() - t))
    return out

worlds = F + "/worlds/"
run("chiral3_60_lift3_mb", worlds + "world_chiral3_60_lift3.json", ("HQ_S1", "MB_S1"))
run("chiral3_60_lift3_hq", worlds + "world_chiral3_60_lift3.json", ("HQ_S1",))
run("hole60_mb", worlds + "world_hole.json", ("MB_S1",))
run("chiral60_mb", worlds + "world_nature.json", ("MB_S1",))
run("chiral5_60_lift3_mb", worlds + "world_chiral5_60_lift3.json", ("HQ_S1", "MB_S1"), wait=True)
run("hole5_60_lift3_mb", worlds + "world_hole5_60_lift3.json", ("HQ_S1", "MB_S1"), wait=True)
run("bodies120_mb", worlds + "world_bodies.json", ("MB_S1",), wait=True)
say("start conservation check on hole60_mb")
with open(D + "/cons_hole60_mb.out", "w") as o:
    subprocess.run(["nice", "-n", "19", P, K + "/conservation_check.py", D + "/hole60_mb.json", "out", D + "/cons_hole60_mb.json"], env=env(("MB_S1",)), cwd=D, stdout=o, stderr=subprocess.STDOUT)
say("done conservation check")
run("measure5_60_lift3_mb", worlds + "world_measure5_60_lift3.json", ("HQ_S1", "MB_S1"), wait=True)
subprocess.run([P, K + "/wait_load.py", "3"], env=env(()), cwd=D)
say("start clicks_48 chiral3 lift3")
with open(D + "/c48_chiral3_lift3_mb.out", "w") as o:
    subprocess.run(["nice", "-n", "19", P, K + "/clicks_48.py", worlds + "world_chiral3_60_lift3.json", "60", D + "/c48_chiral3_lift3_mb.json", "cube", "3"], env=env(("HQ_S1", "MB_S1")), cwd=D, stdout=o, stderr=subprocess.STDOUT)
say("done clicks_48")
say("chain done")
