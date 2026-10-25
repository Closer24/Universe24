"""fd1's runner: one toy (David's folder or the flagged copy's) run on one world with the run back, the record's identity taken bit for bit (the state hash at the end of the forward run, the log's sha256, the counts, the census), and, with `readings`, the integer readings of the unifications on the run: the ties of the odd rounding against the half-up (cphi = phi p_0 at the start), the Wronskian at every turned Node before and after the exchange, the wall identity 2 w = S + D + SUM R at every Node, the current's antisymmetry F_ij + F_ji = 0 on every Link, the remainders at 0 at the end.
Usage: python compare_fd1.py <toy dir> <world.json> <out.json> [back N] [readings]
Integers only."""
import sys, os, json, hashlib, time, importlib.util
sys.set_int_max_str_digits(0)
toy_dir, world_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
back = int(sys.argv[sys.argv.index('back') + 1]) if 'back' in sys.argv else 0
want = 'readings' in sys.argv
spec = importlib.util.spec_from_file_location('lean_full', os.path.join(toy_dir, 'lean_full.py'))
LF = importlib.util.module_from_spec(spec); sys.modules['lean_full'] = LF; spec.loader.exec_module(LF)
import numpy as np
from event_universe.core import paces

universe, world = LF.load_world(world_path)
b = LF.Lean(universe, world)
n = int(world['intervals']); t0 = time.monotonic_ns()
hashes = []; maxbits = 0
R = {'ties negative (odd rounding differs from half up)': 0, 'ties positive (the two agree)': 0, 'turned Node-records': 0, 'W kept at the turned Node': 0, 'wall identity 2w = S + D + sum R held at Nodes': 0, 'wall identity Nodes': 0, 'Links with F_ij + F_ji = 0': 0, 'Links': 0}
gamma = b.gamma
for t in range(n):
    if want:
        phi = b.row(4).lines[0].now; c = b.content(); p0 = paces.clock_of(gamma, c)
        x = phi * p0
        for v in np.asarray(x, dtype=object).reshape(-1):
            v = int(v)
            if (2 * v) % (2 * gamma) == gamma:
                if v < 0: R['ties negative (odd rounding differs from half up)'] += 1
                else: R['ties positive (the two agree)'] += 1
        factors = b.link_factors(); massless = b.row(2, gap=0); r = b.rule(massless.pair, c, factors)
        ok = (2 * r.wall == r.self_coefficient + r.mass + sum(r.reaches))
        R['wall identity 2w = S + D + sum R held at Nodes'] += int(np.sum(np.asarray(ok, dtype=object).astype(int))) if np.ndim(ok) else int(bool(ok)) * int(np.prod(b.shape))
        R['wall identity Nodes'] += int(np.prod(b.shape))
        z = massless.lines[0]
        for a in range(3):
            fp = b.link_current(z, 2 * a); fm = b.link_current(z, 2 * a + 1)
            s = fp + LF.across(fm, 2 * a)
            R['Links with F_ij + F_ji = 0'] += int(sum(1 for v in s.reshape(-1) if int(v) == 0)); R['Links'] += int(s.size)
        pre = [(l.now.copy(), l.before.copy()) for rec in b.records() for l in rec.lines]
    if back and t >= n - back: hashes.append(b.state_hash())
    b.step(); maxbits = max(maxbits, b.census()[1])
    if want and b.turned.any():
        for k, rec in enumerate(b.records()):
            re0n, re0b = pre[2 * k]; im0n, im0b = pre[2 * k + 1]
            W_pre = re0n * im0b - im0n * re0b; W_post = LF.wronskian(*rec.lines)
            for at in zip(*np.nonzero(b.turned)):
                R['turned Node-records'] += 1; R['W kept at the turned Node'] += int(int(W_pre[at]) == int(W_post[at]))
state_hash = b.state_hash(); log_sha = hashlib.sha256(json.dumps(b.log, sort_keys=True).encode()).hexdigest()
zeros = sum(int(sum(1 for v in l.rem.reshape(-1) if int(v) == 0)) for l in b.all_lines())
exact = 0
for k in range(back):
    b.step_back(); exact += (b.state_hash() == hashes[back - 1 - k])
out = {'toy': toy_dir, 'world': world_path, 'intervals': n, 'flag': world.get('control', {}).get('fd1'), 'state hash at the end': state_hash, 'log sha256': log_sha, 'log lines': len(b.log) if not back else None, 'counts': {k: int(v) for k, v in b.counts.items()}, 'integers per Node': b.census()[0], 'max state bits': maxbits, 'max transient bits': b.max_transient, 'run back': {'intervals': back, 'exact': exact}, 'remainders at 0 at the end (where w - r would fail the mirror)': zeros, 'seconds': (time.monotonic_ns() - t0) // 10 ** 9}
if want: out['readings'] = R
if getattr(b, 'ties', None) is not None: out['ties'] = b.ties
json.dump(out, open(out_path, 'w'), indent=1); print(json.dumps(out))
