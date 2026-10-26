"""H-Angular-Momentum-2's test (under 15 s): the orbital L reader on the uniform pair world (L = 0 and P = 0 at every phase), the identity L about another point (L2 = 2 L0 - (c - 1) SUM_a e_a x P exactly), the hole's seed symmetry kept bit for bit by the acts (P_y = P_z = 0, L_y = -L_z at every interval), and the exact rational conservation of L by Rule3's uniform step for a field inside the torus's cut."""
import json, pathlib, random, subprocess, sys
from fractions import Fraction
from itertools import product

HERE = pathlib.Path(__file__).resolve().parent
PY = sys.executable

def run(world, out):
    subprocess.run([PY, str(HERE / "am2_angular.py"), str(HERE / "out" / world), str(out)], check=True, capture_output=True)
    return json.load(open(out))

def test_uniform_board_has_no_angular_momentum(tmp_path):
    r = run("world_pair_3_smoke.json", tmp_path / "pair.json")
    for p in r["per_interval"]:
        for key in ("dL2_step", "dL2_write", "dL2_swap", "dL2_click", "dP_step", "dP_swap", "dP_click", "L2_end", "P_end"):
            assert p[key] == [0, 0, 0], key
        assert p["dL2_step_remainders"] == ["0/1"] * 3

def test_hole_keeps_its_seed_symmetry_and_the_moment_identity(tmp_path):
    r = run("world_hole_smoke.json", tmp_path / "hole.json")
    c = r["cube"]
    for p in r["per_interval"]:
        P, L2 = p["P_end"], p["L2_end"]
        assert P[1] == 0 and P[2] == 0
        assert L2[1] == -L2[2]
        assert L2 != [0, 0, 0]
        for row in p["rows_end"].values():
            P, L0, L2 = row["P"], row["L0"], row["L2"]
            # L about the centre from L about the origin: L2 = 2 L0 - (c - 1) (1, 1, 1) x P, exact
            cross = [P[2] - P[1], P[0] - P[2], P[1] - P[0]]
            assert L2 == [2 * l - (c - 1) * x for l, x in zip(L0, cross)]

def test_rule3_uniform_step_conserves_l_inside_the_cut():
    random.seed(3)
    c = 5
    S, R, w = Fraction(1000), Fraction(37), Fraction(1200)
    nodes = list(product(range(c), repeat=3))
    def shift(i, b, s):
        j = list(i); j[b] = (j[b] + s) % c; return tuple(j)
    now = {i: Fraction(random.randint(-50, 50)) if all(1 <= x <= c - 2 for x in i) else Fraction(0) for i in nodes}
    before = {i: Fraction(random.randint(-50, 50)) if all(1 <= x <= c - 2 for x in i) else Fraction(0) for i in nodes}
    nxt = {i: (S * now[i] - w * before[i] + R * sum(now[shift(i, b, s)] for b in range(3) for s in (1, -1))) / w for i in nodes}
    def L(n, b0):
        p = {b: {i: n[shift(i, b, 1)] * b0[i] - n[i] * b0[shift(i, b, 1)] for i in nodes} for b in range(3)}
        return [sum(i[a] * p[b][i] - i[b] * p[a][i] for i in nodes) for a, b in ((1, 2), (2, 0), (0, 1))]
    assert L(nxt, now) == L(now, before)
    assert any(x != 0 for x in L(now, before))
