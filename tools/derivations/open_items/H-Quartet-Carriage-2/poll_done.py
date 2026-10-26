"""H-Quartet-Carriage-2: a poller (no shell loop) that exits when chain4 (the 48) and chain5 (the flag check) have ended, or after the deadline given in seconds."""
import sys, time, os
deadline = time.time() + int(sys.argv[1])
D = "/dev/shm/tmp/qe2"
while time.time() < deadline:
    a = "CHAIN3 DONE" in open(D + "/chain4.log").read()
    b = os.path.exists(D + "/chain5.done")
    if a and b:
        print("BOTH DONE"); sys.exit(0)
    time.sleep(15)
print("DEADLINE", "chain4 done" if "CHAIN3 DONE" in open(D + "/chain4.log").read() else "chain4 running", "chain5 done" if os.path.exists(D + "/chain5.done") else "chain5 running")
