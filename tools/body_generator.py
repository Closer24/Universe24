"""THE GENERATOR BY THE RULE (ALGEBRA.md 9.118; the Boss's record 2233 on the model
owner's word; record 1924: "the generator is the operator iterated, with its stop").

A body's integers as the rule iterated with a stop, one tool for every world's
generator (a HOST tool: it writes integers into the world file under the stamp, and the
engine reads integers alone):

- THE PROFILE (9.118 item 1; record 1898; 9.22 (7)): the rule's spatial operator
  iterated in integers from the body's Nodes' indicator, the stop the loader's
  residual bound (`iterated_mode` of the margin module, the one copy of the step).
  Today's profile is the mode of the rule at the vacuum's pace (c = 0 everywhere).
- THE PERIOD (9.118 item 2 (a)): the one-Node rule is the rotation, c_(t+1) = (a / b)
  c_t - c_(t-1) from c_0 = 1 and c_1 = a / (2 b), exact rationals; P is the first t at
  which the rotation has passed half a turn and returned within half a step of its
  start, the nearest integer to 2 pi / omega with no pi.
- THE RUN'S RULE (9.118 item 3, a finding): the run steps the body's record at the pace
  Gamma - c with its own content, so the run's spatial operator at the body's Nodes
  differs from the vacuum's by the content's share; `run_rule_reading` reads, for a
  shipped body, the run's own 2 cos omega (the quotient of the profile on the engine's
  integers (R, S, w) of 9.57 (1)) against the file's clock, the world's move before any
  regeneration. The profile by the run's rule waits for the model owner's word.
- The twist "own" and a moving body's proper pairs keep their present numbers until
  9.118 items 2 (b) and (c) are decided.

Integers and exact rationals only; no float in any number written.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.diagnostics.massive_record_margin import iterated_mode
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.rule import rule_coefficients
from event_universe.events.world import body_node_indices, six_neighbours_flat
from event_universe.world_files import parse_nature_beam_world

RETURN_LIMIT = 1 << 24  # intervals; a rotation slower than this is no mode of a run


def period_by_the_rule(a: int, b: int) -> int:
    """THE PERIOD BY THE ONE-NODE RULE (ALGEBRA.md 9.118 item 2 (a)): the clock a / b = 2 cos
    omega; the rotation c_t = cos(t omega) by the rule's own recurrence; P the first t from 1
    with some c_s < 0 before it, c_t >= 0 and c_t^2 >= (2 b + a) / (4 b), that is cos(t omega)
    >= cos(omega / 2): the nearest integer to 2 pi / omega, exactly (a tie excepted)."""
    if b < 1 or not -2 * b < a < 2 * b:
        raise ValueError(f"the clock [{a}, {b}] is no rotation: b from 1 and |a| below 2 b")
    ratio = Fraction(a, b)
    half_squared = Fraction(2 * b + a, 4 * b)
    before, now = Fraction(1), ratio / 2
    seen_negative = now < 0
    t = 1
    while t <= RETURN_LIMIT:
        if seen_negative and now >= 0 and now * now >= half_squared:
            return t
        before, now = now, ratio * now - before
        t += 1
        if now < 0:
            seen_negative = True
    raise ValueError(f"the clock [{a}, {b}] returns within no {RETURN_LIMIT} intervals")


def vacuum_profile(
    document: dict[str, Any], number: int, amplitude: int
) -> tuple[list[int], tuple[int, int], int]:
    """The profile by the rule at the vacuum's pace, today's (record 1898): the iteration
    with the stop, from the parsed document; the profile (x-major), the clock and the
    iterations taken."""
    world = parse_nature_beam_world(document)
    flat, clock, iterations = iterated_mode(world, number, amplitude)
    return [int(v) for v in flat], (int(clock[0]), int(clock[1])), int(iterations)


@dataclass(frozen=True)
class RunRuleReading:
    """The reading of 9.118 item 3 on one shipped body: its clock; the content at its
    Nodes; the mode's 2 cos omega as the exact quotient under the vacuum's rule and under
    the run's; the run's shift in units of b; the file's clock against the vacuum's quotient
    in units of b; the worst residual ratio of the file's profile under each rule."""

    clock: tuple[int, int]
    content_at_body: int
    two_cos_omega_vacuum: Fraction
    two_cos_omega_run: Fraction
    shift_in_units_of_b: Fraction
    file_clock_minus_vacuum_in_units_of_b: Fraction
    worst_residual_ratio_vacuum: Fraction
    worst_residual_ratio_run: Fraction


def run_rule_reading(document: dict[str, Any], number: int) -> RunRuleReading:
    """THE FINDING OF 9.118 ITEM 3, read on a shipped body: the profile p and the clock
    [a, b] of the file; the engine's integers (R, S, w) at every Node under the run's own
    pace (the content the body's family reads at load, `_effective_content`); the run's
    2 cos omega as the exact quotient (p . (R S_6 p + S p)) / (p . w p); the vacuum's as the
    same quotient at c = 0; their difference in units of b; and the worst residual of the
    file's profile under the run's integers against the vacuum's, as a ratio."""
    world = parse_nature_beam_world(document)
    simulation = DetectorLawSimulation(world)
    block = simulation.block_by_number[number]
    definition = world.measured[number].block
    assert definition is not None and definition.profile is not None
    a, b = (int(value) for value in definition.clock)
    shape = simulation.shape
    wrap = world.kind_periodic(world.measured[number].family)
    # the family's kind everywhere, the body's pair at its Nodes (as the loader reads them)
    kind = definition.kind
    num = np.full(shape, int(kind[0]), dtype=object)
    den = np.full(shape, int(kind[1]), dtype=object)
    corner = tuple(int(c) for c in world.measured[number].position)
    for index in body_node_indices(shape, corner, definition.extents, wrap):
        num.ravel()[index] = int(definition.pair[0])
        den.ravel()[index] = int(definition.pair[1])
    p = np.array(list(definition.profile), dtype=object).reshape(shape)
    six = np.array(six_neighbours_flat(list(definition.profile), shape, wrap), dtype=object).reshape(
        shape
    )
    gamma = simulation.node_clock
    content = simulation._effective_content(block.family)
    quotients: dict[str, Fraction] = {}
    residuals: dict[str, Fraction] = {}
    for word, c in (("vacuum", 0 * content), ("run", content)):
        read, self_coefficient, wall = rule_coefficients(num, den, gamma, c.astype(object), True)
        image = read * six + self_coefficient * p
        quotients[word] = Fraction(int(np.sum(p * image)), int(np.sum(wall * p * p)))
        residual = np.abs(b * image - wall * a * p)
        scale = b * (3 * read + np.abs(self_coefficient)) + wall * b
        residuals[word] = max(
            Fraction(int(r), int(s)) for r, s in zip(residual.ravel(), scale.ravel(), strict=True)
        )
    return RunRuleReading(
        (a, b),
        int(np.max(content[block.mask])),
        quotients["vacuum"],
        quotients["run"],
        (quotients["run"] - quotients["vacuum"]) * b,
        (Fraction(a, b) - quotients["vacuum"]) * b,
        residuals["vacuum"],
        residuals["run"],
    )


def check_world(path: Path) -> list[str]:
    """One line per seeded body of the world: the period by the rule against the file's,
    and the run's rule's shift of the mode (9.118 items 2 (a) and 3)."""
    document = json.loads(path.read_text(encoding="utf-8"))
    lines: list[str] = []
    if not isinstance(document, dict) or "measured" not in document:
        return [f"{path.name}: no world (no `measured`); skipped"]
    try:
        parse_nature_beam_world(document)
    except ValueError as refusal:
        return [f"{path.name}: the loader refuses it ({refusal}); skipped"]
    for number, entry in enumerate(document.get("measured", [])):
        if "clock" not in entry or "seed" not in entry:
            continue
        a, b = (int(value) for value in entry["clock"])
        period = period_by_the_rule(a, b)
        words = [f"{path.name} measured[{number}]: clock [{a}, {b}], the period by the rule {period}"]
        emitter = entry.get("emitter")
        if isinstance(emitter, dict) and "period" in emitter:
            verdict = "the same" if int(emitter["period"]) == period else "DIFFERS"
            words.append(f"the file's {emitter['period']} ({verdict})")
        reading = run_rule_reading(document, number)
        words.append(
            f"the content at the body {reading.content_at_body}; the run's rule shifts 2 cos omega by "
            f"{float(reading.shift_in_units_of_b):.3f} units of b; the file's profile's worst residual "
            f"ratio {float(reading.worst_residual_ratio_vacuum):.3f} (vacuum) against "
            f"{float(reading.worst_residual_ratio_run):.3f} (the run's rule)"
        )
        lines.append("; ".join(words))
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="the generator by the rule: check a world's bodies")
    parser.add_argument("worlds", nargs="+", type=Path)
    arguments = parser.parse_args()
    for path in arguments.worlds:
        for line in check_world(path):
            print(line)


if __name__ == "__main__":
    main()
