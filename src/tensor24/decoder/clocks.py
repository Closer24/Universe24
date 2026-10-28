"""The Node-clocks' ticks, read from the rate lines: proper time, where no count stands outside a Node-clock."""

# A Node-clock's rate line stands at its first beat and at each beat whose k differs from its last beat's, with the
# count the beat reached, the first beat being 1 (the schema): so its ticks up to and with its beat at a count are the
# beats of its stretches whose k is 1 (Animate). They are read where its rate lines stand from its first beat, each
# with a whole count and k, the counts rising, at a whole count from 0 (before its first beat, no tick); else they are
# not read, and the cause is named. A line that lacks its count or k stands as the line holds it, so it is seen.

from typing import Any

from tensor24.decoder.records import Record, whole

Stretch = tuple[Any, Any]  # a rate line's count and k, as the line holds them


def stretches(record: Record) -> dict[int, list[Stretch]]:
    """Each Node-clock's rate lines as (count, k), in the record's order, as the lines hold them."""
    by_site: dict[int, list[Stretch]] = {}
    for line in record.of("rate"):
        by_site.setdefault(line["site"], []).append((line.get("count"), line.get("k")))
    return by_site


def unread(lines: list[Stretch], count: Any) -> str:
    """Why a Node-clock's ticks up to a count are not read from its rate lines, or nothing where they are."""
    counts = [c for c, _ in lines]
    if not whole(count) or count < 0:
        return "the count is no whole number from 0"
    if not lines:
        return "its Node-clock holds no rate line"
    if not all(whole(c) and whole(k) for c, k in lines):
        return "a rate line of its Node-clock holds no whole count and k"
    if counts[0] != 1:
        return "its Node-clock's first rate line stands at no first beat"
    if not all(a < b for a, b in zip(counts, counts[1:], strict=False)):
        return "its Node-clock's rate lines do not rise in count"
    return ""


def ticks_to(lines: list[Stretch], count: Any) -> int | None:
    """The ticks of one Node-clock up to and with its beat at count, or None where they are not read."""
    if unread(lines, count):
        return None
    ticks = 0
    for (start, k), (following, _) in zip(lines, [*lines[1:], (count + 1, 0)], strict=True):
        if start <= count:
            ticks += k * ((following if following <= count else count + 1) - start)
    return ticks
