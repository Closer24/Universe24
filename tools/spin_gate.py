"""The joint-share reader for a gate of a record of planes (ALGEBRA.md, Spin, the spin branch of 2026-10-19; tests/test_the_spin.py, the singlet): tools/bell_gate.py's reading in the plane's form, the engine's own (`credit.joined`): a part of a plane family has two lines, re and im, so the `parts` line of a region holds 2 x parts rows, the part k's pair on the rows 2 k and 2 k + 1, and the meeting's share is J = SUM over the window and both members of |SUM_k c_k PROD_sides psi^s_k|^2 with psi^s_k the part's (re, im) sums at the side s, the product over the sides a plane's product and the square the pair's norm; a record of real lines (one line per part) is the same form with im at 0, bell_gate's. The family's declared sign under exchange is read from the loaded world (the key `exchange`, 2026-10-19; ALGEBRA.md, Spin, closed for the paper as a route, The family's sign under exchange): under the antisymmetric sign the meeting's amplitude is SUM over the ordered pairs (k, l), k != l, of sign(l - k) e^L_k(port_L) psi^L_k x e^R_l(port_R) psi^R_l, the plane products as `times` makes them, then the norm, the determinant of the two sides' parts, two sides and more refused by name; the symmetric and the undeclared record the form above; the local credits (by the parts' shares, by the local sums, by the sign) the fences as they stand; `at_equal_parts(ports, exchange)` the blind's numbers in the same form for a folder's builder. A side's setting is read as the loader reads it, `axis` where it declares one (a record of planes: the half-angle pair (c, s)) and `basis` otherwise, the ports' arithmetic one (`loader/draw.ports_of`: e_k(+) = alpha_k c + beta_k s, e_k(-) = alpha_k (-s) + beta_k c). The singlet's two regions, the left's pattern the identity and the right's [[0, 1], [-1, 0]], read E(a, b) = -cos(theta_a - theta_b) exact in the integers' rationals from the engine's `parts` lines: -119 / 169, 119 / 169, -120 / 169 and -120 / 169 at the four Bell settings, S = -478 / 169 with the CHSH signs (|S| = 478 / 169, above 2 and below 2 sqrt 2 by 2.5 x 10^-5), every marginal 1 / 2, the shares of (+, +) and (-, -) 0 at equal axes; beside them the three local credits as the fence, in the same plane form (by the parts' shares, each part's norm alone; by the local sums, the product of the sides' own norms; by the sign, each side's larger port), every one a product form with |S| at most 2; the combination realised per world from the output's `credit` lines, the engine's one draw; the mismatch diagnostics on the real part of the cross-side products, LATTICE and never in the blind. The reader's file is bell_gate's, key for key (`bases` the side's setting as declared), so that tools/look/page.py's gate panels read it unchanged; E, the marginals, the combination and the blind are bell_gate's own functions; the tool holds no number.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/spin_gate.py --expectation examples/events/bell_singlet/expectation.json --outputs runs/singlet/*.output.json
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from itertools import combinations
from math import prod
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bell_gate  # noqa: E402  # the reader's own arithmetic: E, the marginals, the combination, the file's form
from bell_gate import Joint, Levels, Ports  # noqa: E402

from event_universe.loader.derived import count_wall  # noqa: E402
from event_universe.reports import PORT_NAMES as PORTS  # noqa: E402  # a side's two ports
from event_universe.world_files import load_world  # noqa: E402

Pair = tuple[int, int]  # a plane's (re, im)
EXCHANGE_WORDS = {
    -1: "antisymmetric",
    1: "symmetric",
}  # the family's sign under exchange, as the universe file declares it; None undeclared


def amplitude(levels: list[list[int]], k: int, width: int, member: int) -> Pair:
    """The part k's amplitude at one member of the level pair: its (re, im) on the rows k width and k width + 1 for a plane, (re, 0) for a real line."""
    re = levels[k * width][member]
    im = levels[k * width + 1][member] if width == 2 else 0
    return re, im


def times(u: Pair, v: Pair) -> Pair:
    """A plane's product."""
    return u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0]


def norm(u: Pair) -> int:
    """A plane's norm squared."""
    return u[0] * u[0] + u[1] * u[1]


def terms_of(parts: int, sides: int, exchange: int) -> list[tuple[int, tuple[int, ...]]]:
    """The amplitude's terms as (the sign, the part each side reads), the record's sign under exchange, the family's declaration (the engine's `credit.joined`; ALGEBRA.md, Spin, closed for the paper as a route, The family's sign under exchange): SUM_k over the same part k at every side for the symmetric record and a family declaring no sign (`exchange` 1 or 0, the form as it stood); SUM_{k != l} sign(l - k) over the ordered pairs of parts across two sides for the antisymmetric (`exchange` -1), the determinant of the two sides' parts, more than two sides refused by name."""
    if exchange >= 0:
        return [(1, (k,) * sides) for k in range(parts)]
    if sides != 2:
        raise ValueError(
            f"the antisymmetric sign under exchange is read over two sides, and {sides} are declared: the pair's "
            "amplitude is the determinant of two sides' parts"
        )
    return [(1 if k < m else -1, (k, m)) for k in range(parts) for m in range(parts) if k != m]


def credited(
    sides: list[Levels], ports: list[Ports], parts: int, width: int, joined: bool, exchange: int = 0
) -> Joint:
    """The shares of every combination of ports accumulated over the window on both members: per interval and member the amplitude's terms (`terms_of`, by the family's sign under exchange: over the parts for the symmetric or undeclared record, over the ordered pairs of parts with their sign for the antisymmetric), each the product over the sides of e_k(port) times the part's amplitude there, the plane products as `times` makes them, summed and then the norm where `joined` (the meeting), or each norm alone (the local credit by the parts' shares, a fence read over the parts whatever the sign)."""
    found = {key: Fraction(0) for key in bell_gate.keys_of(len(sides))}
    signed = terms_of(parts, len(sides), exchange if joined else 0)
    for interval in bell_gate.intervals_of(*sides):
        levels = [bell_gate.at(side, interval, parts * width) for side in sides]
        for key in found:
            for member in range(2):
                terms = []
                for sign, which in signed:
                    product: Pair = (sign, 0)
                    for e, port, now, k in zip(ports, key, levels, which, strict=True):
                        factor = e[port][k]
                        re, im = amplitude(now, k, width, member)
                        product = times(product, (factor * re, factor * im))
                    terms.append(product)
                if joined:
                    total = (sum(t[0] for t in terms), sum(t[1] for t in terms))
                    found[key] += norm(total)
                else:
                    found[key] += sum(norm(t) for t in terms)
    return found


def side_sums(levels: Levels, ports: Ports, parts: int, width: int) -> dict[str, Fraction]:
    """A side's local shares per port: the norm of its own sum over the parts accumulated over the window on both members, what one node_detector could read alone."""
    found = {port: Fraction(0) for port in PORTS}
    for interval in bell_gate.intervals_of(levels):
        here = bell_gate.at(levels, interval, parts * width)
        for port in PORTS:
            for member in range(2):
                total: Pair = (0, 0)
                for k in range(parts):
                    re, im = amplitude(here, k, width, member)
                    total = (total[0] + ports[port][k] * re, total[1] + ports[port][k] * im)
                found[port] += norm(total)
    return found


def local_sums(sides: list[Levels], ports: list[Ports], parts: int, width: int) -> Joint:
    """The local credit by the local sums: the product over the sides of each side's own share at its port, a product form."""
    own = [side_sums(side, e, parts, width) for side, e in zip(sides, ports, strict=True)]
    return {
        key: prod((shares[port] for shares, port in zip(own, key, strict=True)), start=Fraction(1))
        for key in bell_gate.keys_of(len(sides))
    }


def by_the_sign(sides: list[Levels], ports: list[Ports], parts: int, width: int) -> Fraction:
    """The local credit by the sign: the product over the sides of each side's larger port, +1 or -1, 0 where a side ties."""
    return Fraction(
        prod(
            bell_gate.sign_of(side_sums(side, e, parts, width))
            for side, e in zip(sides, ports, strict=True)
        )
    )


def credits_of(
    sides: list[Levels], ports: list[Ports], parts: int, width: int, exchange: int = 0
) -> dict[str, Any]:
    """The reader's numbers from the sides' reports in the plane's form: the 2^n joint shares of the meeting in the sign's form (`credited` with the family's `exchange`), E_n, each side's marginal, every sub-correlation and the three local credits' E, the fences as they stand whatever the sign, exact fractions (E and the marginals by bell_gate's own functions)."""
    shares, count = credited(sides, ports, parts, width, True, exchange), len(ports)
    subsets = [chosen for size in range(2, count) for chosen in combinations(range(count), size)]
    return {
        "shares": shares,
        "correlation": bell_gate.correlation(shares),
        "marginals": [bell_gate.marginal(shares, side) for side in range(count)],
        "sub_correlations": {chosen: bell_gate.correlation(shares, chosen) for chosen in subsets},
        "by_the_parts_shares": bell_gate.correlation(credited(sides, ports, parts, width, False)),
        "by_the_local_sums": bell_gate.correlation(local_sums(sides, ports, parts, width)),
        "by_the_sign": by_the_sign(sides, ports, parts, width),
    }


def at_equal_parts(ports: list[Ports], exchange: int = 0) -> dict[str, Any]:
    """The reader's numbers at equal parts, the blind's (the builders' call, before any run; bell_gate's `at_equal_parts` in the plane's form with the family's sign under exchange): every part of every side reading (1, 0) at one interval, so every ratio is the ports' alone, the parts' common factor cancelling; under the antisymmetric sign the determinant of the two sides' ports, e^L_0 e^R_1 - e^L_1 e^R_0 at two parts, the crossed pattern's numbers at the plain identity on both sides."""
    parts = len(ports[0][PORTS[0]])
    return credits_of([{1: [[1, 0], [0, 0]] * parts} for _ in ports], ports, parts, 2, exchange)


def mismatch(sides: list[Levels], parts: int, width: int) -> dict[str, Any]:
    """The parts' mismatch, LATTICE diagnostics (bell_gate's `mismatch` on the real part of the cross-side products): M_k the sum over the window and both members of the real part of the product over the sides of the part k's amplitude, the ratios M_k / M_1, rho = 2 M_1 M_2 / (M_1^2 + M_2^2), and per side the parts' norms' ratios to the first part's; None where a divisor is 0."""
    products = [Fraction(0)] * parts
    squares = [[Fraction(0)] * parts for _ in sides]
    for interval in bell_gate.intervals_of(*sides):
        levels = [bell_gate.at(side, interval, parts * width) for side in sides]
        for k in range(parts):
            for member in range(2):
                product: Pair = (1, 0)
                for own, now in zip(squares, levels, strict=True):
                    u = amplitude(now, k, width, member)
                    product = times(product, u)
                    own[k] += norm(u)
                products[k] += product[0]
    first, second = products[0], products[1]
    size = first * first + second * second
    return {
        "label": "LATTICE",
        "products": [bell_gate.pair(value) for value in products],
        "ratios": [bell_gate.pair(value / first) if first else None for value in products[1:]],
        "rho": bell_gate.pair(2 * first * second / size) if size else None,
        "squares_ratios": [
            [bell_gate.pair(v / own[0]) if own[0] else None for v in own[1:]] for own in squares
        ],
    }


def one_world(world: Path, lines: list[dict[str, object]], expected: dict[str, Any]) -> dict[str, Any]:
    """One world's reading in the plane's form, bell_gate's `one_world` key for key, the side's setting read as the loader reads it (its `axis` where it declares one, its `basis` otherwise) and the family's declared sign under exchange read from the loaded world (`FamilyRule.exchange`, the key `exchange`; the joint shares in the sign's form, `credited`, named in `exchange`): the sides' settings and patterns, the 2^n joint shares, E_n, each side's marginal and every sub-correlation, the three local credits, the combination the draw realised (`drawn`), the mismatch and each side's inflow over the window; a pattern of other than the family's parts is refused by name."""
    loaded = load_world(world)
    family = next(f for f in loaded.families if f.name == expected["family"])
    window = (int(expected["window"][0]), int(expected["window"][1]))
    labels = list(expected["sides"])
    rows = [
        next(d for d in loaded.node_detectors if d.name == expected["sides"][label]) for label in labels
    ]
    for row in rows:
        if len(row.pattern) != family.parts:
            raise ValueError(
                f"node_detector {row.name!r} declares a pattern of {len(row.pattern)} parts, and the family "
                f"{family.name!r} has {family.parts}"
            )
    settings = [tuple(row.axis) or tuple(row.basis) for row in rows]  # the loader's rule: axis or basis
    ports = [
        bell_gate.ports_of(setting, row.pattern) for setting, row in zip(settings, rows, strict=True)
    ]
    sides = [bell_gate.reports(lines, family.name, row.name, window) for row in rows]
    parts, width, exchange = family.parts, family.width, family.exchange
    wall = count_wall(family, loaded.quantum_action)
    return {
        "world": world.name,
        "bases": {label: list(setting) for label, setting in zip(labels, settings, strict=True)},
        "settings_declared_as": {
            label: "axis" if row.axis else "basis" for label, row in zip(labels, rows, strict=True)
        },
        "lines_per_part": width,
        "patterns": {
            label: [list(part) for part in row.pattern] for label, row in zip(labels, rows, strict=True)
        },
        "exchange": EXCHANGE_WORDS.get(exchange),
        "form": "the sign's form, the determinant of the two sides' parts"
        if exchange < 0
        else "the parts paired part with part through the root",
        "intervals_reported": len(bell_gate.intervals_of(*sides)),
        **bell_gate.written(credits_of(sides, ports, parts, width, exchange), labels),
        "drawn": bell_gate.realised(lines, family.name, [row.name for row in rows], window),
        "mismatch": mismatch(sides, parts, width),
        "quanta": {
            label: [bell_gate.inflow_of(lines, family.name, row.name, window), wall]
            for label, row in zip(labels, rows, strict=True)
        },
    }


bell_gate.one_world = (
    one_world  # the reader's `reading` over the gate's worlds, each world read in the plane's form
)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--expectation", type=Path, required=True, help="the blind expectation file")
    parser.add_argument("--outputs", type=Path, nargs="+", required=True, help="the four output files")
    args = parser.parse_args(argv)
    print(json.dumps(bell_gate.reading(args.expectation, args.outputs), indent=1))


if __name__ == "__main__":
    main()
