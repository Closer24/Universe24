"""Matter's birth from light, the heaviest pair within the two quanta's own energy (ALGEBRA.md, Matter's birth from light; act.born_table, act.born_list, meeting_board.child_of): the chooser on the one universe file, exact in the integers; the board's births stand in tests/test_universe24_runs_its_cycle.py."""

import json

from event_universe.act import born_table
from event_universe.loader.derived import count_wall
from event_universe.loader.universe import universe_of
from tests.laws import ROOT

UNIVERSE = ROOT / "examples" / "events" / "universe24" / "universe_universe24.json"
SHARE_AT_29 = 254_493_485_120_013_736_379_770_556  # every Node's share of light at the folded course's first meeting at the enlarged den, 2.019227 W_c (11,681,869,594,679 at den 53,567,765 to 2026-10-24, the same 2.019227 W_c)


def families_of(document: dict) -> tuple:  # type: ignore[type-arg]
    integers, families = universe_of(document)
    return families, [family.name for family in families], integers["quantum_action"]


def test_the_heaviest_pair_within_the_two_quanta_on_natures_den() -> None:
    """On nature's den (the enlarged den 1,166,991,900,949,580,266,237 since 2026-10-24, 53,567,765 to that day, T 36,000): W_c = 3 den T; the proton pair's walls 2 x 3 T s_p are 483 / 485 of two quanta at the top at either den (s_p / den 0.99629 and 0.99588) and the electron pair's 2 x 3 T s_e; two quanta at the top birth the proton pair, two quanta one unit below the proton's walls the electron pair, two quanta below the electron's walls nothing; the fraction two n-ths of a share where n stand read cross-multiplied; the folded course's share at 29 births the proton pair. The former clause (2026-10-23 to 2026-10-24, the lightest within 2 x 3 den T): the electron pair at every one of these energies, the threshold a tautology."""
    families, names, action = families_of(json.loads(UNIVERSE.read_text(encoding="utf-8")))
    light, proton, electron = names.index("light"), names.index("proton"), names.index("electron")
    den = families[light].pair[1]
    wall_c, wall_p, wall_e = (count_wall(families[k], action) for k in (light, proton, electron))
    assert (wall_c, wall_p, wall_e) == (
        3 * den * action,
        3 * action * 1_162_656_062_845_119_254_100,
        3 * action * 633_202_287_062_780_012,
    )  # the legs at the enlarged den (53,346,867 and 29,276 at den 53,567,765 to 2026-10-24)
    assert 2 * wall_p * 485 < 2 * wall_c * 483 + 2 * wall_c  # 483 / 485 of the top, within one 485th
    proton_pair, electron_pair = ((proton, -1), (proton, 1)), ((electron, -1), (electron, 1))
    heaviest = lambda energy, over=1: born_table(families, light, action, energy, over)  # noqa: E731
    assert (
        heaviest(2 * wall_c) == proton_pair
    )  # two quanta at the top: the proton pair (the former clause: the electron pair)
    assert heaviest(2 * wall_p) == proton_pair  # at the proton pair's walls exactly
    assert heaviest(2 * wall_p - 1) == electron_pair  # one unit below them: the electron pair
    assert heaviest(2 * wall_e) == electron_pair  # at the electron pair's walls exactly
    assert (
        heaviest(2 * wall_e - 1) is None
    )  # below the lightest pair's walls nothing is born (the former clause: the electron pair)
    assert (
        heaviest(2 * (3 * wall_c), 3) == proton_pair
    )  # three quanta at the top at the Node: two of them carry the proton
    assert (
        heaviest(2 * (3 * wall_p - 1), 3) == electron_pair
    )  # three quanta a third of a unit below it: the electron
    assert (
        heaviest(2 * SHARE_AT_29, 2) == proton_pair
    )  # the folded course at 29: 2.019227 W_c against 1.99175 W_c
    assert (
        heaviest(2 * (SHARE_AT_29 - 2 * wall_c + wall_c), 2) == electron_pair
    )  # one quantum and the rest at 28
