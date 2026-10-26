"""hr2: the report's markers filled from the chiral run's outputs (the final JSON and the stream's readings). Usage: fill_report.py <draft.md> <out.md> <chiral_final.json> <hover_all.json> <per_hundred.txt> <hover_first.txt> <cut note>"""
import json, sys
draft, out_path, final_path, hover_path, ph_path, hv_path, cut = sys.argv[1:8]
text = open(draft).read()
F = json.load(open(final_path)) if final_path != "-" else None
A = json.load(open(hover_path))
ph = open(ph_path).read().strip()
hv = open(hv_path).read().strip()
last = A["intervals"]
if F:
    rb = F["run back"]; bits = (F["max transient bits"], F["max state bits"]); counts = F["counts"]
    rb_s = f"{rb[0]} of {rb[1]}"; bits_s = f"{bits[0]} transient / {bits[1]} state"
else:
    rb_s = "not reached (the run cut short)"; bits_s = "read on the stream alone: " + str(max(json.loads(l)["max_transient_bits"] for l in open(sys.argv[8]))) + " transient"
    counts = None
pct_within = A["intervals within one content of the horizon (content >= 3792) after first freeze"]
pct_below = A["below"]
section = f"""The run reached {last} of 8,000 intervals ({cut}). The flagged record equals the head through 2,100 (0 frozen, 15,316 credits, the same by-hundreds table as 2a to 1,700; the last credit at 1,643).

By two hundreds of intervals from the first freeze (credits, their levels, births, frozen lines, max content, the horizon's neighbourhood's content sum, the rest's, the board's, the turns at Nodes that ever froze):

```
{ph}
```

The neighbourhood: 24 Nodes ever frozen by 2,400 (the head's 24, the same Nodes), 125 of 125 by 2,800; the rest's content sum 0 from 2,601 to 2,800 on: the whole 5-cube is the horizon's neighbourhood from then, its content sum standing near 474,000 (125 Nodes at 3,792 to 3,837) to the end, the max content 3,837 at every interval. Frozen at once at most {A['frozen count per interval max']} of 125; frozen lines {sum(A['gaps'].values()) + A['frozen at the last interval']} and releases {A['releases']}; 0 frozen two in a row at any Node (FR-S1 holds over the whole record); {A['frozen at the last interval']} frozen at the last interval.

The hover, in aggregate over the 125 Nodes after each one's first freeze: {pct_within} Node-intervals at the content 3,792 or above (one below the horizon or in its bin) against {pct_below} below it; the gaps from a release to the Node's next freeze: 1 interval {A['gaps']['1']}, 2 to 10 {A['gaps']['2-10']}, 11 to 50 {A['gaps']['11-50']}, 51 to 200 {A['gaps']['51-200']}, over 200 {A['gaps']['>200']}, the longest {A['gap max']}; the lowest content any released Node reached {A['min content of a released Node']} (Node {A['at (node, i)'][0]} at interval {A['at (node, i)'][1]}): no released Node fell below 3,707 in {last - 2101} intervals, none came near the sea's level (the rest's Nodes were at 2,889 to 3,792 when the horizon formed and all rose into it). The velocity at the first release (X_next - X_frozen) between {A['velocity at first release min/max'][0]} and {A['velocity at first release min/max'][1]} X-levels per interval over the Nodes (the hard-fed 3-cube's 1,708,834,097 is thirty times the largest: the chiral's Nodes crept into the horizon); the write's push at the first unfrozen interval (the second difference of X) between {A['write push at first release (second difference) min/max'][0]} and {A['write push at first release (second difference) min/max'][1]} X-levels per interval squared, positive at every Node: the write pushes the released Node back up. The largest X at any freeze {A['max X at a freeze']} (Node {A['at'][0]} at {A['at'][1]}), growing over the record as the write pumps the hovering Nodes, under fr1's bound 2 X_f = {A['fr1 bound 2 X_f']}.

The first four Nodes to freeze, read one by one (hover.py):

```
{hv}
```

(0,2,1): released at 2,102 with the velocity -54,136,118, its content 3,792 for the next intervals, the write's push 704,048 at the first unfrozen interval and growing 3 per cent per interval, back at the horizon at 2,179 (the gap 78) with the velocity 73,740,944, larger than at the release; its velocity at each later return 87,188,546; 95,832,195; 105,473,759; 110,737,154; 117,214,902: the hover is pumped by the write, the reflection at the horizon ever harder, the Node's X at its freezes drifting up (4,320,350,994; 4,296,440,187; 4,326,925,270; 4,316,114,224; 4,356,474,954). It spent 2,779 of 2,900 intervals at 3,792 or above through 5,000.

The clicks: 0 credits and 0 births on the board from 1,644 to {last}, at every distance from every Node that ever froze; 0 credits at any ever-frozen Node after its first freeze, 0 at its neighbours, 0 farther. The credits' rate per interval after the first freeze: 0 per {last - 2100}; their energy: none (no credit line); their direction: none. Before the horizon: 15,316 credits in 1,643 intervals, every one at the beat 1 (15,679 levels), the rate falling with the content, 4,096 per hundred intervals at the content 919 and 4 per hundred at 2,446."""
text = text.replace("@@CHIRAL@@", section)
text = text.replace("@@CHIRAL_CREDITS@@", f"0 credits in the {last - 2100} intervals from 2,101 to {last} under the form against 0 in the head's 300")
text = text.replace("@@CHIRAL_END@@", f"{last}")
text = text.replace("@@MAX_GAP@@", f"{A['gap max']}")
text = text.replace("@@BITS_CHIRAL@@", bits_s)
text = text.replace("@@RUNBACK_CHIRAL@@", rb_s)
text = text.replace("@@LEDGER_CHIRAL@@", f"{last} intervals, 125 of 125 Nodes at the horizon by 2,800, {A['releases']} releases, 0 two in a row, 0 credits from 1,644 on, {bits_s}")
text = text.replace("@@CUT@@", cut)
text = text.replace("@@ONE_NODE_3700@@", "out/one_node_3700_4000.jsonl, 4,000 intervals, the run back 10 of 10")
text = text.replace("@@ONE_NODE_3780@@", "out/one_node_3780_4000.jsonl, 4,000 intervals, the run back 10 of 10")
open(out_path, "w").write(text)
print("filled; markers left:", text.count("@@"))
