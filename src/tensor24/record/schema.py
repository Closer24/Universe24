"""The record's schema 1.0: JSON Lines of whole numbers and labels, each line's kind its record's name in lower case."""

from dataclasses import dataclass

MAJOR = 1  # a breaking change; the decoder upcasts an older major and refuses an unknown one
MINOR = 0  # an added field


@dataclass(frozen=True)
class File:
    """One of the three files, verbatim, with its digest."""

    name: str
    text: str
    digest: str


@dataclass(frozen=True)
class Kind:
    """One kind of the 24 as the engine built it: its index, label, dimension, characters on the classes, T T."""

    index: int
    label: str
    dimension: int
    characters: tuple[int, ...]
    tt: int


@dataclass(frozen=True)
class Train:
    """One train: its index, label, kinds, own size and winding, and its coupling rows as the universe gives them."""

    index: int
    label: str
    kinds: tuple[int, ...]
    size: int
    winding: int
    couplings: tuple[tuple[int, int, int, int, int, int], ...]


@dataclass(frozen=True)
class Header:
    """The first line. The board wraps by Rule3 at each side, its sites in the order named; every going starts at 0."""

    record: str
    major: int
    minor: int
    engine: str
    runner: str
    files: tuple[File, ...]
    sides: tuple[int, ...]
    sites: int
    order: str
    classes: tuple[int, ...]
    kinds: tuple[Kind, ...]
    trains: tuple[Train, ...]
    draw: int
    width: int


@dataclass(frozen=True)
class Holding:
    """One train's holding at a click: its windings and its remainder, each before and after."""

    train: int
    windings: tuple[int, int]
    kept: tuple[int, int]


@dataclass(frozen=True)
class Taking:
    """One end of a whole click that takes at both ends, a reading of its own one-ended act: site, books, push."""

    site: int
    taken: tuple[Holding, ...]
    laid: tuple[Holding, ...]
    push: tuple[int, int, int]


@dataclass(frozen=True)
class Child:
    """A part a whole click laid: its train, its Node-clock, its sweep after the lay, its push and moment at it."""

    train: int
    site: int
    sweep: int
    push: tuple[int, int, int]
    moment: tuple[int, int, int]


@dataclass(frozen=True)
class Reading:
    """A twin pair's reading in the axis form: its train, rho and the spin's three integers."""

    train: int
    rho: int
    spin: tuple[int, int, int]


@dataclass(frozen=True)
class Whole:
    """A whole click (law 5): q windings left a train at a Node-clock, with the books and the parts it laid."""

    round: int
    site: int
    count: int  # the Node-clock's own beat count c, read at its site
    dial: int  # its rate dial after the beat
    steps: int  # its ticks so far, the runner's count of Out's k, which the engine never reads
    spoke: int | None  # the Spoke's index in the six where two ends hold the click, else None
    far: int | None  # the far end's site: a reading of the two one-ended acts, never an act joining them
    train: int
    q: int
    winding: int
    tooth: tuple[int, int]
    wind: tuple[int, int]
    sweep: int
    push: tuple[int, int, int]
    moment: tuple[int, int, int]
    taken: tuple[Holding, ...]
    laid: tuple[Holding, ...]
    ends: tuple[Taking, ...]
    children: tuple[Child, ...]
    lead: int
    twist: int


@dataclass(frozen=True)
class Split:
    """A split click (law 6 on the composite clock), its count, dial and steps as a whole click's: c over room."""

    round: int
    site: int
    count: int
    dial: int
    steps: int
    train: int
    sizes: tuple[int, ...]
    kinds: tuple[int, ...]
    c: int
    room: int
    drawn: int
    q: int
    tooth: tuple[int, int]
    wind: tuple[int, int]
    detector: Reading
    written: Reading


@dataclass(frozen=True)
class Turnover:
    """A turnover (law 4): the time gear's carry q at its top, T's bit, with the gear's reading there."""

    round: int
    site: int
    count: int
    q: int
    x: int


@dataclass(frozen=True)
class Rate:
    """A change of a Node-clock's tick, written at the change alone: k 0 where the dial stops, 1 at the release."""

    round: int
    site: int
    count: int
    dial: int
    steps: int
    k: int


@dataclass(frozen=True)
class Books:
    """A remainder booked at a Node-clock, signed (law 8's books)."""

    round: int
    site: int
    train: int
    kept: int


@dataclass(frozen=True)
class End:
    """The last line: the rounds, the state's digest, the rounds the rewind undid, and 1 where it came back exact."""

    rounds: int
    digest: str
    undone: int
    exact: int


@dataclass(frozen=True)
class Ledger:
    """A line of the ledger's own file, per round and train, at "step" (after the step) or "clicks" (after them)."""

    round: int
    at: str
    train: int
    wind: int
    sweep: int
    push: tuple[int, int, int]
    moment: tuple[int, int, int]
    windings: int
