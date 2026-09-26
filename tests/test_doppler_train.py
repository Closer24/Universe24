"""CANCELLED (the one stroke's commit 7; ALGEBRA.md 9.85 (5), 9.91 (10) 7; the model owner's
record 2102: marked and disconnected, not deleted): the train and its boosted clock are retired;
a moving body's light is its own rotation at its Node, written by the window (9.63 (3)); this
suite is skipped whole, its text kept as the record.
DOPPLER, THE GIVEN ROWS OF A MOVING BODY CARRY ITS MOTION (ALGEBRA.md 9.62 (4), adopted by
the model owner through the Boss, record 2042; BUILD.md section 26 item 49): (1) the
generator's boosted clock: on the long wave [4096, 21] of N = 2048 (k = 0.299, c_l = 0.573)
at v = 1 / 4 the forward wave number k gamma (1 + v / c_l) = 0.478 gives the wavelength 13
and the pair [4096, 13], the backward k gamma (1 - v / c_l) = 0.187 the wavelength 34 and
[2048, 17]; at k = pi / 2 the forward boost reaches the band's edge (the wavelength 2); a pace
at or above the light's is refused; (2) the loader admits the train's own `clock` on a
moving body alone and holds the body's extent to the periods of the boosted wavelength; (3)
the long-wave Lorentz pair: the resting emitter 168 Nodes at the family's clock, the moving
one 104 Nodes at [4096, 13], its written train crossing zero 16 times along its way (8 periods
of 13), the mirror 90 Links beyond each head. COMPUTATION on the generator's integers; no pin."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe.events.world import input_stamp, parse_nature_beam_world
from tests.test_emitter import massive_generator
from tests.test_toward_nature import document, load_module

ROOT = Path(__file__).resolve().parents[1]
generator = load_module("make_worlds")

pytestmark = pytest.mark.skip(
    reason="CANCELLED at commit 7: the train and its Doppler clock are retired, a moving body's "
    "light is its own rotation written by the window (ALGEBRA.md 9.85 (5), 9.63 (3); record 2102)"
)


def test_the_boosted_clock_is_the_wave_number_times_gamma_one_plus_or_minus_v_over_c():
    massive = massive_generator()
    forward, wavelength = massive.doppler_clock([4096, 21], 2048, [1, 1], Fraction(1, 4), True)
    assert (forward, wavelength) == ([4096, 13], 13)
    backward, wavelength = massive.doppler_clock([4096, 21], 2048, [1, 1], Fraction(1, 4), False)
    assert (backward, wavelength) == ([2048, 17], 34)
    # the pair's wavelength on the circle is the whole number (the loader's rule)
    assert 2 * 2048 * 13 // 4096 == 13 and 2 * 2048 * 17 // 2048 == 34
    # at k = pi / 2 the forward boost at v = 1 / 4 reaches the band's edge: not a light
    assert massive.doppler_clock([512, 1], 1024, [1, 1], Fraction(1, 4), True) == ([1024, 1], 2)
    with pytest.raises(ValueError, match="no boost"):
        massive.doppler_clock([4096, 21], 2048, [1, 1], Fraction(3, 5), True)


def test_the_long_wave_lorentz_pair_carries_the_boosted_train_on_the_moving_emitter_alone():
    rest, moving = document("lorentz_rest_long"), document("lorentz_moving_long")
    a, b = rest["measured"][0], moving["measured"][0]
    assert a["extents"] == [168, 3, 3] and "clock" not in a["emitter"]["train"]
    assert b["extents"] == [104, 3, 3] and b["emitter"]["train"]["clock"] == [4096, 13]
    assert b["momentum"] == [3120, 0, 0] and a["momentum"] == [0, 0, 0]
    # the mirror 90 Links beyond each train's head
    start = generator.LONG_LORENTZ_EMITTER_X
    assert a["position"] == [start, 0, 0] == b["position"]
    assert rest["measured"][1]["position"][0] == start + 168 + generator.LONG_LORENTZ_ARM
    assert moving["measured"][1]["position"][0] == start + 104 + generator.LONG_LORENTZ_ARM
    # the written train: 8 periods of 13 along x, read on the middle row of the body
    now = b["emitter"]["given"]["now"]
    line = [now[(x * 3 + 1) * 3 + 1] for x in range(104)]
    crossings = sum(1 for u, w in zip(line, line[1:], strict=False) if (u > 0 > w) or (u < 0 < w))
    assert 14 <= crossings <= 17, crossings
    world = parse_nature_beam_world(moving)
    train = world.measured[0].block.emitter.train  # type: ignore[union-attr]
    assert train.clock == (4096, 13) and train.wavelength == 13 and train.periods == 8
    # the loader: the train's clock at rest refused; a wrong extent refused naming the wavelength
    at_rest = json.loads(json.dumps(rest))
    at_rest["measured"][0]["emitter"]["train"]["clock"] = [4096, 13]
    at_rest["input"] = input_stamp(at_rest)
    with pytest.raises(ValueError, match="admitted on a moving body alone"):
        parse_nature_beam_world(at_rest)
    wrong = json.loads(json.dumps(moving))
    wrong["measured"][0]["emitter"]["train"]["clock"] = [4096, 21]
    wrong["input"] = input_stamp(wrong)
    with pytest.raises(ValueError, match="8 periods of the wavelength 21 = 168 Nodes"):
        parse_nature_beam_world(wrong)
