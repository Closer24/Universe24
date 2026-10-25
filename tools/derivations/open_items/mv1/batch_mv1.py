"""mv1: the batch of measurements (a Python driver, no shell loop). Usage: python batch_mv1.py <case> ... ; writes out/<case>.json and prints one summary line per case."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)
import lean_mv1
from measure_mv1 import run, images_test
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
UNI = json.load(open(os.path.join(HERE, 'toy', 'universe_middle.json')))
SEA = {"lay": "sea", "row": 0}
HOLD = {"well": {"at": [0, 0, 0], "levels": 0, "radius": 1, "held": True}}  # the toy's control key: the metric's row held at the vacuum (content 0, every pace Gamma), a control and no lay of the law


def world(cube, intervals, lays, control=None):
    w = {"universe": "universe_middle.json", "shape": [cube] * 3, "intervals": intervals, "seed": lays}
    if control: w["control"] = control
    return w


def at(row, centre, width, n, wave=None, top=None):
    lay = {"lay": "at", "row": row, "centre": centre, "width": width, "quanta": n}
    if wave is not None: lay["wave"] = wave
    if top is not None: lay["top"] = top
    return lay


CASES = {
    # (a) the electron (row 1, the light lift) along x on the 9-cube, 60 intervals, the sea laid; k in counts of the orbit's unit (1 / Gamma radians per Link): 785 = pi/4, 1571 = pi/2, 2356 = 3pi/4, 3141 the edge
    'e_k785_sea': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125, [785, 0, 0])]), 10, 0, False),
    'e_k1571_sea': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125, [1571, 0, 0])]), 10, 0, False),
    'e_k2356_sea': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125, [2356, 0, 0])]), 10, 0, False),
    'e_k3141_sea': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125, [3141, 0, 0])]), 10, 0, False),
    'e_k1571_w3_sea': (world(9, 60, [SEA, at(1, [2, 4, 4], 3, 125, [1571, 0, 0])]), 10, 0, False),
    # the same at the vacuum's paces held (the control key): the band's velocity clean of the sea's deepening
    'e_k785_hold': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125, [785, 0, 0])], HOLD), 10, 0, False),
    'e_k1571_hold': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125, [1571, 0, 0])], HOLD), 10, 0, False),
    'e_k2356_hold': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125, [2356, 0, 0])], HOLD), 10, 0, False),
    'e_k3141_hold': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125, [3141, 0, 0])], HOLD), 10, 0, False),
    'e_k1571_w3_hold': (world(9, 60, [SEA, at(1, [2, 4, 4], 3, 125, [1571, 0, 0])], HOLD), 10, 0, False),
    'e_k1571_exact_hold': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125, [1571, 0, 0])], HOLD), 10, 0, True),
    # the heavy row (row 2, g 0.69) laid moving at its fastest k (near pi/2)
    'h_k1571_sea': (world(9, 60, [SEA, at(2, [2, 4, 4], 2, 125, [1571, 0, 0])]), 10, 0, False),
    'h_k1571_hold': (world(9, 60, [SEA, at(2, [2, 4, 4], 2, 125, [1571, 0, 0])], HOLD), 10, 0, False),
    # (b) light with a direction: the massless row (row 0) with k along x, width 2 and 3
    'l_k785_hold': (world(9, 60, [SEA, at(0, [2, 4, 4], 2, 125, [785, 0, 0])], HOLD), 10, 0, False),
    'l_k1571_hold': (world(9, 60, [SEA, at(0, [2, 4, 4], 2, 125, [1571, 0, 0])], HOLD), 10, 0, False),
    'l_k785_w3_hold': (world(9, 60, [SEA, at(0, [2, 4, 4], 3, 125, [785, 0, 0])], HOLD), 10, 0, False),
    'l_k785_sea': (world(9, 60, [SEA, at(0, [2, 4, 4], 2, 125, [785, 0, 0])]), 10, 0, False),
    'l_k1571_sea': (world(9, 60, [SEA, at(0, [2, 4, 4], 2, 125, [1571, 0, 0])]), 10, 0, False),
    # (c) the controls: no wave (David's path), wave 0 plain, wave 0 exact
    'c_nowave_sea': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125)]), 10, 0, False),
    'c_wave0_plain_sea': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125, [0, 0, 0])]), 10, 0, False),
    'c_wave0_exact_sea': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125, [0, 0, 0])]), 10, 0, True),
    # (d) the collision: two electron packets 4 Links apart laid toward each other, 60 intervals, with the sea (the clicks) and at the held vacuum
    'coll_sea': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125, [1571, 0, 0]), at(1, [6, 4, 4], 2, 125, [-1571, 0, 0])]), 10, 0, False),
    'coll_hold': (world(9, 60, [SEA, at(1, [2, 4, 4], 2, 125, [1571, 0, 0]), at(1, [6, 4, 4], 2, 125, [-1571, 0, 0])], HOLD), 10, 0, False),
    # the packet longer than its wavelength: the flat top along x (the former envelope kept by name), the vacuum held; k = pi/2 (4 Links per wavelength): top 5 on the 13-cube (7 Nodes along x), top 9 on the 15-cube (11 Nodes); light the same
    'e_k1571_top5_hold': (world(13, 40, [SEA, at(1, [3, 6, 6], 2, 125, [1571, 0, 0], 5)], HOLD), 5, 0, False),
    'e_k1571_top9_hold': (world(15, 40, [SEA, at(1, [4, 7, 7], 2, 125, [1571, 0, 0], 9)], HOLD), 5, 0, False),
    'l_k1571_top5_hold': (world(13, 40, [SEA, at(0, [3, 6, 6], 2, 125, [1571, 0, 0], 5)], HOLD), 5, 0, False),
    'e_k785_top9_hold': (world(15, 40, [SEA, at(1, [4, 7, 7], 2, 125, [785, 0, 0], 9)], HOLD), 5, 0, False),
    'h_k1571_top5_hold': (world(13, 40, [SEA, at(2, [3, 6, 6], 2, 125, [1571, 0, 0], 5)], HOLD), 5, 0, False),
    # the 48 on the 7-cube: the electron with k along x, 12 intervals; the collision 10 intervals
    'img_e_k1571': (world(7, 12, [SEA, at(1, [1, 3, 3], 2, 125, [1571, 0, 0])]), 0, 12, False),
    'img_coll': (world(7, 10, [SEA, at(1, [1, 3, 3], 2, 125, [1571, 0, 0]), at(1, [5, 3, 3], 2, 125, [-1571, 0, 0])]), 0, 10, False),
}

for name in sys.argv[1:]:
    w, back, images, exact = CASES[name]
    lean_mv1.PLAIN_LAY = not exact
    json.dump(w, open(os.path.join(OUT, 'world_%s.json' % name), 'w'))
    t0 = time.monotonic()
    w_run = dict(w); w_run['universe'] = os.path.join(HERE, 'toy', 'universe_middle.json')
    if images:
        res = {'world': w, 'images': images_test(UNI, w, images)}
    else:
        res, b = run(UNI, w, int(w['intervals']), back)
        for e in res.get('births', []): pass
    res['plain_lay'] = not exact; res['seconds'] = int(time.monotonic() - t0)
    json.dump(res, open(os.path.join(OUT, '%s.json' % name), 'w'), default=str)
    if images:
        print(name, json.dumps(res['images'])); continue
    first, last = res['rows'][0], res['rows'][-1]
    summary = {'case': name, 'lays': [(l['amplitude'], l['share'] // l['unit'], l.get('wave')) for l in res['lays']], 'run back': res.get('run back'), 'counts': {k: res['counts'][k] for k in ('births', 'body_clicks', 'turns', 'taken', 'booked')},
               'content last': last['content min/max'], 'pace last': last['pace min/max'], 'bits': max(r['bits'] for r in res['rows']), 'transient': max(r['transient bits'] for r in res['rows']), 'integers': last['integers'], 'seconds': res['seconds']}
    for rec in sorted(first['rows']):
        f, l = first['rows'][rec], last['rows'][rec]
        v = res.get('velocity row %s' % rec, {})
        summary['row ' + rec] = {'count first/last': [f['count'][0], l['count'][0]], 'P first': f['P'], 'P last': l['P'], 'W sum first/last': [f['W sum'], l['W sum']], 'W abs last': l['W abs'],
                                 'v x windows': v.get('axis 0 windows of 10'), 'x positions 0..20': v.get('axis 0 positions', [])[:21], 'nodes with share first/last': [f['nodes with share'], l['nodes with share']]}
    print(json.dumps(summary, default=str))
