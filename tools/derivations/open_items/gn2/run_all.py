"""gn2's runner: every comparison as its own process (no shell loop), the outputs under out/; prints each job's line when done."""
import os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); PY = '/home/user/Universe24/venv314/bin/python'
env0 = dict(os.environ, TMPDIR='/dev/shm/tmp')
jobs = [  # name, args of compare_states (world, intervals, back, flags...)
    ('off_hole60', ['worlds/world_hole60.json', '60', '10']),
    ('turn_all_hole60', ['worlds/world_hole60.json', '60', '10', 'TURN=all']),
    ('turn_scaled_hole60', ['worlds/world_hole60.json', '60', '10', 'TURN=scaled']),
    ('emit_pair_hole60', ['worlds/world_hole60.json', '60', '10', 'EMIT=pair']),
    ('click_generic_hole60', ['worlds/world_hole60.json', '60', '10', 'CLICK=generic']),
    ('rows_rank_hole60', ['worlds/world_hole60.json', '60', '10', 'ROWS=rank']),
    ('all_on_hole60', ['worlds/world_hole60.json', '60', '10', 'EMIT=pair', 'CLICK=generic', 'ROWS=rank', 'TURN=scaled']),
    ('off_chiral300', ['worlds/world_chiral300.json', '300', '10']),
    ('click_generic_chiral300', ['worlds/world_chiral300.json', '300', '10', 'CLICK=generic']),
    ('turn_all_chiral300', ['worlds/world_chiral300.json', '300', '10', 'TURN=all']),
    ('turn_scaled_chiral300', ['worlds/world_chiral300.json', '300', '10', 'TURN=scaled']),
    ('off_bodies120', ['worlds/world_bodies120.json', '120', '10']),
    ('click_generic_bodies120', ['worlds/world_bodies120.json', '120', '10', 'CLICK=generic']),
    ('turn_scaled_bodies120', ['worlds/world_bodies120.json', '120', '10', 'TURN=scaled']),
]
procs = []
for name, args in jobs:
    out = open(os.path.join(HERE, 'out', name + '.json'), 'w')
    procs.append((name, subprocess.Popen([PY, os.path.join(HERE, 'compare_states.py')] + args, cwd=HERE, stdout=out, stderr=subprocess.STDOUT, env=env0), out, time.monotonic_ns()))
# the flagged CLI records for the decoder and the gapped sea (the copy's own path)
cli = [
    ('rec_david_hole60', dict(env0), os.path.join(HERE, 'toy_former', 'lean_full.py'), 'worlds/world_hole60.json'),
    ('rec_click_generic_hole60', dict(env0, GN2_CLICK='generic'), os.path.join(HERE, 'flagged', 'lean_full.py'), 'worlds/world_hole60.json'),
    ('rec_turn_scaled_hole60', dict(env0, GN2_TURN='scaled'), os.path.join(HERE, 'flagged', 'lean_full.py'), 'worlds/world_hole60.json'),
    ('rec_sea_gapped_node10', dict(env0, GN2_SEA='named'), os.path.join(HERE, 'flagged', 'lean_full.py'), 'worlds/world_sea_gapped.json'),
    ('rec_sea_gapped_click_node10', dict(env0, GN2_SEA='named', GN2_CLICK='generic'), os.path.join(HERE, 'flagged', 'lean_full.py'), 'worlds/world_sea_gapped.json'),
]
for name, env, script, world in cli:
    out = open(os.path.join(HERE, 'out', name + '.txt'), 'w')
    procs.append((name, subprocess.Popen([PY, script, world, os.path.join(HERE, 'out', name + '.json'), 'back', '10'], cwd=HERE, stdout=out, stderr=subprocess.STDOUT, env=env), out, time.monotonic_ns()))
for name, p, out, t0 in procs:
    p.wait(); out.close()
    print(name, 'exit', p.returncode, 'ms', (time.monotonic_ns() - t0) // 1000000, flush=True)
