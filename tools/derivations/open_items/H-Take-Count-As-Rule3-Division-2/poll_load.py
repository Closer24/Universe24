"""Wait until the 1-minute load is below 3, polling every 60 s (the load rule). Prints the load seen."""
import time
while True:
    one = open("/proc/loadavg").read().split()[0]
    whole, frac = one.split(".")
    if int(whole) < 3:
        print("load", one); break
    print("load", one, "waiting"); time.sleep(60)
