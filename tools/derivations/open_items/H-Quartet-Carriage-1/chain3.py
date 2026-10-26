"""H-Quartet-Carriage-1's third chain: after the second chain's end, the chiral 5-cube at 60 on the second leg, the middle's heavy leg and the middle's first leg, and the hole 5-cube on the middle's heavy leg, each with the readers and the merger count; the kit's wait_load before each (about a minute each)."""
import os, subprocess, time
P = "/home/user/Universe24/venv314/bin/python"
W = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/qe1"
K = W + "/tools/derivations/open_items/H-Kit-48-Re-Cut-1"
F = W + "/tools/derivations/open_items/H-Quartet-Carriage-1"
Q1 = W + "/tools/derivations/open_items/H-Quartet-Children-1"
Q2 = W + "/tools/derivations/open_items/H-Quartet-Children-2"
D = "/dev/shm/tmp/qe1"
SRC = "/dev/shm/tmp/qc1/src_qc1"
env = dict(os.environ, TMPDIR="/dev/shm/tmp", PYTHONPATH=SRC, HQ_S1="1")
def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)
def run(args, out, wait=False):
    if wait:
        subprocess.run([P, K + "/wait_load.py", "3"], env=env)
    log("start", out)
    subprocess.run(["nice", "-n", "19", *args], env=env, stdout=open(out, "w"), stderr=subprocess.STDOUT, cwd=D)
    log("done", out)
while "CHAIN2 DONE" not in open(D + "/chain2.log").read():
    time.sleep(20)
for name in ("chiral5_p2", "chiral5_m2", "chiral5_m1", "hole5_m2"):
    run([P, "-m", "event_universe.run", F + "/worlds/w_%s.json" % name, D + "/%s.json" % name, "back", "10"], D + "/%s.out" % name, wait=True)
    run([P, Q1 + "/hq_reader.py", D + "/%s.json" % name, SRC, F + "/out/%s_reading.json" % name], F + "/out/%s_reader.txt" % name)
    run([P, Q2 + "/merger_after_birth.py", D + "/%s.json" % name], F + "/out/merger_after_birth_%s.txt" % name)
log("CHAIN3 DONE")
