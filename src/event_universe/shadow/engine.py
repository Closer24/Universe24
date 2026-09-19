"""The engine of the law of the shadow (field-only-v1): held contents, the
shadow layers and the interval.

Only shadows and events (the model owner, 2026-09-18, the evening): every ray
on the board is a shadow, a whole quantum of a family in flight, moving one
Link per interval and spreading by the Node's mixing; an event is a whole
quantum at a Node that holds content, where it is read, kept or released
again by the holder's table; from the event the shadows spread. Matter is
content held at Nodes (`Holder`): an amount per family, a momentum with its
three accumulators, a phase, a number, a whole charge, a table. The interval
follows the Node rule of DERIVATIONS.md round 8, section 56 (S2 of section
51), in this order:

1. every shadow in flight moves one Link (`ShadowLayer.walk`; a paid
   family's phase turns by its amount over K, a matter shadow's does not),
   the escapes booked;
2. at every Node the size of the coherent sum of each number's arrivals is
   formed; a held content reads the sizes of the other numbers at its Node
   and owes one interval per whole unit at the world's `wait_per_quantum`
   (its clock, `Holder.owed`, a remainder carried); the quanta of a paid
   family in flight read the free families' sizes at the Node they cross
   and owe the same (`ShadowLayer.charge_wait`, a hold per Node);
3. a held content meets the whole quanta that arrive at its Node: its own
   number's are home, sunk for their amount alone and pooled to leave again
   with its release, pushing nothing (R13; round 8 sections 52 and 54);
   another number's are met by its table: `read` (the default for a free
   family: the push taken, the units left to mix on as at an empty Node),
   `keep` (the default for a paid family: the click, the push taken and the
   amount joining the holder's content), `rerelease` (the push taken, the
   amount pooled to leave again with the holder's release and number) or
   `pass` (no push, the units mix on);
4. at every Node the shadows of one number mix (node-mixing-v1), the
   remainders park and release, the departures go into flight;
5. a held content releases: per free family it holds, content x the world's
   `release` per Port with a remainder per Port; the pooled amount six-fold
   with a remainder; a lamp its paid family at its rate on its headings,
   spending its content; every release stamped with the holder's number and
   current phase; nothing in an interval it owes or in the interval after a
   step;
6. the holder's phase turns by its content over K with a remainder; each
   accumulator adds its component of the momentum (held at the content
   while a step is not allowed), and the first axis (x before y before z)
   whose accumulator has reached the content steps the content one Link
   that way, the accumulator giving back the content and the momentum
   untouched (section 53: Newton's first law by bookkeeping), at most once
   per interval and never in the interval after a step (T2: an event takes
   the interval); a step onto a held content merges the two into the
   resident (amounts, momentum and charge added, the resident's number,
   phase and table kept), a step off the board escapes; `fixed` never steps.

The readings (Highlights 5.4 point 16 as amended; round 8 S3): a unit of a
free family with heading h pushes by -M a h (gravity, toward the emitter,
the holder's content the cross-section) and by +(q_A / M_A) q a h
(electricity, the owner's whole charge over its declared content times the
holder's whole charge, kept exactly in units of 1 / D on the holder, D the
least common multiple of the charged contents' declared amounts); a unit of
a paid family pushes by +a h, its own momentum. A shadow carries no
momentum and no ledger of the field's momentum exists (S8): the momentum
lives on held content and changes only by the pushes, and the third law is
the symmetry of the two fields. The books, per family and interval: the
held line, initial + kept = current + spent (lamps) + escaped (contents off
the board); the shadows' line, initial + released = current + escaped +
absorbed (home, kept, re-released), exact at every interval.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field

import numpy as np

from event_universe.core.integer import signed_divrem
from event_universe.core.lattice import PORT_HEADINGS, Address3
from event_universe.shadow.layer import HEADINGS, ShadowLayer
from event_universe.shadow.mixing import MIXING_AMPLITUDE_SCALE
from event_universe.shadow.world import SHADOW_LAW, ContentDefinition, ShadowWorld

Record = Callable[[dict[str, object]], None]
ZERO3 = (0, 0, 0)
NO_MOMENTUM = np.zeros(3, dtype=np.int64)


@dataclass
class Holder:
    """A held content at a Node."""

    number: int
    position: Address3
    family: int
    held: list[int]
    phase: int
    charge: int
    momentum: list[int]
    fixed: bool
    table: tuple[str, ...]
    lamp_rate: tuple[int, int] | None
    lamp_headings: tuple[int, ...]
    declared_content: int
    # The accumulators of the step (one per axis), the remainders (the phase
    # below one step, the release per family and Port in d-ths, the lamp's
    # in d-ths, the pool's six-fold share per family, the electric push per
    # axis in 1 / D, the wait's debt in 1 / (32 d)), the intervals owed and
    # whether the content arrived by a step this interval (T2).
    accumulators: list[int] = field(default_factory=lambda: [0, 0, 0])
    phase_remainder: int = 0
    release_remainder: list[list[int]] = field(default_factory=list)
    lamp_remainder: int = 0
    pool: list[int] = field(default_factory=list)
    pool_remainder: list[int] = field(default_factory=list)
    push_remainder: list[int] = field(default_factory=lambda: [0, 0, 0])
    wait_debt: int = 0
    owed: int = 0
    arrived: bool = False
    # The counters: intervals waited, phase steps made, steps walked, per
    # family what was met by each rule, and the push taken.
    waited: int = 0
    phase_steps: int = 0
    steps: int = 0
    absorbed: list[dict[str, int]] = field(default_factory=list)
    pushed: list[int] = field(default_factory=lambda: [0, 0, 0])

    @property
    def content(self) -> int:
        return sum(self.held)

    def state(self) -> dict[str, object]:
        return {
            "number": self.number,
            "position": list(self.position),
            "family": self.family,
            "held": list(self.held),
            "content": self.content,
            "phase": self.phase,
            "charge": self.charge,
            "momentum": list(self.momentum),
            "accumulators": list(self.accumulators),
            "fixed": self.fixed,
            "owed": self.owed,
            "waited": self.waited,
            "phase_steps": self.phase_steps,
            "steps": self.steps,
            "absorbed": [dict(entry) for entry in self.absorbed],
            "pushed": list(self.pushed),
            "pool": list(self.pool),
        }


class ShadowSimulation:
    """One world of the law of the shadow, stepped interval by interval."""

    def __init__(self, world: ShadowWorld, observer: Record | None = None) -> None:
        self.world = world
        self.record = observer
        self.tick = 0
        self.shape = world.shape
        self.families = world.families
        count = len(world.families)
        self.layers = [
            ShadowLayer(
                index,
                world.shape,
                world.owners(index),
                world.phase_steps,
                world.clock,
                rotates=family.turns,
            )
            for index, family in enumerate(world.families)
        ]
        self.denominator = world.content_lcm()
        self.holders: dict[int, Holder] = {}
        self.at: dict[Address3, int] = {}
        for index, content in enumerate(world.contents):
            holder = self._holder(index + 1, content)
            self.holders[holder.number] = holder
            self.at[holder.position] = holder.number
        # The books (cumulative): per family the held line's initial, absorbed,
        # spent and escaped; the shadows' line's initial, released, absorbed;
        # the momentum's initial, escaped by contents and spent on steps.
        self.held_initial = [sum(h.held[f] for h in self.holders.values()) for f in range(count)]
        self.held_absorbed = [0] * count
        self.held_spent = [0] * count
        self.held_escaped = [0] * count
        self.shadow_initial = [0] * count
        self.shadow_released = [0] * count
        self.shadow_absorbed = [0] * count
        for shadow in world.initial_shadows:
            self._seed(
                shadow.position, shadow.family, shadow.number, shadow.port, shadow.amount, shadow.phase
            )
            self.shadow_initial[shadow.family] += shadow.amount
        # The readings of the last interval (diagnostics): per family the
        # arrivals per Node, their net flow and the sizes per Node and number.
        self.count: list[np.ndarray] = [np.zeros(world.shape, dtype=np.int64) for _ in range(count)]
        self.per_port: list[np.ndarray] = [
            np.zeros((*world.shape, 6), dtype=np.int64) for _ in range(count)
        ]
        self.flow: list[np.ndarray] = [np.zeros((*world.shape, 3), dtype=np.int64) for _ in range(count)]
        self.size: list[np.ndarray] = [
            np.zeros((*world.shape, len(layer.owners)), dtype=np.int64) for layer in self.layers
        ]

    def _holder(self, number: int, content: ContentDefinition) -> Holder:
        count = len(self.families)
        held = [0] * count
        held[content.family] = content.amount
        return Holder(
            number,
            content.position,
            content.family,
            held,
            content.phase,
            content.charge,
            list(content.momentum),
            content.fixed,
            content.table,
            None if content.lamp is None else content.lamp.rate,
            () if content.lamp is None else content.lamp.headings,
            content.amount,
            release_remainder=[[0] * 6 for _ in range(count)],
            pool=[0] * count,
            pool_remainder=[0] * count,
            absorbed=[{"home": 0, "read": 0, "keep": 0, "rerelease": 0} for _ in range(count)],
        )

    def _seed(
        self, position: Address3, family: int, number: int, port: int, amount: int, phase: int
    ) -> None:
        """A shadow given with the board: as an arrival at its Node on its
        travel heading, the arrivals of tick 0 that the first interval mixes."""
        layer = self.layers[family]
        cell = (*position, layer.rank[number], port)
        for index in range(layer.arr_amt.shape[-1]):
            if layer.arr_amt[(*cell, index)] == 0:
                layer.arr_amt[(*cell, index)] = amount
                layer.arr_ph[(*cell, index)] = phase
                return
        raise ValueError(f"{SHADOW_LAW}: more initial shadows on one lane than its layers")

    # -- the interval ----------------------------------------------------------

    def step(self) -> None:
        """One interval, in the order of the module docstring."""
        self.tick += 1
        world = self.world
        for layer in self.layers:
            layer.walk()
        # The readings: the sizes per Node and number, per family; the total
        # over families per number, over numbers per Node, and the free
        # families' total per Node (what light in flight reads).
        numbers = len(world.contents)
        size_by_number = np.zeros((*self.shape, numbers + 1), dtype=np.int64)
        free_size = np.zeros(self.shape, dtype=np.int64)
        for index, layer in enumerate(self.layers):
            self.count[index] = layer.count()
            self.per_port[index] = layer.arr_amt.sum(axis=(3, 5))
            self.flow[index] = self.per_port[index] @ HEADINGS
            sizes = layer.sizes() if layer.owners else np.zeros((*self.shape, 0), dtype=np.int64)
            self.size[index] = sizes
            for rank, number in enumerate(layer.owners):
                size_by_number[..., number] += sizes[..., rank]
            if self.families[index].free:
                free_size += sizes.sum(axis=-1)
        size_total = size_by_number.sum(axis=-1)
        # The wait of light in flight: a paid family's quanta read the free
        # families' sizes at the Node they cross.
        if world.wait[0]:
            for index, layer in enumerate(self.layers):
                if self.families[index].free or not layer.owners:
                    continue
                read = np.repeat(free_size[..., None], len(layer.owners), axis=-1)
                layer.charge_wait(read, world.wait[0], world.wait[1])
        # The events at the held contents and their wait, then the mixing.
        for number in sorted(self.holders):
            holder = self.holders[number]
            self._read_wait(holder, size_total, size_by_number)
            self._meet(holder)
        for layer in self.layers:
            layer.cycle()
        # The releases and the clocks; the steps last, in number order.
        for number in sorted(self.holders):
            self._release(self.holders[number])
        for number in sorted(self.holders):
            if number in self.holders:
                self._move(self.holders[number])

    def _read_wait(self, holder: Holder, size_total: np.ndarray, size_by_number: np.ndarray) -> None:
        numerator, denominator = self.world.wait
        if not numerator:
            return
        read = int(size_total[holder.position]) - int(size_by_number[(*holder.position, holder.number)])
        unit = MIXING_AMPLITUDE_SCALE * denominator
        debt = holder.wait_debt + read * numerator
        holder.owed += debt // unit
        holder.wait_debt = debt % unit

    def _meet(self, holder: Holder) -> None:
        """The events at a held content's Node: every arrival of its own
        number sunk for its amount, every other number's met by the table."""
        position = holder.position
        for index, layer in enumerate(self.layers):
            if not layer.owners:
                continue
            rule = holder.table[index]
            free = self.families[index].free
            for rank, number in enumerate(layer.owners):
                cell = (*position, rank)
                if not layer.arr_amt[cell].any():
                    continue
                if number == holder.number:
                    amounts, _, _ = layer.take(position, rank)
                    total = int(amounts.sum())
                    holder.pool[index] += total
                    holder.absorbed[index]["home"] += total
                    self.shadow_absorbed[index] += total
                    self._event("home", holder, index, number, total, ZERO3)
                    continue
                if rule == "pass":
                    continue
                per_port = layer.arr_amt[cell].sum(axis=-1)
                total = int(per_port.sum())
                push = self._push(holder, free, number, per_port)
                holder.momentum = [int(a) + int(b) for a, b in zip(holder.momentum, push, strict=True)]
                holder.pushed = [int(a) + int(b) for a, b in zip(holder.pushed, push, strict=True)]
                holder.absorbed[index][rule] += total
                if rule == "read":
                    self._event("read", holder, index, number, total, push)
                    continue
                layer.take(position, rank)
                self.shadow_absorbed[index] += total
                if rule == "keep":
                    holder.held[index] += total
                    self.held_absorbed[index] += total
                    self._event("click", holder, index, number, total, push)
                else:
                    holder.pool[index] += total
                    self._event("rerelease", holder, index, number, total, push)

    def _push(
        self, holder: Holder, free: bool, number: int, per_port: np.ndarray
    ) -> tuple[int, int, int]:
        """The push of the units of one number arriving at a holder, summed
        over the Ports: the gravity and the electric readings for a free
        family, the unit's own momentum for a paid one."""
        flux = [int(v) for v in per_port @ HEADINGS]
        if not free:
            return flux[0], flux[1], flux[2]
        content = holder.content
        push = [-flux[axis] * content for axis in range(3)]
        owner = self.world.contents[number - 1]
        if owner.charge and holder.charge:
            scale = owner.charge * holder.charge * (self.denominator // owner.amount)
            for axis in range(3):
                total = holder.push_remainder[axis] + flux[axis] * scale
                whole, rest = signed_divrem(total, self.denominator)
                holder.push_remainder[axis] = rest
                push[axis] += whole
        return push[0], push[1], push[2]

    def _release(self, holder: Holder) -> None:
        """The holder's releases of the interval and its clock, unless it owes
        or arrived by a step this interval."""
        if holder.owed > 0:
            holder.owed -= 1
            holder.waited += 1
            return
        if holder.arrived:
            return
        position = holder.position
        numerator, denominator = self.world.release
        for index, layer in enumerate(self.layers):
            if not layer.owners or holder.number not in layer.rank:
                continue
            own = layer.rank[holder.number]
            family = self.families[index]
            if family.free and holder.held[index] > 0:
                for port in range(6):
                    total = holder.release_remainder[index][port] + holder.held[index] * numerator
                    amount, holder.release_remainder[index][port] = divmod(total, denominator)
                    if amount:
                        layer.place(position, own, port, amount, holder.phase, NO_MOMENTUM)
                        self.shadow_released[index] += amount
            if holder.lamp_rate is not None and index == holder.family:
                rate_n, rate_d = holder.lamp_rate
                for port in holder.lamp_headings:
                    total = holder.lamp_remainder + rate_n
                    amount, holder.lamp_remainder = divmod(total, rate_d)
                    amount = min(amount, holder.held[index])
                    if amount:
                        layer.place(position, own, port, amount, holder.phase, NO_MOMENTUM)
                        holder.held[index] -= amount
                        self.shadow_released[index] += amount
                        self.held_spent[index] += amount
            if holder.pool[index]:
                total = holder.pool[index] + holder.pool_remainder[index]
                share, holder.pool_remainder[index] = divmod(total, 6)
                holder.pool[index] = 0
                if share:
                    for port in range(6):
                        layer.place(position, own, port, share, holder.phase, NO_MOMENTUM)
                    self.shadow_released[index] += 6 * share
        total = holder.phase_remainder + holder.content
        steps, holder.phase_remainder = divmod(total, self.world.clock)
        if 2 * steps >= self.world.phase_steps:
            raise ValueError(
                f"{SHADOW_LAW}: content {holder.number} turns its phase by half the circle or more "
                "per interval (its content has grown past K x N / 2)"
            )
        holder.phase = (holder.phase + steps) & self.world.phase_mask
        holder.phase_steps += steps

    def _move(self, holder: Holder) -> None:
        """The step by the accumulators (section 53, T2)."""
        if holder.arrived:
            holder.arrived = False
            return
        if holder.fixed or holder.owed > 0:
            return
        content = holder.content
        if content <= 0:
            return
        for axis in range(3):
            value = holder.accumulators[axis] + holder.momentum[axis]
            holder.accumulators[axis] = max(-content, min(content, value))
        for axis in range(3):
            if abs(holder.accumulators[axis]) < content:
                continue
            sign = 1 if holder.accumulators[axis] > 0 else -1
            holder.accumulators[axis] -= sign * content
            holder.steps += 1
            holder.arrived = True
            target = list(holder.position)
            target[axis] += sign
            origin = holder.position
            del self.at[origin]
            if not 0 <= target[axis] < self.shape[axis]:
                # Off the board with its content; what it pooled stays on the
                # absorbed line, absorbed for good.
                for index in range(len(self.families)):
                    self.held_escaped[index] += holder.held[index]
                del self.holders[holder.number]
                self._event("escaped", holder, holder.family, holder.number, content, ZERO3)
                return
            destination: Address3 = (target[0], target[1], target[2])
            if destination in self.at:
                other = self.holders[self.at[destination]]
                for index in range(len(self.families)):
                    other.held[index] += holder.held[index]
                    other.pool[index] += holder.pool[index]
                    other.pool_remainder[index] += holder.pool_remainder[index]
                other.momentum = [
                    int(a) + int(b) for a, b in zip(other.momentum, holder.momentum, strict=True)
                ]
                other.charge += holder.charge
                del self.holders[holder.number]
                self._event("merged", holder, holder.family, other.number, content, ZERO3)
                return
            holder.position = destination
            self.at[destination] = holder.number
            if self.record is not None:
                self.record(
                    {
                        "event": "step",
                        "tick": self.tick,
                        "number": holder.number,
                        "node": list(origin),
                        "to": list(destination),
                        "momentum": list(holder.momentum),
                    }
                )
            return

    def _event(
        self,
        kind: str,
        holder: Holder,
        family: int,
        number: int,
        amount: int,
        push: tuple[int, int, int],
    ) -> None:
        if self.record is None:
            return
        self.record(
            {
                "event": kind,
                "tick": self.tick,
                "node": list(holder.position),
                "holder": holder.number,
                "family": self.families[family].name,
                "number": number,
                "amount": amount,
                "push": list(push),
            }
        )

    # -- the books -------------------------------------------------------------

    def books(self) -> dict[str, object]:
        """The ledger at the current tick, every line with its identity."""
        families: dict[str, object] = {}
        balanced = True
        for index, family in enumerate(self.families):
            held_current = sum(holder.held[index] for holder in self.holders.values())
            # What came home or was re-released is on the absorbed line until
            # its release (the pool is the holder's, not the layer's).
            layer = self.layers[index]
            held = {
                "initial": self.held_initial[index],
                "absorbed": self.held_absorbed[index],
                "current": held_current,
                "spent": self.held_spent[index],
                "escaped": self.held_escaped[index],
            }
            held["balanced"] = held["initial"] + held["absorbed"] == (
                held["current"] + held["spent"] + held["escaped"]
            )
            shadows = {
                "initial": self.shadow_initial[index],
                "released": self.shadow_released[index],
                "current": layer.current(),
                "escaped": layer.escaped,
                "absorbed": self.shadow_absorbed[index],
            }
            shadows["balanced"] = shadows["initial"] + shadows["released"] == (
                shadows["current"] + shadows["escaped"] + shadows["absorbed"]
            )
            balanced = balanced and bool(held["balanced"]) and bool(shadows["balanced"])
            families[family.name] = {"held": held, "shadows": shadows}
        held_momentum = [0, 0, 0]
        for holder in self.holders.values():
            held_momentum = [a + b for a, b in zip(held_momentum, holder.momentum, strict=True)]
        return {
            "tick": self.tick,
            "families": families,
            # The momentum lives on held content alone and changes only by the
            # pushes (round 8, S8): no ledger of the field's momentum.
            "momentum": {"held": held_momentum},
            "charge": sum(holder.charge for holder in self.holders.values()),
            "balanced": balanced,
        }

    def contents(self) -> list[dict[str, object]]:
        return [self.holders[number].state() for number in sorted(self.holders)]

    def shell_readings(self, family: int, centre: Address3, radius: int) -> dict[str, float]:
        """The shell means at one radius of the last interval's readings: the
        Nodes at Euclidean distance within a half Link of `radius` from the
        centre, their number, the mean count (the amount that arrived per
        Node), the mean radial flow (amount x heading projected on the radial
        unit vector, summed per Node) and the mean size in quanta^(1/2) (the
        32nds over 32), every number summed."""
        grid = np.indices(self.shape).reshape(3, -1).T - np.array(centre)
        distance = np.sqrt((grid * grid).sum(axis=1))
        chosen = np.abs(distance - radius) < 0.5
        chosen &= distance > 0
        positions = grid[chosen]
        radial = positions / distance[chosen][:, None]
        cells = tuple((positions + np.array(centre)).T)
        count = self.count[family][cells]
        flow = self.flow[family][cells]
        size = self.size[family][cells].sum(axis=-1)
        return {
            "nodes": float(chosen.sum()),
            "count": float(count.mean()),
            "flow": float((flow * radial).sum(axis=1).mean()),
            "size": float(size.mean()) / MIXING_AMPLITUDE_SCALE,
        }

    def cube_flux(self, family: int, centre: Address3, half: int) -> int:
        """The net outward flow through the closed surface between the cube of
        half-width `half` about the centre and its neighbours, this interval:
        the amount that arrived just outside each face moving outward (it
        crossed the surface out) less the amount that arrived on the face
        moving inward (it crossed the surface in), Gauss's flux."""
        per_port = self.per_port[family]
        total = 0
        for axis in range(3):
            for sign in (1, -1):
                face = centre[axis] + sign * half
                outside = face + sign
                if not 0 <= outside < self.shape[axis]:
                    continue
                lows = [max(0, centre[a] - half) for a in range(3)]
                highs = [min(self.shape[a], centre[a] + half + 1) for a in range(3)]
                slices = [slice(lows[a], highs[a]) for a in range(3)]
                outward = 2 * axis + (0 if sign > 0 else 1)
                inward = outward ^ 1
                slices[axis] = slice(outside, outside + 1)
                total += int(per_port[tuple(slices)][..., outward].sum())
                slices[axis] = slice(face, face + 1)
                total -= int(per_port[tuple(slices)][..., inward].sum())
        return total

    # -- the snapshot ----------------------------------------------------------

    def snapshot_stream(self) -> Iterator[tuple[str, object]]:
        """The snapshot as (key, value) pairs, the Nodes with content as an
        iterator over one entry at a time (`snapshot_writer.write_snapshot`)."""
        yield "law", SHADOW_LAW
        yield "tick", self.tick
        yield "shape", list(self.shape)
        yield "boundary", "open"
        yield "contents", self.contents()
        yield (
            "escaped",
            [
                {"family": family.name, "amount": layer.escaped}
                for family, layer in zip(self.families, self.layers, strict=True)
            ],
        )
        yield "nodes", self._node_entries()

    def snapshot(self) -> dict[str, object]:
        return {
            key: (list(value) if isinstance(value, Iterator) else value)
            for key, value in self.snapshot_stream()
        }

    def _node_entries(self) -> Iterator[dict[str, object]]:
        present = np.zeros(self.shape, dtype=bool)
        for layer in self.layers:
            if layer.owners:
                present |= (
                    layer.arr_amt.any(axis=(3, 4, 5))
                    | layer.reg.any(axis=(3, 4))
                    | layer.fly_amt.any(axis=(3, 4, 5))
                )
        for x, y, z in zip(*np.nonzero(present), strict=True):
            position = (int(x), int(y), int(z))
            entry: dict[str, object] = {"position": list(position), "families": []}
            families = entry["families"]
            assert isinstance(families, list)
            for family, layer in zip(self.families, self.layers, strict=True):
                if not layer.owners:
                    continue
                arrivals = []
                departures = []
                parked = []
                for rank, number in enumerate(layer.owners):
                    for port in range(6):
                        for index in range(layer.arr_amt.shape[-1]):
                            cell = (*position, rank, port, index)
                            if layer.arr_amt[cell]:
                                arrivals.append(
                                    {
                                        "number": number,
                                        "heading": list(PORT_HEADINGS[port]),
                                        "amount": int(layer.arr_amt[cell]),
                                        "phase": int(layer.arr_ph[cell]),
                                        "waiting": int(layer.wait_owed[(*position, rank)]),
                                    }
                                )
                            if layer.fly_amt[cell]:
                                departures.append(
                                    {
                                        "number": number,
                                        "heading": list(PORT_HEADINGS[port]),
                                        "amount": int(layer.fly_amt[cell]),
                                        "phase": int(layer.fly_ph[cell]),
                                    }
                                )
                        slot = (*position, rank, port)
                        if layer.reg[slot]:
                            parked.append(
                                {
                                    "number": number,
                                    "heading": list(PORT_HEADINGS[port]),
                                    "ninths": int(layer.reg[slot]),
                                    "phase": int(layer.regph[slot]),
                                }
                            )
                if arrivals or departures or parked:
                    families.append(
                        {
                            "family": family.name,
                            "arrivals": arrivals,
                            "departures": departures,
                            "parked": parked,
                        }
                    )
            yield entry
