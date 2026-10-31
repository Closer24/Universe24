"""Clock: the boundary between the board and the clicks: only the readers read it.
Algebra: schema 2.0, its version a label (VERSION), the major before the point and the minor after: JSON Lines of whole numbers of any width and labels, each line's kind its record's name in lower case.
Board: the header (the version, the files and their digests, the sides, each kind's characters on the 24, each train's kinds, part, winding, key and square flag), the click lines the run writes (a round, a Node-clock, a train, its q and each edge side that carried, the other train, the side's q and its tooth before and after), the end (the rounds, the digest, the run back exact or not) and the ledger's Count lines beside them.
Clicks: its click lines name a train, a Node-clock and a round and carry q, the sum of its sides' carries signed, a give below 0 and a take above it; nothing is computed in it.
"""

from dataclasses import dataclass

# The record's lines, in the order (round, site, train): Header first; then the Click lines; End last. The ledger's own
# file holds Count lines. The other records stand inside lines. A digest is SHA-256 in hex.
# The version, a label: its major before the point, its minor after. A minor's change is an added field or line that
# no reader needs, or a line no run writes retired; any other is a new major, and the decoder reads its own major
# alone. 2.0, from 1.4: every click line carries on its sides, in its site and across a Mesh, q 0 among them, and the
# line's tooth is retired, so no 1.x reader reads it (writer B's 1.4 line, DECODE3); the old engine's records and the
# ledger's line of winds retired (1.5); the version a label (Sofer's form 1). The 1.x minors stand in git.
VERSION = "2.0"


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
    version: str
    engine: str
    runner: str  # "synchronous": every Node-clock steps in every round
    files: tuple[File, ...]
    sides: tuple[int, ...]
    order: str
    kinds: tuple[Kind, ...]
    trains: tuple[Train, ...]
    operands: tuple[str, ...]  # the readings, in order, as the loader names them
    width: int
    dial: int  # the edge dial D, every edge side's key, read from the layout
    birth: int  # every edge side's tooth at its birth, (D - 1) div senses, as the load lays it


# One word, two things: a 1.4 click line's "sides" are its edge sides, one per other train at its Node-clock, and
# the header's "sides" are the board's, which the cone reads; the fields keep the names their writers give them.
SIDE = ("u", "q", "before", "after")  # a 1.4 click line's side, [u, q_tu, k_before, k_after], in order
ACROSS = ("u", "place", "q", "before", "after")  # a 1.4 side across a Mesh, the other clock at place


@dataclass(frozen=True)
class Click:
    """A click line: at a round and a Node-clock, a train's click carried q whole keys, a give below 0 and a take above it, on its sides: every edge side of its clock, [u, q_tu, k_before, k_after] in u's order, q_tu 0 included, q the sum of their q, k the train's own tooth on the edge with train u, within [0, K) at the card's edge key K, k_before as the round's carry reads it (the round's start on term 11's edges; after the round's turn where one comes), so x = K q_tu + k_after - k_before is the side's passing, and across its Mesh edge sides that carried (q the sum over both)."""

    round: int
    site: int
    train: int
    q: int
    sides: tuple[tuple[int, int, int, int], ...]
    # 1.4: each Mesh edge side that carried, [u, place, q_tu, k_before, k_after] by (place, u), place u's Node-clock
    # across the Spoke; its mirror [t, the line's site, -q_tu, K - 1 - k_before, K - 1 - k_after] in u's line there
    across: tuple[tuple[int, int, int, int, int], ...]


@dataclass(frozen=True)
class End:
    """The last line: the rounds, the state's digest, the rounds the rewind undid, and 1 where it came back exact."""

    rounds: int
    digest: str
    undone: int
    exact: int
    teeth: tuple[
        tuple[int, int, tuple[int, ...]], ...
    ]  # 1.4: per edge side (t, u), its tooth at every Node-clock at the end
    # 1.4: per Mesh edge side (Spoke, t, u) in that order, [t, u, the partner's place across the Spoke at every
    # Node-clock, the side's tooth at every Node-clock] at the end
    across: tuple[tuple[int, int, tuple[int, ...], tuple[int, ...]], ...]


@dataclass(frozen=True)
class Count:
    """A line of the ledger's own file, per round, Node-clock and train, at "step": the train's now counts there, row by row."""

    round: int
    at: str
    site: int
    train: int
    count: tuple[int, ...]
