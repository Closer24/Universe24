"""Matter's birth from light, the heaviest pair within the two quanta's own energy (ALGEBRA.md, Matter's birth from light; act.born_table, act.born_list, meeting_board.child_of): the chooser on the one universe file, exact in the integers, over every point of den's circle since the file carries no row (2026-10-24; the fit vacuous at two whole quanta, so the two quanta at the top birth the point nearest the top, the builder's finding of #2187; the selection sentence the builder's sense runs decide): W_c = 3 den T, each point's walls 2 x 3 T s, the heaviest whose walls fit."""

import json

from event_universe.act import born_table
from event_universe.loader.derived import count_wall
from event_universe.loader.universe import MASSLESS, universe_of
from tests.laws import ROOT

UNIVERSE = ROOT / "examples" / "events" / "universe24" / "universe_universe24.json"
SHARE_AT_29 = 2_019_227  # every Node's share of light at the uniform sea's first meeting in millionths of W_c, 2.019227 W_c: 254,493,485,120,013,736,379,770,556 at the top tier's den, the massless levels alike at every den (11,681,869,594,679 at den 53,567,765 to 2026-10-24)


def test_the_heaviest_pair_within_the_two_quanta_on_natures_den() -> None:
    """On nature's den (the PeV tier 21,397,363,965,165,989,151,899,244,775,347,635,252,768,274,397 since 2026-10-24, the owner's word, the den chosen after the clicks; T 36,000): W_c = 3 den T; the electron's point, the least leg, the heaviest prime's lift at this den, and the proton's, point 2 0 0, the lightest prime's lift, among the 26 points; two quanta at the top birth the heaviest point of all (the fit vacuous), at a point's walls exactly that point, one unit below them the next lighter point, below the lightest point's walls nothing; one quantum and the rest, the heaviest point whose two walls fit, point 2 2 2 at this den."""
    integers, families = universe_of(json.loads(UNIVERSE.read_text(encoding="utf-8")))
    action, names = integers["quantum_action"], [family.name for family in families]
    light = names.index(MASSLESS)
    den = families[light].pair[1]
    planes = sorted(
        (k for k, f in enumerate(families) if f.plane), key=lambda k: count_wall(families[k], action)
    )
    electron, proton = (
        planes[0],
        names.index("point 2 0 0"),
    )  # the least leg and the proton's point, the lightest prime's lift (s_p / s_e = 1836.15265582)
    wall_c, wall_p, wall_e = (count_wall(families[k], action) for k in (light, proton, electron))
    assert (
        (wall_c, wall_p, wall_e)
        == (
            3 * den * action,
            3 * action * 14_337_524_090_452_503_379_101_009_450_350_924_059_372,
            3 * action * 7_808_459_740_549_578_735_922_594_780_248_829_328,
        )
    )  # the legs at the PeV den (1,162,656,062,845,119,254,100 and 633,202,287,062,780,012 at the top tier)
    assert names[electron] == "point 0 0 2" and 1_492_403 * wall_p <= wall_c < 1_492_404 * wall_p
    pair = lambda k: ((k, -1), (k, 1))  # noqa: E731
    heaviest = lambda energy, over=1: born_table(families, light, action, energy, over)  # noqa: E731
    top = planes[-1]
    assert (
        heaviest(2 * wall_c) == pair(top) and top != proton
    )  # two quanta at the top: the point nearest the top, not the proton
    assert heaviest(2 * wall_p) == pair(proton)  # at the proton's walls exactly, that point
    below = planes[planes.index(proton) - 1]
    assert (
        heaviest(2 * wall_p - 1) == pair(below) and count_wall(families[below], action) < wall_p
    )  # one unit below: the next lighter point
    assert heaviest(2 * wall_e) == pair(electron)  # at the lightest point's walls exactly
    assert heaviest(2 * wall_e - 1) is None  # below the lightest pair's walls nothing is born
    assert heaviest(2 * (3 * wall_p), 3) == pair(
        proton
    )  # three quanta at the proton's walls at the Node: two of them carry it
    share = SHARE_AT_29 * wall_c // 1_000_000  # 2.019227 W_c in this den's unit
    assert heaviest(2 * share, 2) == pair(top)  # the uniform sea's first meeting: every point fits
    assert heaviest(2 * (share - wall_c), 2) == pair(
        names.index("point 2 2 2")
    )  # one quantum and the rest
