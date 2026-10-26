"""gn1: compare two records of the toy (base against a variant): the counts, the reader's rows' course, the log (its hash), the run back, the births' charge and take, the integers and bits.
Usage: python compare.py <base.json> <variant.json> [label]"""
import sys, json, hashlib
sys.set_int_max_str_digits(0)
a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2])); label = sys.argv[3] if len(sys.argv) > 3 else sys.argv[2]


def digest(x): return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()[:16]
def course(r): return [(x['i'], x['births'], x['body_clicks'], x['turns'], x['volume mean'], x['content min/mean/max'][1], x['W total']) for x in r['rows']]
def laws(r):
    births = [l for l in r['log'] if l['event'] == 'birth']; credits = [l for l in r['log'] if l['event'] == 'credit']; lights = [l for l in r['log'] if l['event'] == 'light']
    taken = sum(x['taken'] for x in births) + sum(x['taken'] for x in credits) + sum(x.get('taken', 0) for x in lights)
    booked = sum(x['booked'] for x in births) + sum(1 for x in credits) * 0  # the credits' booking is one unit of the record each; read from the counts below
    return {'births': len(births), 'body credits': len(credits), 'light credits': len(lights), 'senses sum (charge)': sum(s for x in births for s in x['senses']),
            'taken >= booked on every birth': all(x['taken'] >= x['booked'] for x in births), 'taken total (births+credits)': str(taken), 'booked at births': str(sum(x['booked'] for x in births)),
            'rooms bits (entropy H)': sum((int(x['room']) - 1).bit_length() for x in births if 'room' in x),
            'run back': r['run_back'], 'integers per Node': sorted({x['integers'] for x in r['rows']}), 'max state bits': max(x['max bits'] for x in r['rows']), 'max transient bits': max(x['max transient bits'] for x in r['rows'])}


print(json.dumps({'compare': label, 'counts equal': a['counts'] == b['counts'], 'course equal': course(a) == course(b), 'log equal': a['log'] == b['log'], 'log digest base/variant': [digest(a['log']), digest(b['log'])]}))
print(json.dumps({'base counts': a['counts']}))
print(json.dumps({'variant counts': b['counts']}))
ca, cb = course(a), course(b)
first = next((k for k, (x, y) in enumerate(zip(ca, cb)) if x != y), None)
print(json.dumps({'course (i, births, body_clicks, turns, volume mean, content mean, W total)': {'base': ca, 'variant': cb, 'first differing mark': None if first is None else ca[first][0]}}))
print(json.dumps({'laws base': laws(a)}))
print(json.dumps({'laws variant': laws(b)}))
