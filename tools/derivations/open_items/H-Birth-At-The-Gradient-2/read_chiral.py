"""bg2: the chiral probe read: per 100 intervals the frozen count, the board's content sum, the ever-frozen count, the form's counters; the births with their Nodes, contents, paces, distance from the frozen set; the refusals by name from the first freeze on; the Link-pace spread of the watch."""
import json, sys
lines=[json.loads(l) for l in open(sys.argv[1])]
head=lines[0]; body=[l for l in lines[1:] if "i" in l]; tail=lines[-1] if "tail" in lines[-1] else None
print("head", head); print("tail", tail)
first=[l["i"] for l in body if l["frozen"]]
f0=first[0] if first else None; print("first freeze", f0, "last interval", body[-1]["i"])
def S(key, frm=0): return sum(l["bg2"][key] for l in body if l["i"]>=frm)
print("whole run: met_gradient",S("met_gradient"),"twist_nonzero",S("twist_nonzero"),"sense_opposite",S("sense_opposite"),"drawn",S("drawn"),"clock_apart_only",S("clock_apart_only"))
if f0: print("from first freeze: met_gradient",S("met_gradient",f0),"twist_nonzero",S("twist_nonzero",f0),"sense_opposite",S("sense_opposite",f0),"drawn",S("drawn",f0),"clock_apart_only",S("clock_apart_only",f0))
ref={}; ref0={}
for l in body:
    for k,v in l["counts_delta"].items():
        ref[k]=ref.get(k,0)+v
        if f0 and l["i"]>=f0: ref0[k]=ref0.get(k,0)+v
print("counts whole", ref); print("counts from first freeze", ref0)
births=[(l["i"],c) for l in body for c in l["clicks"] if c["event"]=="birth"]; credits=[(l["i"],c) for l in body for c in l["clicks"] if c["event"]=="credit"]
print("births", len(births), "credits", len(credits), "last credit", credits[-1][0] if credits else None, "births from first freeze", sum(1 for i,_ in births if f0 and i>=f0))
gb=[(l["i"],g) for l in body for g in l["bg2"]["born"]]; print("gradient-born candidates", len(gb))
for i,b in births:
    if f0 and i>=f0: print(" birth", i, b["node"], "row", b["taken_row"], "pair", b["line_pair"], b["minus"], b["plus"], "c", b.get("content_minus_plus"), "p", b.get("pace_minus_plus"), "W", b["W_children"], "taken", b["taken"], "dist", b.get("dist_frozen_minus_plus"))
for l in body:
    if l["i"]%100==0 or (f0 and l["i"]==f0):
        pw=l["pace_watch"].values(); print(l["i"], "frozen", len(l["frozen"]), "turned", l["turned"], "ever", l["ever"], "sum", l["board_content_sum"], "distinct pace", l["distinct_pace"], "watch paces min/max", (min(pw),max(pw)) if pw else None, "bg2", {k:v for k,v in l["bg2"].items() if k!="born"}, "bits", l["max transient"], l["state bits"])
fro=[len(l["frozen"]) for l in body]; print("frozen per interval max", max(fro), "ever", body[-1]["ever"])
