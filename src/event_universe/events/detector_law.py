"""The local detector law (`detector-law-v1`; the model owner's words of
2026-09-23, docs/designs/detector_law/DESIGN.md): the ray splits at every
free Node inside the board and holds its amplitudes; outside there is no
board, only clicks, and nothing passes from Node to Node except through a
detector, at rest or moving. Selected by the world key `detector_law`,
beside the ray law as built, which stays the default.

The Inside (DESIGN.md sections 1 and 2): a record's row at a Node holds
its amplitude now `a_now`, its amplitude one interval ago `a_before`
(integers on the record's wheel, the amplitude unit 2^20) and a
remainder `r`; every interval, at every Node with a row of the record,

    3 a_next + r' = (a_E + a_W + a_N + a_S + a_U + a_D) - 3 a_before + r,  0 <= r' < 3

(the group-ring addition over the six neighbours, verb G, and the
Euclidean division by 3 with the remainder kept on the record's row, verb
D; the pair [1, 3] of the exact square its only constant; a periodic axis
wraps, an open face is a declared wall that is not read). A record is
kept as dense arrays over the board (the first build; the record's rows
are the Nodes it has reached, the rest zero), one record per birth.

The Outside (DESIGN.md sections 1 and 5): two things only on the board,
the free Node and the receiver-inserter. A measured event with a lamp
INSERTS: each birth is a record driven at the lamp's Nodes by the
family's clock (the pair `phase_per_link` [n, d] on the circle of N steps)
for the lamp's train (the key `train`, in periods); the lamp pays the
family's quantum h at the birth. Every measured event's Nodes, every
detector set's Nodes and every open face's layer RECEIVE: the offer
`a_next^2` arriving at such a Node is added to the record's pointer for
that cell (a measured event's own cell `measured:<number>`, a set's cell
by the set's name, a face's `face:<axis>`), and the Node's amplitude is
taken (0 re-emitted). The record completes when its train has ended and
its offer on the board has been exhausted into the cells (below one rung
of the wheel of what the cells hold); the click's cell is chosen by
`cell_of` over the pointers on the record's wheel (the counting form,
record 1288; `amplitude.cell_of`), one click per record; the click line
(`gather`, the amplitude law's keys, with `clock` the detector's own count
and `birth` the record's birth stamp) is written, the record's content h
handed to the measured event at the chosen Node (or booked as escaped at a
face or a set without a body), and the record's rows removed. The books
balance as today: held content initial + measured == current + spent +
escaped; transit released == current + absorbed + escaped.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field

import numpy as np

from event_universe.core.phase import PHASE_COSINE_SCALE, phase_cosines
from event_universe.events.amplitude import cell_of, rungs
from event_universe.events.world import BEAM_LAW, NatureBeamWorld

Record = Callable[[dict[str, object]], None]

DETECTOR_LAW_RULE = "detector-law-v1"
UNIT = 1 << 20  # the amplitude unit (the wheel's resolution)
FACE_NAMES = ("face:-x", "face:+x", "face:-y", "face:+y", "face:-z", "face:+z")
DEFAULT_TRAIN = 32  # periods of the record's clock (DESIGN.md section 6.2)
# The receiver's take (DESIGN.md sections 1 and 5): a Node that receives does
# not send the wave back (a mirror is a receiver body that re-emits, never a
# wall). The record's row at a receiver holds one amplitude per Port that
# faces a free Node (the NodeState's Ports), the wave entering by that Port,
# following it one way: g(t + 1) = a_f(t) + k (a_f(t + 1) - g(t)) with a_f
# the free neighbour's amplitude and k = (c - 1) / (c + 1) at c = 1 / sqrt 3,
# the declared pair [-15, 56] (-0.2679 against sqrt 3 - 2 = -0.2679), a
# rounding declared at load, not a root at run time; the free neighbour reads
# g as the receiver's amplitude on that Link, and the receiver books g^2 as
# the offer arriving by that Port.
TAKE_NUMERATOR = -15
TAKE_DENOMINATOR = 56


@dataclass
class LiveRecord:
    """One record on the board: its dense rows and its ledger."""

    identity: int
    lamp: int
    family: int
    u: int
    born: int
    birth_tick: int
    content: int
    period_numerator: int
    period_denominator: int
    train: int
    period: int
    now: np.ndarray
    before: np.ndarray
    remainder: np.ndarray
    age: int = 0
    pointers: list[int] = field(default_factory=list)
    absorbed: int = 0
    norm: int = 0
    first_rung: list[int | None] = field(default_factory=list)
    ports: list[np.ndarray] = field(default_factory=list)
    driven: np.ndarray | None = None


@dataclass
class Ledger:
    """The books per family (Python integers, exact)."""

    held_initial: list[int]
    held_measured: list[int]
    held_spent: list[int]
    held_escaped: list[int]
    transit_released: list[int]
    transit_absorbed: list[int]
    transit_escaped: list[int]

    def escaped_amount(self, family: int) -> int:
        return self.transit_escaped[family]

    def escaped_content(self, family: int) -> int:
        return self.transit_escaped[family]

    def escaped_momentum(self, family: int) -> list[int]:
        return [0, 0, 0]


class DetectorLawLayer:
    """The record's lines the runner writes into run.json (the amplitude law's shape)."""

    def __init__(self) -> None:
        self.gathers: list[dict[str, object]] = []
        self.born = 0
        self.gathered = 0

    def open_records(self) -> list[dict[str, object]]:
        return []

    def report(self) -> dict[str, object]:
        return {"law": DETECTOR_LAW_RULE, "born": self.born, "gathered": self.gathered, "open": 0}


class DetectorLawSimulation:
    """One world under the local detector law, stepped interval by interval."""

    def __init__(self, world: NatureBeamWorld, observer: Record | None = None) -> None:
        if not world.detector_law:
            raise ValueError(f"{BEAM_LAW}: the world does not declare detector_law")
        self.world = world
        self.record = observer
        self.tick = 0
        self.shape = tuple(int(n) for n in world.shape)
        self.families = world.families
        self.fast_steps = 0
        self.hypotheses = list(world.hypotheses)
        self.layer = DetectorLawLayer()
        count = len(world.families)
        self.held: list[list[int]] = [
            list(entry.held) + [0] * (count - len(entry.held)) for entry in world.measured
        ]
        self.ledger = Ledger(
            [sum(h[f] for h in self.held) for f in range(count)],
            [0] * count,
            [0] * count,
            [0] * count,
            [0] * count,
            [0] * count,
            [0] * count,
        )
        # The cells: index 0 .. K - 1 with a name, the Nodes of each, and the
        # measured event (if any) that receives the content of a click there.
        self.cell_names: list[str] = []
        self.cell_measured: list[int | None] = []
        self.cell_face: list[bool] = []
        self.cell_index = np.full(self.shape, -1, dtype=np.int64)
        self.absorbing = np.zeros(self.shape, dtype=bool)
        self.lamp_nodes: dict[int, list[tuple[int, int, int]]] = {}
        self.lamp_accumulator: dict[int, int] = {}
        self.lamp_births: dict[int, int] = {}
        for number, entry in enumerate(world.measured):
            nodes = self._span_nodes(entry.position, entry.span)
            if entry.lamp is not None:
                self.lamp_nodes[number] = nodes
                self.lamp_accumulator[number] = 0
                self.lamp_births[number] = 0
            own = self._cell(f"measured:{number}", number, False)
            for node in nodes:
                self.cell_index[node] = own
                self.absorbing[node] = True
        for detector in world.detectors:
            set_cell: int | None = None
            for position in detector.positions:
                node = (int(position[0]), int(position[1]), int(position[2]))
                existing = int(self.cell_index[node])
                measured = self.cell_measured[existing] if existing >= 0 else None
                if set_cell is None:
                    set_cell = self._cell(detector.name, measured, False)
                elif measured is not None and self.cell_measured[set_cell] is None:
                    self.cell_measured[set_cell] = measured
                self.cell_index[node] = set_cell
                self.absorbing[node] = True
        for axis in range(3):
            if world.periodic[axis] or self.shape[axis] < 2:
                continue
            for side, index in ((0, 0), (1, self.shape[axis] - 1)):
                cell = self._cell(FACE_NAMES[2 * axis + side], None, True)
                view = np.moveaxis(self.cell_index, axis, 0)[index]
                mask = np.moveaxis(self.absorbing, axis, 0)[index]
                free = view < 0
                view[free] = cell
                mask[:] = True
        self.records: dict[int, LiveRecord] = {}
        self.wheel = max(
            (entry.lamp.wheel[1] for entry in world.measured if entry.lamp is not None), default=1
        )
        self.cosine: dict[int, np.ndarray] = {}
        # The receivers' free neighbours per direction (for the one-way take):
        # for each of the six shifts, the absorbing Nodes whose neighbour on
        # that side is a free Node.
        self.take_masks: list[tuple[int, int, np.ndarray]] = []
        free = ~self.absorbing
        for axis in range(3):
            if self.shape[axis] == 1:
                continue
            for sign in (1, -1):
                neighbour_free = self._shift(free, axis, sign, fill=False)
                mask = self.absorbing & neighbour_free
                if mask.any():
                    self.take_masks.append((axis, sign, mask))
        self.take_count = np.zeros(self.shape, dtype=np.int64)
        for _, _, mask in self.take_masks:
            self.take_count += mask

    def _cell(self, name: str, measured: int | None, face: bool) -> int:
        self.cell_names.append(name)
        self.cell_measured.append(measured)
        self.cell_face.append(face)
        return len(self.cell_names) - 1

    def _span_nodes(
        self, position: tuple[int, int, int], span: tuple[int, int, int]
    ) -> list[tuple[int, int, int]]:
        found: list[tuple[int, int, int]] = []
        for dx in range(int(span[0])):
            for dy in range(int(span[1])):
                for dz in range(int(span[2])):
                    node = (int(position[0]) + dx, int(position[1]) + dy, int(position[2]) + dz)
                    if all(0 <= node[a] < self.shape[a] for a in range(3)):
                        found.append(node)
        return found

    # The source

    def _cosine_table(self, steps: int) -> np.ndarray:
        """The clock's cosine on the amplitude unit: the phase circle's integer
        table (`core.phase.phase_cosines`, cos x 256, immutable law data)
        scaled to UNIT, formed once."""
        if steps not in self.cosine:
            factor = UNIT // PHASE_COSINE_SCALE
            self.cosine[steps] = np.array([c * factor for c in phase_cosines(steps)], dtype=np.int64)
        table: np.ndarray = self.cosine[steps]
        return table

    def _births(self) -> None:
        world = self.world
        for number in self.lamp_nodes:
            entry = world.measured[number]
            lamp = entry.lamp
            assert lamp is not None
            family = entry.family
            definition = world.families[family]
            cost = definition.quantum
            rate_numerator, rate_denominator = lamp.rate
            self.lamp_accumulator[number] += rate_numerator
            while (
                self.lamp_accumulator[number] >= rate_denominator and self.held[number][family] >= cost
            ):
                self.lamp_accumulator[number] -= rate_denominator
                ordinal = self.lamp_births[number] + 1
                self.lamp_births[number] = ordinal
                u = (ordinal - 1) * lamp.wheel[0] % lamp.wheel[1]
                identity = number * (1 << 32) + ordinal
                pair = definition.phase_per_age
                if pair is None:
                    raise ValueError(
                        f"{BEAM_LAW}: {DETECTOR_LAW_RULE} needs the pair form of phase_per_link on the family "
                        f"{definition.name!r} (its clock)"
                    )
                numerator, denominator = pair
                steps = world.phase_steps
                if steps % 4:
                    raise ValueError(
                        f"{BEAM_LAW}: {DETECTOR_LAW_RULE} needs N divisible by 4 (the clock's zero)"
                    )
                if numerator <= 0:
                    raise ValueError(
                        f"{BEAM_LAW}: {DETECTOR_LAW_RULE} needs a positive clock on the family {definition.name!r}"
                    )
                # The period in intervals, N d / n, its ceiling as an integer.
                period = (steps * denominator + numerator - 1) // numerator
                train_periods = lamp.train if lamp.train is not None else DEFAULT_TRAIN
                # The train begins at the clock's zero (the phase 3 N / 4, the
                # cosine 0 and rising) and ends at the first zero after the
                # declared periods, so that the insertion starts and stops
                # smoothly: a step in the inserted amplitude would leave a
                # static level on the board (the wave's zero-frequency mode),
                # which no receiver takes.
                train = max(1, (train_periods * steps * denominator + numerator - 1) // numerator)
                while self._phase(train, numerator, denominator, steps) not in (
                    steps // 4,
                    3 * steps // 4,
                ):
                    train += 1
                self.held[number][family] -= cost
                self.ledger.held_spent[family] += cost
                self.ledger.transit_released[family] += cost
                live = LiveRecord(
                    identity,
                    number,
                    family,
                    u,
                    ordinal,
                    self.tick,
                    cost,
                    numerator,
                    denominator,
                    train,
                    period,
                    np.zeros(self.shape, dtype=np.int64),
                    np.zeros(self.shape, dtype=np.int64),
                    np.zeros(self.shape, dtype=np.int64),
                    pointers=[0] * len(self.cell_names),
                    first_rung=[None] * len(self.cell_names),
                    ports=[np.zeros(self.shape, dtype=np.int64) for _ in self.take_masks],
                )
                driven = np.zeros(self.shape, dtype=bool)
                for node in self.lamp_nodes[number]:
                    driven[node] = True
                live.driven = driven
                # The record's norm: the offer its train inserts (the squared
                # amplitudes over the train at the lamp's Nodes), the wheel's
                # rungs divide it; the first rung of a cell is the click's time.
                table = self._cosine_table(world.phase_steps)
                # The record's norm: the motion its train inserts (the squared
                # steps of the driven amplitude over the train at the lamp's
                # Nodes); the wheel's rungs divide it, the first rung of a cell
                # is the click's time.
                values = [
                    int(table[self._phase(t, numerator, denominator, steps)]) for t in range(train + 1)
                ]
                values[-1] = 0
                live.norm = len(self.lamp_nodes[number]) * sum(
                    (values[t + 1] - values[t]) ** 2 for t in range(train)
                )
                self.records[identity] = live
                self.layer.born += 1
                if self.record is not None:
                    self.record(
                        {
                            "event": "birth",
                            "tick": self.tick,
                            "node": list(entry.position),
                            "measured": number,
                            "family": definition.name,
                            "record": identity,
                            "u": u,
                            "labels": [[0, 1]],
                            "arms": 1,
                            "units": 1,
                            "multiplicity": 1,
                            "train": train,
                            **({"clock": self.tick} if world.clock_stamp else {}),
                        }
                    )

    @staticmethod
    def _phase(age: int, numerator: int, denominator: int, steps: int) -> int:
        """The record's clock at its age: the zero (3 N / 4) advanced by the
        whole part of age x n / d on the circle of N steps."""
        return (3 * steps // 4 + age * numerator // denominator) % steps

    def _drive(self, live: LiveRecord) -> None:
        """The record's clock at the lamp's Nodes for the train."""
        if live.age >= live.train:
            return
        steps = self.world.phase_steps
        phase = self._phase(live.age, live.period_numerator, live.period_denominator, steps)
        value = int(self._cosine_table(steps)[phase])
        for node in self.lamp_nodes[live.lamp]:
            live.now[node] = value

    # The rule

    def _shift(self, a: np.ndarray, axis: int, sign: int, fill: int | bool = 0) -> np.ndarray:
        """The neighbour on the side `sign` of `axis`: the wrap on a periodic
        axis, `fill` beyond an open face."""
        if self.world.periodic[axis]:
            return np.roll(a, sign, axis=axis)
        out = np.full_like(a, fill)
        lower = [slice(None)] * 3
        upper = [slice(None)] * 3
        if sign > 0:
            lower[axis] = slice(1, None)
            upper[axis] = slice(None, -1)
        else:
            lower[axis] = slice(None, -1)
            upper[axis] = slice(1, None)
        out[tuple(lower)] = a[tuple(upper)]
        return out

    def _neighbours(
        self, a: np.ndarray, ports: list[np.ndarray] | None = None, driven: np.ndarray | None = None
    ) -> np.ndarray:
        """The sum of the six neighbours' amplitudes at every Node: the wrap on
        a periodic axis, 0 beyond an open face, the row itself on an axis of
        one layer; a receiver neighbour read through its Port's amplitude
        (`ports`, one per take mask) where one is given."""
        total = np.zeros_like(a)
        for axis in range(3):
            if self.shape[axis] == 1:
                total += 2 * a
                continue
            for sign in (1, -1):
                source = a
                if ports is not None:
                    for index, (mask_axis, mask_sign, mask) in enumerate(self.take_masks):
                        # The receiver r with a free neighbour on its -mask_sign side
                        # (the mask) is read by that neighbour as the +mask_sign
                        # neighbour of the free Node: the shift by -mask_sign.
                        if mask_axis == axis and mask_sign == -sign:
                            read = mask if driven is None else (mask & ~driven)
                            source = np.where(read, ports[index], source)
                total += self._shift(source, axis, sign)
        return total

    def _advance(self, live: LiveRecord) -> None:
        # The inserter's own Nodes are driven for the train and read their own
        # record only after its tail has left them (two periods after the
        # train; the first build's grace, DESIGN.md section 11): a receiver's
        # Port books the wave's motion beside it, and the tail leaving the
        # lamp is not an arrival.
        grace = live.train + 2 * live.period
        driven = live.driven if live.age < grace else None
        total = self._neighbours(live.now, live.ports, driven)
        total -= 3 * live.before
        total += live.remainder
        nxt = np.floor_divide(total, 3)
        live.remainder = total - 3 * nxt
        nxt[self.absorbing] = 0
        # The receivers: each Port facing a free Node follows the wave entering
        # by it one way (the take, no reflection); the offer booked to the cell
        # is the sum over the Ports of the squared Port amplitudes. The
        # record's own lamp is driven during its train and receives nothing
        # from that record then.
        offer = np.zeros(self.shape, dtype=np.int64)
        for index, (axis, sign, mask) in enumerate(self.take_masks):
            free_now = self._shift(live.now, axis, sign)
            free_next = self._shift(nxt, axis, sign)
            ghost = np.floor_divide(
                TAKE_DENOMINATOR * free_now + TAKE_NUMERATOR * (free_next - live.ports[index]),
                TAKE_DENOMINATOR,
            )
            ghost = np.where(mask if driven is None else (mask & ~driven), ghost, 0)
            # The offer arriving by the Port is the Port's motion, (g(t + 1) -
            # g(t))^2: a wave moves the receiver, a static level on the board
            # (the rule's zero-frequency mode, which no receiver takes and
            # which carries nothing) does not.
            motion = ghost - live.ports[index]
            live.ports[index] = ghost
            offer += motion * motion
        live.before = live.now
        offer = offer[self.absorbing]
        cells = self.cell_index[self.absorbing]
        if live.age < grace:
            own = self.cell_index[tuple(zip(*self.lamp_nodes[live.lamp], strict=True))]
            keep = ~np.isin(cells, own)
            offer = offer[keep]
            cells = cells[keep]
        squares = offer.astype(object)
        for cell, value in zip(cells.tolist(), squares.tolist(), strict=True):
            if value:
                live.pointers[cell] += int(value)
                live.absorbed += int(value)
                if live.first_rung[cell] is None and live.pointers[cell] * self.wheel >= live.norm:
                    live.first_rung[cell] = self.tick
        live.now = nxt
        self._drive(live)
        live.age += 1

    def _complete(self, live: LiveRecord) -> bool:
        """The record completes when its train has ended and the motion left on
        the board (the squared steps of every row, the wave's energy in the
        rule's own terms; a static level moves nothing) is below one rung of
        what the receivers hold."""
        if live.age <= live.train:
            return False
        motion = (live.now - live.before).astype(object)
        energy = int(np.sum(motion * motion))
        if live.absorbed == 0:
            return energy == 0 and live.age > live.train + 2
        return energy * self.wheel < live.absorbed

    def _click(self, live: LiveRecord) -> None:
        weights = [(p, 1) for p in live.pointers]
        chosen = cell_of(weights, self.wheel, live.u) if live.absorbed else None
        family = live.family
        ladder, total = rungs(weights, self.wheel)
        if chosen is None:
            self.ledger.transit_escaped[family] += live.content
            self.ledger.held_escaped[family] += 0
            name = None
        else:
            name = self.cell_names[chosen]
            measured = self.cell_measured[chosen]
            if measured is not None and not self.cell_face[chosen]:
                self.held[measured][family] += live.content
                self.ledger.held_measured[family] += live.content
                self.ledger.transit_absorbed[family] += live.content
            else:
                self.ledger.transit_escaped[family] += live.content
        self.layer.gathered += 1
        gather: dict[str, object] = {
            "event": "gather",
            "tick": self.tick,
            "arrived": self.tick,
            "family": self.families[family].name,
            "record": live.identity,
            "u": live.u,
            "born": live.born,
            "chosen": [[name, 0, "0"]] if name is not None else None,
            "node": [],
            "windows": [],
            "content": live.content,
            "momentum": [0, 0, 0],
            "weight": [live.pointers[chosen] if chosen is not None else 0, 1],
            "total": list(total),
            "unit": UNIT,
            "T": live.absorbed,
            "before": sum(1 for p in live.pointers if p),
            "after": 1 if chosen is not None else 0,
            "cells": [
                [[[cell_name, 0, "0"]], rung]
                for cell_name, rung, pointer in zip(self.cell_names, ladder, live.pointers, strict=True)
                if pointer
            ],
            "birth": live.birth_tick,
            # The click's time: the interval at which the chosen cell's pointer
            # crossed its first rung (the counting form, s_D = 1 / W), the
            # detector's own count on the click line; the record completed at
            # `tick`, when its offer was exhausted.
            "click": (
                live.first_rung[chosen]
                if chosen is not None and live.first_rung[chosen] is not None
                else self.tick
            ),
            **(
                {
                    "clock": (
                        live.first_rung[chosen]
                        if chosen is not None and live.first_rung[chosen] is not None
                        else self.tick
                    )
                }
                if self.world.clock_stamp
                else {}
            ),
        }
        self.layer.gathers.append(gather)
        if self.record is not None:
            self.record(gather)

    def step(self) -> None:
        self.tick += 1
        self._births()
        for identity in list(self.records):
            live = self.records[identity]
            self._advance(live)
            if self._complete(live):
                self._click(live)
                del self.records[identity]

    # The readings

    def books(self, recount: bool = False) -> dict[str, object]:
        families: dict[str, object] = {}
        balanced = True
        ledger = self.ledger
        for index, family in enumerate(self.families):
            current = sum(h[index] for h in self.held)
            measured = {
                "initial": ledger.held_initial[index],
                "measured": ledger.held_measured[index],
                "became": 0,
                "current": current,
                "spent": ledger.held_spent[index],
                "escaped": ledger.held_escaped[index],
            }
            measured["balanced"] = measured["initial"] + measured["measured"] == (
                measured["current"] + measured["spent"] + measured["escaped"]
            )
            transit_current = sum(live.content for live in self.records.values() if live.family == index)
            transit = {
                "initial": 0,
                "released": ledger.transit_released[index],
                "current": transit_current,
                "absorbed": ledger.transit_absorbed[index],
                "escaped": ledger.transit_escaped[index],
            }
            transit["balanced"] = transit["released"] == (
                transit["current"] + transit["absorbed"] + transit["escaped"]
            )
            balanced = balanced and bool(measured["balanced"]) and bool(transit["balanced"])
            families[family.name] = {"measured": measured, "transit": transit}
        return {
            "tick": self.tick,
            "families": families,
            "momentum": {"held": [0, 0, 0], "transit": [0, 0, 0], "escaped": [0, 0, 0]},
            "records": len(self.records),
            "balanced": balanced,
        }

    def contents(self) -> list[dict[str, object]]:
        return [
            {
                "number": number,
                "position": list(entry.position),
                "family": self.families[entry.family].name,
                "held": list(self.held[number]),
            }
            for number, entry in enumerate(self.world.measured)
        ]

    def detectors(self) -> list[dict[str, object]]:
        found = []
        for detector in self.world.detectors:
            clicks = 0
            for gather in self.layer.gathers:
                chosen = gather["chosen"]
                if isinstance(chosen, list) and chosen and chosen[0][0] == detector.name:
                    clicks += 1
            found.append(
                {
                    "name": detector.name,
                    "positions": [list(p) for p in detector.positions],
                    "clicks": clicks,
                }
            )
        return found

    def covariant_report(self) -> dict[str, object]:
        return {}

    def snapshot_stream(self) -> Iterator[tuple[str, object]]:
        """The state's (key, value) pairs for state.json: the law, the tick,
        the held content per measured event and the live records (their
        identity, age, train and the cells' pointers), not their rows."""
        yield "law", DETECTOR_LAW_RULE
        yield "tick", self.tick
        yield "measured", self.contents()
        yield (
            "records",
            [
                {
                    "record": live.identity,
                    "lamp": live.lamp,
                    "family": self.families[live.family].name,
                    "u": live.u,
                    "born": live.born,
                    "birth": live.birth_tick,
                    "age": live.age,
                    "train": live.train,
                    "norm": live.norm,
                    "absorbed": live.absorbed,
                    "pointers": dict(zip(self.cell_names, live.pointers, strict=True)),
                }
                for live in self.records.values()
            ],
        )
