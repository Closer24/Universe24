"""The draw's declaration (ALGEBRA.md, The NodeDetector is one declaration kind for every world; #the-click-is-the-meeting, the pair's form and the GHZ gate; The click's read of the board): on the world the `draw`, the window in intervals after which the NodeDetectors over regions draw and write their click derived at the end of the load from the regions' passages and declared by no key (`Draw`, `draw_of`, `loader/window.drawn`; the owner's decision of 2026-10-23; the draw itself the click's read of the board, `digits.read_of`, so no seed and no generator: `seed`, `multiplier` and `increment` are unknown keys, refused by name as every unknown key is), and the run back's reach (`reach`, `cone` or `board`; ALGEBRA.md, The meeting's reading, the run back's reach; the owner's words of 2026-10-19 and 2026-10-20): there is one meeting, the click that writes at the record's birth, the sides reading in the order of their closes (`meeting_back`, `lists.readings`), so the key `meeting` is refused by name (2026-10-20); a body with a probe among its transitions (a transition of a part into itself) declares its `node_detector` with no key (`windowless_of`, a `Draw` with no window), its window bounded by the probe's lays at its Node (ALGEBRA.md, The pulsed gate), and no body's `node_detector` admits the meeting, the world's draw's word; and on a node_detector's region its setting `basis` (p, q), the coefficients of its credit, and its parts' `pattern`, one integer pair [alpha_k, beta_k] per part of the record it reads, the + port reading the part k as e_k(+) = alpha_k p + beta_k q and the - port as e_k(-) = alpha_k (-q) + beta_k p (the pair's pattern [[1, 0], [0, 1]], the ports (p, q) and (-q, p); `ports_of`, the two ports exactly orthogonal with equal norms, refused by name otherwise), read by the reader (`tools/bell_gate.py`) and by the sides' draws in the run (`meeting_back.coefficients_of`); every defect refused by name and no default written."""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.loader.keys import keyed

Gauss = tuple[
    int, int
]  # a Gaussian integer (re, im), a part's coefficient: an integer where im is 0, a quarter turn's unit on a plane's second component (the two-term plane GHZ, 2026-10-20)
WINDOW = "window"  # the former key: admitted at the parse to be refused by name at the end of the load with the derived number
DRAW_KEYS = (
    WINDOW,
)  # the draw declares no number: the window is derived (the owner's decision of 2026-10-23), the key read for its refusal alone
# the digits' order of the click's read of the board, the one declared constant of the read (`digits.read_of`):
# the lines outer in the record's declared order (part 0's lines, then part 1's; a plane's two lines in their
# order; the records of a family in their order), the Nodes read inner in the lattice's index order (x-major,
# numpy's order of a mask), the first digit the most significant, each digit the remainder's index on its
# Node's lattice; the realisation depends on this order and the measure does not
DIGIT_ORDER = "the lines in the record's declared order, each line's Nodes in the lattice's index order, the first digit the most significant, each digit the remainder's index on its Node's lattice, r div F, in the base w div F + 1"  # the draw with its window: the world's and a body's without a probe


@dataclass(frozen=True)
class Draw:
    """A draw as the files declare it, the click's read of the board with its window (features/click, `digits.read_of`): the world's window, the intervals after which every node_detector's window closes and the NodeDetector draws and writes; a body's without a probe (derived from the lays' passage over the body, or from its own beat where a drive's lay has no end, `loader/window.py`; the owner's decision of 2026-10-23: the window shall not be declared); None where the window is bounded by a probe's lays at the body's Node, the world's schedule and no number of the body's (`windowless_of`; ALGEBRA.md, The pulsed gate); and the run back's reach of the world's draw alone, `cone` or `board` (`REACHES`, `meeting_back`), None where the file declares none, which the engine reads as the record's light cone (`credit.Books.reach`), written nowhere; no seed, no multiplier and no increment: the draw carries no number of the run outside the world file and Rule3."""

    window: int | None


def windowless_of(value: object, label: str) -> Draw:
    """A body's `node_detector`, an object with no key: the body with a probe among its transitions, whose window is bounded by the probe's lays at its Node, the world's schedule and no number of the body's (ALGEBRA.md, The pulsed gate), and every other body, whose window is derived at the end of the load, the passage of its drives' lays with an end over it or, where a lay has no end or none is laid, its own beat (`loader/window.windowed`; the owner's decision of 2026-10-23); the key `window` refused by name with the rule (`body_draw_of`), every other key refused by name as unknown (`keyed`), the draw being the click's read of the board and no number of the file's."""
    keyed(value, label, (), ())
    return Draw(None)


def body_draw_of(value: object, label: str) -> Draw:
    """A body's `node_detector`: no key at all, the window derived at the end of the load from the lays' passage over the body, or from its own beat where a drive is laid with no end or nowhere (`loader/window.windowed`); the key `window` refused by name with the rule."""
    return Draw(keyed(value, label, DRAW_KEYS, ()).get(WINDOW))


def times(a: Gauss, b: Gauss) -> Gauss:
    """The product of two Gaussian integers, (a_re b_re - a_im b_im, a_re b_im + a_im b_re), exact; the integers' product where both im are 0 (ALGEBRA.md, The click is the meeting of the future with the past, the Gaussian clause of 2026-10-20)."""
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def norm(a: Gauss) -> int:
    """The norm of a Gaussian integer, re^2 + im^2, the square where im is 0: the coefficient's weight in the record's scale."""
    return a[0] * a[0] + a[1] * a[1]
