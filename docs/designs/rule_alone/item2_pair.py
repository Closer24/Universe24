"""ITEM 2 of record 2134: two matter bodies attract and move toward each other, each by the
content alone, with the one seam: the well hops with its record's centroid. The rule alone.

The board [80, 32, 32], periodic across, open along x. Two bodies of s = 2000 on wells of side
5 at the kind [800, 850], centres 20 Links apart at x = 30 and 50. The content is the two
bodies' static levels (the lattice Laplace level of s on a body's Nodes, by relaxation), each
moving with its well: the gravity time part's steady level as a declared field (a first run
stepped the gravity time part by the rule with the hold; on this runner's reflecting faces it
rang by 15 percent for 1500 intervals and never settled, so it is not used; the engine's faces
absorb). Each body's record reads the total content for its pace (its own and the other's, as
the engine's pace does) and steps by the rule in its own pair array (its well, the kind
elsewhere). THE ONE SEAM: the well moves to the Node nearest the envelope's centroid over its
support (the box of half-width 5 about the well, 9.98 (8)); a first run took the centroid over
the whole board, which the mode's tail pulls, and the wells wandered: not read. Read every 50
intervals: the two centroids, the wells' centres, the separation, the widths. HOST.

    PYTHONPATH=src python docs/designs/rule_alone/item2_pair.py [intervals]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodies as B  # noqa: E402
import rule_alone as R  # noqa: E402

SHAPE = (80, 32, 32)
WRAP = (False, True, True)
AMOUNT = 2000
SEPARATION = 20
EVERY = 50
HALF = 5  # the support's window about the well, the seam's tally (9.98 (8))


def run(intervals: int, seam: str = "centroid") -> dict:
    middle = SHAPE[1] // 2
    a = B.Body([SHAPE[0] // 2 - SEPARATION // 2, middle, middle], AMOUNT)
    b = B.Body([SHAPE[0] // 2 + SEPARATION // 2, middle, middle], AMOUNT)
    t0 = time.time()
    records = []
    for body in (a, b):
        profile, clock = B.bound_mode(SHAPE, WRAP, body)
        records.append(
            {
                "body": body,
                "now": profile.copy(),
                "before": profile.copy(),
                "rem": np.zeros(SHAPE, dtype=R.INT),
                "clock": clock,
            }
        )
    seeding = time.time() - t0
    lone = B.lone_static_field(SHAPE, WRAP, a)
    readings = []
    hops = []
    carried = {id(rec): [0.0, 0.0, 0.0] for rec in records}
    t0 = time.time()
    for t in range(intervals + 1):
        content = B.shifted_content(lone, [a, b], SHAPE)
        if t % EVERY == 0:
            line = {"t": t, "content_between": int(content[SHAPE[0] // 2, middle, middle])}
            for name, rec in zip("AB", records, strict=True):
                num, den = rec["body"].pairs(SHAPE)
                read, own, wall = R.coefficients(num, den, content)
                e2 = R.envelope_squared(rec["now"], rec["before"], B.pair_cosine(num, den))
                cx, cy, cz = B.window_centroid(e2, rec["body"].centre, HALF, SHAPE, WRAP)
                xs = np.arange(SHAPE[0]).reshape(-1, 1, 1)
                width = float(np.sqrt((e2 * (xs - cx) ** 2).sum() / e2.sum()))
                line[name] = {
                    "x": cx,
                    "y": cy,
                    "z": cz,
                    "well_x": rec["body"].centre[0],
                    "width_x": width,
                    "peak": int(np.abs(rec["now"]).max()),
                }
            line["separation"] = line["B"]["x"] - line["A"]["x"]
            readings.append(line)
        if t == intervals:
            break
        # the bodies' records step in their own pair arrays, reading the total content
        for rec in records:
            num, den = rec["body"].pairs(SHAPE)
            read, own, wall = R.coefficients(num, den, content)
            rec["now"], rec["before"], rec["rem"] = R.step(
                rec["now"], rec["before"], rec["rem"], read, own, wall, WRAP
            )
            e2 = R.envelope_squared(rec["now"], rec["before"], B.pair_cosine(num, den))
            if seam == "current":
                pace = B.current_pace(
                    rec["now"],
                    rec["before"],
                    num,
                    den,
                    B.pair_cosine(num, den),
                    rec["body"].centre,
                    HALF,
                    SHAPE,
                    WRAP,
                )
                moved = B.hop_by_pace(rec["body"], carried[id(rec)], pace, SHAPE, WRAP)
            else:
                moved = B.hop(
                    rec["body"],
                    B.window_centroid(e2, rec["body"].centre, HALF, SHAPE, WRAP),
                    SHAPE,
                    WRAP,
                )
            if moved:
                hops.append(
                    {
                        "t": t + 1,
                        "body": "A" if rec is records[0] else "B",
                        "well_x": rec["body"].centre[0],
                    }
                )
        if (a.centre[0] - b.centre[0]) ** 2 < a.side**2:
            readings.append({"t": t + 1, "met": True})
            break
    return {
        "seam": seam,
        "shape": SHAPE,
        "amount": AMOUNT,
        "separation": SEPARATION,
        "clocks": [r["clock"] for r in records],
        "seeding_seconds": seeding,
        "host_seconds": time.time() - t0,
        "readings": readings,
        "hops": hops,
    }


def main() -> None:
    intervals = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    seam = "current" if "current" in sys.argv[2:] else "centroid"
    result = run(intervals, seam)
    out = Path(__file__).resolve().parent / f"item2_pair{'_current' if seam == 'current' else ''}.json"
    out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    for r in result["readings"]:
        if r.get("met"):
            print(f"t {r['t']}: the wells met")
            continue
        print(
            f"t {r['t']:5d}  A x {r['A']['x']:8.3f} well {r['A']['well_x']:3d} w {r['A']['width_x']:6.2f} peak {r['A']['peak']:7d}  B x {r['B']['x']:8.3f} well {r['B']['well_x']:3d} w {r['B']['width_x']:6.2f}  sep {r['separation']:8.3f}  c_mid {r['content_between']}"
        )
    print("hops:", result["hops"][:40], "..." if len(result["hops"]) > 40 else "")
    print(
        f"clocks {result['clocks']}; HOST seeding {result['seeding_seconds']:.1f} s, run {result['host_seconds']:.1f} s; written {out.name}"
    )


if __name__ == "__main__":
    main()
