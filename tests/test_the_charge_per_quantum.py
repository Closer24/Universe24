"""The charge is the Wronskian per quantum (ALGEBRA.md, The constants, the owner's word of 2026-10-24, nature's charge universality, "nature is the main thing"; the old "one ratio per holder, E_h T num / (Gamma den)" of 2026-10-23 kept by name): the holder of the sign carries one alpha = E_h T / Gamma with any pairs under it (`loader/derived.alpha_of`), and each reader's Wronskian enters the holder's one write times 3 T over its own count unit W_c sin omega_0 (`loader/derived.held_write_of`, the charge factors, the readers' units brought to one wall as the tension lines' dens are; `records.write_sources` on the time line, `bookings.booked_sources` at the start), so that every quantum of every family writes the same charge, T / 2 per count, the proton's and the electron's alike at any masses. Measured here on a small torus with a proton and an electron of different pairs both reading the sign holder, each one quantum laid at the quarter turn (the law's one-Node lay of a plane quantum, now (A, 0), before (0, sense A)): the write per quantum of the two is equal within the lay's rounding of A, exact in the identity factor x count unit; and the one world's universe at nature's den (the proton off the top at (4,859,756, 53,346,867), the electron at (53,567,757, 29,276), Gamma 1,000 kept) loads, which the sentence of 2026-10-23 refused by name."""

from __future__ import annotations

import json

import numpy as np

from event_universe.loader.derived import amplitude_bound, count_wall, held_write_of
from event_universe.loader.universe import universe_of

GAMMA, T = 1000, 36_000
DEN = 53_567_765
SIGN = {
    "name": "charge",
    "pair": [GAMMA, GAMMA],
    "reads": {},
    "held": {"sources": ["wronskian"], "level_weight": 1},
}


def universe(proton: list[int], electron: list[int], gamma: int = GAMMA) -> dict:  # type: ignore[type-arg]
    return {
        "integers": {"node_clock": gamma, "quantum_action": T, "width": 92, "link_unit": 16},
        "families": [
            {**SIGN, "pair": [gamma, gamma]},
            {"name": "proton", "pair": proton, "reads": {"charge": 1}, "dimension": 2},
            {"name": "electron", "pair": electron, "reads": {"charge": 1}, "dimension": 2},
        ],
    }


def test_the_one_world_at_natures_den_loads_with_the_proton_off_the_top():  # type: ignore[no-untyped-def]
    """The universe of $S/arrange/nature_den/universe_nature.json (2026-10-24): the pairs on the circle of den 53,567,765 = 5 x 17 x 73 x 89 x 97 with Gamma 1,000, the proton at (4,859,756, 53,346,867) off the top and the electron at (53,567,757, 29,276), both moving planes reading one holder: refused by name under the sentence of 2026-10-23, loaded under the charge's universality with alpha (36, 1)."""
    document = {
        "integers": {"node_clock": GAMMA, "quantum_action": T, "width": 92, "link_unit": 16},
        "families": [
            {
                "name": "gravity",
                "pair": [53_529_741, DEN],
                "reads": {"gravity": 1},
                "held": {"sources": ["form", "tensions"], "level_weight": 1, "write_weight": 1},
            },
            {
                "name": "charge",
                "pair": [DEN, DEN],
                "reads": {},
                "held": {"sources": ["wronskian"], "level_weight": 1},
            },
            {"name": "matter", "pair": [32_140_659, DEN], "reads": {"gravity": 1}, "dimension": 1},
            {"name": "light", "pair": [DEN, DEN], "reads": {"gravity": 1}, "dimension": 1},
            {
                "name": "proton",
                "pair": [4_859_756, DEN],
                "reads": {"gravity": 1, "charge": 1},
                "dimension": 2,
            },
            {
                "name": "electron",
                "pair": [53_567_757, DEN],
                "reads": {"gravity": 1, "charge": 3},
                "dimension": 2,
            },
            {
                "name": "absorber",
                "pair": [35_564_716, DEN],
                "reads": {"gravity": 1},
                "dimension": [2, 2],
            },
        ],
    }
    _integers, families = universe_of(document)
    sign = next(f for f in families if f.name == "charge")
    assert (sign.write_weight, sign.write_wall) == (36, 1)
    write = held_write_of(families, families.index(sign), T)
    proton, electron = (families.index(f) for f in families if f.name in ("proton", "electron"))
    assert write.factors[proton] * count_wall(families[proton], T) == write.factors[
        electron
    ] * count_wall(families[electron], T)
    assert np.gcd(write.factors[proton], write.factors[electron]) >= 1


def test_the_register_reads_the_content_rooms_and_a_sign_holder_at_w_0_changes_no_neutral_body():
    """The register's scale and the lay's amplitude bound are the loader's tool and no line of the law, and a record laid at W = 0 writes nothing, so a holder of the sign may not change a neutral body's register (the Boss's word, 2026-10-24; the former rule, the min over every family's rooms with the sign holder's write room among them, kept by name, 2026-10-23): the amplitude bound of a universe whose planes read the sign holder (the charge factors standing) equals the bound of the same universe with the planes reading no sign (no charge factor, the holder written by no source), so the register (`node_detector.scale_of` from `World.amplitude_bound`) is the same; the sign holder's write room is gated apart in `bound_under_rooms`, refused by name where it leaves no level inside the width (no width of this universe reaches that gate before Rule3's own totals refuse, so the refusal is asserted by its sentence in the loader and by no world here)."""
    charged = universe([0, 6000], [3600, 6000])
    neutral = json.loads(json.dumps(charged))
    for family in neutral["families"][1:]:
        family["reads"] = {}
    bound_charged = amplitude_bound(universe_of(charged)[1], GAMMA, T, 92, 16)
    bound_neutral = amplitude_bound(universe_of(neutral)[1], GAMMA, T, 92, 16)
    assert bound_charged == bound_neutral  # the sign holder's write room enters no other family's bound
