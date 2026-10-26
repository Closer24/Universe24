"""The bang rows of the board, read from the Node lines: gate 1, the recurring bang (the board tops with every Node turning at once, falls back to the seed's own first state and rises again), row 1b the tops and row 1c the exact returns (the Boss's 6416499848: the return is to the seed's first state, every Node's X and content as the first Node line holds them, and not to a constant of the universe; the bottoms at Gamma, the resolution, named beside), with the rows' reading of the returns kept by name; moved whole out of board.py at the Reader's mend of the return."""

from __future__ import annotations

from typing import Any

from event_universe.decoder import FOUR_LISTED, LISTED, Record, unread_words

BIRTHS = 2  # the index of the births in a mark (the interval, the mean volume, the births)


def marks(record: Record) -> tuple[list[tuple[int, int, int]], list[tuple[int, int]]]:
    """The rows' marks (interval, the mean volume, the births so far) and the steps of the mean volume between marks (the interval, the difference)."""
    rows = [(r["i"], int(r["volume mean"]), int(r["births"])) for r in record.rows]
    return rows, [(b[0], b[1] - a[1]) for a, b in zip(rows, rows[1:], strict=False)]


def returns_of(record: Record) -> list[tuple[int, int, int]]:
    """The marks at which the mean volume is back at or below the first mark's with a birth after the first mark (the rows' reading, kept beside the Node lines')."""
    rows, _steps = marks(record)
    return [(i, v, b) for i, v, b in rows[1:] if v <= rows[0][1] and b > rows[0][BIRTHS]] if rows else []


def volumes(record: Record) -> list[tuple[int, list[int], int]]:
    """The Node lines' volumes: per interval (the interval, every Node's X, the count of Nodes turned)."""
    return [(int(line["i"]), [int(x) for x in line["X"]], len(line["turned"])) for line in record.nodes]


def bottoms_of(record: Record) -> list[tuple[int, int, bool]]:
    """The bottoms of the mean volume in the Node lines (a local least, at or below the mark before and below the one after): the interval, the mean, and whether every Node stands at Gamma exactly, the resolution (named beside the exact returns, no longer the return's predicate: the Boss's 6416499848)."""
    lines = volumes(record)
    means = [sum(xs) // len(xs) for _i, xs, _t in lines]
    return [
        (lines[k][0], means[k], all(x == record.gamma for x in lines[k][1]))
        for k in range(1, len(means) - 1)
        if means[k] <= means[k - 1] and means[k] < means[k + 1]
    ]


def tops_of(record: Record) -> list[int]:
    """The intervals at which every Node turned at once, the board's tops, from the Node lines."""
    lines = volumes(record)
    count = len(lines[0][1]) if lines else 0
    return [i for i, _xs, turned in lines if turned == count and count]


def state_of(line: dict[str, Any]) -> tuple[list[int], list[int]]:
    """A Node line's state, every Node's volume X and content as the line holds them."""
    return [int(x) for x in line["X"]], [int(c) for c in line["content"]]


def exact_of(record: Record) -> list[int]:
    """The intervals of the exact returns (the Boss's 6416499848): the board back at the seed's own first state, every Node's X and content as the first Node line holds them, and not at a constant of the universe (on a sea laid at Gamma the two are one); a run of such lines with no whole-board top between them is one return, read at its last line (the board passes down through the seed's state to its bottom and up through it again, the rising side the bang's)."""
    lines = record.nodes
    if not lines:
        return []
    first, tops = state_of(lines[0]), tops_of(record)
    matches = [int(line["i"]) for line in lines[1:] if state_of(line) == first]
    found: list[int] = []
    for i in matches:
        if found and not any(found[-1] < t < i for t in tops):
            found[-1] = i
        else:
            found.append(i)
    return found


def repeats_of(record: Record) -> list[int]:
    """The exact returns at which the course repeats whole: the line after the return equal to the second Node line too, the pair that fixes Rule3's course (the seed's first pair of states)."""
    lines = record.nodes
    second = state_of(lines[1]) if len(lines) > 1 else None
    return [
        i for i in exact_of(record) if i < len(lines) and state_of(lines[i]) == second
    ]  # the line after the interval i is lines[i] (the lines from 1)


def recurring_bang(record: Record) -> dict[str, Any]:
    """Gate 1 (MA-S1's predicate, the Boss's 6400767119): the recurring bang from the Node lines: the board tops with every Node turning at once, falls to a bottom at the seed's first volumes at every Node exactly (the exact return, the Boss's 6416499848) and rises again; the bangs numbered from the seed's, the births and the body credits counted between the returns."""
    lines, whole, bottoms = volumes(record), tops_of(record), bottoms_of(record)
    exact = exact_of(record)
    bangs = [1] + exact
    between = [
        [
            sum(1 for b in record.births if lo <= int(b["i"]) < hi),
            sum(1 for c in record.credits if lo <= int(c["i"]) < hi),
        ]
        for lo, hi in zip(bangs, bangs[1:] + [record.intervals + 1], strict=False)
    ]
    verdict = (
        unread_words(
            "no Node line in the record",
            "the exact return to the seed's first state with the whole board turning at the top",
        )
        if not lines
        else f"SHOWN: {len(exact)} exact returns to the seed's first state, the whole board turning at once at {len(whole)} tops, {len(bangs)} bangs"
        if exact and whole
        else f"NOT SHOWN: no return to the seed's first state, the bottom at {bottoms[0][1]} against the seed's mean volume {sum(lines[0][1]) // len(lines[0][1])} (Gamma {record.gamma})"
        + (", the whole board turning at once at the top" if whole else ", no whole-board turn")
        if bottoms
        else "NOT SHOWN: no bottom of the mean volume"
        + (", the whole board turning at once" if whole else "")
    )
    return {
        "1 recurring bangs": {
            "tops with every Node turning at once (interval)": whole[:LISTED],
            "exact returns to the seed's first state (interval)": exact[:LISTED],
            "of them repeating the course whole (the first pair of states)": repeats_of(record)[:LISTED],
            "bottoms (interval, mean X, at Gamma at every Node, the resolution)": bottoms[:LISTED],
            "bangs numbered (the interval each begins)": bangs[:LISTED],
            "births and body credits between the bangs": between[:LISTED],
            "rows' reading: marks back at or below the first mark's with a birth after it": returns_of(
                record
            )[:FOUR_LISTED],
            "verdict": verdict,
        }
    }


def tops(record: Record) -> dict[str, Any]:
    """Row 1b (the owner's word of 2026-10-26, 00:5x UTC: the top in the gate too): the board tops, every Node turning at once at one interval, read from the Node lines as gate 1 reads them; SHOWN from the first such top."""
    lines, whole = volumes(record), tops_of(record)
    return {
        "1b the board tops, every Node turning at once": {
            "tops (interval)": whole[:LISTED],
            "verdict": unread_words("no Node line in the record", "every Node turned at one interval")
            if not lines
            else f"SHOWN: the whole board turns at once at {len(whole)} tops, the first at {whole[0]}"
            if whole
            else "NOT SHOWN: no interval with every Node turned",
        }
    }


def returns(record: Record) -> dict[str, Any]:
    """Row 1c (the same word: the return in the gate too): the board returns to the seed, a bottom of the mean volume with every Node's volume at the seed's own first state exactly (the Boss's 6416499848), read from the Node lines as gate 1 reads them; SHOWN from the first such return."""
    exact = exact_of(record)
    return {
        "1c the board returns to the seed": {
            "exact returns (interval)": exact[:LISTED],
            "verdict": unread_words(
                "no Node line in the record",
                "the board back at the seed's first state, every Node's X and content as the first Node line holds them",
            )
            if not record.nodes
            else f"SHOWN: {len(exact)} exact returns to the seed's first state, the first at {exact[0]}"
            if exact
            else "NOT SHOWN: no return to the seed's first state",
        }
    }
