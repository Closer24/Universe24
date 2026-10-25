"""The time series of one record from a measure.py record: every `step`-th interval the unwrapped position (milli-Links), the peak Node and its share in units, the record's quanta, P_x and the content at the peak; the births and credits by interval. Usage: python series.py <out.json> <record> [step]"""
import sys, json
sys.set_int_max_str_digits(0)
d = json.load(open(sys.argv[1])); rec = sys.argv[2]; step = int(sys.argv[3]) if len(sys.argv) > 3 else 5
unit = d['units'][rec]
print('i | x,y,z unwrapped (milli-Links) | peak | peak share (milli-units) | quanta | P_x | content at peak | births so far | credits so far')
for row in d['rows']:
    if row['i'] % step and row['i'] != d['intervals']: continue
    r = row['records'][rec]
    print(row['i'], '|', r['unwrapped milli'], '|', r['peak'], '|', None if r['peak share'] is None else (1000 * r['peak share']) // unit, '|', r['quanta (share div unit)'], '|', r['P'][0], '|', r['content at peak'], '|', row['counts']['births'], '|', row['counts']['body_clicks'])
births = [(e['i'], e['node'], e['line_pair'], e['dP_take'], e['dP_lay']) for e in d['births']]
print('births (i, node, record, dP_take, dP_lay):', births[:12], '... total', len(births))
credits = d['credits']
print('credits:', len(credits), 'first 6 (i, node, record, sense, beat, dP_take, p_record, running cosine):', [(e['i'], e['node'], e['line'], e['sense'], e['beat'], e['dP_take'], e['frame'].get('p_record'), e['frame'].get('running_cosine')) for e in credits[:6]])
if credits:
    print('sum of dP_take over credits (per axis):', [sum(e['dP_take'][a] for e in credits) for a in range(3)], '; sum of p_record:', [sum(e['frame']['p_record'][a] for e in credits if 'p_record' in e['frame']) for a in range(3)], '; senses:', sum(e['sense'] for e in credits), 'of', len(credits))
if births:
    print('sum of dP_take over births:', [sum(e['dP_take'][a] for e in d['births']) for a in range(3)], '; sum of dP_lay:', [sum(e['dP_lay'][a] for e in d['births']) for a in range(3)], '; W_children sums:', sum(sum(e['W_children']) for e in d['births']))
print('run back:', d['run_back'], '| census:', d['rows'][-1]['census (integers, bits)'], '| transient bits:', d['rows'][-1]['max transient bits'], '| refused:', d['refused'])
