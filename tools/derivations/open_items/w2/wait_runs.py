"""W2: wait until every named log holds its summary line (a tool of the hand, no reading)."""
import sys, time
paths = sys.argv[1:]
while True:
    done = [p for p in paths if '"summary"' in open(p).read()]
    if len(done) == len(paths):
        print("done", done)
        break
    time.sleep(5)
