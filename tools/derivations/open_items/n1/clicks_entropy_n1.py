"""Hand n1 (2026-10-25): the clicks log read for what the lattice conserves and for the entropy of the clicks, integers only.

Input: a clicks log (jsonl) of the hole seed's run. Readings: the lines per event; every birth's senses summed
(the charge in the clicks), taken against walls + excess (the exact take, the count in the clicks), the excess below
the step; every credit's beat (None or an integer), its point (one pair or a pair of pairs), its momentum present,
its sense, its kind, its proper; the identities and their credits; the record's growth at checkpoints: N(t) the
credit lines to t, B(t) the births to t, D(t) the distinct credit records to t (the tuple of the readings the
decoder may read: family, identity, point, sense, beat, support, momentum, proper, windows), each monotone by
construction; the integer entropy readings: bits(D) = D.bit_length() and bits(N), and the law's own per-click
entropy as the digits' budget, which the credit line does NOT carry (no weights' total, no candidates' count on the
line): named as the lack. Also the senses' running sum over the births (the charge conserved in the clicks) and the
light's and the bodies' credits apart (only a bound body clicks, the births the light's meetings).
"""
from __future__ import annotations

import json
import sys


def main(path: str, checkpoints=(50, 100, 150, 200, 250, 300)) -> None:
    events: dict[str, int] = {}
    births = 0
    senses_zero = 0
    senses_running = 0
    take_identity = 0
    excess_below_step = 0
    children_count: dict[str, int] = {}
    credits = 0
    beat_none = beat_int = 0
    point_pair = point_pairpair = point_none = 0
    momentum_present = 0
    sense_values: dict[int, int] = {}
    kinds: dict[str, int] = {}
    identities: dict[str, int] = {}
    ident_span: dict = {}
    birth_intervals: list[int] = []
    light_credits = body_credits = 0
    distinct: set = set()
    refused = 0
    refusals: dict[str, int] = {}
    last_interval = 0
    marks = []
    check_i = 0
    lines = [json.loads(l) for l in open(path)]
    for d in lines:
        ev = d.get("event")
        events[ev] = events.get(ev, 0) + 1
        t = d.get("interval", 0)
        last_interval = max(last_interval, t)
        while check_i < len(checkpoints) and t > checkpoints[check_i]:
            marks.append((checkpoints[check_i], credits, births, len(distinct), len(distinct).bit_length(), credits.bit_length()))
            check_i += 1
        if ev == "birth":
            births += 1
            birth_intervals.append(t)
            s = sum(d["senses"])
            senses_running += s
            senses_zero += s == 0
            take_identity += d["taken"] == d["walls"] + d["excess"]
            excess_below_step += d["excess"] < d["step"]
            for c in d["children"]:
                children_count[c] = children_count.get(c, 0) + 1
        elif ev == "credit":
            credits += 1
            b = d.get("beat")
            if b is None:
                beat_none += 1
            else:
                beat_int += 1
            p = d.get("point")
            if p is None:
                point_none += 1
            elif isinstance(p, list) and p and isinstance(p[0], list):
                point_pairpair += 1
            else:
                point_pair += 1
            momentum_present += d.get("momentum") is not None
            sv = d.get("sense")
            sense_values[sv] = sense_values.get(sv, 0) + 1
            k = str(d.get("kind"))
            kinds[k] = kinds.get(k, 0) + 1
            ident = str(d.get("identity"))
            identities[ident] = identities.get(ident, 0) + 1
            if str(d.get("kind")) == "1":
                light_credits += 1  # a real line's credit: the light taken at a birth
            else:
                body_credits += 1  # a plane's credit: a bound body's closing (its identity the body's record)
            ident_span.setdefault(ident, [t, t, 0, []])
            ident_span[ident][1] = t
            ident_span[ident][2] += 1
            if len(ident_span[ident][3]) < 12:
                ident_span[ident][3].append(d.get("proper"))
            distinct.add(json.dumps([d.get("family"), d.get("identity"), d.get("point"), d.get("sense"), d.get("beat"),
                                     d.get("support"), d.get("momentum"), d.get("proper"), d.get("windows")], sort_keys=True))
        elif ev == "refused":
            refused += 1
            c = str(d.get("cause", d.get("reason", "")))[:40]
            refusals[c] = refusals.get(c, 0) + 1
    while check_i < len(checkpoints):
        marks.append((checkpoints[check_i], credits, births, len(distinct), len(distinct).bit_length(), credits.bit_length()))
        check_i += 1
    print(f"log {path}: {len(lines)} lines to interval {last_interval}; events {events}")
    print(f"births {births}: senses sum 0 at {senses_zero} of {births} (the charge in the clicks); running sum of the senses {senses_running};"
          f" taken = walls + excess at {take_identity} of {births} (the count in the clicks); excess below the step at {excess_below_step} of {births}")
    print(f"children born per point: {children_count}")
    print(f"credits {credits}: light's {light_credits}, the bodies' {body_credits}; beat an integer on {beat_int}, None on {beat_none};"
          f" point one pair {point_pair}, a pair of pairs {point_pairpair}, None {point_none}; momentum present {momentum_present}")
    print(f"senses on the credits {sense_values}; kinds {kinds}; identities {len(identities)} with credits {sorted(identities.values())[:12]}...")
    print(f"refused lines {refused}: {refusals}")
    print(f"the births' intervals: {birth_intervals}")
    for k, v in ident_span.items():
        print(f"  identity {k}: credits {v[2]} from interval {v[0]} to {v[1]}; its first proper counts {v[3]}")
    print("the record's growth (interval, N credits, B births, D distinct credit records, bits(D), bits(N)):")
    for m in marks:
        print("  ", m)
    print(f"monotone: N and D never fall (by construction of the log, appended only); the per-click entropy of the law,"
          f" the digits' budget log2 of the draw's total, is on NO line of this log (keys lack the weights' total and the candidates' count): the lack named.")


if __name__ == "__main__":
    main(sys.argv[1])
