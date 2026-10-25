"""Hand g4: the integer readings of the fall.py logs in one table each (the marks printed by fall.py): per mark the
centroid along z about the lay Node in thousandths of a Link, the rms radius in milli Links, the share within 0, 1,
2, 3 Links of the peak in thousandths, the peak's offset, the content at the peak, the turned Nodes, the upward
crossings at the lay Node; for two bodies the separation in thousandths and the peak distance; the summary with the
run back; the fall's integer rates: (z_t - z_0) div t per interval and 2 (z_t - z_0) div t^2 per interval squared,
beside the law's a = (2 / 3)(1 - g)/(2 - g) x G / Gamma in thousandths of a Link per interval squared.

    python tools/derivations/g4/read_runs.py tools/derivations/g4/log_*.txt
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction


def rows_of(path: str) -> list[dict]:
    found = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("{"):
                try:
                    found.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return found


def main() -> None:
    for path in sys.argv[1:]:
        rows = rows_of(path)
        header = next((r for r in rows if r.get("event") == "header"), None)
        if header is None:
            print(f"== {path}: no header (the run has not started)")
            continue
        readings = [r for r in rows if r.get("event") == "reading"]
        summary = next((r for r in rows if r.get("event") == "summary"), None)
        g = Fraction(header["pair"][1] - header["pair"][0], header["pair"][1])
        print(f"== {path}: mode {header['mode']} den {header['den']} ({header['den_bits']} bits) cube {header['cube']} family {header['family']} g {header['g_milli']} milli sin {header['sin_milli']} milli; depth {header['depth']} offset {header['offset']} sigma_tenths {header['sigma_tenths']} quanta {header.get('quanta')} unit {header['unit']} width bits {header['width_bits']} A {header['amplitude_bound']}")
        for lay in header["lays"]:
            print(f"   lay: amplitude {lay['amplitude']} at c {lay['c_lay']} (p_0 {lay['p0_lay']}, cos {lay['cos_milli']} sin {lay['sin_milli']} milli), share {lay['share_total']} = {lay['quanta_milli']} milli quanta of {lay['unit']}")
        if not readings:
            print("   no readings")
            continue
        print("   t | body | centroid z (milli) | rms (milli) | within 0,1,2,3 Links (milli) | peak offset | c_peak c_lay | share at lay (milli) | crossings_lay beat_engine | turned")
        for r in readings:
            for i, b in enumerate(r["bodies"]):
                if not b.get("total"):
                    print(f"   {r['interval']:4d} | {i} | no share")
                    continue
                print(f"   {r['interval']:4d} | {i} | {b['centroid_milli'][2]:6d} | {b['rms_milli']:5d} | {b['within_milli']} | {b['peak_offset']} | {b['c_peak']} {b['c_lay']} | {b['share_lay_milli']} | {b['crossings_lay']} {b['beat_engine_lay']} | {r['turned']}")
            if "separation_milli" in r:
                print(f"        separation {r['separation_milli']} milli, peak distance {r['peak_distance']}")
        z = {r["interval"]: r["bodies"][0]["centroid_milli"][2] for r in readings if r["bodies"] and r["bodies"][0].get("total")}
        if header["mode"] in ("well",) and 0 in z:
            gradient = None
            # the gradient at the lay Node from the profile depth div (1 + r): c(r - 1) - c(r + 1) over 2 Links
            d, o = header["depth"], header["offset"]
            if o >= 1:
                gradient = Fraction(d // o - d // (o + 2), 2)
                law = Fraction(2, 3) * (1 - g) / (2 - g) * gradient / 1000
                print(f"   the gradient at the lay Node {gradient} levels per Link; the law's a = (2/3)(1-g)/(2-g) G/Gamma = {float(law) * 1000:.3f} milli Links per interval^2 (CHECK) = {(law * 1000).numerator * 1000 // (law * 1000).denominator} micro")
            for t in (10, 20, 30, 50, 100):
                if t in z:
                    dz = z[t] - z[0]
                    print(f"   fall by {t}: {dz} milli Links; rate {dz // t} milli per interval; 2 dz div t^2 = {(2 * dz) // (t * t)} milli per interval^2 (x1000: {(2000 * dz) // (t * t)} micro)")
        if header["mode"] == "pair":
            seps = {r["interval"]: r["separation_milli"] for r in readings if "separation_milli" in r}
            for a, b in ((0, 50), (0, 100), (0, 150), (0, 300), (150, 300), (100, 200)):
                if a in seps and b in seps:
                    d = seps[b] - seps[a]
                    print(f"   separation change {a} -> {b}: {d} milli Links over {b - a} intervals = {(1000 * d) // (b - a)} milli per 1000 intervals")
        if header["mode"] == "clock":
            last = readings[-1]["bodies"][0]
            print(f"   crossings at the lay Node over {readings[-1]['interval']} intervals: {last['crossings_lay']}; the engine's beat {last['beat_engine_lay']}; proper count at the lay Node {last['proper_lay']} (p_0 x intervals)")
        if summary:
            print(f"   summary: {json.dumps(summary)}")


if __name__ == "__main__":
    main()
