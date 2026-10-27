"""The hand trains' bilinears, one act on every hand alike: a hand is a train of two gears, its three and its twelve (the hand's three-o'clock and twelve-o'clock shadows), with the plain products gear by gear (`products`, `dot`), a quarter turn J ((three, twelve) -> (-twelve, three)) and a reflection K (the twelve gear's negation): the sweep B.J.N (the hand's Wronskian), the lead, the pawl's reflection of a neighbour's gears, the setting at rest by rule3's signed carries and the rotation's angle read along the law's own circuit (`cosine_count`; the spinor train's Gram form, axis matrices, spin density, curl term and scale struck with the train, 2026-10-27)."""

from __future__ import annotations

from collections.abc import Callable
from functools import cache
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core.rule3 import carries, half, signed_carries, wind_weight
from event_universe.core.spokes import AXES, SPOKES, across, spoke_of
from event_universe.meshes import cross
from event_universe.readings import standard_angle
from event_universe.trains import HAND, Gear, Train, zeros

if TYPE_CHECKING:
    from event_universe.clock import Clock


def signs(size: int) -> list[int]:
    """The train's conjugation K as signs, the pawl's and the turnover's: a hand's twelve gear turned over, every gear of another train its own conjugate."""
    return [1, -1] if size == HAND else [1] * size


def seen(z: list[Any], pawl: Any) -> list[Any]:
    """A neighbour's hand read in the clock's frame, the conjugate where the pawl is -1: its twelve shadow times the pawl (a pawl is 1 or -1)."""
    three, twelve = z
    return [three, pawl * twelve]


def products(xs: list[Any], ys: list[Any]) -> list[Any]:
    """The plain products x_k y_k gear by gear, so that a carry per gear stays one per gear."""
    return [x * y for x, y in zip(xs, ys, strict=True)]


def dot(xs: list[Any], ys: list[Any]) -> Any:
    """The plain products x_k y_k summed over the gears."""
    return sum(products(xs, ys), start=0)


def sweep(gears: list[Gear]) -> Any:
    """The hand's sweep W = Im(conj(z_now) z_before) at every clock, three_now twelve_before - twelve_now three_before (meshes.cross, the hand's Wronskian)."""
    three, twelve = gears
    return cross(three.now, twelve.now, three.before, twelve.before)


def lead(nows: list[Any], pawls: list[Any]) -> list[Any]:
    """The hand's lead on each axis, J_a = Im(conj(z) (z_up - z_down)) with the neighbours read in the clock's frame (`seen`): three dtwelve - twelve dthree."""
    found = []
    for a in range(AXES):
        up = seen([across(n, spoke_of(a, 0)) for n in nows], pawls[spoke_of(a, 0)])
        down = seen([across(n, spoke_of(a, 1)) for n in nows], pawls[spoke_of(a, 1)])
        found.append(cross(*nows, *(u - d for u, d in zip(up, down, strict=True))))
    return found


@cache
def spoke_places(size: tuple[int, ...]) -> Any:
    """The six spokes' neighbour places stacked, [spoke][axis] at every clock: the great clock's own coordinates read across each spoke (`across`), unwind.neighbour at every clock at once."""
    return np.array([[across(g, spoke) for g in np.indices(size)] for spoke in range(SPOKES)])


def wind(clock: Clock, gears: list[Gear], r: Any, window: list[tuple[int, ...]] | None = None) -> Any:
    """The conserved form's wind of a hand at the clock in the regulator's unit (PM-S1: every count of the clock read in the regulator's unit, the one weight for every read and every train alike), one carry per gear: for the gear k, [w (n_k n_k + b_k b_k) - S n_k b_k - n_k (SUM_j R_j b_j)_k], doubled, less SUM_j R_j (b - b_j)_k (n + n_j)_k, times X the regulator's notch at the tick's start, over 4 Gamma^3 G^2 ((Gamma / p_i)^2 = X / Gamma to the unit; at the vacuum X = Gamma and the weight is the former vacuum's 4 Gamma^2 G^2 bit for bit); the hand's wind gear by gear, at the train's gearing. At a window of clocks (`window`, an unwind's clock and its six neighbours, unspring.fitted_windings_of and wind_fall) the same integers read at those clocks alone, each neighbour gathered by its place from the six spokes' stacked places (`spoke_places`), returned in the window's order (the former merger.share_at, gram.share's form re-spelt at one clock, folded 2026-10-26 as R3 of the readings' map: one spelling, the vectorised form inside it)."""
    at: Callable[[Any], Any]
    beyond: Callable[[Any, int], Any]
    if window is None:
        at, beyond, x = (lambda a: a), across, clock.start_stretch
    else:
        places = [tuple(np.array(w) for w in zip(*window, strict=True))]
        places += [tuple(table[(slice(None), *places[0])]) for table in spoke_places(clock.size)]

        def at(a: Any) -> Any:
            return a[places[0]] if np.ndim(a) else a

        def beyond(a: Any, spoke: int) -> Any:
            return a[places[1 + spoke]]

        x = clock.start_stretch[places[0]]
    full_n, full_b = [gear.now for gear in gears], [gear.before for gear in gears]
    nows, befores = [at(n) for n in full_n], [at(b) for b in full_b]
    gripped = [at(zeros(clock.size)) for _ in gears]
    shared = [at(zeros(clock.size)) for _ in gears]
    for spoke, grip in enumerate(r.grips):
        b_j = [beyond(b, spoke) for b in full_b]
        n_j = [beyond(n, spoke) for n in full_n]
        here = at(grip)
        gripped = [v + here * bj for v, bj in zip(gripped, b_j, strict=True)]
        parts = products(
            [b - bj for b, bj in zip(befores, b_j, strict=True)],
            [n + nj for n, nj in zip(nows, n_j, strict=True)],
        )
        shared = [s + here * part for s, part in zip(shared, parts, strict=True)]
    own = [
        at(r.teeth) * (nn + bb) - at(r.hold) * nb - nr
        for nn, bb, nb, nr in zip(
            products(nows, nows),
            products(befores, befores),
            products(nows, befores),
            products(nows, gripped),
            strict=True,
        )
    ]
    teeth = wind_weight(clock.full_rate, clock.G) + wind_weight(clock.full_rate, clock.G)
    found = at(zeros(clock.size))
    for o, s in zip(own, shared, strict=True):
        found = found + np.asarray(carries((o + o - s) * x, teeth))
    return found


def moving(
    base: Any, now_pair: tuple[Any, Any], before_pair: tuple[Any, Any], rim: int, sense: int
) -> list[Gear]:
    """A hand set at an angle over the envelope (MV-S1), its two shadows at the angle (C, S): now = (base C, sense base S) over the rim at the clock's angle pair (C, S) and before the same at the pair (C', S') turned by the band's rotation, each product's carries toward zero gear by gear (rule3.signed_carries), so the two senses' twelve gears cancel exactly and the setting at the conjugate pair is the conjugate setting; the rest setting the case (rim, 0) and (pinion, s) (the former lay's vector, (1, 0) on every hand, struck with the spinor train, 2026-10-27)."""

    def hand(c: Any, s: Any) -> list[Any]:
        return [signed_carries(base * c, rim), sense * signed_carries(base * s, rim)]

    return [Gear(n, b, None, None) for n, b in zip(hand(*now_pair), hand(*before_pair), strict=True)]


def rest(three_now: Any, pinion: int, rim: int, sine: int, sense: int) -> list[Gear]:
    """A hand at rest over the envelope (`moving` at the pair (rim, 0) now and the train's (pinion, s) before): three_now = three_now, twelve_now = 0, three_before = three_now pinion div rim, twelve_before = sense three_now s div rim, the carries taken toward zero."""
    return moving(three_now, (rim, 0), (pinion, sine), rim, sense)


def cosine_count(clock: Clock, p: int, d: int) -> int:
    """The count n along the law's circuit (features/standard, the step 1 / Gamma) at which the circuit's cosine first falls to p / d, the rotation's angle in the circuit's units: a search by comparisons, cos_n d <= p X, bounded by the circuit's half turn where the table reaches it (the deepest cosine the circuit holds)."""
    high = 1
    while standard_angle(clock, high)[0] * d > p * clock.standard_length and (
        clock.circuit_half is None or high < clock.circuit_half
    ):
        high = high + high
    high = high if clock.circuit_half is None else min(high, clock.circuit_half)
    low = 0
    while high - low > 1:
        middle = half(low + high)
        if standard_angle(clock, middle)[0] * d > p * clock.standard_length:
            low = middle
        else:
            high = middle
    return high


def twin_pairs(hands: list[Train]) -> list[tuple[int, int]]:
    """The twin hands' pairs as (up, down), the up twin the first of its train's two hands."""
    return [(u, twin_of(hands, u)) for u in range(len(hands)) if twin_of(hands, u) > u]


def twin_of(hands: list[Train], s: int) -> int:
    """The + fitted hand's hand: the twin of the - fitted hand's hand where its train is twin hands (the pair's spin kept), the same hand otherwise."""
    twin = hands[s].twin
    return s if twin is None else hands.index(twin)
