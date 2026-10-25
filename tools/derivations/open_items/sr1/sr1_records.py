"""sr1: David's records through the flagged copy with a shape-8 row in the universe file (nothing laid on it) against the toy
without the row: the hole seed (world_toy's seed at 60 intervals), the chiral seed (world_chiral, 60 as the file and 300),
the bodies' seed (world_bodies at 120); the counts, the credits, the run back (10), the census. The row at zero levels still
enters the one-Link read of the draw (A2 reads every line of every row: its 8 remainders at the half wall are 8 more digits),
so the births may differ: measured, not assumed. python sr1_records.py
"""
from __future__ import annotations
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'toy'))
import numpy as np
import lean_sr1, lean_full
sys.set_int_max_str_digits(0)
OUT = os.path.join(HERE, 'out'); TOY = os.path.join(HERE, 'toy')


def with_row(universe):
    u = json.loads(json.dumps(universe)); heavy = [r for r in u['rows'] if r['shape'] == 2 and r['pair'][0] != r['pair'][1]][-1]
    u['rows'].append({'shape': 8, 'pair': list(heavy['pair'])}); return u


def record_of(module, universe, world, back):
    rows = []
    found = module.record(universe, world, back, out=lambda line: rows.append(line))
    log = found['log']
    credits = [e for e in log if e['event'] == 'credit']; births = [e for e in log if e['event'] == 'birth']
    return {'counts': found['counts'], 'run_back': found['run_back'], 'credits': len(credits), 'credits_by_line': {str(k): sum(1 for e in credits if e['line'] == k) for k in sorted(set(e['line'] for e in credits))},
            'births': len(births), 'births_senses_sum': sum(sum(1 if x > 0 else -1 if x < 0 else 0 for x in e['W_children']) for e in births), 'last_reading': json.loads(rows[-3]) if len(rows) >= 3 else None}


def main():
    table = {}
    for name, wfile, intervals in (('hole seed 60', 'world_toy.json', 60), ('chiral seed 60', 'world_chiral.json', 60), ('bodies seed 120', 'world_bodies.json', 120), ('chiral seed 300', 'world_chiral.json', 300)):
        world = json.load(open(os.path.join(TOY, wfile))); world['intervals'] = intervals
        universe = json.load(open(os.path.join(TOY, world['universe'])))
        toy = record_of(lean_full, universe, world, 10)
        copy_plain = record_of(lean_sr1, universe, world, 10)
        copy_row = record_of(lean_sr1, with_row(universe), world, 10)
        table[name] = {'toy': toy, 'copy, no row (bit for bit?)': copy_plain, 'copy with the shape-8 row at zero': copy_row,
                       'toy == copy without the row': toy['counts'] == copy_plain['counts'] and toy['credits'] == copy_plain['credits'],
                       'row changes the record': toy['counts'] != copy_row['counts']}
        print(json.dumps({name: table[name]}, default=str), flush=True)
        json.dump(table, open(os.path.join(OUT, 'records.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
