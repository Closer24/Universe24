"""THE REGISTER OF PRIMITIVES (the model owner's decisions of 2026-09-26 through the
Boss, records 2208, 2212 and 2221; the short procedure of skills/workflow.md, point 5;
issue #1154; ALGEBRA.md 9.110 item 7, 9.111 item 7, 9.112 item 1).

A PRIMITIVE is a kind of attribute the engine can apply, written once and applied
to any family by its declaration in the run's files, never by a family's name. Its
IDENTITY is its unique English name, the key of the ledger's table of primitives
(docs/designs/generic_engine/ENGINE_LEDGER.md section 3). Every primitive is ONE
FOLDER under src/event_universe/features/<name>/, which declares its own name,
place, reads and writes (`DECLARATION`) and binds its function (`bind`); the
register FINDS THE FEATURES BY THEIR FOLDERS (`discover`), so adding a feature
touches no shared file, not even a list (record 2221 (3)). The engine holds ONE
register, name to function, read by the central loop alone. The refusals are the
loader's, at load, by name:

- a folder without a declaration, or whose name is not its declared name's;
- a name registered twice;
- a term of the files naming a primitive the register lacks, or one the register
  holds without a function (a row of the ledger not built yet);
- two primitives writing the same value at the same place with no order declared
  between them (a remainder is the writer's own record and never collides);
- a primitive called by the loop at a place other than the one it declares.

NO VERSION: a change of a primitive's behaviour keeps every shipped world bit for
bit or the primitive takes a new English name; the old keeps its function. This
module holds integers and names alone: no float, no family's name, no number of
the universe.
"""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field, replace

from event_universe.core.schema import Schema

# THE FIVE PLACES of the interval (ALGEBRA.md 9.91 (8)): (i) the clicking families'
# step with the transport, every component; (ii) the bookings at the Ports, the
# ladder, the takings and the givings; (iii) the held families' step; (iv) the holds
# written, the clicks' changes of M, Q and n included; (v) the bodies on one Node,
# the feed, the induction, the spin's step, the recoil's accumulator. "any" is the
# trace's, a read-only line at every place.
PLACES: tuple[str, ...] = ("(i)", "(ii)", "(iii)", "(iv)", "(v)", "any")
# THE THREE WORDS of 9.111 item 7, the mathematician's reading of the same interval:
# the right side (read from the interval's start), the step (the rule), after the
# step (the clicks, whose writes enter at t + 1); "any" the trace's.
WORDS: tuple[str, ...] = ("the right side", "the step", "after the step", "any")

Binder = Callable[[object], Callable[..., object]]


# THE VALUES a body's record holds (ALGEBRA.md 9.117 item 1): a write of one of them
# left by a click at (ii) is a deferred write, applied at (iv) with the click's other
# writes (9.111 item 6), so the register orders it among the writers at (iv)
DEFERRED_VALUES: frozenset[str] = frozenset(
    {
        "a body's content M_k",
        "a body's momentum n",
        "a body's spin S",
        "a body's position",
        "a body's remainders",
    }
)

# THE VALUES THAT ARE THE WRITER'S OWN (ALGEBRA.md 9.91 (2), (3); 9.117 item 1: "a body's
# remainders", one per division of every primitive on the body): a remainder lives on
# the record of the primitive that divided (core/primitive.py, Own), so two primitives
# writing it at one place never collide and the register orders no writers of it
OWN_VALUES: frozenset[str] = frozenset({"a body's remainders", "the record's remainder"})


def folder_of(name: str) -> str:
    """The folder a primitive's name takes (the mathematician's contract, PRs 1164 and
    1165): the name without "the ", the apostrophe dropped, a space or a hyphen an
    underscore ("the spin's step" -> "spins_step", "the self-source" -> "self_source")."""
    bare = name[4:] if name.startswith("the ") else name
    return bare.replace("'", "").replace("-", "_").replace(" ", "_")


@dataclass(frozen=True)
class Declaration:
    """What one primitive declares: its name; its place (9.91 (8)) and its word (9.111
    item 7); the values it reads and writes (the ledger's words); its order among the
    writers of one value at one place (None where alone); its ALGEBRA.md line; its
    function once bound (None on a row not built: a term naming it is refused); its
    binder `bind(loop)`; and its schema, its keys of the files (core/schema.py)."""

    name: str
    place: str
    reads: tuple[str, ...]
    writes: tuple[str, ...]
    order: int | Mapping[str, int] | None = None
    function: Callable[..., object] | None = None
    section: str = ""
    word: str = ""
    binder: Binder | None = None
    schema: Schema | None = None

    @property
    def built(self) -> bool:
        return self.function is not None or self.binder is not None

    def order_of(self, value: str) -> int | None:
        """The order among the writers of `value`: one integer for every value the
        primitive writes, or a mapping value to integer (a primitive that writes two
        values with different orders, the giving of ALGEBRA.md 9.117 item 2), or None."""
        if isinstance(self.order, Mapping):
            return self.order.get(value)
        return self.order

    def place_of(self, value: str) -> str:
        """The place at which a write of `value` is ordered: a body's value left by a
        click at (ii) is a deferred write of (iv) (ALGEBRA.md 9.117 item 1)."""
        if self.place == "(ii)" and value in DEFERRED_VALUES:
            return "(iv)"
        return self.place


@dataclass
class Register:
    """The one register: name to declaration, filled from the features' folders at
    load and read by the loop at every interval; nothing else registers and nothing
    else reads it."""

    declarations: dict[str, Declaration] = field(default_factory=dict)

    def add(self, declaration: Declaration) -> None:
        """Register one primitive; a name registered twice is refused at load."""
        if declaration.place not in PLACES:
            raise ValueError(
                f"the primitive {declaration.name!r} declares the place {declaration.place!r}, "
                f"which is none of the interval's places {list(PLACES)}"
            )
        if declaration.word and declaration.word not in WORDS:
            raise ValueError(
                f"the primitive {declaration.name!r} declares the word {declaration.word!r}, "
                f"which is none of {list(WORDS)} (ALGEBRA.md 9.111 item 7)"
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

    def bind(self, loop: object) -> None:
        """Every declared binder gives its function for this loop (at load, once)."""
        for name, declaration in list(self.declarations.items()):
            if declaration.binder is not None:
                self.declarations[name] = replace(declaration, function=declaration.binder(loop))

    def check_writers(self) -> None:
        """Two primitives writing the same value at the same place without an order
        declared between them are refused (record 2212 (3))."""
        writers: dict[tuple[str, str], list[Declaration]] = {}
        for declaration in self.declarations.values():
            for value in declaration.writes:
                if value in OWN_VALUES:
                    continue
                writers.setdefault((declaration.place_of(value), value), []).append(declaration)
        for (place, value), group in sorted(writers.items()):
            if len(group) < 2:
                continue
            orders = [declaration.order_of(value) for declaration in group]
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


def declaration_of(folder: str, module: object) -> Declaration:
    """One folder's declaration read from its module: `DECLARATION`, a `Declaration`
    of this register (the mathematician's folders, PRs 1164 and 1165) or a dict of
    its words (name, place, reads, writes, section, and optionally word and order),
    and `bind`, the loop's binder, or the declaration's own function (a folder whose
    body of code has moved in); neither: a row of the ledger not built."""
    declared = getattr(module, "DECLARATION", None)
    if isinstance(declared, Declaration):
        declaration = declared
    elif isinstance(declared, dict):
        keys = {"name", "place", "reads", "writes", "section"}
        unknown = set(declared) - keys - {"order", "word"}
        missing = keys - set(declared)
        if unknown or missing:
            raise ValueError(
                f"the features folder {folder!r}: DECLARATION has unknown keys {sorted(unknown)} "
                f"or lacks {sorted(missing)}"
            )
        order = declared.get("order")
        declaration = Declaration(
            str(declared["name"]),
            str(declared["place"]),
            tuple(str(value) for value in declared["reads"]),
            tuple(str(value) for value in declared["writes"]),
            order if isinstance(order, Mapping) or order is None else int(order),
            None,
            str(declared["section"]),
            word=str(declared.get("word", "")),
        )
    else:
        raise ValueError(
            f"the features folder {folder!r} declares no DECLARATION (a Declaration of the register: "
            "the primitive's name, place, reads, writes, order, section)"
        )
    if folder_of(declaration.name) != folder:
        raise ValueError(
            f"the features folder {folder!r} declares the name {declaration.name!r}, whose folder is "
            f"{folder_of(declaration.name)!r}: one folder, one name"
        )
    binder = getattr(module, "bind", None)
    if binder is not None and not callable(binder):
        raise ValueError(
            f"the features folder {folder!r}: bind must be a function of the loop or absent"
        )
    if binder is not None:
        declaration = replace(declaration, binder=binder)
    return declaration


def discover(package: str = "event_universe.features") -> Register:
    """The register filled from the features' folders: every subpackage of `package`
    in the folders' order, each read by `declaration_of`; nothing else registers."""
    root = importlib.import_module(package)
    register = Register()
    for info in sorted(pkgutil.iter_modules(root.__path__), key=lambda found: found.name):
        if not info.ispkg:
            continue
        module = importlib.import_module(f"{package}.{info.name}")
        register.add(declaration_of(info.name, module))
    return register
