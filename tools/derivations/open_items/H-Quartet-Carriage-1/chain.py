"""H-Quartet-Carriage-1's chain: one run at a time under nice 19 and the flag HQ_S1 (qc1's final copy), the kit's wait_load before every run above a minute, the readers after each record. No shell loop."""
import os, subprocess, sys, time
P = "/home/user/Universe24/venv314/bin/python"
W = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/qe1"
K = W + "/tools/derivations/open_items/H-Kit-48-Re-Cut-1"
F = W + "/tools/derivations/open_items/H-Quartet-Carriage-1"
Q1 = W + "/tools/derivations/open_items/H-Quartet-Children-1"
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
def record(name, wait=False, back="10"):
    run([P, "-m", "event_universe.run", F + "/worlds/w_%s.json" % name, D + "/%s.json" % name, "back", back], D + "/%s.out" % name, wait)
    run([P, Q1 + "/hq_reader.py", D + "/%s.json" % name, SRC, F + "/out/%s_reading.json" % name], F + "/out/%s_reader.txt" % name)
for tag in ("p3", "p2", "m2", "m1"):
    record("chiral3_" + tag)
run([P, K + "/conservation_check.py", D + "/chiral3_p3.json", "out", F + "/out/conservation_chiral3_p3.json"], F + "/out/conservation_chiral3_p3.txt", wait=True)
record("chiral5_p3", wait=True)
record("hole5_p3", wait=True)
run([P, "-m", "event_universe.run", F + "/worlds/w_measure7_p3.json", D + "/measure7_p3.json", "back", "10"], D + "/measure7_p3.out", wait=True)
run([P, Q1 + "/measure_reader.py", D + "/measure7_p3.json", SRC, F + "/out/measure7_p3_reading.json"], F + "/out/measure7_p3_reader.txt")
run([P, Q1 + "/hq_reader.py", D + "/measure7_p3.json", SRC, F + "/out/measure7_p3_hq.json"], F + "/out/measure7_p3_hq.txt")
run([P, K + "/clicks_48.py", F + "/worlds/w_chiral3_p3.json", "60", D + "/clicks48_chiral3_p3.json", "cube", "3"], F + "/out/clicks48_chiral3_p3.txt", wait=True)
log("CHAIN DONE")
