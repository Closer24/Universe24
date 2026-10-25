"""bh2: the course of a record read from the writer's record alone (run.py's rows and Node lines): per interval the largest content on the board, the count of frozen Nodes (the Link pace 0), the Links held at the wall, the largest X (bits); per mark the max state and transient bits, the births and body clicks; the frozen content named; a compact summary written beside (the record itself dropped by the caller). Usage: python bh2_read_record.py <record.json> <summary.json>"""
import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'src_e5', 'src'))
from event_universe.core import paces
sys.set_int_max_str_digits(0)
rec = json.load(open(sys.argv[1]))
gamma = rec['gamma']
fc = paces.frozen_content(gamma)
nodes = rec['nodes']
course = []
for n in nodes:
    cmax = max(n['content'])
    course.append((n['i'], cmax, len(n['frozen']), len(n['held']), max(n['X']).bit_length()))
peak = max(course, key=lambda t: t[1])
first_frozen = next((t[0] for t in course if t[2] > 0), None)
first_wall = next((t[0] for t in course if t[3] > 0), None)
every = max(1, len(course) // 12)
out = {
 'record': os.path.basename(sys.argv[1]), 'den bits': int(rec['den']).bit_length(), 'cube': rec['cube'], 'intervals': rec['intervals'],
 'frozen content': fc,
 'largest content on the board over the run (interval, content)': [peak[0], peak[1]],
 'first interval with a frozen Node': first_frozen, 'first interval with a Link at the wall': first_wall,
 'Node-intervals frozen': sum(t[2] for t in course), 'Link-intervals at the wall': sum(t[3] for t in course),
 'course every twelfth (interval, max content, frozen Nodes, Links at the wall, max X bits)': course[::every] + [course[-1]],
 'marks (interval, max state bits, max transient bits, births, body clicks, turns, links at the wall, content max)': [(r['i'], r['max bits'], r['max transient bits'], r['births'], r['body_clicks'], r['turns'], r['links at the wall'], r['content min/mean/max'][2]) for r in rec['rows']],
 'counts': rec['counts'], 'run back': rec['run_back'],
 'horizon reached (content at or past the frozen content)': peak[1] >= fc,
}
json.dump(out, open(sys.argv[2], 'w'), indent=1)
for k, v in out.items():
    print(k, ':', v)
