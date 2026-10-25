"""mv1: the table from out/<case>.json (a reading of the records, integers): the lay, the velocity measured (the integer slope over intervals 0..10 and 10..20 in milli-Links per interval), the identity P/(2E) at the lay in milli, the band's v_g, P and the count before/after, the charge, the run back, the clicks, the bits."""
import sys, os, json
sys.set_int_max_str_digits(0)
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
band = json.load(open(os.path.join(OUT, 'band.json')))
cases = sys.argv[1:]
lines = ['| case | row (pair) | k counts | width/top | board | A | count at lay / last | v measured 0..10, 10..20 (milli-Links per interval) | P/(2E) at lay (milli) | band v_g (milli) | P_x at lay / last | W sum last (abs) | run back | births / body clicks | integers, bits, transient |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for c in cases:
    p = os.path.join(OUT, c + '.json')
    if not os.path.exists(p): lines.append('| %s | missing |' % c); continue
    d = json.load(open(p))
    if 'images' in d: continue
    lay = d['lays'][0]; rec = str(d['world']['seed'][1]['row'])
    row_index = [k for k in d['rows'][0]['rows']][0]
    first, last = d['rows'][0]['rows'][row_index], d['rows'][-1]['rows'][row_index]
    unit = lay['unit']; E = first['share']; P = first['P'][0]
    v_id = (1000 * P) // (2 * E) if E else None
    k = lay.get('wave', [0, 0, 0])[0]
    bands = band['rows'][rec]['band']; vg = bands.get(str(abs(k)), {}).get('v_g milli-Links/interval') if str(abs(k)) in bands else None
    vel = d.get('velocity row %s' % row_index, {}); wins = vel.get('axis 0 windows of 10', [])
    v01 = wins[0][0] if wins else None; v12 = wins[1][0] if len(wins) > 1 else None
    hold = 'held' if d['world'].get('control') else 'sea'
    rb = d.get('run back') or {}
    bits = max(r['bits'] for r in d['rows']); tr = max(r['transient bits'] for r in d['rows'])
    lines.append('| %s | %s (%s) | %d | %d/%d | %d-cube %s | %d | %d / %d | %s, %s | %s | %s | %d / %d | %d (%d) | %s of %s | %d / %d | %d, %d, %d |' % (
        c, rec, band['rows'][rec]['pair'][0], k, lay['width'], lay.get('top', 1), d['world']['shape'][0], hold, lay['amplitude'], first['count'][0], last['count'][0], v01, v12, v_id, vg, P, last['P'][0], last['W sum'], last['W abs'], rb.get('exact'), rb.get('intervals'), d['counts']['births'], d['counts']['body_clicks'], d['rows'][-1]['integers'], bits, tr))
open(os.path.join(OUT, 'table.md'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
# the positions of the first 12 intervals for the held cases, and the content/pace at interval 10, 20, 60 for the sea cases
for c in cases:
    p = os.path.join(OUT, c + '.json')
    if not os.path.exists(p): continue
    d = json.load(open(p))
    if 'images' in d: continue
    row_index = [k for k in d['rows'][0]['rows']][0]; vel = d.get('velocity row %s' % row_index, {})
    pos = vel.get('axis 0 positions', [])[:13]
    pace = [(r['i'], r['content min/max'], r['pace min/max']) for r in d['rows'] if r['i'] in (10, 20, 60)]
    print(c, 'x milli 0..12:', pos, 'content/pace at 10,20,60:', pace, 'nodes with share first/last:', d['rows'][0]['rows'][row_index]['nodes with share'], d['rows'][-1]['rows'][row_index]['nodes with share'])
