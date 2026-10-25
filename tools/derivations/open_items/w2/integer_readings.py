"""W2's integer reader (the owner's word, Addition 3: no float in the readers; every reading a quotient with its
remainder or a count over a span). From a two_bodies log: the peak distance per interval (a Manhattan count of
Links on the torus), each body's centroid along z in thousandths of a Link as (1000 x M_z) div S with its
remainder (M_z the integer first moment of the share about the lay Node, S the share's integer total), the two
centroids' separation in thousandths, the change of that separation over the span from interval 150 to 300 as a
quotient per 1,000 intervals with its remainder (the slope's integer reading), the share at the lay Node in
thousandths of the total, the gaps between a body's clicks in intervals and in the Node's proper (integers),
and the clock ratio of the two lay Nodes as (10^6 x proper_A) div proper_B with its remainder, beside the
integer clocks p_0(c) of the two contents (paces.clock_alone, an integer) and their ratio x 10^6 div.

    python tools/derivations/w2/integer_readings.py tools/derivations/w2/int_pair3.jsonl
"""

from __future__ import annotations

import json
import sys

from event_universe.core.paces import clock_alone
from event_universe.core.rule3 import division_forward

GAMMA = 1000
THOUSAND = 1000
MILLION = 1000000


def load(path: str) -> tuple[dict, list[dict], list[dict], dict | None]:
    header, readings, credits, summary = None, [], [], None
    with open(path) as f:
        for line in f:
            row = json.loads(line)
            if row["event"] == "header":
                header = row
            elif row["event"] == "reading":
                readings.append(row)
            elif row["event"] in ("credit", "refused", "birth"):
                credits.append(row)
            elif row["event"] == "summary":
                summary = row
    return header, readings, credits, summary


def quotient(numerator: int, wall: int) -> str:
    q, r = division_forward(numerator, wall, 0)
    return f"{int(q)} rem {int(r)}"


def thousandths_z(body: dict) -> tuple[int, int]:
    """(1000 x M_z) div S and its remainder, the centroid along z in thousandths of a Link; (0, 0) at S = 0."""
    s = body["share_total"]
    if s <= 0:
        return 0, 0
    q, r = division_forward(THOUSAND * body["moment"][2], s, 0)
    return int(q), int(r)


def main() -> None:
    for path in sys.argv[1:]:
        header, readings, credits, summary = load(path)
        cube = header["cube"]
        print("=" * 100)
        print(f"config {header['config']} den {header['den']} cube {cube} intervals {header['intervals']} family {header['family']} pair {header['pair']} unit_k {header['unit_k']}")
        marks = [t for t in (0, 10, 20, 50, 100, 150, 200, 250, 300) if t < len(readings)]
        bodies = header["bodies"]
        for b in range(len(bodies)):
            print(f" body {b} lay {bodies[b][0]} share at lay Node in thousandths of the total (quotient rem) at {marks}: "
                  + " | ".join(quotient(THOUSAND * readings[t]['bodies'][b]['share_lay'], readings[t]['bodies'][b]['share_total']) for t in marks))
            print(f" body {b} total share in units of unit_k (quotient rem) at marks: "
                  + " | ".join(quotient(readings[t]['bodies'][b]['share_total'], header['unit_k']) for t in marks))
            print(f" body {b} centroid z in thousandths of a Link about the lay Node (quotient rem) at marks: "
                  + " | ".join("%d rem %d" % thousandths_z(readings[t]['bodies'][b]) for t in marks))
            offs = {}
            for row in readings:
                key = tuple(row["bodies"][b]["peak_offset"])
                offs[key] = offs.get(key, 0) + 1
            print(f" body {b} peak offsets from the lay Node, counts of intervals: {offs}")
            z0, zn = thousandths_z(readings[150]["bodies"][b])[0], thousandths_z(readings[-1]["bodies"][b])[0]
            span = readings[-1]["interval"] - 150
            print(f" body {b} centroid z change from 150 to {readings[-1]['interval']}: {zn - z0} thousandths over {span} intervals = per 1000 intervals {quotient((zn - z0) * THOUSAND, span)} thousandths")
        if len(bodies) == 2:
            lay_gap = (bodies[1][0][2] - bodies[0][0][2]) % cube
            if lay_gap > cube // 2:
                lay_gap -= cube
            seps = []
            for row in readings:
                za, zb = thousandths_z(row["bodies"][0])[0], thousandths_z(row["bodies"][1])[0]
                seps.append(THOUSAND * lay_gap + zb - za)
            pds = [row["peak_distance"] for row in readings]
            print(f" peak distance (Manhattan Links on the torus): first {pds[0]} last {pds[-1]} min {min(pds)} max {max(pds)}; intervals at each distance {dict(sorted({d: pds.count(d) for d in set(pds)}.items()))}")
            print(f" centroid separation along z in thousandths of a Link at marks: " + " ".join(str(seps[t]) for t in marks))
            d0, dn, span = seps[150], seps[-1], readings[-1]["interval"] - 150
            print(f" separation change from 150 to {readings[-1]['interval']}: {dn - d0} thousandths over {span} intervals = per 1000 intervals {quotient((dn - d0) * THOUSAND, span)} thousandths; from 0: {seps[-1] - seps[0]} thousandths over {readings[-1]['interval']} intervals = per 1000 intervals {quotient((seps[-1] - seps[0]) * THOUSAND, readings[-1]['interval'])}")
            last = readings[-1]
            pa, pb = last["bodies"][0]["proper_lay"], last["bodies"][1]["proper_lay"]
            ca, cb = last["bodies"][0]["c_lay"], last["bodies"][1]["c_lay"]
            print(f" proper counts at the two lay Nodes after {last['interval']} intervals: A {pa} B {pb}; (10^6 x A) div B = {quotient(MILLION * pa, pb)}")
            print(f" contents at the end c_A {ca} c_B {cb}; integer clocks p_0(c): A {clock_alone(GAMMA, ca)} B {clock_alone(GAMMA, cb)}; (10^6 x p_0(c_A)) div p_0(c_B) = {quotient(MILLION * clock_alone(GAMMA, ca), clock_alone(GAMMA, cb))}")
        # the content at the lay Node and at the probes, integers
        print(" content c at the probes (A, mid, mid2, B, far), the board's min, max and the sum div the Nodes:")
        for t in marks:
            row = readings[t]
            cs = row["c"]
            print(f"  t {t:3d}: {cs['A']} {cs['mid']} {cs['mid2']} {cs['B']} {cs['far']} | min {row['c_min']} max {row['c_max']}")
        # the clicks
        by_body: dict[tuple, list[dict]] = {}
        for row in credits:
            if row["event"] == "credit":
                by_body.setdefault((tuple(row["identity"]), tuple(row["support"])), []).append(row)
        lays = {tuple(b[0]) for b in bodies}
        print(f" credits {sum(len(v) for v in by_body.values())} (light credits {sum(1 for r in credits if r['event'] == 'credit' and r['kind'] == 1)}) refused {sum(1 for r in credits if r['event'] == 'refused')} births {sum(1 for r in credits if r['event'] == 'birth')}")
        for key, rows in sorted(by_body.items()):
            if key[1] not in lays:
                continue
            ivs = [r["interval"] for r in rows]
            props = [r["proper"] for r in rows]
            gaps = [b - a for a, b in zip(ivs, ivs[1:])]
            pgaps = [b - a for a, b in zip(props, props[1:])]
            beats = [r["beat"] for r in rows]
            print(f"  identity {key[0]} at {key[1]}: {len(rows)} clicks; gaps in intervals {gaps}; sum {sum(gaps)} over {len(gaps)} gaps = {quotient(sum(gaps), max(1, len(gaps)))}")
            print(f"    gaps in proper {pgaps}; sum {sum(pgaps)} over {len(pgaps)} = {quotient(sum(pgaps), max(1, len(pgaps)))}; beat key None on {sum(1 for x in beats if x is None)} of {len(beats)}")
        if summary:
            print(" summary", json.dumps(summary))


if __name__ == "__main__":
    main()
