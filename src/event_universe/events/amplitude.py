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
coordinate u on the ladder of the offers' weights, normalised by their
sum, the rungs at the nearest integer on the record's wheel W (the owner's
decision (a); the birth wheel of 2026-09-21, BEAM_LAW note 46: W the
denominator of the lamp's declared rate [r, W], u = ordinal x r mod W,
W = N under [1, N]):

    b_k = (2 W C_k + Total) // (2 Total),   b_0 = 0, b_K = W,

the click the cell k with b_{k-1} <= u < b_k. No draw at the detector: the
randomness is the count of the birth; over births, Born. The GameBoard never
reads the layer, and the layer reads the GameBoard only through the
apparatus's events (principle 5: the only non-local operation, at the
one-way border, owned by the apparatus).

An offer is a (set, arm) of the record: per Node of the set and per label
the PHASE-COUNT VECTOR **f** of the rows of that label that ended at that
Node, `f[p] += 32 w` per row of amount w at the phase p (the record's
element of the group ring Z[Z_N] written as a vector, sparse; the click
without amplitudes, 2026-09-21, BEAM_LAW note 37 (xii): the layer keeps
counts and no pointer), and the RESIDUAL per channel, Node and label
after the set's reading, a vector of the same kind: a plain set offers
one channel per label (the which-path click) with the counts scaled by
the identity 256^2; a `sum` set with a window rotates the arm's bit of
the joint label by the half-angle tables of 2N at its setting s (`U_s =
[[C', S' v(t)], [-S', C' v(t)]]` in 1/256^2, t the entry's turn: each
entry a scalar on the counts and, for v(t), a shift of the phases by t)
and offers the channels + and - (the label click, section 4.1); a `read`
at a `sum` set is a which-path reading whose rows go on, a factor that
selects the label, the multiple 256^2 of the ring's identity e_0.
Interference is coherent within one Node only (the decision of 2026-09-20
on the owner's point 5, "on the detector every Node has |Sigma|^2"): an
arm's element at a label and its end's Node is the product in Z[Z_N] of
its factors' residuals (its reads', then its end's, `ring_product`); for
ONE arm the cell's weight at a Node is the bilinear form `f^T G f` of the
sum over the labels of that element, **G** = **E**^T **E** the Gram
matrix of the tables (`core.phase.phase_gram`, G_jk = C_j C_k + S_j S_k,
built once from the rounded tables), through the primitive
`core.integer.signed_inner`, and no pointer is formed; for SEVERAL arms
the weight is the same bilinear form on the tensor product of the arms'
elements, evaluated through its rank-2 factorisation, the product in Z[i]
of the arms' pointers `E f` (`evaluate`, `cmul`) summed over the labels
and taken with itself (`signed_inner`), the same integer by associativity
(the ring convolution across arms is the exact law's statement and not
the built click's: the rounded tables' evaluation is not a ring
homomorphism, the derivations' section 6.7). The cell's weight is the SUM
over the ends' Node tuples (incoherent across Nodes: rows at different
Nodes never meet), over m the product of the arms' multiplicities over
the birth norms they share; the click lands in the set at the Node tuple
that u's position within the cell selects by the same rungs over the
tuples, `c_j = (2 W D_j + T) // (2 T)` with W the cell's width, D_j the
cumulative Node weight and T the cell's weight. The cells are in the lexicographic order of the arms (each arm's
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
import math
from dataclasses import dataclass, field

from event_universe.core.integer import signed_inner
from event_universe.core.phase import (
    GRAM_STORED_STEPS,
    MAX_PHASE_STEPS,
    PHASE_COSINE_SCALE,
    phase_circle,
    phase_cosines,
    phase_gram,
    phase_sines,
)
from event_universe.events.measured import DetectorSet

# The pointer **E f** of a phase-count vector, (X, Y): a report (the first
# moment of the record's counts over the circle) and the factor of the
# several-arm form's rank-2 factorisation; the one-arm click forms none.
Complex = tuple[int, int]
# The phase-count vector **f**: the count at each phase step of the circle,
# sparse (a phase absent counts 0), an element of the group ring Z[Z_N]
# written as a vector; the counts carry the amplitude scale 32 and, in a
# residual, the rotation's entry in 1/256^2.
Counts = dict[int, int]
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
# arm's factors are in one unit (named for the rotation; `nature_beam`'s
# `IDENTITY` is the 3 x 3 identity of the headings).
ROTATION_IDENTITY = PHASE_COSINE_SCALE * PHASE_COSINE_SCALE
# The joint label of a row is its `branch` column: the label in the low
# 32 bits, the arm it flies on above them.
LABEL_BITS = 32
LABEL_MASK = (1 << LABEL_BITS) - 1
# The unit of a weight's numerator: the square of one row of amount 1 at
# the identity rotation, (32 x 256 x 256^2)^2 = 2^58; a record's `total`
# over this unit is its norm as offered (1 up to the tables' rounding and
# the cross terms of paths meeting at one Node).
UNIT = (AMPLITUDE_SCALE * PHASE_COSINE_SCALE * ROTATION_IDENTITY) ** 2
PLUS, MINUS = 0, 1
CHANNEL_NAMES = {PLUS: "+", MINUS: "-"}


def cmul(a: Complex, b: Complex) -> Complex:
    """The product in Z[i] of two arms' pointers: the several-arm weight's
    rank-2 factorisation (note 37 (xii)), the bilinear form on the tensor
    product of the arms' vectors evaluated as the product of their
    pointers, the same integer by associativity."""
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def add_count(into: Counts, phase: int, count: int) -> None:
    """Add a count at one phase to a phase-count vector, in place."""
    into[phase] = into.get(phase, 0) + count


def add_counts(into: Counts, counts: Counts) -> None:
    """The group-ring addition of two phase-count vectors."""
    for phase, count in counts.items():
        into[phase] = into.get(phase, 0) + count


def scale_counts(counts: Counts, factor: int) -> Counts:
    """A phase-count vector scaled by an integer factor."""
    return {phase: count * factor for phase, count in counts.items()}


def ring_product(left: Counts, right: Counts, steps: int) -> Counts:
    """The product in the group ring Z[Z_N] of two phase-count vectors, the
    cyclic convolution over the circle of N steps: an arm's factors are
    multiplied here before the arm is evaluated (a read's factor is the
    multiple 256^2 of the identity e_0, so the product is that scalar
    multiple, the same integers as the click before 2026-09-21). Across
    arms the built click does not use it (the derivations' section 6.7:
    the rounded tables' evaluation is not a ring homomorphism, E(e_1)^2 =
    (64400, 12750) against 256 E(e_2) = (64256, 12800) at N = 64), the
    arms' pointers being multiplied in Z[i] instead (`cmul`)."""
    found: Counts = {}
    for p, a in left.items():
        for q, b in right.items():
            r = (p + q) % steps
            found[r] = found.get(r, 0) + a * b
    return found


def arm_of(branch: int) -> int:
    """The arm of a branch code (its high bits)."""
    return branch >> LABEL_BITS


def label_of(branch: int) -> int:
    """The label of a branch code (its low bits)."""
    return branch & LABEL_MASK


def branch_of(arm: int, label: int) -> int:
    """The branch code of an arm and a label."""
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
    """The least common multiple of two integers (the larger one where one is zero)."""
    return a * b // gcd(a, b) if a and b else max(a, b)


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
    root_a, root_b = math.isqrt(a), math.isqrt(b)
    if root_a * root_a != a or root_b * root_b != b:
        return (0, 0, 0)
    return root_b, root_a, held * b


def rungs(weights: list[tuple[int, int]], steps: int) -> tuple[list[int], tuple[int, int]]:
    """The ladder (the design's section 3.3): the cells' weights as pairs
    (numerator, multiplicity), the cumulative C_k over the common
    denominator D and the rungs b_k = (2 W C_k + Total) // (2 Total) at
    the nearest integer on the wheel `steps` = W (N under [1, N]), b_K =
    W; returns the rungs and the total as the reduced pair. Every u = 0 ..
    W - 1 falls in exactly one cell; an offer below Total / 2W may get an
    empty cell."""
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
    """The cell of u by the rungs: the first k with u < b_k (b_{k-1} <= u
    by the rungs' monotony); None when the ladder is empty. The report's
    form; the click reads `cell_of`, the same cell without the division."""
    for k, b in enumerate(found):
        if u < b:
            return k
    return None


def cell_of(weights: list[tuple[int, int]], steps: int, u: int) -> int | None:
    """The cell of u as the comparison of two products (the fraction-free
    law, 2026-09-20, BEAM_LAW note 41 (v); the mathematician's FORM.md
    section 5): the first k with 2 T u + T <= 2 W C_k, C_k the cumulative
    weight over the cells' common denominator, T the total and W the
    record's wheel (`steps`; N under the wheel [1, N], note 46), which is
    u < b_k for the rung b_k = (2 W C_k + T) // (2 T) at the nearest
    integer, no division and no rounding, the same integers as `choose`
    on `rungs`; None when the ladder is empty (T = 0)."""
    denominator = 1
    for _, m in weights:
        denominator = lcm(denominator, m)
    total = sum(n * (denominator // m) for n, m in weights)
    if total == 0:
        return None
    threshold = 2 * total * u + total
    cumulative = 0
    for k, (n, m) in enumerate(weights):
        cumulative += n * (denominator // m)
        if threshold <= 2 * steps * cumulative:
            return k
    return None


def node_choice(weights: list[int], width: int, position: int) -> int:
    """The Node tuple within a cell: the rungs c_j = (2 W D_j + T) //
    (2 T) over the tuples' weights (W the cell's width in u, D_j the
    cumulative weight, T the cell's weight), the first j with the position
    (u less the cell's first rung) below c_j. The same rungs read the row
    within the chosen Node (`massive-rows-v1`: the ladder's third level,
    over the waiting units per direction at the Node)."""
    total = sum(weights)
    cumulative = 0
    for j, weight in enumerate(weights):
        cumulative += weight
        if position < (2 * width * cumulative + total) // (2 * total):
            return j
    return len(weights) - 1


def node_rung(weights: list[int], width: int, j: int) -> tuple[int, int]:
    """The rung of the j-th choice of `node_choice`: [c_{j-1}, c_j) over
    the same weights and width (c_0 = 0; an empty total gives [0, width)),
    what the next level of the ladder reads its position and width from."""
    total = sum(weights)
    if total == 0:
        return 0, width
    rungs = [0]
    cumulative = 0
    for weight in weights:
        cumulative += weight
        rungs.append((2 * width * cumulative + total) // (2 * total))
    return rungs[j], max(rungs[j + 1], rungs[j] + 1)


@dataclass
class Offer:
    """One offer of a record: the rows of the record that ended at one set
    on one arm (`read` False), or were read there and went on (`read`
    True, a which-path factor). `counts` the phase-count vector per (Node,
    label) of the rows that ended there (Python integers, the amplitude
    scale 32 on the amounts); `residuals` per channel the phase-count
    vector per (Node, label) after the set's reading (the rotation's
    entries as scalars and shifts; a read's the multiple 256^2 of e_0 at
    (NO_NODE, label) under the channel label); `multiplicity` the
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
    counts: dict[tuple[Node, int], Counts] = field(default_factory=dict)
    residuals: dict[int, dict[tuple[Node, int], Counts]] = field(default_factory=dict)
    units: int = 0
    units_at: dict[Node, int] = field(default_factory=dict)
    content: dict[Node, int] = field(default_factory=dict)
    momentum: dict[Node, list[int]] = field(default_factory=dict)
    last_tick: int = 0
    # The record's waiting state (`massive-rows-v1`, the design's section 3
    # item 5): per Node the units, the content and the labels of the rows
    # that ended there and were NOT placed at their arrival ((1 - f_F) x
    # what they brought, f_F the family's placed fraction), and per Node
    # the waiting units per direction (the row the completion places its
    # quantum on is read by the rungs over them); empty at f_F = 1, so the
    # click as built holds nothing here. Resolved at the completion: the
    # chosen end's quantum placed, the rest cancelled.
    waiting_units: dict[Node, int] = field(default_factory=dict)
    waiting_content: dict[Node, int] = field(default_factory=dict)
    waiting_momentum: dict[Node, list[int]] = field(default_factory=dict)
    waiting_directions: dict[Node, dict[int, int]] = field(default_factory=dict)

    def channels(self) -> list[int]:
        """The channels the offer's residuals fill, in order."""
        return sorted(self.residuals)

    def channel_name(self, channel: int) -> str:
        """The name of a channel: its letter under a rotation, its index otherwise."""
        return CHANNEL_NAMES[channel] if self.rotated else str(channel)

    def nodes(self) -> list[Node]:
        """The Nodes of the set the offer's rows ended at, in order."""
        return sorted({node for node, _ in self.counts}) or [NO_NODE]


@dataclass
class LiveRecord:
    """The layer's table entry of one record (the design's section 1.2):
    its identity, its family, the birth coordinate u and its wheel W (the
    rungs' modulus, N under [1, N]), the tick of the birth,
    the birth norm T = sum of the branches' weights squared (a report; the
    ladder is normalised by the total of the offers), the joint labels
    (the set, with the declared weights of the birth as a report: the rows
    carry the amplitudes), the arms, the birth norm of every arm's origin,
    the live count in units, the offers and, once gathered, the gather."""

    identity: int
    family: int
    u: int
    wheel: int
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
    # The completion's choice (`complete`): the chosen ends (one offer and
    # its Node per arm) and u's position within the chosen Node tuple's
    # rung with that rung's width, what the placement reads
    # (`nature_beam.gather_records`: the chosen row by the same rungs over
    # the directions at the Node).
    chosen_ends: list[tuple[Offer, Node]] = field(default_factory=list)
    chosen_position: int = 0
    chosen_width: int = 0

    def offer(self, set_index: int, arm: int, read: bool) -> Offer:
        """The offer of the record at a set and an arm, made on first use."""
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
        # The phase circle (the cyclic group of N steps) with its tables.
        self.circle = phase_circle(phase_steps)
        self.steps = self.circle.steps
        self.cosines = self.circle.cosines
        self.sines = self.circle.sines
        # The Gram matrix G = E^T E of the tables, the one-arm click's
        # declared matrix, built once per N at load (note 37 (xii)); None
        # beyond GRAM_STORED_STEPS, where `gram_entry` forms an entry.
        self.gram: tuple[tuple[int, ...], ...] | None = (
            phase_gram(phase_steps) if phase_steps <= GRAM_STORED_STEPS else None
        )
        self.records: dict[int, LiveRecord] = {}
        # The identities gathered (their table entries and offers released at
        # the completion; `resolve` finds nothing, the lazy deletion of their
        # rows) and the identities whose live count reached 0 since the last
        # completion (the only records a completion visits).
        self.gathered: set[int] = set()
        self.zero: set[int] = set()
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
        wheel: int,
    ) -> LiveRecord:
        """A new record: u on its wheel W, its labels and weights, its arms,
        its live count (the units born; a rebirth births once with 0 and the
        splits that re-create its rows add theirs)."""
        norm = sum(w * w for w in labels.values())
        found = LiveRecord(
            identity, family, u, wheel, tick, norm, dict(labels), arms, [norm] * arms, units
        )
        self.records[identity] = found
        self.born += 1
        if units <= 0:
            self.zero.add(identity)
        return found

    def split(self, identity: int, absorbed: int, born: int) -> None:
        """A split: the units absorbed at the re-emitter and the units born
        again (+ (k - 1) per unit for an equal k-way split)."""
        found = self.resolve(identity)
        if found is not None:
            found.live += born - absorbed
            if found.live <= 0:
                self.zero.add(found.identity)

    def cancel(self, identity: int, amount: int) -> None:
        """The merge's cancel: the units removed end without an offer."""
        found = self.resolve(identity)
        if found is not None:
            found.live -= amount
            if found.live <= 0:
                self.zero.add(found.identity)

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
        for identity in (survivor, *others):
            if identity in self.gathered:
                raise ValueError(
                    f"amplitude-v1: the record {identity} reaches a gate after its gather: a "
                    "gathered record's rows are dropped at their next set, not joined"
                )
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
            """Flip the bits of the arms after the first when the first arm's bit is set (the
            joint label read relative to its first arm)."""
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
            self.zero.discard(live.identity)
        if head.live <= 0:
            self.zero.add(head.identity)
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
        placed: int = 1,
        direction: int = -1,
    ) -> None:
        """Rows of a record that ended at a set (`absorbed`: a click, a
        face, the border; the units leave the live count) or were read
        there and went on (a which-path factor): the offer at (set, arm)
        accumulates their pointer and the residual per channel at their
        Node, with the content and the momentum they brought. With `placed`
        the family's placed fraction f_F (`massive-rows-v1`; 1 by default,
        the click as built): (1 - f_F) x the units, the content and the
        momentum wait in the offer at the Node, the units per `direction`
        (the row's), until the completion. A gathered record's rows are
        dropped (the lazy deletion, section 9: the record left the table
        at its completion and `resolve` finds nothing)."""
        found = self.resolve(identity)
        if found is None:
            return
        if absorbed:
            found.live -= amount
            found.ends += amount
            found.last_end = tick
        if found.live <= 0:
            self.zero.add(found.identity)
        arm, label = arm_of(branch), label_of(branch)
        offer = found.offer(set_index, arm, not absorbed)
        offer.last_tick = tick
        if not absorbed:
            # A read: the factor selects the label, once per label present.
            offer.residuals.setdefault(label, {})[(NO_NODE, label)] = {0: ROTATION_IDENTITY}
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
                offer.counts = {
                    key: scale_counts(value, held_scale) for key, value in offer.counts.items()
                }
                offer.residuals = {
                    channel: {key: scale_counts(value, held_scale) for key, value in entries.items()}
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
        kept = 1 - placed
        if kept:
            offer.waiting_units[at] = offer.waiting_units.get(at, 0) + kept * amount
            offer.waiting_content[at] = offer.waiting_content.get(at, 0) + kept * content
            if momentum is not None:
                waiting = offer.waiting_momentum.setdefault(at, [0] * len(momentum))
                for axis, value in enumerate(momentum):
                    waiting[axis] += kept * value
            by_direction = offer.waiting_directions.setdefault(at, {})
            by_direction[direction] = by_direction.get(direction, 0) + kept * amount
        # The count of the rows at their phase, the amplitude scale on the
        # amount; the residual per channel the count times the entry's
        # scalar at the phase shifted by the entry's turn (no pointer).
        weight = AMPLITUDE_SCALE * amount * scale
        key = (at, label)
        add_count(offer.counts.setdefault(key, {}), phase, weight)
        if rotation is None:
            channel = offer.residuals.setdefault(label, {})
            add_count(channel.setdefault(key, {}), phase, ROTATION_IDENTITY * weight)
        else:
            offer.rotated = True
            if offer.setting is None:
                offer.setting = rotation
            for channel_index, (entry, shift) in enumerate(self.rotation(rotation, (label >> arm) & 1)):
                channel = offer.residuals.setdefault(channel_index, {})
                add_count(channel.setdefault(key, {}), (phase + shift) % self.steps, entry * weight)

    def rotation(self, setting: tuple[int, int], bit: int) -> tuple[tuple[int, int], tuple[int, int]]:
        """The column `bit` of U_s = [[C', S' v(t)], [-S', C' v(t)]] on the
        half-angle tables of 2N at the setting s with the turn t, as the
        group ring reads it: per channel (+, -) the entry's scalar in
        1/256^2 and its shift of the phase in steps, v(t) = e_t the turn by
        t. Bit 0: (C' x 256, 0) and (-S' x 256, 0); bit 1: (S' x 256, t)
        and (C' x 256, t). Until 2026-09-21 the click multiplied the pointer
        by the evaluated turn (C_t, S_t) in Z[i]; the shift gives the same
        integers where the tables turn exactly, at t a multiple of N / 4
        (the register's turns, 0 and 16 at N = 64), and one rounding in
        place of two at any other turn (note 37 (xii))."""
        s, t = setting
        c, sn = half_angle(s, self.steps)
        shift = t % self.steps
        if bit == 0:
            return (c * PHASE_COSINE_SCALE, 0), (-sn * PHASE_COSINE_SCALE, 0)
        return (sn * PHASE_COSINE_SCALE, shift), (c * PHASE_COSINE_SCALE, shift)

    # -- the record's vectors: the evaluation and the bilinear form --------------

    def evaluate(self, counts: Counts) -> Complex:
        """The pointer **E f** of a phase-count vector: the counts against the
        tables' rows C and S, two inner products through the primitive (the
        evaluation of the record's element at the circle; a report's first
        moment, and the factor of the several-arm form's factorisation)."""
        phases = list(counts)
        values = [counts[p] for p in phases]
        ones = (1,) * len(phases)
        return (
            signed_inner(values, [self.cosines[p] for p in phases], ones),
            signed_inner(values, [self.sines[p] for p in phases], ones),
        )

    def gram_entry(self, j: int, k: int) -> int:
        """G_jk = C_j C_k + S_j S_k of the Gram matrix **G** = **E**^T **E**:
        the stored matrix (`core.phase.phase_gram`, built once per N at
        load) or, beyond GRAM_STORED_STEPS, the entry formed from the
        tables where it is read, the same integer."""
        if self.gram is not None:
            return self.gram[j][k]
        return self.cosines[j] * self.cosines[k] + self.sines[j] * self.sines[k]

    def gram_form(self, counts: Counts) -> int:
        """The weight **f**^T **G** **f** of a phase-count vector, one bilinear
        form with the declared matrix G through the primitive: G's rows on
        the support of f against f, then f against that image. The same
        integer as the pointer's inner product with itself, (E f)^T (E f),
        by the associativity of integer arithmetic, and no pointer is
        formed (the click without amplitudes, note 37 (xii))."""
        phases = list(counts)
        values = [counts[p] for p in phases]
        ones = (1,) * len(phases)
        image = [signed_inner([self.gram_entry(p, q) for q in phases], values, ones) for p in phases]
        return signed_inner(values, image, ones)

    def arm_element(self, factors: list[tuple[Offer, int]], node: Node, label: int) -> Counts:
        """An arm's element of the group ring at a label and its end's Node:
        the product in Z[Z_N] of its factors' residuals, the reads' (at no
        Node) and the end's at the Node; empty where a factor has none
        there (the read selects another label; no row of the label ended
        at the Node)."""
        element: Counts | None = None
        for offer, channel in factors:
            residual = offer.residuals.get(channel, {}).get((NO_NODE if offer.read else node, label))
            if not residual:
                return {}
            element = dict(residual) if element is None else ring_product(element, residual, self.steps)
        return element or {}

    # -- the completion: the ladder ---------------------------------------------

    def cells(self, found: LiveRecord) -> list[Cell]:
        """The cells of a record in the ladder's order: per cell the (offer,
        channel) chosen per factor, its weight's numerator (the sum over
        the ends' Node tuples of the tuple's weight: for one arm the
        bilinear form f^T G f of the record's vector at the Node, no
        pointer formed; for several arms the same form on the tensor
        product of the arms' vectors through its factorisation, the
        product of the arms' pointers summed over the labels and taken
        with itself through `signed_inner`; nothing squared as a step of
        its own: the model owner's orders of 2026-09-21, records 173 and
        188 of the log of 2026-09-20, BEAM_LAW note 37 (xi) and (xii); no
        bound is passed, the layer's weights being the host's reports,
        exact and unbounded, 2^116 on a pair and 2^174 on a GHZ triple),
        its multiplicity and the Node tuples with their weights in
        order."""
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
            for nodes in itertools.product(*[arm_choice[-1][0].nodes() for arm_choice in choice]):
                if len(choice) == 1:
                    # One arm: the record's vector at the Node, the sum over
                    # the labels of the arm's element, and its weight the
                    # bilinear form with the Gram matrix; no pointer.
                    vector: Counts = {}
                    for label in present:
                        add_counts(vector, self.arm_element(choice[0], nodes[0], label))
                    weight = self.gram_form(vector)
                else:
                    # Several arms: the form on the tensor product of the
                    # arms' elements through its rank-2 factorisation, the
                    # product of the arms' pointers in Z[i] summed over the
                    # labels and taken with itself.
                    real, imaginary = 0, 0
                    for label in present:
                        product: Complex = (1, 0)
                        for arm_choice, node in zip(choice, nodes, strict=True):
                            element = self.arm_element(arm_choice, node, label)
                            if not element:
                                product = (0, 0)
                                break
                            product = cmul(product, self.evaluate(element))
                        real += product[0]
                        imaginary += product[1]
                    weight = signed_inner((real, imaginary), (real, imaginary), (1, 1))
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
        call; each leaves the table (its offers are the gather's, the
        identity kept in `gathered`), so the host holds a record's offers
        until its completion and no longer."""
        written: list[LiveRecord] = []
        for identity in sorted(self.zero):
            found = self.records.get(identity)
            if found is None or found.live > 0:
                self.zero.discard(identity)
                continue
            if not found.offers:
                continue
            found.gathered = True
            self.completed += 1
            cells = self.cells(found)
            weights = [(numerator, multiplicity) for _, numerator, multiplicity, _ in cells]
            # The ladder on the record's wheel W (N under [1, N]); the cell
            # by the comparison of products, the rungs a report.
            ladder, total = rungs(weights, found.wheel)
            k = cell_of(weights, found.wheel, found.u)
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
                node_weights = [w for _, w in tuples]
                j = node_choice(node_weights, ladder[k] - first, found.u - first)
                lower, upper = node_rung(node_weights, ladder[k] - first, j)
                nodes, _ = tuples[j]
                nodes_chosen = [list(node) for node in nodes]
                chosen_ends = [o for o, _ in factors_chosen if not o.read]
                found.chosen_ends = list(zip(chosen_ends, nodes, strict=True))
                found.chosen_position = found.u - first - lower
                found.chosen_width = upper - lower
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
            del self.records[identity]
            self.gathered.add(identity)
            self.zero.discard(identity)
        return written

    def open_records(self) -> list[dict[str, object]]:
        """The records not gathered at the run's end, with their offers."""
        found = []
        for identity in sorted(self.records):
            entry = self.records[identity]
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
                                f"{list(node)}:{label}": list(self.evaluate(value))
                                for (node, label), value in sorted(offer.counts.items())
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
            "open": len(self.records),
        }
