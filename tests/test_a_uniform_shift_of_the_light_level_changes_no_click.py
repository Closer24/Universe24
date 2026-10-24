"""A uniform shift of the light level changes no click (ALGEBRA.md, The booking is the frame's, the owner's word of 2026-10-23, "go with the sentence", on the gauge clause of The swap at the top: a massless row's uniform level is a gauge read by no act). The sentence in the books: the credit books the frame's current J_ij, the plain current num Q_ij (now_i before_j - before_i now_j) less the step's change of the Link's level term num Q_ij (before_i - before_j)(now_i + now_j) div 2 (`currents.level_term`, `readings.gauge_terms`, `node_detector.gauged`), and reads the share in the frame's form, the Node's own w v^2 (with D now before on a gapped pair) and half of each of its Links' difference products (`share.share`), whose board sums are the plain form's bit for bit; the click's hole on a plain massless record takes the record's wave and leaves the uniform level where the Node is uniform with its neighbours, its faces' target the frame's level at the Node, and is the written hole to 0 at a packet's edge, where one Link's reach reads no frame (`features/click.target_of`, the second test). The first test: a light packet crosses a declared region of two Nodes on a periodic chain of 24 Nodes under the content, with the world's draw, and the same world with the light's level shifted by one constant at every Node, now and before alike, through the lines after the load (the state a coasting mean reaches, which no lay door writes; the count gate reads the lay's own support, so the count is the shifted board's too); through the first close that credits a quantum every click line and every credit line is the same bit for bit, the light's quanta on the board and the region's share in the frame's form are the same at every interval, and the quantum is credited on both boards alike (the hole's two faces fall after the close at the packet's edge, the written hole, which the shift is no symmetry of, named open in FURTHER_RESEARCH.md); the held rows stand at their rests through the run (the universe's level weights raised so that no write of the run reaches one level, the content's paces off the exact vacuum at the rest 60, the digits fine), since the held rows' write reads the plain form per Node, which a shift moves by the Links' differences times the shift, a redistribution whose board sum is 0 (the write's form under the gauge, named in FURTHER_RESEARCH.md, is not this test's). Under the booking to 2026-10-23 the plain current moved by num c (v_i - v_j) per Link under the shift c and the hole dug to the level 0."""

import numpy as np

from event_universe.features.click import target_of

SHIFT = 500  # the uniform shift of the light level, one constant at every Node, now and before alike
INTERVALS = 70
STANDING = (
    10**9
)  # the held rows' level weight: the writes below one level through the run, the content at its rest


def test_the_faces_target_is_the_frames_level_where_the_neighbours_agree_and_moves_with_a_shift():
    """`features/click.target_of` by itself: six neighbours on one drift (the level L and L - v on every Port) give the drift's own next level L + v, and the same neighbours shifted by c give L + v + c; neighbours that do not agree on their next level (a packet's edge) give 0, the written hole; no level before given, 0."""
    level, speed, shift = 1000, 156, 500
    at = (0, 0, 0)
    now = tuple(np.full((1, 1, 1), level, dtype=object) for _port in range(6))
    before = tuple(np.full((1, 1, 1), level - speed, dtype=object) for _port in range(6))
    ports = tuple(range(6))
    assert target_of(now, before, at, ports) == level + speed
    moved = tuple(n + shift for n in now), tuple(b + shift for b in before)
    assert target_of(moved[0], moved[1], at, ports) == level + speed + shift
    edge = (now[0] + 7, *now[1:])
    assert target_of(edge, before, at, ports) == 0 and target_of(now, None, at, ports) == 0
    assert target_of(now, before, at, ()) == 0
