"""The draw's declaration (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment: a seed, its draw; #the-click-is-the-meeting, the pair's form and the GHZ gate): on the world the `draw`, the window in intervals after which the NodeDetectors over regions draw and write their click, the seed and the generator's multiplier and increment (x <- (multiplier x + increment) mod 2^width, the width the file's), every one the file's and none the engine's (`Draw`, `draw_of`), and the meeting's reading, root or back (`meeting`, ALGEBRA.md, The click is the meeting of the future with the past; the owner's word of 2026-10-19): `root`, the one draw through the root over the joint shares (the default where the key is absent, written nowhere, so every world without the key runs bit for bit), or `back`, the click that runs back (`meeting_back`: the first side draws at its own place, the result runs back along the record to its birth and forward to the partner, the partner draws at its own place on the credit's re-weighted parts), admitted where a joint credit exists and the record's birth is one interval (`meeting_of_the_law`); a body with a probe among its transitions (a transition of a part into itself) declares its generator alone (`Generator`, `generator_of`), its window bounded by the probe's lays at its Node (ALGEBRA.md, The pulsed gate), and no body's `node_detector` admits the meeting, the world's draw's word; and on a node_detector's region its setting `basis` (p, q), the coefficients of its credit, and its parts' `pattern`, one integer pair [alpha_k, beta_k] per part of the record it reads, the + port reading the part k as e_k(+) = alpha_k p + beta_k q and the - port as e_k(-) = alpha_k (-q) + beta_k p (the pair's pattern [[1, 0], [0, 1]], the ports (p, q) and (-q, p); `ports_of`, the two ports exactly orthogonal with equal norms, refused by name otherwise), read by the reader (`tools/bell_gate.py`) and by the draw through the root in the run; every defect refused by name and no default written."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from event_universe.core.integer import MAX_WORK_INT
from event_universe.loader.derived import FamilyRule
from event_universe.loader.keys import integer, keyed

Pattern = tuple[tuple[int, int], ...]  # per part [alpha_k, beta_k], the part's read of the setting
Ports = tuple[tuple[int, ...], tuple[int, ...]]  # a side's two ports, + then -, one coefficient per part
GENERATOR_KEYS = (
    "seed",
    "multiplier",
    "increment",
)  # a draw's generator: the keys of a body whose window is bounded by its probe's lays
DRAW_KEYS = (
    "window",
    *GENERATOR_KEYS,
)  # the draw with its window: the world's and a body's without a probe
MEETING = "meeting"  # the world's draw's key: the meeting's reading, root or back
ROOT, BACK = "root", "back"  # its two words: the one draw through the root, the click that runs back
MEETINGS = (ROOT, BACK)
REACH = "reach"  # the back mode's key: the run back's reach, the owner's word of 2026-10-19
BOARD, CONE, BOOKS = (
    "board",
    "cone",
    "books",
)  # its three words: the whole board, the record's light cone, no run
REACHES = (BOARD, CONE, BOOKS)
WORLD_DRAW_KEYS = (
    *DRAW_KEYS,
    MEETING,
    REACH,
)  # the world's draw alone declares the meeting and its reach


@dataclass(frozen=True)
class Generator:
    """A draw's generator as the files declare it: the seed and the generator's multiplier and increment, x <- (multiplier x + increment) mod 2^width (features/click); a body with a probe among its transitions declares this alone under `node_detector`, its window bounded by the probe's lays at its Node, the world's schedule (ALGEBRA.md, The pulsed gate; the two hands)."""

    seed: int
    multiplier: int
    increment: int


@dataclass(frozen=True)
class Draw(Generator):
    """A draw with its declared window beside the generator's three keys: the world's (the intervals after which every node_detector's window closes and the NodeDetector draws and writes), a record converted whole's (its table's rate per window) and a body's without a probe (declared where a drive's lay has no end, derived from the lays' passage over the body otherwise, `loader/window.py`, 2026-10-19); and the meeting's reading, `root` or `back` (`MEETINGS`), the world's draw's alone, `root` where the file declares none (the one draw through the root as built, written nowhere); beside `back` the run back's reach, `board`, `cone` or `books` (`REACHES`, `meeting_back`), None where the file declares none, which the engine reads as the record's light cone (`credit.Books.reach`, the owner's word of 2026-10-19), written nowhere."""

    window: int
    meeting: str = ROOT
    reach: str | None = None


def generator_of(value: object, label: str) -> Generator:
    """A body's `node_detector` where a probe stands among its transitions: the generator's three keys, the seed and the increment from 0 and the multiplier from 1; a `window` refused by name, the window of a body with a probe being bounded by the probe's lays at its Node, the world's schedule and no number of the body's (ALGEBRA.md, The pulsed gate; the two hands); every other key refused by name, the meeting's reading among them (`keyed`: a body's generator admits no `meeting`, the world's draw's word)."""
    if isinstance(value, dict) and "window" in value:
        raise ValueError(
            f"{label} declares a window beside a probe, and the window of a body with a probe is bounded by the "
            f"probe's lays at its Node, the world's schedule (ALGEBRA.md, The pulsed gate); its keys are "
            f"{list(GENERATOR_KEYS)}"
        )
    found = keyed(value, label, GENERATOR_KEYS, GENERATOR_KEYS)
    return Generator(
        integer(found["seed"], f"{label}.seed", 0),
        integer(found["multiplier"], f"{label}.multiplier", 1),
        integer(found["increment"], f"{label}.increment", 0),
    )


def draw_of(value: object, label: str, world: bool = False) -> Draw:
    """The world's `draw` (`world`), a record converted whole's `node_detector` and a body's that declares its window (`body_draw_of`): its four keys, the window from 1, the seed and the increment from 0 and the multiplier from 1; on the world's draw alone the meeting's reading, `meeting`, `root` (the one draw through the root, the default where the key is absent and written nowhere) or `back` (the click that runs back, `meeting_back`), any other value refused by name, and beside `back` the run back's reach, `reach`, `board` (the whole board stepped back to the birth and forward to the close), `cone` (the record's light cone asserted about the same run, the engine's reading where the key is absent, written nowhere) or `books` (no run, the draws from the books alone), any other value refused by name and the key refused by name beside `root` or where `meeting` is absent (the run back's reach is a word of the back mode); every other key refused by name, a body's `meeting` and `reach` among them (`keyed` on `DRAW_KEYS`)."""
    found = keyed(value, label, WORLD_DRAW_KEYS if world else DRAW_KEYS, DRAW_KEYS)
    meeting, reach = found.get(MEETING, ROOT), found.get(REACH)
    if meeting not in MEETINGS:
        raise ValueError(f"{label}.{MEETING} is {meeting!r}: the draw's meeting is {ROOT!r} or {BACK!r}")
    if reach is not None and meeting != BACK:
        raise ValueError(
            f"{label}.{REACH} is declared with the meeting at {ROOT!r}: the run back's reach is a word of the "
            f"back mode, `{MEETING}: {BACK}`"
        )
    if reach is not None and reach not in REACHES:
        raise ValueError(
            f"{label}.{REACH} is {reach!r}: the run back's reach is {BOARD!r}, {CONE!r} or {BOOKS!r}"
        )
    return Draw(
        integer(found["seed"], f"{label}.seed", 0),
        integer(found["multiplier"], f"{label}.multiplier", 1),
        integer(found["increment"], f"{label}.increment", 0),
        integer(found["window"], f"{label}.window", 1),
        str(meeting),
        None if reach is None else str(reach),
    )


def meeting_of_the_law(
    draw: Draw | None,
    patterns: Sequence[Pattern],
    laid: Sequence[int],
    given: Sequence[int],
    families: tuple[FamilyRule, ...],
    weights: Sequence[tuple[int, ...]] = (),
) -> None:
    """The click that runs back needs a joint credit, a birth at one interval and parts laid alike (`weights`, the laid records' lines' weights in the order of `laid`, every laid line weighted alike, so every part: the partner's re-weighting lambda_k = e_k(port) at a_k = 1, ALGEBRA.md, The meeting's identity; a record of several parts whose parts carry different weights is refused by name until the credit carries a_k) (ALGEBRA.md, The click is the meeting of the future with the past: the backward run from the first click passes the root; the owner's word of 2026-10-19): where the world's draw declares `meeting: back`, two sides or more declare a pattern (`patterns`, the node_detectors' in the file's order) and a family of several parts is laid at the start (`laid`, the packets', the bodies' and the whole packets' families), refused by name otherwise (no joint credit: fewer than two sides reading the record, or a record of one part); no such family is given a quantum during the run by a rate, a conversion or a packet laid whole (`given`), refused by name: a record born during the run stands in one part, the act's lays writing the first part's lines, and its lay across the parts is a declaration the law has not made (the births' book and the lay across parts a later round's); the sides any count from two, each side drawing in the time's order on its conditional from the booked joint (`lists.readings`, N sides the general case, the owner's word of 2026-10-19; the antisymmetric record's two sides the credit's own refusal, `credit.joined`); nothing where the draw declares the root or the world none."""
    if draw is None or draw.meeting != BACK:
        return
    sides = sum(1 for pattern in patterns if pattern)
    if sides < 2 or not any(families[index].parts > 1 for index in laid):
        raise ValueError(
            f"draw.{MEETING} is {BACK!r} with {sides} side(s) declaring a pattern over the laid records of "
            f"{sorted({families[index].parts for index in laid})} part(s): the click that runs back needs a record "
            "of several parts read at two or more sides (ALGEBRA.md, The click is the meeting of the future with the past)"
        )
    if any(families[index].parts > 1 for index in given):
        raise ValueError(
            f"draw.{MEETING} is {BACK!r} and a record of several parts is given a quantum during the run (a rate, a "
            "conversion or a packet laid whole): a record born during the run stands in one part, the act's lays "
            "writing the first part's lines, and its lay across the parts is a declaration the law has not made; "
            "the births' book and the lay across parts a later round's"
        )
    for index, found in zip(laid, weights, strict=False):
        if families[index].parts > 1 and found and len(set(found)) > 1:
            raise ValueError(
                f"draw.{MEETING} is {BACK!r} and a record of {families[index].name!r} is laid with weights that "
                f"differ across its lines, {list(found)}: the click that runs back is built for parts laid alike "
                "(the partner's re-weighting lambda_k = e_k(port) at a_k = 1, ALGEBRA.md, The meeting's identity); "
                "weighted parts are a later round's, the credit carrying a_k"
            )


def body_draw_of(value: object, label: str) -> Generator:
    """A body's `node_detector` without a probe: the generator's three keys and, where the declaration carries it, its `window` (`Draw`, `draw_of`), else the generator alone (`Generator`, `generator_of`); the window of a body whose drives are laid with an end is derived at the end of the load from the lays' passage over it, where the key is refused by name, and declared, the instrument's cadence, where a drive is laid with no end or nowhere (`loader/window.windowed`, the atom branch, 2026-10-19)."""
    found = keyed(value, label, DRAW_KEYS, GENERATOR_KEYS)
    return draw_of(found, label) if "window" in found else generator_of(found, label)


def ports_of(basis: tuple[int, ...], pattern: Pattern) -> Ports:
    """A side's two ports from its declared setting (p, q) and its parts' pattern [[alpha_k, beta_k], ...]: e_k(+) = alpha_k p + beta_k q and e_k(-) = alpha_k (-q) + beta_k p, the - port the + port's with the setting turned a quarter (the pair's pattern [[1, 0], [0, 1]] gives (p, q) and (-q, p)); refused by name: a setting of other than two coefficients, no pattern, and two ports not orthogonal with equal norms, which is no setting of two outcomes."""
    if len(basis) != 2 or not pattern:
        raise ValueError(
            "a side declares its setting (p, q) as `basis` and one pair [alpha, beta] per part as "
            f"`pattern`, got {basis} and {list(pattern)}"
        )
    p, q = basis
    plus = tuple(alpha * p + beta * q for alpha, beta in pattern)
    minus = tuple(beta * p - alpha * q for alpha, beta in pattern)
    crossed = sum(u * v for u, v in zip(plus, minus, strict=True))
    if crossed or sum(u * u for u in plus) != sum(v * v for v in minus):
        raise ValueError(
            f"the pattern {list(pattern)} at the setting {basis} gives the ports {plus} and {minus}, "
            "not orthogonal with equal norms: no setting of two outcomes"
        )
    return plus, minus


def basis_of(value: object, label: str) -> tuple[int, ...]:
    """A node_detector's declared basis, its setting: a list of integers not all 0 (the pair's (p, q)); refused by name otherwise."""
    if not isinstance(value, list) or not value or not any(value):
        raise ValueError(f"{label} must be a list of integers, the setting's coefficients, not all 0")
    return tuple(integer(v, f"{label}[{i}]", -MAX_WORK_INT) for i, v in enumerate(value))


def pattern_of(value: object, label: str, basis: tuple[int, ...]) -> Pattern:
    """A node_detector's declared pattern: a list of integer pairs [alpha_k, beta_k], one per part of the record it reads, none [0, 0] (a part read with no coefficient at either port is no part of the read), on a setting of two coefficients (p, q); refused by name otherwise."""
    if len(basis) != 2:
        raise ValueError(
            f"{label} reads the setting (p, q) of two coefficients into the parts, and the basis has {len(basis)}"
        )
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must list one pair [alpha, beta] per part of the record it reads")
    found = []
    for index, entry in enumerate(value):
        if not isinstance(entry, list) or len(entry) != 2:
            raise ValueError(
                f"{label}[{index}] must be a pair [alpha, beta]: e(+) = alpha p + beta q, e(-) = alpha (-q) + beta p"
            )
        alpha = integer(entry[0], f"{label}[{index}][0]", -MAX_WORK_INT)
        beta = integer(entry[1], f"{label}[{index}][1]", -MAX_WORK_INT)
        if alpha == 0 and beta == 0:
            raise ValueError(
                f"{label}[{index}] is [0, 0]: a part read with no coefficient at either port is no part of the read"
            )
        found.append((alpha, beta))
    return tuple(found)


def patterns_of_the_law(
    patterns: list[tuple[str, Pattern]], laid: list[int], families: tuple[FamilyRule, ...]
) -> None:
    """A declared pattern reads one record of several parts, one pair per part: its length is the parts of a family of several parts the world lays (its packets' and its bodies' families, `laid`, by their indexes); refused by name where the lengths differ or the world lays no such record; and a laid family declaring the antisymmetric sign under exchange, where a side's pattern reads its parts, is read by two sides exactly, the determinant of two sides' parts (`credit.joined`, the family's declaration), another count of sides refused by name at load, generic for N sides otherwise (the owner's word of 2026-10-19); read at no side, the sign is the shell's and the lists' own (`lists.absorption`) and nothing is asked."""
    parts = sorted({families[index].parts for index in laid if families[index].parts > 1})
    for name, pattern in patterns:
        if pattern and len(pattern) not in parts:
            raise ValueError(
                f"node_detector {name!r} declares a pattern of {len(pattern)} parts, and the world lays "
                + (
                    f"records of {parts} parts, one pair per part"
                    if parts
                    else "no record of several parts"
                )
            )
    for index in sorted({index for index in laid if families[index].exchange < 0}):
        sides = sum(1 for _name, pattern in patterns if len(pattern) == families[index].parts)
        if sides and sides != 2:  # read at no side, the sign is the shell's and the lists' alone
            raise ValueError(
                f"{families[index].name!r} declares the antisymmetric sign under exchange and {sides} side(s) read "
                "its parts: the antisymmetric record's determinant is two sides', and another count of sides is a "
                "declaration the law has not made (ALGEBRA.md, Spin, closed for the paper as a route)"
            )


def setting_of(row: Mapping[str, object], label: str) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """A node_detector's setting from its row, (basis, axis), each () where the key is absent: `basis`, the setting's coefficients (p, q) for a record of real-line parts, or `axis`, the half-angle pair (c, s) of the detector's axis for a record of planes (the spin branch, 2026-10-19), one of the two; refused by name where both stand, and where a region declares a setting with no `pattern` to read it with (a setting is read by the pattern alone; a body's node_detector refuses a setting by its own line)."""
    basis = basis_of(row["basis"], f"{label}.basis") if "basis" in row else ()
    axis = basis_of(row["axis"], f"{label}.axis") if "axis" in row else ()
    if axis and basis:
        raise ValueError(
            f"{label} declares both `axis` and `basis`: a side's setting is one of the two, `basis` the setting's "
            "coefficients (p, q) for a record of real-line parts and `axis` the half-angle pair (c, s) for planes"
        )
    if (axis or basis) and "pattern" not in row and "block" not in row:
        raise ValueError(
            f"{label} declares a setting and no `pattern` to read it with: a setting is read by the pattern alone"
        )
    return basis, axis


def settings_of_the_law(
    sides: list[tuple[str, tuple[int, ...], tuple[int, ...], Pattern]],
    laid: list[int],
    families: tuple[FamilyRule, ...],
) -> None:
    """A side's setting is `basis` for a record of real-line parts, the setting's coefficients (p, q) at the full angle (the pair's and the GHZ's polarizations), and `axis` for a record of plane parts, the half-angle pair (c, s) of the detector's axis, the spinor read of a two-plane record (the spin branch, 2026-10-19; ALGEBRA.md, Spin, closed for the paper as a route: the half angle is the detector's declared basis and no property of the record under the 48): per side with a pattern, the laid families of as many parts as the pattern name the kind; refused by name where the side declares the other kind or where the laid records are of both kinds. The two ports' arithmetic is one (`ports_of`): e_k(+) = alpha_k c + beta_k s, e_k(-) = beta_k c - alpha_k s."""
    for name, axis, basis, pattern in sides:
        if not pattern:
            continue
        planes = {families[index].plane for index in laid if families[index].parts == len(pattern)}
        if len(planes) == 2:
            raise ValueError(
                f"node_detector {name!r} reads records of planes and of real lines with one pattern: a side's "
                "setting is one kind's, `axis` for planes and `basis` for real lines"
            )
        if planes == {True} and basis:
            raise ValueError(
                f"node_detector {name!r} declares `basis` for a record of planes, whose sides declare `axis`, the "
                "half-angle pair (c, s) of the detector's axis"
            )
        if planes == {False} and axis:
            raise ValueError(
                f"node_detector {name!r} declares `axis` for a record of real lines, whose sides declare `basis`, "
                "the setting's coefficients (p, q)"
            )
