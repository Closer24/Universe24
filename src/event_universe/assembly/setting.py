"""The setting as the piece's file sets it: a list of settings in the five forms of the law (the owner's word of 2026-10-25; the fourth, the even setting, by his word of 17:57 UTC; the fifth, the light's cycle setting, by his word of 22:50 UTC, CS5-S2): `sea` sets the unsprung hand's drift v, the largest integer with v^2 <= T, at every clock; `hole` takes it back at one clock; `at` sets a packet, on the unsprung hand N drifts at the centre, on a sprung hand the conjugate pair over the raised cosine's envelope of the half-width 2 or 3, at rest or, with the field `wave` [h_x, h_y, h_z] in the rim's unit (h_a = rim sin(k_a / 2)), moving at the band's rotation at that stride with the optional flat `top` along the stride's axis (MV-S1 to MV-S3, 2026-10-25; one path for every hand, the unsprung hand with a stride among them, with none the drift by name); `wave` sets the light's cycle pattern at every clock (CS5-S2's piece, the owner's word of 2026-10-25, 22:50 UTC: cs3's cycle form in cs5's and cs7's spelling, `row` the unsprung hand, `quanta` n, `p1` sixteen digits of Z_4 and `cz` one, the angle p(x, y, z) = (p1[4 (x mod 4) + (y mod 4)] + cz z) mod 4, `mirror` 0 or 1 for the negated gears' fine teeth). Refused by name: a form beyond these, a field of no form (an `interval` key among them), a setting onto a train that is no hand, a sea of a sprung hand, a clock off the great clock, a packet of another width, a stride beyond the band's edge (|h| above the rim), an unsprung packet at the stride 0, a top not fitting the great clock, a cycle setting off the unsprung hand or on a cube whose extent is not a multiple of 4, its digits off Z_4, its flip off 0 and 1."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import hands, readings, unwind
from event_universe.assembly.cycle import set_cycle
from event_universe.core.acts import carry, mid
from event_universe.core.rates import rounded, sine_rim
from event_universe.core.rule3 import carries, half, largest_below, least_at, odd
from event_universe.core.spokes import AXES, wrap
from event_universe.meshes import factors, offset_pair
from event_universe.run import logged
from event_universe.trains import REGULATOR, Gear, Train, zeros

if TYPE_CHECKING:
    from event_universe.clock import Clock

HALF_SPANS = (
    1,
    2,
    3,
)  # the envelope's half spans the raised cosine knows (the setting's `width`; 1 the one clock, a fitted pair's own form)
FIELDS = {  # the fields of each form of the law; a field of no form is refused by name (MV-S3)
    "sea": frozenset({"lay", "row", "quanta", "sense", "hand"}),
    "hole": frozenset({"lay", "at"}),
    "at": frozenset({"lay", "row", "centre", "quanta", "width", "sense", "wave", "top", "hand"}),
    "wave": frozenset({"lay", "row", "quanta", "p1", "cz", "mirror"}),
}
Ratio = tuple[Any, Any]


def set_piece(clock: Clock, setting: list[dict[str, Any]]) -> None:
    """Every setting of the piece's file onto the clock's trains, the packets after the sea and the holes; a setting of no form and a field of no form refused by name (MV-S3: the assembly sets the hands before the first tick and nothing after)."""
    packets = []
    for lay in setting:
        form = lay.get("lay")
        if form not in FIELDS:
            raise ValueError(f"a lay of no form of the law: {form!r}")
        beyond = sorted(set(lay) - FIELDS[form])
        if beyond:
            raise ValueError(f"a field of no form of the law in the lay {form!r}: {', '.join(beyond)}")
        train = clock.by_index[int(lay["row"])] if "row" in lay else None
        if "hand" in lay:
            if train is None or train.twin is None or int(lay["hand"]) not in (0, 1):
                raise ValueError("a lay names a hand of a train of twin hands: 0 or 1")
            train = train if int(lay["hand"]) == 0 else train.twin
        if train is not None and train not in clock.hands():
            raise ValueError("a lay is onto a record (a plane)")
        if form == "sea" and "quanta" not in lay:
            if train is None or train is not clock.unsprung() or "sense" in lay:
                raise ValueError(
                    "a sea without a count is the plane at the gap 0 alone (the drift, no sense); a plane with a gap names its quanta (the fourth form)"
                )
            unwind.advance(clock, clock.hands().index(train), Ellipsis, (clock.drift, 0, 0, 0))
        elif form == "sea":
            if train is None or train is clock.unsprung():
                raise ValueError(
                    "the fourth form lays a plane with a gap at a count: the plane at the gap 0 alone is the drift"
                )
            set_even(clock, clock.hands().index(train), int(lay["quanta"]), int(lay.get("sense", 0)))
        elif form == "hole":
            at = clock.clock_of(lay["at"])
            unwind.advance(clock, clock.hands().index(clock.unsprung()), at, (-clock.drift, 0, 0, 0))
        elif form == "wave":
            if train is None or train is not clock.unsprung() or "quanta" not in lay:
                raise ValueError("the cycle lay is the light's: the plane at the gap 0 at its quanta")
            digits = [int(v) for v in lay.get("p1", [])] + [int(lay.get("cz", 1))]
            set_cycle(
                clock, clock.hands().index(train), int(lay["quanta"]), digits, int(lay.get("mirror", 0))
            )
        else:
            n = int(lay["quanta"])
            at = clock.clock_of(lay["centre"])
            if train is None:
                raise ValueError("a packet names its row")
            stride = None if lay.get("wave") is None else tuple(int(x) for x in lay["wave"])
            if train is clock.unsprung() and stride is None:
                unwind.advance(clock, clock.hands().index(train), at, (n * clock.drift, 0, 0, 0))
            else:
                packets.append(
                    (
                        clock.hands().index(train),
                        at,
                        int(lay.get("width", 0)),
                        n,
                        lay.get("sense"),
                        stride,
                        int(lay.get("top", 1)),
                    )
                )
    for rec, at, h, n, sense, stride, top in packets:
        set_packet(clock, rec, at, h, n, sense, stride, top)
    quantum = half(clock.key)
    for hand in (h for h in clock.hands() if h.twin is not None):
        if any(abs(int(w)) >= quantum + quantum for w in hands.sweep(hand.gears).flat):
            raise ValueError(
                "Pauli at the setting: a twin hand sweeps two quanta at a clock, refused by name"
            )


def raised_cosine(h: int) -> tuple[int, ...]:
    """The raised cosine's weights over the half-width h, w_k = 2 + 2 cos(pi k / h) for k = 0 .. h - 1, exact in integers where 2 cos(pi / h) is an integer, at h = 1 (-2, the one clock at the crest's weight 4: a fitted pair's own form set from a file, the Boss's 6414464356), h = 2 (0) and h = 3 (1) and at no other width: the doubled cosines by the Chebyshev recurrence t_(k+1) = t_1 t_k - t_(k-1) from t_0 = 2 (the weights 2, 1 and 4, 3, 1); another width refused by name."""
    if h not in HALF_SPANS:
        raise ValueError(
            "a packet has the half-width 1 (the one Node), 2 or 3: a body is laid over its packet"
        )
    doubled = [1 + 1, h - 1 - 1]
    while len(doubled) < h:
        *_, before, last = doubled
        doubled.append(doubled[1] * last - before)
    return tuple(1 + 1 + t for t in doubled[:h])


def places(h: int, half_tops: tuple[int, ...]) -> list[tuple[int, ...]]:
    """Every place of the envelope about the centre, along each axis from -(h - 1 + its half top) to h - 1 + its half top."""
    reach = [h - 1 + t for t in half_tops]
    return [tuple(j[a] - reach[a] for a in range(AXES)) for j in np.ndindex(*(r + r + 1 for r in reach))]


def envelope_of(
    clock: Clock, at: tuple[int, ...], h: int, half_tops: tuple[int, ...] = (0,) * AXES
) -> tuple[Any, int]:
    """The raised cosine's envelope of the half-width h about the clock, the product of the weights over the three axes, flat at the centre's weight over the half top of each axis given one (MV-S1's `top`, 0 the former envelope), and the centre's weight."""
    weights = raised_cosine(h)
    envelope = zeros(clock.size)
    for off in places(h, half_tops):
        where = tuple(wrap(at[a] + off[a], clock.cube) for a in range(AXES))
        weight = 1
        for a in range(AXES):
            weight *= weights[max(abs(off[a]) - half_tops[a], 0)]
        envelope[where] += weight
    return envelope, weights[0] ** AXES


def rim_point(rim: int, h: int) -> tuple[int, int]:
    """The point of the rim at the half-angle sine h (MV-S1, the stride's unit): rim cos k = (rim^2 - 2 h^2) over rim and rim sin k = 2 h largest_below(rim^2 - h^2) over rim, each rounded once with the sign after (rates.rounded), so the point at -h is the conjugate; (rim, 0) at h = 0, (-rim, 0) at |h| = rim, the band's edge (MV-S2); beyond it refused by name."""
    if abs(h) > rim:
        raise ValueError(f"a wave number beyond the band's edge: |h| {abs(h)} above den {rim}")
    return (
        int(rounded(rim * rim - (h + h) * h, rim)),
        int(rounded((h + h) * largest_below(rim * rim - h * h), rim)),
    )


def axis_pairs(rim: int, point: tuple[int, int], reach: int) -> dict[int, tuple[int, int]]:
    """The pair over the rim at every place from -reach to reach along one axis: from (rim, 0) at the centre, the axis's point composed one mesh at a time (meshes.offset_pair, one odd rounding per part per mesh), the conjugate point for a negative place, so the pair at -n is the conjugate of the pair at n."""
    found = {0: (rim, 0)}
    for side in (1, -1):
        for n in range(1, reach + 1):
            three, twelve = found[side * (n - 1)]
            pair = offset_pair(three, twelve, point[0], side * point[1], rim)
            found[side * n] = (int(pair[0]), int(pair[1]))
    return found


def angle_of(rim: int, pairs: list[tuple[int, int]]) -> tuple[int, int]:
    """The pair over the rim at a clock from its three axes' pairs, composed in their sorted order (two turns, one odd rounding per part each): the same integers at every image of the clock under the 48, the axes' pairs permuted with the axes and each one even under its axis's reflection with the stride."""
    first, second, third = sorted(pairs)
    three, twelve = offset_pair(first[0], first[1], second[0], second[1], rim)
    three, twelve = offset_pair(three, twelve, third[0], third[1], rim)
    return int(three), int(twelve)


def angles_of(
    clock: Clock,
    at: tuple[int, ...],
    h: int,
    half_tops: tuple[int, ...],
    points: list[tuple[int, int]],
) -> Ratio:
    """The angle pair (C, S) over the rim at every clock of the envelope, the three axes' pairs at the clock's places (axis_pairs) composed (angle_of); (rim, 0) beyond the envelope and everywhere at the stride 0."""
    rim = clock.rim
    along = [axis_pairs(rim, points[a], h - 1 + half_tops[a]) for a in range(AXES)]
    cosine, sine = zeros(clock.size) + rim, zeros(clock.size)
    for off in places(h, half_tops):
        where = tuple(wrap(at[a] + off[a], clock.cube) for a in range(AXES))
        cosine[where], sine[where] = angle_of(rim, [along[a][off[a]] for a in range(AXES)])
    return cosine, sine


def running_rotation(pinion: int, rim: int, points: list[tuple[int, int]]) -> tuple[int, int]:
    """The band's rotation at the stride (the kinetic clause): rim cos omega(k) = (pinion SUM_a rim cos k_a) div (3 rim) and its sine by the one search (rates.sine_rim's form); the train's own pair (pinion, s) at the stride 0, (rim, 0) for the unsprung train there, the double root with no rotation."""
    cosine = int(carries(pinion * sum(c for c, _s in points), AXES * rim))
    return cosine, sine_rim(cosine, rim)


def rest_hand(
    clock: Clock,
    train: Train,
    envelope: Any,
    w0: int,
    hand_length: int,
    sense: int,
    pairs: tuple[Ratio, Ratio] | None = None,
) -> list[Gear]:
    """A hand over the envelope at a hand length, base = A w_i div w_0: at rest (hands.rest) the hand's three_now = base, three_before = base pinion div rim, twelve_now = 0, twelve_before = sense base s div rim with s the ratio's sine; at a stride (hands.moving) the base at the clock's angle pair now and at that pair turned by the band's rotation before."""
    assert train.ratio is not None
    pinion = train.ratio[0]
    base = carries(hand_length * envelope, w0)
    if pairs is None:
        return hands.rest(base, pinion, clock.rim, sine_rim(pinion, clock.rim), sense)
    return hands.moving(base, pairs[0], pairs[1], clock.rim, sense)


def carried_rest(clock: Clock, rec: int, lays: list[tuple[list[Gear], list[Any]]]) -> None:
    """The rest lay carried (DAVID-AMPLITUDES.md section 3, the owner's word of 2026-10-27, 15:5x UTC): at the clocks the rest lays touched, each gear's before and fine tooth from one carry of the lays' own rest numerator N (base pinion on the three gear, sense base s on the twelve), V = teeth now - (teeth div rim) N + mid(teeth), before = now - V div teeth, fine = V mod teeth, so the lay's push is the rest push exactly, counted in the fine wheel's teeth (the former before laid toward zero beside a mid tooth ran a slow hand off at up to one notch a tick)."""
    shifts = []
    for k, gear in enumerate(clock.hands()[rec].gears):
        now = sum(gears[k].now for gears, _ in lays)
        before = sum(gears[k].before for gears, _ in lays)
        numerator = sum(numerators[k] for _, numerators in lays)
        total = gear.teeth * now - carries(gear.teeth, clock.rim) * numerator
        carried, fine = carry(total, gear.teeth, mid(gear.teeth))
        touched = (np.asarray(now) != 0) | (np.asarray(numerator) != 0)
        shifts += [0 * now, np.where(touched, now - carried - before, 0)]
        gear.fine = np.where(touched, fine, gear.fine)
    unwind.advance(clock, rec, Ellipsis, tuple(shifts))


def rest_numerators(
    clock: Clock, train: Train, envelope: Any, w0: int, hand_length: int, sense: int
) -> list[Any]:
    """A rest lay's own numerators per gear, the rest turn's before over the rim before its carry: base pinion on the three gear, sense base s on the twelve (the carried lay's N)."""
    assert train.ratio is not None
    base = carries(hand_length * envelope, w0)
    return [base * train.ratio[0], sense * base * sine_rim(train.ratio[0], clock.rim)]


def even_notches(clock: Clock, train: Train, hand_length: int, sense: int) -> list[Gear]:
    """The fourth form's notches at a hand length (MA-S1, ma2's spelling): one hand at rest at every clock (rest_hand with the envelope 1 and the centre's weight 1) at the sense -1 or 1, or the conjugate pair at 0 (both senses summed, the twelve gears cancelling)."""
    if sense == 0:
        a = even_notches(clock, train, hand_length, 1)
        b = even_notches(clock, train, hand_length, -1)
        return [Gear(x.now + y.now, x.before + y.before, None, None) for x, y in zip(a, b, strict=True)]
    return rest_hand(clock, train, zeros(clock.size) + 1, 1, hand_length, sense)


def wind_at_clock(clock: Clock, train: Train, gears: list[Gear], gearing: Any) -> int:
    """A hand's wind at the vacuum's weight at the clock of the great clock's first index, the even setting's wind at every clock alike."""
    return int(hands.wind(clock, gears, gearing).reshape(-1)[0])


def swept(clock: Clock, train: Train, hand_length: int, sense: int) -> int:
    """An even lay's sweep at the clock of the great clock's first index, each sense laid its own |W| (the conjugate pair's two senses summed, never cancelled): the count a sweeping hand's n quanta name (DAVID-AMPLITUDES.md section 7, the owner's word of 2026-10-27, 15:5x UTC), the setting's count, the sweep and Pauli's count one count."""
    senses = (1, -1) if sense == 0 else (sense,)
    return sum(abs(int(hands.sweep(even_notches(clock, train, hand_length, s)).flat[0])) for s in senses)


def set_even(clock: Clock, rec: int, n: int, sense: int) -> None:
    """The fourth form set: the sprung hand at every clock alike at the least hand length whose wind at the vacuum's weight is at or above n windings at every clock (ma2's fitted_uniform: the search by comparisons, doubling then halving, its answer plus one), at the sense -1 or 1 or the conjugate pair at 0; the setting logged."""
    train = clock.hands()[rec]
    assert train.ratio is not None
    clock.start_load, clock.start_stretch = readings.load(clock), clock.train(REGULATOR).gears[0].now
    gearing = readings.gearing(clock, train.ratio, clock.start_load, factors(clock))
    target, e, s = n * clock.windings[rec], half(clock.key), sine_rim(train.ratio[0], clock.rim)
    hand_length = least_at(
        lambda a: (
            wind_at_clock(clock, train, even_notches(clock, train, a, sense), gearing) > target
            if s == 0
            else swept(clock, train, a, sense) >= n * e
        )
    )
    gears = even_notches(clock, train, hand_length, sense)
    unwind.advance(clock, rec, Ellipsis, tuple(x for gear in gears for x in (gear.now, gear.before)))
    one = zeros(clock.size) + 1
    senses = (1, -1) if sense == 0 else (sense,)
    carried_rest(
        clock,
        rec,
        [
            (
                gears,
                [
                    sum(x)
                    for x in zip(
                        *(rest_numerators(clock, train, one, 1, hand_length, s) for s in senses),
                        strict=True,
                    )
                ],
            )
        ],
    )
    logged(
        clock,
        "lay",
        None,
        line_pair=rec,
        quanta=n,
        amplitude=hand_length,
        share=wind_at_clock(clock, train, gears, gearing),
        unit=clock.windings[rec],
        nodes=int(clock.cube) ** AXES,
        sense=sense,
    )


def packet_wind(clock: Clock, train: Train, gears: list[Gear], gearing: Any) -> int:
    """A hand's wind at the vacuum's weight summed over the great clock."""
    return int(sum(int(x) for x in hands.wind(clock, gears, gearing).reshape(-1)))


def fitted(
    clock: Clock,
    train: Train,
    envelope: Any,
    w0: int,
    target: int,
    pairs: tuple[Ratio, Ratio] | None = None,
) -> int:
    """The largest hand length at which the hand's wind at the vacuum's weight, summed over the packet, is at most the target (a search by comparisons, doubling then halving)."""
    assert train.ratio is not None
    gearing = readings.gearing(clock, train.ratio, readings.load(clock), factors(clock))
    sine = sine_rim(train.ratio[0], clock.rim)

    def count_of(hand_length: int) -> int:
        gears = rest_hand(clock, train, envelope, w0, hand_length, 1, pairs)
        if sine == 0:
            return packet_wind(clock, train, gears, gearing)
        return sum(abs(int(w)) for w in hands.sweep(gears).flat)

    return least_at(lambda hand_length: count_of(hand_length) > target) - 1


def stride_of(
    clock: Clock, train: Train, h: int, stride: tuple[int, ...], top: int
) -> tuple[tuple[int, ...], list[tuple[int, int]], tuple[int, int]]:
    """The moving setting's integers from its two fields: the half top per axis (the flat top of `top` clocks along the axes of the stride's largest |h|, refused by name where the top is not an odd count or does not fit the great clock with the raised cosine's edges), the rim's point per axis (rim_point, |h| above the rim refused there) and the band's rotation (running_rotation, the unsprung train at the stride 0 refused by name: its sine 0, the drift its setting)."""
    assert train.ratio is not None
    if len(stride) != AXES:
        raise ValueError("a wave number is three integers, one per axis")
    if top < 1 or not odd(top) or top + (h - 1) + (h - 1) > clock.cube:
        raise ValueError(
            "a top is an odd count of Nodes about the centre that fits the board with its edges"
        )
    largest = max(abs(x) for x in stride)
    half_tops = tuple(int(half(top - 1)) if abs(x) == largest else 0 for x in stride)
    points = [rim_point(clock.rim, int(x)) for x in stride]
    rotation = running_rotation(train.ratio[0], clock.rim, points)
    if rotation[1] == 0:
        raise ValueError("a packet of the gap-0 row at the wave 0 has no rotation: the drift is its lay")
    return half_tops, points, rotation


def set_packet(
    clock: Clock,
    rec: int,
    at: tuple[int, ...],
    h: int,
    n: int,
    one_sense: int | None = None,
    stride: tuple[int, ...] | None = None,
    top: int = 1,
) -> None:
    """The `at` setting of a sprung hand (or of the unsprung hand at a stride): the conjugate pair (the two hands at the senses -1 and 1 where the setting names no sense or the sense 0, EM-S2; the one hand at the sense -1 or 1 named) set over the envelope, at rest where the setting names no stride (`rest_hand`, the former setting by name) or at the stride (MV-S1: the angle pair composed one mesh at a time from the rim's point per axis, the notch before at the band's rotation, `stride_of`, `angles_of`; the stride 0 the rest setting bit for bit) with the flat `top` (1 the former envelope), each hand at the largest hand length whose wind, summed over the packet, is at most n windings (`fitted`); the setting logged."""
    train = clock.hands()[rec]
    assert train.ratio is not None
    named: dict[str, Any] = {"sense": int(one_sense or 0)}
    half_tops: tuple[int, ...] = (0,) * AXES
    pairs, moving = None, stride is not None and any(int(x) != 0 for x in stride)
    if stride is not None:
        half_tops, points, rotation = stride_of(clock, train, h, stride, top)
        named |= {"wave": [int(x) for x in stride], "top": int(top)}
    envelope, w0 = envelope_of(clock, at, h, half_tops)
    if moving:
        angles = angles_of(clock, at, h, half_tops, points)
        pairs = (angles, offset_pair(angles[0], angles[1], rotation[0], rotation[1], clock.rim))
    clock.start_load, clock.start_stretch = readings.load(clock), clock.train(REGULATOR).gears[0].now
    sweeping = sine_rim(train.ratio[0], clock.rim) != 0
    hand_length = fitted(
        clock, train, envelope, w0, n * (half(clock.key) if sweeping else clock.windings[rec]), pairs
    )
    lays = []
    for sense in (-1, 1) if not one_sense else (int(one_sense),):
        gears = rest_hand(clock, train, envelope, w0, hand_length, sense, pairs)
        unwind.advance(clock, rec, Ellipsis, tuple(x for gear in gears for x in (gear.now, gear.before)))
        lays.append((gears, rest_numerators(clock, train, envelope, w0, hand_length, sense)))
    if pairs is None:
        carried_rest(clock, rec, lays)
    gears = rest_hand(clock, train, envelope, w0, hand_length, 1, pairs)
    gearing = readings.gearing(clock, train.ratio, clock.start_load, factors(clock))
    logged(
        clock,
        "lay",
        at,
        line_pair=rec,
        width=h,
        quanta=n,
        amplitude=hand_length,
        share=packet_wind(clock, train, gears, gearing),
        unit=clock.windings[rec],
        nodes=int(sum(1 for x in envelope.reshape(-1) if int(x) > 0)),
        **named,
    )
