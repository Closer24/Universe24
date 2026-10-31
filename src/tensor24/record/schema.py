"""Clock: the boundary between the board and the clicks: only the readers read it.
Algebra: schema 1.3: JSON Lines of whole numbers of any width and labels, each line's kind its record's name in lower case; its minor, MINOR = len(ADDED), is the count of its changes spelt as a length, which ARCHITECTURE section 6 left to be read from the schema with 1.3: not yet read from the schema's structure, it is named here, open for the owner (the first hostile code reader's M11).
Board: the header (the files and their digests, the sides, each kind's characters on the 24, each train's kinds, part, winding, key and square flag), the click lines the run writes (a round, a Node-clock, a train, its q and its click tooth before and after), the end (the rounds, the digest, the run back exact or not) and the ledger's Count lines beside them.
Clicks: its click lines name a train, a Node-clock and a round and carry q, the click tooth's carry signed, a give below 0 and a take above it; nothing is computed in it.
"""

from dataclasses import dataclass

# The record's lines, in the order (round, kind, site, train): Header first; then Whole, Click, Split, Rate and Books;
# End last. The run writes Click lines; no run writes a Whole, Split, Rate or Books line, every Node-clock stepping in
# every round and the clicks standing in the Click line, and their records stay for the records read before. The
# ledger's own file holds Ledger and Count lines, a Count line told by its site, which a Ledger line lacks. The other
# records stand inside lines. A digest is SHA-256 in hex.
MAJOR = 1  # a breaking change; the decoder upcasts an older major and refuses an unknown one
# each minor version's change in order: an added field or line that no reader needs, or a line no run writes retired
ADDED = (
    "the operands named, the coupling row's twelve fields",
    "the ledger's count per Node-clock (Animate's G1), read by her 1.2 reader, which keys a ledger line by round, at,"
    " site and train (the 1.1 reader's guard refused them); the turnover and the rate lines retired, no run writing either",
    "the click line, one per round, Node-clock and train whose click tooth carried, its q the carry's quotient signed"
    " (a give below 0, a take above it) and its tooth before and after; the train card's key and square flag and the"
    " kind card's characters, its trace on each of the 24 turns; the couplings, the classes, the draw and the kind"
    " card's T T retired, no run writing them",
)
MINOR = len(ADDED)


@dataclass(frozen=True)
class File:
    """One of the three files, verbatim, with its digest."""

    name: str
    text: str
    digest: str


@dataclass(frozen=True)
class Kind:
    """One kind as the engine built it: index, label, dimension, and its characters, its trace on each of the 24 turns in the turns' order."""

    index: int
    label: str
    dimension: int
    characters: tuple[int, ...]


@dataclass(frozen=True)
class Train:
    """One train: its index, its label, its kinds, its part, its winding, its key (the click tooth's) and its square flag, 1 on the four-vector's square."""

    index: int
    label: str
    kinds: tuple[int, ...]
    part: int
    winding: int
    key: int
    square: int


@dataclass(frozen=True)
class Header:
    """The first line. The board wraps by Rule3 at each side, its sites in the order named."""

    record: str
    major: int
    minor: int
    engine: str
    runner: str  # "synchronous": every Node-clock steps in every round
    files: tuple[File, ...]
    sides: tuple[int, ...]
    order: str
    kinds: tuple[Kind, ...]
    trains: tuple[Train, ...]
    operands: tuple[str, ...]  # the readings, in order, as the loader names them
    width: int


# One word, two things: a 1.4 click line's "sides" are its edge sides, one per other train at its Node-clock, and
# the header's "sides" are the board's, which the cone reads; the fields keep the names their writers give them.
SIDE = ("u", "q", "before", "after")  # a 1.4 click line's side, [u, q_tu, k_before, k_after], in order
ACROSS = ("u", "place", "q", "before", "after")  # a 1.4 side across a Mesh, the other clock at place


@dataclass(frozen=True)
class Click:
    """A click line: at a round and a Node-clock, a train's click tooth carried q whole keys, a give below 0 and a take above it, its tooth before and after."""

    round: int
    site: int
    train: int
    q: int
    tooth: tuple[int, int]


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
    count: int  # the count the Node-clock's beat reached, its first beat being 1 (the asynchronous runner's; G3 names it)
    dial: int  # its rate dial after the beat (the asynchronous runner's)
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
    """A split click (law 6 on the composite clock), its count and dial as a whole click's (the asynchronous runner's): c over room."""

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
    """A Node-clock's k at its first beat and at each beat whose k differs from its last beat's, with the beat's count: the asynchronous runner's line, which no run writes since G1b."""

    round: int
    site: int
    count: int  # the count the beat reached, the first beat being 1
    dial: int
    k: int  # a bit, 1 where the beat ticked


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
class Count:
    """A line of the ledger's own file, per round, Node-clock and train, at "step": the train's now counts there, row by row."""

    round: int
    at: str
    site: int
    train: int
    count: tuple[int, ...]


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
