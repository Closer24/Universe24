"""THIRD9's member with the twin on the edge dial D (a reading probe, never src): tri7.Member with its twin eta held on
D = G D div G (the triangle's dial over its Gram entry, both read from C), born (D - 1) div senses and flipped as
D - 1 - eta. tau stays on G D, born (G D - 1) div senses; the edges are tri7.Member's. Whole numbers only; every
division is Rule3's carry.

Each shear is a remainder about its own tooth's birth: eta += G (tau - tau's birth) on D, tau += G (eta - eta's birth)
on G D. G eta on G D reads eta only mod D, and eta += G tau descends to D, so the pair (tau mod G D, eta mod D) is
closed and fixes every landing (DERIVED; read against tri7.Member by dec9.py and per9.py)."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tri7  # noqa: E402


class MemberD(tri7.Member):
    def __init__(self, n_edges, triangles, D, senses):
        super().__init__(n_edges, triangles, D, senses)
        self.ddial = [self.carry(td, Gt, 0)[0] for td, Gt in zip(self.tdial, self.G)]  # G D div G
        self.dborn = [self.carry(d - 1, senses, 0)[0] for d in self.ddial]

    def birth(self):
        return list(self.born), list(self.tborn), list(self.dborn)

    def dcen(self, v, t):
        _, r = self.carry(v + self.dborn[t], self.ddial[t], 0)
        return r - self.dborn[t]

    def shear_eta(self, eta, tau, t):
        bd = self.dborn[t]
        return bd + self.dcen(eta - bd + self.G[t] * (tau - self.tborn[t]), t)

    def shear_tau(self, tau, eta, t):
        b = self.tborn[t]
        return b + self.cen(tau - b + self.G[t] * (eta - self.dborn[t]), t)

    def flip(self, eta):
        return [self.ddial[t] - 1 - v for t, v in enumerate(eta)]

    def first_half(self, tau, eta, t):
        e1 = self.shear_eta(eta, tau, t)
        return self.shear_tau(tau, e1, t), e1

    def step(self, x, f, tau, eta, turned=True):
        carry = self.carry
        y = [sum(sg * x[e] for e, sg in col) for col in self.C]
        p = [self.g[e] * x[e] - sum(sg * y[t] for t, sg in self.on[e]) for e in range(self.n)]
        if turned:
            for t in range(len(self.C)):
                eta[t] = self.shear_eta(eta[t], tau[t], t)
                tau[t] = self.shear_tau(tau[t], eta[t], t)
        q = [0] * self.n
        for e in range(self.n):
            q[e], f[e] = carry(p[e], self.dial[e], f[e])
        w = []
        for t, col in enumerate(self.C):
            wt, tau[t] = carry(y[t], self.tdial[t], tau[t])
            w.append(wt)
            for e, sg in col:
                q[e] += sg * wt
        if turned:
            for t in range(len(self.C)):
                tau[t] = self.shear_tau(tau[t], eta[t], t)
                eta[t] = self.shear_eta(eta[t], tau[t], t)
        return q, w
