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
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field, replace

from event_universe.core.step import PLACES, Step

# THE THREE WORDS of 9.111 item 7, the mathematician's reading of the same interval:
# the right side (read from the interval's start), the step (the rule), after the
# step (the clicks, whose writes enter at t + 1); "any" the trace's.
WORDS: tuple[str, ...] = ("the right side", "the step", "after the step", "any")

Binder = Callable[[object], Callable[..., object]]


# a body's values (ALGEBRA.md 9.117 item 1): a click's write of one at (ii) is applied at (iv)
DEFERRED_VALUES: frozenset[str] = frozenset(
    {
        "a body's content M_k",
        "a body's momentum n",
        "a body's spin S",
        "a body's position",
        "a body's remainders",
    }
)

# a remainder is the dividing primitive's own record (ALGEBRA.md 9.117 item 1): no two writers collide
OWN_VALUES: frozenset[str] = frozenset({"a body's remainders", "the record's remainder"})


def folder_of(name: str) -> str:
    """The folder of a primitive's name: no article, no apostrophe, a space or a hyphen an underscore ("the spin's step" -> "spins_step")."""
    bare = name[4:] if name.startswith("the ") else name
    return bare.replace("'", "").replace("-", "_").replace(" ", "_")


@dataclass(frozen=True)
class Declaration:
    """What one primitive declares: its name, its place (9.91 (8)) and word (9.111 item 7), the values it reads and writes, its ALGEBRA.md line, its function once bound (None on a row not built) and its binder; its order among the writers of one value is the step file's."""

    name: str
    place: str
    reads: tuple[str, ...]
    writes: tuple[str, ...]
    function: Callable[..., object] | None = None
    section: str = ""
    word: str = ""
    binder: Binder | None = None

    @property
    def built(self) -> bool:
        return self.function is not None or self.binder is not None

    def place_of(self, value: str) -> str:
        """The place at which a write of `value` is ordered: a body's value left by a
        click at (ii) is a deferred write of (iv) (ALGEBRA.md 9.117 item 1)."""
        if self.place == "(ii)" and value in DEFERRED_VALUES:
            return "(iv)"
        return self.place


@dataclass
class Register:
    """The one register, name to declaration, filled from the features' folders at load and read by the loop."""

    declarations: dict[str, Declaration] = field(default_factory=dict)
    step: Step | None = None

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

    def check_step(self, step: Step) -> None:
        """The step file names registered primitives only, each at its declared place, and leaves out no built one; the register then refuses a call at a place the file does not list."""
        for place, names in step.places.items():
            for name in names:
                declaration = self.declarations.get(name)
                if declaration is None:
                    raise ValueError(
                        f"the step file lists {name!r} at {place}, which the register lacks; the "
                        f"primitives are {list(self.names)}"
                    )
                if declaration.place != place:
                    raise ValueError(
                        f"the step file lists {name!r} at {place}, but it declares {declaration.place}"
                    )
        for name in self.built_names():
            if step.position(name) is None:
                raise ValueError(
                    f"the step file leaves out the built primitive {name!r}: every bound primitive is "
                    "called in the file's order"
                )
        self.step = step

    def writers(self, value: str, place: str, step: Step) -> tuple[str, ...]:
        """The primitives writing `value` at `place` in the step file's order, a write deferred from an earlier place first."""
        found = []
        for declaration in self.declarations.values():
            if value in declaration.writes and declaration.place_of(value) == place:
                position = step.position(declaration.name)
                if position is None:
                    raise ValueError(
                        f"the primitive {declaration.name!r} writes {value!r} at the place {place} and is "
                        "not in the step file: the file orders the writers of one value"
                    )
                found.append((position[0] != place, position[1], declaration.name))
        return tuple(
            name for _deferred, _index, name in sorted(found, key=lambda item: (not item[0], item[1]))
        )

    def check_writers(self, step: Step) -> None:
        """Every value written by two primitives at one place has both in the step file, whose order is theirs."""
        groups: dict[tuple[str, str], int] = {}
        for declaration in self.declarations.values():
            for value in declaration.writes:
                if value not in OWN_VALUES:
                    key = (declaration.place_of(value), value)
                    groups[key] = groups.get(key, 0) + 1
        for (place, value), count in sorted(groups.items()):
            if count > 1:
                self.writers(value, place, step)

    def check_terms(self, terms: Iterable[tuple[str, str]]) -> None:
        """Every term of the files, as (label, name) pairs, names a primitive the register holds with a function."""
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
        """The function of a registered primitive, called by the loop at `place`: a call at another place, or at one the step file does not list, is refused."""
        declaration = self.declarations[name]
        if declaration.place not in (place, "any"):
            raise ValueError(
                f"the loop calls the primitive {name!r} at the place {place}, but it declares "
                f"{declaration.place}"
            )
        if (
            self.step is not None
            and name not in self.step.places.get(place, ())
            and declaration.place != "any"
        ):
            raise ValueError(
                f"the loop calls the primitive {name!r} at {place}, which the step file does not list there"
            )
        if declaration.function is None:
            raise ValueError(f"the primitive {name!r} has no function: a row of the ledger not built")
        return declaration.function

    def built_names(self) -> tuple[str, ...]:
        return tuple(name for name, declaration in self.declarations.items() if declaration.built)


def declaration_of(folder: str, module: object) -> Declaration:
    """One folder's declaration read from its module: `DECLARATION`, a `Declaration` or a dict of its words (name, place, reads, writes, section, optionally word), and `bind` or the declaration's own function; neither: a row not built."""
    declared = getattr(module, "DECLARATION", None)
    if isinstance(declared, Declaration):
        declaration = declared
    elif isinstance(declared, dict):
        keys = {"name", "place", "reads", "writes", "section"}
        unknown = set(declared) - keys - {"word"}
        missing = keys - set(declared)
        if unknown or missing:
            raise ValueError(
                f"the features folder {folder!r}: DECLARATION has unknown keys {sorted(unknown)} "
                f"or lacks {sorted(missing)}"
            )
        declaration = Declaration(
            str(declared["name"]),
            str(declared["place"]),
            tuple(str(value) for value in declared["reads"]),
            tuple(str(value) for value in declared["writes"]),
            None,
            str(declared["section"]),
            word=str(declared.get("word", "")),
        )
    else:
        raise ValueError(
            f"the features folder {folder!r} declares no DECLARATION (a Declaration of the register: "
            "the primitive's name, place, reads, writes, section)"
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
