"""The main loop: the interval's frame (the clock, the deferred writes, the closing), the walk of the step file's acts through the register, and the run-time guards of the views, the writers and the Ports; the stages are the loop object's, handed in, never imported (core/ imports core/ alone)."""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

from event_universe.core.primitive import Write
from event_universe.core.register import DEFERRED_VALUES, OWN_VALUES, Register
from event_universe.core.step import Step

Words = dict[str, object]
Fingerprints = Mapping[str, Mapping[Any, Any]]
ALIVE = "the records alive"
STAGE, GENERIC, LISTED = "stage", "generic", "listed"


@dataclass(frozen=True)
class Stage:
    """One whole-board stage of the loop object: its function, the words it takes, the cards whose writes it carries (a fused stage carries several)."""

    function: Callable[..., None]
    words: tuple[str, ...] = ()
    carries: tuple[str, ...] = ()


@dataclass(frozen=True)
class Act:
    """One act of the file bound: its place, name and words, its kind (a whole-board stage, a card's own function per term, or a listed name whose call is inside another act), its stage and the ledger's words it may change."""

    place: str
    name: str
    words: Words
    kind: str
    stage: Stage | None
    permitted: frozenset[str]


def read_only(array: Any) -> Any:
    """A view of the array that refuses every write (the interval's start as a right-side primitive sees it); the base is untouched."""
    view = array.view()
    view.flags.writeable = False
    return view


def _freeze(arrays: Any, frozen: bool) -> None:
    """The arrays' write flag set (numpy's own refusal at a write; a guard, not a proof: a primitive may thaw a view); a view whose base is frozen elsewhere is left as it is."""
    for array in arrays:
        try:
            array.flags.writeable = not frozen
        except ValueError:
            pass


def _changed(before: Mapping[Any, Any], after: Mapping[Any, Any]) -> set[Any]:
    """The targets whose stamp differs, present on both sides (a target that appears or vanishes is the records-alive word's)."""
    return {target for target, stamp in after.items() if target in before and before[target] != stamp}


@dataclass
class MainLoop:
    """The walk and its guards for one loaded world: the acts planned at load, run once per interval on the loop object handed in."""

    register: Register
    step: Step
    acts: tuple[Act, ...]
    chain: tuple[str, ...]
    terms: tuple[tuple[str, str], ...]
    flush_at: int | None
    deferred: list[tuple[int, str, Write]] = field(default_factory=list)
    sequence: int = 0
    written: dict[tuple[str, object], list[str]] = field(default_factory=dict)
    claimed: list[set[tuple[str, object]]] = field(default_factory=list)
    walked: list[str] = field(default_factory=list)

    @classmethod
    def plan(
        cls,
        register: Register,
        step: Step,
        stages: Mapping[str, Stage],
        chain: tuple[str, ...],
        terms: Any,
    ) -> MainLoop:
        """The file's built acts in the file's order, each bound to its kind; refused at load: a built name with no stage, no chain and no function of its own; words a stage does not take; the chain reordered or interrupted; a (ii) card writing a body's value with no (iv) act after the (ii) acts."""
        built = set(register.built_names())
        acts: list[Act] = []
        for place, name, words in step.acts:
            if name not in built:
                continue
            declaration = register.declarations[name]
            stage = stages.get(name)
            if stage is not None:
                kind, taken, carries = STAGE, stage.words, stage.carries
            elif name in chain:
                kind, taken, carries = LISTED, (), ()
            elif declaration.binder is None:
                kind, taken, carries = GENERIC, (), (name,)
            else:
                raise ValueError(
                    f"the loop has no stage for the built primitives [{name!r}]: every built primitive "
                    "of the step file is bound to one act of the loop"
                )
            if sorted(dict(words)) != sorted(taken):
                raise ValueError(
                    f"the step file's act {name!r} at {place} carries the words {sorted(dict(words))}; "
                    f"the loop's stage of {name!r} takes {sorted(taken)}"
                )
            permitted = frozenset(
                value for card in carries for value in register.declarations[card].writes
            )
            if name == "the giving":
                permitted = permitted | {ALIVE}
            acts.append(Act(place, name, dict(words), kind, stage, permitted))
        _check_chain(acts, chain, built)
        return cls(register, step, tuple(acts), chain, tuple(terms), _flush_index(acts, register))

    def run(self, loop: Any) -> None:
        """One interval: the clock; the start's arrays frozen (and after each act the arrays it rebound); each act through the register with its grants and its writes audited; the deferred writes applied before the first (iv) act after (ii); the closing; the start thawed."""
        loop.tick += 1
        self.written.clear()
        self.walked.clear()
        loop.ports.begin()
        frozen: list[tuple[Any, ...]] = []

        def freeze_now() -> None:
            """Every array the loop holds at this moment frozen: at the start, and after each act, so that an array an act rebound (a record's stepped level) is frozen for the acts after it."""
            arrays = tuple(loop.start_arrays())
            _freeze(arrays, True)
            frozen.append(arrays)

        freeze_now()
        try:
            for index, act in enumerate(self.acts):
                if index == self.flush_at:
                    self.flush(loop)
                function = self.register.at(act.name, act.place)
                self.walked.append(act.name)
                opened = tuple(loop.grants(act.name))
                _freeze(opened, False)
                with self.act(act.name, act.place, act.permitted, loop.fingerprints):
                    if act.kind == STAGE and act.stage is not None:
                        act.stage.function(function, **act.words)
                    elif act.kind == GENERIC:
                        self.generic(loop, act, function)
                _freeze(opened, True)
                freeze_now()
            if self.deferred:
                raise ValueError(
                    "a deferred write is left after the walk: the step file lists no (iv) act after (ii)"
                )
            with self.act("the closing", "any", frozenset({ALIVE}), loop.fingerprints):
                loop.close_interval()
        finally:
            for arrays in frozen:
                _freeze(arrays, False)

    @contextmanager
    def act(
        self,
        name: str,
        place: str,
        permitted: frozenset[str],
        fingerprints: Callable[[], Fingerprints],
    ) -> Iterator[None]:
        """One act, whole-board or nested: the fingerprints before and after, the change audited under `name`; a nested act claims its changes so the act around it does not answer for them."""
        before = fingerprints()
        self.claimed.append(set())
        try:
            yield
        except ValueError as error:
            if "read-only" in str(error):
                raise ValueError(
                    f"the primitive {name!r} at {place} wrote into an array of the interval's start: "
                    "its card names no such write"
                ) from error
            raise
        mine = self.claimed.pop()
        self.audit(name, place, permitted, before, fingerprints(), mine)
        if self.claimed:
            self.claimed[-1] |= mine

    def generic(self, loop: Any, act: Act, function: Callable[..., Any]) -> None:
        """The act of a card with a function of its own and no stage of the loop: once per term of the files naming it, writes = function(term, start, own), the writes taken by the loop."""
        for label, name in self.terms:
            if name != act.name:
                continue
            for write in function(
                loop.term_of(label, name), loop.start_view(), loop.own_of(label, name)
            ):
                self.accept(loop, act, write)

    def accept(self, loop: Any, act: Act, write: Write) -> None:
        """One write of a primitive: refused outside its card's words; a body's value written at (ii) is deferred to (iv); else applied now and audited under the card."""
        card = self.register.declarations[act.name]
        if write.value not in card.writes:
            raise ValueError(
                f"the primitive {act.name!r} wrote {write.value!r}, which its card does not name "
                f"({list(card.writes)})"
            )
        if card.place_of(write.value) != act.place:
            if not write.deferred:
                raise ValueError(
                    f"the primitive {act.name!r} at {act.place} wrote {write.value!r} now; a body's "
                    "value written at (ii) enters at (iv) and must be deferred"
                )
            self.sequence += 1
            self.deferred.append((self.sequence, act.name, write))
            return
        loop.apply_write(write)

    def flush(self, loop: Any) -> None:
        """The deferred writes applied once, in the register's order of the writers of each value at (iv) (a write deferred from (ii) first), then by arrival; each noted under its card as a writer at (iv)."""

        def key(item: tuple[int, str, Write]) -> tuple[int, int]:
            sequence, name, write = item
            return (self.register.writers(write.value, "(iv)", self.step).index(name), sequence)

        for _sequence, name, write in sorted(self.deferred, key=key):
            loop.apply_write(write)
            self.note(name, "(iv)", write.value, write.of)
        self.deferred.clear()

    def audit(
        self,
        name: str,
        place: str,
        permitted: frozenset[str],
        before: Fingerprints,
        after: Fingerprints,
        claimed: set[tuple[str, object]],
    ) -> None:
        """A changed word outside the act's words is refused by act, word and target; a second writer of one (word, target) in the interval is refused unless the step file orders it after the first (an own value never collides)."""
        for word, targets in after.items():
            changed = _changed(before.get(word, {}), targets)
            if word == ALIVE:
                changed = set(targets) ^ set(before.get(word, {}))
            changed -= {target for w, target in claimed if w == word}
            if not changed:
                continue
            if word not in permitted:
                raise ValueError(
                    f"the act {name!r} at {place} changed {word!r} of {sorted(map(repr, changed))}; "
                    f"its card names {sorted(permitted)}"
                )
            for target in changed:
                self.note(name, place, word, target)
                if self.claimed:
                    self.claimed[-1].add((word, target))

    def note(self, name: str, place: str, word: str, target: object) -> None:
        """One writer of one (word, target) this interval; a second distinct name must follow the first in the file's order of the writers."""
        names = self.written.setdefault((word, target), [])
        if names and name not in names and word not in OWN_VALUES and word != ALIVE:
            declaration = self.register.declarations.get(name)
            order = (
                self.register.writers(word, declaration.place_of(word), self.step)
                if declaration is not None
                else ()
            )
            if name not in order or any(
                earlier not in order or order.index(earlier) > order.index(name) for earlier in names
            ):
                raise ValueError(
                    f"{word!r} of {target!r} was written by {names} and then by {name!r} in one "
                    "interval; the step file orders no such pair"
                )
        if not names or names[-1] != name:
            names.append(name)


def _check_chain(acts: list[Act], chain: tuple[str, ...], built: set[str]) -> None:
    """The record's fused chain in the file's order, no whole-board act between its names but the operation's."""
    positions = [index for index, act in enumerate(acts) if act.name in chain]
    ordered = [acts[index].name for index in positions]
    between = (
        [
            act.name
            for act in acts[positions[0] : positions[-1] + 1]
            if act.kind == STAGE and act.name != "the operation"
        ]
        if positions
        else []
    )
    if ordered != [name for name in chain if name in built] or between:
        raise ValueError(
            f"the record's step is one chain today: {', '.join(chain)}; the file orders them as "
            f"{', '.join(ordered) or 'none of them'}"
            + (f", with {', '.join(between)} between them" if between else "")
        )


def _flush_index(acts: list[Act], register: Register) -> int | None:
    """The index of the first (iv) act after the last (ii) act, where the deferred writes of (ii) are applied; refused when a (ii) card writes a body's value and no such act exists."""
    last_ii = max((index for index, act in enumerate(acts) if act.place == "(ii)"), default=None)
    if last_ii is None:
        return None
    found = next(
        (index for index, act in enumerate(acts) if index > last_ii and act.place == "(iv)"), None
    )
    deferring = [
        act.name
        for act in acts
        if act.place == "(ii)" and set(register.declarations[act.name].writes) & DEFERRED_VALUES
    ]
    if found is None and deferring:
        raise ValueError(
            f"the step file lists {deferring} at (ii), whose writes of a body's value enter at (iv), "
            "and no (iv) act after (ii)"
        )
    return found
