"""Tensor24's time gear (stage 7b): laid by the load, every coefficient from the files' integers, the ruler read at its
counts, the count composing as Postulate 6 has it, its spring's swing, and the run back with it moving."""

import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from tensor24.engine import step
from tensor24.engine.state import LAID, Layout, State
from tensor24.main import layout, made
from tensor24.runner.files import NAMES, departures, sites_of
from tensor24.runner.load import load, mesh_unit, ruler_of
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds
from tests import frame

EXAMPLES = Path(__file__).resolve().parents[1] / "examples" / "tensor24"
SHAPE, GAMMA, ROUNDS = (3, 3, 3), 50, 12  # a small board, a small full rate, the rounds of a run back


def built(gamma=GAMMA, massive=False, shape=SHAPE):
    """The example's files at the full rate gamma, with a massive train of A1 beside light where asked, loaded, and their
    layout: (the universe, the loaded, the layout)."""
    u = json.loads((EXAMPLES / "universe.json").read_text(encoding="utf-8"))
    den = u["integers"]["den"]
    u["integers"]["full_rate"], u["couplings"] = gamma, []
    u["trains"] += [{"name": "dust", "kinds": ["A1"], "part": 1, "pinion": den - den // 97}] * massive
    held, found = load(u, {"gears": []}, sites_of(list(shape)), *made(shape))
    assert found == [] and held is not None
    return u, held, layout(u, list(shape), held)


def world(rng, layout, counts):
    """A state on the layout: light's gears across 2**256, each fine tooth within its W, the time gear at the counts."""
    nb, _, _, (w, *_), _, _, _, (row, *_) = layout
    rows, n = len(w), nb.shape[1]
    a, b = frame.wide(rng, (rows, n)), frame.wide(rng, (rows, n))
    a[row], b[row] = counts, counts - rng.integers(-1, 2, n).astype(object)
    zero = np.zeros((1, n), dtype=object)
    r = frame.wide(rng, (rows, n)) % step.ruled(layout.gearing, layout.ruler, b, a, a).w
    return State(a, b, r, 0 * a, 0 * a, zero, zero.copy(), zero.copy())


def test_every_coefficient_is_the_files_integers_by_davids_table_at_rest():
    """David's table (#2187 6488192915, 6488709540): T = 6 den Gamma^2 G^2; light reading the ruler at (2 T, 2), the time
    gear at (T, 1) with its pinion den - den div Gamma, its kick T and its drive (T div 2) key; one cone, 1/6."""
    u, _, layout = built()
    integers = u["integers"]
    den, gamma, key = (integers[k] for k in ("den", "full_rate", "key"))
    g, spokes = mesh_unit(gamma), len(layout.nb)
    teeth = spokes * den * gamma * gamma * g * g
    w, wp, s, spring, kick, drive = (
        np.broadcast_to(x, (len(layout.gearing.w), 1))[:, 0].tolist() for x in layout.gearing
    )
    *hand, time = range(len(w))
    assert w == wp == [teeth + teeth] * len(hand) + [teeth] and s == [1 + 1] * len(hand) + [1]
    assert spring == [0] * len(hand) + [(spokes + spokes) * (den // gamma) * g * g * gamma * gamma]
    assert kick == [1] * len(hand) + [teeth] and drive == [1] * len(hand) + [teeth // (1 + 1) * key]
    assert {Fraction(x * grip, y) for x, y in zip(s, w, strict=True) for grip in layout.grip[0]} == {
        Fraction(1, spokes)
    }
    assert layout.ruler.row == time and layout.ruler.teeth[0] == teeth and (layout.rate == gamma).all()
    for full in (
        1 + 1,
        GAMMA,
        997,
        1000,
        6000,
    ):  # K-S1: the least G at which one notch of tension resolves
        least = mesh_unit(full)
        assert (
            (least + least) * least * (full + full - 1)
            > full * full
            >= (least + least - 1 - 1) * (least - 1) * (full + full - 1)
        )


def test_the_ruler_is_the_rate_line_walked_once_to_the_clocks_last_rate():
    """Y(c) = rate(-c) within one of Gamma (Gamma / (Gamma - 1))^c, its length the hollows' walk to where the Mesh's rate
    rounds to 0, by divmod here and by the load's carries there."""
    for gamma in (GAMMA, 997, 1000):
        ruler, square = ruler_of(gamma), gamma * gamma
        assert ruler[0] == gamma
        assert all(
            abs(y * (gamma - 1) ** c - gamma ** (c + 1)) <= (gamma - 1) ** c for c, y in enumerate(ruler)
        )
        hollow, tooth, stopped = square * gamma, gamma // (1 + 1), 0
        while (((hollow + hollow + square) // (square + square)) ** (1 + 1) * (1 + 1) + gamma) // (
            gamma + gamma
        ):
            hollow, tooth = divmod(hollow * (gamma - 1) + tooth, gamma)
            stopped += 1
        assert len(ruler) == stopped


def test_a_count_below_0_reads_at_0_and_past_the_last_at_the_last():
    last, counts = 7, np.array([-(1 << 70), -3, -1, 0, 4, 7, 8, 1 << 70], dtype=object)
    read = [min(max(c, 0), last) for c in counts]
    assert step.reading(counts, last).tolist() == read
    scale = 3  # a table whose entries tell its counts apart
    table = np.arange(last + 1).astype(object) * scale
    assert step.at(table, counts, last).tolist() == [scale * c for c in read]


def ruled_naively(layout, b, a, after):
    """The round's gearing by loops: a reading row's W = Z_b + Z_n, W+ = Z_n + Z_+, D its factor times Y_n^2."""
    gearing, (row, last, teeth, square, reads, factor) = layout.gearing, layout.ruler
    at = [[min(max(int(x), 0), last) for x in counts[row]] for counts in (b, a, after)]
    rows, n = len(reads), len(at[0])
    out = [np.broadcast_to(x, (rows, n)).copy() for x in gearing]
    for g in range(rows):
        for i in range(n * int(reads[g, 0])):
            zb, zn, zp = (teeth[x[i]] for x in at)
            out[0][g, i], out[1][g, i], out[3][g, i] = zb + zn, zn + zp, factor[g, 0] * square[at[1][i]]
    return out


def test_the_round_reads_the_ruler_at_the_time_gears_three_counts():
    _, _, layout = built()
    rng, row, last = np.random.default_rng(2), layout.ruler.row, layout.ruler.last
    n = layout.nb.shape[1]
    b, a, after = (
        rng.integers(-5, last + 5, (len(layout.gearing.w), n)).astype(object) for _ in range(3)
    )
    got, want = step.ruled(layout.gearing, layout.ruler, b, a, after), ruled_naively(layout, b, a, after)
    assert all((np.broadcast_to(x, y.shape) == y).all() for x, y in zip(got, want, strict=True))
    assert (
        len({int(x) for x in got.w[0]}) > 1 and (got.w[row] == layout.gearing.w[row]).all()
    )  # it moved, and not T


def test_at_rest_the_ruler_reads_the_gearing_as_laid_so_the_act_is_7as():
    """Light too faint to carry one of the drive's quanta leaves the time gear at 0, so the round is 7a's at (2 T, 2)."""
    _, _, layout = built(massive=True)
    s = world(np.random.default_rng(3), layout, np.zeros(layout.nb.shape[1], dtype=object))
    s.a[:] = s.a % (1 + 1)  # each gear at 0 or 1: below one of the drive's quanta, (T div 2) key
    s.b[:] = s.b % (1 + 1)
    s.b[layout.ruler.row] = 0
    s.a[layout.ruler.row] = 0
    tick, laid = step.tick(layout, s, 1), step.tick(Layout(*layout[:-1], LAID), s, 1)
    assert frame.same(frame.flat(tick), frame.flat(laid)) and not (tick[0].a == s.a).all()


def pushes(layout, counts, read=lambda c: c):
    """The time gear's force where its count stands at `read(counts)` at every Node-clock and every other gear is 0."""
    row, rows, n = layout.ruler.row, len(layout.gearing.w), layout.nb.shape[1]
    a = np.zeros((rows, n), dtype=object)
    a[row] = read(counts)
    zero = np.zeros((1, n), dtype=object)
    laid = step.ruled(layout.gearing, layout.ruler, a, a, a)  # the round's gearing, as the tick reads it
    s = State(a, a.copy(), 0 * a, 0 * a, 0 * a, zero, zero.copy(), zero.copy())
    force, _ = step.sources(layout._replace(gearing=laid), s)
    return force[row]


def composed(push):
    """Two loads compose by the sum of their counts (Postulate 6): the push of c1 + c2 is the two pushes' sum, bit for bit."""
    rng = np.random.default_rng(4)
    for _ in range(3):
        c1, c2 = (rng.integers(0, 50, 27).astype(object) for _ in range(1 + 1))
        if not (push(c1 + c2) == push(c1) + push(c2)).all():
            return False
    return True


def test_two_loads_compose_by_the_sum_of_their_counts_and_the_stretch_does_not():
    _, _, layout = built()
    ruler = np.array(ruler_of(GAMMA), dtype=object)
    assert composed(lambda c: pushes(layout, c))
    assert not composed(
        lambda c: pushes(layout, c, lambda x: ruler.take(x.astype(int)))
    )  # the head's law on Y
    own = layout.ruler._replace(reads=layout.ruler.reads * 0 + 1, spring=layout.ruler.spring * 0 + 1)
    assert not composed(
        lambda c: pushes(layout._replace(ruler=own), c)
    )  # the time gear reading its own ruler


def test_the_counts_swing_returns_with_its_period_by_its_one_notch():
    """At rest with no source, a count laid alike everywhere swings by the spring alone, 1 - cos w = s D / (2 W), about
    2 pi sqrt(Gamma / 2) ticks a swing, and returns: no growth, no decay beyond the remainders, through counts below 0."""
    _, _, layout = built()
    (w, _, s, spring, *_), row = layout.gearing, layout.ruler.row
    omega = math.acos(1 - Fraction(int(s[row, 0] * spring[row, 0]), int(w[row, 0] + w[row, 0])))
    n, start = layout.nb.shape[1], 40
    state = world(np.random.default_rng(5), layout, np.full(n, start, dtype=object))
    state.a[:row], state.b[:row], state.b[row] = 0, 0, start
    state.r[:] = 0
    counts = []
    for _ in range(int(10 * math.pi / omega)):
        state, _ = step.tick(layout, state, 1)
        counts.append(int(state.a[row, 0]))
    crossings = [t for t in range(1, len(counts)) if (counts[t - 1] < 0) != (counts[t] < 0)]
    halves = np.diff(crossings)
    swings, period = (
        9,
        int(math.pi / omega + math.pi / omega),
    )  # half swings in the run, and one swing's ticks
    assert len(crossings) >= swings and all(abs(h - math.pi / omega) < 1 + 1 for h in halves)
    assert abs(max(counts[-period:]) - start) <= 1 + 1 and min(counts) < 0
    assert len({tuple(state.a[row])}) == 1 and len(set(state.a[row])) == 1  # alike everywhere


def test_the_run_back_is_exact_with_the_time_gear_moving_and_the_gears_reading_its_counts():
    _, _, layout = built(
        massive=True
    )  # light and a massive train source the time gear by their rho + 3p
    rng, last = np.random.default_rng(6), layout.ruler.last
    n = layout.nb.shape[1]
    s = world(rng, layout, rng.integers(-5, last + 5, n).astype(object))
    masks = [rng.integers(0, 1 + 1, (1, n)).astype(object) for _ in range(ROUNDS)]
    end, outs = rounds(step.tick, layout, s, masks)
    assert frame.same(rewind(step.untick, layout, end, outs), s)
    assert not (end.a[layout.ruler.row] == s.a[layout.ruler.row]).all()  # the time gear moved


def test_the_three_example_files_run_their_ticks_and_run_back():
    paths = [EXAMPLES / f"{name}.json" for name in NAMES]
    assert departures(*paths) == []
    u, p, s = (json.loads(path.read_text(encoding="utf-8")) for path in paths)
    held, found = load(u, s, sites_of(p["shape"]), *made(tuple(p["shape"])))
    assert found == [] and held is not None
    laid = layout(u, p["shape"], held)
    start = State(*held.state)
    end, outs = rounds(step.tick, laid, start, [1] * s["ticks"])
    assert frame.same(rewind(step.untick, laid, end, outs), start) and not (end.a == start.a).all()


def test_the_time_gear_is_sourced_by_every_trains_rho_plus_3p_and_not_by_the_heads_trace():
    """J at the time gear is -2 value . force - D value . value summed over every row of the file's trains (David, #2187
    6488709540), D the row's spring at rest, light's 0; the head's channel, D value . value alone, is the mutant."""
    _, _, layout = built(massive=True)
    row, n = layout.ruler.row, layout.nb.shape[1]
    s = world(np.random.default_rng(7), layout, np.zeros(n, dtype=object))
    s.b[row] = 0
    force, j = step.sources(
        layout._replace(gearing=step.ruled(layout.gearing, layout.ruler, s.b, s.a, s.a)), s
    )
    rest = layout.gearing.spring[:row, 0]
    dot = sum(s.a[x] * force[x] for x in range(row))
    squares = sum(rest[x] * s.a[x] * s.a[x] for x in range(row))
    assert (j[row] == -(dot + dot) - squares).all() and rest[0] == 0 and rest[-1] != 0
    assert not (j[row] == squares).all() and not (j[row] == -squares).all()
