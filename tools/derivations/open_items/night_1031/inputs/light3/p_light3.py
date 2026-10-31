"""LIGHT3's probe: light's click lines, the echo with a turn at B, and the cone, read per clock from one record.

Reads the record's click lines (round, site, train, q, sides, across); the decoder's guard (decoder/sides.paired,
frozen in light3/all) refuses a malformed record first, reading the header's train cards' keys for that guard alone.
No header kind, card name, file, setting or board side is read by any reading. A clock is (site, train). A meeting is
a side of q not 0, once: one give (the end whose q is below 0) and one take; own (both clocks at one site) or across a
Mesh. Rounds are read only by order (strictly later); sites only by identity and by the across field's partner.

Rule L, per clock: a medium clock has Mesh meetings and no own meeting; a matter clock has an own meeting. The medium
is the set of trains whose clocks that meet are all medium clocks, each named. Light's lines: the Mesh meetings with
a medium clock at one end.

The echo (per clock): A, a matter clock, gives a light link at g; t is A's next light meeting after g (A's own quiet
on light: A's own meetings at its site may stand between, and are A's own count) and A takes a light link at t; B, a
matter clock at another site, gives a light link at b2 in (g, t) to a clock at site P, and B's last light take before
b2, at b1, came from site P (the turn at B, read from the across field; B's hold is (b1, b2)); a chain of meetings
from A's give reaches the clock B took from at b1 before b1; a chain of meetings from B's give at b2 reaches the clock
A takes from at t before t. A chain: meetings sharing a clock, each at a strictly later round than the clock was
reached (the Boss's ruling: the next link given by the clock that took the last one, or by a clock that met it in a
recorded meeting at a later round). Variants beside it: the directed chain (light links given by reached clocks
alone), no turn (any later light give of B), and the site quiet (a board check: no light line of any clock at A's
site in (g, t))."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("all", "src")))
from tensor24.decoder import sides as guard  # noqa: E402


def read(path):
    """The record's click lines as tuples, and the guard's cause ("" when the record is well formed)."""
    with path.open(encoding="utf-8") as held:
        raw = [json.loads(text) for text in held]
    clicks = [(e["round"], e["site"], e["train"], e["q"], e.get("sides", []), e.get("across", []))
              for e in raw if e.get("kind") == "click"]
    return clicks, guard.paired(raw)


def meetings(clicks):
    """Every meeting once, (round, giver, taker, kind), kind 'own' or 'mesh', each clock (site, train)."""
    found = set()
    for r, s, t, q, own, across in clicks:
        for u, x, k0, k1 in own:
            if x != 0:
                a, b = (s, t), (s, u)
                found.add((r, a, b, "own") if x < 0 else (r, b, a, "own"))
        for u, p, x, k0, k1 in across:
            if x != 0:
                a, b = (s, t), (p, u)
                found.add((r, a, b, "mesh") if x < 0 else (r, b, a, "mesh"))
    return sorted(found)


def classes(meets):
    """Rule L per clock: the medium clocks, the matter clocks."""
    own, mesh = set(), set()
    for r, g, k, kind in meets:
        (own if kind == "own" else mesh).update((g, k))
    return mesh - own, own


def eligible(meets):
    """The medium as a set of trains (trains with Mesh meetings and no own meeting by any clock) and the clocks of
    the other trains that meet (A and B are taken among them)."""
    medium_c, matter_c = classes(meets)
    med_t, mat_t, mixed = trains_of(medium_c, matter_c)
    med = set(med_t)
    clocks = medium_c | matter_c
    return {c for c in clocks if c[1] in med}, {c for c in clocks if c[1] not in med}


def trains_of(medium, matter):
    """The medium as a set of trains (every clock of the train that meets is a medium clock), the matter trains, and
    the trains with clocks of both classes."""
    med = {c[1] for c in medium}
    mat = {c[1] for c in matter}
    return sorted(med - mat), sorted(mat - med), sorted(med & mat)


def components(meets):
    """The clocks' meeting graph's components, by a union of the two ends of every meeting."""
    parent = {}

    def root(c):
        parent.setdefault(c, c)
        while parent[c] != c:
            parent[c] = parent[parent[c]]
            c = parent[c]
        return c

    for r, g, k, kind in meets:
        a, b = root(g), root(k)
        if a != b:
            parent[a] = b
    groups = {}
    for c in list(parent):
        groups.setdefault(root(c), []).append(c)
    return sorted(groups.values(), key=lambda g: (-len(g), min(g)))


def reach(start, by_round, first, last, directed, light):
    """The earliest round each clock is reached by chains of meetings from the start (clock -> round), through the
    rounds first..last: a meeting at round r reaches its other clock when one of its clocks was reached before r;
    directed: a light link reaches its taker when its giver was reached before r."""
    arrival = dict(start)
    for r in range(first, last + 1):
        new = []
        for m in by_round.get(r, ()):
            _, g, k, kind = m
            if directed:
                if m in light and g in arrival and arrival[g] < r:
                    new.append(k)
            else:
                if g in arrival and arrival[g] < r:
                    new.append(k)
                if k in arrival and arrival[k] < r:
                    new.append(g)
        for c in new:
            if c not in arrival:
                arrival[c] = r
    return arrival


def echoes(meets, medium, matter, directed=False, turn=True, site_quiet=False):
    """Every echo the rule reads: (A, g, B, b1, b2, t, P, A's own meetings in (g, t), B's own meetings in (b1, b2))."""
    light = {m for m in meets if m[3] == "mesh" and (m[1] in medium or m[2] in medium)}
    by_round = {}
    for m in meets:
        by_round.setdefault(m[0], []).append(m)
    gives, takes, light_at, own_at, site_light = {}, {}, {}, {}, {}
    for m in sorted(light):
        r, g, k, _ = m
        gives.setdefault(g, []).append((r, k))
        takes.setdefault(k, []).append((r, g))
        for c in (g, k):
            light_at.setdefault(c, []).append(r)
            site_light.setdefault(c[0], []).append(r)
    for r, g, k, kind in meets:
        if kind == "own":
            for c in (g, k):
                own_at.setdefault(c, []).append(r)
    found, tried, windows = [], 0, 0
    ticking = 0  # windows with an own meeting of A strictly inside: A's own count while quiet on light
    for a in sorted(matter):
        for g, m1 in gives.get(a, ()):
            tried += 1
            quiet = site_light.get(a[0], ()) if site_quiet else light_at.get(a, ())
            later = [r for r in quiet if r > g]
            if not later:
                continue
            t = min(later)
            home_from = [gg for rr, gg in takes.get(a, ()) if rr == t]
            if not home_from:
                continue
            windows += 1
            ticking += 1 if any(g < r < t for r in own_at.get(a, ())) else 0
            out = reach({a: g, m1: g} if not directed else {m1: g}, by_round, g + 1, t, directed, light)
            for b in sorted(matter):
                if b[0] == a[0]:
                    continue
                for b2, k2 in gives.get(b, ()):
                    if not g < b2 < t:
                        continue
                    before = [(rr, gg) for rr, gg in takes.get(b, ()) if rr < b2]
                    if not before:
                        continue
                    if turn:
                        # B's last light takes before b2, all from the site B gives back to (no turn where the last
                        # round's takes came from two sites), one of them from a clock the out chain reached before
                        b1 = max(rr for rr, gg in before)
                        last = [gg for rr, gg in before if rr == b1]
                        if any(gg[0] != k2[0] for gg in last):
                            continue
                        if not any(gg in out and out[gg] < b1 for gg in last):
                            continue
                        site1 = k2[0]
                    else:
                        fed = [(rr, gg) for rr, gg in before if gg in out and out[gg] < rr]
                        if not fed:
                            continue
                        b1, g1 = min(fed)
                        site1 = g1[0]
                    back = reach({b: b2, k2: b2} if not directed else {k2: b2}, by_round, b2 + 1, t, directed, light)
                    if any(gg in back and back[gg] < t for gg in home_from):
                        n_a = sum(1 for r in own_at.get(a, ()) if g < r < t)
                        n_b = sum(1 for r in own_at.get(b, ()) if b1 < r < b2)
                        found.append((a, g, b, b1, b2, t, k2[0], n_a, n_b, site1))
    echoes.ticking = ticking
    return found, tried, windows


def cone(meets):
    """The click world's cone per clock from the first round's meetings: each clock's first meeting reached at its
    own round, only later, or never; and beside it the per-site reading (a board check): each site's first meeting
    against the first round any clock at the site is reached."""
    by_round = {}
    for m in meets:
        by_round.setdefault(m[0], []).append(m)
    first = min(by_round)
    start = {c: first for _, g, k, _ in by_round[first] for c in (g, k)}
    arrival = reach(start, by_round, first + 1, max(by_round), False, set())
    first_meet = {}
    for r, g, k, kind in meets:
        for c in (g, k):
            first_meet[c] = min(first_meet.get(c, r), r)
    own = sum(1 for c in first_meet if arrival.get(c) == first_meet[c])
    later = sum(1 for c in first_meet if c in arrival and arrival[c] > first_meet[c])
    never = sorted(c for c in first_meet if c not in arrival)
    # the per-Node-clock order beside it (a board check): a site is reached when any clock at it is, and any clock at
    # a reached site carries the chain on, pooling the site's trains through the board's act, with no meeting
    site_first = {}
    for c, r in first_meet.items():
        site_first[c[0]] = min(site_first.get(c[0], r), r)
    sites = {c[0]: first for c in start}
    for r in range(first + 1, max(by_round) + 1):
        new = []
        for _, g, k, _ in by_round.get(r, ()):
            if g[0] in sites and sites[g[0]] < r:
                new.append(k[0])
            if k[0] in sites and sites[k[0]] < r:
                new.append(g[0])
        for x in new:
            if x not in sites:
                sites[x] = r
    s_own = sum(1 for x in site_first if sites.get(x) == site_first[x])
    s_never = sum(1 for x in site_first if x not in sites)
    return first, len(first_meet), own, later, never, len(site_first), (s_own, len(site_first) - s_own - s_never, s_never)


def prefixes(meets):
    """The medium train set on each prefix of the record (cut after round R), at the rounds where it changes."""
    changes, last = [], None
    rounds = sorted({m[0] for m in meets})
    for cut in rounds:
        part = [m for m in meets if m[0] <= cut]
        medium, matter = classes(part)
        now = tuple(trains_of(medium, matter)[0])
        if now != last:
            changes.append((cut, now))
            last = now
    return changes


def main():
    path = Path(sys.argv[1])
    clicks, cause = read(path)
    print(f"record {path.name}: {len(clicks)} click lines; the guard (sides.paired): {cause or 'well formed'}")
    if cause:
        print("NOT READ: a malformed record")
        return
    meets = meetings(clicks)
    own = sum(1 for m in meets if m[3] == "own")
    print(f"  meetings (sides of q not 0, once each): {len(meets)}, own {own}, across a Mesh {len(meets) - own}")
    medium, matter = classes(meets)
    med_t, mat_t, mixed = trains_of(medium, matter)
    per = {}
    for c in medium:
        per.setdefault(c[1], [0, 0])[0] += 1
    for c in matter:
        per.setdefault(c[1], [0, 0])[1] += 1
    print(f"RULE L per clock: medium clocks {len(medium)}, matter clocks {len(matter)}; per train [medium, matter] "
          f"clocks {dict(sorted(per.items()))}; the medium, as trains: {med_t}; trains with clocks of both classes "
          f"{mixed} (matter trains)")
    medium, matter = eligible(meets)
    if not medium:
        print("  light's lines: NOT SHOWN (" + ("no Mesh meeting" if own == len(meets) else "no medium clock") + ")")
    if len(sys.argv) > 2 and sys.argv[2] == "prefix":
        print(f"  the medium train set on prefixes, where it changes: {prefixes(meets)}")
    comps = components(meets)
    sites = {}
    for i, comp in enumerate(comps):
        for c in comp:
            sites.setdefault(c[0], set()).add(i)
    shared = sum(1 for s, ids in sites.items() if len(ids) == 1 and sum(1 for c in medium | matter if c[0] == s) > 1)
    multi = sum(1 for s in sites if sum(1 for c in medium | matter if c[0] == s) > 1)
    print(f"  components of the clocks' meeting graph: {len(comps)}, sizes {[len(c) for c in comps][:8]}"
          f"{' ...' if len(comps) > 8 else ''}; sites with two clocks or more {multi}, all of them in one "
          f"component {shared}")
    first, n, own_r, later, never, n_sites, s_own = cone(meets)
    print(f"CONE per clock from round {first}'s meetings: of {n} clocks, first meeting reached at its own round "
          f"{own_r}, only later {later}, never {len(never)}; board check, the per-Node-clock order (a site's trains pooled through the board's act): of {n_sites} sites, reached at the round of their first meeting {s_own[0]}, only later {s_own[1]}, never {s_own[2]}")
    if not medium:
        return
    for directed in (False, True):
        for turn in (True, False):
            found, tried, windows = echoes(meets, medium, matter, directed, turn)
            pairs = sorted({(e[0], e[2]) for e in found})
            name = ("directed" if directed else "meetings") + (", turn at B" if turn else ", no turn")
            bs = sorted({e[2] for e in found})
            print(f"ECHO ({name}; A's own quiet): {'SHOWN' if found else 'NOT SHOWN'}: {len(found)} echoes, "
                  f"{len(pairs)} pairs, B among {bs[:6]}{' ...' if len(bs) > 6 else ''}; {tried} gives of a matter "
                  f"clock, {windows} windows ending in A's take, {echoes.ticking} of them with an own meeting of A "
                  f"inside")
            for e in found[:3]:
                a, g, b, b1, b2, t, p, n_a, n_b, p1 = e
                print(f"    A {a} gives at {g}, B {b} takes at {b1} from site {p1} and gives to site {p} at {b2}, "
                      f"A takes at {t}; A's own meetings between {n_a}, B's own meetings between b1 and b2 {n_b}")
    found, tried, windows = echoes(meets, medium, matter, False, True, True)
    print(f"ECHO (meetings, turn at B; the site quiet, a board check): {'SHOWN' if found else 'NOT SHOWN'}: "
          f"{len(found)} echoes; {tried} gives, {windows} windows")


if __name__ == "__main__":
    main()
