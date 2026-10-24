"""Matter's birth from light, the heaviest pair within the two quanta's own energy (ALGEBRA.md, Matter's birth from light; act.born_table, act.born_list, meeting_board.child_of): the chooser at the top tier's den as a literal, the sentence the law's at every den (the PeV den's own numbers stand in tests/test_the_loader.py::test_dens_circle_is_read_from_its_integers_alone, the one test that factors it, 2026-10-24), exact in the integers, over every point of den's circle since the file carries no row (2026-10-24; the fit vacuous at two whole quanta, so the two quanta at the top birth the point nearest the top, the builder's finding of #2187; the selection sentence the builder's sense runs decide): W_c = 3 den T, each point's walls 2 x 3 T s, the heaviest whose walls fit."""

from event_universe.act import born_table
from event_universe.loader.derived import count_wall
from event_universe.loader.universe import MASSLESS, universe_of

TOP = 1_166_991_900_949_580_266_237  # the constants hand's three-prime den, 649,421 x 13,586,597 x 132,260,701
LEGS = (
    1_162_656_062_845_119_254_100,
    633_202_287_062_780_012,
)  # the proton's point's leg and the least leg at the top tier, s_p / s_e = 1836.15265864


def test_the_heaviest_pair_within_the_two_quanta_at_the_top_tiers_den() -> None:
    """At the top tier's den (T 36,000): W_c = 3 den T; the least leg's point "point 0 2 0" and the proton's "point 0 0 2" (the lightest prime's lift) carry the walls 3 T s; the chooser `born_table` births the point nearest the top at two quanta of light, the proton's point at its two walls exactly and the next lighter one unit below, the lightest at its walls exactly and nothing below them, and the proton at three quanta of its walls; at the sea's meeting, two whole quanta of light at the Node (`meeting_board.child_of`), every point fits and the top is born; no course number of a record (the former pin of the meeting's share struck 2026-10-24)."""
    integers, families = universe_of(
        {"integers": {"den": TOP, "node_clock": 1000, "quantum_action": 36_000}}
    )
    action, names = integers["quantum_action"], [family.name for family in families]
    light = names.index(MASSLESS)
    den = families[light].pair[1]
    planes = sorted(
        (k for k, f in enumerate(families) if f.plane), key=lambda k: count_wall(families[k], action)
    )
    electron, proton = planes[0], names.index("point 0 0 2")
    wall_c, wall_p, wall_e = (count_wall(families[k], action) for k in (light, proton, electron))
    assert (wall_c, wall_p, wall_e) == (3 * den * action, 3 * action * LEGS[0], 3 * action * LEGS[1])
    assert names[electron] == "point 0 2 0" and len(planes) == 3**3 - 1
    pair = lambda k: ((k, -1), (k, 1))  # noqa: E731
    heaviest = lambda energy, over=1: born_table(families, light, action, energy, over)  # noqa: E731
    top = planes[-1]
    assert heaviest(2 * wall_c) == pair(top) and top != proton  # two quanta: the point nearest the top
    assert heaviest(2 * wall_p) == pair(proton)  # at the proton's walls exactly, that point
    below = planes[planes.index(proton) - 1]
    assert heaviest(2 * wall_p - 1) == pair(below) and count_wall(families[below], action) < wall_p
    assert heaviest(2 * wall_e) == pair(electron)  # at the lightest point's walls exactly
    assert heaviest(2 * wall_e - 1) is None  # below the lightest pair's walls nothing is born
    assert heaviest(2 * (3 * wall_p), 3) == pair(proton)  # three quanta at the proton's walls
    assert heaviest(2 * (2 * wall_c), 2) == pair(top)  # the sea's meeting: two whole quanta, the top
