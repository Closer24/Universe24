"""pm1's batch: the runner on a list of world copies, one after the other, each record to out/<name>.json and its lines to out/<name>.txt."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PY = '/home/user/Universe24/venv314/bin/python'
env = dict(os.environ, TMPDIR='/dev/shm/tmp')
for name in sys.argv[1:]:
    world = os.path.join(HERE, 'worlds', name + '.json')
    out = os.path.join(HERE, 'out', name + '.json')
    with open(os.path.join(HERE, 'out', name + '.txt'), 'w') as log:
        subprocess.run([PY, os.path.join(HERE, 'pm1_run.py'), world, out, 'back', '10'], stdout=log, stderr=subprocess.STDOUT, env=env)
    print('done', name, flush=True)
