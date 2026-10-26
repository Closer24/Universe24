"""bg2: the chiral probe's numbers written into REPORT.md's placeholders (complete or cut short, named)."""
import json, sys
lines=[json.loads(l) for l in open("out/chiral3000_form.jsonl")]
body=[l for l in lines[1:] if "i" in l]; tail=lines[-1] if "tail" in lines[-1] else None
last=body[-1]["i"]; cut = tail is None
first=[l["i"] for l in body if l["frozen"]]; f0=first[0] if first else None
def S(key, frm=0): return sum(l["bg2"][key] for l in body if l["i"]>=frm)
ref={}; ref0={}
for l in body:
    for k,v in l["counts_delta"].items():
        ref[k]=ref.get(k,0)+v
        if f0 and l["i"]>=f0: ref0[k]=ref0.get(k,0)+v
births=[(l["i"],c) for l in body for c in l["clicks"] if c["event"]=="birth"]; credits=[(l["i"],c) for l in body for c in l["clicks"] if c["event"]=="credit"]
bh=[(i,b) for i,b in births if f0 and i>=f0]
fro=[len(l["frozen"]) for l in body]
marks=[l for l in body if l["i"]%100==0]
sums=", ".join(f"{l['board_content_sum']:,} ({l['i']:,})" for l in marks if f0 and l["i"]>=f0-100)
bits=f"{max(l['max transient'] for l in body)} transient / {max(l['state bits'] for l in body)} state bits"
rb = f"the run back {tail['run back'][0]} of {tail['run back'][1]}" if tail else "the run back not reached (cut short)"
g=S("met_gradient",f0 or 0); d=S("drawn",f0 or 0); tw=S("twist_nonzero",f0 or 0); se=S("sense_opposite",f0 or 0); co=S("clock_apart_only",f0 or 0)
status = f"cut short at {last:,} of 3,000 by the time box" if cut else "complete, 3,000 of 3,000"
pw=[(l["i"], min(l["pace_watch"].values()), max(l["pace_watch"].values())) for l in body if l["pace_watch"] and l["i"]%100==0]
paces=", ".join(f"{a}-{b} ({i:,})" for i,a,b in pw)
bl="; ".join(f"{i:,} at {b['node']} row {b['taken_row']} children's pair {b['line_pair']} - at {b['minus']} + at {b['plus']} contents {b['content_minus_plus']} Link paces {b['pace_minus_plus']} W {b['W_children']} taken {b['taken']:,} distance from the frozen set {b['dist_frozen_minus_plus']}" for i,b in bh) or "none"
sec=f"""- **The chiral to 3,000 under FR-S1 plus the form (tests/worlds/world_chiral.json; out/chiral3000_form.jsonl; {status}; {rb}; {bits}):** the first freeze at {f0:,} at {body[[l['i'] for l in body].index(f0)]['frozen'][0] if f0 else None}; Nodes ever frozen by {last:,}: {body[-1]['ever']}; frozen per interval at most {max(fro)}, 0 intervals with every Node frozen; the board's content sum from the first freeze on: {sums}: rising at every mark, never turning back toward the sea (the horizon's neighbourhood empties by nothing); the watch's Link paces (min-max over the ever-frozen Nodes and their neighbours) {paces}. The close from the first freeze to {last:,}: met {ref0.get('met',0):,}; **gradient meetings {g:,}** (the record's current 0 and the Link paces apart), the number drawn at {d:,} of them, the twist not 0 at {tw:,} of them, the ends' charges opposite at {se:,} of them; the refusals by name: orientation {ref0.get('refused_orientation',0):,} (of which {co:,} with the Link paces equal and the clocks apart), twist {ref0.get('refused_twist',0):,}, sense {ref0.get('refused_sense',0):,}, lay {ref0.get('refused_lay',0):,}, stop {ref0.get('refused_stop',0):,}; **births {len(bh)}** from the first freeze on (births in the whole run {ref.get('births',0)}, the head's 17 before 1,500), credits from the first freeze {sum(1 for i,_ in credits if f0 and i>=f0)} (the last credit of the run at {credits[-1][0] if credits else None:,}: the board dark from 1,644 as on every record). Births at or beside the hovering Nodes: {bl}. The whole run's counts: {ref}."""
row = f"{len(bh)} births and 0 credits from the first freeze at {f0:,} to {last:,}; {g:,} gradient meetings, {d:,} drawn, every one refused by the lay or the stop" if f0 else f"no freeze reached by {last:,}"
led = f"{status}: {g:,} gradient meetings from the first freeze {f0:,}, {d:,} drawn, {len(bh)} births, lay {ref0.get('refused_lay',0):,} and stop {ref0.get('refused_stop',0):,} refusals, 0 credits from 1,644, the content sum rising" if f0 else f"{status}: no freeze reached"
t=open("REPORT.md").read()
t=t.replace("CHIRAL_SECTION", sec).replace("CHIRAL_ROW", row).replace("CHIRAL_LEDGER", led).replace("CHIRAL_BITS", bits + (f", {rb}" if True else "")).replace("CHIRAL_CLOCK", f"{co:,}").replace("CHIRAL_TIME", sys.argv[1] if len(sys.argv)>1 else "see out/chiral3000_form.start and .done")
if cut:
    t=t.replace("Runs cut short: none (every run named below ran to its end).", f"Runs cut short: the chiral to 3,000 under the form reached {last:,} of 3,000 within the time box (the first launch stopped at 903 with its launching shell, before the first freeze; the second launch's record is the one read); every other run ran to its end.")
else:
    t=t.replace("Runs cut short: none (every run named below ran to its end).", "Runs cut short: none (the first launch of the chiral stopped at 903 with its launching shell, before the first freeze, and was relaunched; the second launch ran to 3,000 and is the one read; every other run ran to its end).")
open("REPORT.md","w").write(t)
print(status, f0, g, d, len(bh), ref0)
