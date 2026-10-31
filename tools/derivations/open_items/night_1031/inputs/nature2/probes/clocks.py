"""NATURE2's click-world probe on one record of schema 1.4 (node-all 9d75a4904's runner):
- the lay, read from the header's own setting.json, per train: the sites laid and their (a, b, r);
- causal order per clock (a site and a train, the decoder's clock), the Boss's ruling of 07:5x UTC: a click is a line
  that passes a quantum (a side, in the site or across a Mesh, with q not 0); a meeting is a side that passes a
  quantum, its partner the clock it names; a later clock is caused where, in the round of its first click, one of its
  meetings joins it to a clock whose first click came in an earlier round; the clocks of the first round are the
  starts, named as such;
- beside it, the per-Node-clock order under its own name (a site's first passing line, caused where one of its across
  partners' sites passed a quantum in an earlier round): it pools a Node-clock's trains through the board's act;
- the structure by what passes: per place, the in-site edges whose side passes a quantum (3, 2, 1, 0), and the places
  with across sides only;
- the first click's landings per side at site 0 (N5's description, no verdict): landings, landings above one quantum,
  gaps, var over mean^2 in thousandths by Rule3's carry, the whole-round reference 1000 - th(1000, th(T, n));
- the teeth: sides whose tooth moves (k_before not k_after); the grain of the passings x = D q + k_after - k_before
  (their greatest common divisor, by Euclid with Rule3's carry);
- homogeneity, a board check: read only where the lay is alike at every site; then each round's lines alike at every
  site;
- causality's no that keeps the books: a mated pair forged across a Mesh between two quiet clocks.
Whole numbers only; Rule3's carry the one division; paths by joinpath.

Usage: python3 -I clocks.py <tree> <record .jsonl> <label>
"""

import copy
import json
import sys
from pathlib import Path

TREE = Path(sys.argv[1])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)

from tensor24.algebra.carry import carry  # noqa: E402


def th(a, b):
    return carry(1000 * a, b, 0)[0]


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, carry(a, b, 0)[1]
    return a


def lay(head):
    files = [f for f in head.get("files", []) if f.get("name") == "setting.json"]
    held = json.loads(files[0]["text"]) if files else {}
    per = {}
    for train, comp, site, a, b, r in held.get("gears", []):
        per.setdefault(train, {}).setdefault(site, []).append((comp, a, b, r))
    return per, held.get("ticks")


def meets(e):
    """The clocks a line's passing sides join it to: (site, train) of each in-site side and across side with q not 0."""
    found = [(e["site"], s[0]) for s in e.get("sides", []) if s[1] != 0]
    found += [(s[1], s[0]) for s in e.get("across", []) if s[2] != 0]
    return found


def per_clock(clicks):
    first = {}
    for e in sorted(clicks, key=lambda e: e["round"]):
        if meets(e):
            first.setdefault((e["site"], e["train"]), e["round"])
    if not first:
        return None
    start = min(first.values())
    starts = sorted(c for c in first if first[c] == start)
    partners = {}
    for e in clicks:
        c = (e["site"], e["train"])
        if first.get(c) == e["round"]:
            partners.setdefault(c, set()).update(meets(e))
    late = sorted(c for c in first if first[c] > start)
    uncaused = [c for c in late if not any(first.get(p, first[c]) < first[c] for p in partners.get(c, set()))]
    by_train = {}
    for site, train in uncaused:
        by_train[train] = by_train.get(train, 0) + 1
    return {"clocks": len(first), "start_round": start, "starts": starts, "late": len(late),
            "uncaused": len(uncaused), "uncaused_by_train": by_train, "first_uncaused": uncaused[:4],
            "late_first_rounds": sorted({first[c] for c in late})[:3]}


def per_node(clicks):
    first = {}
    for e in sorted(clicks, key=lambda e: e["round"]):
        if meets(e):
            first.setdefault(e["site"], e["round"])
    if not first:
        return None
    start = min(first.values())
    partners = {}
    for e in clicks:
        if first.get(e["site"]) == e["round"]:
            partners.setdefault(e["site"], set()).update(s[1] for s in e.get("across", []) if s[2] != 0)
    late = [x for x in first if first[x] > start]
    caused = [x for x in late if any(first.get(y, first[x]) < first[x] for y in partners.get(x, set()))]
    return {"sites": len(first), "start_round": start, "starts": sorted(x for x in first if first[x] == start),
            "late": len(late), "caused": len(caused)}


def structure(clicks):
    places = {}
    for e in clicks:
        p = places.setdefault((e["round"], e["site"]), {"edges": set(), "across": 0})
        for s in e.get("sides", []):
            if s[1] != 0:
                p["edges"].add((min(e["train"], s[0]), max(e["train"], s[0])))
        p["across"] += sum(1 for s in e.get("across", []) if s[2] != 0)
    count = {}
    for p in places.values():
        k = (len(p["edges"]), p["across"] > 0)
        count[k] = count.get(k, 0) + 1
    return len(places), dict(sorted(count.items()))


def lives(clicks, site, t, u):
    land = []
    for e in clicks:
        if e["site"] == site and e["train"] == t:
            for s in e.get("sides", []):
                if s[0] == u and s[1] != 0:
                    land.append((e["round"], s[1]))
    rounds = [r for r, _ in land]
    gaps = [b - a for a, b in zip(rounds, rounds[1:])]
    n = len(gaps)
    out = {"landings": len(land), "above_one_quantum": sum(1 for _, q in land if abs(q) > 1), "gaps": n}
    if n >= 2:
        total, sq = sum(gaps), sum(g * g for g in gaps)
        out.update({"gap_values": sorted(set(gaps)), "var_over_mean2_th": th(n * sq - total * total, total * total),
                    "reference_th": 1000 - th(1000, th(total, n)), "first_landing_round": rounds[0]})
    return out


def teeth(clicks, dial):
    moved = listed = 0
    grain = 0
    for e in clicks:
        for s in e.get("sides", []):
            listed += 1
            moved += 1 if s[2] != s[3] else 0
            grain = gcd(grain, dial * s[1] + s[3] - s[2])
        for s in e.get("across", []):
            listed += 1
            moved += 1 if s[3] != s[4] else 0
            grain = gcd(grain, dial * s[2] + s[4] - s[3])
    return {"sides_listed": listed, "teeth_moved": moved, "grain_of_passings": grain}


def homogeneity(clicks, per, sites_n):
    alike_lay = all(len(set(tuple(v) for v in per[t].values())) == 1 and len(per[t]) == sites_n for t in per)
    if not alike_lay:
        return "NOT READ: the lay is not alike at every site (a board check reads the lay first)"
    rounds = {}
    for e in clicks:
        content = (e["train"], e["q"], tuple((s[0], s[1]) for s in e.get("sides", [])),
                   tuple((s[0], s[2]) for s in e.get("across", [])))
        rounds.setdefault(e["round"], {}).setdefault(e["site"], []).append(content)
    apart = [r for r in sorted(rounds) if len({tuple(v) for v in rounds[r].values()}) != 1
             or len(rounds[r]) != sites_n]
    return (f"{'SHOWN' if not apart else 'NOT SHOWN'} (a board check): {len(rounds) - len(apart)} of {len(rounds)}"
            f" rounds alike at all {sites_n} sites; first apart {apart[:1]}")


def main():
    rows = [json.loads(t) for t in Path(sys.argv[2]).read_text(encoding="utf-8").splitlines() if t.strip()]
    head, label = rows[0], sys.argv[3]
    clicks = [e for e in rows if e.get("kind") == "click"]
    dial = head.get("dial", 0)
    sides = head.get("sides", [])
    sites_n = 1
    for s in sides:
        sites_n *= s
    per, ticks = lay(head)
    print(f"== {label}: click lines {len(clicks)}, dial {dial}, birth {head.get('birth')}, sides {sides}, ticks {ticks}")
    for t in sorted(per):
        values = {}
        for site, v in per[t].items():
            values.setdefault(tuple(v), []).append(site)
        shown = "; ".join(f"{list(k)} at {len(s)} sites {s[:8]}{'...' if len(s) > 8 else ''}" for k, s in values.items())
        print(f"the lay, train {t}: {shown}")
    if not clicks:
        print("NO CLICK: the record holds no click line")
        return
    passing = [e for e in clicks if meets(e)]
    print(f"lines that pass a quantum: {len(passing)} of {len(clicks)}")
    c = per_clock(clicks)
    print(f"causality per clock: {'SHOWN' if c['uncaused'] == 0 and c['late'] else 'NOT SHOWN' if c['late'] else 'NOT READ'}: {c}")
    print(f"the per-Node-clock order: {per_node(clicks)}")
    print(f"the structure by what passes (in-site edges passing, any across passing): {structure(clicks)}")
    edges = sorted({(e["train"], s[0]) for e in clicks for s in e.get("sides", []) if e["train"] < s[0]})
    for t, u in edges:
        print(f"lives at site 0, edge ({t}, {u}) at {t}'s end (a description, no verdict): {lives(clicks, 0, t, u)}")
    print(f"the teeth: {teeth(clicks, dial)}")
    print(f"homogeneity: {homogeneity(clicks, per, sites_n)}")
    # causality's no that keeps the books: a mated pair forged between two clocks that never pass a quantum before
    first = {}
    for e in sorted(clicks, key=lambda e: e["round"]):
        if meets(e):
            first.setdefault((e["site"], e["train"]), e["round"])
    across = any(e.get("across") for e in clicks)
    if across:
        quiet = [x for x in range(sites_n) if not any(k[0] == x for k in first)]
        if len(quiet) >= 2:
            x, y = (110, 111) if 110 in quiet and 111 in quiet else (quiet[0], quiet[1])
            r = 60
            fake = [{"kind": "click", "round": r, "site": x, "train": 0, "q": 1, "sides": [], "across": [[2, y, 1, 1, 1]]},
                    {"kind": "click", "round": r, "site": y, "train": 2, "q": -1, "sides": [], "across": [[0, x, -1, 1, 1]]}]
            forged = clicks + fake
            c2 = per_clock(forged)
            print(f"no, a mated pair forged across a Mesh between quiet sites {x} (train 0) and {y} (train 2) at round {r}:"
                  f" uncaused {c2['uncaused']} {c2['first_uncaused'][:6]}")
            write = Path(sys.argv[2]).parent.parent.joinpath("probes", "forged", f"{label}_nocause.jsonl")
            body = [rows[0]] + sorted(rows[1:-1] + fake, key=lambda e: (e["round"], e["site"], e["train"])) + [rows[-1]]
            write.write_text("".join(json.dumps(e) + "\n" for e in body), encoding="utf-8")
            print(f"  written for the guard and the books: {write.name}")
    else:
        # on a world with no Mesh: a mated in-site pair forged between two clocks that have not passed a quantum,
        # at a round before their first click, named; NOT READ where every clock at a site has clicked
        late = sorted((r, k) for k, r in first.items() if r > min(first.values()))
        if late:
            r0, (site, t) = late[0]
            others = [k for k in first if k[0] == site and k != (site, t) and first[k] > r0 - 1]
            print(f"no on this world: the first later clock {(site, t)} first passes at round {r0}; clocks at its site"
                  f" still quiet then: {others}; a forged no needs two quiet clocks joined by an edge")


main()
