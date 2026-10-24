"""Matter's birth from light, the heaviest pair within the two quanta's own energy (ALGEBRA.md, Matter's birth from light; act.born_table, act.born_list, meeting_board.child_of): the chooser on the one universe file, exact in the integers, over every point of den's circle since the file carries no row (2026-10-24; the fit vacuous at two whole quanta, so the two quanta at the top birth the point nearest the top, the builder's finding of #2187; the selection sentence the builder's sense runs decide): W_c = 3 den T, each point's walls 2 x 3 T s, the heaviest whose walls fit."""

import json

from event_universe.act import born_table
from event_universe.loader.derived import count_wall
from event_universe.loader.universe import MASSLESS, universe_of
from tests.laws import ROOT

UNIVERSE = ROOT / "examples" / "events" / "universe24" / "universe_universe24.json"
SHARE_AT_29 = 254_493_485_120_013_736_379_770_556  # every Node's share of light at the folded course's first meeting at the enlarged den, 2.019227 W_c (11,681,869,594,679 at den 53,567,765 to 2026-10-24)


def test_the_heaviest_pair_within_the_two_quanta_on_natures_den() -> None:
    """On nature's den (the enlarged den 1,166,991,900,949,580,266,237, T 36,000): W_c = 3 den T; the former electron's point, the least leg, and the former proton's, the heaviest prime's lift, among the 26 points; two quanta at the top birth the heaviest point of all (the fit vacuous), at a point's walls exactly that point, one unit below them the next lighter point, below the lightest point's walls nothing."""
    integers, families = universe_of(json.loads(UNIVERSE.read_text(encoding="utf-8")))
    action, names = integers["quantum_action"], [family.name for family in families]
    light = names.index(MASSLESS)
    den = families[light].pair[1]
    planes = sorted(
        (k for k, f in enumerate(families) if f.plane), key=lambda k: count_wall(families[k], action)
    )
    electron, proton = (
        planes[0],
        names.index("point 0 0 2"),
    )  # the least leg and the heaviest prime's point
    wall_c, wall_p, wall_e = (count_wall(families[k], action) for k in (light, proton, electron))
    assert (wall_c, wall_p, wall_e) == (
        3 * den * action,
        3 * action * 1_162_656_062_845_119_254_100,
        3 * action * 633_202_287_062_780_012,
    )  # the legs at the enlarged den (53,346,867 and 29,276 at den 53,567,765 to 2026-10-24)
    assert (
        2 * wall_p * 485 < 2 * wall_c * 483 + 2 * wall_c
    )  # the former proton's walls 483 / 485 of the top
    pair = lambda k: ((k, -1), (k, 1))  # noqa: E731
    heaviest = lambda energy, over=1: born_table(families, light, action, energy, over)  # noqa: E731
    top = planes[-1]
    assert (
        heaviest(2 * wall_c) == pair(top) and top != proton
    )  # two quanta at the top: the point nearest the top, not the former proton
    assert heaviest(2 * wall_p) == pair(proton)  # at the former proton's walls exactly, that point
    below = planes[planes.index(proton) - 1]
    assert (
        heaviest(2 * wall_p - 1) == pair(below) and count_wall(families[below], action) < wall_p
    )  # one unit below: the next lighter point
    assert heaviest(2 * wall_e) == pair(electron)  # at the lightest point's walls exactly
    assert heaviest(2 * wall_e - 1) is None  # below the lightest pair's walls nothing is born
    assert heaviest(2 * (3 * wall_p), 3) == pair(
        proton
    )  # three quanta at the former proton's walls at the Node: two of them carry it
    assert heaviest(2 * SHARE_AT_29, 2) == pair(
        top
    )  # the folded course at 29: 2.019227 W_c, every point fits
