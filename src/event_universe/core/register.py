"""The register of primitives: one name to one declaration and function, found by the features' folders (each declaring its name, place, word, reads, writes, order and the keys of the files it reads), read by the loop and the loader alone; the refusals at load by name; integers and names only."""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field, replace

from event_universe.core.schema import Key as Key

# the five places of the interval (ALGEBRA.md 9.91 (8)) and "any", the trace's read-only line
PLACES: tuple[str, ...] = ("(i)", "(ii)", "(iii)", "(iv)", "(v)", "any")
# the three words of ALGEBRA.md 9.111 item 7 (the right side, the step, after the step) and "any"
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
    """What one primitive declares: its name; its place (a code of 9.91 (8)) and its
    word (9.111 item 7); the values it reads and writes (the words of the ledger's
    columns, one string each); its order among the writers of the same value at
    the same place (an integer, or None where it is the only writer); its ALGEBRA.md
    line; its function once bound (None on a row of the ledger not built: the name
    is known, a term naming it is refused as not built); and its binder, the
    folder's `bind(loop)` that gives the function at load; and its schema, the keys of the
    files it reads under each object's word ("family"), read by the loader."""

    name: str
    place: str
    reads: tuple[str, ...]
    writes: tuple[str, ...]
    order: int | Mapping[str, int] | None = None
    function: Callable[..., object] | None = None
    section: str = ""
    word: str = ""
    binder: Binder | None = None
    schema: Mapping[str, tuple[Key, ...]] = field(default_factory=dict)

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
    """The one register, name to declaration, filled from the features' folders at load and read by the loop and the loader."""

    declarations: dict[str, Declaration] = field(default_factory=dict)
    owners: dict[tuple[str, str], str] = field(default_factory=dict)

    def add(self, declaration: Declaration) -> None:
        """Register one primitive; a name registered twice, or a key of the files read by two, is refused at load."""
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
        for word, keys in declaration.schema.items():
            for key in keys:
                owner = self.owners.setdefault((word, key.name), declaration.name)
                if owner != declaration.name:
                    raise ValueError(
                        f"the primitives {owner!r} and {declaration.name!r} both read the key "
                        f"{key.name!r} of {word}: one key, one reader"
                    )
        self.declarations[declaration.name] = declaration

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(self.declarations)

    def keys(self, word: str) -> tuple[Key, ...]:
        """Every primitive's keys of the files under one object's word, in the register's order."""
        return tuple(
            key for declaration in self.declarations.values() for key in declaration.schema.get(word, ())
        )

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
    body of code has moved in); neither: a row of the ledger not built; `SCHEMA` beside it,
    the keys of the files it reads, word to tuple of Keys, each with its section."""
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
    schema = getattr(module, "SCHEMA", None)
    if schema is None:
        return declaration
    rows = isinstance(schema, dict) and all(
        isinstance(word, str) and isinstance(keys, tuple) and all(isinstance(key, Key) for key in keys)
        for word, keys in schema.items()
    )
    if not rows:
        raise ValueError(
            f"the features folder {folder!r}: SCHEMA must map a word of the files to a tuple of Keys"
        )
    for word, keys in schema.items():
        for key in keys:
            if not key.section:
                raise ValueError(
                    f"the features folder {folder!r}: the key {key.name!r} of {word} names no ALGEBRA.md "
                    "section (an attribute with no section does not exist)"
                )
    return replace(declaration, schema=dict(schema))


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
