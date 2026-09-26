"""THE REGISTER OF PRIMITIVES (the model owner's decisions of 2026-09-26 through the
Boss, records 2208 and 2212; the short procedure of skills/workflow.md, point 5;
issue #1154; ALGEBRA.md 9.110 item 7, 9.111 item 7, 9.112 item 1).

A PRIMITIVE is a kind of attribute the engine can apply, written once and applied
to any family by its declaration in the run's files, never by a family's name. Its
IDENTITY is its unique English name, the key of the ledger's table of primitives
(docs/designs/generic_engine/ENGINE_LEDGER.md section 3). The engine holds ONE
register, name to function, read by the central loop alone; every primitive
DECLARES what it reads, what it writes, its place in the interval and its order
among the writers of the same value at the same place. The refusals are the
loader's, at load, by name:

- a name registered twice;
- a term of the files naming a primitive the register lacks, or one the register
  holds without a function (a row of the ledger not built yet);
- two primitives writing the same value at the same place with no order declared
  between them;
- a primitive called by the loop at a place other than the one it declares.

NO VERSION: a change of a primitive's behaviour keeps every shipped world bit for
bit or the primitive takes a new English name; the old keeps its function. This
module holds integers and names alone: no float, no family's name, no number of
the universe.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field

# THE FIVE PLACES of the interval (ALGEBRA.md 9.91 (8); 9.111 item 7's three places
# read as: (i) the step from the interval's start, (ii) after the step, (iii) to
# (v) the writes that enter at t + 1): (i) the clicking families' step with the
# transport, every component; (ii) the bookings at the Ports, the ladder, the
# takings and the givings; (iii) the held families' step; (iv) the holds written,
# the clicks' changes of M, Q and n included; (v) the bodies on one Node, the feed,
# the induction, the spin's step, the recoil's accumulator. "any" is the trace's,
# a read-only line at every place.
PLACES: tuple[str, ...] = ("(i)", "(ii)", "(iii)", "(iv)", "(v)", "any")


@dataclass(frozen=True)
class Declaration:
    """What one primitive declares: its name, its place, the values it reads and
    writes (the words of the ledger's columns, one string each), its order among
    the writers of the same value at the same place (an integer, or None where it
    is the only writer), and its function (None on a row of the ledger not built:
    the name is known, a term naming it is refused as not built)."""

    name: str
    place: str
    reads: tuple[str, ...]
    writes: tuple[str, ...]
    order: int | None = None
    function: Callable[..., object] | None = None
    section: str = ""  # the ALGEBRA.md line of the primitive, for the trace and the ledger

    @property
    def built(self) -> bool:
        return self.function is not None


@dataclass
class Register:
    """The one register: name to declaration, filled by the loop at load and read
    by it at every interval; nothing else registers and nothing else reads it."""

    declarations: dict[str, Declaration] = field(default_factory=dict)

    def add(self, declaration: Declaration) -> None:
        """Register one primitive; a name registered twice is refused at load."""
        if declaration.place not in PLACES:
            raise ValueError(
                f"the primitive {declaration.name!r} declares the place {declaration.place!r}, "
                f"which is none of the interval's places {list(PLACES)}"
            )
        if declaration.name in self.declarations:
            raise ValueError(
                f"the primitive {declaration.name!r} is registered twice: one register, one "
                "name to one function (the model owner's decision, record 2212)"
            )
        self.declarations[declaration.name] = declaration

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(self.declarations)

    def check_writers(self) -> None:
        """Two primitives writing the same value at the same place without an order
        declared between them are refused (record 2212 (3))."""
        writers: dict[tuple[str, str], list[Declaration]] = {}
        for declaration in self.declarations.values():
            for value in declaration.writes:
                writers.setdefault((declaration.place, value), []).append(declaration)
        for (place, value), group in sorted(writers.items()):
            if len(group) < 2:
                continue
            orders = [declaration.order for declaration in group]
            if any(order is None for order in orders) or len(set(orders)) != len(orders):
                names = ", ".join(repr(declaration.name) for declaration in group)
                raise ValueError(
                    f"the primitives {names} all write {value!r} at the place {place} and declare "
                    "no order between them: each writer of one value at one place declares its "
                    "order, an integer, distinct (record 2212 (3))"
                )

    def check_terms(self, terms: Iterable[tuple[str, str]]) -> None:
        """Every term of the files names a primitive the register holds with a
        function; (label, name) pairs, the label naming the file's line."""
        for label, name in terms:
            declaration = self.declarations.get(name)
            if declaration is None:
                raise ValueError(
                    f"{label} names the primitive {name!r}, which the register lacks; the "
                    f"primitives are {list(self.names)} (the ledger's table, section 3)"
                )
            if not declaration.built:
                raise ValueError(
                    f"{label} names the primitive {name!r}, a row of the ledger not built yet: "
                    "its term is refused until its function lands"
                )

    def at(self, name: str, place: str) -> Callable[..., object]:
        """The function of a registered primitive, called by the loop at `place`; a
        call at a place other than the declared one is refused (the loop checks the
        declaration, not the code's comments)."""
        declaration = self.declarations[name]
        if declaration.place not in (place, "any"):
            raise ValueError(
                f"the loop calls the primitive {name!r} at the place {place}, but it declares "
                f"{declaration.place}"
            )
        if declaration.function is None:
            raise ValueError(f"the primitive {name!r} has no function: a row of the ledger not built")
        return declaration.function

    def built_names(self) -> tuple[str, ...]:
        return tuple(name for name, declaration in self.declarations.items() if declaration.built)
