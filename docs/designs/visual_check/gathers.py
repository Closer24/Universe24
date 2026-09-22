"""The gather lines of the amplitude worlds (series L): one click per record.

A record's one click is its `gather` line (BEAM_LAW note 37): `chosen` names
the set, the arm and the outcome the wheel chose, `record` carries the birth
ordinal in its low 32 bits, `cells` the rungs the click was drawn from. The
register reads the lamp's first `births` records by ordinal (the amplitude
README); so do these scripts. Every count here is an integer (DETECTOR).
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from common import events, ordinal


def chosen_by_ordinal(folder: Path, births: int) -> dict[int, tuple]:
    """The chosen outcome per birth ordinal 1 .. births: a tuple of (set, arm, outcome)."""
    found: dict[int, tuple] = {}
    for line in events(folder, {"gather"}):
        n = ordinal(int(line["record"]))
        if 1 <= n <= births and n not in found:
            found[n] = tuple((c[0], int(c[1]), str(c[2])) for c in line["chosen"])
    return found


def outcome_counts(folder: Path, births: int, sets: tuple[str, ...] | None = None) -> Counter:
    """The counts of the outcome strings (one character per chosen set, in the set order given)."""
    counts: Counter = Counter()
    for chosen in chosen_by_ordinal(folder, births).values():
        by_set = {c[0]: c[2] for c in chosen}
        order = sets if sets is not None else tuple(c[0] for c in chosen)
        counts["".join(by_set[s] for s in order)] += 1
    return counts


def gather_ticks(folder: Path, births: int) -> dict[int, int]:
    """The tick of each record's gather, by ordinal (the completion interval)."""
    ticks: dict[int, int] = {}
    for line in events(folder, {"gather"}):
        n = ordinal(int(line["record"]))
        if 1 <= n <= births and n not in ticks:
            ticks[n] = int(line["tick"])
    return ticks


def correlation(counts: Counter) -> int:
    """E in counts: c(++) + c(--) - c(+-) - c(-+); the register's `E` (an integer over the births)."""
    return counts["++"] + counts["--"] - counts["+-"] - counts["-+"]
