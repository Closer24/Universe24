"""sp1: the pile in the clicks. One record of N quanta in one lay against two lays of N/2 in phase (the same sense) and two lays
of N/2 of opposite senses at one centre (width 3, the body laid over its packet, a sea beneath): the counts in units, the W total,
the credits (count, senses, beats) over the intervals; the run back exact. Integers only.
Usage: python sp1_two_clicks.py <cube> <intervals> <back> <N>"""
from __future__ import annotations
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'toy'))
import sp1_sg
from lean_full import Lean

sys.set_int_max_str_digits(0)
cube, intervals, back, N = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
universe = json.load(open(os.path.join(HERE, 'toy', 'universe_middle.json')))
centre = (cube // 2,) * 3
sea = [{'lay': 'sea', 'row': 0}]


def fresh():
    return Lean(universe, {'universe': 'universe_middle.json', 'shape': [cube, cube, cube], 'intervals': intervals, 'seed': sea})


def measure(name, lays):
    b = fresh(); rec = b.records().index(b.by_index[2]); laid = []
    for sense, n in lays:
        A, share = sp1_sg.one_sense_packet(b, rec, centre, 3, n, sense); laid.append({'sense': sense, 'quanta': n, 'amplitude': A, 'share': share})
    start = sp1_sg.reader(b, rec); hashes = []
    for t in range(intervals):
        if back and t >= intervals - back: hashes.append(sp1_sg.state_hash(b))
        b.step()
    end = sp1_sg.reader(b, rec)
    cr = [e for e in b.log if e['event'] == 'credit' and e['line'] == rec]
    beats = {}
    for c in cr: beats[c['beat']] = beats.get(c['beat'], 0) + 1
    out = {'run': name, 'unit': b.units[rec], 'lays': laid, 'count_units_start': start['count_units'], 'count_units_end': end['count_units'], 'W_total_start': start['W_total'], 'W_total_end': end['W_total'], 'W_abs_end': end['W_abs'],
           'nodes_at_or_above_one_unit_start': start['nodes_at_or_above_one_unit'], 'credits': len(cr), 'credits_s+1': sum(1 for c in cr if c['sense'] == 1), 'credits_s-1': sum(1 for c in cr if c['sense'] == -1), 'credits_s0': sum(1 for c in cr if c['sense'] == 0),
           'beats_histogram': dict(sorted(beats.items())), 'first_credit_interval': (cr[0]['i'] if cr else None), 'births': b.counts['births'], 'refused_lay': b.counts['refused_lay'], 'taken_booked': [b.counts['taken'], b.counts['booked']], 'turns': b.counts['turns']}
    n_int, bits = b.census(); out['integers'] = n_int; out['max_bits'] = bits; out['max_transient_bits'] = b.max_transient
    if back:
        exact = 0
        for k in range(back):
            b.step_back(); exact += (sp1_sg.state_hash(b) == hashes[back - 1 - k])
        out['run_back'] = {'intervals': back, 'exact': exact}
    print(json.dumps(out), flush=True); return out


rows = [measure('one_lay_N_s+1', [(1, N)]), measure('one_lay_N_half_s+1', [(1, N // 2)]), measure('two_lays_N_half_same_sense', [(1, N // 2), (1, N // 2)]),
        measure('two_lays_N_half_opposite_senses', [(1, N // 2), (-1, N // 2)]), measure('one_lay_2N_s+1', [(1, 2 * N)]), measure('two_lays_N_quarter_same_sense', [(1, N // 4), (1, N // 4)])]
json.dump(rows, open(os.path.join(HERE, 'out', 'two_clicks_c%d_i%d_N%d.json' % (cube, intervals, N)), 'w'))
