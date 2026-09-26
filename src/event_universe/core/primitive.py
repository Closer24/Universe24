"""THE INTERFACE OF A PRIMITIVE (the model owner's decisions of 2026-09-26 through the
Boss, records 2208, 2212 and 2221; issue #1154; ALGEBRA.md 9.110 item 7, 9.111 items 6
and 7, 9.112 items 1 and 5, 9.116 item 3):

    apply(term, start, own) -> writes

A TERM is one line of the run's files, [name, target, of, degree, weight, table]: the
primitive's English name, the value it writes into, the family or body whose levels or
count are its argument, the argument's degree, its signed weight and its table (9.110
item 7). START is the read-only view of the interval's start: every family's levels
now and before, the paces, a body's count M_k and wall W = 3 Q M, its momentum n, the
Ports' accumulators; nothing written in the interval is read in it (9.57 (1); 9.111
item 6). OWN is the primitive's own record at the Nodes it acts on: its levels and its
remainder per divisor, the one place a division's remainder lives (9.91 (2), (3)).
WRITES are whole integers into declared targets (a family's level at Nodes, a pace,
the record's tally) or deferred writes the loop applies at t + 1 (a body's count M_k,
its charge Q, its momentum n, the stock); the primitive writes nothing itself: the
loop applies its writes at the declared place and emits one trace line per act (9.112
item 5). Integers only; no float, no root, no draw; no family's name.

Cut 2 declares the interface; cut 3 moves the first body of code (the hold) behind it.
The arrays are the loop's integer numpy arrays; this module names them without importing
numpy (core holds integers alone under its audit; the Node's arrays come with core/node.py).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class Term:
    """One line of the files: the primitive's name, the value it writes into, the
    family or body whose levels or count are its argument (an index, resolved by the
    loader), its degree, its signed weight and its table (a tuple of integers or
    empty), with the line's label for a refusal."""

    name: str
    target: str
    of: int
    degree: int
    weight: int
    table: tuple[int, ...] = ()
    label: str = ""


@dataclass(frozen=True)
class Start:
    """The interval's start, read-only: the levels now and before per family (by
    index), the paces per family, every body's count per family, wall and momentum,
    and the Ports' accumulators; the arrays are the loop's and no primitive writes
    into them."""

    levels_now: Sequence[Any]
    levels_before: Sequence[Any]
    paces: Sequence[Any]
    counts: Sequence[Sequence[int]]
    walls: Sequence[int]
    momenta: Sequence[Sequence[int]]
    accumulators: Mapping[int, Any] = field(default_factory=dict)


@dataclass
class Own:
    """The primitive's own record at the Nodes it acts on: its levels and its
    remainder per divisor (the remainder's one home), whole integers."""

    levels: Any
    remainders: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Write:
    """One write of whole integers: the value's name (a declared target), the family
    or body it belongs to, the Nodes (a mask over the GameBoard or None for a body's
    number), the integers, and whether the loop applies it now at the primitive's
    place or at t + 1 (a click's write)."""

    value: str
    of: int
    at: Any
    integers: Any
    deferred: bool = False


Writes = Sequence[Write]


class Primitive(Protocol):
    """One function per primitive's folder, once its body of code moves in."""

    def __call__(self, term: Term, start: Start, own: Own) -> Writes: ...
