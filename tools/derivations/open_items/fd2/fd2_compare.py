"""The kit's rule 4 for fd2's copy: David's toy (toy_david/) and fd2's folded copy (toy_fd2/) run on one world side by side, the state
hashed at every interval and compared, N intervals run back on both and compared to the kept hashes, the two records (the reader's
rows, the counts, the log) compared as JSON, and the two decoders run on the two records and their gates compared line by line.
Usage: python fd2_compare.py <world.json> <back N> <name>   (writes out/compare_<name>.json and the two records out/<name>_david.json, out/<name>_fd2.json)
Integers only (counts and hashes)."""
import sys, os, json, time, importlib.util, subprocess, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.set_int_max_str_digits(0)


def load(name, folder):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, folder, 'lean_full.py'))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def main():
    world_path, back, name = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    david = load('lean_david', 'toy_david'); fd2 = load('lean_fd2', 'toy_fd2')
    universe, world = david.load_world(world_path)
    n = int(world['intervals'])
    t0 = time.monotonic_ns()
    a = david.Lean(universe, world); b = fd2.Lean(universe, world)
    equal_hashes = 0; first_apart = None; kept_a = []; kept_b = []
    if a.state_hash() == b.state_hash(): equal_hashes += 1
    else: first_apart = 0
    for t in range(n):
        a.step(); b.step()
        ha, hb = a.state_hash(), b.state_hash()
        if t >= n - back: kept_a.append(ha); kept_b.append(hb)
        if ha == hb: equal_hashes += 1
        elif first_apart is None: first_apart = t + 1
    log_equal = json.dumps(a.log, sort_keys=True) == json.dumps(b.log, sort_keys=True)
    counts_equal = a.counts == b.counts
    census_a, census_b = a.census(), b.census()
    back_a = 0; back_b = 0; back_equal = 0
    for k in range(back):
        a.step_back(); b.step_back()
        ha, hb = a.state_hash(), b.state_hash()
        back_a += (ha == kept_a[back - 2 - k]) if back - 2 - k >= 0 else 0
        back_b += (hb == kept_b[back - 2 - k]) if back - 2 - k >= 0 else 0
        back_equal += (ha == hb)
    # the kept hashes are the states after the intervals n - back + 1 .. n; the step back from n lands on n - 1, compared to kept[back - 2]; the last step back lands on n - back, a state not kept here: counted by the record's own run back below
    t1 = time.monotonic_ns()
    # the records written by each toy's own writer, with its run back
    ra = david.record(universe, world, back, out=lambda line: None); rb = fd2.record(universe, world, back, out=lambda line: None)
    ja, jb = json.dumps(ra, sort_keys=True), json.dumps(rb, sort_keys=True)
    json.dump(ra, open(os.path.join(HERE, 'out', name + '_david.json'), 'w')); json.dump(rb, open(os.path.join(HERE, 'out', name + '_fd2.json'), 'w'))
    py = sys.executable
    ga = subprocess.run([py, os.path.join(HERE, 'toy_david', 'decoder_full.py'), os.path.join(HERE, 'out', name + '_david.json')], capture_output=True, text=True).stdout
    gb = subprocess.run([py, os.path.join(HERE, 'toy_fd2', 'decoder_full.py'), os.path.join(HERE, 'out', name + '_fd2.json')], capture_output=True, text=True).stdout
    open(os.path.join(HERE, 'out', name + '_david.gates'), 'w').write(ga); open(os.path.join(HERE, 'out', name + '_fd2.gates'), 'w').write(gb)
    result = {'world': os.path.basename(world_path), 'intervals': n, 'back': back,
              'state hash equal at intervals 0..n (David against fd2)': [equal_hashes, n + 1], 'first interval apart': first_apart,
              'log equal (JSON)': log_equal, 'counts equal': counts_equal, 'counts': {k: str(v) for k, v in a.counts.items()},
              'census David (integers per Node, max bits)': list(census_a), 'census fd2': list(census_b),
              'run back: states equal David against fd2 at every step back': [back_equal, back],
              'run back exact within the kept window (David, fd2)': [back_a, back_b, back - 1],
              'record JSON equal (rows, counts, turns, run_back, log)': ja == jb, 'record sha256 David': hashlib.sha256(ja.encode()).hexdigest(), 'record sha256 fd2': hashlib.sha256(jb.encode()).hexdigest(),
              'record run_back David': ra['run_back'], 'record run_back fd2': rb['run_back'],
              'gates equal (decoder output line by line)': ga == gb, 'gates lines': [len(ga.splitlines()), len(gb.splitlines())],
              'seconds (side by side, records)': [(t1 - t0) // 10 ** 9, (time.monotonic_ns() - t1) // 10 ** 9]}
    json.dump(result, open(os.path.join(HERE, 'out', 'compare_' + name + '.json'), 'w'), indent=1)
    print(json.dumps(result, indent=1))


if __name__ == '__main__':
    main()
