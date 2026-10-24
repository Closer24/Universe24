"""Matter's birth from light, the former clause by name, the heaviest pair within the two quanta's own energy (ALGEBRA.md, Matter's birth from light; act.born_table, the law from 2026-10-24, 05:2x UTC, to the selector's build of 13:xx UTC), and the selector's affordable lists (act.affordable, meeting_board.child_of): the chooser on the one universe file, exact in the integers, over the lifts of den's primes alone since the selector (over every point of the circle before it, where the fit vacuous at two whole quanta birthed the point nearest the top, the builder's finding of #2187): W_c = 3 den T, each lift's walls 2 x 3 T s, the heaviest whose walls fit, and every one whose walls fit."""

import json

from event_universe.act import affordable, born_table
from event_universe.loader.derived import count_wall
from event_universe.loader.universe import MASSLESS, universe_of
from tests.laws import ROOT

UNIVERSE = ROOT / "examples" / "events" / "universe24" / "universe_universe24.json"
SHARE_AT_29 = 254_493_485_120_013_736_379_770_556  # every Node's share of light at the folded course's first meeting at the enlarged den, 2.019227 W_c (11,681,869,594,679 at den 53,567,765 to 2026-10-24)


def test_the_heaviest_pair_within_the_two_quanta_on_natures_den() -> None:
    """On nature's den (the enlarged den 1,166,991,900,949,580,266,237, T 36,000): W_c = 3 den T; the electron's lift, the least leg, the proton's, the heaviest prime's, and the neutron's, the heaviest lift, among the 26 points; under the former clause two quanta at the top birth the heaviest LIFT, the neutron's (the electron's swap at the top, the point nearest the top, is no candidate since the selector, 2026-10-24, 13:xx UTC), at a lift's walls exactly that lift, one unit below the proton's walls the electron's (the next lighter lift), below the lightest lift's walls nothing; the affordable lists at 2.019227 W_c the three lifts, lightest first."""
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
    neutron = names.index(
        "point 2 0 0"
    )  # the heaviest lift, 1.99532 W_c; the top point planes[-1] is no list
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
    assert heaviest(2 * SHARE_AT_29, 2) == pair(
        neutron
    )  # the folded course at 29: 2.019227 W_c, every lift fits
    assert (
        affordable(families, light, action, 2 * SHARE_AT_29, 2)
        == (
            pair(electron),
            pair(proton),
            pair(neutron),
        )
    )  # the selector's candidates there, lightest first; the pick the Node's draw (meeting_board.drawn_among)
