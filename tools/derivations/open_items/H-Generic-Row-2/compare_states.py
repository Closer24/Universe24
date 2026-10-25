"""gn2: David's toy and the flagged copy run side by side on one world, the state compared bit for bit at every interval (state_bytes), the logs compared line for line (the key `taken_row` and the count `met_gapped` are the copy's own and are stripped before the comparison); then N intervals back on the copy, MATCH counted.
Usage: compare_states.py <world.json> <intervals> <back> [FLAG=value ...]   (the flags are set in the environment before the copy is imported)
Prints one JSON line: the first differing interval of the state (or -1), the logs' first difference (or -1), the counts of both, the run back of the copy, the copy's integers and bits.
Integers only."""
import os, sys, json, importlib.util, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.set_int_max_str_digits(0)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    world_path, intervals, back = argv[1], int(argv[2]), int(argv[3])
    for flag in argv[4:]:
        k, v = flag.split('=')
        os.environ['GN2_' + k] = v
    david = load('lean_david', os.path.join(HERE, 'toy_former', 'lean_full.py'))
    copy = load('lean_gn2', os.path.join(HERE, 'flagged', 'lean_full.py'))
    universe, world = david.load_world(world_path)
    a = david.Lean(universe, world); b = copy.Lean(universe, world)
    first_state = -1; first_log = -1
    hashes = []
    for t in range(intervals):
        if back and t >= intervals - back: hashes.append(b.state_hash())
        a.step(); b.step()
        if first_state < 0 and a.state_bytes() != b.state_bytes(): first_state = b.interval
    la = a.log; lb = [{k: v for k, v in e.items() if k != 'taken_row'} for e in b.log if not (e.get('event') == 'refused' and e.get('cause') == 'list')]
    if len(la) != len(lb) or any(x != y for x, y in zip(la, lb)):
        first_log = next((k for k, (x, y) in enumerate(zip(la, lb)) if x != y), min(len(la), len(lb)))
    exact = 0
    for k in range(back):
        b.step_back(); exact += (b.state_hash() == hashes[back - 1 - k])
    n, bits = b.census()
    ca = {k: str(v) for k, v in a.counts.items()}; cb = {k: str(v) for k, v in b.counts.items()}
    same_counts = all(ca[k] == cb[k] for k in ca)
    print(json.dumps({'world': os.path.basename(world_path), 'intervals': intervals, 'flags': {k: v for k, v in os.environ.items() if k.startswith('GN2_')},
                      'state_first_difference': first_state, 'log_first_difference': first_log, 'log_lines': [len(la), len(lb)], 'counts_equal_on_davids_keys': same_counts,
                      'counts_david': ca, 'counts_copy': cb, 'run_back_copy': {'intervals': back, 'exact': exact}, 'integers': n, 'state_bits': bits, 'transient_bits': b.max_transient,
                      'state_sha256_copy': hashlib.sha256(b.state_bytes()).hexdigest()[:16]}))


if __name__ == '__main__':
    main(sys.argv)
