"""The charge written is the Wronskian over T div 2 for every reader (ALGEBRA.md, The constants, the law's sentence of 2026-10-24 on the owner's word of that morning, the charge universal like nature; the former clause of the same day, each reader's Wronskian times 3 T den over its own count unit, kept by name as the defect: the electron's factor 1,822 times the proton's on the one universe file, one born electron written as 1,822 proton charges, the sign holder's row running away; the old "one ratio per holder, E_h T num / (Gamma den)" of 2026-10-23 kept by name too): the holder of the sign carries one alpha = E_h T / Gamma with any pairs under it (`loader/derived.alpha_of`), and each reader's Wronskian enters the holder's one write at the factor 1 over the one wall 2 E_s T Gamma (`loader/derived.held_write_of`, `loader/charge.charge_factors`), so that a quantum of every plane family, W = T div 2 at the birth's quarter-turn lay, writes the same charge; the register's scale and the lay's amplitude bound stay the loader's tool, a holder of the sign changing no neutral body's register."""

from __future__ import annotations

from dataclasses import replace

from event_universe.features.click import amplitude
from event_universe.loader.derived import amplitude_bound, count_wall, held_write_of
from event_universe.loader.universe import universe_of

GAMMA, T = 1000, 36_000
DEN = 53_567_765
SIGN = {"name": "charge", "pair": [GAMMA, GAMMA]}  # the holder of the sign, the held massless row


def universe(proton: list[int], electron: list[int], gamma: int = GAMMA) -> dict:  # type: ignore[type-arg]
    return {
        "integers": {"node_clock": gamma, "quantum_action": T, "width": 92, "link_unit": 16},
        "families": [
            {**SIGN, "pair": [gamma, gamma]},
            {"name": "proton", "pair": proton, "dimension": 2},
            {"name": "electron", "pair": electron, "dimension": 2},
        ],
    }


def test_the_one_world_at_natures_den_loads_with_the_proton_off_the_top():  # type: ignore[no-untyped-def]
    """The universe of $S/arrange/nature_den/universe_nature.json (2026-10-24): the pairs on the circle of den 53,567,765 = 5 x 17 x 73 x 89 x 97 with Gamma 1,000, the proton at (4,859,756, 53,346,867) off the top and the electron at (53,567,757, 29,276), both moving planes reading one holder: refused by name under the sentence of 2026-10-23, loaded under the charge's universality with alpha (36, 1), the write of a born quantum of either family 36 x 17,956 over 72,000 levels per interval."""
    document = {
        "integers": {"node_clock": GAMMA, "quantum_action": T, "width": 92, "link_unit": 16},
        "families": [
            {"name": "gravity", "pair": [53_529_741, DEN]},
            {"name": "charge", "pair": [DEN, DEN]},
            {"name": "matter", "pair": [32_140_659, DEN], "dimension": 1},
            {"name": "light", "pair": [DEN, DEN], "dimension": 1},
            {"name": "proton", "pair": [4_859_756, DEN], "dimension": 2},
            {"name": "electron", "pair": [53_567_757, DEN], "dimension": 2},
        ],  # the rows derived (2026-10-24); the absorber [35,564,716, den] of the file to that day, two planes reading no sign, no row of the derived law
    }
    _integers, families = universe_of(document)
    sign = next(f for f in families if f.name == "charge")
    assert (sign.write_weight, sign.write_wall) == (36, 1)
    write = held_write_of(families, families.index(sign), T)
    proton, electron = (families.index(f) for f in families if f.name in ("proton", "electron"))
    assert write.factors[proton] == write.factors[electron] == 1  # the charge the Wronskian itself
    assert write.walls[0] == 2 * T * sign.write_wall  # the one wall 2 E_s T Gamma, no count unit in it
    born = amplitude(1, T, (DEN, DEN), 1) ** 2  # the birth's quarter-turn lay, W = A^2 for either child
    assert T // 2 - born < 2 * amplitude(1, T, (DEN, DEN), 1)  # the largest square at or below T div 2
    assert (
        count_wall(families[proton], T) > 1800 * count_wall(families[electron], T)
    )  # the count units differ 1,822 times, and none of it enters the write (the former factor kept by name)


def test_the_register_reads_the_content_rooms_and_a_sign_holder_at_w_0_changes_no_neutral_body():
    """The register's scale and the lay's amplitude bound are the loader's tool and no line of the law, and a record laid at W = 0 writes nothing, so a holder of the sign may not change a neutral body's register (the Boss's word, 2026-10-24; the former rule, the min over every family's rooms with the sign holder's write room among them, kept by name, 2026-10-23): the amplitude bound of a universe whose planes read the sign holder (the charge factors standing) equals the bound of the same universe with the planes reading no sign (no charge factor, the holder written by no source), so the register (`node_detector.scale_of` from `World.amplitude_bound`) is the same; the sign holder's write room is gated apart in `bound_under_rooms`, refused by name where it leaves no level inside the width (no width of this universe reaches that gate before Rule3's own totals refuse, so the refusal is asserted by its sentence in the loader and by no world here)."""
    charged = universe_of(universe([0, 6000], [3600, 6000]))[1]
    neutral = tuple(
        replace(family, reads=()) if family.plane else family for family in charged
    )  # the same planes reading no sign, by hand: every plane reads the sign since 2026-10-24, so no file states them
    bound_charged = amplitude_bound(charged, GAMMA, T, 92, 16)
    bound_neutral = amplitude_bound(neutral, GAMMA, T, 92, 16)
    assert bound_charged == bound_neutral  # the sign holder's write room enters no other family's bound
