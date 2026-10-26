"""Two records compared as JSON with the writer's timing field (`milliseconds`, a clock reading and no integer of the law) struck from the reader's rows; prints the equality, the fields that differ if any, and the sha256 of each stripped record.
Usage: python fd2_record_equal.py <a.json> <b.json>"""
import sys, json, hashlib
def stripped(path):
    r = json.load(open(path))
    for row in r['rows']: row.pop('milliseconds', None)
    return r
a, b = stripped(sys.argv[1]), stripped(sys.argv[2])
ja, jb = json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True)
differ = [k for k in a if json.dumps(a[k], sort_keys=True) != json.dumps(b.get(k), sort_keys=True)]
print(json.dumps({'a': sys.argv[1].split('/')[-1], 'b': sys.argv[2].split('/')[-1], 'equal without milliseconds': ja == jb, 'fields differing': differ, 'log lines': [len(a['log']), len(b['log'])], 'rows': [len(a['rows']), len(b['rows'])], 'sha256 a': hashlib.sha256(ja.encode()).hexdigest(), 'sha256 b': hashlib.sha256(jb.encode()).hexdigest()}))
