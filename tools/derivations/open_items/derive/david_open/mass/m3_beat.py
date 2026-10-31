"""The beat on the gear rule: what is a mass and what is not, in whole numbers alone.

Every step below is the head's own gear(a, b, r, W, push) from engine/step.py and its carry, at the head's teeth W:
W (a+ - 2 a + a-) = push, the remainder kept in the fine tooth. A spring D is a push -D a.

(a) on the head's tick with the example's files: the lone gear's beat and the uniform wave's;
(b) a held count's spring on the uniform wave: the exact periods at D = W, 2 W and 3 W; the board's top mode
    (every neighbour opposite, pulled by 12 grip = 2 W) beside it, which runs away once D passes 2 W; and at small
    springs D = W div k^2 the count of sign changes over N rounds times k, nearly one number, so the beat goes as the
    root of the spring and the mass's square as the spring;
(c) the held count pushed back by the gear it holds, the vertex pushing all its legs (the potential (g/2) K X^2):
    the count drifts below 0 and the gear runs away; with a spring of its own (W div 16, off the gear's doubled beat)
    it stays, a little below where it was laid;
(d) a spring between two gears alone, off the diagonal: the mode X + Y beats and the mode X - Y runs away;
(e) the antisymmetric push a T1 count gives a real gear: it runs away;
(f) the lone gear laid at 1, 2, 3 and 10^6 on the head's tick: the 6-round beat stands only while every neighbour's
    push stays below one tooth (the carry's floor), and at 10^6 the gear spreads to its neighbours;
(g) a T1 count along z on a hand of two parts, read as the hermitian i M on the mode (1, -i, 0): its value there is
    -|v|, so the hand runs away with no A1 part and beats with an A1 part of 2 |v|;
(h) the uniform wave under the spring D = W div 400 laid at amplitudes 1 to 1000: the band's beat (period about 126
    rounds) stands only once the swing is about a count a round or more; below, the carry's floor sets a different beat,
    whose exact period, the first return of the hand's whole state, is 2 W / (A D) + 4 A;
(i) the held count with its spring W div 16, as in (c), under larger swings laid at 5 x 10^6, 10^7 and 2 x 10^7: the
    push moves the count's minimum down by g X^2 / (2 kappa) at the swing's top, and once that nears n the count
    crosses 0 and the gear runs away; the spring keeps a minimum, the whole potential stays unbounded below.

Usage: python3 -I m3_beat.py <src of tensor24-review at 2a6203a4a>   (the example files are read from <src>/../examples/tensor24)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import load as L  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

ex = Path(sys.argv[1]).parent.joinpath("examples", "tensor24")
universe = json.loads(ex.joinpath("universe.json").read_text())
shape = json.loads(ex.joinpath("piece.json").read_text())["shape"]
sites = sites_of(shape)
kinds, tables = main.made(L.star(len(shape)))


def run(gears, rounds):
    loaded, found = L.load(universe, {"version": 1, "ticks": rounds, "gears": gears}, sites, kinds, tables)
    assert not found, found
    layout = main.layout(universe, shape, loaded)
    s = main.ENGINE.state(*loaded.state)
    seen, moved, first = [], set(), None
    for at in range(rounds):
        s = step.tick(layout, s)
        seen.append(int(s.a[0, 0]))
        moved |= {x for x in range(1, sites) if s.a[0, x] != 0}
        first = first if first is not None or not moved else at + 1
    run.first = first
    return seen, moved, layout


lone, moved, layout = run([[0, 0, 0, 1, 0, 0]], 60)
W = int(layout.gearing.rest[0][0])
grip = int(layout.grip[0][0])
print("(a) the head's teeth W", W, "and grip", grip, "; 6 grip = W:", 6 * grip == W)
print("    the lone gear, 60 rounds:", lone[:12], "...; period 6:", all(lone[t] == lone[t + 6] for t in range(54)),
      "; neighbours that ever moved:", len(moved))
rest, _, _ = run([[0, 0, x, 1, 1, 0] for x in range(sites)], 60)
moving, _, _ = run([[0, 0, x, 1, 0, 0] for x in range(sites)], 60)
print("    the uniform wave laid at rest:", rest[:6], "... stands at 1 for 60 rounds:", set(rest) == {1})
print("    the uniform wave laid moving:", moving[:6], "... drifts, no beat:", moving == list(range(2, 62)))


def beat(d, rounds, a=10 ** 12, top=False):
    """The uniform wave (or the top mode, pulled by -2 W a) under the spring d; its counts, round by round."""
    b, r, out = a, 0, []
    for _ in range(rounds):
        pull = -2 * W * a if top else 0
        a, b, r = step.gear(a, b, r, W, pull - d * a)
        out.append(a)
    return out


print()
for m in (1, 2, 3):
    u = beat(m * W, 24)
    period = next(p for p in range(1, 13) if all(u[t] == u[t + p] for t in range(24 - p)))
    t = beat(m * W, 24, top=True)
    grow = abs(t[-1]) // 10 ** 12
    told = "stays within its start" if grow <= 1 else "grows by two starts a round, the edge" if grow < 100 else "runs away"
    print(f"(b) D = {m} W: the uniform wave's period {period} rounds; the top mode after 24 rounds {told}"
          f" ({grow} times its start)")
N = 20000
for k in (8, 16, 32, 64, 128):
    u = beat(W // (k * k), N)
    changes = sum(1 for x, y in zip(u, u[1:]) if (x < 0) != (y < 0))
    print(f"    D = W div {k * k}: {changes} sign changes in {N} rounds; times k: {changes * k}")


CAP = 10 ** 60  # where a run is read as run away: the probe stops it there, the step never does


def pair(push, x, y, rounds):
    """Two gears stepped together by push(x, y) -> (push_x, push_y), stopped once either passes CAP."""
    bx, by, rx, ry, xs = x, y, 0, 0, []
    for _ in range(rounds):
        px, py = push(x, y)
        x, bx, rx = step.gear(x, bx, rx, W, px)
        y, by, ry = step.gear(y, by, ry, W, py)
        xs.append((x, y))
        if abs(x) > CAP or abs(y) > CAP:
            break
    return xs


n, A, D = 10 ** 6, 10 ** 5, W // 400
g, _ = carry(D, n, 0)


def held_free(x, k):
    half, _ = carry(g * x * x, 2, 0)
    return -g * k * x, -half


def held_sprung(x, k):
    px, pk = held_free(x, k)
    return px, pk - (W // 16) * (k - n)


print()
for name, push in (("with no law of its own", held_free), ("with a spring of its own, W div 16", held_sprung)):
    xs = pair(push, A, n, 2000)
    ks = [k for _, k in xs]
    gone = len(xs) < 2000
    first = next((i + 1 for i, k in enumerate(ks) if k < 0), None)
    shown = [ks[i] for i in (249, 499, 999, 1999) if i < len(ks)]
    print(f"(c) the held count {name}: K at rounds 250, 500, 1000, 2000 (as far as it ran): {shown};"
          f" below 0 first at round {first}; {'X ran past 10^60 at round ' + str(len(xs)) if gone else 'X stays'}"
          f"; least K {min(ks) if not gone else 'past -10^60'}, most {max(ks)}", flush=True)
print("    (laid K = 10^6, X = 10^5 at rest; g = (W div 400) div K, so g K is W div 400 less", D - g * n, ")")
print()
off = lambda x, y: (-D * y, -D * x)  # noqa: E731
same = pair(off, A, A, 400)
opposite = pair(off, A, -A, 400)
print("(d) a spring off the diagonal alone, D = W div 400: X = Y laid, X after 400 rounds", same[-1][0],
      "; X = -Y laid, X after 400 rounds", opposite[-1][0])
anti = pair(lambda x, y: (D * y, -D * x), A, 0, 400)
print("(e) the T1 count's antisymmetric push on a real gear, D = W div 400: X after 100, 200, 400 rounds",
      [anti[i][0] for i in (99, 199, 399)])


print()
for amp in (1, 2, 3, 10 ** 6):
    seen, moved, _ = run([[0, 0, 0, amp, 0, 0]], 24)
    six = all(seen[i] == seen[i + 6] for i in range(18))
    print(f"(f) the lone gear laid at {amp}: first rounds {seen[:6]}; period 6 kept: {six};"
          f" neighbours moved: {len(moved)}, the first at round {run.first}")


def hand(n0, v, rounds, amp=A):
    """A T1 hand of two parts, (re, im) for x, y, z; the push -(n0 + i M) X with M the cross product with (0, 0, v)."""
    m = [[0, -v, 0], [v, 0, 0], [0, 0, 0]]
    re, im = [amp, 0, 0], [0, -amp, 0]
    b_re, b_im, r_re, r_im = list(re), list(im), [0] * 3, [0] * 3
    for _ in range(rounds):
        p_re = [sum(m[k][j] * im[j] for j in range(3)) - n0 * re[k] for k in range(3)]
        p_im = [-sum(m[k][j] * re[j] for j in range(3)) - n0 * im[k] for k in range(3)]
        out = [step.gear(re[k], b_re[k], r_re[k], W, p_re[k]) for k in range(3)]
        outi = [step.gear(im[k], b_im[k], r_im[k], W, p_im[k]) for k in range(3)]
        re, b_re, r_re = [list(x) for x in zip(*out)]
        im, b_im, r_im = [list(x) for x in zip(*outi)]
    return re[0]


v = W // 400
print(f"(g) the T1 count along z on a hand, laid on the mode (1, -i, 0) at 10^5, v = W div 400: x after 400 rounds"
      f" {hand(0, v, 400)} with no A1 part; {hand(2 * v, v, 400)} with the A1 part 2 v")

print()
def first_return(d, amp, rounds):
    """The first round at which the hand's whole state (a, b, r) returns to its start, or None within the rounds."""
    a, b, r = amp, amp, 0
    for t in range(1, rounds + 1):
        a, b, r = step.gear(a, b, r, W, -d * a)
        if (a, b, r) == (amp, amp, 0):
            return t
    return None


spring = W // 400
wd, rest = carry(W, spring, 0)  # W over the spring laid, by Rule3's carry, its remainder kept
assert rest == 0, rest  # so 2 W / (A D) below is 2 wd / A as written
for amp in (1, 2, 5, 10, 30, 1000):
    u = beat(spring, 8000, a=amp)
    changes = sum(1 for x, y in zip(u, u[1:]) if (x < 0) != (y < 0))
    q, r = carry(2 * 8000, changes, 0) if changes else (0, 0)
    exact = first_return(spring, amp, 8000)
    told = f"the state returns exactly at round {exact}" if exact else "the state does not return within 8000 rounds"
    print(f"(h) the uniform wave at D = W div 400 laid at {amp}: {changes} sign changes in 8000 rounds,"
          f" a period of about {q} rounds and {r}/{changes}; {told}; 2 W / (A D) + 4 A = {2 * wd // amp + 4 * amp}"
          f"{'' if 2 * wd % amp == 0 else ' and ' + str(2 * wd % amp) + '/' + str(amp)}")


print()
kappa = W // 16
for laid in (10 ** 5, 5 * 10 ** 6, 10 ** 7, 2 * 10 ** 7):
    xs = pair(held_sprung, laid, n, 4000)
    gone = len(xs) < 4000
    shift, _ = carry(g * laid * laid, 2 * kappa, 0)
    least = min(k for _, k in xs)
    first = next((i + 1 for i, (_, k) in enumerate(xs) if k < 0), None)
    fate = f"K below 0 first at round {first}, X ran past 10^60 at round {len(xs)}" if gone else (
        f"least K {least}, X stays over 4000 rounds")
    print(f"(i) the held count with its spring W div 16, X laid at {laid}: the push's shift at the swing's top,"
          f" g X^2 div 2 kappa, {shift} against n = {n}; {fate}", flush=True)
