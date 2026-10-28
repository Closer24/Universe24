"""The verifier's mutation driver: copies a draft probe into mut/, changes exactly one term (asserting the old text
occurs once), and runs the copy with python3 -I -B. Usage: python3 -I mutate.py algebra|lattice [names...]"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(os.path.dirname(HERE), "D")
MUT = os.path.join(HERE, "mut")

ALGEBRA = {
    "perp_no_conj": ("return (gn(gc(phi[1])), gc(phi[0]))", "return (gn(phi[1]), phi[0])"),
    "perp_no_sign": ("return (gn(gc(phi[1])), gc(phi[0]))", "return (gc(phi[1]), gc(phi[0]))"),
    "det_sign": ("return gs(gm(u[0], v[1]), gm(u[1], v[0]))", "return ga(gm(u[0], v[1]), gm(u[1], v[0]))"),
    "reading_factor": ("return nrm(a) + nrm(b), (ab[0] + ab[0], ab[1] + ab[1], nrm(a) - nrm(b))",
                       "return nrm(a) + nrm(b), (ab[0], ab[1] + ab[1], nrm(a) - nrm(b))"),
    "twotime_Sz_sign": ("return duu[0] + ddd[0], (dud[0] + dud[0], -(dud[1] + dud[1]), duu[0] - ddd[0])",
                        "return duu[0] + ddd[0], (dud[0] + dud[0], -(dud[1] + dud[1]), ddd[0] - duu[0])"),
    "twotime_W_sign": ("return duu[0] + ddd[0], (dud[0] + dud[0], -(dud[1] + dud[1]), duu[0] - ddd[0])",
                       "return duu[0] - ddd[0], (dud[0] + dud[0], -(dud[1] + dud[1]), duu[0] - ddd[0])"),
    "inner_no_conj": ("return ga(gm(gc(phi[0]), psi[0]), gm(gc(phi[1]), psi[1]))",
                      "return ga(gm(phi[0], psi[0]), gm(gc(phi[1]), psi[1]))"),
    "partner_sign": ("partner_s = tuple(-a * x for x in m1)  # the partner's reading (rho1, -a m1)",
                     "partner_s = tuple(a * x for x in m1)  # the partner's reading (rho1, -a m1)"),
    "law6_factor": ("b = 1 if cb * (r1 + r1) * r2 < room_b", "b = 1 if cb * r1 * r2 < room_b"),
    "chsh_sign": ('PAIRS = [("a", "b", 1), ("a", "b\'", 1), ("a\'", "b", 1), ("a\'", "b\'", -1)]',
                  'PAIRS = [("a", "b", 1), ("a", "b\'", 1), ("a\'", "b", 1), ("a\'", "b\'", 1)]'),
}

LATTICE = {
    "perp_no_conj": ("return (gn(gc(phi[1])), gc(phi[0]))", "return (gn(phi[1]), phi[0])"),
    "perp_no_sign": ("return (gn(gc(phi[1])), gc(phi[0]))", "return (gc(phi[1]), gc(phi[0]))"),
    "law6_sign": ("return 1 if c * (rho + rho) * rd < room * (rho * rd + dot3(s, m)) else -1",
                  "return 1 if c * (rho + rho) * rd < room * (rho * rd - dot3(s, m)) else -1"),
    "remainder_sense": ("eta = sense(phi, -a)\n        rd = nrm(eta[0])", "eta = sense(phi, a)\n        rd = nrm(eta[0])"),
    "unstep_sign": ("p = W * (now[i][k] - a) + fine[i][k] - m - s * self.pull(before, i, k)",
                    "p = W * (now[i][k] - a) + fine[i][k] - m + s * self.pull(before, i, k)"),
    "step_mid": ("q, f = carry(W * (a - before[i][k]) + fine[i][k] - m + s * self.pull(now, i, k), W, m)",
                 "q, f = carry(W * (a - before[i][k]) + fine[i][k] + m + s * self.pull(now, i, k), W, m)"),
}


def make(kind, name):
    src = os.path.join(D, f"closure24_{kind}.py")
    table = ALGEBRA if kind == "algebra" else LATTICE
    old, new = table[name]
    text = open(src).read()
    assert text.count(old) == 1, (kind, name, text.count(old))
    os.makedirs(MUT, exist_ok=True)
    dst = os.path.join(MUT, f"{kind}_{name}.py")
    open(dst, "w").write(text.replace(old, new))
    return dst


if __name__ == "__main__":
    kind = sys.argv[1]
    names = sys.argv[2:] or list((ALGEBRA if kind == "algebra" else LATTICE).keys())
    procs = []
    for name in names:
        dst = make(kind, name)
        out = open(dst[:-3] + ".txt", "w")
        procs.append((name, subprocess.Popen(["python3", "-I", "-B", dst], stdout=out, stderr=subprocess.STDOUT)))
    for name, p in procs:
        p.wait()
        print(name, "exit", p.returncode)
