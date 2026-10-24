"""The charge is the Wronskian per quantum (ALGEBRA.md, The constants, the owner's word of 2026-10-24, nature's charge universality, "nature is the main thing"; the old "one ratio per holder, E_h T num / (Gamma den)" of 2026-10-23 kept by name): the holder of the sign carries one alpha = E_h T / Gamma with any pairs under it (`loader/derived.alpha_of`), and each reader's Wronskian enters the holder's one write times 3 T den over its own count unit W_c sin omega_0 (`loader/derived.held_write_of`, the charge factors, the readers' units brought to one wall as the tension lines' dens are; `records.write_sources` on the time line, `bookings.booked_sources` at the start), so that every quantum of every family writes the same charge, T / 2 per count, the proton's and the electron's alike at any masses. Measured here on a small torus with a proton and an electron of different pairs both reading the sign holder, each one quantum laid at the quarter turn (the law's one-Node lay of a plane quantum, now (A, 0), before (0, sense A)): the write per quantum of the two is equal within the lay's rounding of A, exact in the identity factor x count unit; and the one world's universe at nature's den (the proton off the top at (4,859,756, 53,346,867), the electron at (53,567,757, 29,276), Gamma 1,000 kept) loads, which the sentence of 2026-10-23 refused by name."""

from __future__ import annotations

import json
from dataclasses import replace

import numpy as np

from event_universe.loader.charge import lightest_point
from event_universe.loader.derived import amplitude_bound, count_wall, held_write_of
from event_universe.loader.universe import universe_of
from tests.laws import EVENTS, refused

GAMMA, T = 1000, 36_000
DEN = 53_567_765
SIGN = {"name": "charge", "pair": [GAMMA, GAMMA]}  # the holder of the sign, the held massless row


def universe(proton: list[int], electron: list[int], gamma: int = GAMMA) -> dict:  # type: ignore[type-arg]
    return {
        "integers": {"node_clock": gamma, "quantum_action": T},
        "families": [
            {**SIGN, "pair": [gamma, gamma]},
            {"name": "proton", "pair": proton, "dimension": 2},
            {"name": "electron", "pair": electron, "dimension": 2},
        ],
    }


def test_the_one_world_at_natures_den_loads_with_the_proton_off_the_top():  # type: ignore[no-untyped-def]
    """The universe of $S/arrange/nature_den/universe_nature.json (2026-10-24): the pairs on the circle of den 53,567,765 = 5 x 17 x 73 x 89 x 97 with Gamma 1,000, the proton at (4,859,756, 53,346,867) off the top and the electron at (53,567,757, 29,276), both moving planes reading one holder: refused by name under the sentence of 2026-10-23, loaded under the charge's universality with alpha (36, 1)."""
    document = json.loads(
        (EVENTS / "universe24" / "universe_universe24.json").read_text(encoding="utf-8")
    )
    _integers, families = universe_of(document)  # the one universe file: its rows at nature's den
    sign = next(f for f in families if f.name == "charge")
    assert (sign.write_weight, sign.write_wall) == (36, 1)
    write = held_write_of(families, families.index(sign), T)
    proton, electron = (families.index(f) for f in families if f.name in ("proton", "electron"))
    assert write.factors[proton] * count_wall(families[proton], T) == write.factors[
        electron
    ] * count_wall(families[electron], T)
    assert (
        np.gcd.reduce(
            [write.factors[proton], write.factors[electron], write.walls[0] // (2 * T * sign.write_wall)]
        )
        == 1
    )  # the factors reduced once by their common divisor


def test_the_lightest_point_of_the_circle_is_the_electrons_pair():
    """The extremal sentence (the owner's word of 2026-10-24, 09:1x UTC: the charged plane family at rest is the lightest point of the circle; ALGEBRA.md, The one universe): s_min(den) is the least leg among the Pythagorean points of den's circle, enumerated whole from den's primes, m_e / T = s_min / den; at the one universe's den 53,567,765 the point (53,567,757, 29,276), the electron row's pair; at den 1,000 (960, 280), at 5 (4, 3), at 65 (63, 16), at 25 (24, 7); a den no prime 1 mod 4 divides has no point and is refused by name."""
    num, s = lightest_point(DEN)
    assert (num, s) == (53_567_757, 29_276) and num * num + s * s == DEN * DEN
    rows = json.loads((EVENTS / "universe24" / "universe_universe24.json").read_text(encoding="utf-8"))
    assert [f["pair"] for f in rows["families"] if f["name"] == "electron"] == [[num, DEN]]
    assert [lightest_point(d) for d in (1000, 5, 65, 25)] == [(960, 280), (4, 3), (63, 16), (24, 7)]
    refused("no prime 1 mod 4 divides it", lightest_point, 9)


def test_the_register_reads_the_content_rooms_and_a_sign_holder_at_w_0_changes_no_neutral_body():
    """The register's scale and the lay's amplitude bound are the loader's tool and no line of the law, and a record laid at W = 0 writes nothing, so a holder of the sign may not change a neutral body's register (the Boss's word, 2026-10-24; the former rule, the min over every family's rooms with the sign holder's write room among them, kept by name, 2026-10-23): the amplitude bound of a universe whose planes read the sign holder (the charge factors standing) equals the bound of the same universe with the planes reading no sign (no charge factor, the holder written by no source), so the register (`node_detector.scale_of` from `World.amplitude_bound`) is the same; the sign holder's write room is gated apart in `bound_under_rooms`, refused by name where it leaves no level inside the width (no width of this universe reaches that gate before Rule3's own totals refuse, so the refusal is asserted by its sentence in the loader and by no world here)."""
    charged = universe_of(universe([0, 6000], [3600, 6000]))[1]
    neutral = tuple(
        replace(family, reads=()) if family.plane else family for family in charged
    )  # the same planes reading no sign, by hand: every plane reads the sign since 2026-10-24, so no file states them
    bound_charged = amplitude_bound(charged, GAMMA, T, 92, 16)
    bound_neutral = amplitude_bound(neutral, GAMMA, T, 92, 16)
    assert bound_charged == bound_neutral  # the sign holder's write room enters no other family's bound
