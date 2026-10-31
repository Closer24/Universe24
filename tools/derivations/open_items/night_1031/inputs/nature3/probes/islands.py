"""NATURE3's causal-order probe on one record of schema 1.4: causal order as the order of chains of meetings that share a
clock (the 07:5x rule, the Boss's 08:5x ruling), read from the record's lines and sides alone (q only, no tooth).

- A click is a line that passes a quantum. A meeting is one side passing a quantum (q not 0) with its mate: the
  unordered pair of clocks it joins, at its round, in the site or across a Mesh. A clock is (site, train).
- The islands: the clocks joined by meetings, in any round, into components (union by meeting).
- The reach: chains from the first round's meetings. A chain passes from a meeting to a later or same-round meeting
  that shares a clock. Read two ways, both printed: (s) same-round chains allowed (a round's meetings joined into
  components first), and (t) a meeting reached only through a clock reached in an earlier round.
- Each later clock (first click after the first round) is reached at its first click, reached only later, or never.
- Beside it, the one-step reading, named one-step: a later clock is one-step caused where a meeting of its first round
  joins it to a clock whose first click came in an earlier round.
Whole numbers only; no division; paths by joinpath.

Usage: python3 -I islands.py <record .jsonl> <label>
"""

import json
import sys
from pathlib import Path


def meetings(clicks):
    found = set()
    for e in clicks:
        a = (e["site"], e["train"])
        for s in e.get("sides", []):
            if s[1] != 0:
                b = (e["site"], s[0])
                found.add((e["round"], min(a, b), max(a, b)))
        for s in e.get("across", []):
            if s[2] != 0:
                b = (s[1], s[0])
                found.add((e["round"], min(a, b), max(a, b)))
    return sorted(found)


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(parent, a, b):
    ra, rb = find(parent, a), find(parent, b)
    if ra != rb:
        parent[max(ra, rb)] = min(ra, rb)


def reach(ms, same_round):
    rounds = sorted({r for r, _, _ in ms})
    r0 = rounds[0]
    reached = {}
    by_round = {}
    for r, a, b in ms:
        by_round.setdefault(r, []).append((a, b))
    for r in rounds:
        pairs = by_round[r]
        if r == r0:
            for a, b in pairs:
                reached.setdefault(a, r)
                reached.setdefault(b, r)
            if not same_round:
                continue
        if same_round:
            parent = {}
            for a, b in pairs:
                parent.setdefault(a, a)
                parent.setdefault(b, b)
                union(parent, a, b)
            groups = {}
            for c in parent:
                groups.setdefault(find(parent, c), []).append(c)
            for members in groups.values():
                if any(c in reached for c in members):
                    for c in members:
                        reached.setdefault(c, r)
        elif r != r0:
            before = {c for c, at in reached.items() if at < r}
            for a, b in pairs:
                if a in before or b in before:
                    reached.setdefault(a, r)
                    reached.setdefault(b, r)
    return r0, reached


def main():
    rows = [json.loads(t) for t in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if t.strip()]
    label = sys.argv[2]
    clicks = [e for e in rows if e.get("kind") == "click"]
    ms = meetings(clicks)
    print(f"== {label}: click lines {len(clicks)}, meetings {len(ms)}")
    if not ms:
        print("NO CLICK or no meeting: nothing read")
        return
    first = {}
    for r, a, b in ms:
        first.setdefault(a, r)
        first.setdefault(b, r)
    parent = {c: c for c in first}
    for _, a, b in ms:
        union(parent, a, b)
    islands = {}
    for c in first:
        islands.setdefault(find(parent, c), []).append(c)
    sizes = sorted((len(v) for v in islands.values()), reverse=True)
    sites = {}
    for c in first:
        sites.setdefault(c[0], set()).add(find(parent, c))
    split = sum(1 for v in sites.values() if len(v) > 1)
    print(f"islands: {len(islands)}, sizes {sizes[:6]}{'...' if len(sizes) > 6 else ''}; clocks {len(first)};"
          f" sites whose clocks lie in more than one island: {split} of {len(sites)}")
    r0 = min(first.values())
    starts = sorted(c for c in first if first[c] == r0)
    later = sorted(c for c in first if first[c] > r0)
    # the one-step reading
    partners = {}
    for r, a, b in ms:
        if first[a] == r:
            partners.setdefault(a, set()).add(b)
        if first[b] == r:
            partners.setdefault(b, set()).add(a)
    one_unc = [c for c in later if not any(first[p] < first[c] for p in partners.get(c, set()))]
    for name, same in (("(s) same-round chains", True), ("(t) earlier-round chains only", False)):
        _, reached = reach(ms, same)
        at_first = [c for c in later if reached.get(c) == first[c]]
        after = [c for c in later if c in reached and reached[c] > first[c]]
        never = [c for c in later if c not in reached]
        verdict = "SHOWN" if later and not after and not never else ("NOT SHOWN" if later else "NOT READ")
        print(f"chains {name}: {verdict}: of {len(later)} later clocks, {len(at_first)} reached at their first click,"
              f" {len(after)} only later, {len(never)} never; with the {len(starts)} starts,"
              f" {len(at_first) + len(starts)} reached at their first click")
    per = []
    for root, members in sorted(islands.items(), key=lambda kv: -len(kv[1])):
        held = [c for c in members if c in set(starts)]
        unc = [c for c in members if c in set(one_unc)]
        first_meeting = min(first[c] for c in members)
        per.append((len(members), len(held), len(unc), first_meeting))
    print(f"per island (size, starts, one-step uncaused, first meeting round): {per[:6]}{'...' if len(per) > 6 else ''}")
    trains = {}
    for root, members in islands.items():
        key = tuple(sorted({c[1] for c in members}))
        trains[key] = trains.get(key, 0) + 1
    print(f"islands by the trains they hold: {dict(sorted(trains.items()))}")
    print(f"one-step (named one-step): {len(later) - len(one_unc)} of {len(later)} later clocks one-step caused,"
          f" {len(one_unc)} not; starts {len(starts)} at round {r0}")


main()
