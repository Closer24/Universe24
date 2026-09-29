"""The records' bookkeeping the loop steps (HOST classes, no line of the law): the live record with its arrays, a body's record on its one Node, the block (a body on the GameBoard), the books per family and the runner's layer of lines."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from event_universe.loader.world import BlockDefinition


@dataclass
class LiveRecord:
    """One record on the board: its dense rows, its count and its ledger."""

    identity: int
    family: int
    given: int
    giving_tick: int
    content: int
    now: np.ndarray
    before: np.ndarray
    remainder: np.ndarray
    age: int = 0
    # the emitter's number for a record a body gave (None for a planted record and for a block's own record)
    emitter: int | None = None
    # HOST (the record (b); BUILD.md section 26 item 43): the record's support
    # box, [lo, hi) per axis, outside which its two levels and its remainder
    # are zero; None for the whole board. The step reads and writes the box
    # grown by one Link (the rule's reach) and writes zeros elsewhere: the
    # same integers as the whole-board step, bit for bit, since zero rows with
    # a zero remainder step to zero under the rule. A shortcut of the host,
    # not of the law: the model's local work per Node is unchanged.
    box: tuple[tuple[int, int], ...] | None = None
    # THE FREE RECORD'S COUNT (ALGEBRA.md #the-counts-line, the free record; the model owner's word of
    # 2026-09-29 on #1495, finding 10): the quanta per Node and the line's remainder over the board, laid
    # from the record's form at its birth (one quantum) and moved by the count's line; None on a record
    # with no count (a body's own record, whose count is its body's; a held part)
    counts: np.ndarray | None = None
    count_remainder: np.ndarray | None = None
    # whether the record's last quantum was reported (the record ends at the interval's close)
    reported: bool = False
    # THE FAMILY GENERICITY (the record; item 51): a body's own standing
    # record (the lattice body's, held by the law at the body and read by no
    # detector, its inverse with the body's), marked on the record and not
    # on its family
    standing: bool = False
    # THE RECORD'S PAIR (ALGEBRA.md #the-primitives, #the-interval; the one stroke, commit
    # 1): the rest pair its rows step with, its family's declared pair or, on
    # a family whose pair is the body's, the body's `kind`; the board's pair
    # arrays are read by (family, pair); None reads the family's declared pair
    # (a record made without one, the tests')
    pair: tuple[int, int] | None = None
    # THE COMPONENT (ALGEBRA.md #the-primitives, #the-interval): the index of the record's
    # component in its family's parts (0 the time part; a wave of light in
    # one transverse component of the charge family, commit 4)
    part: int = 0
    # THE HELD PART (item 51; ALGEBRA.md #the-interval): a field family's component
    # record, stepped plain at the pace 1, written by the hold at the bodies'
    # Nodes, reported by no detector; marked on the record, not on its family
    # (the charge family is held and has waves, ALGEBRA.md #the-primitives)
    held_part: bool = False
    # HOST (the record (b); ALGEBRA.md #the-interval "the support-box shortcut keeps a zero
    # part free of work"): a held part never written nonzero: its two levels
    # and remainder are zero everywhere and step to zero exactly, so the step
    # is skipped; cleared by the first nonzero hold
    silent: bool = False
    # THE SECOND LEVEL of a phase-2 record (ALGEBRA.md #the-interval; commit 4): the pair's
    # second component, (now, before, r) over the board, None until a rotation of the
    # transport writes it (a second level that starts zero and meets no twist stays
    # exactly zero, ALGEBRA.md #the-interval)
    im_now: np.ndarray | None = None
    im_before: np.ndarray | None = None
    im_remainder: np.ndarray | None = None
    # THE TWIST "OWN" (ALGEBRA.md #the-primitives): round(2^16 omega_0), the record's own
    # rotation in the table's unit, the loader's integer; 0 for a record with none (a
    # held part, a planted record without one)
    twist: int = 0

    def arrays(self) -> Iterator[np.ndarray]:
        """The record's arrays on the GameBoard: its two levels and remainder, and the second level's where the family has one."""
        for array in (
            self.now,
            self.before,
            self.remainder,
            self.im_now,
            self.im_before,
            self.im_remainder,
        ):
            if isinstance(array, np.ndarray):
                yield array


@dataclass
class NodeRecord:
    """A body's record on its one Node: the two levels and the remainder of its standing wave, stepped by the rule alone with the count's wall."""

    identity: int
    now: int
    before: int
    remainder: int = 0


class StampedMap(dict[tuple[object, ...], int]):
    """A body's remainders as the audit stamps them: a dict whose `version` rises at every write, so the main loop's guard takes the map by its identity and version and never walks its entries (the hold writes one entry per Node and part; the audit stamps every body before and after every act)."""

    version: int = 0

    def __setitem__(self, key: tuple[object, ...], value: int) -> None:
        self.version += 1
        super().__setitem__(key, value)

    def __delitem__(self, key: tuple[object, ...]) -> None:
        self.version += 1
        super().__delitem__(key)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.version += 1
        super().update(*args, **kwargs)

    def pop(self, *args: Any) -> Any:
        self.version += 1
        return super().pop(*args)

    def clear(self) -> None:
        self.version += 1
        super().clear()


@dataclass
class Block:
    """A block on the board (massive-record-v1, MASSIVE_RECORD.md sections 4 to 7; BUILD.md section 2): its Nodes R (the mask over the board, the cube of `side` at `corner`), its own massive record (the seed on its Nodes), the records it gave, its clock (its record's cycles across R, one click per cycle), its momentum per axis with the drive's accumulators against its wall W = 3 Q M (`wall_of`, live with its quanta; ALGEBRA.md #the-primitives), and its detector among the simulation's detectors."""

    number: int
    family: int
    definition: BlockDefinition
    corner: list[int]
    mask: np.ndarray
    detector: int
    momentum: list[int]
    # THE SPIN AS STATE (ALGEBRA.md #a-familys-declaration, #the-interval; commit 6): S now and S one
    # interval back, the leapfrog's two integers; the load's write is the body's
    # declared `spin` at both
    spin: list[int] = field(default_factory=lambda: [0, 0, 0])
    spin_before: list[int] = field(default_factory=lambda: [0, 0, 0])
    # the momentum's level one interval before (the spin's step's KEEP pair; the momentum a reading of the record's current, ALGEBRA.md #the-primitives), the file's `momentum_before`
    momentum_before: list[int] = field(default_factory=lambda: [0, 0, 0])
    # A TOOL HELD IN PLACE (ALGEBRA.md #the-primitives; the Boss's the record): the world's
    # word `fixed`; a body's motion is its record's by Rule3 alone, the word names a tool held in place
    fixed: bool = False
    # THE COUNT AT A NODE (ALGEBRA.md #the-counts-line; the count's line bound): the body's
    # quanta per Node and the line's remainder, laid at the line's first act; the body's Nodes
    # follow the count's centroid by whole Links, `moved` where they shifted in the last act
    counts: np.ndarray | None = None
    count_remainder: np.ndarray | None = None
    moved: bool = False
    previous_sum: int = 0
    own: LiveRecord | None = None
    # THE WELL OF A BODY WITH A RECORD (ALGEBRA.md #what-a-body-is): its record's D_i div T at
    # every Node as the interval's step left them, the counts the hold reads, and the source row's
    # remainder r_i per Node (`record_form`); None where the universe declares no T
    well: np.ndarray | None = None
    well_remainder: np.ndarray | None = None
    # THE BODY'S RECORD AT ITS BODY'S NODE (ALGEBRA.md #what-a-body-is; item 42, item 37
    # HISTORY): the standing record on the body's Node under the world key
    # `body_record`, its own rows then nowhere else on the GameBoard (`own`
    # None); None under the lattice body
    node_record: NodeRecord | None = None
    emitted: list[int] = field(default_factory=list)
    givings: int = 0
    # THE BODY'S CLICK (ALGEBRA.md #the-click; the model owner's word of 2026-09-29 on #1495, finding
    # 10): set at the interval's close where its record's sum crosses from at most 0 to above 0, read
    # and cleared by the giving of the next interval (one giving per click)
    new_cycle: bool = False
    # the interval the current cycle began and the last cycle's length
    cycle_start: int = 0
    cycle_length: int = 0
    # THE HOLDS' REMAINDERS (ALGEBRA.md #the-interval; the one stroke, commit 2): per
    # held family and part, the division's remainder carried between intervals
    # and the value written, (family, part) for the support's writes and ("d",
    # family, i, j, sigma) for the dipole's on the Node + sigma e_j; exact and
    # inverted with the body
    hold_carry: StampedMap = field(default_factory=StampedMap)
    hold_value: StampedMap = field(default_factory=StampedMap)


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


class DetectorLawLayer:
    """The record's lines the runner writes into run.json (the amplitude law's shape)."""

    def __init__(self) -> None:
        self.gathers: list[dict[str, object]] = []
        self.given = 0
        self.gathered = 0
