"""Clock: n/a: the decoder's readings of the three clicks on schema 1.4's click lines, from the record alone, by each place's structure and never by a label (DECODE3, folded on its two hostile readers by the Boss's rulings of 05:1x and 05:2x UTC and DECODE3b): where two clocks alone meet, the first click; where three clocks or more meet, the passing splits and the turn lands it, the third click.
Algebra: whole counts and sums alone: each side's passing x = D q + k_after - k_before, D the header's dial, the split's weights kept as pairs of whole numbers (x_tu, X_t), and a round's part of the record by Rule3's carry; no other division, no float, no root and no search.
Board: the lines' sides in their site, [u, q, k_before, k_after], and across a Mesh, [u, place, q, k_before, k_after], read after the sides' guard has passed; the teeth and the header's dial are board fields carried for the checks, never the click world's physics (the Boss's ruling of 05:2x UTC).
Clicks: read in the click world, on the lines, their rounds, their q and their sides' trains and q: the structure per place, which side lands, and R2 within one record; the checks: the passings and the split's weights against the board's passing, and, on two records compared on their q's alone line for line in the schema's order, R1, R2's two-record form and the swap. Owed, not built: the shares against the weights (3a), the Fano factor (3b), the takers' correlation (3c) and the lives (3d), DECODE3b's, and CHSH with no signal (R4), which waits on Big Pic's stage 4.
"""

from typing import Any

from tensor24.algebra.carry import carry
from tensor24.decoder import clicks, measure
from tensor24.decoder.records import Line, Record, whole
from tensor24.decoder.shadow import ABSENT, NO_LINE, Verdict, lacking
from tensor24.decoder.sides import edged

READ = "READ"  # an extraction read, with no verdict of its own
STRUCTURE = "the structure per place"
PASSING = "the passings and the split's weights, a check of the clicks against the board's passing"
LANDS = "which side lands"
WITHIN = "R2 within one record, by the q's alone"
SWAP = "the swap, a check on two records"
RUN_TWICE = "R1, one lay run twice, a check on two records"
APART = "R2's two-record form, a check on two records"
OWED = (
    "owed, not built: the shares against the weights (3a), the Fano factor (3b), the takers' correlation (3c) and"
    " the lives (3d), DECODE3b's, and CHSH with no signal (R4), Big Pic's stage 4's"
)
Edge = frozenset[int]
Joined = dict[int, list[tuple[int, int]]]  # a place's trains, each with its in-site sides' trains and q


def unread(record: Record) -> Verdict | None:
    """NO CLICK on a record of no click line, NOT READ naming a click line that holds no sides, schema 1.3's, else none."""
    lines = clicks.listed(record)
    bare = [line for line in lines if "sides" not in line and "across" not in line]
    if not lines:
        return measure.verdict(ABSENT, NO_LINE)
    if bare:
        where = f"round {bare[0]['round']}, site {bare[0]['site']}"
        return measure.verdict(
            "NOT READ", f"the click line at {where} holds no sides, a line of schema 1.3"
        )
    return None


def joined(lines: list[Line]) -> dict[clicks.Place, Joined]:
    """Each place, a round and a Node-clock, with each train's in-site sides there as (u, q)."""
    found: dict[clicks.Place, Joined] = {}
    for line in lines:
        held = [(u, q) for u, q, _, _ in line.get("sides", [])]
        found.setdefault((line["round"], line["site"]), {})[line["train"]] = held
    return found


def ends(held: Joined) -> dict[Edge, set[int]]:
    """A place's pairs {t, u} its in-site sides name, each with the trains whose lines name it: an edge where both do."""
    found: dict[Edge, set[int]] = {}
    for t, sides in held.items():
        for u, _ in sides:
            found.setdefault(frozenset((t, u)), set()).add(t)
    return found


def edges_of(held: Joined) -> set[Edge]:
    """A place's edges, the distinct pairs {t, u} seen from both ends."""
    return {pair for pair, seen in ends(held).items() if seen == pair}


def named(held: Joined) -> tuple[int, int, str]:
    """A place's structure: its clocks counted (the lines' trains and every train their sides name), its edges counted, and its name: two clocks alone (one edge), all pairwise joined (three clocks or more), not all joined, or no edge in its site (its lines' sides all across a Mesh)."""
    clocks = set(held) | {u for sides in held.values() for u, _ in sides}
    edges = edges_of(held)
    pairs = {frozenset((a, b)) for a in clocks for b in clocks if a < b}
    joined = "two clocks alone" if len(edges) == 1 else "all pairwise joined"
    partial = "not all joined" if edges else "no edge in its site"
    return len(clocks), len(edges), joined if edges and edges == pairs else partial


def omitted(places: dict[clicks.Place, Joined]) -> list[tuple[clicks.Place, int, int]]:
    """Each place, train and other train where a clock's line holds no side to a clock its site joins it to at another place: a side at q 0 left out, so the place's structure there is a lower bound."""
    union: dict[int, set[Edge]] = {}
    for (_, site), held in places.items():
        union.setdefault(site, set()).update(edges_of(held))
    return [
        ((round_, site), t, u)
        for (round_, site), held in places.items()
        for t, sides in held.items()
        for edge in union[site]
        if t in edge
        for u in edge - {t}
        if u not in {v for v, _ in sides}
    ]


def structure(record: Record) -> Verdict:
    """The structure per place, read from the sides and never assumed (the Boss's ruling of 05:1x UTC; DECODE3b, section 1): at each round and Node-clock, its clocks and its edges, the distinct pairs each seen from both ends, the place two clocks alone (the first click's), all pairwise joined (the split's and the third click's) or not all joined (a path among them), and each side across a Mesh a meeting of two clocks (the first click's); READ, an extraction with no verdict of its own, counted per place and per site (the union of its places), the lines that leave out a side their site holds counted, the structure a lower bound there; NOT SHOWN at the first pair seen from one end alone; NOT READ on a line of schema 1.3; NO CLICK on a record of no click line."""
    gate = unread(record)
    if gate:
        return gate
    lines = clicks.listed(record)
    places = joined(lines)
    lone = [
        (place, sorted(pair))
        for place, held in places.items()
        for pair in ends(held).keys() - edges_of(held)
    ]
    if lone:
        (round_, site), pair = lone[0]
        cause = f"the pair of trains {pair} at round {round_}, site {site} is seen from one end alone, no edge"
        return measure.verdict("NOT SHOWN", cause)
    kinds: dict[tuple[int, int, str], int] = {}
    for held in places.values():
        kinds[named(held)] = kinds.get(named(held), 0) + 1
    union: dict[int, Joined] = {}
    for (_, site), held in places.items():
        for t, sides in held.items():
            union.setdefault(site, {}).setdefault(t, []).extend(sides)
    sites: dict[tuple[int, int, str], int] = {}
    for held in union.values():
        sites[named(held)] = sites.get(named(held), 0) + 1
    across = len([q for line in lines for _, _, q, _, _ in line.get("across", []) if q < 0])
    left = omitted(places)
    said = "; ".join(
        f"{n} of {c} clocks and {e} edges, {name}" for (c, e, name), n in sorted(kinds.items())
    )
    whole_sites = "; ".join(
        f"{n} of {c} clocks and {e} edges, {name}" for (c, e, name), n in sorted(sites.items())
    )
    cause = f"{len(places)} places: {said}; the {len(union)} sites, each the union of its places: {whole_sites}; {across} meetings across a Mesh, two clocks each; {len(left)} sides left out of a line where its site holds them"
    return measure.verdict(READ, cause, kinds=kinds, sites=sites, across=across, omitted=len(left))


def passing(record: Record) -> Verdict:
    """The passings and the split's weights, a check of the clicks against the board's passing, never a reading of physics (the Boss's ruling of 05:2x UTC), read where the sides' guard has passed, the books standing (DECODE3's MINOR 1: the two ends' passings opposite by the books): each side's passing x = D q + k_after - k_before, D the header's dial, in its site and across a Mesh; and, at each place in a site alone, each clock joined there to two clocks or more that gives along a side (x below 0), the split's weights (u, x_tu, X_t), X_t the sum of x over its giving sides; READ, an extraction; NOT READ where the header holds no dial or a line leaves out a side its site holds (a taker's passing missing), on a line of schema 1.3, and NO CLICK on a record of no click line."""
    gate = unread(record)
    if gate:
        return gate
    dial, lines = record.header.get("dial"), clicks.listed(record)
    left = omitted(joined(lines))
    if not whole(dial):
        return measure.verdict("NOT READ", "the header holds no dial D, the board field the check reads")
    if left:
        ((round_, site), t, u), n = left[0], len(left)
        cause = f"the click line at round {round_}, site {site}, train {t} holds no side to train {u}, which its site holds: a taker's passing missing at {n} sides"
        return measure.verdict("NOT READ", cause)
    passings = [dial * q + after - before for line in lines for _, _, q, before, after in edged(line)]
    weights: dict[tuple[int, int, int], list[tuple[int, int, int]]] = {}
    for line in [line for line in lines if len(line.get("sides", [])) > 1]:
        x = [(u, dial * q + after - before) for u, q, before, after in line["sides"]]
        given = [(u, xu) for u, xu in x if xu < 0]
        total = sum(xu for _, xu in given)
        if given:
            weights[(line["round"], line["site"], line["train"])] = [(u, xu, total) for u, xu in given]
    first = next(iter(weights.items()), None)
    shown = f", the first at round, site and train {first[0]}: {first[1]}" if first else ""
    cause = f"x = D q + k_after - k_before on {len(passings)} sides at the header's dial D = {dial}; the split's weights (u, x_tu, X_t) at {len(weights)} giving clocks joined to two or more in their site{shown}"
    return measure.verdict(READ, cause, weights=weights)


def lands(record: Record) -> Verdict:
    """Which side lands (DECODE3, section 3, in the click world): at each place, every in-site side with q below 0 of a clock joined there to two clocks or more lands abs(q) quanta on its taker, the train it names; the giving sides of a clock joined to one alone, in its site or across a Mesh, are the first click's passings, counted beside; READ, an extraction, counted per giving and taking train; NOT READ on a line of schema 1.3; NO CLICK on a record of no click line."""
    gate = unread(record)
    if gate:
        return gate
    landed: dict[tuple[int, int], int] = {}
    quanta: dict[tuple[int, int], int] = {}
    first = 0
    for line in clicks.listed(record):
        sides, t = line.get("sides", []), line["train"]
        split = [(u, q) for u, q, _, _ in sides if q < 0 and len(sides) > 1]
        for u, q in split:
            landed[(t, u)] = landed.get((t, u), 0) + 1
            quanta[(t, u)] = quanta.get((t, u), 0) - q
        first += len([q for _, _, q, _, _ in edged(line) if q < 0]) - len(split)
    each = ", ".join(
        f"from train {t} to train {u} {n} ({quanta[(t, u)]} quanta)"
        for (t, u), n in sorted(landed.items())
    )
    cause = f"{sum(landed.values())} landings of {sum(quanta.values())} quanta where the giver meets two clocks or more, each naming its taker: {each or 'none'}; beside them {first} passings of the first click, a clock meeting one alone or across a Mesh"
    return measure.verdict(READ, cause, landed=landed, quanta=quanta, first=first)


def ambiguous(series: list[int], length: int) -> int:
    """The pasts of a series, its runs of length entries, that recur and are followed by two different entries or more."""
    after: dict[tuple[int, ...], set[int]] = {}
    for end in range(length, len(series)):
        after.setdefault(tuple(series[end - length : end]), set()).add(series[end])
    return len([past for past, seen in after.items() if len(seen) > 1])


def within(record: Record, chosen: Any) -> Verdict:
    """R2 within one record, by the q's alone (the Boss's ruling of 05:2x UTC, the physicist's B1 (i), DECODE3b's rule): on each single, one-way side (q at most one quantum each round, every quantum of one sign), its q at every round of the record, 0 where it lands none, cut into the readings' parts by Rule3's carry; in each part and at each length of the readings' past ladder, the pasts that recur and are followed by two different q's or more counted; the side SHOWN where every count reaches the readings' count, a carried side holding about one; the record SHOWN where a side is, its distinct series counted, NOT SHOWN where no side read is, NOT READ where the readings name no ladder, count and parts, the end no rounds, or no single, one-way side lands in every part; the readings stated in the cause."""
    gate = unread(record)
    if gate:
        return gate
    held = chosen if isinstance(chosen, dict) else {}
    ladder, count, parts, rounds = (
        held.get("pasts"),
        held.get("count"),
        held.get("parts"),
        record.end.get("rounds"),
    )
    if not (isinstance(ladder, list) and ladder and all(whole(n) and n >= 1 for n in ladder)):
        return measure.verdict(
            "NOT READ", "no readings name R2's past ladder, its count and the record's parts"
        )
    if not (whole(count) and whole(parts) and parts >= 1 and whole(rounds) and rounds >= 1):
        return measure.verdict(
            "NOT READ", "no readings name R2's count and the record's parts, or the end no rounds"
        )
    cut: dict[int, list[int]] = {}
    for r in range(1, rounds + 1):
        cut.setdefault(carry((r - 1) * parts, rounds, 0)[0], []).append(r)
    series: dict[tuple[int, int, int, int], dict[int, int]] = {}
    for line in clicks.listed(record):
        for at, u, q, _, _ in edged(line):
            series.setdefault((line["site"], line["train"], at, u), {})[line["round"]] = q
    one_way = {
        side: q
        for side, q in series.items()
        if all(-1 <= v <= 0 for v in q.values()) or all(0 <= v <= 1 for v in q.values())
    }
    read: dict[tuple[int, int, int, int], list[list[int]]] = {}
    for side, q in one_way.items():
        halves = [[q.get(r, 0) for r in part] for part in cut.values()]
        if all(any(half) for half in halves):
            read[side] = [[ambiguous(half, n) for n in ladder] for half in halves]
    shown = [side for side, counts in read.items() if all(c >= count for part in counts for c in part)]
    stated = f"the readings' past ladder {ladder}, count {count} and parts {parts}"
    if not read:
        cause = f"no single, one-way side lands in every part, of {len(one_way)} single, one-way sides of {len(series)}; {stated}"
        return measure.verdict("NOT READ", cause)
    copies = len({tuple(sorted(series[side].items())) for side in shown})
    side = (shown or list(read))[0]
    cause = f"{len(shown)} of {len(read)} single, one-way sides read reach the count in every part and at every length, {copies} distinct series among them; the first (site, train, the other's site and train) {side}: {read[side]} per part; {stated}"
    return measure.verdict("SHOWN" if shown else "NOT SHOWN", cause, shown=len(shown), read=len(read))


def q_lines(record: Record, swap: dict[int, int]) -> list[tuple[Any, ...]]:
    """A record's click lines on their q's alone, each train named through the swap, in the schema's order (round, site, train), each line's sides by their place and train: the teeth, board fields, left out."""
    return sorted(
        (
            line["round"],
            line["site"],
            swap.get(line["train"], line["train"]),
            line["q"],
            tuple(sorted((at, swap.get(u, u), q) for at, u, q, _, _ in edged(line))),
        )
        for line in clicks.listed(record)
    )


def compared(first: Record, second: Record, swap: dict[int, int], same: bool) -> Verdict:
    """Two records' click lines on their q's alone, line for line in the schema's order, the second's trains named through the swap: SHOWN where they are alike throughout and same is true, or where a line stands apart and same is false, the first round apart named, else NOT SHOWN, and it is NOT READ where a line lacks its q or train; NO CLICK where the first record holds no click line."""
    if not clicks.listed(first):
        return measure.verdict(ABSENT, NO_LINE)
    causes = [
        lacking(clicks.listed(record), ("q", "train"), "the check is")[1] for record in (first, second)
    ]
    if any(causes):
        return measure.verdict("NOT READ", [cause for cause in causes if cause][0])
    a, b = q_lines(first, {}), q_lines(second, swap)
    pairs = list(zip(a, b, strict=False))  # the longer record's tail stands apart
    parted = [x[0] if x <= y else y[0] for x, y in pairs if x != y] + [
        line[0] for line in a[len(pairs) :] + b[len(pairs) :]
    ]
    alike = len([x for x, y in pairs if x == y])
    where = f"apart first at round {parted[0]}" if parted else "none apart"
    cause = f"{alike} of {len(a)} lines alike on their q's alone, the second record's {len(b)}, {where}"
    return measure.verdict(
        "SHOWN" if (not parted) == same else "NOT SHOWN", cause, alike=alike, apart=parted[:1]
    )


def swapped(first: Record, second: Record, trains: list[int]) -> Verdict:
    """The swap (3e), a check on two records (the Boss's ruling: one world's counts are relabelling-covariant; the mathematician's MINOR 5): the second record from the lay with the named trains exchanged in the files, its clocks named back, the named trains in their order taken to the reverse of that order, which reverses the swapped edges' orientation by itself; SHOWN where the two are alike line for line in the schema's order, on their q's alone; NOT SHOWN naming the first round apart; NOT READ where no trains are named."""
    if not trains:
        return measure.verdict("NOT READ", "no trains are named as the swap's")
    return compared(first, second, dict(zip(trains, reversed(trains), strict=True)), True)


def twice(first: Record, second: Record) -> Verdict:
    """R1 (3g), a check on two records: one lay run twice gives one record, SHOWN where the two are alike line for line in the schema's order on their q's alone, NOT SHOWN naming the first round apart."""
    return compared(first, second, {}, True)


def apart(first: Record, second: Record) -> Verdict:
    """R2's two-record form (3f), a check on two records (the physicist's B1): two lays one hidden unit apart, alike line for line on their q's alone up to a round and apart from it, SHOWN where a line stands apart, the round named; NOT SHOWN where none does, a carried record its no."""
    return compared(first, second, {}, False)


def readings(record: Record, held: Any) -> dict[str, Verdict]:
    """The three clicks' readings and the check against the board's passing on one record, each its verdict, NO CLICK in each on a record that holds no click line."""
    return {
        STRUCTURE: structure(record),
        LANDS: lands(record),
        WITHIN: within(record, held),
        PASSING: passing(record),
    }
