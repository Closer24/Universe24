"""ALG1: the triangle's twin held on the dial D instead of 3D, against Big Pic's mode 11 Stepper (circ.py, run read
only), on one triangle, every (tau, eta) pair of small dials, three passing sequences. Whole numbers; Rule3's carry.
Args: <tree> <bench dir with circ.py> <rounds>"""
import sys
from pathlib import Path

tree, bench, rounds = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, str(tree.joinpath("src")))
sys.path.insert(0, str(bench))
from tensor24.algebra.carry import carry  # noqa: E402
import circ  # noqa: E402


class Ed:
    def __init__(self, dial):
        self.pairs = [(2, 3), (3, 4), (2, 4)]
        self.dial = dial
        self.triangles = [(0, 1, 2)]


for D in (5, 21, 85):
    st = circ.Stepper(Ed(D))
    D3, B3 = st.D3, st.B3
    BD, _ = carry(D - 1, 2, 0)

    def cen3(v):
        _, r = carry(v + B3, D3, 0)
        return r - B3

    def cenD(v):
        _, r = carry(v + BD, D, 0)
        return r - BD

    seqs = {"steady 7": [[7, 0, 0]] * rounds, "steady 2D+3": [[2 * D + 3, 0, 0]] * rounds,
            "walk": [[carry(7919 * k, 2 * D + 1, 0)[1] - D, carry(104729 * k, 2 * D + 1, 0)[1] - D, 0]
                     for k in range(rounds)]}
    for name, fls in seqs.items():
        off_w, off_tau, off_class, pairs = 0, 0, 0, 0
        for t0 in range(D3):
            for e0 in range(D3):
                gs, ts, es = st.born()
                ts[0], es[0] = t0, e0
                u, v = t0 - B3, cenD(e0 - B3)  # the D-twin: eta's class mod D, centred about D's middle
                for fl in fls:
                    st.step(fl, gs, ts, es)
                    y = fl[0] + fl[1] - fl[2]
                    v = cenD(v + 3 * u)
                    u = cen3(u + 3 * v)
                    w, tt = carry(y, D3, u + B3)
                    u = tt - B3
                    u = cen3(u + 3 * v)
                    v = cenD(v + 3 * u)
                    off_w += int(w != st.last_w[0])
                    off_tau += int(u != ts[0] - B3)
                    off_class += int(v != cenD(es[0] - B3))
                pairs += 1
        print(f"D {D} (3D {D3}, the twin's dial D born {BD}), {name}, {pairs} pairs x {rounds} rounds: landings off "
              f"{off_w}, tau off {off_tau}, the D-twin off eta's class {off_class}")
print("END")
