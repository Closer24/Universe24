"""ck1's record reader: per record the first interval each line fails the colour check, the X course at marks, the turns, the light's current, the clicks per colour and line, the run back; with a second record, the X per interval compared bit for bit."""
import json, sys
sys.set_int_max_str_digits(0)
def read(path, marks=(1,2,3,4,5,6,7,8,10,15,20,40,60,89,100,150,170,182,189,190,200,250,300,350,400)):
    r = json.load(open(path))
    diag = r['diag']
    print(f"\n## {path}: counts {r['counts']}, run back {r['run_back']}, turns {r['turns'][:12]}{' ...' if len(r['turns'])>12 else ''} (total {len(r['turns'])} turn intervals), first_parting {r['first_parting']}")
    first = {}
    for d in diag:
        for name in d['colour']['levels_failed']:
            first.setdefault(name, d['i'])
    print("first interval each line fails the colour check:", dict(sorted(first.items(), key=lambda kv: kv[1])))
    e_nonzero = [d['i'] for d in diag if d['e_max'] > 0]
    print("e > 0 first at", e_nonzero[:1], "intervals with e 0:", sum(1 for d in diag if d['e_max']==0), "of", len(diag), "; X_min==X_max at", sum(1 for d in diag if d['X_min']==d['X_max']))
    f_nz = [d['i'] for d in diag if d['F_abs_max'] > 0]
    print("F != 0 first at", f_nz[:1], "intervals with F 0 on every Link:", sum(1 for d in diag if d['F_links_zero']==192), "; twist nonzero links max", max(d['twist_links_nonzero'] for d in diag), "; light whole at 64 Nodes at", sum(1 for d in diag if d['light_nodes_whole']==64), "intervals; bits max", max(d['bits'] for d in diag))
    print("| i | X mean | even | odd | e | turned | F max | u max | light lvl | light share hundredths | whole | laid | clicks |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for d in diag:
        if d['i'] in marks or d['turned'] or d['clicks']:
            if d['i'] in marks or d['turned'] or (d['clicks'] and d['i'] < 420):
                print(f"| {d['i']} | {d['X_mean']} | {d['X_even_mean']} | {d['X_odd_mean']} | {d['e_max']} | {d['turned']} ({d['turned_even']} even) | {d['F_abs_max']} | {d['u_abs_max']} | {d['light_level_min_max']} | {d['light_share_min_max_hundredths']} | {d['light_nodes_whole']} | {d['counts']['laid']} | {d['clicks']} |")
    offs = {}
    for d in diag:
        for k, v in d['colour']['rem_offsets'].items():
            if all(isinstance(x, int) and abs(x) < 1000 for x in v):
                offs.setdefault(k, set()).update(v)
        for k, v in d['colour']['wr_offsets'].items():
            if all(isinstance(x, int) and abs(x) < 1000 for x in v):
                offs.setdefault('wr:'+k, set()).update(v)
    print("small remainder offsets seen (two's complement test; the odd lines' expected -2 or +2 after a turn):", {k: sorted(v) for k, v in offs.items()})
    return r
def compare(a, b):
    xa = [d['X'] for d in a['nodes']]; xb = [d['X'] for d in b['nodes']]
    same = sum(1 for p, q in zip(xa, xb) if p == q)
    print(f"X per Node per interval equal: {same} of {min(len(xa), len(xb))}; turns equal: {a['turns']==b['turns']}; counts equal: {a['counts']==b['counts']}")
    for i in (6, 7, 8):
        print(f"  i={i}: this X set {sorted(set(xa[i-1]))}, other {sorted(set(xb[i-1]))}")
if __name__ == '__main__':
    recs = [read(p) for p in sys.argv[1:] if not p.startswith('cmp:')]
    cmps = [p[4:] for p in sys.argv[1:] if p.startswith('cmp:')]
    if cmps:
        other = json.load(open(cmps[0])); compare(recs[0], other)
