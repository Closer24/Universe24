"""pc1: every record above 1.5 MB trimmed to its header, rows, counts, run back, the transient's class, the contents visited and the first 300 log lines (the whole log read by the decoder before the trim; the owner's rule: no file above 1.5 MB kept)."""
import os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
for path in glob.glob(os.path.join(HERE, 'out', '**', '*.json'), recursive=True):
    if os.path.getsize(path) <= 1500 * 1024: continue
    R = json.load(open(path))
    if 'log' in R:
        R['log_lines_total'] = len(R['log']); R['log'] = R['log'][:300]; R['trimmed (pc1)'] = 'the log cut to its first 300 lines after the decoder read it whole; the gates beside it in .gates.jsonl'
    json.dump(R, open(path, 'w'))
    print(path, os.path.getsize(path))
