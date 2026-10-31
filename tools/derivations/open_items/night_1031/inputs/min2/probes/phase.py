"""MIN2: mode 11's turn read at its two phases, on Big Pic's own Stepper (circ.py, ed6a1f225), whole numbers only.
(1) At the round's edge (the stored state, y = 0): eta += 3 tau, tau += 3 eta, [the carry], tau += 3 eta, eta += 3 tau.
(2) Between carries: tau += 3 eta, eta += 3 tau, [the round's edge], eta += 3 tau, tau += 3 eta.
Each map read on the unit vectors, then on 60 stated states in the half-sum basis n = (tau + eta) / 2, p = (tau - eta) / 2
(2's inverse on the odd dial 3D by Rule3's carry), against p+ = -27 n - 14 p, p+ = 27 n - 14 p and b+ = a (p+ = n);
(3) the mirror (circ's flip of the twin, the tooth kept) against the swap n <-> p."""
import sys
from pathlib import Path

tree, bench, D = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, str(tree.joinpath("src")))
sys.path.insert(0, str(bench))
from tensor24.algebra.carry import carry  # noqa: E402
import circ  # noqa: E402


class Ed:
    def __init__(self, dial):
        self.pairs, self.dial, self.triangles = [(2, 3), (3, 4), (2, 4)], dial, [(0, 1, 2)]


st = circ.Stepper(Ed(D))
D3, B3 = st.D3, st.B3
half, _ = carry(D3 + 1, 2, 0)  # 2's inverse on the odd dial


def cen(v):
    _, r = carry(v + B3, D3, 0)
    return r - B3


def sh(dst, src):  # Big Pic's shear on centred values
    return st.shear(dst + B3, src + B3, 3) - B3


def at_edge(e, t):
    e = sh(e, t)
    t = sh(t, e)
    t = sh(t, e)
    e = sh(e, t)
    return e, t


def between(e, t):
    t = sh(t, e)
    e = sh(e, t)
    e = sh(e, t)
    t = sh(t, e)
    return e, t


for name, m in (("round's edge", at_edge), ("between carries", between)):
    c1, c2 = m(1, 0), m(0, 1)
    print(f"{name}: (eta, tau) = (1, 0) -> {c1}, (0, 1) -> {c2}: matrix [[{c1[0]}, {c2[0]}], [{c1[1]}, {c2[1]}]] on (eta, tau)")
# the stepper's own round at y = 0 against at_edge
gs, ts, es = [B3] * 3, [B3 + 5], [B3 + 2]
st.step([0, 0, 0], gs, ts, es)
print("Stepper.step at y = 0 from (eta, tau) = (2, 5):", (es[0] - B3, ts[0] - B3), "; at_edge:", at_edge(2, 5))
law = {"edge -27": 0, "edge +27": 0, "edge b+=a": 0, "between +27": 0, "between -27": 0, "between b+=a": 0,
       "mirror swaps": 0}
for k in range(60):
    _, e = carry(37 * k + 11, D3, 0)
    _, t = carry(91 * k * k + 5, D3, 0)
    e, t = cen(e), cen(t)
    nn, pp = cen(half * (t + e)), cen(half * (t - e))
    for name, m in (("edge", at_edge), ("between", between)):
        e1, t1 = m(e, t)
        n1, p1 = cen(half * (t1 + e1)), cen(half * (t1 - e1))
        law[f"{name} -27"] += int(p1 == cen(-27 * nn - 14 * pp))
        law[f"{name} +27"] += int(p1 == cen(27 * nn - 14 * pp))
        law[f"{name} b+=a"] += int(p1 == nn)
    em = st.flip([e + B3])[0] - B3  # the mirror flips the twin and keeps the tooth
    law["mirror swaps"] += int(cen(half * (t + em)) == pp and cen(half * (t - em)) == nn)
print("60 states:", law)
