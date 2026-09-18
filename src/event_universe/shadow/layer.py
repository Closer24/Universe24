"""The shadow layer of one family: every Node's twelve lanes' shadow slots and
its remainder registers as integer arrays, cycled as one vectorized step.

The arrays are the dense layer's (`event_universe/dense_field.py`,
perf-arrays-v1) with the axes (x, y, z, number, Port, layer): `arr_*` hold
the shadows that arrived at each Node this interval per number (the content
whose field they are) and travel Port, two layers (the two phases one Port can
carry from one neighbour's departure: the mixing's and the parked release's),
with the amount, the phase and the momentum carried; `reg*` the parked
shares per Node, number and Port in ninths (the remainder registers of point
22); `fly_*` the departures of the last cycle until the walk delivers them.
The interval's steps on the layer (the engine, `engine.py`, orders them with
the held contents' events):

- the walk: every departure moves one Link, a paid family's phase rotating by
  its amount over K (light's frequency is its amount; a cell below K does not
  turn; a matter shadow does not turn, round 8 section 52 (iv)), what leaves
  the open board booked as escaped;
- the sizes: per Node and number the size of the coherent sum of the arrivals,
  the amplitude the mixing forms, in 32nds of one quantum's (`sizes`), read by
  the held contents and by the quanta in flight for their wait;
- the wait: the quanta of one number at a Node owe one interval per whole unit
  of the other numbers' size read there, at the world's rate per unit, with a
  remainder carried per Node and number (`wait_debt`), and while they owe they
  neither mix nor move (`wait_owed`, the intervals left; a frozen cell), later
  arrivals of the number joining them as one amplitude per Port;
- the mixing (node-mixing-v1, `mix_arrivals` by import), the parked releases
  (`release_parked`) and the two departure layers (`merge_departures`,
  `place_departures`), the same integers as the old engine's.
"""

from __future__ import annotations

import numpy as np

from event_universe.core.disturbance_state import Address3
from event_universe.core.spatial_state import (
    MIXING_AMPLITUDE_SCALE,
    MIXING_DENOMINATOR,
    PHASE_COSINE_SCALE,
    PORT_HEADINGS,
    phase_cosines,
    phase_sines,
)
from event_universe.dense_field import (
    LAYERS,
    merge_departures,
    mix_arrivals,
    place_departures,
    release_parked,
)

HEADINGS = np.array(PORT_HEADINGS, dtype=np.int64)
# The momenta the layer carries are bounded by the 64-bit work register, not by
# the old engine's 32-bit cells: a push is a quantum's amount times the
# holder's content.
MOMENTUM_BOUND = (1 << 62) - 1


def array_sqrt(scaled: np.ndarray) -> np.ndarray:
    """The integer square root of every entry, the floor, exact (the dense
    layer's idiom: the float root corrected by one either way)."""
    root = np.floor(np.sqrt(scaled.astype(np.float64))).astype(np.int64)
    root = np.where(root * root > scaled, root - 1, root)
    return np.where((root + 1) * (root + 1) <= scaled, root + 1, root)


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
    a tie (the engine's `_phase_of_sum`), computed exactly over the window of
    candidates around the step nearest the direction of (x, y) that
    `step_window` bounds: no step beyond it can win, the candidates'
    projections are exact integers, and the lowest step among those at the
    maximum is the first on a tie over the circle. Step 0 for a zero sum."""
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


class ShadowLayer:
    """The arrays of one family (`MixingArrays` for the dense kernels)."""

    def __init__(
        self,
        family: int,
        shape: Address3,
        owners: tuple[int, ...],
        phase_steps: int,
        clock: int,
        rotates: bool = True,
    ) -> None:
        self.family = family
        # Whether the quanta turn their phase in flight by their amount over K
        # (light does; a matter shadow does not, round 8 section 52 (iv)).
        self.rotates = rotates
        self.shape = shape
        self.owners = owners
        self.rank = {number: rank for rank, number in enumerate(owners)}
        count = len(owners)
        self.modulus = phase_steps
        self.mask = phase_steps - 1
        self.clock = clock
        self.total = MIXING_DENOMINATOR
        cosines = np.array(phase_cosines(phase_steps), dtype=np.int64)
        sines = np.array(phase_sines(phase_steps), dtype=np.int64)
        self.cosines: np.ndarray | None = cosines
        self.sines: np.ndarray | None = sines
        self.mix_cosines = cosines
        self.mix_sines = sines
        cells = (*shape, count, 6)
        self.arr_amt = np.zeros((*cells, LAYERS), dtype=np.int64)
        self.arr_ph = np.zeros((*cells, LAYERS), dtype=np.int64)
        self.arr_mom = np.zeros((*cells, LAYERS, 3), dtype=np.int64)
        self.reg = np.zeros(cells, dtype=np.int64)
        self.regph = np.zeros(cells, dtype=np.int64)
        self.reg_mom = np.zeros((*cells, 3), dtype=np.int64)
        self.fly_amt = np.zeros((*cells, LAYERS), dtype=np.int64)
        self.fly_ph = np.zeros((*cells, LAYERS), dtype=np.int64)
        self.fly_mom = np.zeros((*cells, LAYERS, 3), dtype=np.int64)
        self.wait_debt = np.zeros((*shape, count), dtype=np.int64)
        self.wait_owed = np.zeros((*shape, count), dtype=np.int64)
        # The escapes, cumulative: the amount and the momentum carried.
        self.escaped = 0
        self.escaped_momentum = np.zeros(3, dtype=np.int64)

    # -- the kernels' protocol -------------------------------------------------

    def _nearest_step(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        assert self.cosines is not None and self.sines is not None
        return nearest_step(self.cosines, self.sines, x, y)

    def combine(
        self, held: np.ndarray, hph: np.ndarray, share: np.ndarray, sph: np.ndarray
    ) -> np.ndarray:
        assert self.cosines is not None and self.sines is not None
        x = held * self.cosines[hph] + share * self.cosines[sph]
        y = held * self.sines[hph] + share * self.sines[sph]
        return self._nearest_step(x, y)

    # -- readouts --------------------------------------------------------------

    def current(self) -> int:
        """The amount on the layer: the arrivals, the departures in flight and
        the parked shares' whole quanta (their ninths sum to whole quanta)."""
        parked = int(self.reg.sum())
        if parked % self.total:
            raise ValueError("a family's parked shadows hold whole quanta in total")
        return int(self.arr_amt.sum()) + int(self.fly_amt.sum()) + parked // self.total

    def carried(self) -> np.ndarray:
        """The momentum in flight on the layer, three integers."""
        return (
            self.arr_mom.reshape(-1, 3).sum(axis=0)
            + self.fly_mom.reshape(-1, 3).sum(axis=0)
            + self.reg_mom.reshape(-1, 3).sum(axis=0)
        )

    def port_sums(self) -> tuple[np.ndarray, np.ndarray]:
        """Per Node, number and travel Port: the amount that arrived (the
        layers summed) and the phase of their coherent sum."""
        amount = self.arr_amt.sum(axis=-1)
        assert self.cosines is not None and self.sines is not None
        x = (self.arr_amt * self.cosines[self.arr_ph]).sum(axis=-1)
        y = (self.arr_amt * self.sines[self.arr_ph]).sum(axis=-1)
        return amount, self._nearest_step(x, y)

    def sizes(self) -> np.ndarray:
        """Per Node and number the size of the coherent sum of the arrivals in
        32nds of one quantum's amplitude (`arrival_amplitude`): per travel Port
        the integer root of the amount at the phase of its sum, the six summed
        on the circle, the root of x^2 + y^2 over the tables' scale."""
        amount, phase = self.port_sums()
        assert self.cosines is not None and self.sines is not None
        amplitude = array_sqrt(amount * (MIXING_AMPLITUDE_SCALE * MIXING_AMPLITUDE_SCALE))
        x = (amplitude * self.cosines[phase]).sum(axis=-1)
        y = (amplitude * self.sines[phase]).sum(axis=-1)
        return array_sqrt(x * x + y * y) // PHASE_COSINE_SCALE

    def count(self) -> np.ndarray:
        """Per Node the amount that arrived this interval, every number."""
        return self.arr_amt.sum(axis=(3, 4, 5))

    def flow(self) -> np.ndarray:
        """Per Node the sum of amount x heading over the arrivals, three
        integers: the net flux of the field through the Node."""
        per_port = self.arr_amt.sum(axis=(3, 5))
        return per_port @ HEADINGS

    # -- the steps -------------------------------------------------------------

    def walk(self) -> None:
        """Every departure one Link on, its phase turned by its amount over K,
        into the arrivals at the neighbour (joining what waits there as one
        amplitude per Port); what leaves the board is booked as escaped with
        the momentum it carried."""
        if not self.fly_amt.any():
            return
        incoming_amt = np.zeros_like(self.arr_amt)
        incoming_ph = np.zeros_like(self.arr_ph)
        incoming_mom = np.zeros_like(self.arr_mom)
        for port in range(6):
            source = self.fly_amt[..., port, :]
            if not source.any():
                continue
            axis, forward = port >> 1, (port & 1) == 0
            phase = self.fly_ph[..., port, :]
            if self.rotates:
                phase = (phase + source // self.clock) & self.mask
            momentum = self.fly_mom[..., port, :, :]
            ahead: list[slice | int] = [slice(None)] * 3
            behind: list[slice | int] = [slice(None)] * 3
            edge: list[slice | int] = [slice(None)] * 3
            if forward:
                ahead[axis], behind[axis], edge[axis] = slice(1, None), slice(None, -1), -1
            else:
                ahead[axis], behind[axis], edge[axis] = slice(None, -1), slice(1, None), 0
            incoming_amt[(*ahead, slice(None), port, slice(None))] = source[tuple(behind)]
            incoming_ph[(*ahead, slice(None), port, slice(None))] = phase[tuple(behind)]
            incoming_mom[(*ahead, slice(None), port, slice(None), slice(None))] = momentum[tuple(behind)]
            gone = source[tuple(edge)]
            if gone.any():
                self.escaped += int(gone.sum())
                self.escaped_momentum += momentum[tuple(edge)].reshape(-1, 3).sum(axis=0)
        self.fly_amt[...] = 0
        self.fly_ph[...] = 0
        self.fly_mom[...] = 0
        self.receive(incoming_amt, incoming_ph, incoming_mom)

    def receive(self, amount: np.ndarray, phase: np.ndarray, momentum: np.ndarray) -> None:
        """Arrivals into the arrays: into empty cells as they are; where a cell
        holds quanta that waited (their countdown over, due to mix with what
        arrives now) or still wait, the four layers are one amplitude per Port
        (the amounts added, the phase of their coherent sum, the momenta
        added)."""
        if not self.arr_amt.any():
            self.arr_amt[...] = amount
            self.arr_ph[...] = phase
            self.arr_mom[...] = momentum
            return
        held = self.arr_amt.sum(axis=-1) > 0
        coming = amount.sum(axis=-1) > 0
        both = held & coming
        free = ~held
        self.arr_amt[free] = amount[free]
        self.arr_ph[free] = phase[free]
        self.arr_mom[free] = momentum[free]
        if both.any():
            assert self.cosines is not None and self.sines is not None
            old_amt, old_ph, old_mom = self.arr_amt[both], self.arr_ph[both], self.arr_mom[both]
            new_amt, new_ph, new_mom = amount[both], phase[both], momentum[both]
            x = (old_amt * self.cosines[old_ph]).sum(axis=-1) + (new_amt * self.cosines[new_ph]).sum(
                axis=-1
            )
            y = (old_amt * self.sines[old_ph]).sum(axis=-1) + (new_amt * self.sines[new_ph]).sum(axis=-1)
            merged_amt = np.zeros_like(old_amt)
            merged_ph = np.zeros_like(old_ph)
            merged_mom = np.zeros_like(old_mom)
            merged_amt[:, 0] = old_amt.sum(axis=-1) + new_amt.sum(axis=-1)
            merged_ph[:, 0] = self._nearest_step(x, y)
            merged_mom[:, 0, :] = old_mom.sum(axis=-2) + new_mom.sum(axis=-2)
            self.arr_amt[both] = merged_amt
            self.arr_ph[both] = merged_ph
            self.arr_mom[both] = merged_mom

    def charge_wait(self, read: np.ndarray, numerator: int, denominator: int) -> None:
        """The wait of the quanta in flight: per Node and number the size read
        (the other numbers' sizes at the Node, in 32nds) at n / d intervals per
        whole unit joins the debt, the whole intervals owed are added to the
        countdown, and a countdown above zero freezes the number's arrivals at
        the Node this interval. Cells already waiting read nothing more."""
        if not numerator:
            return
        present = self.arr_amt.sum(axis=(4, 5)) > 0
        fresh = present & (self.wait_owed == 0)
        unit = MIXING_AMPLITUDE_SCALE * denominator
        debt = self.wait_debt + np.where(fresh, read * numerator, 0)
        owed = debt // unit
        self.wait_debt = debt - owed * unit
        self.wait_owed = self.wait_owed + owed

    def frozen(self) -> np.ndarray:
        """Per Node and number whether the arrivals wait this interval."""
        return self.wait_owed > 0

    def cycle(self) -> None:
        """The mixing at every Node of the arrivals that do not wait, the parked
        releases and the departures into flight; the waiting cells stay as
        arrivals for the next interval, their countdown paid by one."""
        frozen = self.frozen()
        kept = None
        if frozen.any():
            kept = (self.arr_amt[frozen].copy(), self.arr_ph[frozen].copy(), self.arr_mom[frozen].copy())
            self.arr_amt[frozen] = 0
            self.arr_ph[frozen] = 0
            self.arr_mom[frozen] = 0
        if self.arr_amt.any() or self.reg.any():
            departures, phase, departure_momenta = mix_arrivals(self, MOMENTUM_BOUND)
            released, released_phase, released_momenta = release_parked(self)
            layer_0, layer_1, phase_1, momenta_0, momenta_1 = merge_departures(
                departures, released, phase, released_phase, departure_momenta, released_momenta
            )
            place_departures(
                self, layer_0, layer_1, phase, phase_1, momenta_0, momenta_1, MOMENTUM_BOUND
            )
        self.arr_amt[...] = 0
        self.arr_ph[...] = 0
        self.arr_mom[...] = 0
        if kept is not None:
            self.arr_amt[frozen], self.arr_ph[frozen], self.arr_mom[frozen] = kept
            self.wait_owed[frozen] -= 1

    def take(self, position: Address3, rank: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """The arrivals of one number at one Node, taken out of the arrays
        (absorbed by a held content): the amounts, phases and momenta per
        Port and layer."""
        cell = (*position, rank)
        amount, phase, momentum = (
            self.arr_amt[cell].copy(),
            self.arr_ph[cell].copy(),
            self.arr_mom[cell].copy(),
        )
        self.arr_amt[cell] = 0
        self.arr_ph[cell] = 0
        self.arr_mom[cell] = 0
        return amount, phase, momentum

    def place(
        self, position: Address3, rank: int, port: int, amount: int, phase: int, momentum: np.ndarray
    ) -> None:
        """A release from a held content into the departures of its Node on one
        Port: the first free layer, or one amplitude with layer 0 when both
        layers are taken (the amounts added, the phase of the coherent sum)."""
        if amount <= 0:
            return
        cell = (*position, rank, port)
        layers = self.fly_amt[cell]
        for layer in range(LAYERS):
            if layers[layer] == 0:
                self.fly_amt[(*cell, layer)] = amount
                self.fly_ph[(*cell, layer)] = phase
                self.fly_mom[(*cell, layer)] = momentum
                return
        assert self.cosines is not None and self.sines is not None
        held, held_phase = int(layers[0]), int(self.fly_ph[(*cell, 0)])
        x = np.array(held * self.cosines[held_phase] + amount * self.cosines[phase])
        y = np.array(held * self.sines[held_phase] + amount * self.sines[phase])
        self.fly_amt[(*cell, 0)] = held + amount
        self.fly_ph[(*cell, 0)] = int(self._nearest_step(x, y))
        self.fly_mom[(*cell, 0)] += momentum
