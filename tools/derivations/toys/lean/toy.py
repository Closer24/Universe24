"""The toy's measurement controls over the engine's Node, kept by name (the fold of 2026-10-25: the engine refuses the `control` and `detectors` keys; this subclass reads them): `ride` absent runs the former interval (one loop over the rows at the fixed wall, the metric's write from the forms) in place of the symmetric ride; `digits` former or folded changes the one-Link read's digit set; `metric_sources` names the rows whose form sources the metric's write in the former loop; `well` holds the volume by hand; `detectors` names the Nodes whose gap-0 quanta the record credits. Usage: `python toy.py <world.json> <out.json> [back N]`."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import readings, run
from event_universe.core import paces, rule3
from event_universe.core.ports import PORTS, across
from event_universe.core.rule3 import half
from event_universe.features import volume
from event_universe.links import plane_current, stress_parts, tensor_parts, wronskian
from event_universe.loader.world import read_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE, POTENTIAL, TRACE, Line, zeros

AXES = 3
CONTROLS = ("control", "detectors")


def load_toy_world(path: str | Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """The two files with the toy's keys allowed: the engine's loader reads the rest."""
    where = Path(path)
    world = json.loads(where.read_text(encoding="utf-8"))
    universe = json.loads((where.parent / world["universe"]).read_text(encoding="utf-8"))
    read_world({k: v for k, v in world.items() if k not in CONTROLS}, universe)
    return universe, world


class Toy(Node):
    """The engine's Node with the toy's controls."""

    def __init__(self, universe: dict[str, Any], world: dict[str, Any]) -> None:
        self.control: dict[str, Any] = world.get("control", {})
        self.hold_volume = False
        self.detectors: list[tuple[int, ...]] = []
        super().__init__(universe, {k: v for k, v in world.items() if k not in CONTROLS})
        self.counts["light_credits"] = 0
        well = self.control.get("well")
        if well:
            at = self.node_of(well["at"])
            levels, radius = int(well["levels"]), int(well["radius"])
            self.hold_volume = bool(well.get("held", False))
            m = self.row(CARRIER).lines[0]
            for node in np.ndindex(*self.shape):
                r2 = sum(
                    min(abs(node[a] - at[a]), self.cube - abs(node[a] - at[a])) ** 2 for a in range(AXES)
                )
                if r2 < radius * radius:
                    c = levels * (radius * radius - r2) // (radius * radius)
                    level = volume.volume_of(self.gamma, np.array([c], dtype=object))
                    m.now[node] = int(np.asarray(level, dtype=object).reshape(-1)[0])
                    m.before[node] = m.now[node]
        self.detectors = [self.node_of(d) for d in world.get("detectors", [])]
        if (
            self.control.get("ride") != "symmetric"
        ):  # the former loop: every line's remainder at the fixed wall w
            for r in self.rows_:
                if r.wall is None and r.shape != CARRIER:
                    for line in r.lines:
                        line.wall, line.rem = self.w, zeros(self.shape) + half(self.w)

    def carried(
        self,
        lines: list[Line],
        r: rule3.Rule,
        numerators: list[Any],
        direction: int,
        top: Any,
        kept: list[Line] | None,
    ) -> list[Line]:
        """The carrier's act, or the carrier held by hand (the well's `held`)."""
        return lines if self.hold_volume else super().carried(lines, r, numerators, direction, top, kept)

    def read_lines(
        self, held: list[list[Line]], plane_starts: list[list[Line]], c: Any, factors: tuple[Any, ...]
    ) -> list[tuple[Line, rule3.Rule]]:
        """The digit set: the former (the shape-4 and shape-10 rows' first lines after the step, the planes' lines at the start) under the key, else the engine's."""
        if self.control.get("digits") != "former":
            return super().read_lines(held, plane_starts, c, factors)
        rules = [
            (r.lines[0], self.rule_of(r, c, factors)) for r in (self.row(POTENTIAL), self.row(CARRIER))
        ]
        for rec, r in enumerate(self.records()):
            rules += [(line, self.rule_of(r, c, factors)) for line in plane_starts[rec]]
        return rules

    def digit_of(self, rem: int, values: int) -> tuple[int, int]:
        """The folded digit under the key: every remainder's distance to the nearer edge of its wall, conjugation-even on every line alike."""
        if self.control.get("digits") != "folded":
            return rem, values
        wall = values  # the lattice's values, the wall over its step
        return min(rem, wall - rem), wall // 2 + 1

    def click(self, plane_starts: list[list[Line]], held: list[list[Line]]) -> None:
        """The engine's close, then the detectors' reading."""
        super().click(plane_starts, held)
        if not self.detectors:
            return
        c = self.start_content
        gap0 = self.row(PLANE, gap=0)
        r_gap0 = self.rule_of(gap0, c, self.link_factors())
        pace = paces.link_pace_of(self.gamma, c)
        z = gap0.lines[0]
        gap0_start = plane_starts[self.records().index(gap0)]
        sh_end, sh_vac = (
            self.share(z, r_gap0, pace, vacuum=True),
            self.share(gap0_start[0], r_gap0, pace, vacuum=True),
        )
        for det in self.detectors:
            rise = int(sh_end[det]) // self.unit_gap0 - int(sh_vac[det]) // self.unit_gap0
            if rise > 0:
                self.counts["light_credits"] += rise
                self.log.append(
                    {
                        "event": "detector",
                        "i": self.interval,
                        "node": list(det),
                        "line": self.records().index(gap0),
                        "quanta": rise,
                        "proper": int(self.proper[det]),
                        "content": int(c[det]),
                        "light_now": int(z.now[det]),
                        "light_before": int(z.before[det]),
                    }
                )

    def run(self, direction: int = 1) -> None:
        """The symmetric ride under the key, else the former loop."""
        if self.control.get("ride") == "symmetric":
            return super().run(direction)
        self.former(direction)

    def former(self, direction: int) -> None:
        """The former interval: the readings at the start, one act on every row in the rows' order at the fixed wall (the walled row with its write inside the division, a plane with a gap turned by the Link's pair and the odd tangent, the plane at the gap 0 taking W-S1, the shape-4 row 2 W and the current, the metric's row the riding rows' forms less the pressure and the traceless stress), the swap and the close."""
        if direction == 1:
            self.interval += 1
            top: Any = np.zeros(self.shape, dtype=bool)
            kept = None
        else:
            frame = self.stack.pop()
            self.unclick(frame)
            top = frame["turned"]
        held = [[line.copy() for line in row] for row in self.rows()]
        if direction == -1:
            if top.any():
                self.exchange(top, held)
            kept = [[line.copy() for line in row] for row in self.rows()]

        def at(line: Line) -> Any:
            return line.now if direction == 1 else np.where(top, line.now, line.before)

        rows = self.rows()
        metric, walled, potential = self.row(CARRIER), self.walled(), self.row(POTENTIAL)
        c = np.asarray(volume.level_of(self.gamma, at(metric.lines[0])), dtype=object)
        self.start_content = c
        p0 = paces.clock_of(self.gamma, c)
        self.proper = self.proper + direction * p0
        factors = self.link_factors([at(line) for line in metric.lines[1 : 1 + AXES]])
        self.start_factors = factors
        frames = readings.frames(self, walled.lines[0].rem)
        self.start_frames = frames
        cphi = paces.rounded(at(potential.lines[0]) * p0, self.gamma)
        out: list[list[Line]] = [[] for _ in rows]
        riding = self.records() + (
            [potential] if self.control.get("metric_sources") == "every riding row" else []
        )
        trace, traceless = tensor_parts(
            stress_parts(
                [(at(line), r.pair[0]) for r in riding if r.pair for line in r.lines], self.shape
            )
        )
        forms, w_start, w_after = zeros(self.shape), zeros(self.shape), zeros(self.shape)
        current = [zeros(self.shape) for _ in range(AXES)]
        plane_starts: list[list[Line]] = []
        stepped: list[list[Line]] = []
        phases: Any = None
        odd: Any = None
        for k, r in enumerate(self.rows_):
            rule = self.rule_of(r, c, factors)
            turn = None
            flux = None
            numerators: list[Any] = [None] * r.shape
            if r.wall is not None:
                flux = [2 * cphi]
            elif r.shape == PLANE:
                turn = None if r.gap == 0 else (phases, odd, frames)
                if r.gap == 0:
                    numerators = [w_after - w_start, None]
            elif r.shape == POTENTIAL:
                numerators = [2 * w_after, *current]
            elif r.shape == CARRIER:
                if self.hold_volume:
                    out[k] = rows[k]
                    continue
                x, p02 = at(r.lines[0]), p0 * p0
                numerators = [4 * x * (forms * TRACE * self.den * self.gamma**2 - trace * p02) * p0]
                numerators += [traceless[a] * p02 for a in range(AXES)] + [None] * (r.shape - 1 - AXES)
            ends = (top, None if kept is None else kept[k])
            start, levels, out[k] = self.act(rows[k], rule, turn, numerators, direction, flux, *ends)
            if r in riding:
                for l0, lv in zip(start, levels, strict=True):
                    forms = forms + (l0.now * l0.now - lv * l0.before)
            if r.wall is not None:
                count = readings.centred_count(self, cphi, start[0])
                self.count_max = max(
                    int(abs(int(x)))
                    for port in range(PORTS)
                    for x in (count - frames[port] * across(count, port)).reshape(-1)
                )
                phases = readings.link_phases(self, frames, count)
                odd = [at(line) for line in potential.lines[1 : 1 + AXES]]
                self.start_phases, self.start_odd = phases, [o.copy() for o in odd]
            elif r.shape == PLANE:
                re, im = start
                w_start = w_start + wronskian(re, im)
                after = out[k] if direction == 1 else held[k]
                w_after = w_after + wronskian(*after)
                stepped.append([line.copy() for line in after])
                plane_starts.append(start)
                for a, j_a in enumerate(plane_current(re, im, frames)):
                    current[a] = current[a] + j_a
                if r.gap == 0 and direction == 1:
                    laid = out[k][0].now - levels[0]
                    self.counts["laid"] += int(sum(abs(int(x)) for x in laid.reshape(-1)))
                    self.counts["laid_nodes"] += int(sum(1 for x in laid.reshape(-1) if int(x) != 0))
        self.stepped = stepped
        self.set_rows(out)
        if direction == -1:
            self.interval -= 1
            return
        counters = (
            [a.copy() for a in self.standing],
            [a.copy() for a in self.crossed],
            [a.copy() for a in self.beats],
        )
        top = self.swap(held)
        log_from = len(self.log)
        self.click(plane_starts, held)
        self.stack.append({"turned": top, "counters": counters, "log_from": log_from})


def main(argv: list[str]) -> None:
    """The toy's writer: the engine's record with the toy's Node."""
    sys.set_int_max_str_digits(0)
    universe, world = load_toy_world(argv[1])
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    run.Node = Toy  # type: ignore[misc]
    found = run.record(universe, world, back, lambda line: print(line, flush=True))
    found["counts"]["light_credits"] = (
        str(Toy.light_credits) if False else found["counts"].get("light_credits", "0")
    )
    with open(argv[2], "w", encoding="utf-8") as out:
        json.dump(found, out)


if __name__ == "__main__":
    main(sys.argv)
