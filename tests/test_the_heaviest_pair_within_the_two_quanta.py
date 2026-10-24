"""Matter's birth from light, the former clause by name, the heaviest pair within the two quanta's own energy (ALGEBRA.md, Matter's birth from light; act.born_table, the law from 2026-10-24, 05:2x UTC, to the selector's build of 13:xx UTC), and the selector's affordable lists (act.affordable, meeting_board.child_of): the chooser on the one universe file, exact in the integers, over the lifts of den's primes alone since the selector (over every point of the circle before it, where the fit vacuous at two whole quanta birthed the point nearest the top, the builder's finding of #2187): W_c = 3 den T, each lift's walls 2 x 3 T s, the heaviest whose walls fit, and every one whose walls fit."""

import json

from event_universe.act import affordable, born_table
from event_universe.loader.derived import count_wall
from event_universe.loader.universe import MASSLESS, universe_of
from tests.laws import ROOT

UNIVERSE = ROOT / "examples" / "events" / "universe24" / "universe_universe24.json"
SHARE_AT_29 = 2_019_227  # every Node's share of light at the uniform sea's first meeting in millionths of W_c, 2.019227 W_c: 254,493,485,120,013,736,379,770,556 at the top tier's den, the massless levels alike at every den (11,681,869,594,679 at den 53,567,765 to 2026-10-24)


def test_the_heaviest_pair_within_the_two_quanta_on_natures_den() -> None:
    """On nature's den (the PeV tier 21,397,363,965,165,989,151,899,244,775,347,635,252,768,274,397 since 2026-10-24, the owner's word, the den chosen after the clicks; T 36,000): W_c = 3 den T; the electron's lift, the least leg, point 0 0 2, the proton's, point 2 0 0, and the neutron's, point 0 2 0, the heaviest lift, among the 26 points; under the former clause two quanta at the top birth the heaviest LIFT, the neutron's (the point nearest the top, a swap at rung 2, is no candidate since the selector, 2026-10-24, 13:xx UTC), at a lift's walls exactly that lift, one unit below the proton's walls the electron's (the next lighter lift), below the lightest lift's walls nothing; at the uniform sea's first meeting, 2.019227 W_c, and at one quantum and the rest every lift fits (the rungs below 1.4 x 10^-6 at this den) and the former clause names the neutron's where it named the top and point 2 2 2; the affordable lists there the three lifts, lightest first, the pick the Node's draw (meeting_board.drawn_among)."""
    integers, families = universe_of(json.loads(UNIVERSE.read_text(encoding="utf-8")))
    action, names = integers["quantum_action"], [family.name for family in families]
    light = names.index(MASSLESS)
    den = families[light].pair[1]
    planes = sorted(
        (k for k, f in enumerate(families) if f.plane), key=lambda k: count_wall(families[k], action)
    )
    electron, proton, neutron = (
        planes[0],
        names.index("point 2 0 0"),
        names.index("point 0 2 0"),
    )  # the least leg; the proton's point, the lightest prime's lift (s_p / s_e = 1836.15265582); the heaviest lift
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
    assert (
        heaviest(2 * wall_c) == pair(neutron) != pair(planes[-1])
    )  # two quanta at the top: the heaviest lift
    assert heaviest(2 * wall_p) == pair(proton)  # at the proton's walls exactly, that lift
    assert (
        heaviest(2 * wall_p - 1) == pair(electron) and count_wall(families[electron], action) < wall_p
    )  # one unit below: the next lighter lift (the next lighter point, composed, before the selector)
    assert heaviest(2 * wall_e) == pair(electron)  # at the lightest point's walls exactly
    assert heaviest(2 * wall_e - 1) is None  # below the lightest pair's walls nothing is born
    assert heaviest(2 * (3 * wall_p), 3) == pair(
        proton
    )  # three quanta at the proton's walls at the Node: two of them carry it
    share = SHARE_AT_29 * wall_c // 1_000_000  # 2.019227 W_c in this den's unit
    assert heaviest(2 * share, 2) == pair(neutron)  # the uniform sea's first meeting: every lift fits
    assert (
        heaviest(2 * (share - wall_c), 2) == pair(neutron)
    )  # one quantum and the rest: every lift fits (point 2 2 2, the heaviest composed point fitting, before the selector)
    assert affordable(families, light, action, 2 * share, 2) == (
        pair(electron),
        pair(proton),
        pair(neutron),
    )  # the selector's candidates there, lightest first
