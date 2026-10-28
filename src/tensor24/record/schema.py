"""The record's schema, version 1: the events the runner writes from the engine's out, integers and labels."""

from dataclasses import dataclass

VERSION = 1


@dataclass(frozen=True)
class Header:
    """The run's header: the schema's version, the three files' digests, the board's shape, the trains."""

    version: int
    universe: str
    piece: str
    setting: str
    shape: tuple[int, ...]
    trains: tuple[str, ...]
    kinds: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class WholeClick:
    """A whole click: q quanta left a train's component at a Node-clock, and the remainder stayed."""

    tick: int
    site: int
    train: int
    component: int
    q: int
    kept: int


@dataclass(frozen=True)
class SplitClick:
    """A split click: the draw's number c over its room picked one part by the parts' sizes."""

    tick: int
    site: int
    train: int
    sizes: tuple[int, ...]
    c: int
    room: int
    part: int
    kept: int


@dataclass(frozen=True)
class Write:
    """An additive write a click made at the receiving Node-clock."""

    tick: int
    site: int
    train: int
    component: int
    amount: int


@dataclass(frozen=True)
class Turnover:
    """A turnover: a Node-clock's time gear carried q at its own top."""

    tick: int
    site: int
    q: int


@dataclass(frozen=True)
class Ledger:
    """A round's books over the board: the wind, the sweep, the push and the remainders booked."""

    tick: int
    wind: int
    sweep: int
    push: int
    booked: int
