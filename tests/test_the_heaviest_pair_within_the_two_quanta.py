"""Matter's birth from light, the heaviest list within the two quanta's own energy (ALGEBRA.md, Matter's birth from light; act.born_table, act.born_list, meeting_board.child_of; N children one record each, 2026-10-24): the chooser on the one universe file, exact in the integers; the board's births stand in tests/test_universe24_runs_its_cycle.py."""

import json

from event_universe.act import born_table
from event_universe.loader.derived import count_wall
from event_universe.loader.universe import universe_of
from tests.laws import ROOT

UNIVERSE = ROOT / "examples" / "events" / "universe24" / "universe_universe24.json"
SHARE_AT_29 = (
    11_681_869_594_679  # every Node's share of light at the folded course's first meeting, 2.019227 W_c
)


def families_of(document: dict) -> tuple:  # type: ignore[type-arg]
    integers, families = universe_of(document)
    return families, [family.name for family in families], integers["quantum_action"]


def test_the_heaviest_list_within_the_two_quanta_on_natures_den() -> None:
    """On nature's den (den 53,567,765, T 36,000): W_c = 3 den T; the proton pair's walls 2 x 3 T x 53,346,867 are 483 / 485 of two quanta at the top and the electron pair's 2 x 3 T x 29,276; the lists of at most 2 + BEYOND children, their summed walls the energy they need (N children one record each, 2026-10-24): two quanta at the top birth the proton pair with the electron pair (2 u_p + 2 u_e within 2 W_c), the proton pair alone at exactly its own walls, four electrons one unit below them, four protons at twice them, the electron pair at exactly its walls and nothing below them."""
    families, names, action = families_of(json.loads(UNIVERSE.read_text(encoding="utf-8")))
    light, proton, electron = names.index("light"), names.index("proton"), names.index("electron")
    den = families[light].pair[1]
    wall_c, wall_p, wall_e = (count_wall(families[k], action) for k in (light, proton, electron))
    assert (wall_c, wall_p, wall_e) == (3 * den * action, 3 * action * 53_346_867, 3 * action * 29_276)
    assert 2 * wall_p * 485 < 2 * wall_c * 483 + 2 * wall_c  # 483 / 485 of the top, within one 485th
    p, e = ((proton, -1), (proton, 1)), ((electron, -1), (electron, 1))
    pp, ee, ppee, eeee, pppp = (
        p,
        e,
        p + e,
        ((electron, -1), (electron, -1), (electron, 1), (electron, 1)),
        ((proton, -1), (proton, -1), (proton, 1), (proton, 1)),
    )
    heaviest = lambda energy, over=1: born_table(families, light, action, energy, over)  # noqa: E731
    assert heaviest(2 * wall_c) == ppee  # two quanta at the top: the proton pair with the electron pair
    assert heaviest(2 * wall_p) == pp  # at the proton pair's walls exactly: the proton pair alone
    assert heaviest(2 * wall_p - 1) == eeee  # one unit below them: four electrons
    assert heaviest(4 * wall_p) == pppp  # at twice the proton pair's walls: four protons
    assert (
        heaviest(4 * wall_e) == eeee and heaviest(2 * wall_e) == ee
    )  # the electron lists at their walls
    assert heaviest(2 * wall_e - 1) is None  # below the lightest list's walls nothing is born
    assert (
        heaviest(2 * (3 * wall_c), 3) == ppee
    )  # three quanta at the top at the Node: two of them carry the list
    assert heaviest(2 * (3 * wall_p - 1), 3) == eeee  # three quanta a third of a unit below it
    assert (
        heaviest(2 * SHARE_AT_29, 2) == ppee
    )  # the folded course at 29: 2.019227 W_c against 1.99285 W_c
    assert heaviest(2 * (SHARE_AT_29 - 2 * wall_c + wall_c), 2) == eeee  # one quantum and the rest at 28
