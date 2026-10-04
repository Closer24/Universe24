"""Bell's gate and the GHZ gate, the joint-share reader (ALGEBRA.md #the-click-is-the-meeting, the pair's form and the GHZ gate; HIGHLIGHTS.md, One experiment and one gate: Bell is the engine's gate and no experiment). Four worlds, one per combination of settings, each with one record of several parts laid equal (the pair family's two, the GHZ family's four), one beam to each side and one declared region per side whose `basis` (p, q) is the side's setting and whose `pattern`, one integer pair [alpha_k, beta_k] per part, says how each part reads it; the engine reports per interval the parts' signed level sums at each region (the `parts` lines, the NodeReader's read). The reader pairs each part with the same part through the root across every side: with e_k(+) = alpha_k p + beta_k q and e_k(-) = alpha_k (-q) + beta_k p the ports of a side and c_k the product over the sides of e_k at their ports, the joint share of one combination of ports is accumulated over the window on both members of the level pair, J = SUM over the window of (SUM_k c_k PROD_sides now_k)^2 + (SUM_k c_k PROD_sides before_k)^2 (the advisor, #1563 comment 5924731760; the mathematician, #1572 comments 5925374010 and 5927559738), a sum of squares and never negative, so no floor is needed; E_n is the sum of the shares signed by the product of the ports' signs over their sum (for two sides E(a, b) = (J_++ + J_-- - J_+- - J_-+) over the four), a side's marginal P(+) its + shares over the sum, a sub-correlation over a subset of the sides the same signed by that subset alone; the four worlds' E combined with the expectation's signs, S = E(a, b) - E(a, b') + E(a', b) + E(a', b') for two sides (CHSH) and M = E(a, b', c') + E(a', b, c') + E(a', b', c) - E(a, b, c) for three (Mermin); every combination of ports credited (the efficiency 1 by the draw's construction); the combination realised per world is the reader's own draw inside the run, read from the output's `credit` lines (the click written on the lattice, `src/event_universe/credit.py`; None for a world declaring no draw), the reader drawing nothing; every number an exact fraction. At equal parts the pair gives E = ((p p' + q q')^2 - (p q' - q p')^2) / ((p^2 + q^2) (p'^2 + q'^2)), Lagrange's identity, S = 478 / 169 at (1, 0), (1, 1), (12, 5), (5, 12); the GHZ patterns give the shares cos^2(a + b + c) / 4 at an even number of - ports and sin^2(a + b + c) / 4 at an odd, E_3 = cos 2(a + b + c), M = -4 at x = (1, 0) and y = (1, 1). Beside it, from the same reports, the local credits as the fence: by the parts' shares (each part's share credited alone, no sum before the square; S = 238 / 169, M = -1), by the local sums (the product of the sides' own squared sums; S = 240 / 169, M = -1) and by the sign (each side's larger port, 0 at a tie; S = 2, M = -1), every one a product form, S at most 2 and |M| at most 2; and the diagnostics `mismatch` (the parts' accumulated cross-side products M_k, their ratios M_k / M_1 and the pair's rho = 2 M_1 M_2 / (M_1^2 + M_2^2), the mismatch's one number, E = cos 2a cos 2b + rho sin 2a sin 2b for the pair, the mathematician, #1572 comment 5925175652), LATTICE, never in the blind and never in the credit. The settings, the patterns, the window, the regions, the seed and the combination's signs are the files'; the tool holds no number; the builders derive the blind by the same algebra on equal parts (`at_equal_parts`).

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/bell_gate.py --expectation examples/events/bell/expectation.json --outputs runs/bell/*.output.json
    PYTHONPATH=src python tools/bell_gate.py --expectation examples/events/ghz/expectation.json --outputs runs/ghz/*.output.json
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from fractions import Fraction
from itertools import combinations, product
from math import prod
from pathlib import Path
from typing import Any

from event_universe.loader.derived import count_wall
from event_universe.loader.draw import ports_of as loader_ports
from event_universe.reports import PORT_NAMES as PORTS  # a side's two ports: at (p, q) and at (-q, p)
from event_universe.world_files import load_world

Levels = dict[int, list[list[int]]]  # per interval, per part [now, before] at a region
Ports = dict[str, tuple[int, ...]]  # a side's two ports, each one coefficient per part
Key = tuple[str, ...]  # one port per side
Joint = dict[Key, Fraction]  # per combination of ports a share
Pattern = tuple[tuple[int, int], ...]  # per part [alpha_k, beta_k], as the loader reads it


def pair(value: Fraction | None) -> list[int] | None:
    """A fraction as [numerator, denominator] for the file; None where nothing was credited."""
    return None if value is None else [value.numerator, value.denominator]


def fraction(value: object) -> Fraction | None:
    """A file's [numerator, denominator] or whole number as a fraction; None where nothing was credited."""
    if value is None:
        return None
    return Fraction(*value) if isinstance(value, list) else Fraction(int(str(value)))


def ports_of(basis: tuple[int, ...], pattern: Pattern) -> Ports:
    """A side's two ports from its declared setting and its parts' pattern, the loader's own (`loader/draw.py`, `ports_of`: e_k(+) = alpha_k p + beta_k q and e_k(-) = alpha_k (-q) + beta_k p, refused by name where not orthogonal with equal norms), keyed by the ports' names."""
    plus, minus = loader_ports(basis, pattern)
    return {PORTS[0]: plus, PORTS[1]: minus}


def reports(
    lines: list[dict[str, object]], family: str, node_reader: str, window: tuple[int, int]
) -> Levels:
    """The `parts` lines of one region and family within the window, per interval the parts' [now, before] sums (an interval with no line reported nothing but zeros)."""
    found: Levels = {}
    for line in lines:
        if line.get("event") != "parts" or line.get("family") != family:
            continue
        if (
            line.get("node_reader") == node_reader
            and window[0] <= int(str(line["interval"])) <= window[1]
        ):
            levels = line["levels"]
            assert isinstance(levels, list)
            found[int(str(line["interval"]))] = [[int(v) for v in part] for part in levels]
    return found


def at(levels: Levels, interval: int, parts: int) -> list[list[int]]:
    """A region's parts at one interval, zeros where nothing was reported."""
    return levels.get(interval, [[0, 0]] * parts)


def intervals_of(*sides: Levels) -> list[int]:
    """Every interval at which a side reported, sorted."""
    return sorted({interval for side in sides for interval in side})


def keys_of(sides: int) -> list[Key]:
    """Every combination of ports over the sides, 2^n keys, one port per side, the + port first."""
    return list(product(PORTS, repeat=sides))


def credited(sides: list[Levels], ports: list[Ports], joined: bool) -> Joint:
    """The shares of every combination of ports accumulated over the window on both members of the level pair: per interval and member the parts' terms, each the product over the sides of e_k(port) times the part's sum there, summed over the parts and then squared where `joined` (the meeting: the parts paired by their label through the root across every side, then summed, then squared), or each squared alone (the local credit by the parts' shares)."""
    parts = len(ports[0][PORTS[0]])
    found = {key: Fraction(0) for key in keys_of(len(sides))}
    for interval in intervals_of(*sides):
        levels = [at(side, interval, parts) for side in sides]
        for key in found:
            for member in range(2):
                terms = [
                    prod(
                        e[port][k] * now[k][member]
                        for e, port, now in zip(ports, key, levels, strict=True)
                    )
                    for k in range(parts)
                ]
                found[key] += sum(terms) ** 2 if joined else sum(term * term for term in terms)
    return found


def joint(sides: list[Levels], ports: list[Ports]) -> Joint:
    """The meeting's joint shares: J = SUM over the window of (SUM_k c_k PROD_sides now_k)^2 + (SUM_k c_k PROD_sides before_k)^2, c_k the product over the sides of e_k at their ports."""
    return credited(sides, ports, True)


def parts_shares(sides: list[Levels], ports: list[Ports]) -> Joint:
    """The local credit by the parts' shares: each part's share credited alone, the squares summed over the parts and never the amplitudes (rho = 0, E = cos 2a cos 2b for the pair; S = 238 / 169 and M = -1 at the gates' settings)."""
    return credited(sides, ports, False)


def side_sums(levels: Levels, ports: Ports) -> dict[str, Fraction]:
    """A side's local shares per port, the square of its own sum over the parts accumulated over the window on both members: what one node_reader could read alone."""
    parts = len(ports[PORTS[0]])
    found = {port: Fraction(0) for port in PORTS}
    for interval in intervals_of(levels):
        here = at(levels, interval, parts)
        for port in PORTS:
            for member in range(2):
                total = sum(ports[port][k] * here[k][member] for k in range(parts))
                found[port] += total * total
    return found


def local_sums(sides: list[Levels], ports: list[Ports]) -> Joint:
    """The local credit by the local sums: the product over the sides of each side's own share at its port, a product form (E = sin 2a sin 2b for the pair; S = 240 / 169 and M = -1 at the gates' settings)."""
    own = [side_sums(side, e) for side, e in zip(sides, ports, strict=True)]
    return {
        key: prod((shares[port] for shares, port in zip(own, key, strict=True)), start=Fraction(1))
        for key in keys_of(len(sides))
    }


def sign_of(shares: dict[str, Fraction]) -> int:
    """A side's outcome by the sign alone: +1 where its + port's share is the larger, -1 where the - port's is, 0 at a tie."""
    return (shares[PORTS[0]] > shares[PORTS[1]]) - (shares[PORTS[0]] < shares[PORTS[1]])


def by_the_sign(sides: list[Levels], ports: list[Ports]) -> Fraction:
    """The local credit by the sign: the product over the sides of each side's larger port, +1 or -1, 0 where a side ties (S = 2 and M = -1 at the gates' settings)."""
    return Fraction(prod(sign_of(side_sums(side, e)) for side, e in zip(sides, ports, strict=True)))


def signed(key: Key, chosen: Iterable[int]) -> int:
    """The product of the port signs of the sides chosen, +1 for the + port and -1 for the - port."""
    return prod(1 if key[i] == PORTS[0] else -1 for i in chosen)


def correlation(shares: Joint, chosen: Iterable[int] | None = None) -> Fraction | None:
    """E over the sides chosen by their indexes (every side where None): the shares signed by the product of those sides' port signs over their sum, the other sides summed over; for two sides (J_++ + J_-- - J_+- - J_-+) over the four, for n sides E_n by the product of the n signs, for a subset a sub-correlation; None where nothing was credited."""
    total = sum(shares.values(), Fraction(0))
    if not total:
        return None
    sides = tuple(range(len(next(iter(shares))))) if chosen is None else tuple(chosen)
    return sum((signed(key, sides) * value for key, value in shares.items()), Fraction(0)) / total


def marginal(shares: Joint, side: int = 0) -> Fraction | None:
    """A side's marginal, the shares of its + port over the sum of all; None where nothing was credited."""
    total = sum(shares.values(), Fraction(0))
    if not total:
        return None
    return sum((value for key, value in shares.items() if key[side] == PORTS[0]), Fraction(0)) / total


def credits_of(sides: list[Levels], ports: list[Ports]) -> dict[str, Any]:
    """The reader's numbers from the sides' reports: the 2^n joint shares of the meeting, E_n, each side's marginal, every sub-correlation over two or more sides below n (keyed by the sides' indexes) and the three local credits' E, exact fractions."""
    shares, count = joint(sides, ports), len(ports)
    subsets = [chosen for size in range(2, count) for chosen in combinations(range(count), size)]
    return {
        "shares": shares,
        "correlation": correlation(shares),
        "marginals": [marginal(shares, side) for side in range(count)],
        "sub_correlations": {chosen: correlation(shares, chosen) for chosen in subsets},
        "by_the_parts_shares": correlation(parts_shares(sides, ports)),
        "by_the_local_sums": correlation(local_sums(sides, ports)),
        "by_the_sign": by_the_sign(sides, ports),
    }


def at_equal_parts(ports: list[Ports]) -> dict[str, Any]:
    """The reader's numbers at equal parts, the blind's (the builders' call, before any run): every part of every side reading [1, 0] at one interval, so every ratio is the ports' alone, the parts' common factor cancelling."""
    parts = len(ports[0][PORTS[0]])
    return credits_of([{1: [[1, 0]] * parts} for _ in ports], ports)


def written(credits: dict[str, Any], labels: list[str]) -> dict[str, Any]:
    """The reader's numbers as the file writes them: every fraction [numerator, denominator], the joint shares J keyed by the ports' names in the sides' order (`joint`, as accumulated) and over their sum (`shares`, the probabilities of the combinations), the marginals and the sub-correlations by the sides' labels."""
    joint_shares, subsets = credits["shares"], credits["sub_correlations"]
    total = sum(joint_shares.values(), Fraction(0))
    return {
        "joint": {" ".join(key): pair(value) for key, value in joint_shares.items()},
        "shares": {
            " ".join(key): pair(value / total) if total else None for key, value in joint_shares.items()
        },
        "correlation": pair(credits["correlation"]),
        "marginals": dict(zip(labels, map(pair, credits["marginals"]), strict=True)),
        "sub_correlations": {
            " ".join(labels[i] for i in chosen): pair(e) for chosen, e in subsets.items()
        },
        "by_the_parts_shares": pair(credits["by_the_parts_shares"]),
        "by_the_local_sums": pair(credits["by_the_local_sums"]),
        "by_the_sign": pair(credits["by_the_sign"]),
    }


def mismatch(sides: list[Levels], parts: int) -> dict[str, Any]:
    """The parts' mismatch, LATTICE diagnostics from the same reports: M_k the cross-side products of the part k (the product over the sides of its sums) accumulated over the window on both members, the ratios M_k / M_1 of the parts after the first (1 at equal parts; the pair's r), the pair's rho = 2 M_1 M_2 / (M_1^2 + M_2^2) from the first two parts (S = (238 + 240 rho) / 169 at Bell's settings), and per side the parts' squares' ratios to the first part's; None where a divisor is 0."""
    products = [Fraction(0)] * parts
    squares = [[Fraction(0)] * parts for _ in sides]
    for interval in intervals_of(*sides):
        levels = [at(side, interval, parts) for side in sides]
        for k in range(parts):
            for member in range(2):
                products[k] += prod(now[k][member] for now in levels)
                for own, now in zip(squares, levels, strict=True):
                    own[k] += now[k][member] * now[k][member]
    first, second = products[0], products[1]
    norm = first * first + second * second
    return {
        "label": "LATTICE",
        "products": [pair(value) for value in products],
        "ratios": [pair(value / first) if first else None for value in products[1:]],
        "rho": pair(2 * first * second / norm) if norm else None,
        "squares_ratios": [[pair(v / own[0]) if own[0] else None for v in own[1:]] for own in squares],
    }


def realised(
    lines: list[dict[str, object]], family: str, node_readers: list[str], window: tuple[int, int]
) -> list[str] | None:
    """The combination of ports the draw realised in the run, one port per side from the output's `credit` lines of the family at the sides' regions within the window (the last of a window per side), the click; None where a side has none (a world declaring no draw)."""
    found: dict[str, str] = {}
    for line in lines:
        if line.get("event") != "credit" or line.get("family") != family:
            continue
        if (
            line.get("node_reader") in node_readers
            and window[0] <= int(str(line["interval"])) <= window[1]
        ):
            found[str(line["node_reader"])] = str(line["realised"])
    return (
        [found[name] for name in node_readers] if all(name in found for name in node_readers) else None
    )


def inflow_of(
    lines: list[dict[str, object]], family: str, node_reader: str, window: tuple[int, int]
) -> int:
    """A region's `click` lines' inflows of one family summed over the window, in the current's units."""
    return sum(
        int(str(line["inflow"]))
        for line in lines
        if line.get("event") == "click"
        and line.get("family") == family
        and line.get("node_reader") == node_reader
        and window[0] <= int(str(line["interval"])) <= window[1]
    )


def one_world(world: Path, lines: list[dict[str, object]], expected: dict[str, Any]) -> dict[str, Any]:
    """One world's reading: its sides' declared settings and patterns, the 2^n joint shares, E_n, each side's marginal and every sub-correlation, the three local credits, the combination the draw realised in the run (`drawn`, from the credit lines), the mismatch and each side's inflow in quanta over the window; a pattern of other than the family's parts is refused by name."""
    loaded = load_world(world)
    family = next(f for f in loaded.families if f.name == expected["family"])
    window = (int(expected["window"][0]), int(expected["window"][1]))
    labels = list(expected["sides"])
    rows = [
        next(d for d in loaded.node_readers if d.name == expected["sides"][label]) for label in labels
    ]
    for row in rows:
        if len(row.pattern) != family.parts:
            raise ValueError(
                f"node_reader {row.name!r} declares a pattern of {len(row.pattern)} parts, and the family "
                f"{family.name!r} has {family.parts}"
            )
    ports = [ports_of(row.basis, row.pattern) for row in rows]
    sides = [reports(lines, family.name, row.name, window) for row in rows]
    wall = count_wall(family, loaded.quantum_action)
    return {
        "world": world.name,
        "bases": {label: list(row.basis) for label, row in zip(labels, rows, strict=True)},
        "patterns": {
            label: [list(part) for part in row.pattern] for label, row in zip(labels, rows, strict=True)
        },
        "intervals_reported": len(intervals_of(*sides)),
        **written(credits_of(sides, ports), labels),
        "drawn": realised(lines, family.name, [row.name for row in rows], window),
        "mismatch": mismatch(sides, family.parts),
        "quanta": {
            label: [inflow_of(lines, family.name, row.name, window), wall]
            for label, row in zip(labels, rows, strict=True)
        },
    }


def combination(values: Iterable[Fraction | None], signs: Iterable[int]) -> Fraction | None:
    """The four worlds' E combined with the expectation's signs in its order: S = E(a, b) - E(a, b') + E(a', b) + E(a', b') for two sides (the signs 1, -1, 1, 1), M = E(a, b', c') + E(a', b, c') + E(a', b', c) - E(a, b, c) for three (1, 1, 1, -1); None where a world credited nothing."""
    found = list(values)
    if any(value is None for value in found):
        return None
    return sum((sign * value for sign, value in zip(signs, found, strict=True)), Fraction(0))


def blind_of(
    worlds: dict[str, list[Ports]], labels: list[str], name: str, signs: list[int]
) -> dict[str, Any]:
    """The blind's numbers from the settings alone, the builders' call before any run: per combination of settings (keyed in the expectation's order) the reader's numbers at equal parts, and the combination `name` (S or M) of the four E by the meeting and by each local credit with the signs given; the statuses are the builder's."""
    numbers = {key: written(at_equal_parts(ports), labels) for key, ports in worlds.items()}

    def combined(field: str) -> list[int] | None:
        return pair(combination((fraction(numbers[key][field]) for key in worlds), signs))

    found: dict[str, Any] = {
        field: {key: numbers[key][field] for key in worlds}
        for field in ("correlation", "marginals", "sub_correlations", "shares", "joint")
    }
    found[name] = combined("correlation")
    for field in ("by_the_parts_shares", "by_the_local_sums", "by_the_sign"):
        found[field] = {
            "correlation": {key: numbers[key][field] for key in worlds},
            name: combined(field),
        }
    return found


def reading(expectation: Path, outputs: list[Path]) -> dict[str, object]:
    """The reading of the four worlds against the expectation: per world the shares, E_n, the marginals, the sub-correlations, the local credits, the combination realised in the run and the mismatch; the combination (S or M, named by the expectation with its signs) by the meeting and by each local credit; the blind row copied from the expectation."""
    expected = json.loads(expectation.read_text(encoding="utf-8"))
    worlds: dict[str, dict[str, Any]] = {}
    for path in outputs:
        output = json.loads(path.read_text(encoding="utf-8"))
        name = Path(str(output["input"])).stem
        worlds[name] = one_world(expectation.with_name(f"{name}.json"), output["lines"], expected)
    ordered = [worlds[str(expected["runs"][key])] for key in expected["order"]]
    label, signs = (
        str(expected["combination"]["name"]),
        [int(s) for s in expected["combination"]["signs"]],
    )

    def combined(field: str) -> list[int] | None:
        return pair(combination((fraction(world[field]) for world in ordered), signs))

    return {
        "verdict": "NODEREADER",
        "rule": expected["rule"],
        "worlds": {name: worlds[name] for name in sorted(worlds)},
        "correlation": {
            key: world["correlation"] for key, world in zip(expected["order"], ordered, strict=True)
        },
        label: combined("correlation"),
        "marginals": {
            key: world["marginals"] for key, world in zip(expected["order"], ordered, strict=True)
        },
        "sub_correlations": {
            key: world["sub_correlations"] for key, world in zip(expected["order"], ordered, strict=True)
        },
        f"{label}_by_the_parts_shares": combined("by_the_parts_shares"),
        f"{label}_by_the_local_sums": combined("by_the_local_sums"),
        f"{label}_by_the_sign": combined("by_the_sign"),
        "blind": expected["blind"],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--expectation", type=Path, required=True, help="the blind expectation file")
    parser.add_argument("--outputs", type=Path, nargs="+", required=True, help="the four output files")
    args = parser.parse_args(argv)
    print(json.dumps(reading(args.expectation, args.outputs), indent=1))


if __name__ == "__main__":
    main()
