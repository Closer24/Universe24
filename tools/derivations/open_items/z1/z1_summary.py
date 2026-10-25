"""Hand z1: the readings file summarised at marks (the integer readings of z1_run.py per interval): the light's quanta,
the content at the origin and its least and largest, the turned Nodes and the swaps, the records standing with the largest
record's quanta and the peak pairs adjacent or at one Node (part c), and for a bodies' seed each body's centroid along z,
its share within one Link of its centre, its content against the far Node's and its proper count against the far Node's,
the two bodies' separation and their peaks' distance (part d), with the extremes over the run.

    python tools/derivations/z1/z1_summary.py tools/derivations/z1/out/hole/hole.readings.jsonl
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

MARKS = (0, 1, 2, 3, 5, 10, 15, 20, 25, 50, 75, 100, 150, 200, 250, 300)


def main(path: str) -> None:
    rows = [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]
    readings = [r for r in rows if "interval" in r and r.get("event") is None]
    summary = [r for r in rows if r.get("event") == "summary"]
    out = []
    for r in readings:
        if r["interval"] not in MARKS:
            continue
        line = {
            "t": r["interval"],
            "light_quanta": r["light"]["quanta_div"],
            "light_max_level": r["light"]["max_level"],
            "c_origin": r["content"]["origin"],
            "c_least": r["content"]["least"],
            "c_largest": r["content"]["largest"],
            "X_origin": r["content"]["X_origin"],
            "turned": r["turned"],
            "swaps": r["swaps_total"],
            "refusals": r["refusals_this_interval"],
            "records": r["records"]["records"],
            "largest_record_milli": r["records"]["largest_quanta_milli"],
            "peak_pairs_adjacent": r["records"]["peak_pairs_adjacent"],
            "peak_pairs_same_node": r["records"]["peak_pairs_same_node"],
            "proper_origin_far": [r["proper"]["origin"], r["proper"]["far"]],
            "proper_least_largest": [r["proper"]["least"], r["proper"]["largest"]],
        }
        if "bodies" in r:
            line["bodies"] = [
                {k: b.get(k) for k in ("centre", "record", "quanta_milli", "peak", "centroid_milli", "within_one_of_centre_milli", "within_one_of_peak_milli", "c_centre", "c_peak", "c_far", "proper_centre", "proper_far")}
                for b in r["bodies"]
            ]
            line["separation_milli"] = r.get("separation_milli")
            line["peak_distance"] = r.get("peak_distance")
        out.append(line)
    extremes = {
        "light_quanta_least_largest": [min(r["light"]["quanta_div"] for r in readings), max(r["light"]["quanta_div"] for r in readings)],
        "largest_record_milli_over_run": max(r["records"]["largest_quanta_milli"] for r in readings),
        "records_most": max(r["records"]["records"] for r in readings),
        "intervals_with_adjacent_peaks": sum(1 for r in readings if r["records"]["peak_pairs_adjacent"] > 0),
        "intervals_with_same_node_peaks": sum(1 for r in readings if r["records"]["peak_pairs_same_node"] > 0),
        "intervals_with_turns": sum(1 for r in readings if r["turned"] > 0),
        "c_largest_over_run": max(r["content"]["largest"] for r in readings),
        "refusals_total": {},
    }
    for r in readings:
        for cause, n in r["refusals_this_interval"].items():
            extremes["refusals_total"][cause] = extremes["refusals_total"].get(cause, 0) + n
    if any("separation_milli" in r for r in readings):
        seps = [(r["interval"], r["separation_milli"]) for r in readings if r.get("separation_milli") is not None]
        extremes["separation_milli_first_last"] = [seps[0], seps[-1]] if seps else None
        extremes["separation_milli_least_largest"] = [min(s for _t, s in seps), max(s for _t, s in seps)] if seps else None
        extremes["peak_distance_least"] = min(r["peak_distance"] for r in readings if r.get("peak_distance") is not None)
        extremes["intervals_peaks_adjacent_bodies"] = sum(1 for r in readings if r.get("peak_distance") == 1)
        extremes["intervals_peaks_same_node_bodies"] = sum(1 for r in readings if r.get("peak_distance") == 0)
    print(json.dumps({"marks": out, "extremes": extremes, "summary": summary}, default=str))
    Path(path).with_suffix(".summary.json").write_text(json.dumps({"marks": out, "extremes": extremes, "summary": summary}, indent=1, default=str) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
