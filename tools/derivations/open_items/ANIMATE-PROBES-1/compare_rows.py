import json, sys, os, hashlib
import sys as _s
OLD, NEW = _s.argv[1], _s.argv[2]; _s.argv = _s.argv[2:]
def rows(path):
    out={}
    for line in open(path):
        d=json.loads(line)
        for k,v in d.items():
            if isinstance(v,dict) and "verdict" in v:
                out[k.split()[0]]=str(v["verdict"])
    return out
def kind(v):
    for k in ("SHOWN in part","SHOWN","NOT SHOWN","NOT READ","NOT REACHED"):
        if v.startswith(k): return k
    return v[:20]
names=sys.argv[1:] or ["bodies","onebigbang","nature","hole","ga2","plasma","sea","collapse_800","universe","plasma_3","universe_3","sea_3600","sea_50000","nature_bang","matter_bang","matter_horizon"]
tot_moved=0
for n in names:
    po, pn = f"{OLD}/{n}.json", f"{NEW}/{n}.json"
    if not os.path.exists(pn) or not os.path.exists(f"{NEW}/{n}.reading.jsonl"): print(n, "not ready"); continue
    a=json.load(open(po)); b=json.load(open(pn))
    same_nodes = a["nodes"]==b["nodes"]; same_log = a["log"]==b["log"]
    ra=rows(f"{OLD}/{n}.reading.jsonl"); rb=rows(f"{NEW}/{n}.reading.jsonl")
    moved=[k for k in ra if kind(ra[k])!=kind(rb.get(k,""))]
    tot_moved+=len(moved)
    births=lambda d: sum(1 for e in d["log"] if e.get("event")=="birth")
    credits=lambda d: sum(1 for e in d["log"] if e.get("event")=="credit")
    rb_back=b.get("run_back")
    print(f"{n}: clock lines alike {same_nodes}, log alike {same_log}; births {births(a)}->{births(b)}, credits {credits(a)}->{credits(b)}; rewind {rb_back}; rows moved {len(moved)}")
    for k in moved: print(f"    {k}: {kind(ra[k])} -> {kind(rb.get(k,''))} | {rb.get(k,'')[:150]}")
print("total moved", tot_moved)
