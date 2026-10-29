"""The record's schema 1.1: JSON Lines of whole numbers and labels, each line's kind its record's name in lower case."""

from dataclasses import dataclass

# The lines, in the order (round, kind, site, train): Header first; then Whole, Split, Turnover, Rate and Books; End
# last. The ledger's own file holds Ledger lines. The other records stand inside lines. A digest is SHA-256 in hex.
MAJOR = 1  # a breaking change; the decoder upcasts an older major and refuses an unknown one
MINOR = 1  # an added field; 1.1 names the operands, and the coupling row took its twelve fields at 1.1, before any record held one


@dataclass(frozen=True)
class File:
    """One of the three files, verbatim, with its digest."""

    name: str
    text: str
    digest: str


@dataclass(frozen=True)
class Kind:
    """One kind as the engine built it: index, label, dimension, its character on each class as a + b sqrt 2, T T."""

    index: int
    label: str
    dimension: int
    characters: tuple[tuple[int, int], ...]
    tt: int


@dataclass(frozen=True)
class Train:
    """One train: its index, its label, its kinds, its part and its winding."""

    index: int
    label: str
    kinds: tuple[int, ...]
    part: int
    winding: int


@dataclass(frozen=True)
class Header:
    """The first line. The board wraps by Rule3 at each side, its sites in the order named; every going starts at 0."""

    record: str
    major: int
    minor: int
    engine: str
    runner: str  # "synchronous", or the asynchronous run with its masks' seed named
    files: tuple[File, ...]
    sides: tuple[int, ...]
    order: str
    classes: tuple[int, ...]
    kinds: tuple[Kind, ...]
    trains: tuple[Train, ...]
    couplings: tuple[
        tuple[int, int, int, int, int, int, int, int, int, int, int, int], ...
    ]  # as the universe gives them
    operands: tuple[str, ...]  # the readings a coupling row's operand indexes, in order
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
    """One end of a whole click that takes at both, a reading of its own one-ended act: site, Spoke, books, push."""

    site: int
    spoke: int  # the Spoke's index in the board's six, +x, -x, +y, -y, +z, -z, toward the other end
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
    """A whole click (law 5): q windings left a train at a Node-clock, with the books and the parts it laid, the books in ends alone where both take."""

    round: int
    site: int
    count: int  # the count the Node-clock's beat reached, its first beat being 1
    dial: int  # its rate dial after the beat
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
    ends: tuple[
        Taking, ...
    ]  # both ends where both take, each its own one-ended act, taken and laid above then empty; none where one end takes
    children: tuple[Child, ...]
    lead: int
    twist: int


@dataclass(frozen=True)
class Split:
    """A split click (law 6 on the composite clock), its count and dial as a whole click's: c over room."""

    round: int
    site: int
    count: int
    dial: int
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
class Rate:
    """A Node-clock's k at its first beat and at each beat whose k differs from its last beat's, with the beat's count."""

    round: int
    site: int
    count: int  # the count the beat reached, the first beat being 1
    dial: int
    k: int  # a bit, 1 where the beat ticked, under the second promise: every rate within [0, the full rate]


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
