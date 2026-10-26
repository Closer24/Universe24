"""H-Quartet-Carriage-2's last chain: after chain4's end (polled every 20 s; no shell loop), the kit's check that the flagged copy with the flag empty runs the hole 60 and the chiral 60 bit for bit with the head (about 50 s), after the kit's wait_load."""
import os, subprocess, time
P = "/home/user/Universe24/venv314/bin/python"
W = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/qe2"
K = W + "/tools/derivations/open_items/H-Kit-48-Re-Cut-1"
Q1 = W + "/tools/derivations/open_items/H-Quartet-Children-1"
D = "/dev/shm/tmp/qe2"
env = dict(os.environ, TMPDIR="/dev/shm/tmp", PYTHONPATH=W + "/src")
while "CHAIN3 DONE" not in open(D + "/chain4.log").read():
    time.sleep(20)
subprocess.run([P, K + "/wait_load.py", "3"], env=env)
with open(D + "/flag_check.out", "w") as out:
    subprocess.run(["nice", "-n", "19", P, K + "/make_flagged_copy.py", "qe2chk", "HQ_S1", Q1 + "/hq_s1_replacements.json", "src", W + "/src", "python", P], env=env, stdout=out, stderr=subprocess.STDOUT, cwd=D)
open(D + "/chain5.done", "w").write("CHAIN5 DONE\n")
