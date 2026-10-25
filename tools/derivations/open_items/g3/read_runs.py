"""Hand g3: the readings of the toy's runs from their jsonl files, integers only: per run the header's den, g, lay and hold; at the
marks 0, 10, 20, 50, 100, 150, 200 (300) the centroid along z in thousandths of a Link (the quotient (1000 M_z) div S), the
squared radius about the lay Node in thousandths, the share within 1, 2, 3 Links of the peak in thousandths, the peak's offset,
the content at the lay Node and the well's centre, the turned Nodes; the fall as a count over a span, (centroid at t2 -
centroid at t1) x 1000 div (t2 - t1) thousandths of a Link per 1,000 intervals... no: thousandths of a Link per interval is
(c(t2) - c(t1)) div (t2 - t1) with its remainder, the centroid already in thousandths; the beat: the upward crossings at the lay
Node and at the peak over the run, and the crossings per 1,000 proper units at the lay Node; the two-body separation; the
summary's credits, refusals, swaps, largest bit length and the run back's verdict.
Run: python tools/derivations/g3/read_runs.py tools/derivations/g3/out/*.jsonl
"""

from __future__ import annotations

import json
import sys


def marks_of(n: int) -> list[int]:
    return [m for m in (0, 5, 10, 20, 30, 50, 75, 100, 150, 200, 250, 300) if m <= n]


def main() -> None:
    for path in sys.argv[1:]:
        rows = [json.loads(line) for line in open(path)]
        header = rows[0]
        readings = [r for r in rows if r.get("event") == "reading"]
        summary = rows[-1] if rows[-1].get("event") == "summary" else {}
        n = readings[-1]["interval"] if readings else 0
        print(f"== {path}")
        print(f"den {header['den']} ({header['den_bits']} bits) family {header['family']} g {header['g_thousandths'][0]}/1000 lay {header['lay']} sigma_tenths {header.get('sigma_tenths')} quanta {header.get('quanta')} hold {header['hold']} well {header['well_depth']} at {header['well_centre']} content {header['content']} pair {header['pair']} cube {header['cube']} width_bits {header['width_bits']}")
        for lay in header.get("lays", []):
            if lay.get("lay") == "wide":
                print(f"  wide lay record {lay['record']}: A0 {lay['A0']} sum_A2 {lay['sum_A2']} share_total {lay['share_total']} unit {lay['unit']} quanta (at the lay Node's content) {lay['quanta_quotient_remainder'][0]} rem {lay['quanta_quotient_remainder'][1]}")
        by_interval = {r["interval"]: r for r in readings}
        for b in range(len(readings[0]["bodies"])):
            print(f"  body record {b}:")
            print("   t    cz_thousandths  r2_thousandths  within1/2/3_of_peak  peak_offset  share_lay  c_lay c_well turned proper_lay crossings_lay/peak quanta")
            for m in marks_of(n):
                r = by_interval.get(m)
                if r is None:
                    continue
                body = r["bodies"][b]
                print(f"  {m:4d} {str(body['centroid_z_thousandths'][0]):>10} {str(body['radius2_thousandths'][0]):>12}  {str(body['within_1_2_3_of_peak_thousandths']):>18}  {str(body['peak_offset']):>11}  {str(body['share_lay_thousandths']):>8}  {r['c_lay']:5d} {r['c_well']:5d} {r['turned']:5d} {r['proper_lay']:9d}  {body['crossings_lay']:3d}/{body['crossings_peak']:3d}  {body['quanta'][0]}")
            # the fall over spans as integer quotients with remainders (thousandths of a Link per interval)
            for t1, t2 in ((0, 20), (0, 50), (0, 100), (50, 100), (100, 200), (0, n)):
                if t2 <= n and t1 in by_interval and t2 in by_interval and t2 > t1:
                    c1 = by_interval[t1]["bodies"][b]["centroid_z_thousandths"][0]
                    c2 = by_interval[t2]["bodies"][b]["centroid_z_thousandths"][0]
                    if c1 is not None and c2 is not None:
                        q, rem = divmod(c2 - c1, t2 - t1)
                        print(f"   fall {t1}->{t2}: {c2 - c1} thousandths over {t2 - t1} intervals = {q} rem {rem} thousandths per interval")
            last = by_interval[n]["bodies"][b]
            proper = by_interval[n]["proper_lay"]
            if proper:
                q, rem = divmod(1000 * last["crossings_lay"], proper)
                print(f"   beat at the lay Node: {last['crossings_lay']} upward crossings in {n} intervals, proper {proper}: (1000 x crossings) div proper = {q} rem {rem}; per interval (1000 x crossings) div n = {1000 * last['crossings_lay'] // n}")
        if len(readings[0]["bodies"]) == 2:
            print("   separation_z_thousandths / peak_distance at marks:", [(m, by_interval[m].get("separation_z_thousandths"), by_interval[m].get("peak_distance")) for m in marks_of(n) if m in by_interval])
        print(f"  summary: {json.dumps(summary)}")


if __name__ == "__main__":
    main()
