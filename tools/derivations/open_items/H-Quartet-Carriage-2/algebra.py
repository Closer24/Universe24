"""H-Quartet-Carriage-2: the algebra's integers per candidate pair of den's circle (a reader of the universe files and the flagged copy's gram; no run).
For each pair (num, den): the gap den - num; num over den to thousandths (quotient, remainder); the Link's reach R = 2 num Gamma^2 and the Node's mass D = 12 (den - num) Gamma^2 at the vacuum's paces (the wall w = 6 den Gamma^2, S = 2 w - D - 6 R = 0); the carriage inequality D >= R, i.e. 6 (den - num) >= num; the hop per neighbour per interval of a level N = A = 125, (num N) div (3 den); the one-Node lay's return next = -before exact at the Node; the intervals to thin the Node's level below the rounding's unit.
Usage: python algebra.py <src of the flagged copy>"""
import json, sys
sys.path.insert(0, sys.argv[1])
from event_universe import gram  # noqa: E402  (a reader's import of the quartet's matrices)

GAMMA, T, A = 1000, 36000, 125
pairs = {
    "lift1 (toy, the first lift)": (15162854575528411, 15162856759112389),
    "p3 (toy, the third plane, qc2's)": (2458210083751875, 15162856759112389),
    "lift3 (toy, the third lift)": (2580388913625285, 15162856759112389),
    "mid (middle universe, the head's quartet packet)": (506298091, 1655909141),
    "mid light (middle universe, the first lift)": (1655880909, 1655909141),
    "ga2 (the heavy leg of universe_ga2)": (115762739551980, 15162856759112389),
}
out = {}
for name, (num, den) in pairs.items():
    gap = den - num
    R = 2 * num * GAMMA * GAMMA
    D = 12 * gap * GAMMA * GAMMA
    w = 6 * den * GAMMA * GAMMA
    hop = (num * A) // (3 * den)
    row = {
        "num": num, "den": den, "gap den - num": gap,
        "num over den, thousandths [q, r]": [(1000 * num) // den, (1000 * num) % den],
        "S = 2 w - D - 6 R at the vacuum": 2 * w - D - 6 * R,
        "D >= R (6 (den - num) >= num)": 6 * gap >= num,
        "6 (den - num) over num [q]": (6 * gap) // num if num else None,
        "hop per neighbour per interval at N = 125, (num N) div (3 den)": hop,
        "share of the level hopping to six neighbours per interval, thousandths": (6 * hop * 1000) // A,
        "level staying at the Node after one hop round, 125 - 6 hop": A - 6 * hop,
        "N below which the hop rounds to 0, (3 den) div num": (3 * den) // num if num else None,
    }
    out[name] = row
# the quartet's matrices: the eigenspace kept by the step (J commutes with Gamma_a; one rule for the eight lines)
G, J = gram.gram(8), gram.rotation(8)
axes = gram.axes(8)
checks = {}
for a, Ga in enumerate(axes):
    checks[f"J Gamma_{a} - Gamma_{a} J = 0"] = gram.matmul(J, Ga) == gram.matmul(Ga, J)
    GGa = gram.matmul(G, Ga)
    checks[f"G Gamma_{a} symmetric"] = all(GGa[i][j] == GGa[j][i] for i in range(8) for j in range(8))
    for s in (1, -1):
        v = list(gram.spin_vector(8, a, s))
        dens = [int(gram.form(gram.matmul(G, Gb), v, v)) for Gb in axes]
        checks[f"spin_vector axis {a} sign {s}"] = {"v": v, "v.G.v": int(gram.form(G, v, v)), "density": dens,
            "Gamma_a v = s v": gram.matvec(Ga, v) == [s * x for x in v]}
# the rounding's leaver: the largest |(G Gamma_b delta)_k| over digits delta in {-1, 0, 1}^8 (the row sum of |G Gamma_b|)
checks["row sum max of |G Gamma_b|"] = [max(sum(abs(x) for x in row) for row in gram.matmul(G, Gb)) for Gb in axes]
checks["G diagonal"] = [G[i][i] for i in range(8)]
out["matrices"] = checks
print(json.dumps(out, indent=1))
