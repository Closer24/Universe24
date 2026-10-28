"""The Node-clocks' ticks, read from the rate lines: proper time, where no count stands outside a Node-clock."""

# A Node-clock's rate line stands at its first beat and at each beat whose k differs from its last beat's, with the
# beat's count (Animate); so its ticks up to and with its beat at a count are the beats of its stretches whose k is 1.

from typing import Any

from tensor24.decoder.records import Record

Line = dict[str, Any]


def stretches(record: Record) -> dict[int, list[tuple[int, int]]]:
    """Each Node-clock's rate lines as (count, k), in the record's order."""
    by_site: dict[int, list[tuple[int, int]]] = {}
    for line in record.of("rate"):
        by_site.setdefault(line["site"], []).append((line["count"], line["k"]))
    return by_site


def ticks_to(lines: list[tuple[int, int]], count: int) -> int:
    """The ticks of one Node-clock up to and with its beat at count."""
    ticks = 0
    for (start, k), (following, _) in zip(lines, [*lines[1:], (count + 1, 0)], strict=True):
        if start <= count:
            end = following if following <= count else count + 1
            ticks += k * (end - start)
    return ticks
