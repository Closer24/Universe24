"""bb1's reader: one compact summary per record (the counts, the run back, the bits, the tops, the returns to the
seed's X, the spread's course, the births by interval, the 48) and the lift's form checked against the Links' sum
read on the run: lift_pace = SUM over Links of quotient(Gamma (X_j - X_i)^2, 3 X_i X_j) (the reach the Link pace
squared, (p_i / Gamma)^2 = Gamma / X) against lift_clock = SUM over Links of quotient((X_j - X_i)^2 largest_below(Gamma X_i),
2 X_i^2) (BG's form, (p / Gamma)^2 = sqrt(Gamma / X)). Usage: read_all.py <name> [<name> ...] (names under out/)."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "src"))
from event_universe.core.rule3 import largest_below  # noqa: E402

AT = (2, 5, 10, 20, 40, 60, 100, 130, 160, 200, 250, 300)


def links_of(cube: int):
    found = []
    for x in range(cube):
        for y in range(cube):
            for z in range(cube):
                i = x * cube * cube + y * cube + z
                for j in (
                    ((x + 1) % cube) * cube * cube + y * cube + z,
                    x * cube * cube + ((y + 1) % cube) * cube + z,
                    x * cube * cube + y * cube + (z + 1) % cube,
                ):
                    found.append((i, j))
    return found


def lifts(xs: list[int], links, gamma: int) -> tuple[int, int, int]:
    pace = clock = 0
    emax = 0
    for i, j in links:
        a, b = int(xs[i]), int(xs[j])
        d = b - a
        pace += gamma * d * d // (3 * a * b)
        clock += d * d * largest_below(gamma * a) // (2 * a * a)
        emax = max(emax, abs(d) * 1000 // min(a, b))
    return pace, clock, emax


def main() -> None:
    sys.set_int_max_str_digits(0)
    for name in sys.argv[1:]:
        lines = [json.loads(line) for line in open(os.path.join(HERE, "out", name + ".jsonl"), encoding="utf-8")]
        s, rows = lines[0]["summary"], lines[1:]
        print("=" * 8, name, "laid", s["laid"])
        c = s["counts"]
        print(
            "births", c["births"], "credits", s["credits"], "turns", c["turns"], "refused lay/orient/stop",
            c["refused_lay"], c["refused_orientation"], c["refused_stop"], "run back", s["run_back"],
            "bits", s["state_bits"], "/", s["transient_bits"], "integers", s["integers"], "48", s["48 at the end"],
            "seconds", s["seconds"],
        )
        print("tops", s["tops (interval, mean X)"][:8])
        print("at the seed's X", s["intervals at the seed's mean X"], "uniform intervals", s["uniform intervals (x_min == x_max)"])
        print("runs", s["runs of the mean (start, end, X start, X end)"][:8])
        print("births at", s["births_by_interval"][:20])
        by = {r["i"]: r for r in rows}
        print("i: mean X | min | max | e_max | e_mean | mass | links | write | turned | births | content max")
        for i in AT:
            if i in by:
                r = by[i]
                print(
                    i, ":", r["x_mean"], "|", r["x_min"], "|", r["x_max"], "|", r["e_max"], "|", r["e_mean"], "|",
                    r["mass_sum"], "|", r["links_sum"], "|", r["write_sum"], "|", r["turned"], "|", r["births"], "|",
                    r["content_max"],
                )
        last = rows[-1]
        print("last", last["i"], ":", last["x_mean"], last["x_min"], last["x_max"], "e", last["e_max"], last["e_mean"], "mass", last["mass_sum"], "links", last["links_sum"], "write", last["write_sum"])
        emax_all = max(r["e_max"] for r in rows)
        print("e_max over the run", emax_all, "at", next(r["i"] for r in rows if r["e_max"] == emax_all), "; e_max at the first top", by.get(s["tops (interval, mean X)"][0][0], {}).get("e_max") if s["tops (interval, mean X)"] else None)
        rec_path = os.path.join(HERE, "out", name + "_record.json")
        if os.path.exists(rec_path) and "lift" in os.environ.get("BB1_READ", "lift"):
            rec = json.load(open(rec_path, encoding="utf-8"))
            nodes, gamma, cube = rec["nodes"], rec["gamma"], rec["cube"]
            links = links_of(cube)
            print("lift check (i: measured links_sum | lift_pace | lift_clock | e_max)")
            for i in AT:
                if i - 2 < len(nodes) and i in by and i >= 2:
                    pace, clock, emax = lifts(nodes[i - 2]["X"], links, gamma)
                    print(i, ":", by[i]["links_sum"], "|", pace, "|", clock, "|", emax)


if __name__ == "__main__":
    main()
