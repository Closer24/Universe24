"""G0 (drafter G): one lane of engine runs, one process at a time, each job waiting while a full check
holds S/check.lock. argv: lane name; the jobs are read from jobs_<lane>.txt (output file, then a probe .py
and its arguments, or g1's arguments alone), the log written to queue_<lane>.txt."""
import os
import subprocess
import sys
import time

S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
G = S + '/derive/G'
PY = '/home/user/Universe24/venv314/bin/python'
lane = sys.argv[1]
with open(f'{G}/jobs_{lane}.txt', encoding='ascii') as f:
    jobs = [line.split() for line in f if line.strip()]
for out, *args in jobs:
    while os.path.exists(S + '/check.lock'):
        time.sleep(30)
    t0 = time.time()
    with open(f'{G}/{out}', 'w', encoding='ascii') as fh:
        script, rest = (args[0], args[1:]) if args and args[0].endswith('.py') else ('g1_ties.py', args)
        code = subprocess.run([PY, '-I', f'{G}/{script}', *rest], stdout=fh, stderr=subprocess.STDOUT,
                              cwd=G, timeout=5400).returncode
    with open(f'{G}/queue_{lane}.txt', 'a', encoding='ascii') as log:
        log.write(f'{out} exit {code} {time.time() - t0:.0f}s\n')
with open(f'{G}/queue_{lane}.txt', 'a', encoding='ascii') as log:
    log.write('DONE\n')
