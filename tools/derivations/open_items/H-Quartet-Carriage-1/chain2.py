"""H-Quartet-Carriage-1's second chain: after the first chain's end (polled every 20 s, no shell loop), the measurement world on the 5-cube at 60 with the third lift's pair (the 7-cube's run ended at the interval 15 with no record), then its readers."""
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
while "CHAIN DONE" not in open(D + "/chain.log").read():
    time.sleep(20)
run([P, "-m", "event_universe.run", F + "/worlds/w_measure5_p3.json", D + "/measure5_p3.json", "back", "10"], D + "/measure5_p3.out", wait=True)
run([P, Q1 + "/measure_reader.py", D + "/measure5_p3.json", SRC, F + "/out/measure5_p3_reading.json"], F + "/out/measure5_p3_reader.txt")
run([P, Q1 + "/hq_reader.py", D + "/measure5_p3.json", SRC, F + "/out/measure5_p3_hq.json"], F + "/out/measure5_p3_hq.txt")
run([P, F + "/axis_track_reader.py", D + "/measure5_p3.json", F + "/out/axis_track_measure5_p3.json"], F + "/out/axis_track_measure5_p3.txt")
run([P, Q2 + "/merger_after_birth.py", D + "/measure5_p3.json"], F + "/out/merger_after_birth_measure5_p3.txt")
log("CHAIN2 DONE")
