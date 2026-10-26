"""The measurement batch (a script, no shell loop): measure.py on every world named on the command line, each output to out/<name>.json and the summary lines to out/<name>.txt. Usage: python run_batch.py <name> [<name> ...]"""
import sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
py = sys.executable
for name in sys.argv[1:]:
    world = os.path.join(HERE, 'worlds', name + '.json'); out = os.path.join(HERE, 'out', name + '.json')
    found = subprocess.run([py, os.path.join(HERE, 'measure.py'), world, out], capture_output=True, text=True)
    lines = [l for l in (found.stdout + found.stderr).splitlines() if not l.startswith('interval')]
    open(os.path.join(HERE, 'out', name + '.txt'), 'w').write('\n'.join(lines) + '\n')
    print(name, 'done', 'rc', found.returncode, flush=True)
