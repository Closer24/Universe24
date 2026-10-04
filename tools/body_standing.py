"""The standing world's reads, lattice readings labelled so and no measurement (docs/ENGINE.md #5-the-output; HIGHLIGHTS.md, the body round's standing world: the mathematician's 167 with the advisor's second hand 5955658812 and, restating reads 2 and 3 for a real mode, the mathematician's 172 (#1572 comment 5959853571) with the advisor's second hand (#1563 comment 5960096992)): a world of one body is loaded as tools/run_inputs.py loads it and stepped by the engine's own step over the window, and at the body's declared Nodes (where the lay's share stands) the readings are taken from the record and the share, every number an exact fraction of the engine's integers. (1) The drift: the centroid of the body's share along each axis at the window's ends and its change, the centroid taken along each axis in turn with the density summed over the other two. (2) The deviation over the body of the law's own static quantity per Node, the form D_i = now^2 - next x before (ALGEBRA.md #the-count-is-the-records-share, the count the record's share), A_i^2 sin^2 omega exactly for one real mode at every interval: rho_D^2 = SUM over the body's Nodes of (D_i(k) - D_i(0))^2 / SUM of D_i(0)^2 at every interval (the series) and at the quarters of the window, so that the sqrt(n) law rho_D(n) / rho_D(n / 4) is read within the run, rho_D itself the fixed point of the division act on rho_D^2 at the scale of the universe's T, [rho_D T, T], no root; the form at the interval k needs the three levels z_(k - 1), z_k, z_(k + 1), so the window's last form is centred one interval before its end. Beside it, labelled the convention 167 wrote, the share's deviation rho_s on the levels' squares (`Lattice.share_of`, s_0 the lay's and s_n the share at the interval n), the real mode's own breathing at 2 omega and no drift, kept so that both stand in one output, with its series' local maxima and their spacings (`breathing`). The beat of a second mode the lay also carries (the lay's admixture, Delta omega between the two modes, T-free) is read on the series' envelope: the local maxima of rho_D^2 at every interval and of its means over successive windows of one period, with their spacings; with --beat-period the Fourier line of the series at that period in floats (the beat's weight, reported and not blinded, 175 (3)) and the series less the line at the quarters, the walk's part; a line near the board's lowest mode's period names the start's rest short of its own line if present. (3) The rotation read over a window of whole periods, 2 cos omega_read = SUM over the window's intervals of SUM over the body of z_t (z_(t + 1) + z_(t - 1)) / the same double sum of z_t^2, exact for one real mode with no singular interval, the period in whole intervals from the mode file's clock pair (2 cos omega = clock[0] / clock[1], the whole intervals nearest 2 pi / omega by the rotation's own recurrence, no angle and no root), as a fraction per successive window and over the whole run, the windows' least, largest and spread, and the window series' local maxima and spacings (two laid modes swing it at Delta omega, the beat read); the per-interval read cos omega_read = SUM z_t (z_(t + 1) + z_(t - 1)) / (2 SUM z_t^2) kept for the record, labelled near-singular twice a period for a real mode (every Node crossing 0 at once), its least and largest over the intervals where the record's weight 2 SUM z_t^2 is at least half its largest and the window's accumulated ratio. (4) The cube's 48 images (166's theorem, the body round's part 2): at the lay and after every interval every line of every family against its 48 images about the board's centre, the scalars equal to the bit, the tensions' lines carried as a tensor's diagonal and a holder's odd lines signed with the axis with their remainders complemented where signed; the interval through which the 48 held and the first departure named. The tool compares nothing, holds no number of the law and writes nothing to the engine; with an expectation file its blind and the body's own numbers from the lay are printed beside the readings.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/body_standing.py [--intervals N] [--beat-period P] [--expectation <expectation>.json] <world>.json ...
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.core.rule3 import coefficients, division_fixed_point
from event_universe.lattice import Lattice
from event_universe.loader.keys import AXES
from event_universe.records import complement
from event_universe.world_files import load_world

LABEL = "LATTICE"
MODE_SUFFIX = ".mode.json"  # the generator's mode file beside the world (ENGINE.md #4-the-input)


def pair(value: Fraction | None) -> list[int] | None:
    """A fraction as [numerator, denominator] for the output, None where there is none."""
    return None if value is None else [value.numerator, value.denominator]


def rooted(square: Fraction, scale: int) -> list[int]:
    """A fraction's root at a scale as [root x scale, scale] by the fixed point of the division act on the square's numerator times the scale squared over its denominator, the largest integer whose square fits (no root act)."""
    found = division_fixed_point(square.numerator * scale * scale // square.denominator)
    return [found, scale]


def centroids(density: np.ndarray, nodes: np.ndarray) -> list[Fraction | None]:
    """The centroid of a density over the Nodes `nodes` along each axis, the density summed over the other two axes at each coordinate, exact fractions; None where the density sums to 0."""
    weights = np.where(nodes, density, 0).astype(object)
    total = int(weights.sum())
    if total == 0:
        return [None] * len(AXES)
    grids = np.indices(density.shape)
    return [Fraction(int((weights * grids[axis]).sum()), total) for axis in range(len(AXES))]


def deviation(found: np.ndarray, laid: np.ndarray, nodes: np.ndarray) -> Fraction:
    """A quantity's deviation squared over the body's Nodes from its lay, SUM (q_n - q_0)^2 over SUM q_0^2, exact: the share's (rho_s^2, 167's convention) or the form's (rho_D^2, 172's read 2)."""
    moved = np.where(nodes, found.astype(object) - laid.astype(object), 0)
    return Fraction(
        int((moved * moved).sum()), int((np.where(nodes, laid, 0).astype(object) ** 2).sum())
    )


def form(before: np.ndarray, now: np.ndarray, after: np.ndarray, nodes: np.ndarray) -> np.ndarray:
    """The law's own static quantity per Node, the form D = now^2 - next x before (ALGEBRA.md #the-count-is-the-records-share: the count is the record's share, SUM D div T), over the body's Nodes and 0 elsewhere, exact integers: for one real mode A_i cos(omega t + phi) it is A_i^2 sin^2 omega at every interval, Node by Node, with no 2 omega term (172 (2))."""
    z, b, a = (np.where(nodes, levels, 0).astype(object) for levels in (now, before, after))
    return np.asarray(z * z - a * b)


def rotation(
    before: np.ndarray, now: np.ndarray, after: np.ndarray, nodes: np.ndarray
) -> tuple[int, int]:
    """The rotation of the body's record read in the summed form over its Nodes at one interval, as the pair (SUM z_t (z_(t + 1) + z_(t - 1)), 2 SUM z_t^2), whose ratio is cos omega_read (167's line as written; twice it is the rotation 2 cos omega the mode file's clock pair reads, z_(t + 1) + z_(t - 1) = 2 cos omega z_t on a standing record), exact integers; the pairs summed over a window of whole periods are read 3 as 172 restates it (`windows_read`), and per interval a real standing record passes through 0 at every Node at once twice a period, where the pair's second number is small and the ratio is the rounding's (`rotations_read`)."""
    z = np.where(nodes, now, 0).astype(object)
    return int((z * (after.astype(object) + before.astype(object))).sum()), 2 * int((z * z).sum())


def rotations_read(found: list[tuple[int, int, int]]) -> dict[str, Any]:
    """The per-interval rotation readings over the window, (numerator, weight, tick) per interval, kept for the record and labelled: cos omega_read's least and largest over the intervals whose weight is at least half the largest weight (the record away from its zero crossings) with their ticks and the spread, the count of those intervals, the window's accumulated ratio SUM numerators / SUM weights, and the first interval's 2 cos omega; for a real mode the per-interval read is near-singular twice a period (172 (3)), so its spread is those intervals' and no drift."""
    heaviest = max(weight for _n, weight, _t in found)
    strong = [(Fraction(n, w), t) for n, w, t in found if 2 * w >= heaviest]
    least, largest = min(strong), max(strong)
    return {
        "label": "per interval, near-singular twice a period for a real mode (172 (3))",
        "cos_omega_least": {"reading": pair(least[0]), "tick": least[1]},
        "cos_omega_largest": {"reading": pair(largest[0]), "tick": largest[1]},
        "spread": pair(largest[0] - least[0]),
        "intervals_read": len(strong),
        "accumulated_cos_omega": pair(
            Fraction(sum(n for n, _w, _t in found), sum(w for _n, w, _t in found))
        ),
        "two_cos_omega_first": pair(2 * Fraction(found[0][0], found[0][1])) if found[0][1] else None,
    }


def period_of(two_cos_omega: Fraction, longest: int) -> int:
    """The record's period in whole intervals from the mode file's clock pair, 2 cos omega = clock[0] / clock[1]: the least k from 1 at which u_k = cos(k omega), by the rotation's own recurrence u_(k + 1) = 2 cos omega u_k - u_(k - 1) from u_0 = 1 and u_1 = cos omega in exact fractions, is at or above both its neighbours, the whole intervals nearest to 2 pi / omega (no angle and no root); `longest`, the whole window, where the clock turns the record through no period within it."""
    previous, here = Fraction(1), two_cos_omega / 2
    for k in range(1, longest):
        following = two_cos_omega * here - previous
        if here >= previous and here >= following:
            return k
        previous, here = here, following
    return longest


def envelope(series: list[Fraction], first: int, step: int = 1) -> dict[str, Any]:
    """A series' local maxima (above the entry before, at or above the one after), each at `first` + its index x `step`, the spacings between them in the same unit and the spacings' mean as an exact fraction: the envelope's periods, a breathing's (a real mode's levels squared at 2 omega), a beat's (two laid modes at Delta omega) or a rest's miss ringing in the board's lowest mode."""
    maxima = [
        first + t * step
        for t in range(1, len(series) - 1)
        if series[t] > series[t - 1] and series[t] >= series[t + 1]
    ]
    spacings = [b - a for a, b in zip(maxima, maxima[1:], strict=False)]
    mean = Fraction(sum(spacings), len(spacings)) if spacings else None
    return {"maxima_at": maxima, "spacings": spacings, "mean_spacing": pair(mean)}


def every_tenth(series: list[Fraction], first: int, scale: int) -> dict[str, list[int]]:
    """A deviation squared series' root at every tenth index from `first`, as [rho x scale, scale] by the division act's fixed point."""
    every = 2 * (2 + 3)  # every tenth interval
    return {
        str(first + t): rooted(square, scale)
        for t, square in enumerate(series)
        if (first + t) % every == 0
    }


def breathing(series: list[Fraction], scale: int) -> dict[str, Any]:
    """The share's deviation squared at every interval from the interval 1 read for a breathing (the Boss's word on the advisor's finding, #1563 comment 5958624379, and 172 (2): a real mode's levels squared breathe at 2 omega, the maxima half a period apart, and a rest short of its own static line in the board's lowest mode rings at that mode's period): the series' envelope (`envelope`) and rho_s at every tenth interval as [rho_s x scale, scale]; a lattice diagnostic, nothing of the law."""
    return {**envelope(series, 1), "rho_every_tenth": every_tenth(series, 1, scale)}


def fourier_line(
    series: list[Fraction], first: int, step: int, period: int, at: list[int], scale: int
) -> dict[str, Any]:
    """The Fourier line of a series at a period in intervals (the entry t standing at the interval `first` + t x `step`), a float diagnostic of the series and nothing of the law (the mathematician's 175 (3) with the advisor's second hand: the lay's admixture, a neighbouring mode of the well, beats with the laid mode at Delta omega, its weight the line's at the beat's period, reported and not blinded, the lay at the integer fixed point carrying it by construction): the components c = (2 / N) SUM (m_t - mean) cos(2 pi k_t / period) and s = (2 / N) SUM (m_t - mean) sin(2 pi k_t / period), k_t the interval, the weight of the line as [weight x scale, scale] by the division act's fixed point on c^2 + s^2, and the series with the line subtracted at the intervals `at` (the walk's part, where the series is a deviation squared, as [root x scale, scale]; None where the residual is below 0)."""
    values = np.array([float(v) for v in series])
    k = first + step * np.arange(len(series))
    angle = 2 * np.pi * k / period
    centred = values - values.mean()
    c, s = 2 * (centred * np.cos(angle)).mean(), 2 * (centred * np.sin(angle)).mean()
    line = c * np.cos(angle) + s * np.sin(angle)
    residual = {int(i): float(values[t] - line[t]) for t, i in enumerate(k) if int(i) in at}
    return {
        "label": "a float diagnostic of the series; the beat's line, not blinded",
        "period": period,
        "cosine": c,
        "sine": s,
        "weight": rooted(Fraction(c * c + s * s), scale),
        "mean": float(values.mean()),
        "residual_at": {
            str(i): (rooted(Fraction(r), scale) if r >= 0 else None) for i, r in residual.items()
        },
    }


def form_read(
    series: list[Fraction],
    at: dict[str, Any],
    period: int,
    scale: int,
    last: int,
    beat: int | None,
) -> dict[str, Any]:
    """Read 2 as 172 restates it: rho_D^2 at every form centre k from 1 (the form at k from z_(k - 1), z_k and z_(k + 1), the lay's own form at 0 the reference, the window's last centre `last`), rho_D at the quarters (`at`, read in the loop) and at every tenth centre, the series' envelope (its maxima and spacings at the interval scale), and the series' means over successive windows of `period` intervals (the whole windows from the centre 1, each labelled by its first centre, rho_D of each mean as [rho_D x scale, scale]) with their envelope, the beat's read: two laid modes swing D at Delta omega, the walk alone rises as sqrt(n); with `beat`, the beat's period in intervals declared on the command line, the Fourier line of the series at it with the series less the line at the quarters, the walk's part (`fourier_line`)."""
    whole = [series[first : first + period] for first in range(0, len(series) - period + 1, period)]
    means = [Fraction(sum(window), len(window)) for window in whole]
    quarters = [int(centre) for centre in at]
    return {
        "centres": f"the form at k from z_(k - 1), z_k, z_(k + 1); the lay's own form at 0 the reference; the last centre {last}",
        "at": at,
        "rho_every_tenth": every_tenth(series, 1, scale),
        "envelope": envelope(series, 1),
        "beat_line": None if beat is None else fourier_line(series, 1, 1, beat, quarters, scale),
        "over_windows": {
            "period": period,
            "rho_of_mean": {str(1 + w * period): rooted(mean, scale) for w, mean in enumerate(means)},
            "envelope": envelope(means, 1, period),
        },
    }


def windows_read(
    turns: list[tuple[int, int]], period: int, beat: int | None, scale: int
) -> dict[str, Any]:
    """Read 3 as 172 restates it (with the advisor's second hand 5960096992): 2 cos omega_read = SUM over the window's intervals of SUM over the body of z_t (z_(t + 1) + z_(t - 1)) / the same double sum of z_t^2, the per-interval pairs (numerator, 2 SUM z_t^2) summed over successive windows of `period` intervals, whole periods from the first centre (a last partial window left out), exact for one real mode with no singular interval, every Node's zero crossing summed over the period; per window as a fraction, labelled by the window's first centre; over the whole run; the windows' least and largest with their labels and the spread; the window series' envelope, the beat's read where two modes are laid (the series swings at Delta omega), and with `beat` the Fourier line of the window series at the beat's period (`fourier_line`, the residual at no interval)."""
    whole = [turns[first : first + period] for first in range(0, len(turns) - period + 1, period)]
    series = [2 * Fraction(sum(n for n, _w in window), sum(w for _n, w in window)) for window in whole]
    least, largest = min(series), max(series)
    return {
        "period": period,
        "windows": len(series),
        "two_cos_omega": {str(w * period): pair(value) for w, value in enumerate(series)},
        "two_cos_omega_whole_run": pair(
            2 * Fraction(sum(n for n, _w in turns), sum(w for _n, w in turns))
        ),
        "least": {"reading": pair(least), "from": series.index(least) * period},
        "largest": {"reading": pair(largest), "from": series.index(largest) * period},
        "spread": pair(largest - least),
        "envelope": envelope(series, 0, period),
        "beat_line": None if beat is None else fourier_line(series, 0, period, beat, [], scale),
    }


def imaged(array: np.ndarray, axes: tuple[int, ...], signs: tuple[int, ...]) -> np.ndarray:
    """An array under one of the cube's 48 symmetries about the board's centre (an odd board, its centre a Node): its axes permuted and each reflected where its sign is -1."""
    return np.transpose(array, axes)[tuple(slice(None, None, sign) for sign in signs)]


def images_kept(board: Lattice) -> list[str]:
    """The cube's 48 images of the state, 166's theorem read as a lattice diagnostic (HIGHLIGHTS.md, the mathematician's 166 with the advisor's second hand; the body round's part 2): for every one of the 48 symmetries about the board's centre (an odd board), every scalar line (a family of quanta's lines, a held row's time line) equal at the image to the bit, levels, remainder and write remainder; a held row's three axis lines carried by their kind, the line of the image axis equal at the image for the tensions (the diagonal of a tensor) and, for the odd lines of a holder under the rotation, negated where the axis is reflected with the remainder and the write remainder complemented there (`records.complement`, Rule3's wall and the write's); every departure named once, by the family, the row and the symmetry; an empty list where the 48 hold."""
    found = []
    gamma, unit = board.world.node_clock, board.unit
    for index, (family, state) in enumerate(zip(board.families, board.states, strict=True)):
        width, lines = family.width, state.lines
        vectors = width - 1 if family.axes else 0
        rule_wall = coefficients(family.pair[0], family.pair[1], gamma, gamma, gamma, None, unit)[2]
        for axes, signs in product(permutations(range(len(AXES))), product((1, -1), repeat=len(AXES))):
            for first in range(0, len(lines), width):
                kept = True
                for line in range(first, first + width - vectors):
                    arrays = [lines[line].now, lines[line].before, lines[line].remainder]
                    arrays += [state.write_remainders[line]] if family.held else []
                    kept = kept and all(np.array_equal(imaged(a, axes, signs), a) for a in arrays)
                for axis in range(vectors):
                    here, source = lines[first + 1 + axis], lines[first + 1 + axes[axis]]
                    writes = state.write_remainders
                    carried = (writes[first + 1 + axis], writes[first + 1 + axes[axis]])
                    pairs: list[tuple[np.ndarray, np.ndarray, int | None]] = [
                        (here.now, source.now, None),
                        (here.before, source.before, None),
                    ]
                    pairs += [(here.remainder, source.remainder, rule_wall)]
                    pairs += [(carried[0], carried[1], board.walls(index)[first + 1 + axis])]
                    for own, image, wall in pairs:
                        expected = imaged(image, axes, signs)
                        if family.rotation and signs[axis] == -1:
                            expected = -expected if wall is None else complement(expected, wall)
                        kept = kept and np.array_equal(expected, own)
                if not kept:
                    found.append(
                        f"{family.name} row {first // width} under the axes {axes} and the signs {signs}"
                    )
    return found


def clock_of(path: Path) -> Fraction:
    """The body's clock pair from the generator's mode file beside the world, 2 cos omega = clock[0] / clock[1] (ENGINE.md #4-the-input), the rotation the lay stands at; the window's period is read from it."""
    mode = json.loads(path.with_suffix(MODE_SUFFIX).read_text(encoding="utf-8"))
    clock = mode["bodies"][0]["clock"]
    return Fraction(int(clock[0]), int(clock[1]))


def standing(path: Path, intervals: int | None, beat: int | None = None) -> dict[str, Any]:
    """One world's reads over the window (the world's ticks, or `intervals`; `beat` the beat's period in intervals for the Fourier line, None for none): the body's declared Nodes read, the lay's share and form kept, the board stepped interval by interval with the record's level before each step kept as z_(t - 1); the rotation's pair at every interval, the form's and the share's deviations at the quarters of the window and at every interval, the centroids at its ends, the 48 images after every interval, labelled LATTICE."""
    board = Lattice(load_world(path))
    if len(board.world.bodies) != 1:
        raise ValueError(
            f"{path.name} declares {len(board.world.bodies)} bodies: the standing world has one"
        )
    row = board.world.bodies[0]
    index, nodes, action = row.family, board.mask(row.nodes), board.world.quantum_action
    steps = board.world.ticks if intervals is None else intervals
    quarters = sorted({steps * part // (2 * 2) for part in (1, 2, 3, 2 * 2)} - {0})
    centres = sorted({steps * part // (2 * 2) for part in (1, 2, 3)} | {steps - 1}) if steps else []
    period = period_of(clock_of(path), steps)
    laid = board.share_of(index)[0]
    start = centroids(laid, nodes)
    deviations: dict[str, Any] = {}
    series: list[Fraction] = []  # the share's deviation squared at every interval, the breathing's
    laid_form: np.ndarray | None = None  # the lay's own form, D_i(0), the reference of read 2
    forms: dict[str, Any] = {}
    form_series: list[Fraction] = []  # rho_D^2 at every form centre from 1
    turns: list[tuple[int, int]] = []  # the rotation's pair at every interval, read 3's windows
    rotations: list[tuple[int, int, int]] = []
    images: dict[str, Any] = {"departed": images_kept(board), "tick": 0}  # the lay's own images
    for _ in range(steps):
        record = board.record(index)[0]
        previous, current = record.before.copy(), record.now.copy()  # z_(t - 1) and z_t at the tick t
        board.step()
        if board.ended is not None:
            break
        after = board.record(index)[0].now  # z_(t + 1) stepped
        turned = rotation(previous, current, after, nodes)
        turns.append(turned)
        if turned[1]:
            rotations.append((*turned, board.tick))
        here, centre = form(previous, current, after, nodes), board.tick - 1  # D centred at t
        if laid_form is None:
            laid_form = here
        else:
            square = deviation(here, laid_form, nodes)
            form_series.append(square)
            if centre in centres:
                forms[str(centre)] = {"squared": pair(square), "rho": rooted(square, action)}
        if not images["departed"]:
            images = {"departed": images_kept(board), "tick": board.tick}
        square = deviation(board.share_of(index)[0], laid, nodes)
        series.append(square)
        if board.tick in quarters:
            deviations[str(board.tick)] = {"squared": pair(square), "rho": rooted(square, action)}
    end = centroids(board.share_of(index)[0], nodes)
    return {
        "label": LABEL,
        "input": path.name,
        "intervals": board.tick,
        "ended": board.ended,
        "quantum_action": action,
        "amplitude_bound": board.world.amplitude_bound,
        "nodes": int(nodes.sum()),
        "family": board.families[index].name,
        "two_cos_omega_clock": pair(clock_of(path)),
        "centroid": {
            "start": [pair(c) for c in start],
            "end": [pair(c) for c in end],
            "drift": [
                None if a is None or b is None else pair(b - a) for a, b in zip(start, end, strict=True)
            ],
        },
        "form_deviation": form_read(form_series, forms, period, action, board.tick - 1, beat),
        "share_deviation": {
            "label": "the levels' squares, 167's convention; a real mode's own breathing at 2 omega",
            "at": deviations,
            "breathing": breathing(series, action),
        },
        "rotation_windows": windows_read(turns, period, beat, action),
        "rotation": rotations_read(rotations),
        "images": {
            "kept_to_the_bit_through": board.tick if not images["departed"] else images["tick"] - 1,
            "first_departure": None
            if not images["departed"]
            else {"tick": images["tick"], "named": images["departed"][: 2 + 1]},
        },
        "books": board.books(),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "worlds", type=Path, nargs="+", help="the world files, each with its mode file beside it"
    )
    parser.add_argument(
        "--intervals", type=int, default=None, help="the intervals read (the world's ticks)"
    )
    parser.add_argument("--expectation", type=Path, default=None, help="the blind expectation file")
    parser.add_argument(
        "--beat-period",
        type=int,
        default=None,
        help="the beat's period in intervals for the Fourier line of the series (none: not read)",
    )
    args = parser.parse_args(argv)
    found: dict[str, Any] = {"label": LABEL}
    found["worlds"] = {
        path.stem: standing(path, args.intervals, args.beat_period) for path in args.worlds
    }
    if args.expectation is not None:
        expected = json.loads(args.expectation.read_text(encoding="utf-8"))
        found["blind"] = {
            key: expected.get(key) for key in ("reading", "blind", "fence", "status", "from_the_lay")
        }
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()
