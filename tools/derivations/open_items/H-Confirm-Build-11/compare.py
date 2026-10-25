"""vf11: two probe summaries compared: the counts, the turns, the run back, the first interval apart in the Node lines and in the log, the rows at the marks, the SHOWN sets and every gate changing kind with its verdicts."""
import json
import sys

a, b = (json.load(open(p, encoding="utf-8")) for p in sys.argv[1:3])
na, nb = sys.argv[3:5] if len(sys.argv) > 4 else ("A", "B")
print(f"== {na} against {nb}: {a['world']['universe']} {a['world']['shape']} intervals {a['world']['intervals']}")
for key in ("counts", "turns", "run_back", "credits", "laid_back", "births", "first_birth_interval", "x_equals_gamma_at", "max_bits", "integers"):
    same = a[key] == b[key]
    print(f"  {key}: {'same' if same else 'APART'} {a[key]}" + ("" if same else f" | {b[key]}"))
apart = [i + 1 for i, (x, y) in enumerate(zip(a["node_hashes"], b["node_hashes"])) if x != y]
print(f"  Node lines apart at {len(apart)} of {len(a['node_hashes'])} intervals; first apart: {apart[:3] if apart else 'none (bit for bit)'}")
la = {int(k): v for k, v in a["log_hash_by_interval"].items()}
lb = {int(k): v for k, v in b["log_hash_by_interval"].items()}
log_apart = sorted(i for i in set(la) | set(lb) if la.get(i) != lb.get(i))
print(f"  log apart first at interval: {log_apart[:3] if log_apart else 'none'} (log lengths {a['log_len']} / {b['log_len']})")
print(f"  rows at the marks (timeless): {'same' if a['rows_timeless'] == b['rows_timeless'] else 'APART'}")
sa, sb = set(a["shown"]), set(b["shown"])
print(f"  SHOWN {na}: {sorted(sa)}")
print(f"  SHOWN {nb}: {sorted(sb)}")
for n in sorted(sa - sb):
    print(f"  gate {n} SHOWN -> NOT SHOWN: {na}: {a['kinds'][str(n)]} | {nb}: {b['kinds'][str(n)]}")
    for k, v in a["verdicts"].items():
        if k.startswith(f"{n} "):
            print(f"    {na} verdict: {v}")
            print(f"    {nb} verdict: {b['verdicts'][k]}")
for n in sorted(sb - sa):
    print(f"  gate {n} gained SHOWN: {na}: {a['kinds'][str(n)]} | {nb}: {b['kinds'][str(n)]}")
    for k, v in b["verdicts"].items():
        if k.startswith(f"{n} "):
            print(f"    {nb} verdict: {v}")
