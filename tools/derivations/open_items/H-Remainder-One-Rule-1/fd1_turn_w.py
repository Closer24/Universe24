"""fd1: the Wronskian at every turned Node before and after the exchange on a record, and where it differs whether the close laid a child at that Node in the same interval (the lay after the swap). Usage: python fd1_turn_w.py <toy dir> <world.json> <out.json>"""
import sys, os, json, importlib.util
sys.set_int_max_str_digits(0)
toy_dir, world_path, out_path = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('lean_full', os.path.join(toy_dir, 'lean_full.py')); LF = importlib.util.module_from_spec(spec); sys.modules['lean_full'] = LF; spec.loader.exec_module(LF)
import numpy as np
universe, world = LF.load_world(world_path); b = LF.Lean(universe, world)
kept = 0; apart = 0; apart_laid = 0; apart_free = []
for t in range(int(world['intervals'])):
    pre = [(l.now.copy(), l.before.copy()) for rec in b.records() for l in rec.lines]; log_from = len(b.log)
    b.step()
    if not b.turned.any(): continue
    laid = set()
    for e in b.log[log_from:]:
        if e['event'] == 'birth': laid.add((e['line_pair'], tuple(e['minus']))); laid.add((e['line_pair'], tuple(e['plus'])))
    for k, rec in enumerate(b.records()):
        W_pre = pre[2 * k][0] * pre[2 * k + 1][1] - pre[2 * k + 1][0] * pre[2 * k][1]; W_post = LF.wronskian(*rec.lines)
        for at in zip(*np.nonzero(b.turned)):
            at = tuple(int(x) for x in at)
            if int(W_pre[at]) == int(W_post[at]): kept += 1
            else:
                apart += 1
                if (k, at) in laid: apart_laid += 1
                else: apart_free.append((b.interval, k, at, int(W_pre[at]), int(W_post[at])))
out = {'turned Node-records': kept + apart, 'W kept': kept, 'W apart': apart, 'of the apart: a child of that record laid at that Node by the close of the same interval': apart_laid, 'apart with no lay (interval, record, Node, W before, W after)': apart_free[:10]}
json.dump(out, open(out_path, 'w'), indent=1); print(json.dumps(out))
