"""Run a test world on the src the PYTHONPATH names, N intervals forward and N back: the state's hash at the end (bit for bit against the head), the counts, the births' W, taken against booked, the run back. Usage: PYTHONPATH=<src> CA1_ODD_TAKE=<flag> python ca1_run_flagged.py <worktree> <world.json name> <N> <back N>"""
import copy, hashlib, json, os, sys, time
sys.set_int_max_str_digits(0)
W = sys.argv[1]
sys.path.insert(0, os.path.join(W, 'tests'))
from laws import node_of, run_back_exact, state_of
import event_universe
name, n, back = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
node = node_of(name)
kept = copy.deepcopy(node)
t0 = time.time()
for _ in range(n):
    node.step()
secs = int(time.time() - t0)
h = hashlib.sha256(state_of(node).encode()).hexdigest()[:16]
births = [e for e in node.log if e['event'] == 'birth']
credits = [e for e in node.log if e['event'] == 'credit']
out = {
    'src': os.path.dirname(os.path.dirname(event_universe.__file__)), 'flag': os.environ.get('CA1_ODD_TAKE', ''), 'world': name, 'intervals': n,
    'state_hash': h, 'seconds': secs,
    'counts': {k: str(v) for k, v in node.counts.items()},
    'births': len(births), 'credits': len(credits),
    'children_W_sum_0': sum(sum(b['W_children']) == 0 for b in births),
    'taken_eq_booked': sum(e['taken'] == e['booked'] for e in births),
    'taken_ge_booked': sum(e['taken'] >= e['booked'] for e in births),
    'log_hash': hashlib.sha256(json.dumps(node.log).encode()).hexdigest()[:16],
    'run_back': [run_back_exact(kept, back), back] if back else None,
}
print(json.dumps(out))
