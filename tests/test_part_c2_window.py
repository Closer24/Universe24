"""Part C, Task 2 (the local trial, Worker C2): the window's turn of the labels by carried divisions. The labels (u, v) are Python integers in the books, so the window's turn is one hop by the phase line's pair at the window's angle, (u', v') = ((C u - S v + r_u) div X, (S u + C v + r_v) div X), the remainders carried in the books between windows (`resonance.window_pair`, `resonance.hopped`, `meeting.turned_labels`, `NodeBooks.carried`), and no shear: features/rotation is gone (Task 3). The numbers here are the first build's (tests/test_the_meeting.py (vi) before this task): the 48 sub-turns of three shears each gave the labels' angle 1.5680 at the Zeno world's n = 1 and the one shear of the whole window 1.330, the tangent half-angle's compression."""

import hashlib
import json
import math
import random
import time

import numpy as np

from event_universe import resonance, world_files
from event_universe.features import phase
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import EVENTS

GAMMA, WIDTH, TURN = (
    6000,
    63,
    9408,
)  # the Zeno world's window turn at n = 1, in units of theta_0 = 1 / Gamma
SUB_TURNS, ONE_SHEAR = (
    1.5680,
    1.330,
)  # the first build's numbers: 48 x 2 arctan(9,408 / (12,000 x 48)) and 2 arctan(9,408 / 12,000)
TURNS, LABEL = 1000, 10**6
X = phase.amplitude(GAMMA, WIDTH)  # the phase line's amplitude at the Zeno world's width, the hop's wall
FLOOR_PER_TURN = 3  # the hop's floor: one level per label from the two carried divisions (root 2 on the radius) and under one level from the pair's magnitude, (1.42 |n| + 2.3 Gamma) / X x r below 1 at r = 10^6, |n| <= 12,000, X = 32,025,594,000


def hop(
    u: int, v: int, turn: int, carried: tuple[int, int], direction: int = 1
) -> tuple[int, int, int, int]:
    """The labels hopped by the window's pair at `turn` acts of theta_0, the remainders carried."""
    cosine, sine, amplitude = resonance.window_pair(turn, GAMMA, X)
    return resonance.hopped(
        u, v, cosine, direction * sine, amplitude, carried
    )  # back: the conjugate pair


def test_the_windows_turn_is_one_hop_at_the_phase_lines_angle():
    """The window's turn: the pair (C, S) at theta_W = 9,408 theta_0 read from the phase line iterated from the seed (`window_pair`), X = 32,025,594,000 its magnitude to the walk's bound; the labels (10^6, 0) hopped once stand at the angle 9,408 / 6,000 = 1.5680 to the angle's own rounding (theta_0 = 1 / Gamma to 2.6 x 10^-9), where the first build's 48 sub-turns of three shears gave 1.5680 to 2 x 10^-3 (the sub-turns' angles adding, each a tangent half-angle) and the one shear of the whole window 1.330 (the compression the advisor's second found): the relation is new = turn x theta_0, the sub-turn form's limit as the pieces grow, with no shear and no float; the radius within a level of 10^6."""
    resonance.clear_memo()
    resonance.window_pair(
        TURN + 1234, GAMMA, X
    )  # a pair kept: the next is iterated from it, not the seed
    cosine, sine, amplitude = resonance.window_pair(TURN, GAMMA, X)
    seed = phase.seed(phase.amplitude(GAMMA, WIDTH), GAMMA)
    assert (cosine, sine) == tuple(
        int(a) for a in phase.read(phase.iterate(seed, TURN, GAMMA))
    )  # bit for bit
    assert amplitude == phase.amplitude(GAMMA, WIDTH) == X
    assert abs(math.hypot(cosine, sine) - amplitude) <= 1.42 * TURN + 2.3 * GAMMA  # the walk's bound
    u, v, r_u, r_v = resonance.hopped(LABEL, 0, cosine, sine, amplitude)
    new, exact = math.atan2(v, u), TURN / GAMMA
    print(
        f"the window's turn at n = 1 of the Zeno world: the first build's 48 sub-turns {SUB_TURNS}, its one shear "
        f"{ONE_SHEAR}; the hop {new:.7f} against theta_W = {TURN} / {GAMMA} = {exact:.7f}; the labels ({u}, {v}), "
        f"the remainders ({r_u}, {r_v}) of X = {amplitude}; the pair ({cosine}, {sine})"
    )
    assert abs(new - exact) <= 1e-6 and abs(new - SUB_TURNS) <= 2e-3 and abs(new - ONE_SHEAR) > 0.2
    assert abs(math.hypot(u, v) - LABEL) <= 1 and 0 <= r_u < amplitude and 0 <= r_v < amplitude
    assert resonance.hopped(LABEL, 0, cosine, sine, amplitude)[:2] == (u, v)  # no state but the books'
    assert hop(0, 0, TURN, (0, 0))[:2] == (0, 0) and hop(LABEL, 0, 0, (0, 0))[:2] == (LABEL, 0)


def test_the_labels_square_is_conserved_to_the_hops_floor_over_a_thousand_turns():
    """u^2 + v^2 over 1,000 hops at random window angles in [-12,000, 12,000] acts of theta_0 from the labels (10^6, 0), the remainders carried between the hops as the books carry them: the radius stays within the hop's floor, at most 3 levels per turn (`FLOOR_PER_TURN`: one level per label from the carried division's floor and under one from the pair's magnitude), 3,000 over the thousand; the measured worst departure printed (about 9 levels: the carried remainders make the floors' mean 0, so the departure walks and does not drift)."""
    draw, u, v, carried, worst = random.Random(1), LABEL, 0, (0, 0), 0.0
    for _ in range(TURNS):
        u, v, *remainders = hop(u, v, draw.randint(-2 * GAMMA, 2 * GAMMA), carried)
        carried = (remainders[0], remainders[1])
        worst = max(worst, abs(math.hypot(u, v) - LABEL))
    print(
        f"u^2 + v^2 over {TURNS} hops: the radius's worst departure {worst:.2f} levels, the floor {FLOOR_PER_TURN * TURNS}"
    )
    assert worst <= FLOOR_PER_TURN * TURNS and worst < 2 * FLOOR_PER_TURN * TURNS**0.5


def test_the_back_turn_returns_the_labels_to_the_hops_floor_and_not_bit_for_bit():
    """The reversal: 1,000 hops forward and the same 1,000 back in the reverse order by the conjugate pair (C, -S) with the remainders carried (`hopped` at direction -1). The carried remainder does not make the back-turn exact: the hop divides the two labels by X and keeps one remainder per label, and (u, v) are not recoverable from (u', v', r_u', r_v'), since C u - S v = X u' + r_u' - r_u with r_u the remainder before the hop, which the books no longer hold (one hop from (10^6, 12,345) at 777 acts comes back to (999,999, 12,345), one level short); the labels return to the hop's floor, within 3 levels per hop over the 2,000. The law's reading: the window's close is the NodeDetector's own act, a write on its books as the root is (ALGEBRA.md, The two-mode line; the advisor's precision (iii)), outside Rule3's lines; the back-in-time gate is exact between clicks on the lattice's lines, where every act is Rule3's and inverted bit for bit (the phase line among them: `phase.iterate` at direction -1 returns the pair exactly), and the books' labels are re-laid at the click (`meeting`, the counts to labels); the labels' back-turn is no claim of the law, and the first build's three shears, exact in the inverse, are gone with their compression."""
    seed = phase.seed(phase.amplitude(GAMMA, WIDTH), GAMMA)
    assert (
        phase.iterate(phase.iterate(seed, 777, GAMMA), 777, GAMMA, -1) == seed
    )  # the line's inverse exact
    once = hop(LABEL, 12_345, 777, (0, 0))
    back_once = hop(*once[:2], 777, (once[2], once[3]), -1)
    assert back_once[:2] == (LABEL - 1, 12_345), back_once
    draw, u, v, carried = random.Random(2), LABEL, 0, (0, 0)
    turns = [draw.randint(-2 * GAMMA, 2 * GAMMA) for _ in range(TURNS)]
    for turn in turns:
        u, v, *remainders = hop(u, v, turn, carried)
        carried = (remainders[0], remainders[1])
    for turn in reversed(turns):
        u, v, *remainders = hop(u, v, turn, carried, -1)
        carried = (remainders[0], remainders[1])
    miss = (u - LABEL, v)
    print(
        f"the back-turn over {TURNS} hops: the labels return to ({u}, {v}) from ({LABEL}, 0), the miss {miss}; not bit for bit"
    )
    assert max(map(abs, miss)) <= FLOOR_PER_TURN * 2 * TURNS and miss != (0, 0)


def test_the_two_slits_hop_no_label_and_stand_bit_for_bit_on_the_oracle(monkeypatch):
    """The two slits world declares no transition, so no label is hopped (no books with labels), and its 20 intervals equal the frozen look file frame by frame (the oracle of Part A), the levels' digest printed: the sha256 of `tools/run_inputs.py` on it, c50eaa36, stands (run beside the suite and reported)."""
    from tests.test_part_a_fold import ORACLE

    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", EVENTS.parents[1])
    started, look = time.perf_counter(), json.loads(ORACLE.read_text(encoding="utf-8"))
    board = Lattice(load_world(EVENTS / "two_slits" / "two_slits.json"))
    assert board.credit.bodies == []
    digest = hashlib.sha256()
    for interval in range(21):
        frame = look["frames"][interval]
        for index, family in enumerate(board.families):
            recorded = frame["families"][family.name]["now" if family.quanta else "level"]
            flat = np.zeros(board.shape, dtype=object).reshape(-1)
            if isinstance(recorded, dict):
                flat[recorded["at"]] = recorded["values"]
            else:
                flat = np.array(recorded, dtype=object).reshape(-1)
            assert np.array_equal(flat.reshape(board.shape), board.states[index].lines[0].now), interval
            digest.update(board.states[index].lines[0].now.tobytes())
        board.step()
    print(
        f"the two slits bit for bit the oracle over 20 intervals; the levels' digest {digest.hexdigest()[:16]}; {time.perf_counter() - started:.1f} s"
    )
