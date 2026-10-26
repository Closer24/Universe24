"""ck1: the records kept below the size limit (1,500 KB): the Node lines' currents dropped (the diag holds F per interval), the colour check's large remainder offsets replaced by their count; the readers above read the shrunk records alike."""
import json, os, sys
sys.set_int_max_str_digits(0)
for path in sys.argv[1:]:
    r = json.load(open(path))
    for d in r['nodes']:
        d.pop('current', None)
    for e in r['log']:
        if e.get('event') == 'credit':
            e.pop('frame', None)  # the credit's frame dropped (the readers read the node, the line, the sense, the levels)
    for d in r['diag']:
        for key in ('rem_offsets', 'wr_offsets'):
            o = d['colour'].get(key, {})
            for k, v in list(o.items()):
                if any(not isinstance(x, int) or abs(x) >= 100000 for x in v):
                    o[k] = f"{len(v)} offsets, large (the walls differ between the colours once X parts)"
    kept = [e for e in r['log'] if e.get('event') != 'refused']  # the refusals summed per interval in the diag's clicks; the log keeps the lays, the births and the credits
    r['log_refused_dropped'] = len(r['log']) - len(kept)
    r['log'] = kept
    json.dump(r, open(path, 'w'))
    print(path, os.path.getsize(path))
