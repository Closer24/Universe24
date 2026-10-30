"""The gear's spring as one algebraic operation of the Node-clock's act, checked on the head's own gear step in whole numbers."""

# The operation, at one Node-clock, for a family's gears x and the coupling family's held count k (an A1 count here):
#   the contraction c = x . x (the 24's table of T1 with T1 onto A1, the dot product);
#   the push on each gear x_i: -g k x_i - lam c x_i (the three-leg vertex, the spring; the four-leg term, the bound);
#   the push on the held count: -(g / 2) c - kappa (k - n) (the vertex's back push; the count's own spring).
# They are minus the derivatives of one potential, V = (g / 2) k c + (lam / 4) c c + (kappa / 2) (k - n)^2, so every
# vertex pushes all its legs. Each push enters the head's gear step, W (a+ - 2 a + a-) = push, its remainder kept in
# the fine tooth (engine/step.py, gear); each strength enters as a quotient by the carry, the remainder dropped here,
# a probe's simplification. The strengths are set by hand here, as David's m3 sets them; on the act they are the law's.
# One Node-clock with no Mesh, an A1 held count: the E or T2 count's operation is OPEN (the decoder's page 3.8.7, git 8c4f3ff59).

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))

from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.main import layout as laid  # noqa: E402
from tensor24.main import made  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402
from tensor24.runner.load import load, star  # noqa: E402

EXAMPLES = ROOT / "examples" / "tensor24"
CAP = 10**60  # where a run is read as run away: the probe stops it there, the step never does
ROUNDS = 4000  # the rounds each lay is run


def teeth() -> int:
    """The head's teeth at rest, W, read from the example files through the loader and the layout."""
    universe, piece, setting = (
        json.loads((EXAMPLES / n).read_text(encoding="utf-8")) for n in ("universe.json", "piece.json", "setting.json")
    )
    shape = list(piece["shape"])
    kinds, tables, square = made(star(len(shape)))
    loaded, found = load(universe, setting, sites_of(shape), kinds, tables, square)
    assert not found, found
    return int(laid(universe, shape, loaded).gearing.rest.reshape(-1)[0])


W = teeth()
N = 10**6  # the held count's steady count, as in David's m3
G, _ = carry(W // 400, N, 0)  # the vertex's strength, so that the spring at the steady count is about W div 400
KAPPA = W // 16  # the held count's own spring, as in David's m3 (c) and (i)


def run(x: list[int], lam: tuple[int, int], quartic: str = "dot") -> tuple[list[list[int]], list[int], int]:
    """Step the gears x and the held count by the operation; lam is the four-leg strength as a quotient, 0 for none.

    It returns the gears and the held count round by round, and the largest local spring the first gear felt, the
    vertex's g k and the four-leg term's lam x . x, in thousandths of W: a gear's step holds a spring only below 4 W."""
    bx, rx, k, bk, rk = list(x), [0] * len(x), N, N, 0
    xs, ks, stiffest = [], [], 0
    for _ in range(ROUNDS):
        c = sum(v * v for v in x)
        local, _ = carry(1000 * (lam[0] * c + lam[1] * G * k), lam[1] * W, 0)
        stiffest = max(stiffest, local)
        pushes = []
        for v in x:
            four = c * v if quartic == "dot" else v * v * v
            extra, _ = carry(lam[0] * four, lam[1], 0)
            pushes.append(-G * k * v - extra)
        half, _ = carry(G * c, 2, 0)
        pk = -half - KAPPA * (k - N)
        stepped = [step.gear(v, b, r, W, p) for v, b, r, p in zip(x, bx, rx, pushes, strict=True)]
        x, bx, rx = [s[0] for s in stepped], [s[1] for s in stepped], [s[2] for s in stepped]
        k, bk, rk = step.gear(k, bk, rk, W, pk)
        xs.append(list(x))
        ks.append(k)
        if any(abs(v) > CAP for v in x) or abs(k) > CAP:
            break
    return xs, ks, stiffest


def changes(values: list[int]) -> int:
    """The sign changes along a run, 0 counted with neither sign."""
    signs = [v > 0 for v in values if v != 0]
    return sum(1 for a, b in zip(signs, signs[1:], strict=False) if a != b)


if __name__ == "__main__":
    print("The gear's spring as one operation of the act, on the head's gear step; whole numbers only\n")
    print(f"The head's teeth W = {W}; the steady count n = {N}; g = (W div 400) div n = {G}; kappa = W div 16")
    bound = (G * G, 2 * KAPPA)
    print("The four-leg bound, lam at least g^2 / (2 kappa); the runs take lam at twice it, at half of it, and at 0\n")
    strengths = (("none", (0, 1)), ("half the bound", (G * G, 4 * KAPPA)), ("twice the bound", (G * G, KAPPA)))
    print("1. The beat at a small swing, x laid at 10^5: sign changes of x over 4000 rounds (the mass's beat)")
    for name, lam in strengths:
        xs, _, _ = run([10**5], lam)
        print(f"   four-leg {name:15}: {changes([v[0] for v in xs])} sign changes")
    print("   One spring at W div 400 beats about every 126 rounds: about 63 sign changes in 4000 rounds")
    print("\n2. Larger swings, x laid at 10^7, 2 x 10^7 and 10^8: does the gear stay, or run away past 10^60?")
    for laid_at in (10**7, 2 * 10**7, 10**8):
        for name, lam in strengths:
            xs, ks, stiffest = run([laid_at], lam)
            gone = len(xs) < ROUNDS
            fate = f"ran away at round {len(xs)}" if gone else f"stays over {ROUNDS} rounds, largest |x| {max(abs(v[0]) for v in xs)}"
            least = min(ks) if not gone else "past -10^60"
            told = "past 10^60" if gone else stiffest
            print(f"   laid at {laid_at:>9}, four-leg {name:15}: x {fate}; the held count's least {least};"
                  f" the largest local spring {told} thousandths of W")
            if not gone:
                below = sum(1 for k in ks if k < 0)
                print(f"      the held count below 0 in {below} of {ROUNDS} rounds; x's sign changes {changes([v[0] for v in xs])}"
                      f" (the mass's beat gives about 64): the four-leg term bounds the swing, and the beat is no longer the mass's")
            if gone and name == "twice the bound":
                first = next(i for i, (v, k) in enumerate(zip(xs, ks)) if lam[0] * v[0] * v[0] + lam[1] * G * k > 4 * lam[1] * W)
                print(f"      the local spring first passes 4 W at round {first + 1}, the held count then {ks[first]}"
                      f" ({ks[first] // N} n): the step's limit for a lone gear (the board's top mode holds only below 2 W)")
    print(f"   (the bound itself, g^2 / (2 kappa), as a quotient: {bound[0]} / {bound[1]})")
    print("   At 10^8 the four-leg term's own spring is W at the lay; the step x+ - 2 x + x- = -(D / W) x beats only while")
    print("   D stays below 4 W, and once the local spring passes it the run breaks: the step's limit, not the potential's,")
    print("   which is bounded. The beat is the mass's only between the floor and a ceiling where the held count barely")
    print("   moves: its shift at the swing's top, g x^2 / (2 kappa), far below n.")
    for laid_at in (10**5, 10**7, 2 * 10**7):
        shift, _ = carry(G * laid_at * laid_at, 2 * KAPPA, 0)
        print(f"   laid at {laid_at:>9}: the held count's shift at the swing's top {shift}, against n = {N}")
    print("\n3. The four-leg term's channel, on a T1 family of three gears at twice the bound, laid along an axis and off it,")
    print("   (10^7, 0, 0) and (6 x 10^6, 8 x 10^6, 0), one length: sign changes of the gears' sum over 4000 rounds")
    for quartic, title in (("dot", "through A1, (x . x)^2"), ("cube", "the sum of x_i^4, through E and T2")):
        counts = []
        for lay in ([10**7, 0, 0], [6 * 10**6, 8 * 10**6, 0]):
            xs, _, _ = run(lay, (G * G, KAPPA), quartic)
            counts.append(changes([sum(v) for v in xs]))
        print(f"   {title:35}: along the axis {counts[0]}, off it {counts[1]}")
    print("   Alike in both directions only through A1: the other channel reads the board's axes.")
