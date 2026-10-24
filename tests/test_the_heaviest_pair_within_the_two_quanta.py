"""Matter's birth from light, the former clause by name, the heaviest pair within the two quanta's own energy (ALGEBRA.md, Matter's birth from light; act.born_table, the law from 2026-10-24, 05:2x UTC, to the selector's build of 13:xx UTC, kept for act.born_list), and the selector's affordable lists (act.affordable, meeting_board.child_of): the chooser at the top tier's den as a literal, exact in the integers, over the lifts of den's primes alone since the selector (over every point of the circle before it, where the fit vacuous at two whole quanta birthed the point nearest the top): W_c = 3 den T, each lift's walls 2 x 3 T s, the heaviest whose walls fit, and every one whose walls fit."""

from event_universe.act import affordable, born_table
from event_universe.loader.derived import count_wall
from event_universe.loader.universe import MASSLESS, universe_of

TOP = 1_166_991_900_949_580_266_237  # the constants hand's three-prime den, 649,421 x 13,586,597 x 132,260,701
LEGS = (
    1_162_656_062_845_119_254_100,
    633_202_287_062_780_012,
)  # the proton's point's leg and the least leg at the top tier, s_p / s_e = 1836.15265864


def test_the_heaviest_pair_within_the_two_quanta_at_the_top_tiers_den() -> None:
    """At the top tier's den (T 36,000): W_c = 3 den T; the least leg's point "point 0 2 0" (the electron's lift), the proton's "point 0 0 2" (the lightest prime's lift) and the neutron's "point 2 0 0" (the heaviest lift, 1.99532 W_c) carry the walls 3 T s; under the former clause two quanta at the top birth the heaviest LIFT, the neutron's, and not the point nearest the top (a swap at rung 2, no candidate since the selector, 2026-10-24, 13:xx UTC), at a lift's walls exactly that lift, one unit below the proton's walls the electron's (the next lighter lift; the next lighter point, composed, before the selector), below the lightest lift's walls nothing; at the sea's meeting of two whole quanta the neutron's lift (the top before), at one quantum and the rest 1.019 W_c the electron's alone; the affordable lists there the three lifts and the one lift, lightest first, the pick the Node's draw from the quotient (meeting_board.drawn_among)."""
    integers, families = universe_of(
        {"integers": {"den": TOP, "node_clock": 1000, "quantum_action": 36_000}}
    )
    action, names = integers["quantum_action"], [family.name for family in families]
    light = names.index(MASSLESS)
    den = families[light].pair[1]
    planes = sorted(
        (k for k, f in enumerate(families) if f.plane), key=lambda k: count_wall(families[k], action)
    )
    electron, proton, neutron = planes[0], names.index("point 0 0 2"), names.index("point 2 0 0")
    wall_c, wall_p, wall_e = (count_wall(families[k], action) for k in (light, proton, electron))
    assert (wall_c, wall_p, wall_e) == (3 * den * action, 3 * action * LEGS[0], 3 * action * LEGS[1])
    assert names[electron] == "point 0 2 0" and len(planes) == 3**3 - 1
    pair = lambda k: ((k, -1), (k, 1))  # noqa: E731
    heaviest = lambda energy, over=1: born_table(families, light, action, energy, over)  # noqa: E731
    assert heaviest(2 * wall_c) == pair(neutron) != pair(planes[-1])  # two quanta: the heaviest lift
    assert heaviest(2 * wall_p) == pair(proton)  # at the proton's walls exactly, that lift
    assert (
        heaviest(2 * wall_p - 1) == pair(electron) and count_wall(families[electron], action) < wall_p
    )  # one unit below: the next lighter lift
    assert heaviest(2 * wall_e) == pair(electron)  # at the lightest point's walls exactly
    assert heaviest(2 * wall_e - 1) is None  # below the lightest pair's walls nothing is born
    assert heaviest(2 * (3 * wall_p), 3) == pair(proton)  # three quanta at the proton's walls
    assert heaviest(2 * (2 * wall_c), 2) == pair(neutron)  # the sea's meeting, two whole quanta
    assert heaviest(2 * (wall_c + wall_c // 1_000), 2) == pair(
        electron
    )  # one quantum and a rest below the proton's rung: the electron's lift alone
    assert affordable(families, light, action, 2 * (2 * wall_c), 2) == (
        pair(electron),
        pair(proton),
        pair(neutron),
    )  # the selector's candidates at two quanta, lightest first
    assert affordable(families, light, action, 2 * (wall_c + wall_c // 1_000), 2) == (pair(electron),)
