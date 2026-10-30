"""David's probe for open step 4: the whole click as stage 7a's own drive carry, the take by the coupling, the lay into
the first free slot under the cap, the books, the run back, and the decoder's reading.

usage: python3 -I click_probe.py <a copy of the tensor24 src at 298bec5d8>

The world: a ring of 8 Node-clocks (shape 8 x 1 x 1). Rows: light, a Gaussian A1 hand (rows 0 and 1, the doubler's hold,
grip W / 6 per Mesh); the channel (row 2, an A1 gear with no grip, no spring and no kick, whose drive carries the
coupling row's source); the matter train's m = 2 slots (rows 3 and 4, rows 5 and 6), each a Gaussian hand with a spring
and no grip (a bound quantum stands at one Node-clock). The coupling row: J_channel = g (light_re light_re + light_im
light_im), the intensity, one gather and one product per term (the plan's contract). Stage 7a's tick runs unchanged;
the click layer reads the act's own drive quotient q on the start state and writes after the tick:
  - the lay: slot j at a Node-clock takes the child where it is free and fewer than q free slots stand before it,
    c_j = free_j nonneg(q - 1 - SUM_{i<j} free_i), free_j = nonneg(-(the slot's a a + b b summed)), whethers alone;
  - the books (the plan's e per hand): the giver's windings (light) fall by the laid count, the receiver's (matter)
    rise by it; the channel's fine tooth r_d is the fraction in transit, held by the receiver and owed by the giver
    (signed, law 8);
  - the out: the m bits c_j per Node-clock, which the run back reads.
Every integer is a Python integer; no float enters the act or the books (the setting's plane wave alone is rounded
from floats once, before the first tick).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import numpy as np  # noqa: E402

from tensor24.algebra.carry import carry, home, nonneg  # noqa: E402
from tensor24.decoder import books, records  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, State  # noqa: E402

GAMMA = 1000
N = 8
ROWS = 7
LIGHT, CHANNEL = (0, 1), 2
SLOTS = ((3, 4), (5, 6))
M = len(SLOTS)
T = 4_000_000  # the channel's teeth, the winding the click carries at (above the largest J, so q is 0 or 1)
G = 1  # the coupling's strength
CHILD_A, CHILD_B = (300, 400), (320, 384)  # the laid hand's now and before on its two rows
TICKS = 300
OUT = Path(__file__).with_suffix(".txt")


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


def world():
    nb = board((N, 1, 1))
    grip = obj(np.zeros((ROWS, 3 * N), dtype=object))
    grip[LIGHT[0], :N] = grip[LIGHT[1], :N] = 100  # the x Meshes; s grip / W = 100 / 600 = 1/6
    w = column([600, 600, 1, 900, 900, 900, 900])
    spring = column([0, 0, 0, 9, 9, 9, 9])
    kick = column([1, 1, 0, 1, 1, 1, 1])
    teeth = column([1, 1, T, 1, 1, 1, 1])
    gearing = Gearing(w, w, 1, spring, kick, teeth)
    first, second = np.array([LIGHT[0], LIGHT[1]], np.intp), np.array([LIGHT[0], LIGHT[1]], np.intp)
    plan = Plan(first, second, obj([G, G]), np.array([CHANNEL, CHANNEL], np.intp))
    layout = Layout(nb, meshes_of(nb), grip, gearing, plan, obj(np.full((1, N), GAMMA)), GAMMA)
    a = obj(np.zeros((ROWS, N), dtype=object))
    b = obj(np.zeros((ROWS, N), dtype=object))
    for x in range(N):  # a plane wave on the ring, k = 2 pi / 8, laid as integers
        phase, back = 2 * np.pi * x / N, 2 * np.pi * x / N - 0.3133
        a[LIGHT[0], x], a[LIGHT[1], x] = int(round(1000 * np.cos(phase))), int(round(1000 * np.sin(phase)))
        b[LIGHT[0], x], b[LIGHT[1], x] = int(round(1000 * np.cos(back))), int(round(1000 * np.sin(back)))
    go = obj(np.zeros((ROWS, N), dtype=object))
    r = home(w + 0 * a, go)  # every fine tooth at its home
    zeros = obj(np.zeros((ROWS, N), dtype=object))
    one = obj(np.zeros((1, N), dtype=object))
    return layout, State(a, b, r, go, zeros, one, one.copy(), one.copy())


def equal(s, t):
    return all(np.array_equal(x, y) for x, y in zip(s, t, strict=True))


def quotient(layout, s):
    """The act's own drive quotient and kept on the start state, as step.tick computes them."""
    _, j = step.sources(layout, s)
    q, kept = step.drive(j, layout.gearing.drive, s.rd)
    return q, kept, j


def frees(s):
    """free_j per slot and Node-clock: 1 where the slot's two rows hold 0 in now and before, by one whether."""
    return [nonneg(-sum(s.a[row] * s.a[row] + s.b[row] * s.b[row] for row in slot)) for slot in SLOTS]


def click(s, q, cap=True):
    """The lay into the first free slots and its out; cap=False is the mutant that lays past the cap."""
    free = frees(s)
    before = 0 * q
    marks = []
    for j in range(M):
        mark = (free[j] if cap else 1) * nonneg(q - 1 - (before if cap else j))
        marks.append(mark)
        before = before + free[j]
    a, b = s.a.copy(), s.b.copy()
    for slot, mark in zip(SLOTS, marks, strict=True):
        for row, ca, cb in zip(slot, CHILD_A, CHILD_B, strict=True):
            a[row], b[row] = a[row] + mark * ca, b[row] + mark * cb
    return s._replace(a=a, b=b), marks


def unclick(s, marks):
    a, b = s.a.copy(), s.b.copy()
    for slot, mark in zip(SLOTS, marks, strict=True):
        for row, ca, cb in zip(slot, CHILD_A, CHILD_B, strict=True):
            a[row], b[row] = a[row] - mark * ca, b[row] - mark * cb
    return s._replace(a=a, b=b)


def gear_wind(s):
    """Each train's wind on the gears, twice the leapfrog's kept form summed over the board: light, then matter."""
    layout, _ = world()
    w, spring = layout.gearing.w, layout.gearing.spring
    out = []
    for rows in ((LIGHT,), SLOTS):
        total = 0
        for group in rows:
            for row in group:
                a, b = s.a[row], s.b[row]
                total += sum(2 * w[row, 0] * (a - b) * (a - b) + 2 * spring[row, 0] * a * b)
                if row in LIGHT:
                    for sign in (1, -1):
                        aj, bj = np.roll(a, -sign), np.roll(b, -sign)
                        total += sum(100 * (a - aj) * (b - bj))
        out.append(total)
    return np.array(out, dtype=object)


def holding(train, windings, kept):
    return {"train": train, "windings": [int(w) for w in windings], "kept": [int(k) for k in kept]}


def run(ticks, stock, cap=True, drop_remainder=False, drop_take=False, no_out=False):
    layout, s = world()
    start = s
    e_light, e_matter = obj(np.full(N, stock, dtype=object)), obj(np.zeros(N, dtype=object))
    books0 = (e_light.copy(), e_matter.copy())
    lines, ledger, outs = [], [], []
    record = {"same": 0, "telescope": True, "most": 0, "refused": 0, "gears": np.zeros(2, dtype=object)}
    sums = obj(np.zeros(N, dtype=object))
    clicks = obj(np.zeros(N, dtype=object))
    rd0 = s.rd[CHANNEL].copy()
    totals = set()
    below = 0
    for t in range(1, ticks + 1):
        q_all, kept, j = quotient(layout, s)
        after, out = step.tick(layout, s, 1)
        record["same"] += int(np.array_equal(kept, after.rd))
        if drop_remainder:
            rd = after.rd.copy()
            rd[CHANNEL] = 0 * rd[CHANNEL]
            after = after._replace(rd=rd)
        q = q_all[CHANNEL]
        laid_state, marks = click(after, q, cap)
        laid = sum(marks)
        sums, clicks = sums + j[CHANNEL], clicks + q
        record["refused"] += int(sum(q - laid))
        rd_before, rd_after = s.rd[CHANNEL], laid_state.rd[CHANNEL]
        light_before, matter_before = e_light.copy(), e_matter.copy()
        if not drop_take:
            e_light = e_light - laid
        e_matter = e_matter + laid
        below += int(sum(nonneg(-e_light - 1)))
        totals.add(int(sum(e_light + e_matter)))
        record["most"] = max(record["most"], int(max(e_matter)))
        wholes, booked_lines = [], []
        for x in range(N):
            if laid[x]:
                wholes.append({
                    "kind": "whole", "round": t, "site": x, "count": t, "train": 0, "q": int(laid[x]),
                    "winding": T,
                    "taken": [holding(0, (light_before[x], e_light[x]), (-rd_before[x], -rd_after[x] - T * (q[x] - laid[x])))],
                    "laid": [holding(1, (matter_before[x], e_matter[x]), (rd_before[x], rd_after[x] + T * (q[x] - laid[x])))],
                    "ends": [], "children": [{"train": 1, "site": x, "sweep": 0, "push": [0, 0, 0], "moment": [0, 0, 0]}],
                })
            if q[x] - laid[x]:
                booked_lines.append({"kind": "books", "round": t, "site": x, "train": 0, "kept": int(T * (q[x] - laid[x]))})
        lines += wholes + booked_lines
        if laid.any():
            record["gears"] += gear_wind(laid_state) - gear_wind(after)
            ledger += [{"round": t, "at": "step", "train": 0, "wind": int(sum(light_before * T - rd_before))},
                       {"round": t, "at": "step", "train": 1, "wind": int(sum(matter_before * T + rd_before))},
                       {"round": t, "at": "clicks", "train": 0, "wind": int(sum(e_light * T - rd_after))},
                       {"round": t, "at": "clicks", "train": 1, "wind": int(sum(e_matter * T + rd_after))}]
        outs.append((out, marks, laid, layout))
        s = laid_state
    record["telescope"] = bool(np.array_equal(clicks * T + s.rd[CHANNEL] - rd0, sums))
    record["clicks"], record["laid"] = int(sum(clicks)), int(sum(len([1 for L in lines if L["kind"] == "whole"]) for _ in [0]))
    record["totals"], record["below"] = len(totals), below
    back = s
    e_l, e_m = e_light.copy(), e_matter.copy()
    for out, marks, laid, layout_ in reversed(outs):
        if no_out:  # the mutant run back that keeps no click bits: a slot full now is read as laid by this click
            occupied = [1 - f for f in frees(back)]
            marks = [o * nonneg(laid - 1 - i) for i, o in enumerate(occupied)]
        back = unclick(back, marks)
        back = step.untick(layout_, back, out)
        if not drop_take:
            e_l = e_l + laid
        e_m = e_m - laid
    record["back"] = equal(back, start) and np.array_equal(e_l, books0[0]) and np.array_equal(e_m, books0[1])
    return record, lines, ledger, s


def decode(lines, ledger, ticks, weighted, path):
    trains = [{"index": 0, "label": "light", "kinds": [0], "part": 2, "winding": T},
              {"index": 1, "label": "matter", "kinds": [0], "part": 2, "winding": T}]
    header = {"kind": "header", "record": "tensor24", "major": 1, "minor": 1, "sides": [N, 1, 1], "trains": trains}
    end = {"kind": "end", "rounds": ticks, "undone": 0, "exact": 1}
    path.write_text("".join(json.dumps(x) + "\n" for x in [header, *lines, end]))
    record, cause = records.read(str(path))
    if record is None:
        return f"not read: {cause}"
    plain = books.gained
    if weighted:
        winding = {t["index"]: t["winding"] for t in trains}
        books.gained = lambda hs: sum((h["windings"][1] - h["windings"][0]) * winding[h["train"]]
                                      + h["kept"][1] - h["kept"][0] for h in hs)
    try:
        verdict = books.row_15(record, ledger)
    finally:
        books.gained = plain
    return f"{verdict['kind']}: {verdict['cause']}"


def gear_wind_child():
    return 2 * 900 * sum((x - y) * (x - y) for x, y in zip(CHILD_A, CHILD_B)) + 2 * 9 * sum(x * y for x, y in zip(CHILD_A, CHILD_B))


def main():
    global T
    say = []
    rec, lines, ledger, final = run(TICKS, 1000)
    say.append(f"the law, {TICKS} ticks on a ring of {N}, m = {M} slots, the channel's teeth T = {T:,}:")
    say.append(f"  the click's q is the act's own drive quotient: the drive's kept equal to the tick's r_d at {rec['same']} of {TICKS} ticks")
    say.append(f"  the clicks counted {rec['clicks']} quotients; the telescoping SUM q T + r_d(end) - r_d(start) = SUM J at every Node-clock: {rec['telescope']}")
    whole = sum(1 for x in lines if x['kind'] == 'whole')
    back_lines = sum(1 for x in lines if x['kind'] == 'books')
    say.append(f"  laid {whole} hands, refused {rec['refused']} at full Node-clocks (each a Books line, laid back to the light)")
    say.append(f"  the cap: the most quanta booked at one Node-clock {rec['most']} (m = {M}); the books' total took {rec['totals']} value(s)")
    say.append(f"  the light's windings below 0 at {rec['below']} Node-clock ticks")
    say.append(f"  the run back through every click and tick to the start state and the start books: {rec['back']}")
    say.append(f"  the gears' wind moved by the clicks (twice the kept form, light then matter): {list(map(int, rec['gears']))}; "
               f"each laid hand's own is {int(gear_wind_child())}, so the light's gears are not unwound by the take")
    folder = Path(__file__).parent
    say.append(f"  the decoder as built (holdings summed unweighted): {decode(lines, ledger, TICKS, False, folder / 'record_plain.jsonl')}")
    say.append(f"  the decoder with each holding weighed by its train's winding: {decode(lines, ledger, TICKS, True, folder / 'record_weighted.jsonl')}")
    say.append(f"  a whole click as written: {json.dumps(next(x for x in lines if x['kind'] == 'whole'))}")
    say.append(f"  a Books line as written: {json.dumps(next((x for x in lines if x['kind'] == 'books'), {}))}")
    keep = T
    T = 400_000
    rec2, lines2, ledger2, _ = run(TICKS, 1000)
    say.append(f"the same world at the channel's teeth T = {T:,}, below the largest J, so one tick carries up to "
               f"{max(x['q'] for x in lines2 if x['kind'] == 'whole')} laid and more quotients:")
    say.append(f"  quotients {rec2['clicks']}, laid {sum(x['q'] for x in lines2 if x['kind'] == 'whole')}, refused {rec2['refused']}; "
               f"telescoping {rec2['telescope']}; most at one Node-clock {rec2['most']}; the books' total took {rec2['totals']} value(s); "
               f"run back {rec2['back']}")
    say.append(f"  the decoder, weighted: {decode(lines2, ledger2, TICKS, True, folder / 'record_teeth.jsonl')}")
    T = keep
    for name, kw in (("the remainder dropped (r_d set to 0 after each carry)", {"drop_remainder": True}),
                     ("the run back with no click bits in the out (a slot full now read as laid now)", {"no_out": True}),
                     ("the slot past the cap (laid without the free whether)", {"cap": False}),
                     ("the take dropped (the light's windings kept)", {"drop_take": True}),
                     ("the light laid with no windings to give", {"stock": 0})):
        args = {"stock": 1000, **kw}
        m_rec, m_lines, m_ledger, _ = run(TICKS, **args)
        say.append(f"the mutant, {name}:")
        say.append(f"  telescoping {m_rec['telescope']}; most at one Node-clock {m_rec['most']}; the books' total took "
                   f"{m_rec['totals']} value(s); the light below 0 at {m_rec['below']}; run back {m_rec['back']}")
        say.append(f"  the decoder, weighted: {decode(m_lines, m_ledger, TICKS, True, folder / 'record_mutant.jsonl')}")
    text = "\n".join(say) + "\n"
    OUT.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
