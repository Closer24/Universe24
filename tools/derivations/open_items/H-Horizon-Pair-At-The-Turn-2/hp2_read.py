"""hp2: read a probe stream: at every release (a Node frozen at i and turned at i+1, or turned at i after frozen at i-1), the close's letter at the hovering Node and its six neighbours: the standing shares against the unit per record, the frozen mask, whether any Link of the hovering Node had both ends standing on any record (a meeting), the refusals per interval, the clicks after the first freeze; the carrier's Link term at the watch Nodes against the write's quotient. Usage: hp2_read.py <probe.jsonl>"""
import json
import sys

sys.set_int_max_str_digits(0)
L = [json.loads(l) for l in open(sys.argv[1])]
head, tail, body = L[0], L[-1] if L[-1].get("tail") else None, [l for l in L[1:] if not l.get("tail")]
shape = head["shape"]
def nb(at):
    out = []
    for a in range(3):
        for d in (-1, 1):
            j = list(at); j[a] = (j[a] + d) % shape[a]; out.append(j)
    return out
first = next((l["i"] for l in body if l["frozen"]), None)
print("world", head["world"].split("/")[-1], "intervals", len(body), "first freeze", first, "frozen content", head["frozen content"], "units", head["units"], "T", head["T"], "A", head["A"], "B", head["B"])
if tail: print("run back", tail["run back"], "max transient", tail["max transient"], "counts", tail["counts"])
if first is None: sys.exit()
after = [l for l in body if l["i"] >= first]
clicks = [(l["i"], c) for l in after for c in l["clicks"]]
print("clicks from the first freeze on:", len(clicks), "births", sum(1 for _, c in clicks if c["event"] == "birth"), "credits", sum(1 for _, c in clicks if c["event"] == "credit"))
# releases: Node frozen at i and not frozen at i+1 (turned at i or i+1)
frozen_prev = set()
releases = 0; rel_rows = []
stand_hover = {}; stand_nb = {}; both_ends = 0; meet_links = 0; hover_frozen_in_close = 0
link_terms = []; q_rows = []
refusals = {}
for k, l in enumerate(after):
    fr = set(tuple(f) for f in l["frozen"])
    released = [f for f in frozen_prev if f not in fr]
    releases += len(released)
    for kk, v in l["counts_delta"].items():
        refusals[kk] = refusals.get(kk, 0) + v
    pr = l["probe"]
    recs = pr.get("records", {})
    nxt = after[k + 1] if k + 1 < len(after) else None
    pr = nxt["probe"] if nxt else {}
    recs = pr.get("records", {})
    for f in released:
        key = str(list(f))
        for rec, d in recs.items():
            sh = d["shares"].get(key)
            if sh is None: continue
            stand_hover[rec] = stand_hover.get(rec, 0) + sh[1]
            hover_frozen_in_close += sh[2]
            nbs = [d["shares"].get(str(j)) for j in nb(f)]
            s_nb = sum(x[1] for x in nbs if x)
            stand_nb[rec] = stand_nb.get(rec, 0) + s_nb
            if sh[1]:
                both_ends += sum(1 for x in nbs if x and x[1] and not x[2])
        car = pr.get("carrier", {}).get(key)
        if car:
            link_terms.append((nxt["i"], key, car["link_term"], car["link_term_div_w"], car["write_q"], car["X_now"], car["X_before"], car["reaches"][0], car["mass"]))
    frozen_prev = fr
print("releases (frozen at i, not at i+1):", releases)
print("at the released Node at its first unfrozen interval (the interval after its frozen-and-turned one), per record: intervals standing (share >= unit) at the hovering Node", stand_hover, "; at its six neighbours (sum over the six)", stand_nb, "; Links with both ends standing and the neighbour not frozen", both_ends, "; the hovering Node read frozen by the close", hover_frozen_in_close)
print("refusals and counts summed from the first freeze:", refusals)
# shares by magnitude at watch nodes: max share / unit across the tail
mx = {}
for l in after:
    for rec, d in l["probe"].get("records", {}).items():
        u = d["unit"]
        for key, (s, st, fz) in d["shares"].items():
            mx[rec] = max(mx.get(rec, 0), s)
print("largest share at any watch Node after the first freeze, per record, against the unit:", {r: (mx[r], head["units"][int(r)], mx[r] * 1000 // head["units"][int(r)]) for r in mx})
print("the carrier's Link term at the released Node (i, node, SUM R_j (m_j - now), its quotient at w, the write's q, X now, X before, R_ij, D) first 6:")
for row in link_terms[:6]: print("  ", row)
if link_terms:
    print("  over all", len(link_terms), "releases: |link term div w| max", max(abs(r[3]) for r in link_terms), "; write q min/max", min(r[4] for r in link_terms), max(r[4] for r in link_terms), "; R_ij at the release 0 in", sum(1 for r in link_terms if r[7] == 0), "of", len(link_terms))
# carrier link term at all watch nodes, all intervals after first freeze: distribution
allt = [(c["link_term_div_w"], c["write_q"], c["reaches"][0]) for l in after for c in l["probe"].get("carrier", {}).values()]
if allt:
    print("carrier at every watch Node-interval after the first freeze:", len(allt), "; link term div w: min", min(a for a, _, _ in allt), "max", max(a for a, _, _ in allt), "nonzero", sum(1 for a, _, _ in allt if a != 0), "; write q: min", min(b for _, b, _ in allt), "max", max(b for _, b, _ in allt), "positive", sum(1 for _, b, _ in allt if b > 0), "; R_ij = 0 (p_i 0) in", sum(1 for _, _, r in allt if r == 0))
sums = [(l["i"], l["board_content_sum"], len(l["frozen"]), l["ever"]) for l in body if l["i"] % 100 == 0 or l["i"] == len(body)]
print("board content sum, frozen count, ever frozen at every 100:", sums)
print("max transient", max(l["max transient"] for l in body), "state bits", max(l["state bits"] for l in body))
