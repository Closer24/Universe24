"""Time symmetry of stage 7b's act: does tick(L, T s1) = T s0 hold exactly, s1 = tick(L, s0), for one involution T?

usage: python3 -I tsym.py (the repository's interpreter, with numpy; about 16 seconds; the worktree's committed act)

T, derived carry by carry from engine/step.py: a <-> b on every row; the fine tooth r -> W - 1 - r at the W the state's
own next tick reads (Z(b_t) + Z(a_t) on a reading row, the laid T on the time gear's row); the going go -> 1 - go; the
drive's tooth rd -> T_d - 1 - rd; the dial ph -> Gamma - 1 - ph; the count and the time c -> C - c, tn -> C - tn, one C
at every site. Nothing under src/ is changed; a layout's rate is replaced only in section 4, in this script's memory.
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[6] / "src"))  # the worktree's committed act

import numpy as np  # noqa: E402

from tensor24 import main as tensor24  # noqa: E402
from tensor24.algebra.carry import home  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.mesh import due  # noqa: E402
from tensor24.engine.state import Out, State  # noqa: E402
from tensor24.runner import load  # noqa: E402

DEN = 15162856759112389
INTEGERS = {"den": DEN, "full_rate": 1000, "key": 36000, "trace": 6, "width": 128}
SHAPE, SITES = [4, 4, 4], 64
WAVE = (1, 0, -1, 0)
LIGHT = {"name": "light", "kinds": ["A1"], "part": 1, "pinion": DEN}
MATTER = {"name": "matter", "kinds": ["A1"], "part": 1, "pinion": DEN - DEN // 50}
G = load.mesh_unit(INTEGERS["full_rate"])
TEETH = 6 * DEN * INTEGERS["full_rate"] ** 2 * G * G  # T; a reading row's laid W is 2 T
ONES = np.ones((1, SITES), dtype=object)
C = 1007  # the counts' and times' mirror: any whole number, one for every site


def built(trains, amplitude, seed):
    """Layout and laid state as act_push.built makes them: light a standing wave along the fastest axis, matter a
    uniform mode, each with noise of a quarter of the amplitude, a small stride (b != a) and a fine tooth in [0, 2T)."""
    universe = {"version": 1, "integers": INTEGERS, "trains": trains, "couplings": []}
    rnd, gears = random.Random(seed), []
    for t, train in enumerate(trains):
        for site in range(SITES):
            shape = WAVE[site % 4] if train is LIGHT else 1
            a = amplitude * shape + rnd.randint(-amplitude // 4, amplitude // 4)
            gears.append([t, 0, site, a, a - rnd.randint(-9, 9), rnd.randrange(TEETH + TEETH)])
    kinds, tables = tensor24.made(tuple(SHAPE))
    loaded, found = load.load(universe, {"version": 1, "ticks": 0, "gears": gears}, SITES, kinds, tables)
    assert loaded is not None, found
    layout = tensor24.layout(universe, SHAPE, loaded)
    s = tensor24.ENGINE.state(*loaded.state)
    assert not load.promises(s.r, layout.gearing.w, layout.rate, layout.gamma)
    return layout, s


def mirror(L, s, at=C, variant=""):
    """T, or one of its ablations: 'laid W' (r flipped at the laid W), 'rd kept', 'go+1', 'ph kept'."""
    w = L.gearing.w if variant == "laid W" else step.ruled(L.gearing, L.ruler, s.b, s.a, s.a).w
    return State(
        s.b.copy(),
        s.a.copy(),
        w - 1 - s.r,
        s.go + 1 if variant == "go+1" else 1 - s.go,
        s.rd.copy() if variant == "rd kept" else L.gearing.drive - 1 - s.rd,
        s.ph.copy() if variant == "ph kept" else L.gamma - 1 - s.ph,
        at - s.c,
        at - s.tn,
    )


def diffs(x, y):
    """Every component where two records differ: its first index, the two values there, and how many cells."""
    found = []
    for name, p, q in zip(x._fields, x, y, strict=True):
        p, q = np.broadcast_arrays(np.asarray(p, dtype=object), np.asarray(q, dtype=object))
        bad = np.argwhere(p != q)
        if len(bad):
            at = tuple(int(i) for i in bad[0])
            found.append(f"{name}{list(at)}: {p[at]} vs {q[at]} ({len(bad)} cells)")
    return found


def first_diff(x, y):
    """The first component where two records differ, or None."""
    found = diffs(x, y)
    return found[0] if found else None


def check(L, s0, allowed=ONES, back=None, variant=""):
    """One round forward and the mirrored round: the first difference of tick(T s1) from T s0, of its out from the
    reversed out (the same fire and k, the time T s1's), and the cells where this round's W and W+ differ."""
    s1, out = step.tick(L, s0, allowed)
    t1 = mirror(L, s1, variant=variant)
    r0, o = step.tick(L, t1, allowed if back is None else back)
    state = first_diff(r0, mirror(L, s0, variant=variant))
    outs = first_diff(o, Out(out.fire, out.k, t1.tn))
    w = step.ruled(L.gearing, L.ruler, s0.b, s0.a, s0.a).w
    wp = step.ruled(L.gearing, L.ruler, s0.b, s0.a, s1.a).wp
    return state, outs, int((w != wp).sum()), s1, out


def carries(trials=3000, seed=1):
    """Section 0: each carry's reflection on random whole numbers, the gear at W != W+ and any going."""
    rnd, off = random.Random(seed), dict.fromkeys(("gear", "drive", "beat", "home", "home go+1"), 0)
    for _ in range(trials):
        w, wp, go = rnd.randint(1, 10**6), rnd.randint(1, 10**6), rnd.randint(-3, 3)
        a, b, push, j = (rnd.randint(-(10**7), 10**7) for _ in range(4))
        r = rnd.randrange(w)
        a1, b1, r1 = step.gear(a, b, r, go, w, wp, push)
        off["gear"] += step.gear(b1, a1, wp - 1 - r1, 1 - go, wp, w, push) != (b, a, w - 1 - r)
        td = rnd.randint(1, 10**5)
        rd = rnd.randrange(td)
        q, rd1 = step.drive(j, td, rd)
        off["drive"] += step.drive(j, td, td - 1 - rd1) != (q, td - 1 - rd)
        gamma = rnd.randint(1, 10**4)
        rate, ph = rnd.randint(0, gamma), rnd.randrange(gamma)
        k, ph1 = step.beat(ph, rate, gamma, 1)
        off["beat"] += step.beat(gamma - 1 - ph1, rate, gamma, 1) != (k, gamma - 1 - ph)
        off["home"] += home(w, go) + home(w, 1 - go) != w - 1
        off["home go+1"] += home(w, go) + home(w, go + 1) != w - 1
    return off


def run(L, s, ticks):
    """Section 1: a synchronous run, each tick's state checked: T tick T = 1 on state and out, T T = 1, and
    T tick T = untick; the counts, the first failure, the time gear's count range and its rounds off the ruler."""
    exact, rounds, cells, low, high, past, below, fail = 0, 0, 0, 0, 0, 0, 0, None
    last = int(L.ruler.last)
    for n in range(ticks):
        state, outs, moved, s1, out = check(L, s)
        twice = first_diff(mirror(L, mirror(L, s)), s)
        undo = first_diff(mirror(L, step.tick(L, mirror(L, s1), ONES)[0]), step.untick(L, s1, out))
        ok = not (state or outs or twice or undo)
        exact, rounds, cells = exact + ok, rounds + (moved > 0), cells + moved
        t = [int(v) for v in s.a[L.ruler.row]]
        low, high = min(low, *t), max(high, *t)
        past, below = past + (max(t) > last), below + (min(t) < 0)
        fail = fail or (None if ok else (n, state, outs, twice, undo))
        s = s1
    return exact, rounds, cells, (low, high), past, below, fail


def doubled(L, s0, ticks, at=C, allowed=ONES):
    """The doubled Node-clock: ticks forward, T, the same ticks forward on the mirrored copy, T: back at s0?"""
    s = s0
    for _ in range(ticks):
        s, _ = step.tick(L, s, allowed)
    s = mirror(L, s, at)
    for _ in range(ticks):
        s, _ = step.tick(L, s, allowed)
    return first_diff(mirror(L, s, at), s0)


def main():
    print(
        "Time symmetry of stage 7b's act (tensor24's committed act, the clean copy): tick(L, T s1) = T s0?"
    )
    print(f"C = {C}; T = {TEETH}; the ruler's last count {len(load.ruler_of(1000)) - 1}")
    print("\n0. Carry by carry, 3000 random cases each (W != W+, go in [-3, 3]); cases off:")
    print("   " + ", ".join(f"{k} {v}" for k, v in carries().items()))
    print(
        "   (gear: gear(b1, a1, W+-1-r1, 1-go, W+, W, push) = (b, a, W-1-r); drive, beat: remainder flipped at T_d,"
        " Gamma, q and k kept; home: home(W,go) + home(W,go') = W-1 with go' = 1-go, and with go' = go+1)"
    )

    ticks = 120
    runs = [
        ("light", [LIGHT], 600, 11),
        ("light", [LIGHT], 300, 111),
        ("matter", [MATTER], 600, 12),
        ("matter", [MATTER], 300, 112),
        ("light + matter", [LIGHT, MATTER], 300, 113),
        ("light + matter", [LIGHT, MATTER], 600, 13),
    ]
    print(
        f"\n1. Synchronous runs from the laid state, every due beat firing, every tick's state checked ({ticks} each):"
    )
    totals = {}
    for name, trains, amplitude, seed in runs:
        L, s = built(trains, amplitude, seed)
        exact, rounds, cells, span, past, below, fail = run(L, s, ticks)
        far = [doubled(L, s, ticks, at) for at in (C, 0)]
        totals[name] = [
            x + y for x, y in zip(totals.get(name, [0, 0, 0]), (ticks, exact, rounds), strict=True)
        ]
        print(
            f"   {name}, A = {amplitude} ({L.gearing.w.shape[0]} rows): exact {exact}/{ticks}; W != W+ in {rounds}"
            f" rounds ({cells} cells); time gear's count {span[0]}..{span[1]}, past the ruler's last in {past} rounds,"
            f" below 0 in {below}; first failure {fail}; doubled clock at C = {C}, 0: {far}"
        )
    for name, (n, exact, rounds) in totals.items():
        print(
            f"   {name}: {exact} of {n} states exact on all eight components and the out ({rounds} with W != W+)"
        )

    L, s = built([LIGHT], 600, 11)
    warm = s
    for _ in range(40):
        warm, _ = step.tick(L, warm, ONES)
    print(
        "\n2. Ablations of T on light A = 600, 40 states from tick 40 (one round from s / from T s; T T = 1):"
    )
    for variant in ("laid W", "rd kept", "go+1", "ph kept"):
        one = rev = twice = 0
        first, s_ = None, warm
        for _ in range(40):
            a, b = check(L, s_, variant=variant)[0], check(L, mirror(L, s_), variant=variant)[0]
            again = first_diff(mirror(L, mirror(L, s_, variant=variant), variant=variant), s_)
            one, rev, twice = one + (a is None), rev + (b is None), twice + (again is None)
            first = first or a or b or again
            s_, _ = step.tick(L, s_, ONES)
        print(
            f"   {variant}: exact from s {one}/40, from T s {rev}/40, T T = 1 {twice}/40; first difference {first}"
        )

    print("\n3. Staggered counts (masks; every dial at the full rate, so tn = c), light A = 600:")
    alone = np.zeros((1, SITES), dtype=object)
    alone[0, 0] = 1
    ahead, _ = step.tick(L, s, alone)  # site 0 one beat ahead of every other
    same = first_diff(step.tick(L, s, ONES)[0], step.tick(L, ahead, ONES)[0])
    print(
        f"   all ones from the laid state s and from s' = s after site 0's beat alone: results differ at {same}"
        f" (None: the round maps s and s' to one state)"
    )
    s1, out = step.tick(L, ahead, ONES)
    back, o = step.tick(L, mirror(L, s1), ONES)
    print(
        f"   minimal failing example, s0 = s': fire at site 0 forward {out.fire[0, 0]}, mirrored {o.fire[0, 0]};"
        f" tick(T s1) vs T s0 differ at {diffs(back, mirror(L, ahead))}; the out at {diffs(o, Out(out.fire, out.k, mirror(L, s1).tn))}"
    )
    rnd, held, sx = random.Random(7), [], s
    for n in range(60):
        mask = np.array([[rnd.randint(0, 1) for _ in range(SITES)]], dtype=object)
        sx, _ = step.tick(L, sx, mask)
        held += [sx] if n >= 29 else []
    ones = masked = equal = inside = 0
    spread = max(int(max(h.c[0]) - min(h.c[0])) for h in held)
    for h in held:
        s1, out = step.tick(L, h, ONES)
        fire_back = due(mirror(L, s1).c, L.nb)
        ones += check(L, h)[0] is None
        masked += check(L, h, back=out.fire)[:2] == (None, None)
        equal += bool((fire_back == out.fire).all())
        inside += bool((fire_back * out.fire == out.fire).all())
    print(
        f"   {len(held)} staggered states (counts spread up to {spread}): mirrored round with all ones exact at {ones};"
        f" due(T s1) = the forward fire at {equal}, contains it at {inside}; with the forward fire as the mirrored"
        f" round's mask exact (state and out) at {masked}"
    )

    print(
        "\n4. Dials below the full rate (the layout's rate replaced in memory, 400..999 per site), light A = 600:"
    )
    slow = L._replace(rate=np.array([random.Random(9).choices(range(400, 1000), k=SITES)], dtype=object))
    found, outs_ok, kept, s_ = {}, 0, 0, s
    for _ in range(60):
        state, outs, *_ = check(slow, s_)
        found[(state or "exact").split("[")[0]] = found.get((state or "exact").split("[")[0], 0) + 1
        outs_ok += outs is None
        kept += check(slow, s_, variant="ph kept")[1] is None
        s_, _ = step.tick(slow, s_, ONES)
    print(
        f"   60 synchronous states: the first differing component of tick(T s1) vs T s0 {found}; the out exact"
        f" {outs_ok}/60, with the dial not flipped {kept}/60; doubled clock (60 ticks): {doubled(slow, s, 60)}"
    )


if __name__ == "__main__":
    main()
