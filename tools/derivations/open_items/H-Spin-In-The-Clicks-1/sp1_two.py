"""sp1 (2026-10-25): two quanta of one record against two records, on David's lean toy (the copy under toy/, run and never edited).

The question of the brief's item 3: do two quanta of one pair at one Node add in amplitude (a boson's pile) or refuse one
Node (the exclusion)? Measured: (a) one record, one lay of 2 quanta (width 2); (b) one record, two lays of 1 quantum each at
one centre, the same sense (the amplitudes add: the share is quadratic); (c) one record, 1 quantum of each sense at one centre
(the im lines cancel: a real record, W = 0); (d) two records (the file's rows 1 and 2), 1 quantum each at one centre; (e) one
quantum alone, the reference. Read in integers: the record's count in units at the lay and at the end, the W total, the
credits (count, beats, senses) over the intervals, the births and the lay refusals; the run back exact.
Also the births' refusal of the toy's close read from the log of the emergence seed (a sea with a hole) over the intervals:
how many lays were refused because the child's family stood at the Node, and whether that refusal reads the sense (it does
not: `refuse` tests the standing share owns[s_] > 0 at either end, the sign of W unread).
Usage: python sp1_two.py <cube> <intervals> <back>"""
from __future__ import annotations
import sys, os, json, argparse, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'toy'))
import numpy as np
import sp1_sg
from lean_full import Lean, wronskian

sys.set_int_max_str_digits(0)
cube, intervals, back = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
universe = json.load(open(os.path.join(HERE, 'toy', 'universe_middle.json')))
centre = (cube // 2,) * 3


def fresh(seed):
    world = {'universe': 'universe_middle.json', 'shape': [cube, cube, cube], 'intervals': intervals, 'seed': seed}
    return Lean(universe, world)


def measure(name, b, recs, lays):
    """`lays`: a list of (record index in the file, sense, quanta); the run; the readings per record."""
    laid = []
    for row, sense, n in lays:
        rec = b.records().index(b.by_index[row]); A, share = sp1_sg.one_sense_packet(b, rec, centre, 2, n, sense); laid.append({'row': row, 'rec': rec, 'sense': sense, 'quanta': n, 'amplitude': A, 'share': share, 'unit': b.units[rec]})
    start = {rec: sp1_sg.reader(b, rec) for rec in recs}
    hashes = []
    for t in range(intervals):
        if back and t >= intervals - back: hashes.append(sp1_sg.state_hash(b))
        b.step()
    end = {rec: sp1_sg.reader(b, rec) for rec in recs}
    credits = [e for e in b.log if e['event'] == 'credit']
    out = {'run': name, 'lays': laid}
    for rec in recs:
        cr = [c for c in credits if c['line'] == rec]
        out['rec%d' % rec] = {'count_units_start': start[rec]['count_units'], 'count_rem_start': start[rec]['count_rem'], 'count_units_end': end[rec]['count_units'], 'W_total_start': start[rec]['W_total'], 'W_total_end': end[rec]['W_total'],
                              'W_abs_end': end[rec]['W_abs'], 'nodes_at_or_above_one_unit_start': start[rec]['nodes_at_or_above_one_unit'], 'nodes_at_or_above_one_unit_end': end[rec]['nodes_at_or_above_one_unit'],
                              'credits': len(cr), 'credits_s+1': sum(1 for c in cr if c['sense'] == 1), 'credits_s-1': sum(1 for c in cr if c['sense'] == -1), 'credits_s0': sum(1 for c in cr if c['sense'] == 0),
                              'beats': sorted(set(c['beat'] for c in cr)), 'first_credit_interval': (cr[0]['i'] if cr else None)}
    out['births'] = b.counts['births']; out['refused_lay'] = b.counts['refused_lay']; out['taken_booked'] = [b.counts['taken'], b.counts['booked']]; out['turns'] = b.counts['turns']
    n_int, bits = b.census(); out['integers'] = n_int; out['max_bits'] = bits; out['max_transient_bits'] = b.max_transient
    if back:
        exact = 0
        for k in range(back):
            b.step_back(); exact += (sp1_sg.state_hash(b) == hashes[back - 1 - k])
        out['run_back'] = {'intervals': back, 'exact': exact}
    print(json.dumps(out), flush=True)
    return out


sea = [{'lay': 'sea', 'row': 0}]
rows = []
b = fresh(sea); r2 = b.records().index(b.by_index[2]); r1 = b.records().index(b.by_index[1])
rows.append(measure('e_one_quantum_row2_s+1', fresh(sea), [r2], [(2, 1, 1)]))
rows.append(measure('a_two_quanta_one_lay_row2_s+1', fresh(sea), [r2], [(2, 1, 2)]))
rows.append(measure('b_one_plus_one_same_sense_row2', fresh(sea), [r2], [(2, 1, 1), (2, 1, 1)]))
rows.append(measure('c_one_plus_one_opposite_senses_row2', fresh(sea), [r2], [(2, 1, 1), (2, -1, 1)]))
rows.append(measure('d_one_each_rows1_and_2_s+1', fresh(sea), [r1, r2], [(1, 1, 1), (2, 1, 1)]))
rows.append(measure('f_four_quanta_one_lay_row2_s+1', fresh(sea), [r2], [(2, 1, 4)]))
# the births' refusal on the emergence seed (a sea with a hole and one quantum more beside it), the log's causes counted
world = {'universe': 'universe_middle.json', 'shape': [cube, cube, cube], 'intervals': intervals, 'seed': [{'lay': 'sea', 'row': 0}, {'lay': 'hole', 'at': [0, 0, 0]}, {'lay': 'at', 'row': 0, 'centre': [1, 0, 0], 'quanta': 1}]}
e = Lean(universe, world)
for t in range(intervals): e.step()
refusals = [x for x in e.log if x['event'] == 'refused']
by_cause = {}
for x in refusals: by_cause[x['cause']] = by_cause.get(x['cause'], 0) + 1
standing = [x for x in refusals if x['cause'] == 'lay' and 'standing' in x]
crowded = [x for x in refusals if x['cause'] == 'lay' and 'children_at_one_node' in x]
births = [x for x in e.log if x['event'] == 'birth']
emergence = {'run': 'emergence_seed', 'births': len(births), 'refusals_by_cause': by_cause, 'refused_lay_family_standing': len(standing), 'refused_lay_two_children_one_node': len(crowded),
             'births_senses_sum': sum((w > 0) - (w < 0) for x in births for w in x['W_children']), 'births_children_opposite_signs': sum(1 for x in births if len(x['W_children']) == 2 and x['W_children'][0] * x['W_children'][1] < 0),
             'standing_shares_at_refusal_min_max_in_units': ([min(x['standing'] for x in standing) // standing[0]['unit'], max(x['standing'] for x in standing) // standing[0]['unit']] if standing else None),
             'refuse_reads_sense': 'no: lean_full.refuse tests owns[s_][minus] > 0 or owns[s_][plus] > 0, the share at the vacuum weight, a sum of squares; the sign of W enters nowhere'}
print(json.dumps(emergence), flush=True); rows.append(emergence)
json.dump(rows, open(os.path.join(HERE, 'out', 'two_quanta_c%d_i%d.json' % (cube, intervals)), 'w'))
