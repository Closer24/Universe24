"""W2's reader of the two_bodies logs: per config the peak and centroid distances over the intervals with their
least-squares slopes, each body's share fraction at its lay Node along the run, the content level c at the lay
Node against the empty sea's mean (the self-dug well), the well's profile at the probes, each body's clicks
(count, intervals between them, beat, proper) and the clock ratio read from the contents and from the clicks.

    python tools/derivations/w2/read_runs.py tools/derivations/w2/two_bodies_*.jsonl
"""

from __future__ import annotations

import json
import sys
from math import exp, log

import numpy as np

GAMMA = 1000


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


def slope(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    return float(np.polyfit(xs, ys, 1)[0])


def u_of(c: int) -> float:
    return -c * log(1 - 1 / GAMMA)


def omega_of(g: float, c: int) -> float:
    return float(np.arccos(1 - g * exp(-2 * u_of(c))))


def main() -> None:
    paths = sys.argv[1:]
    empty = None
    for p in paths:
        h, r, c, s = load(p)
        if h["config"] == "empty":
            empty = {row["interval"]: row for row in r}
    for p in paths:
        header, readings, credits, summary = load(p)
        g = header["g"]
        print("=" * 100)
        print(f"config {header['config']}  den {header['den']} ({header['den_bits']} bits)  cube {header['cube']}  intervals {header['intervals']}  family {header['family']}  pair {header['pair']}  g {g:.4f}  period0 {header['period0']:.3f}")
        print("bodies", header["bodies"], "well", header["well"], header["well_depth"], "unit_k", header["unit_k"])
        n = len(readings)
        ts = [row["interval"] for row in readings]
        marks = [t for t in (0, 1, 2, 5, 10, 20, 50, 100, 150, 200, 250, 300) if t < n]
        for b in range(len(header["bodies"])):
            fr = [readings[t]["bodies"][b]["frac_lay"] for t in marks]
            print(f" body {b} frac_lay at {marks}: " + " ".join(f"{x:.3f}" if x is not None else "None" for x in fr))
            tot = [readings[t]["bodies"][b]["share_total"] / header["unit_k"] for t in marks]
            print(f" body {b} share_total/unit_k at marks: " + " ".join(f"{x:.3f}" for x in tot))
            rad = [readings[t]["bodies"][b]["radius"] for t in marks]
            print(f" body {b} centroid radius about lay at marks: " + " ".join(f"{x:.4f}" for x in rad))
            peaks = {}
            for row in readings:
                peaks[tuple(row["bodies"][b]["peak_offset"])] = peaks.get(tuple(row["bodies"][b]["peak_offset"]), 0) + 1
            print(f" body {b} peak offsets (count of intervals): {peaks}")
            cz = [readings[t]["bodies"][b]["centroid"][2] for t in marks]
            print(f" body {b} centroid z at marks: " + " ".join(f"{x:+.5f}" for x in cz))
            print(f" body {b} centroid z slope (Links/interval) over all: {slope(ts, [row['bodies'][b]['centroid'][2] for row in readings]):+.3e}; over the last half: {slope(ts[n//2:], [row['bodies'][b]['centroid'][2] for row in readings[n//2:]]):+.3e}")
        if len(header["bodies"]) == 2:
            pd = [row["peak_distance"] for row in readings]
            cd = [row["centroid_distance"] for row in readings]
            print(f" peak distance: first {pd[0]} last {pd[-1]} min {min(pd)} max {max(pd)} slope {slope(ts, pd):+.3e} Links/interval")
            print(f" centroid distance: first {cd[0]:.5f} last {cd[-1]:.5f} min {min(cd):.5f} max {max(cd):.5f} slope {slope(ts, cd):+.3e} Links/interval; last half slope {slope(ts[n//2:], cd[n//2:]):+.3e}")
            print(f" centroid distance at marks: " + " ".join(f"{cd[t]:.5f}" for t in marks))
        # the content at the probes against the empty sea's mean
        print(" content c at probes (A, mid, mid2, B, far) and the sea's mean (empty run) at marks:")
        for t in marks:
            row = readings[t]
            base = empty[t]["c_mean"] if empty and t in empty else None
            cs = row["c"]
            extra = "" if base is None else f"  excess over empty mean: A {cs['A'] - base:+.1f} mid {cs['mid'] - base:+.1f} mid2 {cs['mid2'] - base:+.1f} B {cs['B'] - base:+.1f} far {cs['far'] - base:+.1f}"
            print(f"  t {t:3d}: A {cs['A']:5d} mid {cs['mid']:5d} mid2 {cs['mid2']:5d} B {cs['B']:5d} far {cs['far']:5d} | mean {row['c_mean']:.1f} min {row['c_min']} max {row['c_max']}" + (f" | empty mean {base:.1f}" if base is not None else "") + extra)
        print(" free row of the sign at probes at marks: " + "; ".join(f"t{t}: " + ",".join(str(readings[t]['free_row'][k]) for k in ('A', 'mid', 'mid2', 'B', 'far')) for t in marks))
        print(" light share/unit_light at probes at marks: " + "; ".join(f"t{t}: " + ",".join(f"{readings[t]['light'][k] / header['unit_light']:.3f}" for k in ('A', 'mid', 'mid2', 'B', 'far')) for t in marks))
        print(" light quanta total at marks: " + " ".join(f"{readings[t]['light_quanta_total']:.2f}" for t in marks))
        # the clicks
        by_body: dict[tuple, list[dict]] = {}
        for row in credits:
            if row["event"] == "credit":
                by_body.setdefault((tuple(row["identity"]), tuple(row["support"])), []).append(row)
        refused = [row for row in credits if row["event"] == "refused"]
        print(f" credits {sum(len(v) for v in by_body.values())} refused {len(refused)} births {sum(1 for r in credits if r['event'] == 'birth')}")
        for key, rows in sorted(by_body.items()):
            ivs = [r["interval"] for r in rows]
            gaps = [b - a for a, b in zip(ivs, ivs[1:])]
            beats = [r["beat"] for r in rows]
            propers = [r["proper"] for r in rows]
            pgaps = [b - a for a, b in zip(propers, propers[1:])]
            print(f"  identity {key[0]} at {key[1]}: {len(rows)} clicks at intervals {ivs[:12]}{'...' if len(ivs) > 12 else ''}")
            print(f"    gaps in intervals {gaps[:20]}{'...' if len(gaps) > 20 else ''} mean {np.mean(gaps) if gaps else None}")
            print(f"    beats {beats[:20]} ; proper at clicks {propers[:8]}... gaps in proper {pgaps[:12]} mean {np.mean(pgaps) if pgaps else None}")
            print(f"    kind {set(r['kind'] for r in rows)} sense {set(r['sense'] for r in rows)} windows {[r['windows'] for r in rows][:12]} point {rows[0]['point']} momentum {rows[0]['momentum']}")
        if refused:
            print(f"  refusals: {[(r['interval'], r.get('cause'), r.get('node')) for r in refused[:10]]}")
        # the clock ratio from the contents at the two bodies' Nodes (the board's view) at the end
        if len(header["bodies"]) == 2:
            last = readings[-1]
            cA, cB = last["bodies"][0]["c_lay"], last["bodies"][1]["c_lay"]
            print(f" at the end: c_A {cA} c_B {cB}; e^(U_A - U_B) = {exp(u_of(cA) - u_of(cB)):.6f}; omega(c_A)/omega(c_B) = {omega_of(g, cA) / omega_of(g, cB):.6f}; proper A {last['bodies'][0]['proper_lay']} proper B {last['bodies'][1]['proper_lay']} ratio {last['bodies'][0]['proper_lay'] / last['bodies'][1]['proper_lay']:.6f}")
        print(" summary", json.dumps(summary))


if __name__ == "__main__":
    main()
