"""The joint-share reader for a gate of a record of planes (ALGEBRA.md, Spin, the spin branch of 2026-10-19; tests/test_the_spin.py, the singlet), read side by side (ALGEBRA.md, The meeting's reading, the one meeting): every side is read by its own local form from its own region's `parts` lines over its own window, w_side(p) = SUM_kl e_k(p) e_l(p) G_kl M_kl, M_kl the second moments of the parts' sums over the side's window and both members of the level pair (a part of a plane family has two lines, re and im, so the `parts` line of a region holds 2 x parts rows, the part k's pair on the rows 2 k and 2 k + 1, and M_kl = SUM re_k re_l + im_k im_l; a record of real lines the same with im at 0), G the Gram of the sides closing after it from their declared patterns (G_kl = PROD over those sides of SUM over the side's two ports of v_k v_l, v the side's coefficients on the record's parts, e_k(port) for the symmetric record and the determinant's partner column SUM_{l != k} sign(l - k) e_l(port) for the antisymmetric pair; every entry 1 for the last side), the realised ports of the sides closing before it standing on the parts as its lines hold them (the engine's write at the birth, read in the lines after that side's close, and applied to the lines at or before it, the write absent from them); the first side's read is the joint form's marginal by the Gram theorem, a later side's the rewritten record's. The gate's E for a run is the realised branch, E = SUM over the last side's ports of the sign of the combination (the earlier sides' realised ports with it) times the last side's share on that branch, P(b | a*) for two sides, a* the first side's realised port from the output's `credit` lines; the branch is named in the file. On the singlet the blind's E holds for either branch, the record being symmetric under the swap of the two ports (P(b | a*) at one port is P(-b | -a*) at the other, and the sign of the combination the same); no claim beyond it. Where the joint form is defined on the same lines, every side's lines before every write (the sides closing together in one window), the local read and the joint read are asserted equal exactly, share by share on the realised branch, the Gram theorem in the tool: the tool refuses by name where they differ. The joint form of the earlier declaration stays as the diagnostic and the blind's form: tools/bell_gate.py's reading in the plane's form, the gate's own arithmetic: the joint share J = SUM over the window and both members of |SUM_k c_k PROD_sides psi^s_k|^2 with psi^s_k the part's (re, im) sums at the side s, the product over the sides a plane's product and the square the pair's norm; a record of real lines is the same form with im at 0, bell_gate's. The family's declared sign under exchange is read from the loaded world (the key `exchange`, 2026-10-19; ALGEBRA.md, Spin, closed for the paper as a route, The family's sign under exchange): under the antisymmetric sign the meeting's amplitude is SUM over the ordered pairs (k, l), k != l, of sign(l - k) e^L_k(port_L) psi^L_k x e^R_l(port_R) psi^R_l, the plane products as `times` makes them, then the norm, the determinant of the two sides' parts, two sides and more refused by name; the symmetric and the undeclared record the form above; the local credits (by the parts' shares, by the local sums, by the sign) the fences as they stand; `at_equal_parts(ports, exchange)` the blind's numbers in the same form for a folder's builder. A side's setting is read as the loader reads it, `axis` where it declares one (a record of planes: the half-angle pair (c, s)) and `basis` otherwise, the ports' arithmetic one (`loader/draw.ports_of`: e_k(+) = alpha_k c + beta_k s, e_k(-) = alpha_k (-s) + beta_k c). The singlet's two regions, the left's pattern the identity and the right's [[0, 1], [-1, 0]], read E(a, b) = -cos(theta_a - theta_b) exact in the integers' rationals from the engine's `parts` lines: -119 / 169, 119 / 169, -120 / 169 and -120 / 169 at the four Bell settings, S = -478 / 169 with the CHSH signs (|S| = 478 / 169, above 2 and below 2 sqrt 2 by 2.5 x 10^-5), every marginal 1 / 2, the shares of (+, +) and (-, -) 0 at equal axes; beside them the three local credits as the fence, in the same plane form (by the parts' shares, each part's norm alone; by the local sums, the product of the sides' own norms; by the sign, each side's larger port), every one a product form with |S| at most 2; the combination realised per world from the output's `credit` lines, the sides' draws; the mismatch diagnostics on the real part of the cross-side products, LATTICE and never in the blind. The reader's file is bell_gate's, key for key (`bases` the side's setting as declared; `correlation` the realised branch's E, the joint form's under `correlation_by_the_joint_shares`), so that tools/look/page.py's gate panels read it unchanged; E, the marginals, the combination and the blind are bell_gate's own functions; the tool holds no number.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/spin_gate.py --expectation examples/events/bell_singlet/expectation.json --outputs runs/singlet/*.output.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from fractions import Fraction
from itertools import combinations, product
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
Terms = list[tuple[int, tuple[int, ...]]]  # the amplitude's terms: the sign, the part each side reads
Matrix = list[list[int]]  # parts x parts, the Gram or the second moments
Close = dict[
    str, Any
]  # a side's credit line read: its order, the window drawn over, the close, the realised port
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


def terms_of(parts: int, sides: int, exchange: int) -> Terms:
    """The amplitude's terms as (the sign, the part each side reads), the record's sign under exchange, the family's declaration (the engine's `credit.terms_of`; ALGEBRA.md, Spin, closed for the paper as a route, The family's sign under exchange): SUM_k over the same part k at every side for the symmetric record and a family declaring no sign (`exchange` 1 or 0, the form as it stood); SUM_{k != l} sign(l - k) over the ordered pairs of parts across two sides for the antisymmetric (`exchange` -1), the determinant of the two sides' parts, more than two sides refused by name."""
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
    """The shares of every combination of ports accumulated over the window on both members, the joint form: per interval and member the amplitude's terms (`terms_of`, by the family's sign under exchange: over the parts for the symmetric or undeclared record, over the ordered pairs of parts with their sign for the antisymmetric), each the product over the sides of e_k(port) times the part's amplitude there, the plane products as `times` makes them, summed and then the norm where `joined` (the joint form, the gate's own arithmetic), or each norm alone (the local credit by the parts' shares, a fence read over the parts whatever the sign)."""
    found = {key: Fraction(0) for key in bell_gate.keys_of(len(sides))}
    signed = terms_of(parts, len(sides), exchange if joined else 0)
    for interval in bell_gate.intervals_of(*sides):
        levels = [bell_gate.at(side, interval, parts * width) for side in sides]
        for key in found:
            for member in range(2):
                terms = []
                for sign, which in signed:
                    product_: Pair = (sign, 0)
                    for e, port, now, k in zip(ports, key, levels, which, strict=True):
                        factor = e[port][k]
                        re, im = amplitude(now, k, width, member)
                        product_ = times(product_, (factor * re, factor * im))
                    terms.append(product_)
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
    """The reader's numbers from the sides' reports in the plane's form, the joint form: the 2^n joint shares in the sign's form (`credited` with the family's `exchange`), E_n, each side's marginal, every sub-correlation and the three local credits' E, the fences as they stand whatever the sign, exact fractions (E and the marginals by bell_gate's own functions)."""
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
                product_: Pair = (1, 0)
                for own, now in zip(squares, levels, strict=True):
                    u = amplitude(now, k, width, member)
                    product_ = times(product_, u)
                    own[k] += norm(u)
                products[k] += product_[0]
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


def closes_of(
    lines: list[dict[str, object]], family: str, node_detectors: list[str], window: tuple[int, int]
) -> dict[str, Close | None]:
    """Per side, by its region's name, its credit line of the family within the window (the last of a window per side, the click), read as the side's close: `order`, the side's place among the sides' draws (1 the first), the `window` it drew over (the expectation's where the line names none), the close (the line's interval), the port `realised`, and `scale` and `board_count` where the line carries them; None for a side with no credit line (a world declaring no draw)."""
    found: dict[str, Close | None] = {name: None for name in node_detectors}
    for line in lines:
        if line.get("event") != "credit" or line.get("family") != family:
            continue
        name = str(line.get("node_detector"))
        if name in found and window[0] <= int(str(line["interval"])) <= window[1]:
            drawn = line.get("window")
            found[name] = {
                "order": None if line.get("order") is None else int(str(line["order"])),
                "window": [int(str(v)) for v in drawn] if isinstance(drawn, list) else list(window),
                "close": int(str(line["interval"])),
                "realised": None if line.get("realised") is None else str(line["realised"]),
                "scale": line.get("scale"),
                "board_count": line.get("board_count"),
            }
    return found


def drawn_order(closes: list[Close | None]) -> list[int]:
    """The sides' indexes in the order of their draws: by the credit lines' `order` where every side carries one, else by their closes where every side clicked, else as the expectation lists them (equal values in the listed order)."""
    indexes = list(range(len(closes)))
    if all(c is not None and c["order"] is not None for c in closes):
        return sorted(indexes, key=lambda i: (int(closes[i]["order"]), i))  # type: ignore[index]
    if all(c is not None for c in closes):
        return sorted(indexes, key=lambda i: (int(closes[i]["close"]), i))  # type: ignore[index]
    return indexes


def vector_of(terms: Terms, reading: int, other: int, ports: Ports, port: str, parts: int) -> list[int]:
    """The other side's coefficients on the record's parts as the reading side holds them: v_k = SUM over the terms whose part at the reading side is k of the term's sign times the other side's e at the port on its part in the term; e_k(port) itself for the symmetric record (the terms paired part with part), for the antisymmetric pair the determinant's partner column SUM_{l != k} sign(l - k) e_l(port). At the other side's realised port it is that side's write on the parts before the reduction (the engine's `meeting_back.coefficients_of`, `credit.reduced` taking the greatest common divisor out, a common factor every share cancels); summed over the other side's two ports in products it is the Gram (`meeting_back.gram_of`)."""
    found = [0] * parts
    for sign, which in terms:
        found[which[reading]] += sign * ports[port][which[other]]
    return found


def gram_of(terms: Terms, reading: int, later: list[int], ports: list[Ports], parts: int) -> Matrix:
    """The Gram of the sides closing after the reading side, from their declared patterns: G_kl = SUM over the combinations of the later sides' ports of the product over those sides of v_k v_l (the entrywise product of their Grams, the terms pairing the parts side by side); every entry 1 for the last side, the coherent read (the engine's `meeting_back.gram_of`)."""
    found = [[0] * parts for _ in range(parts)]
    for key in product(PORTS, repeat=len(later)):
        vectors = [
            vector_of(terms, reading, other, ports[other], port, parts)
            for other, port in zip(later, key, strict=True)
        ]
        for k in range(parts):
            for m in range(parts):
                found[k][m] += prod(v[k] * v[m] for v in vectors)
    return found


def moments_of(levels: Levels, parts: int, width: int, standing: Callable[[int], list[int]]) -> Matrix:
    """A side's second moments over its window and both members of the level pair: M_kl = SUM over the intervals reported and both members of re_k re_l + im_k im_l, the part's (re, im) sums at the side (im 0 for a real line), each interval's parts first scaled by the coefficients standing on them there (`standing(interval)`: the earlier sides' realised coefficients absent from the lines, 1 where the write is in the lines; the engine's `Books.moments`, booked from the record where it stands)."""
    found = [[0] * parts for _ in range(parts)]
    for interval in bell_gate.intervals_of(levels):
        here, scale = bell_gate.at(levels, interval, parts * width), standing(interval)
        for member in range(2):
            amplitudes = [amplitude(here, k, width, member) for k in range(parts)]
            for k in range(parts):
                for m in range(parts):
                    found[k][m] += (
                        scale[k]
                        * scale[m]
                        * (amplitudes[k][0] * amplitudes[m][0] + amplitudes[k][1] * amplitudes[m][1])
                    )
    return found


def local_weights(ports: Ports, gram: Matrix, moments: Matrix) -> dict[str, Fraction]:
    """A side's local form per port, w(p) = SUM_kl e_k(p) e_l(p) G_kl M_kl (ALGEBRA.md, The meeting's reading; the engine's `meeting_back.side_weights`): its own second moments under the Gram of the sides closing after it, a sum of norms over the later sides' ports and never negative."""
    parts = len(gram)
    return {
        port: Fraction(
            sum(
                ports[port][k] * ports[port][m] * gram[k][m] * moments[k][m]
                for k in range(parts)
                for m in range(parts)
            )
        )
        for port in PORTS
    }


def shares_of(weights: dict[str, Fraction]) -> dict[str, Fraction] | None:
    """A side's shares per port, its weights over their sum; None where nothing was read."""
    total = sum(weights.values(), Fraction(0))
    return None if not total else {port: value / total for port, value in weights.items()}


def local_reads(
    sides: list[Levels],
    ports: list[Ports],
    closes: list[Close | None],
    order: list[int],
    parts: int,
    width: int,
    exchange: int,
) -> list[dict[str, Any]]:
    """Every side's local read in the order of the draws (ALGEBRA.md, The meeting's reading, 2026-10-20: the one meeting, each side drawn alone on its own region's lines): per side the Gram of the sides closing after it, the earlier sides' realised coefficients on the parts (`vector_of` at the realised port, applied to the lines at or before that side's close, the write absent from them; the lines after it carry the write), its second moments over its own window, its weights per port and its shares (None after a side that realised no port); the first side's read is the joint form's marginal by the Gram theorem, a later side's the rewritten record's."""
    terms = terms_of(parts, len(sides), exchange)
    found = []
    for position, reading in enumerate(order):
        earlier, later = order[:position], order[position + 1 :]
        realised = [None if closes[e] is None else closes[e]["realised"] for e in earlier]  # type: ignore[index]
        gram = gram_of(terms, reading, later, ports, parts)
        read: dict[str, Any] = {
            "side": reading,
            "order": position + 1,
            "gram": gram,
            "earlier": None,
            "weights": None,
            "shares": None,
        }
        close = closes[reading]
        window = None if close is None else close["window"]
        levels = (
            sides[reading]
            if window is None
            else {t: v for t, v in sides[reading].items() if window[0] <= t <= window[1]}
        )
        read["window"] = window
        if all(port is not None for port in realised):
            vectors = [
                (int(closes[e]["close"]), vector_of(terms, reading, e, ports[e], str(port), parts))  # type: ignore[index]
                for e, port in zip(earlier, realised, strict=True)
            ]

            def standing(interval: int, vectors: list[tuple[int, list[int]]] = vectors) -> list[int]:
                return [prod(v[k] for close, v in vectors if interval <= close) for k in range(parts)]

            intervals = bell_gate.intervals_of(levels)
            read["earlier"] = [
                {
                    "side": e,
                    "realised": port,
                    "coefficients": v,
                    "in_the_lines": "all"
                    if all(t > close for t in intervals)
                    else "none"
                    if all(t <= close for t in intervals)
                    else "mixed",
                }
                for (e, port), (close, v) in zip(
                    zip(earlier, realised, strict=True), vectors, strict=True
                )
            ]
            moments = moments_of(levels, parts, width, standing)
            weights = local_weights(ports[reading], gram, moments)
            read["weights"], read["shares"] = weights, shares_of(weights)
        found.append(read)
    return found


def branch_of(reads: list[dict[str, Any]], order: list[int]) -> dict[str, Any]:
    """The realised branch: the ports the sides before the last realised and the last side's shares given them; E on the branch = SUM over the last side's ports of the sign of the combination (the realised ports with it, the product of the ports' signs) times the last side's share; None where a side before the last realised no port or the last side read nothing."""
    last, earlier = reads[-1], reads[-1]["earlier"]
    if last["shares"] is None or earlier is None:
        return {"realised": None, "last": order[-1], "shares": None, "correlation": None}
    realised = {int(found["side"]): str(found["realised"]) for found in earlier}

    def key_with(port: str) -> tuple[str, ...]:
        found = [""] * len(order)
        for side, p in realised.items():
            found[side] = p
        found[order[-1]] = port
        return tuple(found)

    correlation = sum(
        (
            bell_gate.signed(key_with(port), range(len(order))) * share
            for port, share in last["shares"].items()
        ),
        Fraction(0),
    )
    return {
        "realised": realised,
        "last": order[-1],
        "shares": last["shares"],
        "correlation": correlation,
    }


def agreed(
    joint: Joint,
    reads: list[dict[str, Any]],
    order: list[int],
    closes: list[Close | None],
    sides: list[Levels],
    labels: list[str],
) -> dict[str, Any]:
    """The Gram theorem checked where the joint form is defined on the same lines (every side's lines at or before every earlier side's close, no write in them, and the joint shares not all 0): every side's local shares equal the joint form's shares on the realised branch, the first side's its marginal, a later side's its conditional given the earlier sides' realised ports, exactly as fractions, and E on the branch the joint form's on that branch; refused by name where they differ; not checked, and said so, where the sides read in different windows."""
    total = sum(joint.values(), Fraction(0))
    before_every_write = all(
        t <= int(closes[e]["close"])  # type: ignore[index]
        for position, s in enumerate(order)
        for e in order[:position]
        if closes[e] is not None
        for t in sides[s]
    )
    if not total:
        return {
            "checked": False,
            "words": "the joint form reads nothing on these lines (the sides' lines share no interval): the local read alone",
        }
    if not before_every_write:
        return {
            "checked": False,
            "words": "a side's lines carry an earlier side's write: the joint form is not the same record, the local read alone",
        }
    if any(read["shares"] is None for read in reads):
        return {"checked": False, "words": "a side realised no port: the branch is not read"}
    for position, read in enumerate(reads):
        s, fixed = int(read["side"]), {e: str(closes[e]["realised"]) for e in order[:position]}  # type: ignore[index]
        on_branch = {
            key: value for key, value in joint.items() if all(key[e] == p for e, p in fixed.items())
        }
        branch_total = sum(on_branch.values(), Fraction(0))
        conditional = {
            port: sum((v for key, v in on_branch.items() if key[s] == port), Fraction(0)) / branch_total
            for port in PORTS
        }
        if conditional != read["shares"]:
            raise ValueError(
                f"the local read of the side {labels[s]!r} {dict(read['shares'])} differs from the joint form's "
                f"share on the realised branch {conditional}: the Gram theorem holds for parts stepping alike at "
                "the side, and these lines do not"
            )
    return {
        "checked": True,
        "words": "the local read of every side equals the joint form's share on the realised branch, exactly (the Gram theorem)",
    }


def one_world(world: Path, lines: list[dict[str, object]], expected: dict[str, Any]) -> dict[str, Any]:
    """One world's reading in the plane's form, bell_gate's `one_world` key for key, the side's setting read as the loader reads it (its `axis` where it declares one, its `basis` otherwise) and the family's declared sign under exchange read from the loaded world (`FamilyRule.exchange`, the key `exchange`): the sides' settings and patterns, the sides' local reads in the order of their draws (`local_reads`), the realised branch and its E (`correlation`), the joint form's 2^n shares, E_n (`correlation_by_the_joint_shares`), each side's marginal (the first side's by its local read, the later sides' the joint form's where it reads, `marginals_by_the_joint_shares` the joint form's alone) and every sub-correlation, the three local credits, the combination the sides' draws realised (`drawn`), the agreement of the local and the joint reads where both are defined (`agreement`), the mismatch and each side's inflow over the window; a pattern of other than the family's parts is refused by name."""
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
    names = [row.name for row in rows]
    by_name = closes_of(lines, family.name, names, window)
    closes = [by_name[name] for name in names]
    order = drawn_order(closes)
    reads = local_reads(sides, ports, closes, order, parts, width, exchange)
    branch = branch_of(reads, order)
    joint = credited(sides, ports, parts, width, True, exchange)
    agreement = agreed(joint, reads, order, closes, sides, labels)
    written = bell_gate.written(credits_of(sides, ports, parts, width, exchange), labels)
    marginals = dict(
        written["marginals"]
    )  # the first side's by its local read, the others the joint form's
    if reads[0]["shares"] is not None:
        marginals[labels[int(reads[0]["side"])]] = bell_gate.pair(reads[0]["shares"][PORTS[0]])
    if branch["correlation"] is not None and agreement["checked"]:
        on_branch = {
            key: value
            for key, value in joint.items()
            if all(key[e] == p for e, p in branch["realised"].items())
        }
        if bell_gate.correlation(on_branch) != branch["correlation"]:
            raise ValueError(
                f"E on the realised branch by the local read, {branch['correlation']}, differs from the joint "
                f"form's on that branch, {bell_gate.correlation(on_branch)}"
            )
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
        **written,
        "correlation": bell_gate.pair(branch["correlation"]),
        "correlation_by_the_joint_shares": written["correlation"],
        "marginals": marginals,
        "marginals_by_the_joint_shares": written["marginals"],
        "local_reads": [
            {
                "side": labels[int(read["side"])],
                "order": read["order"],
                "window": read["window"],
                "close": None
                if closes[int(read["side"])] is None
                else closes[int(read["side"])]["close"],  # type: ignore[index]
                "realised": None
                if closes[int(read["side"])] is None
                else closes[int(read["side"])]["realised"],  # type: ignore[index]
                "scale": None
                if closes[int(read["side"])] is None
                else closes[int(read["side"])]["scale"],  # type: ignore[index]
                "board_count": None
                if closes[int(read["side"])] is None
                else closes[int(read["side"])]["board_count"],  # type: ignore[index]
                "gram": read["gram"],
                "earlier": None
                if read["earlier"] is None
                else [{**found, "side": labels[int(found["side"])]} for found in read["earlier"]],
                "weights": None
                if read["weights"] is None
                else {port: str(value) for port, value in read["weights"].items()},
                "shares": None
                if read["shares"] is None
                else {port: bell_gate.pair(value) for port, value in read["shares"].items()},
            }
            for read in reads
        ],
        "branch": {
            "realised": None
            if branch["realised"] is None
            else {labels[side]: port for side, port in branch["realised"].items()},
            "last": labels[branch["last"]],
            "shares": None
            if branch["shares"] is None
            else {port: bell_gate.pair(value) for port, value in branch["shares"].items()},
        },
        "agreement": agreement,
        "drawn": bell_gate.realised(lines, family.name, names, window),
        "mismatch": mismatch(sides, parts, width),
        "quanta": {
            label: [bell_gate.inflow_of(lines, family.name, row.name, window), wall]
            for label, row in zip(labels, rows, strict=True)
        },
    }


def reading(expectation: Path, outputs: list[Path]) -> dict[str, object]:
    """The reading of the gate's worlds against the expectation, bell_gate's `reading` with this file's `one_world`, key for key (`correlation` and the combination by the realised branch), with the combination by the joint form beside it (`<name>_by_the_joint_shares`, None where a world's joint form reads nothing), the realised branch per world and the agreement of the local and the joint reads."""
    found = bell_gate.reading(expectation, outputs, one_world)
    expected = json.loads(expectation.read_text(encoding="utf-8"))
    worlds = found["worlds"]
    assert isinstance(worlds, dict)
    ordered = [worlds[str(expected["runs"][key])] for key in expected["order"]]
    label, signs = (
        str(expected["combination"]["name"]),
        [int(s) for s in expected["combination"]["signs"]],
    )
    found[f"{label}_by_the_joint_shares"] = bell_gate.pair(
        bell_gate.combination(
            (bell_gate.fraction(world["correlation_by_the_joint_shares"]) for world in ordered), signs
        )
    )
    found["branches"] = {
        key: world["branch"] for key, world in zip(expected["order"], ordered, strict=True)
    }
    found["agreement"] = {
        key: world["agreement"] for key, world in zip(expected["order"], ordered, strict=True)
    }
    return found


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--expectation", type=Path, required=True, help="the blind expectation file")
    parser.add_argument("--outputs", type=Path, nargs="+", required=True, help="the four output files")
    args = parser.parse_args(argv)
    print(json.dumps(reading(args.expectation, args.outputs), indent=1))


if __name__ == "__main__":
    main()
