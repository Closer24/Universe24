"""The events in transit of one family: every Node's six arrival slots and
six departure slots per number as integer arrays, cycled as one vectorized
step (the law of events, Highlights 5.4).

The arrays have the axes (x, y, z, number, Port): `arr_*` hold the events
that arrived at each Node this interval per number (the measured event whose
continuation they are) and travel Port, with the amount, the phase and the
momentum carried; `fly_*` the departures of the last cycle until the walk
delivers them; `suspended` per Node and number the count the arrivals there
carry, the intervals their exit is still suspended. Nothing else is kept at
a Node: no parked share, no remainder. The interval's steps on the transit
(the engine, `engine.py`, orders them with the measured events):

- the walk: every departure is created one Link on, at the neighbour, with
  its record unchanged (an event in transit does not turn: a transfer is not
  a tick of its clock), what leaves through an open face booked as escaped;
  on an axis the world declares periodic the departures through one face
  are created at the first Node of the opposite face (the wrap), nothing
  escapes on that axis, and with an extent of 1 a departure returns to its
  own Node as its arrival through that Port (a one-interval stub);
- the sizes: per Node and number the size of the coherent sum of the
  arrivals, the amplitude the mixing forms, in 32nds of one unit's (`sizes`),
  read by the measured events and by the exits for their suspension;
- the suspension: the arrivals of one number that reached a Node this
  interval read the sizes of the free families there and carry a count, the
  whole intervals of the world's `suspension` per whole unit of size read;
  while the count runs they are created here, interval after interval, and
  what arrives behind them joins them and waits with them (the next event is
  delayed); a count is written once, on arrival, never accumulated;
- the mixing (node-mixing-v2, `mix_arrivals` by import): the sides' shares
  from the vectors, whole units placed by the largest remainder with the
  ties in the tick's Port order, a group with no whole for any side going
  whole by its momentum; the departures into flight.
"""

from __future__ import annotations

import numpy as np

from event_universe.core.lattice import PORT_HEADINGS, Address3
from event_universe.core.phase import PHASE_COSINE_SCALE, phase_cosines, phase_sines
from event_universe.events.mixing import (
    MIXING_AMPLITUDE_SCALE,
    integer_root,
    mix_arrivals,
    place_departures,
)

HEADINGS = np.array(PORT_HEADINGS, dtype=np.int64)
# The momenta the transit carries are bounded by the 64-bit work register: a
# push is a unit's momentum times the measured event's content.
MOMENTUM_BOUND = (1 << 62) - 1


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
        *,
        exact_transport: bool = False,
    ) -> None:
        self.family = family
        self.shape = shape
        # Per axis whether the walk wraps (the world's `boundary`); an open
        # axis lets its departures escape at the edge.
        self.periodic = periodic
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
        self.suspended = np.zeros((*shape, count), dtype=np.int64)
        # The slots filled at the start (the events in transit the world
        # declares), arrivals of the first interval for the suspension.
        self.fresh = np.zeros((*shape, count), dtype=bool)
        # The escapes, cumulative: the amount and the momentum carried.
        self.escaped = 0
        self.escaped_momentum = np.zeros(3, dtype=np.int64)

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

    def phase_at(self, position: Address3, rank: int) -> int:
        """The phase of one number's arrivals at one Node: the nearest step of
        the coherent sum whose size `sizes` reports, per travel Port the
        integer root of the amount at its phase, the six summed on the circle
        (step 0 for a zero sum). What a measured event reads for its phase
        window and stamps on its records. The tables at 1/256 read a single
        arrival's step back exactly on a circle of up to 64 steps; on a
        larger circle neighbouring steps can read as one, as in `receive`
        and `place`."""
        assert self.cosines is not None and self.sines is not None
        cell = (*position, rank)
        amount, phase = self.arr_amt[cell], self.arr_ph[cell]
        amplitude = integer_root(amount * (MIXING_AMPLITUDE_SCALE * MIXING_AMPLITUDE_SCALE))
        x = (amplitude * self.cosines[phase]).sum(keepdims=True)
        y = (amplitude * self.sines[phase]).sum(keepdims=True)
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
        with the momentum it carried, and on a periodic axis the departures
        through one face are created at the first Node of the opposite face,
        in the slot of their travel heading, nothing escaping. Returns, per
        Node and number, whether anything arrived this interval."""
        arrived = self.fresh.copy()
        self.fresh[...] = False
        if not self.fly_amt.any():
            return arrived
        incoming_amt = np.zeros_like(self.arr_amt)
        incoming_ph = np.zeros_like(self.arr_ph)
        incoming_mom = np.zeros_like(self.arr_mom)
        for port in range(6):
            source = self.fly_amt[..., port]
            if not source.any():
                continue
            axis, forward = port >> 1, (port & 1) == 0
            phase = self.fly_ph[..., port]
            momentum = self.fly_mom[..., port, :]
            if self.periodic[axis]:
                # The wrap: every Node's departure on this heading is created
                # at the next Node along the axis, the last face's at the
                # first (with an extent of 1, at the same Node).
                shift = 1 if forward else -1
                incoming_amt[..., port] = np.roll(source, shift, axis=axis)
                incoming_ph[..., port] = np.roll(phase, shift, axis=axis)
                incoming_mom[..., port, :] = np.roll(momentum, shift, axis=axis)
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
            gone = source[tuple(edge)]
            if gone.any():
                self.escaped += int(gone.sum())
                self.escaped_momentum += momentum[tuple(edge)].reshape(-1, 3).sum(axis=0)
        self.fly_amt[...] = 0
        self.fly_ph[...] = 0
        self.fly_mom[...] = 0
        arrived |= incoming_amt.sum(axis=-1) > 0
        self.receive(incoming_amt, incoming_ph, incoming_mom)
        return arrived

    def receive(self, amount: np.ndarray, phase: np.ndarray, momentum: np.ndarray) -> None:
        """Arrivals into the arrays: into empty slots as they are; where a slot
        holds events that wait, one amplitude per Port (the amounts added, the
        phase of their coherent sum, the momenta added)."""
        if not self.arr_amt.any():
            self.arr_amt[...] = amount
            self.arr_ph[...] = phase
            self.arr_mom[...] = momentum
            return
        held = self.arr_amt > 0
        coming = amount > 0
        both = held & coming
        free = ~held & coming
        self.arr_amt[free] = amount[free]
        self.arr_ph[free] = phase[free]
        self.arr_mom[free] = momentum[free]
        if both.any():
            assert self.cosines is not None and self.sines is not None
            old_amt, old_ph = self.arr_amt[both], self.arr_ph[both]
            new_amt, new_ph = amount[both], phase[both]
            x = old_amt * self.cosines[old_ph] + new_amt * self.cosines[new_ph]
            y = old_amt * self.sines[old_ph] + new_amt * self.sines[new_ph]
            self.arr_amt[both] = old_amt + new_amt
            self.arr_ph[both] = self._nearest_step(x, y)
            self.arr_mom[both] = self.arr_mom[both] + momentum[both]

    def suspend(self, read: np.ndarray, width: int, arrived: np.ndarray) -> None:
        """The suspension of the arrivals: per Node and number where something
        arrived this interval, the size read (the free families' sizes at the
        Node, in 32nds) at `width` intervals per whole unit is the count the
        arrivals carry, written once; what joins a waiting slot waits with it,
        the larger count kept. A count above zero holds the number's arrivals
        at the Node this interval."""
        if not width:
            return
        derived = np.where(arrived, read * width // MIXING_AMPLITUDE_SCALE, 0)
        self.suspended = np.maximum(self.suspended, derived)

    def frozen(self) -> np.ndarray:
        """Per Node and number whether the arrivals are held this interval."""
        return self.suspended > 0

    def cycle(self) -> None:
        """The mixing at every Node of the arrivals that are not held, the
        departures into flight; the held slots stay as arrivals for the next
        interval, their count paid by one."""
        frozen = self.frozen()
        kept = None
        if frozen.any():
            kept = (self.arr_amt[frozen].copy(), self.arr_ph[frozen].copy(), self.arr_mom[frozen].copy())
            self.arr_amt[frozen] = 0
            self.arr_ph[frozen] = 0
            self.arr_mom[frozen] = 0
        if self.arr_amt.any():
            whole, phase, momenta = mix_arrivals(self, MOMENTUM_BOUND)
            place_departures(self, whole, phase, momenta, MOMENTUM_BOUND)
        self.arr_amt[...] = 0
        self.arr_ph[...] = 0
        self.arr_mom[...] = 0
        if kept is not None:
            self.arr_amt[frozen], self.arr_ph[frozen], self.arr_mom[frozen] = kept
            self.suspended[frozen] -= 1

    def take(self, position: Address3, rank: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """The arrivals of one number at one Node, taken out of the arrays
        (measured by a measured event): the amounts, phases and momenta per
        Port."""
        cell = (*position, rank)
        amount, phase, momentum = (
            self.arr_amt[cell].copy(),
            self.arr_ph[cell].copy(),
            self.arr_mom[cell].copy(),
        )
        self.arr_amt[cell] = 0
        self.arr_ph[cell] = 0
        self.arr_mom[cell] = 0
        self.suspended[cell] = 0
        return amount, phase, momentum

    def place(
        self, position: Address3, rank: int, port: int, amount: int, phase: int, momentum: np.ndarray
    ) -> None:
        """A release from a measured event into the departures of its Node on
        one Port: the slot as it is when empty, or one amplitude with what is
        there (the amounts added, the phase of the coherent sum, the momenta
        added)."""
        if amount <= 0:
            return
        cell = (*position, rank, port)
        held = int(self.fly_amt[cell])
        if held == 0:
            self.fly_amt[cell] = amount
            self.fly_ph[cell] = phase
            self.fly_mom[cell] = momentum
            return
        assert self.cosines is not None and self.sines is not None
        held_phase = int(self.fly_ph[cell])
        x = np.array(held * self.cosines[held_phase] + amount * self.cosines[phase])
        y = np.array(held * self.sines[held_phase] + amount * self.sines[phase])
        self.fly_amt[cell] = held + amount
        self.fly_ph[cell] = int(self._nearest_step(x, y))
        self.fly_mom[cell] += momentum
