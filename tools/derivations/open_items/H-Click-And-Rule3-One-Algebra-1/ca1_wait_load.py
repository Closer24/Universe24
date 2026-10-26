"""Poll /proc/loadavg every 60 s (no shell loop) until the 1-minute load is below the bound, then run the command given; gives up after the minutes named. Usage: python ca1_wait_load.py <bound> <max minutes> -- <command...>"""
import subprocess, sys, time
bound, minutes = int(sys.argv[1]), int(sys.argv[2])
cmd = sys.argv[sys.argv.index('--') + 1:]
for k in range(minutes):
    load = open('/proc/loadavg').read().split()[0]
    whole = int(load.split('.')[0])
    if whole < bound:
        print('load', load, 'under', bound, 'after', k, 'minutes; running', flush=True)
        sys.exit(subprocess.call(cmd))
    time.sleep(60)
print('gave up: the load stayed at or above', bound, 'for', minutes, 'minutes', flush=True)
sys.exit(3)
