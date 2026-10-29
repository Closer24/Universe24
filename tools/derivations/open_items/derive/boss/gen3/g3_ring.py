"""g3: what the Gaussian ring and the gear's integer recurrence allow, exactly (beside the engine; no file changed).

usage: python3 -I g3_ring.py > g3_ring.txt

 1. The C3 turn (the axes' 3-cycle) on Gaussian triples: no eigenvector but (1, 1, 1); the C4 turn: three Gaussian
    eigenvectors with the eigenvalues 1, i, -i. (The same holds for any Z3 cycle, e.g. of three trains.)
 2. The exact rest rotations: an integer second-order recurrence of finite order has 2 cos w in {-1, 0, 1, +-2};
    in Tensor24's gearing 2 cos w0 = 2 pinion / den; which of them the files' own rules admit (files.pair_departures),
    for gears and for hands; and the act: gears at pinion den/2 and 0 and a hand at (0, den) on a 1x1x1 board,
    their state back bit for bit after 6, 4 and 4 ticks.
 3. Twin hands (ring.axis): the spin axes an integer twin can point along: the cube's axes yes, the face and body
    diagonals never (|S| = rho would need sqrt 2 or sqrt 3).
 4. T on a hand (ring.conj) squares to 1, on a twin (ring.reverse) to -1; the dual run's mirror is antiunitary.
"""

import itertools
import random
import sys
from fractions import Fraction as F
from pathlib import Path

SRC = str(Path(__file__).resolve().parents[6] / "src")  # the worktree's committed act
sys.path.insert(0, SRC)

import numpy as np  # noqa: E402

from tensor24 import main as tensor24  # noqa: E402
from tensor24.algebra import ring  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import files, load  # noqa: E402


def gmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gsub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def parallel(u, v):
    """u and v (Gaussian triples) parallel over C: every 2 x 2 minor of [u, v] is 0."""
    return all(gsub(gmul(u[i], v[j]), gmul(u[j], v[i])) == (0, 0) for i, j in ((0, 1), (0, 2), (1, 2)))


def main():
    out = []
    p = out.append
    box = range(-2, 3)
    gauss = [(a, b) for a in box for b in box]
    p("1. Turns on Gaussian triples (entries a + b i, |a|, |b| <= 2; all 15,624 nonzero triples):")

    def c3(v):  # the 120-deg turn about (1, 1, 1): x -> y -> z -> x
        return (v[2], v[0], v[1])

    def c4(v):  # the 90-deg turn about z: (x, y, z) -> (-y, x, z)
        return ((-v[1][0], -v[1][1]), v[0], v[2])

    eig3, eig4 = {}, {}
    for v in itertools.product(gauss, repeat=3):
        if v == ((0, 0),) * 3:
            continue
        if parallel(v, c3(v)):
            k = next(i for i in range(3) if v[i] != (0, 0))
            lam = (
                F(c3(v)[k][0] * v[k][0] + c3(v)[k][1] * v[k][1], v[k][0] ** 2 + v[k][1] ** 2),
                F(c3(v)[k][1] * v[k][0] - c3(v)[k][0] * v[k][1], v[k][0] ** 2 + v[k][1] ** 2),
            )
            eig3[lam] = eig3.get(lam, 0) + 1
        if parallel(v, c4(v)):
            k = next(i for i in range(3) if v[i] != (0, 0))
            w = c4(v)[k]
            lam = (
                F(w[0] * v[k][0] + w[1] * v[k][1], v[k][0] ** 2 + v[k][1] ** 2),
                F(w[1] * v[k][0] - w[0] * v[k][1], v[k][0] ** 2 + v[k][1] ** 2),
            )
            eig4[lam] = eig4.get(lam, 0) + 1

    def fmt(lam):
        return f"{lam[0]}{'+' if lam[1] >= 0 else '-'}{abs(lam[1])}i"

    p(
        f"   C3 eigenvectors found, by eigenvalue: {{{', '.join(f'{fmt(k)}: {n}' for k, n in eig3.items())}}} "
        "(only 1: the multiples of (1, 1, 1); omega = (-1 + sqrt -3) / 2 is no Gaussian rational, since -3 is no square "
        "in Q(i): (a + b i)^2 = -3 needs a b = 0 and a^2 = -3 or b^2 = 3)"
    )
    p(
        f"   C4 eigenvectors found, by eigenvalue: {{{', '.join(f'{fmt(k)}: {n}' for k, n in eig4.items())}}} "
        "(1 on (0, 0, z), and i, -i on (1, -+i, 0) times a Gaussian integer: the ring's own units label three states)"
    )

    p("")
    p("2. The exact rest rotations:")
    for c in (2, 1, 0, -1, -2):
        x0, x1 = 1, 1  # at rest: the before equals the now
        seq = [x0, x1]
        for _ in range(14):
            seq.append(c * seq[-1] - seq[-2])
        period = next((n for n in range(1, 14) if seq[n] == seq[0] and seq[n + 1] == seq[1]), None)
        p(f"   x+ = {c:2d} x - x-: {seq[:10]} ... period {period}")
    p(
        "   so the finite orders are 6, 4, 3 (and 2), at 2 cos w = 1, 0, -1 (and -2): Niven's three in (0, pi)"
    )
    den = 3311818282  # the hand's den (even): 2 x 3,529 x 469,229
    integers = {"den": den, "full_rate": 1000, "key": 36000, "trace": 6, "width": 128}
    p(
        f"   Tensor24's gearing: s D / W = 2 (den - pinion) / den, so 2 cos w0 = 2 pinion / den; at den = {den}:"
    )
    s_half = int(np.sqrt(3) * den / 2)
    trials = (
        ("gear, 60 deg", {"name": "g60", "kinds": ["A1"], "part": 1, "pinion": den // 2}),
        ("gear, 90 deg", {"name": "g90", "kinds": ["A1"], "part": 1, "pinion": 0}),
        ("gear, 120 deg", {"name": "g120", "kinds": ["A1"], "part": 1, "pinion": -(den // 2)}),
        (
            "hand, 60 deg",
            {"name": "h60", "kinds": ["A1"], "part": 2, "pinion": den // 2, "sine": s_half},
        ),
        ("hand, 90 deg", {"name": "h90", "kinds": ["A1"], "part": 2, "pinion": 0, "sine": den}),
        (
            "hand, 120 deg",
            {"name": "h120", "kinds": ["A1"], "part": 2, "pinion": -(den // 2), "sine": s_half},
        ),
    )
    admitted = []
    for label, train in trials:
        found = files.pair_departures("train", train, den)
        p(
            f"     {label:14s} pinion {train['pinion']:>12d}: {'admitted' if not found else 'refused: ' + found[0]}"
        )
        if not found:
            admitted.append((label, train))
    p(
        "     (no Gaussian integer of norm den^2 has real part den/2: the roots of unity in Q(i) are 1, i, -1, -i, so a hand's"
        " exact rest turn is the quarter turn alone; the 120-deg gear needs a pinion below 0, which the files refuse)"
    )
    # the act: each admitted exact train alone, a 1x1x1 board, at rest at amplitude 7
    kinds, tables = tensor24.made((1, 1, 1))
    for label, train in admitted:
        universe = {"version": 1, "integers": integers, "trains": [train], "couplings": []}
        rows = train["part"]
        gears = [[0, row, 0, 7, 7, 0] for row in range(rows)]
        loaded, found = load.load(universe, {"version": 1, "ticks": 0, "gears": gears}, 1, kinds, tables)
        assert loaded is not None, found
        layout = tensor24.layout(universe, [1, 1, 1], loaded)
        s0 = tensor24.ENGINE.state(*loaded.state)
        s = s0
        allowed = np.ones((1, 1), dtype=object)
        back = None
        seq = []
        time_row = layout.ruler.row
        for n in range(1, 25):
            s, _ = step.tick(layout, s, allowed)
            seq.append(int(s.a[0, 0]))
            same = all(
                (np.asarray(x)[:time_row] == np.asarray(y)[:time_row]).all()
                for x, y in ((s.a, s0.a), (s.b, s0.b), (s.r, s0.r))
            )
            if same and back is None:
                back = n
        p(
            f"     on the act, {label}: row 0's notch {seq[:12]}; the train's (a, b, r) back bit for bit first at tick "
            f"{back}; the time gear's load stayed {int(s.a[time_row, 0])}"
        )

    p("")
    p(
        "3. Twin hands (ring.axis: S = (2 Re(up* down), 2 Im(up* down), |up|^2 - |down|^2), S . S = rho^2):"
    )
    small = [(a, b) for a in range(-3, 4) for b in range(-3, 4)]
    hits = {"axis": 0, "face": 0, "body": 0}
    total = 0
    for up, down in itertools.product(small, repeat=2):
        if up == (0, 0) and down == (0, 0):
            continue
        total += 1
        rho_, S = ring.axis(((up[0], up[1]), (down[0], down[1])))
        S = [int(x) for x in S]
        nz = sorted(abs(x) for x in S)
        if nz[0] == nz[1] == 0:
            hits["axis"] += 1
        elif nz[0] == 0 and nz[1] == nz[2]:
            hits["face"] += 1
        elif nz[0] == nz[1] == nz[2]:
            hits["body"] += 1
    p(
        f"   over {total} twins with |re|, |im| <= 3: spin along an axis {hits['axis']}, along a face diagonal "
        f"{hits['face']}, along a body diagonal {hits['body']}"
    )
    p(
        "   (S along (1, 1, 0) needs |S| = sqrt 2 s = rho, along (1, 1, 1) |S| = sqrt 3 s = rho: no integer twin; so of "
        "the 24's three special axes a twin's spin can stand on the 4-fold one alone)"
    )

    p("")
    p("4. T on hands and twins (ring.conj, ring.reverse), 1,000 random cases each:")
    rnd = random.Random(7)
    ok_hand = ok_twin = 0
    for _ in range(1000):
        z = (rnd.randint(-99, 99), rnd.randint(-99, 99))
        ok_hand += ring.conj(ring.conj(z)) == z
        psi = (
            (rnd.randint(-99, 99), rnd.randint(-99, 99)),
            (rnd.randint(-99, 99), rnd.randint(-99, 99)),
        )
        twice = ring.reverse(ring.reverse(psi))
        ok_twin += twice == ((-psi[0][0], -psi[0][1]), (-psi[1][0], -psi[1][1]))
    p(f"   T T = +1 on hands: {ok_hand}/1000; T T = -1 on twins: {ok_twin}/1000")
    p(
        "   T is antiunitary (it conjugates), so T U, the history run forward and mirrored, is antiunitary: its square is "
        "unitary and its cube antiunitary, never 1; the dual run's agreement (T U)^2 = T^2 = +-1 holds a state alone "
        "(hands) or in a Kramers pair (twins): the group of U and T is dihedral, irreducible pieces of size 1 or 2"
    )
    print("\n".join(out))


if __name__ == "__main__":
    main()
