"""The Node-clocks' ticks, read from the rate lines: proper time, where no count stands outside a Node-clock."""

# A Node-clock's rate line stands at its first beat and at each beat whose k differs from its last beat's, with the
# count the beat reached, the first beat being 1, and k a bit under the second promise (the schema): so its ticks up to
# and with its beat at a count are the beats of its stretches whose k is 1 (Animate). They are read where its rate
# lines stand from its first beat, each with a whole count and a k that is a bit, the counts rising and no k repeated,
# at a whole count from 0 (before its first beat, no tick); else they are not read, and the cause is named. A line that
# lacks its count or k stands as the line holds it, so it is seen. A Node-clock's lines are read once for all its
# counts: the ticks before each stretch summed once, each count found among the stretches by bisection.

import bisect
from typing import Any

from tensor24.decoder.records import Record, whole

Stretch = tuple[Any, Any]  # a rate line's count and k, as the line holds them
BIT = (0, 1)  # a beat's k under the second promise


def stretches(record: Record) -> dict[int, list[Stretch]]:
    """Each Node-clock's rate lines as (count, k), in the record's order, as the lines hold them."""
    by_site: dict[int, list[Stretch]] = {}
    for line in record.of("rate"):
        by_site.setdefault(line["site"], []).append((line.get("count"), line.get("k")))
    return by_site


def stands(lines: list[Stretch]) -> str:
    """Why a Node-clock's rate lines are not read, or nothing where they are."""
    counts, ks = [c for c, _ in lines], [k for _, k in lines]
    if not lines:
        return "its Node-clock holds no rate line"
    if not all(whole(c) and whole(k) for c, k in lines):
        return "a rate line of its Node-clock holds no whole count and k"
    if not all(k in BIT for k in ks):
        return "a rate line of its Node-clock holds a k that is no bit"
    if counts[0] != 1:
        return "its Node-clock's first rate line stands at no first beat"
    if not all(a < b for a, b in zip(counts, counts[1:], strict=False)):
        return "its Node-clock's rate lines do not rise in count"
    if not all(a != b for a, b in zip(ks, ks[1:], strict=False)):
        return "its Node-clock's rate lines repeat a k"
    return ""


def unread(lines: list[Stretch], count: Any) -> str:
    """Why a Node-clock's ticks up to a count are not read from its rate lines, or nothing where they are."""
    if not whole(count) or count < 0:
        return "the count is no whole number from 0"
    return stands(lines)


def ticks_at(lines: list[Stretch], counts: list[Any]) -> list[int | None]:
    """The ticks of one Node-clock up to and with its beat at each count, or None where they are not read."""
    if stands(lines):
        return [None for _ in counts]
    starts, ks = [c for c, _ in lines], [k for _, k in lines]
    before = [0]
    for (start, k), following in zip(lines, starts[1:], strict=False):
        before.append(before[-1] + k * (following - start))
    found = []
    for count in counts:
        at = bisect.bisect_right(starts, count) - 1 if whole(count) and count >= 0 else None
        found.append(
            None if at is None else 0 if at < 0 else before[at] + ks[at] * (count - starts[at] + 1)
        )
    return found


def ticks_to(lines: list[Stretch], count: Any) -> int | None:
    """The ticks of one Node-clock up to and with its beat at count, or None where they are not read."""
    return ticks_at(lines, [count])[0]
