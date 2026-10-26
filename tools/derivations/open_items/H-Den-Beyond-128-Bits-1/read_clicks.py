"""Hand dn1: the clicks of a run read by David's decoder (decoder_full.gates, imported and never edited) and, beside it, the readings this brief asks from the credit lines alone: the births per lift with their senses summed (the charge), the taken against the booked (the count), the beats of the born records per lift (gate 19 from the clicks) against the legs' ratio of the header, the credits' and births' bit lengths. Integers only.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/open_items/H-Den-Beyond-128-Bits-1/read_clicks.py <out.json of run_toy.py> <reading.json>
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "toy"))
sys.set_int_max_str_digits(0)

from decoder_full import gates  # the toy's decoder, imported and never edited

from event_universe.core.paces import sine_den


def quot(a: int, b: int, scale: int) -> list[int]:
    q, r = divmod(a * scale, b)
    return [int(q), int(r)]


def main() -> None:
    run = json.load(open(sys.argv[1]))
    den = int(run["den"])
    planes = [int(x) for x in run["planes"]]
    legs = {k: sine_den(num, den) for k, num in enumerate(planes) if num != den}
    by_leg = sorted(legs.items(), key=lambda kv: kv[1])
    names = {k: name for (k, _leg), name in zip(by_leg, ("lightest lift", "middle lift", "heaviest lift"))}
    log = run["log"]
    births = [e for e in log if e["event"] == "birth"]
    credits = [e for e in log if e["event"] == "credit"]
    out = {"den_bits": den.bit_length(), "intervals": run["intervals"], "cube": run["cube"], "counts": run["counts"], "run_back": run["run_back"]}
    out["births_per_lift"] = {names[e]: n for e, n in Counter(e["line_pair"] for e in births).items()}
    out["births_intervals_first_last"] = [births[0]["i"], births[-1]["i"]] if births else None
    out["charge_senses_sum_over_births"] = sum(s for e in births for s in e["senses"])
    taken, booked = sum(e["taken"] for e in births), sum(e["booked"] for e in births)
    out["count_taken_over_booked"] = {"taken": taken, "booked": booked, "excess": taken - booked, "taken_per_booked_hundredths": quot(taken, booked, 100) if booked else None, "births_at_excess_0": sum(1 for e in births if e["taken"] == e["booked"]), "identity_taken_at_least_booked_on_every_birth": all(e["taken"] >= e["booked"] for e in births)}
    out["births_rooms_bits"] = sorted(Counter((int(e["room"]) - 1).bit_length() for e in births).items())
    out["body_credits_per_lift"] = {names[e]: n for e, n in Counter(e["line"] for e in credits).items()}
    beats = {}
    for k in legs:
        bs = sorted(int(e["beat"]) for e in credits if e["line"] == k and int(e["beat"]) > 0)
        beats[names[k]] = {"credits_with_a_beat": len(bs), "beat_min_median_max": [bs[0], bs[len(bs) // 2], bs[-1]] if bs else None, "beat_histogram": dict(sorted(Counter(bs).items())[:12])}
    out["beats_from_the_clicks_per_lift"] = beats
    # the mass ratio from the clicks: the beat (intervals per period) is 2 pi den / s; two lifts' beats stand in the inverse ratio of their legs
    header = {}
    for (ka, sa), (kb, sb) in zip(by_leg, by_leg[1:]):
        header[f"{names[kb]} over {names[ka]} legs per 1e6"] = quot(sb, sa, 10**6)
        ba = sorted(int(e["beat"]) for e in credits if e["line"] == ka and int(e["beat"]) > 0)
        bb = sorted(int(e["beat"]) for e in credits if e["line"] == kb and int(e["beat"]) > 0)
        if ba and bb:
            header[f"{names[ka]} beat over {names[kb]} beat (medians) per 1e6"] = quot(ba[len(ba) // 2], bb[len(bb) // 2], 10**6)
        else:
            header[f"{names[ka]} beat over {names[kb]} beat"] = "no beat read for one of the two (no body credit within the run)"
    header["expected beat per period at the vacuum (intervals), per lift: 2 pi den div s as 6283185 x (den div s) div 1000000"] = {names[k]: (6283185 * (den // s)) // 10**6 for k, s in by_leg}
    out["mass_ratios_header_against_clicks"] = header
    out["decoder_gates"] = gates(run)
    json.dump(out, open(sys.argv[2], "w"), default=str, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "decoder_gates"}, default=str))
    for k, v in out["decoder_gates"].items():
        print(json.dumps({k: v}, default=str)[:600])


if __name__ == "__main__":
    main()
