"""gn2: the kit's conservation check on the copy (the generic click, the pair emitter, the rank finders) and on the flag-off copy, the chiral seed at 60; two CLI records of the chiral seed (David's, the copy with the flags) and the former decoder on both. Each its own process."""
import os, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__)); PY = '/home/user/Universe24/venv314/bin/python'
KIT = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit/conservation_check.py'
env0 = dict(os.environ, TMPDIR='/dev/shm/tmp'); flags = dict(env0, GN2_CLICK='generic', GN2_EMIT='pair', GN2_ROWS='rank')
procs = []
def go(name, args, env):
    out = open(os.path.join(HERE, 'out', name + '.txt'), 'w')
    procs.append((name, subprocess.Popen(args, cwd=HERE, stdout=out, stderr=subprocess.STDOUT, env=env), out, time.monotonic_ns()))
go('check_flags_chiral60', [PY, KIT, 'worlds/world_chiral60.json', '60', '--toy', os.path.join(HERE, 'flagged')], flags)
go('check_off_chiral60', [PY, KIT, 'worlds/world_chiral60.json', '60', '--toy', os.path.join(HERE, 'flagged')], env0)
go('rec_david_chiral60', [PY, os.path.join(HERE, 'toy_former', 'lean_full.py'), 'worlds/world_chiral60.json', 'out/rec_david_chiral60.json', 'back', '10'], env0)
go('rec_flags_chiral60', [PY, os.path.join(HERE, 'flagged', 'lean_full.py'), 'worlds/world_chiral60.json', 'out/rec_flags_chiral60.json', 'back', '10'], flags)
for name, p, out, t0 in procs[2:]:
    p.wait(); out.close(); print(name, 'exit', p.returncode, 'ms', (time.monotonic_ns() - t0) // 1000000, flush=True)
go('dec_david_chiral60', [PY, os.path.join(HERE, 'toy_former', 'decoder_full.py'), 'out/rec_david_chiral60.json'], env0)
go('dec_flags_chiral60', [PY, os.path.join(HERE, 'toy_former', 'decoder_full.py'), 'out/rec_flags_chiral60.json'], env0)
for name, p, out, t0 in procs[:2] + procs[4:]:
    p.wait(); out.close(); print(name, 'exit', p.returncode, 'ms', (time.monotonic_ns() - t0) // 1000000, flush=True)
