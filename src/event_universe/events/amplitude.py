"""The apparatus's layer of the amplitude law (`amplitude-v1`; the model
owner, 2026-09-20, Highlights 5.4, "DECIDED: `amplitude-v1` is built"; the
ten principles, (4) and (5); the physicist's and the mathematician's
design, docs/designs/amplitude-v1/DESIGN.md, sections 1.2, 3, 4, 5 and 10;
docs/BEAM_LAW.md note 37).

The world is the list of clicks. The GameBoard computes every path of a
record (`nature_beam`: the flight, the collision, the split, the label
rotation, the gate, the merge with its cancel), and the layer, host state
owned by the apparatus, reads the record's OFFERS where its rows end (a
click at a set, an open face, the border `lifetime`) and, at the record's
COMPLETION (every unit of the record ended: its live count reaches 0
through the apparatus's Port events, the births, the splits, the ends and
the cancels the merge reports), chooses one offer by the record's birth
phase u on the ladder of the offers' weights, normalised by their sum, the
rungs at the nearest integer (the owner's decision (a)):

    b_k = (2 N C_k + Total) // (2 Total),   b_0 = 0, b_K = N,

the click the cell k with b_{k-1} <= u < b_k. No draw at the detector: the
randomness is the clock of the birth; over births, Born. The GameBoard never
reads the layer, and the layer reads the GameBoard only through the
apparatus's events (principle 5: the only non-local operation, at the
one-way border, owned by the apparatus).

An offer is a (set, arm) of the record: per Node of the set and per label
the accumulated pointer, `(X, Y) += sum 32 w (C[p], S[p])` over the rows of
that label that ended at that Node (the same first moment over the circle
as `coherent_pointer`, the scope one record and label in place of the
crowd: the owner's unification (4)), and the RESIDUAL per channel, Node
and label after the set's reading: a plain set offers one channel per
label (the which-path click), a `sum` set with a window rotates the arm's
bit of the joint label by the half-angle tables of 2N at its setting s
(`U_s = [[C', S' v(t)], [-S', C' v(t)]]` in 1/256^2, t the entry's turn)
and offers the channels + and - (the label click, section 4.1); a `read`
at a `sum` set is a which-path reading whose rows go on, a factor that
selects the label without a pointer. Interference is coherent within one
Node only (the decision of 2026-09-20 on the owner's point 5, "on the
detector every Node has |Sigma|^2"): the joint amplitude of a cell (one
channel per read factor and one (end, channel) per arm) at one Node per
end is `sum_l prod_k residual_k[c_k][node_k, l]`, complex integers, and
the cell's weight is the SUM over the ends' Node tuples of `|amplitude|^2`
(incoherent across Nodes: rows at different Nodes never meet), over m the
product of the arms' multiplicities over the birth norms they share; the
click lands in the set at the Node tuple that u's position within the cell
selects by the same rungs over the tuples, `c_j = (2 W D_j + T) // (2 T)`
with W the cell's width, D_j the cumulative Node weight and T the cell's
weight. The cells are in the lexicographic order of the arms (each arm's
read factors in the sets' order, then its ends in the sets' order, the
channels + before - and the labels ascending); the sets in the design's
order (the measured events outside every declared detector by number, the
declared detectors, the faces in Port order, the border). Python integers
throughout: a report of the host, exact, never refused (a record's
weights can pass 2^64).

The record's labels are a set of joint labels (the bit k of a label its
value on arm k), the rows carrying the amplitudes: a birth's `branches`
weights are the rows' amounts, a GameBoard rotation of a label bit
(`rotate`) doubles the set on that bit, and a gate joins records into the
product of their sets with the CNOT's permutation (`join`).
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

from event_universe.core.phase import (
    MAX_PHASE_STEPS,
    PHASE_COSINE_SCALE,
    phase_cosines,
    phase_sines,
)
from event_universe.events.measured import DetectorSet

Complex = tuple[int, int]
Node = tuple[int, int, int]
# The Node of a read factor (a reading is not a click site) and of an end
# whose Node the engine did not name.
NO_NODE: Node = (-1, -1, -1)
# The weight of a row's pointer, 32 x amount (BEAM_LAW note 33: the one
# reading's amplitude, so that one unit's pointer squares to 2^26 and the
# tables' rounding stays below one part in 2^8 of it; a scale, nothing of
# the law).
AMPLITUDE_SCALE = 32
# The identity entry of a plain set's residual: the rotation's entries are
# in 1/256^2, so a set that rotates nothing scales by 256^2, and every
# arm's factors are in one unit.
IDENTITY = PHASE_COSINE_SCALE * PHASE_COSINE_SCALE
# The joint label of a row is its `branch` column: the label in the low
# 32 bits, the arm it flies on above them.
LABEL_BITS = 32
LABEL_MASK = (1 << LABEL_BITS) - 1
# The unit of a weight's numerator: the square of one row of amount 1 at
# the identity rotation, (32 x 256 x 256^2)^2 = 2^58; a record's `total`
# over this unit is its norm as offered (1 up to the tables' rounding and
# the cross terms of paths meeting at one Node).
UNIT = (AMPLITUDE_SCALE * PHASE_COSINE_SCALE * IDENTITY) ** 2
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


def half_angle(setting: int, steps: int) -> tuple[int, int]:
    """C'[s] and S'[s] of the half-angle tables of 2N at the setting s: the
    tables of 2N where they exist (N through MAX_PHASE_STEPS / 2, 32768 since
    the bound was raised to 65536 on 2026-09-20), else the tables of
    MAX_PHASE_STEPS at s / 2 (the same rounding of the same angle), an odd
    setting at N = MAX_PHASE_STEPS refused (no table carries it)."""
    size = min(2 * steps, MAX_PHASE_STEPS)
    factor = 2 * steps // size
    index = setting % (2 * steps)
    if index % factor:
        raise ValueError(
            f"amplitude-v1: the setting {setting} has no half-angle entry at N = {steps} (the "
            f"tables end at {MAX_PHASE_STEPS} steps; an even setting)"
        )
    index //= factor
    return phase_cosines(size)[index], phase_sines(size)[index]


def gcd(a: int, b: int) -> int:
    """Euclid on Python integers: the layer's sums are the host's reports,
    exact and unbounded (a record's weights can pass 2^64)."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b) if a and b else max(a, b)


def isqrt(value: int) -> int:
    """The integer square root of a nonnegative Python integer (Newton on
    the host's integers, exact)."""
    if value < 2:
        return value
    x = 1 << ((value.bit_length() + 1) // 2)
    while True:
        y = (x + value // x) // 2
        if y >= x:
            return x
        x = y


def common_denominator(held: int, arriving: int) -> tuple[int, int, int]:
    """Two multiplicities of one record at one offer (the design's 2.5;
    stage (vii)): the offer's pointers are amplitudes over the square root
    of its multiplicity, so rows of the multiplicities D and m add exactly
    when D / m is the square of a rational, a / b in lowest terms with a
    and b squares: the held pointers scaled by sqrt(b), the arriving row
    by sqrt(a), the common denominator D x b = m x a. Returns (the scale
    of the held pointers, the scale of the arriving row, the common
    denominator); None where the ratio is not a square (the caller
    refuses: the integer form has no cross term over sqrt(D m))."""
    common = gcd(held, arriving)
    a, b = held // common, arriving // common
    root_a, root_b = isqrt(a), isqrt(b)
    if root_a * root_a != a or root_b * root_b != b:
        return (0, 0, 0)
    return root_b, root_a, held * b


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


def node_choice(weights: list[int], width: int, position: int) -> int:
    """The Node tuple within a cell: the rungs c_j = (2 W D_j + T) //
    (2 T) over the tuples' weights (W the cell's width in u, D_j the
    cumulative weight, T the cell's weight), the first j with the position
    (u less the cell's first rung) below c_j."""
    total = sum(weights)
    cumulative = 0
    for j, weight in enumerate(weights):
        cumulative += weight
        if position < (2 * width * cumulative + total) // (2 * total):
            return j
    return len(weights) - 1


@dataclass
class Offer:
    """One offer of a record: the rows of the record that ended at one set
    on one arm (`read` False), or were read there and went on (`read`
    True, a which-path factor). `pointers` the accumulated pointer per
    (Node, label) (Python integers); `residuals` per channel the complex
    residual per (Node, label) after the set's reading; `multiplicity` the
    rows' m at the set (the common denominator of the rows' multiplicities,
    which differ by square factors or are refused, `common_denominator`);
    `rotated` whether the set rotated the labels (the channels + and -),
    else the channels are the labels; `setting` the rotation's (setting,
    turn); per Node the units, the content and the momentum the rows
    brought."""

    set_index: int
    arm: int
    read: bool = False
    rotated: bool = False
    setting: tuple[int, int] | None = None
    multiplicity: int | None = None
    pointers: dict[tuple[Node, int], Complex] = field(default_factory=dict)
    residuals: dict[int, dict[tuple[Node, int], Complex]] = field(default_factory=dict)
    units: int = 0
    units_at: dict[Node, int] = field(default_factory=dict)
    content: dict[Node, int] = field(default_factory=dict)
    momentum: dict[Node, list[int]] = field(default_factory=dict)
    last_tick: int = 0

    def channels(self) -> list[int]:
        return sorted(self.residuals)

    def channel_name(self, channel: int) -> str:
        return CHANNEL_NAMES[channel] if self.rotated else str(channel)

    def nodes(self) -> list[Node]:
        """The Nodes of the set the offer's rows ended at, in order."""
        return sorted({node for node, _ in self.pointers}) or [NO_NODE]


@dataclass
class LiveRecord:
    """The layer's table entry of one record (the design's section 1.2):
    its identity, its family, the birth phase u, the tick of the birth,
    the birth norm T = sum of the branches' weights squared (a report; the
    ladder is normalised by the total of the offers), the joint labels
    (the set, with the declared weights of the birth as a report: the rows
    carry the amplitudes), the arms, the birth norm of every arm's origin,
    the live count in units, the offers and, once gathered, the gather."""

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


Cell = tuple[list[tuple[Offer, int]], int, int, list[tuple[tuple[Node, ...], int]]]


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

    def origin(self, identity: int) -> int:
        """The identity a row was born to, as the gate's label map keys it."""
        return identity

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
        """A new record: u, its labels and weights, its arms, its live count
        (the units born; a rebirth births once with 0 and the splits that
        re-create its rows add theirs)."""
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

    def rotate(self, identity: int, bit: int) -> None:
        """A GameBoard rotation of a label bit: the record's label set doubles
        on that bit (the rows carry the amplitudes)."""
        found = self.resolve(identity)
        if found is None:
            return
        mask = 1 << bit
        labels: dict[int, int] = {}
        for label in found.labels:
            labels[label & ~mask] = 1
            labels[label | mask] = 1
        found.labels = labels
        found.norm = len(labels)

    def join(
        self,
        tick: int,
        survivor: int,
        others: list[int],
        present: dict[int, set[int]] | None = None,
        here: dict[int, int] | None = None,
    ) -> tuple[dict[tuple[int, int], list[int]], dict[int, int]]:
        """The gate's join (the design's section 10): the records `others`
        join the `survivor` (the control): the joint labels the product of
        the label sets (the survivor's bits first, then each other's in
        order), then the CNOT from the control's bit 0 to the bit of every
        other arm (one bit per arm); the arms concatenated, the live units
        and the ends summed, the others aliased. Returns per (record,
        label) the joint labels its rows take (one per combination of the
        other records' labels, permuted) and per record its arm offset.
        `present` names the labels of every record's rows at the gate (the
        label sets the product is over); without it the records' label
        sets serve. `here`, the units of every record pending at the gate:
        a record with units elsewhere or with an offer already made is
        refused (its rows and offers elsewhere would keep their pre-join
        labels and drop out of the joint cells; the lazy relabelling of
        the design's section 10 is not built; the review of (v), B2)."""
        found = [self.records[survivor]] + [self.records[other] for other in others]
        if here is not None and others:
            for live in found:
                elsewhere = live.live - here.get(live.identity, 0)
                offers = sorted(self.names[s] for (s, _), o in live.offers.items())
                if elsewhere or offers:
                    raise ValueError(
                        f"amplitude-v1: the record {live.identity} reaches the gate with "
                        f"{elsewhere} of its {live.live} live units elsewhere and offers at "
                        f"{offers}: a record joins a gate with every unit at it and no offer made "
                        "(the lazy relabelling of the design's section 10 is not built; BEAM_LAW "
                        "note 37 (vii))"
                    )
        sets = [
            sorted(present[live.identity])
            if present and live.identity in present
            else sorted(live.labels)
            for live in found
        ]
        bits: list[int] = []
        offset = 0
        for live in found:
            bits.append(offset)
            offset += live.arms
        total_arms = offset

        def permute(joint: int) -> int:
            if joint & 1:
                for position in range(1, total_arms):
                    joint ^= 1 << position
            return joint

        joint_labels: dict[int, int] = {}
        for combination in itertools.product(*sets):
            joint = sum(label << bits[k] for k, label in enumerate(combination))
            joint_labels[permute(joint)] = 1
        label_map: dict[tuple[int, int], list[int]] = {}
        for k, live in enumerate(found):
            others_labels = [sets[j] for j in range(len(found)) if j != k]
            other_bits = [bits[j] for j in range(len(found)) if j != k]
            for label in sets[k]:
                joints = []
                for others_combination in itertools.product(*others_labels):
                    joint = label << bits[k]
                    for position, other_label in zip(other_bits, others_combination, strict=True):
                        joint |= other_label << position
                    joints.append(permute(joint))
                label_map[(live.identity, label)] = joints
        head = found[0]
        head.labels = joint_labels
        head.norm = sum(w * w for w in joint_labels.values())
        arm_offsets = {live.identity: bits[k] for k, live in enumerate(found)}
        for k, live in enumerate(found[1:], start=1):
            head.arms += live.arms
            head.arm_norms.extend(live.arm_norms)
            head.live += live.live
            head.ends += live.ends
            head.last_end = max(head.last_end, live.last_end)
            for (set_index, arm), offer in live.offers.items():
                offer.arm = arm + bits[k]
                head.offers[(set_index, arm + bits[k])] = offer
            self.aliases[live.identity] = survivor
            del self.records[live.identity]
        return label_map, arm_offsets

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
        node: Node | None = None,
        content: int = 0,
        momentum: list[int] | None = None,
    ) -> None:
        """Rows of a record that ended at a set (`absorbed`: a click, a
        face, the border; the units leave the live count) or were read
        there and went on (a which-path factor): the offer at (set, arm)
        accumulates their pointer and the residual per channel at their
        Node, with the content and the momentum they brought. A gathered
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
        if not absorbed:
            # A read: the factor selects the label, once per label present.
            offer.residuals.setdefault(label, {})[(NO_NODE, label)] = (IDENTITY, 0)
            return
        at = NO_NODE if node is None else node
        scale = 1
        if offer.multiplicity is None:
            offer.multiplicity = multiplicity
        elif offer.multiplicity != multiplicity:
            # Several multiplicities of one record at one offer (stage
            # (vii)): the common denominator where the ratio is a square,
            # the held pointers and residuals rescaled; refused otherwise.
            held_scale, scale, common = common_denominator(offer.multiplicity, multiplicity)
            if not common:
                raise ValueError(
                    f"amplitude-v1: the rows of the record {identity} at the set "
                    f"{self.names[set_index]} carry the multiplicities {offer.multiplicity} and "
                    f"{multiplicity}, whose ratio is not a square: two paths of one record add "
                    "exactly at a set only when their multiplicities differ by a square factor "
                    "(the integer form has no cross term over the square root of their "
                    "product; the design's section 2.5)"
                )
            if held_scale != 1:
                offer.pointers = {
                    key: (x * held_scale, y * held_scale) for key, (x, y) in offer.pointers.items()
                }
                offer.residuals = {
                    channel: {key: (x * held_scale, y * held_scale) for key, (x, y) in entries.items()}
                    for channel, entries in offer.residuals.items()
                }
            offer.multiplicity = common
        offer.units += amount
        offer.units_at[at] = offer.units_at.get(at, 0) + amount
        offer.content[at] = offer.content.get(at, 0) + content
        if momentum is not None:
            held = offer.momentum.setdefault(at, [0] * len(momentum))
            for axis, value in enumerate(momentum):
                held[axis] += value
        weight = AMPLITUDE_SCALE * amount * scale
        pointer: Complex = (weight * self.cosines[phase], weight * self.sines[phase])
        key = (at, label)
        offer.pointers[key] = cadd(offer.pointers.get(key, (0, 0)), pointer)
        if rotation is None:
            channel = offer.residuals.setdefault(label, {})
            channel[key] = cadd(channel.get(key, (0, 0)), cmul((IDENTITY, 0), pointer))
        else:
            offer.rotated = True
            if offer.setting is None:
                offer.setting = rotation
            for channel_index, entry in enumerate(self.rotation(rotation, (label >> arm) & 1)):
                channel = offer.residuals.setdefault(channel_index, {})
                channel[key] = cadd(channel.get(key, (0, 0)), cmul(entry, pointer))

    def rotation(self, setting: tuple[int, int], bit: int) -> tuple[Complex, Complex]:
        """The column `bit` of U_s = [[C', S' v(t)], [-S', C' v(t)]] on the
        half-angle tables of 2N at the setting s with the turn t: the
        entries for the channels + and -, complex integers in 1/256^2."""
        s, t = setting
        c, sn = half_angle(s, self.steps)
        turn: Complex = (self.cosines[t % self.steps], self.sines[t % self.steps])
        if bit == 0:
            return (c * PHASE_COSINE_SCALE, 0), (-sn * PHASE_COSINE_SCALE, 0)
        return cmul((sn, 0), turn), cmul((c, 0), turn)

    # -- the completion: the ladder ---------------------------------------------

    def cells(self, found: LiveRecord) -> list[Cell]:
        """The cells of a record in the ladder's order: per cell the (offer,
        channel) chosen per factor, its weight's numerator (the sum over the
        ends' Node tuples of |amplitude|^2), its multiplicity and the Node
        tuples with their weights in order."""
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
        cells: list[Cell] = []
        for choice in itertools.product(*per_arm):
            factors_chosen = [item for arm_choice in choice for item in arm_choice]
            read_factors = [(o, c) for o, c in factors_chosen if o.read]
            end_factors = [(o, c) for o, c in factors_chosen if not o.read]
            tuples: list[tuple[tuple[Node, ...], int]] = []
            numerator = 0
            present = sorted(
                {
                    label
                    for offer in found.offers.values()
                    for channel in offer.residuals.values()
                    for _, label in channel
                }
            )
            for nodes in itertools.product(*[o.nodes() for o, _ in end_factors]):
                real, imaginary = 0, 0
                for label in present:
                    product: Complex = (1, 0)
                    for offer, channel in read_factors:
                        residual = offer.residuals.get(channel, {}).get((NO_NODE, label), (0, 0))
                        product = cmul(product, residual)
                        if product == (0, 0):
                            break
                    for (offer, channel), node in zip(end_factors, nodes, strict=True):
                        if product == (0, 0):
                            break
                        residual = offer.residuals.get(channel, {}).get((node, label), (0, 0))
                        product = cmul(product, residual)
                    real += product[0]
                    imaginary += product[1]
                weight = real * real + imaginary * imaginary
                tuples.append((nodes, weight))
                numerator += weight
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
            cells.append((factors_chosen, numerator, multiplicity, tuples))
        return cells

    def complete(self, tick: int) -> list[LiveRecord]:
        """Every record whose live count reached 0 and is not gathered: the
        ladder over its cells, the cell of u, the Node tuple within it, the
        gather (the world's row); a record whose offers weigh nothing
        gathers nowhere (`chosen` None). Returns the records gathered this
        call."""
        written: list[LiveRecord] = []
        for identity in sorted(self.records):
            found = self.records[identity]
            if found.gathered or found.live > 0 or not found.offers:
                continue
            found.gathered = True
            self.completed += 1
            cells = self.cells(found)
            weights = [(numerator, multiplicity) for _, numerator, multiplicity, _ in cells]
            ladder, total = rungs(weights, self.steps)
            k = choose(ladder, found.u) if total[0] else None
            chosen: list[list[object]] | None = None
            weight: list[int] = [0, 1]
            windows: list[list[object]] | None = None
            nodes_chosen: list[list[int]] | None = None
            content = 0
            momentum: list[int] = []
            if k is not None:
                factors_chosen, numerator, multiplicity, tuples = cells[k]
                chosen = [
                    [self.names[offer.set_index], offer.arm, offer.channel_name(channel)]
                    for offer, channel in factors_chosen
                ]
                windows = [
                    [self.names[offer.set_index], offer.setting[0], offer.setting[1]]
                    for offer, _ in factors_chosen
                    if offer.setting is not None
                ]
                common = gcd(numerator, multiplicity) or 1
                weight = [numerator // common, multiplicity // common]
                first = ladder[k - 1] if k else 0
                j = node_choice([w for _, w in tuples], ladder[k] - first, found.u - first)
                nodes, _ = tuples[j]
                nodes_chosen = [list(node) for node in nodes]
                chosen_ends = [o for o, _ in factors_chosen if not o.read]
                for offer, node in zip(chosen_ends, nodes, strict=True):
                    content += offer.content.get(node, 0)
                    for axis, value in enumerate(offer.momentum.get(node, [])):
                        if axis >= len(momentum):
                            momentum.append(0)
                        momentum[axis] += value
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
                # The Node of every chosen end (one per arm), the rotation's
                # setting and turn of every rotated offer among the chosen
                # factors, the content the chosen rows brought and the
                # momentum they gave (the books' line of the click).
                "node": nodes_chosen,
                "windows": windows,
                "content": content,
                "momentum": momentum,
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
                    for (factors_chosen, _, _, _), rung in zip(cells, ladder, strict=True)
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
                            "pointers": {
                                f"{list(node)}:{label}": list(value)
                                for (node, label), value in sorted(offer.pointers.items())
                            },
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
