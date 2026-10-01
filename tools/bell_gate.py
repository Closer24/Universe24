"""Bell's gate, the joint-share reader (ALGEBRA.md #the-click-is-the-meeting, the pair's form; HIGHLIGHTS.md, One experiment and one gate: Bell is the engine's gate and no experiment). Four worlds, one per pair of settings, each with the pair family's two parts laid equal, one beam to each side and one declared region per side whose `basis` (p, q) is the side's setting; the engine reports per interval the parts' signed level sums at each region (the `parts` lines, the instrument's read). The reader pairs each part with the same part through the root: with e(+) = (p, q) and e(-) = (-q, p) the ports of a side and c_k = e_k(p_A) e_k(p_B) for a pair of ports, the joint share is accumulated over the window on both members of the level pair, J(p_A, p_B) = SUM over the window of (SUM_k c_k now_k^A now_k^B)^2 + (SUM_k c_k before_k^A before_k^B)^2 (the advisor, #1563 comment 5924731760; the mathematician's confirmation, #1572 comment 5925374010), a sum of squares and never negative, so no floor is needed; E(a, b) = (J_++ + J_-- - J_+- - J_-+) over the four summed, the marginal P(A+) = (J_++ + J_+-) over the four, S = E(a, b) - E(a, b') + E(a', b) + E(a', b'), every pair credited (the efficiency 1 by the draw's construction), one pair drawn per world by the shares with the declared seed (the click); every number an exact fraction. At equal parts E = ((p p' + q q')^2 - (p q' - q p')^2) / ((p^2 + q^2) (p'^2 + q'^2)) exactly, Lagrange's identity, 478 / 169 at (1, 0), (1, 1), (12, 5), (5, 12). Beside it, from the same reports, the local credits as the fence: by the parts' shares (each part's share credited alone, no sum before the square; 238 / 169), by the local sums (the square of each side's own sum; 240 / 169) and by the sign (each side's larger port, 0 at a tie; 2); and the diagnostics r (the parts' accumulated cross-side products' ratio M_2 / M_1) and rho = 2 M_1 M_2 / (M_1^2 + M_2^2), the mismatch's one number (E = cos 2a cos 2b + rho sin 2a sin 2b, the mathematician, #1572 comment 5925175652), GAMEBOARD, never in the blind and never in the credit. The settings, the window, the regions and the seed are the files'; the tool holds no number.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/bell_gate.py --expectation examples/events/bell/expectation.json --outputs runs/bell/*.output.json
"""

from __future__ import annotations

import argparse
import json
import random
from collections.abc import Iterable
from fractions import Fraction
from pathlib import Path
from typing import Any

from event_universe.loader.derived import count_wall
from event_universe.world_files import load_world

PORTS = ("plus", "minus")  # a side's two ports, e(+) = (p, q) and e(-) = (-q, p)
Levels = dict[int, list[list[int]]]  # per interval, per part [now, before] at a region
Joint = dict[tuple[str, str], Fraction]  # per pair of ports (A's, B's) a share


def pair(value: Fraction | None) -> list[int] | None:
    """A fraction as [numerator, denominator] for the file; None where nothing was credited."""
    return None if value is None else [value.numerator, value.denominator]


def ports_of(basis: tuple[int, ...]) -> dict[str, tuple[int, ...]]:
    """A side's two ports from its declared basis (p, q): e(+) = (p, q) and e(-) = (-q, p), orthogonal with equal norms; a basis of other than two coefficients is refused by name (the pair has two parts)."""
    if len(basis) != 2:
        raise ValueError(f"a side's basis is a pair (p, q) for the pair family's two parts, got {basis}")
    p, q = basis
    return {PORTS[0]: (p, q), PORTS[1]: (-q, p)}


def reports(
    lines: list[dict[str, object]], family: str, detector: str, window: tuple[int, int]
) -> Levels:
    """The `parts` lines of one region and family within the window, per interval the parts' [now, before] sums (an interval with no line reported nothing but zeros)."""
    found: Levels = {}
    for line in lines:
        if line.get("event") != "parts" or line.get("family") != family:
            continue
        if line.get("detector") == detector and window[0] <= int(str(line["tick"])) <= window[1]:
            levels = line["levels"]
            assert isinstance(levels, list)
            found[int(str(line["tick"]))] = [[int(v) for v in part] for part in levels]
    return found


def at(levels: Levels, tick: int, parts: int) -> list[list[int]]:
    """A region's parts at one interval, zeros where nothing was reported."""
    return levels.get(tick, [[0, 0]] * parts)


def ticks_of(*sides: Levels) -> list[int]:
    """Every interval at which a side reported, sorted."""
    return sorted({tick for side in sides for tick in side})


def joint(
    a: Levels, b: Levels, e_a: dict[str, tuple[int, ...]], e_b: dict[str, tuple[int, ...]]
) -> Joint:
    """The joint shares of the four pairs of ports, accumulated over the window on both members of the level pair: per interval the cross-side sum over the parts of c_k a_k b_k, c_k = e_k(p_A) e_k(p_B), squared (the meeting's form: the parts paired by their label through the root, then summed, then squared)."""
    parts = len(next(iter(e_a.values())))
    found: Joint = {(x, y): Fraction(0) for x in PORTS for y in PORTS}
    for tick in ticks_of(a, b):
        here, there = at(a, tick, parts), at(b, tick, parts)
        for x in PORTS:
            for y in PORTS:
                for member in range(2):
                    amplitude = sum(
                        e_a[x][k] * e_b[y][k] * here[k][member] * there[k][member] for k in range(parts)
                    )
                    found[(x, y)] += amplitude * amplitude
    return found


def parts_shares(
    a: Levels, b: Levels, e_a: dict[str, tuple[int, ...]], e_b: dict[str, tuple[int, ...]]
) -> Joint:
    """The local credit by the parts' shares: each part's share credited alone, the squares summed over the parts and never the amplitudes (rho = 0, E = cos 2a cos 2b; 238 / 169 at the four settings)."""
    parts = len(next(iter(e_a.values())))
    found: Joint = {(x, y): Fraction(0) for x in PORTS for y in PORTS}
    for tick in ticks_of(a, b):
        here, there = at(a, tick, parts), at(b, tick, parts)
        for x in PORTS:
            for y in PORTS:
                for k in range(parts):
                    for member in range(2):
                        term = e_a[x][k] * e_b[y][k] * here[k][member] * there[k][member]
                        found[(x, y)] += term * term
    return found


def side_sums(levels: Levels, ports: dict[str, tuple[int, ...]]) -> dict[str, Fraction]:
    """A side's local shares per port, the square of its own sum over the parts accumulated over the window on both members: what one detector could read alone."""
    parts = len(next(iter(ports.values())))
    found = {port: Fraction(0) for port in PORTS}
    for tick in ticks_of(levels):
        here = at(levels, tick, parts)
        for port in PORTS:
            for member in range(2):
                total = sum(ports[port][k] * here[k][member] for k in range(parts))
                found[port] += total * total
    return found


def local_sums(
    a: Levels, b: Levels, e_a: dict[str, tuple[int, ...]], e_b: dict[str, tuple[int, ...]]
) -> Joint:
    """The local credit by the local sums: the product of the two sides' own shares per port (E = sin 2a sin 2b, a product form; 240 / 169 at the four settings)."""
    here, there = side_sums(a, e_a), side_sums(b, e_b)
    return {(x, y): here[x] * there[y] for x in PORTS for y in PORTS}


def sign_of(shares: dict[str, Fraction]) -> int:
    """A side's outcome by the sign alone: +1 where its + port's share is the larger, -1 where the - port's is, 0 at a tie."""
    return (shares[PORTS[0]] > shares[PORTS[1]]) - (shares[PORTS[0]] < shares[PORTS[1]])


def correlation(shares: Joint) -> Fraction | None:
    """E from four shares, (++ and -- less +- and -+) over their sum; None where nothing was credited (every share 0)."""
    total = sum(shares.values(), Fraction(0))
    if not total:
        return None
    signed = sum((1 if x == y else -1) * value for (x, y), value in shares.items())
    return signed / total


def marginal(shares: Joint) -> Fraction | None:
    """A's marginal, the shares of its + port over the four; None where nothing was credited."""
    total = sum(shares.values(), Fraction(0))
    return None if not total else (shares[(PORTS[0], PORTS[0])] + shares[(PORTS[0], PORTS[1])]) / total


def mismatch(a: Levels, b: Levels, parts: int) -> dict[str, Any]:
    """The parts' mismatch, GAMEBOARD diagnostics from the same reports: M_k the cross-side products of the part k accumulated over the window on both members, r = M_2 / M_1 and rho = 2 M_1 M_2 / (M_1^2 + M_2^2) (1 and 1 for equal parts; S = (238 + 240 rho) / 169 at the four settings), and per side the parts' squares' ratio; None where a divisor is 0."""
    products = [Fraction(0)] * parts
    squares = {"a": [Fraction(0)] * parts, "b": [Fraction(0)] * parts}
    for tick in ticks_of(a, b):
        here, there = at(a, tick, parts), at(b, tick, parts)
        for k in range(parts):
            for member in range(2):
                products[k] += here[k][member] * there[k][member]
                squares["a"][k] += here[k][member] * here[k][member]
                squares["b"][k] += there[k][member] * there[k][member]
    first, second = products[0], products[1]
    norm = first * first + second * second
    return {
        "label": "GAMEBOARD",
        "products": [pair(value) for value in products],
        "r": pair(second / first) if first else None,
        "rho": pair(2 * first * second / norm) if norm else None,
        "squares_ratio": {
            side: pair(values[1] / values[0]) if values[0] else None for side, values in squares.items()
        },
    }


def drawn(shares: Joint, seed: int) -> list[str] | None:
    """One pair of ports drawn by the joint shares with the declared seed, the click of the world: the instrument's draw and no line of the law; None where nothing was credited."""
    keys = sorted(shares)
    weights = [shares[key] for key in keys]
    if not sum(weights):
        return None
    scale = 1
    for weight in weights:
        scale *= weight.denominator
    whole = [int(weight * scale) for weight in weights]
    return list(random.Random(seed).choices(keys, weights=whole, k=1)[0])


def one_world(world: Path, lines: list[dict[str, object]], expected: dict[str, Any]) -> dict[str, Any]:
    """One world's reading: its two sides' declared bases and ports, the joint shares, E and the marginal, the three local credits, the drawn pair, the mismatch and each side's inflow in quanta over the window."""
    loaded = load_world(world)
    family = next(f for f in loaded.families if f.name == expected["family"])
    window = (int(expected["window"][0]), int(expected["window"][1]))
    sides = {}
    for side, name in expected["sides"].items():
        row = next(d for d in loaded.detectors if d.name == name)
        sides[side] = (ports_of(row.basis), reports(lines, family.name, name, window), row.basis)
    (e_a, a, basis_a), (e_b, b, basis_b) = sides["a"], sides["b"]
    shares = joint(a, b, e_a, e_b)
    by_shares, by_sums = parts_shares(a, b, e_a, e_b), local_sums(a, b, e_a, e_b)
    outcome = sign_of(side_sums(a, e_a)) * sign_of(side_sums(b, e_b))
    wall = count_wall(family, loaded.quantum_action)
    seen = {
        side: sum(
            int(str(line["inflow"]))
            for line in lines
            if line.get("event") == "click"
            and line.get("family") == family.name
            and line.get("detector") == expected["sides"][side]
            and window[0] <= int(str(line["tick"])) <= window[1]
        )
        for side in expected["sides"]
    }
    return {
        "world": world.name,
        "bases": {"a": list(basis_a), "b": list(basis_b)},
        "intervals_reported": len(ticks_of(a, b)),
        "shares": {f"{x} {y}": pair(value) for (x, y), value in shares.items()},
        "correlation": pair(correlation(shares)),
        "marginal": pair(marginal(shares)),
        "drawn": drawn(shares, int(expected["seed"])),
        "by_the_parts_shares": pair(correlation(by_shares)),
        "by_the_local_sums": pair(correlation(by_sums)),
        "by_the_sign": outcome,
        "mismatch": mismatch(a, b, family.parts),
        "quanta": {side: [value, wall] for side, value in seen.items()},
    }


def chsh(values: Iterable[Fraction | None]) -> Fraction | None:
    """S = E(a, b) - E(a, b') + E(a', b) + E(a', b') from the four worlds' E in the expectation's order; None where a world credited nothing."""
    found = list(values)
    if any(value is None for value in found):
        return None
    first, second, third, fourth = found
    assert first is not None and second is not None and third is not None and fourth is not None
    return first - second + third + fourth


def reading(expectation: Path, outputs: list[Path]) -> dict[str, object]:
    """The reading of the four worlds against the expectation: per world the shares, E, the marginal, the local credits, the drawn pair and the mismatch; S by the meeting and by each local credit; the blind row copied from the expectation."""
    expected = json.loads(expectation.read_text(encoding="utf-8"))
    worlds: dict[str, dict[str, Any]] = {}
    for path in outputs:
        output = json.loads(path.read_text(encoding="utf-8"))
        name = Path(str(output["input"])).stem
        worlds[name] = one_world(expectation.with_name(f"{name}.json"), output["lines"], expected)
    ordered = [worlds[str(expected["runs"][key])] for key in expected["order"]]
    return {
        "verdict": "DETECTOR",
        "rule": expected["rule"],
        "worlds": {name: worlds[name] for name in sorted(worlds)},
        "correlation": {key: ordered[i]["correlation"] for i, key in enumerate(expected["order"])},
        "S": pair(chsh(Fraction(*w["correlation"]) if w["correlation"] else None for w in ordered)),
        "marginal": [w["marginal"] for w in ordered],
        "S_by_the_parts_shares": pair(
            chsh(
                Fraction(*w["by_the_parts_shares"]) if w["by_the_parts_shares"] else None
                for w in ordered
            )
        ),
        "S_by_the_local_sums": pair(
            chsh(Fraction(*w["by_the_local_sums"]) if w["by_the_local_sums"] else None for w in ordered)
        ),
        "S_by_the_sign": pair(chsh(Fraction(w["by_the_sign"]) for w in ordered)),
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
