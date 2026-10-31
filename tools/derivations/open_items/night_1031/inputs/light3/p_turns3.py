"""LIGHT3's turn count, on one record, by p_light3's own readings: (1) of the clocks of matter trains that meet light,
how many turn somewhere in the record (a light give to the site its last light take came from, all of that round's
takes from that one site), and how many turns each holds at the least and the most; (2) whether the clocks the cone
never reaches from the first round's meetings are exactly one whole component of the meeting graph."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p_light3 as rule  # noqa: E402


def main():
    path = Path(sys.argv[1])
    clicks, cause = rule.read(path)
    if cause:
        print(f"{path.name}: NOT READ, {cause}")
        return
    meets = rule.meetings(clicks)
    medium, matter = rule.eligible(meets)
    light = sorted(m for m in meets if m[3] == "mesh" and (m[1] in medium or m[2] in medium))
    takes, gives = {}, {}
    for r, g, k, _ in light:
        gives.setdefault(g, []).append((r, k))
        takes.setdefault(k, []).append((r, g))
    counts = []
    for c in sorted(matter):
        if c not in gives and c not in takes:
            continue
        n = 0
        for b2, k2 in gives.get(c, ()):
            before = [(r, g) for r, g in takes.get(c, ()) if r < b2]
            if before:
                b1 = max(r for r, _ in before)
                if all(g[0] == k2[0] for r, g in before if r == b1):
                    n += 1
        counts.append(n)
    turning = sum(1 for n in counts if n > 0)
    print(f"{path.name}: clocks of matter trains meeting light {len(counts)}; with a turn somewhere {turning}; turns per "
          f"clock from {min(counts) if counts else '-'} to {max(counts) if counts else '-'}")
    comps = rule.components(meets)
    by_round = {}
    for m in meets:
        by_round.setdefault(m[0], []).append(m)
    first = min(by_round)
    start = {c: first for _, g, k, _ in by_round[first] for c in (g, k)}
    arrival = rule.reach(start, by_round, first + 1, max(by_round), False, set())
    clocks = {c for _, g, k, _ in meets for c in (g, k)}
    never = clocks - set(arrival)
    whole = [len(comp) for comp in comps if set(comp) == never]
    print(f"  the cone's never-reached clocks {len(never)}; exactly one whole component: {bool(whole)}"
          f"{' (' + str(whole[0]) + ' clocks)' if whole else ''}")


if __name__ == "__main__":
    main()
