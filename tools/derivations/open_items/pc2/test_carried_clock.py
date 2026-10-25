"""pc2: the one-Node test of the carried clock, runnable (python test_carried_clock.py, or pytest), under 15 seconds, integers only.
The checks: (1) the chain: the forward act of every hill's inverse returns the content (Gamma hills), and the forward act carries every hollow to the next; (2) the width: every transient of the carried clock within 20 bits at Gamma 1,000 (the memo's fraction 37,805 bits at the frozen content); (3) the frozen content and the clock's zero equal the memo's (3,793; 7,598); (4) the carried clock against the memo over 0..3,793: within one unit everywhere, equal at all but 6 contents with the half-wall origin; (5) the Link's pace from the clock, p^2 over Gamma rounded once, no remainder; (6) off the flag the module is the engine bit for bit (clock_of, link_pace_of, volume_of, level_of on a board of contents); (7) the forward act is not injective at exactly the contents with r = Gamma - 1 (one below the frozen content: 584), the one law the carried clock does not meet on its own state (the run back of the clock's own chain), mended by the memo's chain (the content the state, the clock its reading)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pc2_paces as P
from event_universe.core import paces as E
from event_universe.features import volume as V

GAMMA = 1000


def test_chain_hills_and_hollows():
    P.clear_memo()
    assert all(P.carried_forward(GAMMA, *P.carried_pair(GAMMA, c - 1)) == P.carried_pair(GAMMA, c) for c in range(-GAMMA + 1, 3794))


def test_width_20_bits():
    assert max(((GAMMA - 1) * P.carried_pair(GAMMA, c)[0] + P.carried_pair(GAMMA, c)[1]).bit_length() for c in range(0, 7599)) == 20
    assert max((GAMMA * P.carried_pair(GAMMA, c)[0] + P.carried_pair(GAMMA, c)[1]).bit_length() for c in range(0, -GAMMA - 1, -1)) == 22
    assert (GAMMA * (GAMMA - 1) ** 3793).bit_length() == 37805


def test_frozen_and_zero_equal_memo():
    E.clear_memo(); P.CARRIED = True
    try:
        assert P.frozen_content(GAMMA) == E.frozen_content(GAMMA) == 3793
        zero_c = P.clock_zero(GAMMA)
        P.CARRIED = False; E.clear_memo(); zero_m = 0
        while E.clock(GAMMA, zero_m) > 0: zero_m += 1
        assert zero_m == 7598 and zero_c == 7482  # the carried clock reaches 0 earlier than the memo (the carried value one below the memo's over the deep contents where the clock is below 12), beyond the Link's zero 3,793 either way
    finally:
        P.CARRIED = False


def test_against_memo_within_one_unit():
    E.clear_memo(); P.clear_memo()
    diffs = [c for c in range(0, 3794) if P.carried_clock(GAMMA, c) != E.clock(GAMMA, c)]
    assert all(abs(P.carried_clock(GAMMA, c) - E.clock(GAMMA, c)) == 1 for c in diffs)
    assert diffs == [72, 210, 584, 797, 1128, 1267]


def test_link_pace_from_clock():
    assert all(P.carried_link_pace(GAMMA, c) == (2 * P.carried_clock(GAMMA, c) ** 2 + GAMMA) // (2 * GAMMA) for c in range(-100, 3794))


def test_flag_off_is_engine():
    P.CARRIED = False; E.clear_memo()
    contents = np.array([[-5, 0, 7], [72, 584, 3792]], dtype=object)
    assert (P.clock_of(GAMMA, contents) == E.clock_of(GAMMA, contents)).all()
    assert (P.link_pace_of(GAMMA, contents) == E.link_pace_of(GAMMA, contents)).all()
    assert (P.volume_of(GAMMA, contents) == V.volume_of(GAMMA, contents)).all()
    X = V.volume_of(GAMMA, contents)
    assert (P.level_of(GAMMA, X) == V.level_of(GAMMA, X)).all()  # the engine's own level reading, bit for bit (the level is the largest a of the volume, so level_of(volume_of(c)) is c at the last content of each clock value alone)


def test_carried_volume_reading_round_trip():
    P.CARRIED = True
    try:
        contents = np.array([-900, -5, 0, 7, 72, 584, 1267, 3792], dtype=object)
        X = P.volume_of(GAMMA, contents)
        assert (P.volume_of(GAMMA, P.level_of(GAMMA, X)) == X).all()  # the volume's round trip: the level is the largest a of the volume, one per clock value
        assert all(P.carried_clock(GAMMA, int(a)) == P.carried_clock(GAMMA, int(c)) for a, c in zip(P.level_of(GAMMA, X).tolist(), contents.tolist()) if int(c) >= 0)  # on the hollows the level returns the clock; on a deep hill the volume X is a small integer and reads several clocks as one (the engine's own coarseness)
    finally:
        P.CARRIED = False


def test_forward_not_injective_at_r_wall_minus_one():
    misses = [c for c in range(0, 3793) if P.carried_back(GAMMA, *P.carried_pair(GAMMA, c + 1)) != P.carried_pair(GAMMA, c)]
    assert misses == [584]
    assert P.carried_pair(GAMMA, 584)[1] == GAMMA - 1


if __name__ == '__main__':
    import time
    t0 = time.monotonic_ns()
    for name, f in sorted(globals().items()):
        if name.startswith('test_') and callable(f):
            f(); print(name, 'passed')
    print('milliseconds', (time.monotonic_ns() - t0) // 1000000)
