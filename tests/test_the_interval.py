"""The hypothesis's construction (ALGEBRA.md, The board's interval is no observable; The mean's velocity is the content's; The motion of gravity's row is a hill at the symmetry's weight; The hill's weight is the write's mix; The form's own clock; The factor carried; the hypotheses under their own names, 2026-10-22; DESIGN section 3, T3 to T8), construction alone and no world of the experiment: the form's own clock as one power of the write (T6), the hill's weight's integer and its rounding (T3), the premise as a test (T4), the run back refused by name under the key (T5), the mix's weight following the Node's own sources (T7) and the end's booking switch (T8); the declaration and the attractor stand in tests/test_the_uniform_mode.py (T1, T2 and T9), the builders in tests/laws_interval.py."""

import math

import numpy as np

from event_universe import world_files
from event_universe.core import paces
from event_universe.features.held_write import held_write
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws_interval import GAMMA, laid_torus, lockstep, universe_at_weight_one


def test_the_forms_own_clock_books_a_count_once_and_the_write_dims_as_the_pairs_integer(
    tmp_path, monkeypatch
):
    """T6, the form's own clock (ALGEBRA.md, The write per proper volume and per proper interval, The form's own clock; loader/universe.booking_of, loader/derived.FamilyRule.power and exponent, records.write_sources): on the 3-cube torus under the law's key with gravity declaring `booking: form` the booking's power is 1 and the row's exponents 6 for its own massless pair and 5 for matter's gapped pair (7 and 6 under `count`, the law), the write's numerator over 60 intervals is `paces.write_factor(D, p, p, p, p_0, Gamma, 1)` bit for bit, the Wronskian's power on a count, and gravity's level after each write the held write's own (features/held_write) with the remainder after it, under `count` the same at the power 2; the write's dimming read from the first and the last interval as -ln(s_t / s_0) / (U_t - U_0) lies within 0.3 of 4.8 under the key (between 4 and 5: the form's clock's e^(-4 U) with the record's own sine running) and within 0.3 of 5.8 without it (between 5 and 6), the eras hand's and the kinematics hand's exponents for [4000, 6000] at small U; the genericity hand's line: one power of the write, no other act."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    exponents = {}
    for booking, power in (("form", 1), ("count", 2)):
        universe_at_weight_one(tmp_path, gravity={"booking": booking})
        board = Lattice(load_world(laid_torus(tmp_path, f"clock_{booking}", uniform="carried")))
        names = [family.name for family in board.families]
        gravity, matter = board.families[names.index("gravity")], board.families[names.index("matter")]
        assert (gravity.power, gravity.exponent(), matter.exponent(power)) == (
            power,
            3 + power + 2,
            3 + power + 1,
        )
        assert (gravity.form_clock, matter.exponent()) == (
            power == 1,
            3 + 2 + 1,
        )  # a reader's own power the law's
        wall, numerators = board.walls(names.index("gravity"))[0], []
        for step in lockstep(board, names.index("gravity"), names.index("matter"), 60):
            form = step["now"] * step["now"] - step["next"] * step["before_record"]
            clock, pace = paces.node_paces(
                GAMMA, step["level"]
            )  # matter reads gravity at 1, the content
            numerator = int(paces.write_factor(np.array(form), pace, pace, pace, clock, GAMMA, power))
            level, carried = held_write(
                2 * step["level"] - step["before"], numerator, wall, step["remainder"]
            )
            assert (step["after"], step["remainder_after"]) == (int(level), int(carried))
            numerators.append((step["level"] / GAMMA, numerator))
        (first_u, first), (last_u, last) = numerators[0], numerators[-1]
        exponents[booking] = -math.log(last / first) / (last_u - first_u)
        assert last_u - first_u > 0.5  # the content moved: the exponent read over a span of U
    assert abs(exponents["form"] - 4.8) < 0.3 and abs(exponents["count"] - 5.8) < 0.3, exponents
