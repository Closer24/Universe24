"""The load rule: sleep until the 1-minute load of /proc/loadavg is below the bound (default 3), polled every 60 s; no shell loop. Usage: python wait_load.py [bound]"""
import sys
import time

bound = int(sys.argv[1]) if len(sys.argv) > 1 else 3
while True:
    one = open("/proc/loadavg").read().split()[0]
    whole = int(one.split(".")[0])
    if whole < bound:
        print("load", one, "below", bound, flush=True)
        break
    print("load", one, "waiting 60 s", flush=True)
    time.sleep(60)
