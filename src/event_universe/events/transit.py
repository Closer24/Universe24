"""The events in transit of one family: every Node's six arrival slots and
six departure slots per number as integer arrays, cycled as one vectorized
step (the law of events, Highlights 5.4).

The arrays have the axes (x, y, z, number, Port): `arr_*` hold the events
that arrived at each Node this interval per number (the measured event whose
continuation they are) and travel Port, with the amount, the phase, the
momentum carried and the content carried (`*_con`: what the units cost their
emitter, the family's `quantum` per unit per phase step of the emitter's turn
at the release, E = h f; the model owner, 2026-09-19, "I approve the
proposal"); `fly_*` the departures of the last cycle until the walk delivers
them; `suspended` per Node and number the count the arrivals there carry,
the intervals their exit is still suspended. Nothing else is kept at a Node:
no parked share, no remainder. The interval's steps on the transit (the
engine, `engine.py`, orders them with the measured events):

- the walk: every departure is created one Link on, at the neighbour, with
  its record unchanged (an event in transit does not turn: a transfer is not
  a tick of its clock), what leaves through an open face booked as escaped
  and reported to the engine's face observer as a click on that face (an
  open face is a detector, the model owner, 2026-09-19: the escape is a
  measurement at the border, not a loss; `face_observer`); on an axis the
  world declares periodic the departures through one face are created at
  the first Node of the opposite face (the wrap), nothing escapes on that
  axis, and with an extent of 1 a departure returns to its own Node as its
  arrival through that Port (a one-interval stub);
- the sizes: per Node and number the size of the coherent sum of the
  arrivals, the amplitude the mixing forms, in 32nds of one unit's (`sizes`),
  a reading (the shell means) and the phase window's sum; they no longer
  feed the suspension;
- the suspension: the arrivals of one number of a paid family that reached
  a Node this interval read the presence there, everything present this
  interval over every family and every number but their own (the amount
  that arrived, the units waiting there among it, and the content of the
  measured event at the Node, here; the engine forms it), and carry a
  count, `presence x n // d` intervals at the world's `suspension`
  `[n, d]`; while the count runs they are created here, interval after
  interval, and what arrives behind them joins them and waits with them
  (the next event is delayed); a count is written once, on arrival, never
  accumulated;
- the mixing (node-mixing-v3, `mix_arrivals` by import, one rule for every
  family): the sides' weights from all the arrivals at the Node, whatever
  their number, the coherent sum's squared leaving amplitudes for a family
  with a phase circle (the weights common to every number there) and its
  diagonal, per number 32^2 x (its amount over the six Ports + 3 x its
  amount through the side's own Port), for a family without one
  (`"phase": false`); per number
  whole units placed by the largest remainder with the ties in the tick's
  Port order, a number with no whole for any side going whole by its own
  momentum, every unit keeping its number, its momentum apportioned over
  its departures; the departures into flight. The content a number's
  arrivals carry goes with its units placed as the momentum does, exact
  (`apportion_carried` on one component), so a slot's content is
  amount x quantum x s while every unit in it was released at one turn s,
  and the sum over the slots is exact whatever met. `sizes` is a reading
  per Node and number (the shell means); `phase_at` reads the coherent sum
  over a set of numbers, and what a measured event reads for its window is
  the one reading set, every number at its Node but its own (the model
  owner, 2026-09-19).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np

from event_universe.core.lattice import PORT_HEADINGS, Address3
from event_universe.core.phase import PHASE_COSINE_SCALE, phase_cosines, phase_sines
from event_universe.events.mixing import (
    MIXING_AMPLITUDE_SCALE,
    apportion_carried,
    integer_root,
    mix_arrivals,
    place_departures,
    tie_order,
)

HEADINGS = np.array(PORT_HEADINGS, dtype=np.int64)
# The momenta the transit carries are bounded by the 64-bit work register: a
# push is a unit's momentum times the measured event's content.
MOMENTUM_BOUND = (1 << 62) - 1
# What the walk reports for every escape through an open face, one call per
# Node, number and face: the family, the face (its Port index), the edge
# Node the units left from, the number, the amount, the phase, the momentum
# carried and the content carried. The engine records it as a click on the
# face detector; the transit keeps no record of its own.
FaceObserver = Callable[[int, int, Address3, int, int, int, list[int], int], None]


def step_window(modulus: int) -> int:
    """How many steps either side of the step nearest a direction can hold the
    greatest rounded projection: the tables are the circle's cosines and sines
    rounded to 1/256, so two projections of a size v compare with an error
    below 1.415 v (0.5 (|x| + |y|) each), while a step k away from the nearest
    lies at least (2k - 1) pi / N from the direction and loses at least
    256 v (cos(pi / N) - cos((2k - 1) pi / N)) against it; the window is the
    last k at which that loss is below the error (at least 1, since the
    nearest step's neighbour can tie with it exactly)."""
    window = 1
    while 256.0 * (np.cos(np.pi / modulus) - np.cos((2 * window + 1) * np.pi / modulus)) <= 1.415:
        window += 1
        if 2 * window + 1 >= modulus:
            return modulus // 2
    return window


def nearest_step(cosines: np.ndarray, sines: np.ndarray, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """The phase step whose projection x cos + y sin is greatest, the first on
    a tie, computed exactly over the window of candidates around the step
    nearest the direction of (x, y) that `step_window` bounds: no step beyond
    it can win, the candidates' projections are exact integers, and the
    lowest step among those at the maximum is the first on a tie over the
    circle. Step 0 for a zero sum."""
    modulus = len(cosines)
    mask = modulus - 1
    window = step_window(modulus)
    result = np.zeros(x.shape, dtype=np.int64)
    active = (x != 0) | (y != 0)
    if not active.any():
        return result
    ax, ay = x[active], y[active]
    angle = np.arctan2(ay.astype(np.float64), ax.astype(np.float64))
    centre = np.rint(angle * (modulus / (2.0 * np.pi))).astype(np.int64) & mask
    offsets = np.arange(-window, window + 1, dtype=np.int64)
    candidates = (centre[:, None] + offsets) & mask
    projection = ax[:, None] * np.take(cosines, candidates) + ay[:, None] * np.take(sines, candidates)
    best = projection.max(axis=-1, keepdims=True)
    # The lowest step among those at the maximum (the first on a tie).
    stepped = np.where(projection == best, candidates, modulus)
    result[active] = stepped.min(axis=-1)
    return result


class Transit:
    """The arrays of one family (`MixingArrays` for the kernels)."""

    def __init__(
        self,
        family: int,
        shape: Address3,
        owners: tuple[int, ...],
        phase_steps: int,
        clock: int,
        periodic: tuple[bool, bool, bool] = (False, False, False),
        phased: bool = True,
        *,
        exact_transport: bool = False,
        face_observer: FaceObserver | None = None,
    ) -> None:
        self.family = family
        self.shape = shape
        # Told of every escape through an open face (a click on the face
        # detector, recorded by the engine); None records nothing.
        self.face_observer = face_observer
        # Per axis whether the walk wraps (the world's `boundary`); an open
        # axis lets its departures escape at the edge.
        self.periodic = periodic
        # Whether the family has a phase circle: without one every phase is
        # 0, nothing turns, and the Node's weights are the diagonal of the
        # coherent sum (`mixing.diagonal_weights`).
        self.phased = phased
        self.owners = owners
        self.rank = {number: rank for rank, number in enumerate(owners)}
        count = len(owners)
        self.modulus = phase_steps
        self.mask = phase_steps - 1
        self.clock = clock
        # The interval's tick, set by the engine before the cycle: the ties of
        # the sides' apportionment are broken in Port order counted from it.
        self.tick = 0
        # Exact transport does not call the default coherent-mixing kernels.
        # It keeps their array protocol but needs no phase lookup tables.
        cosines = np.array([] if exact_transport else phase_cosines(phase_steps), dtype=np.int64)
        sines = np.array([] if exact_transport else phase_sines(phase_steps), dtype=np.int64)
        self.cosines: np.ndarray | None = cosines
        self.sines: np.ndarray | None = sines
        self.mix_cosines = cosines
        self.mix_sines = sines
        cells = (*shape, count, 6)
        self.arr_amt = np.zeros(cells, dtype=np.int64)
        self.arr_ph = np.zeros(cells, dtype=np.int64)
        self.arr_mom = np.zeros((*cells, 3), dtype=np.int64)
        self.fly_amt = np.zeros(cells, dtype=np.int64)
        self.fly_ph = np.zeros(cells, dtype=np.int64)
        self.fly_mom = np.zeros((*cells, 3), dtype=np.int64)
        # The content carried per slot: amount x quantum x s at birth (s the
        # emitter's phase turn at the release), apportioned with the units.
        self.arr_con = np.zeros(cells, dtype=np.int64)
        self.fly_con = np.zeros(cells, dtype=np.int64)
        self.suspended = np.zeros((*shape, count), dtype=np.int64)
        # The slots filled at the start (the events in transit the world
        # declares), arrivals of the first interval for the suspension.
        self.fresh = np.zeros((*shape, count), dtype=bool)
        # The escapes, cumulative: the amount, the momentum and the content
        # carried.
        self.escaped = 0
        self.escaped_momentum = np.zeros(3, dtype=np.int64)
        self.escaped_content = 0

    # -- the kernels' protocol -------------------------------------------------

    def _nearest_step(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        assert self.cosines is not None and self.sines is not None
        return nearest_step(self.cosines, self.sines, x, y)

    # -- readouts --------------------------------------------------------------

    def current(self) -> int:
        """The amount on the transit: the arrivals and the departures in flight."""
        return int(self.arr_amt.sum()) + int(self.fly_amt.sum())

    def carried(self) -> np.ndarray:
        """The momentum in flight on the transit, three integers."""
        return self.arr_mom.reshape(-1, 3).sum(axis=0) + self.fly_mom.reshape(-1, 3).sum(axis=0)

    def content(self) -> int:
        """The content carried on the transit: the sum over the arrivals and
        the departures of amount x quantum x s (what the emitters spent)."""
        return int(self.arr_con.sum()) + int(self.fly_con.sum())

    def port_sums(self) -> tuple[np.ndarray, np.ndarray]:
        """Per Node, number and travel Port: the amount that arrived and the
        phase of its coherent sum (the slot's own phase)."""
        return self.arr_amt.copy(), self.arr_ph.copy()

    def sizes(self) -> np.ndarray:
        """Per Node and number the size of the coherent sum of the arrivals in
        32nds of one unit's amplitude: per travel Port the integer root of the
        amount at its phase, the six summed on the circle, the root of
        x^2 + y^2 over the tables' scale."""
        amount, phase = self.port_sums()
        assert self.cosines is not None and self.sines is not None
        amplitude = integer_root(amount * (MIXING_AMPLITUDE_SCALE * MIXING_AMPLITUDE_SCALE))
        x = (amplitude * self.cosines[phase]).sum(axis=-1)
        y = (amplitude * self.sines[phase]).sum(axis=-1)
        return integer_root(x * x + y * y) // PHASE_COSINE_SCALE

    def phase_at(self, position: Address3, ranks: Sequence[int]) -> int:
        """The phase of the arrivals of a set of numbers (their ranks) at one
        Node: the nearest step of their coherent sum, per number and travel
        Port the integer root of the amount at its phase, all summed on the
        circle (step 0 for a zero sum; for one number the sum whose size
        `sizes` reports). What a measured event reads for its phase window
        and stamps on its records is the one reading set, every number at
        its Node but its own (the model owner, 2026-09-19); the home record
        reads its own number alone. The tables at 1/256 read a single
        arrival's step back exactly on a circle of up to 64 steps; on a
        larger circle neighbouring steps can read as one, as in `receive`
        and `place`."""
        assert self.cosines is not None and self.sines is not None
        cell = (*position, list(ranks))
        amount, phase = self.arr_amt[cell], self.arr_ph[cell]
        amplitude = integer_root(amount * (MIXING_AMPLITUDE_SCALE * MIXING_AMPLITUDE_SCALE))
        x = np.array([(amplitude * self.cosines[phase]).sum()], dtype=np.int64)
        y = np.array([(amplitude * self.sines[phase]).sum()], dtype=np.int64)
        return int(self._nearest_step(x, y)[0])

    def count(self) -> np.ndarray:
        """Per Node the amount that arrived this interval, every number."""
        return self.arr_amt.sum(axis=(3, 4))

    def flow(self) -> np.ndarray:
        """Per Node the sum of amount x heading over the arrivals, three
        integers: the net flux through the Node."""
        return self.arr_amt.sum(axis=3) @ HEADINGS

    # -- the steps -------------------------------------------------------------

    def walk(self) -> np.ndarray:
        """Every departure created one Link on, its record unchanged, into the
        arrivals at the neighbour (joining what waits there as one amplitude
        per Port); what leaves through an open face is booked as escaped
        with the momentum and the content it carried and reported to the
        face observer as a click on that face, one per Node and number, and
        on a periodic axis the departures through one face are created at
        the first Node of the opposite face, in the slot of their travel
        heading, nothing escaping. Returns, per Node and number, whether
        anything arrived this interval."""
        arrived = self.fresh.copy()
        self.fresh[...] = False
        if not self.fly_amt.any():
            return arrived
        incoming_amt = np.zeros_like(self.arr_amt)
        incoming_ph = np.zeros_like(self.arr_ph)
        incoming_mom = np.zeros_like(self.arr_mom)
        incoming_con = np.zeros_like(self.arr_con)
        for port in range(6):
            source = self.fly_amt[..., port]
            if not source.any():
                continue
            axis, forward = port >> 1, (port & 1) == 0
            phase = self.fly_ph[..., port]
            momentum = self.fly_mom[..., port, :]
            content = self.fly_con[..., port]
            if self.periodic[axis]:
                # The wrap: every Node's departure on this heading is created
                # at the next Node along the axis, the last face's at the
                # first (with an extent of 1, at the same Node).
                shift = 1 if forward else -1
                incoming_amt[..., port] = np.roll(source, shift, axis=axis)
                incoming_ph[..., port] = np.roll(phase, shift, axis=axis)
                incoming_mom[..., port, :] = np.roll(momentum, shift, axis=axis)
                incoming_con[..., port] = np.roll(content, shift, axis=axis)
                continue
            ahead: list[slice | int] = [slice(None)] * 3
            behind: list[slice | int] = [slice(None)] * 3
            edge: list[slice | int] = [slice(None)] * 3
            if forward:
                ahead[axis], behind[axis], edge[axis] = slice(1, None), slice(None, -1), -1
            else:
                ahead[axis], behind[axis], edge[axis] = slice(None, -1), slice(1, None), 0
            incoming_amt[(*ahead, slice(None), port)] = source[tuple(behind)]
            incoming_ph[(*ahead, slice(None), port)] = phase[tuple(behind)]
            incoming_mom[(*ahead, slice(None), port, slice(None))] = momentum[tuple(behind)]
            incoming_con[(*ahead, slice(None), port)] = content[tuple(behind)]
            gone = source[tuple(edge)]
            if gone.any():
                self.escaped += int(gone.sum())
                self.escaped_momentum += momentum[tuple(edge)].reshape(-1, 3).sum(axis=0)
                self.escaped_content += int(content[tuple(edge)].sum())
                if self.face_observer is not None:
                    self._report_face(port, axis, edge, gone, phase, momentum, content)
        self.fly_amt[...] = 0
        self.fly_ph[...] = 0
        self.fly_mom[...] = 0
        self.fly_con[...] = 0
        arrived |= incoming_amt.sum(axis=-1) > 0
        self.receive(incoming_amt, incoming_ph, incoming_mom, incoming_con)
        return arrived

    def _report_face(
        self,
        port: int,
        axis: int,
        edge: list[slice | int],
        gone: np.ndarray,
        phase: np.ndarray,
        momentum: np.ndarray,
        content: np.ndarray,
    ) -> None:
        """The clicks on one open face this interval, one per edge Node and
        number that left through it: the amount, the phase, the momentum and
        the content of that slot, to the face observer (a record; the
        physics of the escape is booked above)."""
        assert self.face_observer is not None
        gone_ph, gone_mom, gone_con = phase[tuple(edge)], momentum[tuple(edge)], content[tuple(edge)]
        face_index = edge[axis]
        assert isinstance(face_index, int)
        edge_coordinate = face_index % self.shape[axis]
        for found in np.argwhere(gone):
            cell = tuple(int(value) for value in found)
            coordinates = list(cell[:-1])
            coordinates.insert(axis, edge_coordinate)
            node: Address3 = (coordinates[0], coordinates[1], coordinates[2])
            self.face_observer(
                self.family,
                port,
                node,
                self.owners[cell[-1]],
                int(gone[cell]),
                int(gone_ph[cell]),
                [int(value) for value in gone_mom[cell]],
                int(gone_con[cell]),
            )

    def receive(
        self,
        amount: np.ndarray,
        phase: np.ndarray,
        momentum: np.ndarray,
        content: np.ndarray | None = None,
    ) -> None:
        """Arrivals into the arrays: into empty slots as they are; where a slot
        holds events that wait, one amplitude per Port (the amounts added, the
        phase of their coherent sum, the momenta added, the contents added).
        Arrivals given without a content carry none."""
        if content is None:
            content = np.zeros_like(amount)
        if not self.arr_amt.any():
            self.arr_amt[...] = amount
            self.arr_ph[...] = phase
            self.arr_mom[...] = momentum
            self.arr_con[...] = content
            return
        held = self.arr_amt > 0
        coming = amount > 0
        both = held & coming
        free = ~held & coming
        self.arr_amt[free] = amount[free]
        self.arr_ph[free] = phase[free]
        self.arr_mom[free] = momentum[free]
        self.arr_con[free] = content[free]
        if both.any():
            assert self.cosines is not None and self.sines is not None
            old_amt, old_ph = self.arr_amt[both], self.arr_ph[both]
            new_amt, new_ph = amount[both], phase[both]
            self.arr_amt[both] = old_amt + new_amt
            if self.phased:
                x = old_amt * self.cosines[old_ph] + new_amt * self.cosines[new_ph]
                y = old_amt * self.sines[old_ph] + new_amt * self.sines[new_ph]
                self.arr_ph[both] = self._nearest_step(x, y)
            self.arr_mom[both] = self.arr_mom[both] + momentum[both]
            self.arr_con[both] = self.arr_con[both] + content[both]

    def suspend(self, read: np.ndarray, width: tuple[int, int], arrived: np.ndarray) -> None:
        """The suspension of the arrivals: per Node and number where something
        arrived this interval, the presence read (per Node and number,
        everything present this interval over every family and every number
        but the reader's own: the amount that arrived, the units waiting and
        the content of a measured event there, formed by the engine) times
        the width's numerator over its denominator,
        the whole part, is the count the arrivals carry, written once; what
        joins a waiting slot waits with it, the larger count kept. A count
        above zero holds the number's arrivals at the Node this interval."""
        numerator, denominator = width
        if not numerator:
            return
        if int(read.max(initial=0)) * numerator >= 1 << 62:
            raise OverflowError("64-bit intermediate range exceeded")
        derived = np.where(arrived, read * numerator // denominator, 0)
        self.suspended = np.maximum(self.suspended, derived)

    def frozen(self) -> np.ndarray:
        """Per Node and number whether the arrivals are held this interval."""
        return self.suspended > 0

    def cycle(self) -> None:
        """The mixing at every Node of the arrivals that are not held, the
        departures into flight, each number's content carried going with its
        units placed (exact per Node and number, `apportion_carried` on one
        component with the tick's ties); the held slots stay as arrivals for
        the next interval, their count paid by one."""
        frozen = self.frozen()
        kept = None
        if frozen.any():
            kept = (
                self.arr_amt[frozen].copy(),
                self.arr_ph[frozen].copy(),
                self.arr_mom[frozen].copy(),
                self.arr_con[frozen].copy(),
            )
            self.arr_amt[frozen] = 0
            self.arr_ph[frozen] = 0
            self.arr_mom[frozen] = 0
            self.arr_con[frozen] = 0
        if self.arr_amt.any():
            whole, phase, momenta = mix_arrivals(self, MOMENTUM_BOUND)
            place_departures(self, whole, phase, momenta, MOMENTUM_BOUND)
            self.fly_con[...] = self._apportion_content(self.arr_con.sum(axis=-1), whole)
        self.arr_amt[...] = 0
        self.arr_ph[...] = 0
        self.arr_mom[...] = 0
        self.arr_con[...] = 0
        if kept is not None:
            self.arr_amt[frozen], self.arr_ph[frozen], self.arr_mom[frozen], self.arr_con[frozen] = kept
            self.suspended[frozen] -= 1

    def _apportion_content(self, content: np.ndarray, whole: np.ndarray) -> np.ndarray:
        """Per Node and number the content that arrived shared over the six
        headings in proportion to the units placed on them, exact: the floors
        and the units left to the largest remainders, the ties in the tick's
        Port order (`apportion_carried` on one component, the momentum's own
        rule). A slot of one turn s keeps amount x quantum x s exactly."""
        if not content.any():
            return np.zeros(whole.shape, dtype=np.int64)
        if int(content.max(initial=0)) > MOMENTUM_BOUND:
            raise OverflowError("64-bit intermediate range exceeded")
        carried = np.zeros((*content.shape, 3), dtype=np.int64)
        carried[..., 0] = content
        return apportion_carried(carried, whole, tie_order(self.tick))[..., 0]

    def take(
        self, position: Address3, rank: int
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """The arrivals of one number at one Node, taken out of the arrays
        (measured by a measured event): the amounts, phases, momenta and
        contents per Port."""
        cell = (*position, rank)
        amount, phase, momentum, content = (
            self.arr_amt[cell].copy(),
            self.arr_ph[cell].copy(),
            self.arr_mom[cell].copy(),
            self.arr_con[cell].copy(),
        )
        self.arr_amt[cell] = 0
        self.arr_ph[cell] = 0
        self.arr_mom[cell] = 0
        self.arr_con[cell] = 0
        self.suspended[cell] = 0
        return amount, phase, momentum, content

    def place(
        self,
        position: Address3,
        rank: int,
        port: int,
        amount: int,
        phase: int,
        momentum: np.ndarray,
        content: int = 0,
    ) -> None:
        """A release from a measured event into the departures of its Node on
        one Port, with the content it carries (amount x quantum x s; 0 for a
        release that costs nothing): the slot as it is when empty, or one
        amplitude with what is there (the amounts added, the phase of the
        coherent sum, the momenta added, the contents added)."""
        if amount <= 0:
            return
        cell = (*position, rank, port)
        held = int(self.fly_amt[cell])
        if held == 0:
            self.fly_amt[cell] = amount
            self.fly_ph[cell] = phase
            self.fly_mom[cell] = momentum
            self.fly_con[cell] = content
            return
        assert self.cosines is not None and self.sines is not None
        self.fly_amt[cell] = held + amount
        if self.phased:
            held_phase = int(self.fly_ph[cell])
            x = np.array(held * self.cosines[held_phase] + amount * self.cosines[phase])
            y = np.array(held * self.sines[held_phase] + amount * self.sines[phase])
            self.fly_ph[cell] = int(self._nearest_step(x, y))
        self.fly_mom[cell] += momentum
        self.fly_con[cell] += content
