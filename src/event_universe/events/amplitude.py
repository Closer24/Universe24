"""The apparatus's layer of the amplitude law (`amplitude-v1`; the model
owner, 2026-09-20, Highlights 5.4, "DECIDED: `amplitude-v1` is built"; the
ten principles, (4) and (5); the physicist's and the mathematician's
design, scratchpad/amplitude/DESIGN.md, sections 1.2, 3, 4 and 5;
docs/BEAM_LAW.md note 37).

The world is the list of clicks. The lattice computes every path of a
record (`nature_beam`: the flight, the collision, the split, the merge with
its cancel), and the layer, host state owned by the apparatus, reads the
record's OFFERS where its rows end (a click at a set, an open face, the
border `lifetime`) and, at the record's COMPLETION (every unit of the
record ended: its live count reaches 0 through the apparatus's Port
events, the births, the splits, the ends and the cancels the merge
reports), chooses one offer by the record's birth phase u on the ladder
of the offers' weights, normalised by their sum, the rungs at the nearest
integer (the owner's decision (a)):

    b_k = (2 N C_k + Total) // (2 Total),   b_0 = 0, b_K = N,

the click the cell k with b_{k-1} <= u < b_k. No draw at the detector: the
randomness is the clock of the birth; over births, Born. The lattice never
reads the layer, and the layer reads the lattice only through the
apparatus's events (principle 5: the only non-local operation, at the
one-way border, owned by the apparatus).

An offer is a (set, arm) of the record: the accumulated pointer per label,
`(X, Y) += sum 32 w (C[p], S[p])` over the rows of that label that ended
there (the same first moment over the circle as `coherent_pointer`, the
scope one record and label in place of the crowd: the owner's unification
(4)), and the RESIDUAL per channel and label after the set's reading: a
plain set offers one channel per label (the which-path click), a `sum`
set with a window rotates the arm's bit of the joint label by the
half-angle tables of 2N at its setting s (`U_s = [[C', S' v(t)], [-S',
C' v(t)]]` in 1/256^2, t the entry's turn) and offers the channels + and -
(the label click, section 4.1); a `read` at a `sum` set is a which-path
reading whose rows go on, a factor that selects the label without a
pointer. The joint amplitude of a cell (one channel per read factor and
one (end, channel) per arm) is `sum_l w_l x prod_k residual_k[c_k][l]`,
complex integers, its weight `|amplitude|^2 / m` with m the product of the
arms' multiplicities over the birth norms they share; the cells in the
lexicographic order of the arms (each arm's read factors in the sets'
order, then its ends in the sets' order, the channels + before - and the
labels ascending); the sets in the design's order (the measured events
outside every declared detector by number, the declared detectors, the
faces in Port order, the border). Python integers throughout: a report
of the host, exact, never refused (a record's weights can pass 2^64).
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

from event_universe.core.phase import PHASE_COSINE_SCALE, phase_cosines, phase_sines
from event_universe.events.measured import DetectorSet

Complex = tuple[int, int]
# The amplitude of one unit in 32nds, as the detector's record reads it
# (`nature_beam.AMPLITUDE_SCALE`; spelled here so that the layer imports
# nothing of the law).
AMPLITUDE_SCALE = 32
# The identity entry of a plain set's residual: the rotation's entries are
# in 1/256^2, so a set that rotates nothing scales by 256^2, and every
# arm's factors are in one unit.
IDENTITY = PHASE_COSINE_SCALE * PHASE_COSINE_SCALE
# The joint label of a row is its `branch` column: the label in the low
# 32 bits, the arm it flies on above them.
LABEL_BITS = 32
# The unit of a weight's numerator: the square of one row of amount 1 at
# the identity rotation, (32 x 256 x 256^2)^2 = 2^58; a record's `total`
# over this unit is its norm as offered (1 up to the tables' rounding and
# the cross terms of paths meeting at one set).
UNIT = (AMPLITUDE_SCALE * PHASE_COSINE_SCALE * IDENTITY) ** 2
LABEL_MASK = (1 << LABEL_BITS) - 1
PLUS, MINUS = 0, 1
CHANNEL_NAMES = {PLUS: "+", MINUS: "-"}


def cmul(a: Complex, b: Complex) -> Complex:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cadd(a: Complex, b: Complex) -> Complex:
    return (a[0] + b[0], a[1] + b[1])


def arm_of(branch: int) -> int:
    return branch >> LABEL_BITS


def label_of(branch: int) -> int:
    return branch & LABEL_MASK


def branch_of(arm: int, label: int) -> int:
    return (arm << LABEL_BITS) | label


def gcd(a: int, b: int) -> int:
    """Euclid on Python integers: the layer's sums are the host's reports,
    exact and unbounded (a record's weights can pass 2^64)."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b) if a and b else max(a, b)


def rungs(weights: list[tuple[int, int]], steps: int) -> tuple[list[int], tuple[int, int]]:
    """The ladder (the design's section 3.3): the cells' weights as pairs
    (numerator, multiplicity), the cumulative C_k over the common
    denominator D and the rungs b_k = (2 N C_k + Total) // (2 Total) at
    the nearest integer, b_K = N; returns the rungs and the total as the
    reduced pair. Every u = 0 .. N - 1 falls in exactly one cell; an offer
    below Total / 2N may get an empty cell."""
    denominator = 1
    for _, m in weights:
        denominator = lcm(denominator, m)
    scaled = [n * (denominator // m) for n, m in weights]
    total = sum(scaled)
    if total == 0:
        return [0] * len(weights), (0, 1)
    found = []
    cumulative = 0
    for value in scaled:
        cumulative += value
        found.append((2 * steps * cumulative + total) // (2 * total))
    common = gcd(total, denominator) or 1
    return found, (total // common, denominator // common)


def choose(found: list[int], u: int) -> int | None:
    """The cell of u: the first k with u < b_k (b_{k-1} <= u by the
    rungs' monotony); None when the ladder is empty."""
    for k, b in enumerate(found):
        if u < b:
            return k
    return None


@dataclass
class Offer:
    """One offer of a record: the rows of the record that ended at one set
    on one arm (`read` False), or were read there and went on (`read`
    True, a which-path factor). `pointers` the accumulated pointer per
    label (Python integers); `residuals` per channel the complex residual
    per label after the set's reading; `multiplicity` the rows' m at the
    set (the rows of one offer share it, refused otherwise); `rotated`
    whether the set rotated the labels (the channels + and -), else the
    channels are the labels."""

    set_index: int
    arm: int
    read: bool = False
    rotated: bool = False
    # The rotation's (setting, turn) of a rotated offer (the first end's;
    # the set's setting is one per group).
    setting: tuple[int, int] | None = None
    multiplicity: int | None = None
    pointers: dict[int, Complex] = field(default_factory=dict)
    residuals: dict[int, dict[int, Complex]] = field(default_factory=dict)
    units: int = 0
    last_tick: int = 0

    def channels(self) -> list[int]:
        return sorted(self.residuals)

    def channel_name(self, channel: int) -> str:
        return CHANNEL_NAMES[channel] if self.rotated else str(channel)


@dataclass
class LiveRecord:
    """The layer's table entry of one record (the design's section 1.2):
    its identity, its family, the birth phase u, the tick of the birth,
    the birth norm T = sum of the branches' weights squared (a report; the
    ladder is normalised by the total of the offers), the joint labels with
    their weights, the arms, the birth norm of every arm's origin, the live
    count in units, the offers and, once gathered, the gather."""

    identity: int
    family: int
    u: int
    born: int
    norm: int
    labels: dict[int, int]
    arms: int
    arm_norms: list[int]
    live: int = 0
    offers: dict[tuple[int, int], Offer] = field(default_factory=dict)
    gathered: bool = False
    gather: dict[str, object] | None = None
    ends: int = 0
    last_end: int = 0

    def offer(self, set_index: int, arm: int, read: bool) -> Offer:
        key = (set_index, arm)
        found = self.offers.get(key)
        if found is None:
            found = Offer(set_index, arm, read)
            self.offers[key] = found
        return found


class Layer:
    """The apparatus's layer: the sets in the design's order (`names`), the
    live records and the world's list of gathers."""

    def __init__(
        self,
        names: list[str],
        keys: list[tuple[str, int]],
        sets: list[DetectorSet],
        families: list[str],
        phase_steps: int,
    ) -> None:
        # The sets in the design's order: their names, their keys (("set",
        # the detector set's index), ("face", the Port), ("border", 0)),
        # the detector sets themselves and the indices by kind.
        self.names = names
        self.keys = keys
        self.sets = sets
        self.families = families
        self.set_index = {key[1]: index for index, key in enumerate(keys) if key[0] == "set"}
        self.face_index = {key[1]: index for index, key in enumerate(keys) if key[0] == "face"}
        self.border_index = next((index for index, key in enumerate(keys) if key[0] == "border"), -1)
        self.steps = phase_steps
        self.cosines = phase_cosines(phase_steps)
        self.sines = phase_sines(phase_steps)
        self.half_cosines = phase_cosines(2 * phase_steps)
        self.half_sines = phase_sines(2 * phase_steps)
        self.records: dict[int, LiveRecord] = {}
        self.aliases: dict[int, int] = {}
        self.gathers: list[dict[str, object]] = []
        self.born = 0
        self.completed = 0

    # -- the apparatus's events ------------------------------------------------

    def resolve(self, identity: int) -> LiveRecord | None:
        """The record an identity names, through the gate's aliases."""
        while identity in self.aliases:
            identity = self.aliases[identity]
        return self.records.get(identity)

    def birth(
        self,
        tick: int,
        identity: int,
        family: int,
        u: int,
        labels: dict[int, int],
        arms: int,
        units: int,
    ) -> LiveRecord:
        """A new record: u, its labels and weights, its arms, its live count."""
        norm = sum(w * w for w in labels.values())
        found = LiveRecord(identity, family, u, tick, norm, dict(labels), arms, [norm] * arms, units)
        self.records[identity] = found
        self.born += 1
        return found

    def split(self, identity: int, absorbed: int, born: int) -> None:
        """A split: the units absorbed at the re-emitter and the units born
        again (+ (k - 1) per unit for an equal k-way split)."""
        found = self.resolve(identity)
        if found is not None:
            found.live += born - absorbed

    def cancel(self, identity: int, amount: int) -> None:
        """The merge's cancel: the units removed end without an offer."""
        found = self.resolve(identity)
        if found is not None:
            found.live -= amount

    def end(
        self,
        tick: int,
        set_index: int,
        identity: int,
        branch: int,
        multiplicity: int,
        amount: int,
        phase: int,
        absorbed: bool = True,
        rotation: tuple[int, int] | None = None,
    ) -> None:
        """Rows of a record that ended at a set (`absorbed`: a click, a
        face, the border; the units leave the live count) or were read
        there and went on (a which-path factor): the offer at (set, arm)
        accumulates their pointer and the residual per channel. A gathered
        record's rows are dropped (the lazy deletion, section 9)."""
        found = self.resolve(identity)
        if found is None:
            return
        if absorbed:
            found.live -= amount
            found.ends += amount
            found.last_end = tick
        if found.gathered:
            return
        arm, label = arm_of(branch), label_of(branch)
        offer = found.offer(set_index, arm, not absorbed)
        offer.last_tick = tick
        if absorbed:
            if offer.multiplicity is None:
                offer.multiplicity = multiplicity
            elif offer.multiplicity != multiplicity:
                raise ValueError(
                    f"amplitude-v1: the rows of the record {identity} at the set "
                    f"{self.names[set_index]} carry the multiplicities {offer.multiplicity} and "
                    f"{multiplicity}: one multiplicity per offer (the design's section 3.1)"
                )
            offer.units += amount
            weight = AMPLITUDE_SCALE * amount
            pointer: Complex = (weight * self.cosines[phase], weight * self.sines[phase])
            offer.pointers[label] = cadd(offer.pointers.get(label, (0, 0)), pointer)
            if rotation is None:
                channel = offer.residuals.setdefault(label, {})
                channel[label] = cadd(channel.get(label, (0, 0)), cmul((IDENTITY, 0), pointer))
            else:
                offer.rotated = True
                if offer.setting is None:
                    offer.setting = rotation
                for channel_index, entry in enumerate(self.rotation(rotation, (label >> arm) & 1)):
                    channel = offer.residuals.setdefault(channel_index, {})
                    channel[label] = cadd(channel.get(label, (0, 0)), cmul(entry, pointer))
        else:
            # A read: the factor selects the label, once per label present.
            offer.residuals.setdefault(label, {})[label] = (IDENTITY, 0)

    def rotation(self, setting: tuple[int, int], bit: int) -> tuple[Complex, Complex]:
        """The column `bit` of U_s = [[C', S' v(t)], [-S', C' v(t)]] on the
        half-angle tables of 2N at the setting s with the turn t: the
        entries for the channels + and -, complex integers in 1/256^2."""
        s, t = setting
        c, sn = self.half_cosines[s % (2 * self.steps)], self.half_sines[s % (2 * self.steps)]
        turn: Complex = (self.cosines[t % self.steps], self.sines[t % self.steps])
        if bit == 0:
            return (c * PHASE_COSINE_SCALE, 0), (-sn * PHASE_COSINE_SCALE, 0)
        return cmul((sn, 0), turn), cmul((c, 0), turn)

    # -- the completion: the ladder ---------------------------------------------

    def cells(self, found: LiveRecord) -> list[tuple[list[tuple[Offer, int]], int, int]]:
        """The cells of a record in the ladder's order: per cell the (offer,
        channel) chosen per factor, its weight's numerator |amplitude|^2 and
        its multiplicity."""
        per_arm: list[list[list[tuple[Offer, int]]]] = []
        for arm in range(found.arms):
            offers = sorted(
                (o for (s, a), o in found.offers.items() if a == arm), key=lambda o: o.set_index
            )
            reads = [o for o in offers if o.read]
            ends = [o for o in offers if not o.read]
            factors = [[(o, c) for c in o.channels()] for o in reads]
            alternatives: list[list[tuple[Offer, int]]] = []
            for chosen_reads in itertools.product(*factors) if factors else [()]:
                for end in ends:
                    for c in end.channels():
                        alternatives.append([*chosen_reads, (end, c)])
            per_arm.append(alternatives)
        origins: dict[int, int] = {}
        cells: list[tuple[list[tuple[Offer, int]], int, int]] = []
        for choice in itertools.product(*per_arm):
            factors_chosen = [item for arm_choice in choice for item in arm_choice]
            real, imaginary = 0, 0
            for label, weight in found.labels.items():
                product: Complex = (weight, 0)
                for offer, channel in factors_chosen:
                    product = cmul(product, offer.residuals.get(channel, {}).get(label, (0, 0)))
                    if product == (0, 0):
                        break
                real += product[0]
                imaginary += product[1]
            numerator = real * real + imaginary * imaginary
            multiplicity = 1
            origins.clear()
            for arm, arm_choice in enumerate(choice):
                end = arm_choice[-1][0]
                assert end.multiplicity is not None
                norm = found.arm_norms[arm]
                multiplicity *= end.multiplicity // norm
                origins[norm] = norm
            for norm in origins:
                multiplicity *= norm
            cells.append((factors_chosen, numerator, multiplicity))
        return cells

    def complete(self, tick: int) -> list[LiveRecord]:
        """Every record whose live count reached 0 and is not gathered: the
        ladder over its cells, the cell of u, the gather (the world's row);
        a record whose offers weigh nothing gathers nowhere (`chosen`
        None). Returns the records gathered this call."""
        written: list[LiveRecord] = []
        for identity in sorted(self.records):
            found = self.records[identity]
            if found.gathered or found.live > 0 or not found.offers:
                continue
            found.gathered = True
            self.completed += 1
            cells = self.cells(found)
            weights = [(numerator, multiplicity) for _, numerator, multiplicity in cells]
            ladder, total = rungs(weights, self.steps)
            k = choose(ladder, found.u) if total[0] else None
            chosen: list[list[object]] | None = None
            weight: list[int] = [0, 1]
            if k is not None:
                factors_chosen, numerator, multiplicity = cells[k]
                chosen = [
                    [self.names[offer.set_index], offer.arm, offer.channel_name(channel)]
                    for offer, channel in factors_chosen
                ]
                common = gcd(numerator, multiplicity) or 1
                weight = [numerator // common, multiplicity // common]
            combinations = len(found.labels) * sum(
                len(offer.residuals) for offer in found.offers.values()
            )
            gather: dict[str, object] = {
                "event": "gather",
                "tick": tick,
                "arrived": found.last_end,
                "family": self.families[found.family],
                "record": identity,
                "u": found.u,
                "born": found.born,
                "chosen": chosen,
                # The rotation's setting and turn of every rotated offer
                # among the chosen factors (the settings of a pair's clicks).
                "windows": (
                    None
                    if k is None
                    else [
                        [self.names[offer.set_index], offer.setting[0], offer.setting[1]]
                        for offer, _ in cells[k][0]
                        if offer.setting is not None
                    ]
                ),
                "weight": weight,
                "total": list(total),
                "unit": UNIT,
                "T": found.norm,
                "before": combinations,
                "after": 1 if chosen is not None else 0,
                "cells": [
                    [
                        [
                            [self.names[offer.set_index], offer.arm, offer.channel_name(channel)]
                            for offer, channel in factors_chosen
                        ],
                        rung,
                    ]
                    for (factors_chosen, _, _), rung in zip(cells, ladder, strict=True)
                ],
            }
            found.gather = gather
            self.gathers.append(gather)
            written.append(found)
        return written

    def open_records(self) -> list[dict[str, object]]:
        """The records not gathered at the run's end, with their offers."""
        found = []
        for identity in sorted(self.records):
            entry = self.records[identity]
            if entry.gathered:
                continue
            found.append(
                {
                    "record": identity,
                    "family": self.families[entry.family],
                    "u": entry.u,
                    "born": entry.born,
                    "live": entry.live,
                    "offers": [
                        {
                            "set": self.names[offer.set_index],
                            "arm": offer.arm,
                            "read": offer.read,
                            "units": offer.units,
                            "multiplicity": offer.multiplicity,
                            "pointers": {str(k): list(v) for k, v in offer.pointers.items()},
                        }
                        for offer in entry.offers.values()
                    ],
                }
            )
        return found

    def report(self) -> dict[str, object]:
        """The layer's line of `run.json`: the sets in order, the records
        born, gathered and open."""
        return {
            "sets": list(self.names),
            "unit": UNIT,
            "born": self.born,
            "gathered": self.completed,
            "open": len(self.records) - self.completed,
        }
