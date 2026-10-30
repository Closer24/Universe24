"""David's probe for the take on light's gears, way (b): one carry of the stride's linear term at the click's Node-clock,
the miss booked signed in light's kept, the replaced kept in the out.

usage: python3 -I takeb_probe.py <the tensor24 src at 298bec5d8>

The world is click_probe.py's: a ring of 8 Node-clocks; light, a Gaussian A1 hand on rows 0 and 1 (W 600, grip 100 per
Mesh, a plane wave of amplitude 1,000); the channel, row 2, whose drive carries the intensity g (re re + im im) at the
teeth T; the matter train's m = 2 slots, rows 3 and 4 and rows 5 and 6. Stage 7a's tick runs unchanged; the click layer
writes after the tick, on the post-tick state, at each Node-clock alone:
  - the lay, as click_probe.py has it, with one more whether: the light at the Node-clock must hold the children's sweep;
  - the take: where a child was laid, light's now slot moves by delta, two carries of the stride's linear term.
The sweep of a hand is Q = Im(conj(a) b) = a_re b_im - a_im b_re = Im(conj(a - b) b): linear in the stride, its gradient
in the now slot n = (b_im, -b_re). A child laid carries Q_child, so light owes laid Q_child. With the kept k, light's
signed debt at the Node-clock, the take writes delta_row = carry(-n_row (owed + k), |n|^2, |n|^2 div 2)'s quotient and
books k+ = owed + k + delta . n, so that Q_light + Q_matter - SUM k moves by 0 at every click, exactly. The out holds the
kept the click replaced, from which the run back reads delta again, since the take leaves the before slot unmoved.
Every integer is a Python integer; no float enters the act, the click or the books (the setting's waves alone are
rounded from floats once, before the first tick).
"""
import sys

sys.path.insert(0, sys.argv[1])
import numpy as np  # noqa: E402

from tensor24.algebra.carry import carry, nonneg  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, State  # noqa: E402

GAMMA = 1000
N = 8
ROWS = 7
LIGHT, CHANNEL = (0, 1), 2
SLOTS = ((3, 4), (5, 6))
M = len(SLOTS)
T = 4_000_000
G = 1
W_LIGHT, GRIP = 600, 100
CHILD_A, CHILD_B = (300, 400), (320, 384)  # the laid hand's now and before: re on the slot's first row, im on its second
Q_CHILD = CHILD_A[0] * CHILD_B[1] - CHILD_A[1] * CHILD_B[0]  # the child's sweep, -12,800
SIGN = 1 if Q_CHILD > 0 else -1  # read once at load from the child
TICKS = 300


def obj(x):
    return np.asarray(x, dtype=object)


def board(shape):
    xyz, sides = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    steps = [sign * axis for axis in np.eye(3, dtype=int) for sign in (1, -1)]
    return np.stack([np.ravel_multi_index(tuple((xyz + s[:, None]) % sides), shape) for s in steps])


def meshes_of(nb):
    axes, n = np.arange(len(nb)) // 2, nb.shape[1]
    own, theirs = axes[:, None] * n + np.arange(n)[None, :], axes[:, None] * n + nb
    return np.where((np.arange(len(nb)) % 2 == 0)[:, None], own, theirs)


def column(values):
    return obj(np.array(values, dtype=object).reshape(-1, 1))


def layout_of():
    nb = board((N, 1, 1))
    grip = obj(np.zeros((ROWS, 3 * N), dtype=object))
    grip[LIGHT[0], :N] = grip[LIGHT[1], :N] = GRIP
    w = column([W_LIGHT, W_LIGHT, 1, 900, 900, 900, 900])
    gearing = Gearing(w, w, 1, column([0, 0, 0, 9, 9, 9, 9]), column([1, 1, 0, 1, 1, 1, 1]), column([1, 1, T, 1, 1, 1, 1]))
    plan = Plan(np.array(LIGHT, np.intp), np.array(LIGHT, np.intp), obj([G, G]), np.array([CHANNEL, CHANNEL], np.intp))
    return Layout(nb, meshes_of(nb), grip, gearing, plan, obj(np.full((1, N), GAMMA)), GAMMA)


def start_of(light_now, light_before):
    """The start state from light's now and before, (re, im) per Node-clock; every fine tooth at its home."""
    layout = layout_of()
    a, b = obj(np.zeros((ROWS, N), dtype=object)), obj(np.zeros((ROWS, N), dtype=object))
    for x in range(N):
        a[LIGHT[0], x], a[LIGHT[1], x] = light_now[x]
        b[LIGHT[0], x], b[LIGHT[1], x] = light_before[x]
    go = obj(np.zeros((ROWS, N), dtype=object))
    r = (layout.gearing.w + 0 * a - go) // 2
    zeros, one = obj(np.zeros((ROWS, N), dtype=object)), obj(np.zeros((1, N), dtype=object))
    return State(a, b, r, go, zeros, one, one.copy(), one.copy())


def plane_wave(amplitude=1000):
    now, before = [], []
    for x in range(N):
        phase, back = 2 * np.pi * x / N, 2 * np.pi * x / N - 0.3133
        now.append((int(round(amplitude * np.cos(phase))), int(round(amplitude * np.sin(phase)))))
        before.append((int(round(amplitude * np.cos(back))), int(round(amplitude * np.sin(back)))))
    return now, before


def sweep(s, rows):
    return s.a[rows[0]] * s.b[rows[1]] - s.a[rows[1]] * s.b[rows[0]]


def sweeps(s, kept):
    """The second reading in the sweep: Q_light + Q_matter - SUM kept over the board."""
    return sum(sweep(s, LIGHT)) + sum(sweep(s, SLOTS[0])) + sum(sweep(s, SLOTS[1])) - sum(kept)


def frees(s):
    return [nonneg(-sum(s.a[row] * s.a[row] + s.b[row] * s.b[row] for row in slot)) for slot in SLOTS]


def payable(s, kept):
    """How many children the light at each Node-clock can pay: (SIGN (Q_light - kept)) div |Q_child|, one carry."""
    q, _ = carry(SIGN * (sweep(s, LIGHT) - kept), abs(Q_CHILD), 0)
    return q


def lay(s, q, kept, pay=True):
    """The lay into the first free slots, as click_probe.py has it, the j-th child also within the light's payable count."""
    free = frees(s)
    p = payable(s, kept)
    before = 0 * q
    marks = []
    for j in range(M):
        marks.append(free[j] * nonneg(q - 1 - before) * (nonneg(p - 1 - before) if pay else 1))
        before = before + free[j]
    a, b = s.a.copy(), s.b.copy()
    for slot, mark in zip(SLOTS, marks, strict=True):
        for row, ca, cb in zip(slot, CHILD_A, CHILD_B, strict=True):
            a[row], b[row] = a[row] + mark * ca, b[row] + mark * cb
    return s._replace(a=a, b=b), marks


def unlay(s, marks):
    a, b = s.a.copy(), s.b.copy()
    for slot, mark in zip(SLOTS, marks, strict=True):
        for row, ca, cb in zip(slot, CHILD_A, CHILD_B, strict=True):
            a[row], b[row] = a[row] - mark * ca, b[row] - mark * cb
    return s._replace(a=a, b=b)


def delta_of(s, laid, kept):
    """The tangential form, for comparison: light's now slot moved along the sweep's gradient n = (b_im, -b_re)."""
    on = nonneg(laid - 1)
    owed = laid * Q_CHILD
    n_re, n_im = s.b[LIGHT[1]], -s.b[LIGHT[0]]
    norm = n_re * n_re + n_im * n_im
    d = norm + nonneg(-norm)  # one whether: a still before slot reads the teeth 1, where n is 0 and so delta is 0
    d_re, _ = carry(-n_re * (owed + kept), d, d // 2)
    d_im, _ = carry(-n_im * (owed + kept), d, d // 2)
    zero = 0 * d_re
    return [on * d_re, on * d_im, zero, zero]


def radial_of(s, laid, kept):
    """Way (b): light's now and before at the Node-clock each shrink by e = (owed + k) / (2 Q), one carry per row.
    Q -> (1 - e)^2 Q, whose linear term 2 e Q is what light owes; the quadratic part and the rounding go to the kept."""
    on = nonneg(laid - 1)
    owed = laid * Q_CHILD
    held = SIGN * sweep(s, LIGHT)  # the light's sweep in the child's sense, above 0 where the lay let a child through
    d = 2 * held
    d = nonneg(d - 1) * d + (1 - nonneg(d - 1))  # the teeth at least 1 by one whether; the lay's pay whether keeps d >= 2 |owed|
    part = SIGN * (owed + kept)
    out = []
    for slot in (s.a, s.b):
        for row in LIGHT:
            dq, _ = carry(-slot[row] * part, d, d // 2)
            out.append(on * dq)
    return out  # the now slot's two rows, then the before slot's


def take(s, laid, kept, book=True, form="radial"):
    """Light's slots at the Node-clock move by the take's write where children were laid; the kept books the miss, signed."""
    write = (radial_of if form == "radial" else delta_of)(s, laid, kept)
    a, b = s.a.copy(), s.b.copy()
    a[LIGHT[0]], a[LIGHT[1]] = a[LIGHT[0]] + write[0], a[LIGHT[1]] + write[1]
    b[LIGHT[0]], b[LIGHT[1]] = b[LIGHT[0]] + write[2], b[LIGHT[1]] + write[3]
    t = s._replace(a=a, b=b)
    on, owed = nonneg(laid - 1), laid * Q_CHILD
    moved = sweep(t, LIGHT) - sweep(s, LIGHT)
    booked = owed + kept + moved if book else 0 * kept
    return t, on * booked + (1 - on) * kept, write


def untake(s, write):
    """The take run back from the write the out holds, as the head's rewind restores a take from its line."""
    a, b = s.a.copy(), s.b.copy()
    a[LIGHT[0]], a[LIGHT[1]] = a[LIGHT[0]] - write[0], a[LIGHT[1]] - write[1]
    b[LIGHT[0]], b[LIGHT[1]] = b[LIGHT[0]] - write[2], b[LIGHT[1]] - write[3]
    return s._replace(a=a, b=b)


def wind_light(s):
    """Light's kept form summed over the ring: W |a - b|^2 + SUM over the Meshes of the grip (da . db), both rows."""
    total = 0
    for row in LIGHT:
        a, b = s.a[row], s.b[row]
        total += sum(W_LIGHT * (a - b) * (a - b)) + sum(GRIP * (a - np.roll(a, -1)) * (b - np.roll(b, -1)))
    return total


def equal(s, t):
    return all(np.array_equal(x, y) for x, y in zip(s, t, strict=True))


def run(start, ticks, pay=True, book=True, keep_out=True, take_on=True, form="radial"):
    layout = layout_of()
    s, kept = start, obj(np.zeros(N, dtype=object))
    e_light, e_matter = obj(np.full(N, 1000, dtype=object)), obj(np.zeros(N, dtype=object))
    outs, states = [], [start]
    rep = {"energy_taken": 0, "clicks": 0, "laid": 0, "refused": 0, "write_moves": set(), "kept_max": 0, "totals": set(), "act_moves": [],
           "light_taken": 0, "children": 0, "click_ticks": 0}
    for _ in range(ticks):
        before_sum = sweeps(s, kept)
        _, j = step.sources(layout, s)
        q_all, _ = step.drive(j, layout.gearing.drive, s.rd)
        after, out = step.tick(layout, s, 1)
        rep["act_moves"].append(int(sweeps(after, kept) - before_sum))
        q = q_all[CHANNEL]
        laid_state, marks = lay(after, q, kept, pay=pay)
        laid = sum(marks)
        rep["clicks"] += int(sum(q))
        rep["laid"] += int(sum(laid))
        rep["refused"] += int(sum(q - laid))
        kept_before = kept.copy()
        if take_on:
            taken, kept, write = take(laid_state, laid, kept, book=book, form=form)
        else:
            taken, write = laid_state, [0 * kept] * 4
        if laid.any():
            rep["click_ticks"] += 1
            rep["write_moves"].add(int(sweeps(taken, kept) - sweeps(after, kept_before)))
            rep["light_taken"] += int(sum(sweep(taken, LIGHT)) - sum(sweep(laid_state, LIGHT)))
            rep["energy_taken"] += int(wind_light(laid_state) - wind_light(taken))
            rep["children"] += int(sum(laid) * Q_CHILD)
        rep["kept_max"] = max(rep["kept_max"], int(max(abs(k) for k in kept)))
        e_light, e_matter = e_light - laid, e_matter + laid
        rep["totals"].add(int(sum(e_light + e_matter)))
        outs.append((out, marks, laid, write if keep_out else [0 * kept] * 4))
        s = taken
        states.append(s)
    rep["final"], rep["kept_final"], rep["states"] = s, kept, states
    back = s
    for out, marks, laid, write in reversed(outs):
        if take_on:
            back = untake(back, write)
        back = unlay(back, marks)
        back = step.untick(layout, back, out)
    rep["back"] = equal(back, start)
    return rep


def image(state):
    """The half turn about the y axis, one of the 24, on the ring: x -> -x, the A1 rows unturned."""
    perm = [(-x) % N for x in range(N)]
    return State(*[obj(np.asarray(f)[:, perm]) for f in state])


def energy_form_at(start):
    """For comparison: the take written against the light's kept form instead of its sweep, at site 0 of the start,
    for one child (its kept form 2,836,800): delta by the form's linear term, and the quadratic part it leaves."""
    owed = (900 * 656 + 9 * 249_600)
    g = []
    for row in LIGHT:
        a, b = start.a[row], start.b[row]
        g.append(2 * W_LIGHT * (a - b) + GRIP * ((b - np.roll(b, -1)) + (b - np.roll(b, 1))))
    norm = g[0] * g[0] + g[1] * g[1]
    d = norm + nonneg(-norm)
    deltas = [carry(-gr * owed, d, d // 2)[0] for gr in g]
    linear = sum(gr * dl for gr, dl in zip(g, deltas, strict=True))
    quadratic = W_LIGHT * sum(dl * dl for dl in deltas)
    return int(owed), [int(x[0]) for x in deltas], int(linear[0]), int(quadratic[0])


def main():
    say = []
    now, before = plane_wave()
    start = start_of(now, before)
    q_start, e_start = int(sum(sweep(start, LIGHT))), int(wind_light(start))
    for form in ("radial", "tangential"):
        rep = run(start, TICKS, form=form)
        name = "way (b), the radial take" if form == "radial" else "the tangential take, for comparison"
        say.append(f"{name}, {TICKS} ticks on a ring of {N}:")
        if form == "radial":
            say.append(f"  the child's sweep Q_child = {Q_CHILD:,}; the light's sweep at the start {q_start:,}, "
                       f"{int(sweep(start, LIGHT)[0]):,} at site 0; its kept form {e_start:,}, so {-e_start / q_start:,.1f} per unit of sweep")
            say.append(f"  quotients {rep['clicks']}, laid {rep['laid']} at {rep['click_ticks']} click ticks, refused {rep['refused']} "
                       f"(laid back, a Books line each)")
        say.append(f"  the click's write moved Q_light + Q_matter - SUM kept by {sorted(rep['write_moves'])} at every click tick")
        say.append(f"  light's sweep moved by {rep['light_taken']:,} at the takes, the children carry {rep['children']:,}; "
                   f"the kept at the end {list(map(int, rep['kept_final']))}, at most {rep['kept_max']:,} in size at any tick")
        say.append(f"  light's kept form fell by {rep['energy_taken']:,} at the takes: {rep['energy_taken'] / rep['light_taken']:,.1f} "
                   f"per unit of sweep taken, against its own {-e_start / q_start:,.1f}; the children hold {2_836_800 / -Q_CHILD:,.1f} "
                   f"per unit of sweep, so the sweep balances and the energy only at resonance")
        if form == "radial":
            acts = rep["act_moves"]
            say.append(f"  between the clicks the act moves the same sum by Rule3's torques alone: at most {max(abs(x) for x in acts):,} "
                       f"a tick, {sum(acts):,} over the run")
            say.append(f"  the books' windings: their total took {len(rep['totals'])} value(s)")
            say.append(f"  the run back through every take, lay and tick, from the out's write: {rep['back']}")
            img = run(start_of([now[(-x) % N] for x in range(N)], [before[(-x) % N] for x in range(N)]), TICKS)
            same = all(equal(image(x), y) for x, y in zip(rep["states"], img["states"], strict=True))
            say.append(f"  the 24: the run of the turned start equals the turned run at every one of {TICKS + 1} states: {same}")
            for mname, kw in (("the miss dropped (the kept not booked)", {"book": False}),
                              ("the take dropped (no write on light's gears, the click probe's gap)", {"take_on": False}),
                              ("the out without the take's write", {"keep_out": False})):
                m = run(start, TICKS, **kw)
                moves = sorted(m["write_moves"])
                say.append(f"  the mutant, {mname}: the click's write moved the sum by {len(moves)} value(s) from {moves[0]:,} "
                           f"to {moves[-1]:,}; run back {m['back']}")
    owed, deltas, linear, quadratic = energy_form_at(start)
    say.append(f"the energy form, for comparison, one child at site 0 of the start: owed {owed:,} of the kept form; delta "
               f"{deltas}; its linear term {linear:,}; the quadratic part W |delta|^2 = {quadratic:,} left to the kept")
    say.extend(grangier())
    print("\n".join(say))


def grangier():
    """One child's sweep of light, split half and half over the Node-clocks A = 0 and B = 4, and whole at A alone."""
    out = []
    amp = 145  # |Q| = amp^2 sin(0.3133), about half the child's 12,800 at each of A and B
    for name, sites, scale in (("split, half at A and half at B", (0, 4), amp), ("whole at A", (0,), 204)):
        now, before = [(0, 0)] * N, [(0, 0)] * N
        for x in sites:
            now[x] = (scale, 0)
            before[x] = (int(round(scale * np.cos(-0.3133))), int(round(scale * np.sin(-0.3133))))
        start = start_of(now, before)
        q0, e0 = int(sum(sweep(start, LIGHT))), int(wind_light(start))
        rep = run(start, 160)
        q1, e1 = int(sum(sweep(rep["final"], LIGHT))), int(wind_light(rep["final"]))
        out.append(f"one quantum, {name}: light's sweep {q0:,} against the child's {Q_CHILD:,}; quotients {rep['clicks']}, "
                   f"laid {rep['laid']}; light's sweep {q0:,} -> {q1:,} and its kept form {e0:,} -> {e1:,}; the kept at most "
                   f"{rep['kept_max']:,}; the click's write moved the sum by {sorted(rep['write_moves'])}; run back {rep['back']}")
        lows = [int(min(sweep(x, LIGHT) * SIGN)) for x in rep["states"]]
        highs = [int(max(sweep(x, LIGHT) * SIGN)) for x in rep["states"]]
        out.append(f"  its sweep density in the child's sense, over the Node-clocks and ticks, from {min(lows):,} to {max(highs):,}: "
                   f"it takes both signs, so a Node-clock alone cannot read whether one quantum stands on the board")
    return out


if __name__ == "__main__":
    main()
