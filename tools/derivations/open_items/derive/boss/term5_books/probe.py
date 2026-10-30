"""Term 5 in the books' form at dial 2 on the built loader (the Boss's code writer, 2026-10-30; the night's PLAN.md B2b):
the deriver's probe_f (g2_t5/TERM5_FIFTH.md) rerun on plans.pushing and load.geared as built, the clock reading the 00
slot at k0 = Spokes x senses and the 00 push reading the momenta of every row the push does not land on (the square's 00
and ii rows left out, the Boss's ruling of 20:4x UTC): the matter's energy loss against the metric's gain by windows, the
run back with the drive's tooth moving on the pushed rows, light's h_xx / h_00, and on the well world the sign, the run
back over its 128 rounds and the price (the metric's own kinetic share against the matter's); whole numbers and Rule3's
carry alone, the universes through the loader, no train declared here.

Clock: the clock's gear takes what the matter's momentum gives up as its teeth move, the Mesh's ii gear what the Mesh's
stretch gives up as its grip moves; a gear nothing reads takes nothing.
Algebra: the energy per gear is the physicist's 16H = 2 W M_in M_out div (D_in D_out) + 4 SUM over the Spokes of
grip (neighbour - own)^2 (the leapfrog's invariant at fixed reads), by rows and by windows of 5 rounds over 30: the
matter's loss (its first window's mean less its last's), the metric's gain, gain / loss in permille and in parts per
million; the momenta in whole turns of the rest dial, sigma = split(M, 2 rest) as step.stress reads them, the round's
own sigma_out the next state's sigma_in.
Board: cubes of 3 (dust: a hand gliding at a stride of 10^13), 3 by 3 by 6 (the tent, a slope of 10^17 a site, free
and held: its matter's rows reset every round), 12 by 3 by 3 (the bump of peak 10^16, free and held); the drawn lay of
the deriver's probe_e for the run back; the well world's own files (examples/tensor24-well) for the rest.
Clicks: n/a: the clicks' books are G5's.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/term5_books/probe.py; its output is probe.txt beside it.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT.joinpath("src")))

from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

EXAMPLE = ROOT.joinpath("examples", "tensor24")
WELL = ROOT.joinpath("examples", "tensor24-well")
STRIDE, SLOPE, PEAK = 10**13, 10**17, 10**16  # the deriver's dust, tent and bump
ROUNDS, WIDTH, BACK = 30, 5, 12
DERIVER = "the deriver at k0 = 1: dust 1000, the free tent 1133, the held tent 1000, the free bump 1041, the held bump 1000"


def recurrence(seed):
    """Whole numbers from a fixed recurrence, each step one carry: no random module (the deriver's)."""
    v = seed
    while True:
        _, v = carry(v * 6364136223846793005 + 1442695040888963407, 1 << 64, 0)
        yield v


def drawn(src, low, high):
    """A whole number in [low, high] from the recurrence's high bits, by two carries."""
    top, _ = carry(next(src), 1 << 33, 0)
    _, x = carry(top, high - low + 1, 0)
    return low + x


def coords(x, shape):
    """A site's three coordinates by two carries, z the fastest (runner/board.py's order)."""
    _, sy, sz = shape
    rest, z = carry(x, sz, 0)
    cx, cy = carry(rest, sy, 0)
    return cx, cy, z


def world(universe, shape, lay, seed=6):
    """The universe on the board of the shape, its gears laid by lay(train, component, site, src, shape) -> (a, b, s)."""
    sites = sites_of(shape)
    made = main.made(loading.star(len(shape)))
    empty, _ = loading.load(universe, {"version": 1, "gears": []}, sites, *made)
    src, gears = recurrence(seed), []
    for t in range(len(empty.trains)):
        train = empty.trains[t]
        for component in range(train.rows()):
            for x in range(sites):
                a, b, s = lay(train, component, x, src, shape)
                gears.append([t, component, x, a, b, s])
    return loaded(universe, shape, gears)


def loaded(universe, shape, gears):
    """The files on the engine: the held trains, the layout and the state laid; no departure of the lay."""
    made = main.made(loading.star(len(shape)))
    held, laid = loading.load(universe, {"version": 1, "gears": gears}, sites_of(shape), *made)
    assert not laid, laid
    return held, main.layout(universe, shape, held), State(*held.state)


def slots(held):
    """The square's rows (00, [0i], [ii], [jk]) and the matter's rows."""
    first = next(int(held.trains[t].first) for t in range(len(held.trains)) if held.trains[t].square)
    rows = int(held.trains.size.sum())
    square = list(range(first, first + 10))
    matter = [r for r in range(rows) if r not in square]
    return first, [first + 1 + i for i in range(3)], [first + 4 + i for i in range(3)], [first + 7 + i for i in range(3)], matter


def gliding(train, component, x, src, shape):
    return (10**14, 10**14 - STRIDE, 0) if (not train.square and component == 0) else (0, 0, 0)


def tent(train, component, x, src, shape):
    z = coords(x, shape)[2]
    a = SLOPE * (z if z <= 3 else 6 - z)
    return (a, a, 0) if (not train.square and component == 0) else (0, 0, 0)


def bump(train, component, x, src, shape):
    cx = coords(x, shape)[0]
    u = cx - 6
    inside = int(-4 < u < 4)
    q, _ = carry(PEAK * (16 - u * u) ** 2, 256, 0)
    return (inside * q, inside * q, 0) if (not train.square and component == 0) else (0, 0, 0)


def moving(train, component, x, src, shape):
    """The deriver's drawn lay (probe_e): strides in [-30, 30]; the 00 slot in [0, 10^6], the 0i slots in [-1000, 1000] standing."""
    if train.square:
        if component == 0:
            return drawn(src, 0, 10**6), drawn(src, 0, 10**6), 0
        if component in (1, 2, 3):
            v = drawn(src, -1000, 1000)
            return v, v, 0
        return 0, 0, 0
    a = drawn(src, -1000, 1000)
    return a, a - drawn(src, -30, 30), 0


def momentum(layout, st):
    wa, wb = step.dials(layout, st)
    return 2 * (wa + wb) * (st.a - st.b) + st.r


def sigma(layout, st):
    """Every gear's momentum in whole turns of the rest dial, as step.stress reads sigma_in: split(M, 2 rest) at the senses."""
    senses = step.halves(layout)
    q, _ = step.split(momentum(layout, st), senses * layout.gearing.rest, senses)
    return q


def energy16(layout, now, nxt):
    """The physicist's 16H per row, summed over the board, at the state now (his probe_b)."""
    wa, wb = step.dials(layout, now)
    wa1, wb1 = step.dials(layout, nxt)
    kin, _ = carry(2 * wa * momentum(layout, now) * momentum(layout, nxt), (wa + wb) * (wa1 + wb1), 0)
    grips = step.grips(layout, now)[0]
    diff = now.a[:, layout.nb] - now.a[:, None, :]
    return (kin + 4 * (grips[None, :, :] * diff * diff).sum(axis=1)).sum(axis=1)


def per(num, den, unit):
    """num / den in parts of the unit by one carry, the sign carried on num; den at least 1 in magnitude."""
    if den < 0:
        den, num = -den, -num
    q, _ = carry(num * unit, den, 0)
    return q


def books(layout, s0, groups, held=None):
    """The window means of 16H by group over the rounds: the matter's loss, the metric's gain; held: the matter's rows reset to the lay every round (a static source)."""
    states = [s0]
    for _ in range(ROUNDS + 1):
        s = step.tick(layout, states[-1])
        if held is not None:
            a, b, r = s.a.copy(), s.b.copy(), s.r.copy()
            a[held], b[held], r[held] = s0.a[held], s0.b[held], s0.r[held]
            s = State(a, b, r, s.rd, s.k)
        states.append(s)
    e = [energy16(layout, states[n], states[n + 1]) for n in range(1, ROUNDS + 1)]
    means = []
    for start in range(0, ROUNDS, WIDTH):
        window = e[start : start + WIDTH]
        row = []
        for rows in groups.values():
            q, _ = carry(sum(int(x[rows].sum()) for x in window), WIDTH, 0)
            row.append(q)
        means.append(row)
    first, last = means[0], means[-1]
    loss, gains = first[0] - last[0], [last[i] - first[i] for i in range(1, len(first))]
    end = states[ROUNDS]
    strides = {name: int(abs(end.a[rows] - end.b[rows]).max()) for name, rows in groups.items()}
    return loss, gains, strides


def the_books(say, universe):
    """1: the matter's loss against the metric's gain by windows on the deriver's five cases."""
    cases = (
        (f"dust: a hand gliding at the stride {STRIDE} on 3^3", [3, 3, 3], gliding, False),
        (f"the tent: a slope of {SLOPE} a site along z on 3 x 3 x 6, free", [3, 3, 6], tent, False),
        ("the tent held (its matter's rows reset every round, a static source)", [3, 3, 6], tent, True),
        (f"the bump: peak {PEAK} along x on 12 x 3 x 3, free (light, splitting)", [12, 3, 3], bump, False),
        ("the bump held", [12, 3, 3], bump, True),
    )
    for name, shape, lay, hold in cases:
        held, layout, s0 = world(universe, shape, lay)
        s00, s0i, sii, sjk, matter = slots(held)
        groups = {"matter": np.array(matter), "00": np.array([s00]), "ii": np.array(sii), "0i+jk": np.array(s0i + sjk)}
        loss, gains, strides = books(layout, s0, groups, np.array(matter) if hold else None)
        gain = sum(gains)
        ratio = f"{per(gain, loss, 1000)} permille, {per(gain, loss, 10**6)} ppm" if loss else "-"
        say(
            f"1. {name}: strides at the end {strides}; the matter's loss {loss}, the metric's gain {gain} (00 {gains[0]},"
            f" ii {gains[1]}, 0i+jk {gains[2]}); gain / loss {ratio}"
        )
    say(f"   ({DERIVER}; here the clock reads the 00 slot at k0 = Spokes x senses as built)")


def the_drawn_run_back(say, universe):
    """2: the run back on the deriver's drawn lay, the drive's tooth moving on the pushed rows."""
    held, layout, s0 = world(universe, [3, 3, 3], moving)
    s00, s0i, sii, sjk, matter = slots(held)
    states = [s0]
    for _ in range(BACK):
        states.append(step.tick(layout, states[-1]))
    back = sum(all(np.array_equal(x, y) for x, y in zip(step.untick(layout, states[n + 1]), states[n], strict=True)) for n in range(BACK))
    end = states[-1]
    for _ in range(BACK):
        end = step.untick(layout, end)
    whole = all(np.array_equal(x, y) for x, y in zip(end, s0, strict=True))
    dials = sorted(set(layout.gearing.drive[[s00, *sii], 0].tolist())), sorted(set(np.delete(layout.gearing.drive[:, 0], [s00, *sii]).tolist()))
    say(
        f"2. the run back on the drawn lay (strides within 30, the 00 slot within 10^6, the 0i slots standing within 1000), the drive's teeth"
        f" {dials[0]} on the 00 and ii rows and {dials[1]} elsewhere: untick(tick s) = s in {back} of {BACK} rounds, the start returned after"
        f" {BACK} rounds back: {whole}; the drive's tooth r_d after one round not 0 at {int((states[1].rd != 0).sum())} gears of {states[1].rd.size}"
    )


def the_gamma(say, universe):
    """3: light's h_xx / h_00 on the bump after the rounds: -S ii_x / (k0 c00), S = Spokes x senses."""
    held, layout, s = world(universe, [12, 3, 3], bump)
    s00, s0i, sii, sjk, matter = slots(held)
    scale, _ = carry(len(layout.spokes) * len(layout.spokes), len(layout.spokes[0]), 0)
    k0 = int(layout.clock.factor.max())
    for _ in range(ROUNDS):
        s = step.tick(layout, s)
    c, ii = int(s.a[s00].sum()), [int(s.a[r].sum()) for r in sii]
    say(
        f"3. light's gamma, the bump after {ROUNDS} rounds: the clock reads the 00 slot at k0 = {k0} (Spokes x senses = {scale});"
        f" the board sums c00 {c}, ii {ii}; h_xx / h_00 = -{scale} ii_x / (k0 c00) = {per(-scale * ii[0], k0 * c, 1000) if c else '-'} permille"
        f" (GR's light 1000; the deriver measured 915 at k0 = 12 and 131,837 at k0 = 1)"
    )


def well_files():
    universe = json.loads(WELL.joinpath("universe.json").read_text(encoding="utf-8"))
    shape = json.loads(WELL.joinpath("piece.json").read_text(encoding="utf-8"))["shape"]
    setting = json.loads(WELL.joinpath("setting.json").read_text(encoding="utf-8"))
    return universe, shape, setting


def places(held, s):
    """The well world's crests and void read off the light's lay, the square-free train of the most rows: the crests where its
    first row's count is largest in magnitude, the void where its rows' counts are all 0."""
    trains = [t for t in range(len(held.trains)) if not held.trains[t].square]
    light = max(trains, key=lambda t: held.trains[t].rows())
    first, rows = int(held.trains[light].first), held.trains[light].rows()
    top = int(abs(s.a[first]).max())
    crests = [x for x in range(s.a.shape[1]) if abs(int(s.a[first, x])) == top]
    void = [x for x in range(s.a.shape[1]) if not any(int(s.a[first + c, x]) or int(s.b[first + c, x]) for c in range(rows))]
    return crests, void


def mean_at(row, sites):
    q, _ = carry(sum(int(row[x]) for x in sites), len(sites), 0)
    return q


def the_well(say):
    """4: the well world: the sign from 0, the run back over the setting's rounds, the price and the strides."""
    universe, shape, setting = well_files()
    held, layout, s = loaded(universe, shape, setting["gears"])
    s00, s0i, sii, sjk, matter = slots(held)
    crests, void = places(held, s)
    square = [t for t in range(len(held.trains)) if held.trains[t].square]
    # (a) the sign: the first run from 0, the metric's gears taken out of the lay
    bare = [g for g in setting["gears"] if g[0] not in square]
    _, layout0, s0 = loaded(universe, shape, bare)
    marks = []
    for n in range(1, ROUNDS + 1):
        s0 = step.tick(layout0, s0)
        if n in (1, 5, 10, 20, 30):
            marks.append(f"round {n}: crests {mean_at(s0.a[s00], crests)}, void {mean_at(s0.a[s00], void)}")
    deepest = int(s0.a[s00].max())
    say(
        f"4a. the sign on the well world ({shape}, push {universe['chosen']['push']}, notch {universe['chosen']['notch']}), the first run from 0 (the"
        f" metric's gears taken out), the 00 slot's mean at the {len(crests)} crests and the {len(void)} sites of the void: {'; '.join(marks)};"
        f" its most {deepest} at round {ROUNDS}, at a crest: {deepest in [int(s0.a[s00, x]) for x in crests]} (gravity's sign: the clock deepens, a"
        f" slower clock, where the matter is)"
    )
    # (b) the laid world over the setting's rounds: the run back round by round, the price and the strides
    ticks = setting["ticks"]
    groups = {"matter": matter, "the 00 push's square rows (0i, jk)": s0i + sjk, "the ii rows (left out)": sii, "the 00 row": [s00]}
    paid = {name: 0 for name in groups}
    strides = {name: 0 for name in groups}
    back, si = 0, sigma(layout, s)
    for _ in range(ticks):
        s1 = step.tick(layout, s)
        back += all(np.array_equal(x, y) for x, y in zip(step.untick(layout, s1), s, strict=True))
        so = sigma(layout, s1)
        for name, rows in groups.items():
            paid[name] += int((si[rows] * so[rows]).sum())
            strides[name] = max(strides[name], int(abs(s1.a[rows] - s1.b[rows]).max()))
        s, si = s1, so
    ratio = per(paid["the ii rows (left out)"], paid["matter"], 10**6)
    say(
        f"4b. the laid well world, {ticks} rounds: untick(tick s) = s in {back} of {ticks} rounds; the momenta in and out, sigma_in sigma_out"
        f" summed over the rounds and the board by rows (the round's own sigma_out, the next state's sigma_in): {paid}; the metric's own"
        f" kinetic share left out of the books, the ii rows' against the matter's, {ratio} ppm; the largest stride a round by rows: {strides}"
        f" (the 00 push resolves none below half a count a round)"
    )


def main_():
    lines = []

    def say(line):
        print(line, flush=True)
        lines.append(line)

    universe = json.loads(EXAMPLE.joinpath("universe.json").read_text(encoding="utf-8"))
    universe["chosen"]["push"] = 1
    say(
        f"term 5 in the books' form at dial 2 on the built loader: the example universe at push 1 (den {universe['integers']['den']},"
        f" Gamma {universe['integers']['full_rate']}), the energy per gear the physicist's 16H by windows of {WIDTH} over {ROUNDS} rounds"
    )
    the_books(say, universe)
    the_drawn_run_back(say, universe)
    the_gamma(say, universe)
    the_well(say)
    Path(__file__).with_name("probe.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main_()
