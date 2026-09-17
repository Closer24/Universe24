"""The mean-field kernel of examples/nature/a5_static/mean_field_gauss.py, the
computation after experiment A5s (docs/EXPERIMENTS.md), pinned on a minimal board:
the split of one heading's content at one Node by the catalog's table [6, 1, 1, 1,
1, 1], the conservation of the transport (the total kept until the front reaches
the open boundary, the source's own sink taking the backward shares), and the beam
4096 x (6/11)^(r-1) as the first push on a sink at r = 1 to 4.

Expected numbers are pinned in docs/TEST_EXPECTATIONS.md ("The split table's mean
field"), written before the first run.
"""

import importlib.util
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples/nature/a5_static/mean_field_gauss.py"
RELEASE = 4096


def load_module():
    spec = importlib.util.spec_from_file_location("a5_static_mean_field_gauss", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


MF = load_module()


def test_one_heading_is_split_by_the_table_relative_to_its_heading():
    # 11 arriving on +X at the centre: 6 forward (+X), 1 backward (-X), 1 on each of
    # +Y, -Y, +Z, -Z; nothing anywhere else; the total kept.
    f = np.zeros((6, 3, 3, 3))
    f[0, 1, 1, 1] = 11.0
    out = MF.spread(f)
    assert out[:, 1, 1, 1].tolist() == [6.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert np.count_nonzero(out) == 6
    assert out.sum() == 11.0
    # The net momentum of the departures is 6 - 1 = 5 on +X (the transverse cancel).
    momentum = sum(out[j, 1, 1, 1] * np.array(h) for j, h in enumerate(MF.HEADINGS))
    assert momentum.tolist() == [5.0, 0.0, 0.0]
    # 1 arriving on +Y: forward is +Y, backward -Y, the transverse +X, -X, +Z, -Z.
    f[...] = 0.0
    f[2, 1, 1, 1] = 1.0
    out = MF.spread(f)
    assert np.allclose(out[:, 1, 1, 1], [1 / 11, 1 / 11, 6 / 11, 1 / 11, 1 / 11, 1 / 11])
    # Linear in the arrivals: 11 on +X and 22 on -X give 8 on +X, 13 on -X, 3 transverse.
    f[...] = 0.0
    f[0, 1, 1, 1] = 11.0
    f[1, 1, 1, 1] = 22.0
    out = MF.spread(f)
    assert np.allclose(out[:, 1, 1, 1], [8.0, 13.0, 3.0, 3.0, 3.0, 3.0])
    assert math.isclose(out.sum(), 33.0)
    # The simple walk, the table [1, 1, 1, 1, 1, 1]: 6 on +X give 1 on every Port.
    f[...] = 0.0
    f[0, 1, 1, 1] = 6.0
    out = MF.spread(f, MF.SIMPLE_WALK)
    assert out[:, 1, 1, 1].tolist() == [1.0] * 6
    # The walks' diffusion constants: 4/9 for the table, 1/6 for the simple walk.
    assert math.isclose(MF.diffusion(MF.SPREAD), 4 / 9)
    assert math.isclose(MF.diffusion(MF.SIMPLE_WALK), 1 / 6)


def test_transport_conserves_the_total_until_the_boundary():
    # 11 on +X at the centre of a 9^3 box, no source, no sink: the total is 11 exactly
    # while the front is inside (ticks 1 to 4), then the open faces take what walks out.
    board = MF.Board((9, 9, 9), (False, False, False), (4, 4, 4), sinks=[], release=0.0)
    f = board.empty()
    f[0, 4, 4, 4] = 11.0
    totals = []
    for _ in range(6):
        f, pushes = board.step(f)
        assert pushes == []
        totals.append(float(f.sum()))
    assert all(math.isclose(total, 11.0, rel_tol=1e-12) for total in totals[:4])
    assert totals[4] < 11.0 and totals[5] < totals[4]
    # The source with its own sink, the release 4096 on six headings: the totals after
    # the first three steps 6R, 12R - 6R/11 and 18R - 12R/11 (the backward shares of the
    # fresh releases return to the source and are absorbed), the source's push zero.
    full = MF.Board((9, 9, 9), (False, False, False), (4, 4, 4), [(4, 4, 4)])
    f = full.empty()
    expected = [6 * RELEASE, 12 * RELEASE - 6 * RELEASE / 11, 18 * RELEASE - 12 * RELEASE / 11]
    for total in expected:
        f, pushes = full.step(f)
        assert pushes[0].tolist() == [0.0, 0.0, 0.0]
        assert math.isclose(float(f.sum()), total, rel_tol=1e-12)
    # The octant with three mirror planes holds the same field on its stored part.
    octant = MF.Board((5, 5, 5), (True, True, True), (0, 0, 0), [(0, 0, 0)])
    g = octant.empty()
    for _ in range(3):
        g, _ = octant.step(g)
    assert np.allclose(f[:, 4:, 4:, 4:], g, rtol=1e-12, atol=1e-9)


def test_the_beam_is_the_first_push_at_every_r():
    # A sink at (r, 0, 0) with the boundary 6 away: no push before tick r; at ticks r
    # and r + 1 exactly the unscattered 4096 (6/11)^(r-1) (a detour costs two ticks, so
    # nothing scattered arrives before tick r + 2, when the push exceeds the beam for
    # r >= 2; at r = 1, the source's neighbour, the first detoured content arrives on a
    # transverse heading and the push on x stays 4096 through tick 4).
    beams = {1: 4096.0, 2: 2234.181818181818, 3: 1218.6446280991736, 4: 664.7152516904583}
    for r, expected in beams.items():
        assert math.isclose(MF.beam(r), expected, rel_tol=1e-12)
        board = MF.sink_board(r, 6)
        f = board.empty()
        pushes = []
        for _ in range(r + 3):
            f, (_, on_sink) = board.step(f)
            pushes.append(on_sink)
        assert all(push.tolist() == [0.0, 0.0, 0.0] for push in pushes[: r - 1])
        for push in pushes[r - 1 : r + 1]:
            assert math.isclose(push[0], expected, rel_tol=1e-12)
            assert push[1] == 0.0 and push[2] == 0.0
        if r == 1:
            assert all(push.tolist() == [4096.0, 0.0, 0.0] for push in pushes[:4])
        else:
            assert pushes[r + 1][0] > expected
