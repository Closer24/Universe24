"""UNC1's reading of one record: the count and the beat, the tooth and the count, from the click lines alone.

Usage: python -I unc1_read.py <tree> <record .jsonl>

Read: the record through the decoder's own reader (tensor24.decoder.records.read, every guard, the sides' guard among
them), the header's dial K and birth, and the click lines (schema 1.4: each side [u, q, k_before, k_after], each Mesh
side [u, place, q, k_before, k_after]). Nothing of the board, the ledger or the act is read. Whole numbers only; Rule3's
carry (the tree's tensor24.algebra.carry.carry) is the one division. Every count printed is a count of the record.

Printed, per record:
  R0  the dial, the birth and the dial's half (K - 1) div 2, and the lines, sides and listings read.
  R1  record faithfulness (a code check, not physics): consecutive listings of one side one round apart hold
      k_before(next) = k_after(prev); the gap's passing over silent rounds G = k_before(next) - k_after(prev).
  U1  the count and the beat. From the birth: D = K Q_n - S_n = birth - k_after at every listing (|D| <= half,
      derived); its realized range. On one-line windows: the passing P = K q + k_after - k_before grouped by q, the
      record-wide and per-side count of distinct P at one q (SHOWN where one q carries two passings: the count does
      not fix the beat; NOT SHOWN where every q carries one passing).
  U2  the tooth and the count: per side, the listings grouped by the count from the birth Q_n, distinct teeth at one
      count (SHOWN where one count stands with two teeth: the count does not fix the tooth; NOT SHOWN otherwise).
  F2  windows by a clock's own count (the FACE2 ruling): per clock (site, train), between two consecutive meetings
      (decoder.shadow.met, one give and one take of a quantum on a side), T its own lines strictly between, Q the
      quanta its own sides passed over (m1, m2], and on its own sides the passing S = K Q + k_after(m2) - k_after(m1);
      the band a q-only reader holds, [K Q - (K - 1), K Q + (K - 1)], and the realized D = K Q - S; windows of one
      (T, Q) carrying two passings counted (SHOWN: the own count and the quanta do not fix the beat).
"""

import sys
from pathlib import Path

TREE, RECORD = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)

from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.decoder import records, shadow  # noqa: E402


def permille(n: int, d: int) -> int:
    """n per mille of d, floored, by Rule3's carry; d at least 1."""
    q, _ = carry(1000 * n, d, 0)
    return q


def verdict(found: int) -> str:
    """SHOWN where a counterexample to 'the count fixes it' stands, else NOT SHOWN."""
    return "SHOWN" if found else "NOT SHOWN"


record, cause = records.read(str(RECORD))
print(f"record: {RECORD.name}")
if record is None:
    print(f"NOT READ: {cause}")
    sys.exit(0)
K, birth = record.header["dial"], record.header["birth"]
half, _ = carry(K - 1, 2, 0)
lines = record.of("click")
print(f"R0 dial K {K}, birth {birth}, the dial's half (K - 1) div 2 = {half}, birth at the half: {int(birth == half)}")
print(f"R0 click lines {len(lines)}, rounds {record.end['rounds']}")

# every side's listings in round order: own sides keyed (site, train, site, u), Mesh sides (site, train, place, u)
listed: dict[tuple[int, int, int, int, str], list[tuple[int, int, int, int]]] = {}
for e in lines:
    for u, q, before, after in e["sides"]:
        listed.setdefault((e["site"], e["train"], e["site"], u, "own"), []).append((e["round"], q, before, after))
    for u, at, q, before, after in e["across"]:
        listed.setdefault((e["site"], e["train"], at, u, "mesh"), []).append((e["round"], q, before, after))
own = {k: v for k, v in listed.items() if k[4] == "own"}
mesh = {k: v for k, v in listed.items() if k[4] == "mesh"}
print(f"R0 sides listed: {len(own)} own (at a Node-clock), {len(mesh)} across a Mesh; listings "
      f"{sum(len(v) for v in own.values())} own, {sum(len(v) for v in mesh.values())} across")
moved_q = sum(1 for v in listed.values() for _, q, _, _ in v if q)
print(f"R0 listings with q not 0: {moved_q}")

# R1: faithfulness, and the silent gaps
adjacent = matched = gaps = 0
gap_low = gap_high = 0
for v in listed.values():
    for (r1, _, _, a1), (r2, _, b2, _) in zip(v, v[1:], strict=False):
        if r2 == r1 + 1:
            adjacent += 1
            matched += int(b2 == a1)
        else:
            gaps += 1
            g = b2 - a1
            gap_low, gap_high = min(gap_low, g), max(gap_high, g)
print(f"R1 consecutive listings one round apart: {adjacent}, k_before(next) = k_after(prev) at {matched} of them")
print(f"R1 silent gaps between listings: {gaps}; their passing G = k_before(next) - k_after(prev) from {gap_low} to "
      f"{gap_high} (band [-{K - 1}, {K - 1}])")

# U1 from the birth: D = K Q_n - S_n = birth - k_after; only own sides are listed whenever they carry (a Mesh side is
# listed only when it carries, so its Q_n is whole too: its q is 0 at every round it is not listed)
d_low = d_high = 0
for v in listed.values():
    for _, _, _, after in v:
        d = birth - after
        d_low, d_high = min(d_low, d), max(d_high, d)
widest = max(-d_low, d_high)
print(f"U1 from the birth, D = K Q_n - S_n = birth - k_after over every listing: from {d_low} to {d_high}; "
      f"|D| at most {widest} = {permille(widest, half) if half else 0} per mille of the half {half}")

# U1 on one-line windows: the passing at one q
by_q: dict[int, set[int]] = {}
per_side_two = 0
sides_with_two = 0
for v in listed.values():
    mine: dict[int, set[int]] = {}
    for _, q, before, after in v:
        p = K * q + after - before
        by_q.setdefault(q, set()).add(p)
        mine.setdefault(q, set()).add(p)
    two = [q for q, ps in mine.items() if q and len(ps) > 1]
    per_side_two += len(two)
    sides_with_two += int(bool(two))
moving = [q for q in by_q if q and len(by_q[q]) > 1]
qs = sorted(by_q)
print(f"U1 one-line windows: {len(qs)} distinct q, from {qs[0]} to {qs[-1]}; q not 0 holding two passings or more: "
      f"{len(moving)}")
for q in [q for q in qs if -3 <= q <= 3]:
    ps = sorted(by_q[q])
    print(f"U1 one-line windows at q {q}: {len(ps)} distinct passings, from {ps[0]} to {ps[-1]}, "
          f"spread {ps[-1] - ps[0]} against the band's 2 (K - 1) = {2 * (K - 1)}")
print(f"U1 the count does not fix the beat (one line, q not 0, two passings), record-wide: {verdict(len(moving))}; "
      f"within one side: {sides_with_two} of {len(listed)} sides hold a q with two passings")

# U2: per side, the teeth at one count from the birth
two_teeth = sides_two = 0
pairs_total = 0
for v in listed.values():
    count = 0
    teeth: dict[int, set[int]] = {}
    for _, q, _, after in v:
        count += q
        teeth.setdefault(count, set()).add(after)
    pairs_total += sum(len(t) for t in teeth.values())
    many = [c for c, t in teeth.items() if len(t) > 1]
    two_teeth += len(many)
    sides_two += int(bool(many))
print(f"U2 (side, count from the birth) classes holding two teeth or more: {two_teeth}; sides with one: {sides_two} of "
      f"{len(listed)}; distinct (side, count, tooth) {pairs_total}")
print(f"U2 the count does not fix the tooth: {verdict(two_teeth)}")

# F2: windows by a clock's own count, between two consecutive meetings
by_place: dict[tuple[int, int], list[dict]] = {}
for e in lines:
    by_place.setdefault((e["round"], e["site"]), []).append(e)
meets: dict[tuple[int, int], list[int]] = {}
for (round_, site), held in by_place.items():
    if shadow.met(held):
        for e in shadow.pair(held):
            meets.setdefault((site, e["train"]), []).append(round_)
own_lines: dict[tuple[int, int], list[dict]] = {}
for e in lines:
    if not shadow.silent(e):
        own_lines.setdefault((e["site"], e["train"]), []).append(e)
line_at = {(e["round"], e["site"], e["train"]): e for e in lines}
windows = 0
zero_t = 0
band_low = band_high = 0
classes: dict[tuple[int, int], set[int]] = {}
for clock, rounds_ in sorted(meets.items()):
    site, train = clock
    mine = own_lines.get(clock, [])
    for m1, m2 in zip(rounds_, rounds_[1:], strict=False):
        t = sum(1 for e in mine if m1 < e["round"] < m2)
        q_w = sum(e["q"] for e in mine if m1 < e["round"] <= m2)
        first, last = line_at[(m1, site, train)], line_at[(m2, site, train)]
        # the passing on the clock's own sides, from the teeth after the two meetings (both lines list every own side)
        a1 = {u: after for u, _, _, after in first["sides"]}
        a2 = {u: after for u, _, _, after in last["sides"]}
        q_own = sum(side[1] for e in mine if m1 < e["round"] <= m2 for side in e["sides"])
        s_w = K * q_own + sum(a2[u] - a1[u] for u in a2)
        d = K * q_own - s_w
        windows += 1
        zero_t += int(t == 0)
        band_low, band_high = min(band_low, d), max(band_high, d)
        classes.setdefault((t, q_own), set()).add(s_w)
        _ = q_w
two_beats = [c for c, s in classes.items() if len(s) > 1]
print(f"F2 clocks with two meetings or more: {sum(1 for r in meets.values() if len(r) > 1)} of {len(meets)} that meet; "
      f"windows between consecutive meetings: {windows}, of own count T = 0: {zero_t}")
if windows:
    print(f"F2 realized D = K Q - S on the clocks' own sides over the windows: from {band_low} to {band_high}; "
          f"the q-only band per window [-(K - 1), K - 1] = [-{K - 1}, {K - 1}]")
    print(f"F2 (own count T, quanta Q) classes: {len(classes)}; holding two passings or more: {len(two_beats)}")
    for t, q in sorted(classes):
        ss = sorted(classes[(t, q)])
        width, _ = carry(2 * (K - 1), t, 0) if t else (0, 0)
        print(f"F2 class T {t}, Q {q}: {len(ss)} passings, spread {ss[-1] - ss[0]}; the q-only beat's width per own "
              f"line 2 (K - 1) div T = {width}, so T x width = {t * width} (2 (K - 1) = {2 * (K - 1)})")
    print(f"F2 the own count and the quanta do not fix the beat: {verdict(len(two_beats))}")
else:
    print("F2 the own count and the quanta do not fix the beat: NOT READ: no clock of the record meets twice")

# the passings' grain: the gcd of every passing the record carries (line rounds and silent gaps), by Rule3's carry
def gcd(x: int, y: int) -> int:
    """Euclid's gcd of two whole numbers by Rule3's carry, both taken from 0 up."""
    x, y = abs(x), abs(y)
    while y:
        _, r = carry(x, y, 0)
        x, y = y, r
    return x


grain = 0
for v in listed.values():
    for _, q, before, after in v:
        grain = gcd(grain, K * q + after - before)
    for (_, _, _, a1), (_, _, b2, _) in zip(v, v[1:], strict=False):
        grain = gcd(grain, b2 - a1)
reach = gcd(grain, K)
places, _ = carry(K, reach, 0) if reach else (K, 0)
print(f"G0 the passings' grain g (gcd of every passing read): {grain}; gcd(g, K) = {reach}; the tooth's reachable "
      f"places on the dial K / gcd(g, K) = {places}")
teeth_seen = {after for v in listed.values() for _, _, _, after in v} | {
    before for v in listed.values() for _, _, before, _ in v}
print(f"G0 distinct teeth written in the record: {len(teeth_seen)}")

# U3: the lines' q (each clock's count, the sum of its sides) against the circulation of a triangle of three clocks at
# a place, c = q_tu + q_uv + q_vt over three laid edges: adding c' to the three oriented edges moves no line's q
# (q_t = q_tu - q_vt, q_u = q_uv - q_tu, q_v = q_vt - q_uv), so the lines alone never read c; the sides do
tri_places = three_places = circ_nonzero = 0
circ_values: dict[int, int] = {}
lines_hold = 0
for (round_, site), held in by_place.items():
    side_q = {(e["train"], u): q for e in held for u, q, _, _ in e["sides"]}
    trains_here = sorted({e["train"] for e in held})
    found = False
    for i, t in enumerate(trains_here):
        for j, u in enumerate(trains_here[i + 1:], start=i + 1):
            for v in trains_here[j + 1:]:
                if (t, u) in side_q and (u, v) in side_q and (v, t) in side_q:
                    found = True
                    c = side_q[(t, u)] + side_q[(u, v)] + side_q[(v, t)]
                    three = all(side_q[x] for x in ((t, u), (u, v), (v, t)))
                    three_places += int(three)
                    circ_values[c] = circ_values.get(c, 0) + 1
                    circ_nonzero += int(c != 0)
                    # the lines' q unchanged by the circulation: each line's q is the sum of its sides (the guard's)
                    q_of = {e["train"]: e["q"] for e in held}
                    lines_hold += int(q_of[t] == side_q[(t, u)] - side_q[(v, t)] + sum(
                        q for (a, b), q in side_q.items() if a == t and b not in (u, v)))
    tri_places += int(found)
print(f"U3 places holding a triangle of three clocks on laid edges: {tri_places}; triangles with all three edges "
      f"passing a quantum: {three_places}; lines whose q is its sides' sum there: {lines_hold}")
print(f"U3 circulations c = q_tu + q_uv + q_vt: not 0 at {circ_nonzero}; values (c: places) "
      f"{sorted(circ_values.items())[:12]}")
print("U3 the lines' q do not fix the circulation (a circulation not 0 stands): "
      f"{verdict(circ_nonzero) if tri_places else 'NOT READ: no place holds a triangle of three clocks'}")

# the alike sites: each side's history (round, q, before, after) by (train, u, kind) across the sites
hist: dict[tuple[int, int, str], set[tuple]] = {}
for (site, train, at, u, kind), v in listed.items():
    hist.setdefault((train, u, kind), set()).add(tuple(v) if kind == "own" else (at - site, tuple(v)))
print(f"G1 sides by (train, other train): {len(hist)}; distinct histories across the sites: "
      f"{sum(len(h) for h in hist.values())}")
