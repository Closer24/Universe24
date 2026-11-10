"""Gauged guides and in-flight packets (pure port of r04 ``guides.py``; data only).

A guide is a chain of channel addresses linked by the fixed ports: x_{i+1} = x_i + e_{d_i},
g_{i+1} = ports[d_i][g_i], gauge sigma_{i+1} = sigma_i * w_i; rest (0,0,4) where sigma = +1 and
(0,0,0) where sigma = -1 (MEDIA s1). ``packet_state`` is the exact snapshot of the free forward
solution c_i(t) = f(t - i + lead) of an admissible profile f (guide propagation lemma, THEOREM).
``superpose`` adds disjoint packet deviations on the same hardware (r04 semantics).

Ported verbatim in arithmetic from research/matter_light_v1/r04/guides.py (sha recorded by the
verifier); local coordinates are allowed (``L=None``: no wrapping), the composer wraps explicitly.
"""
from __future__ import annotations

from collections import defaultdict

from universe24.core.group_2o import DIRECTIONS

VAC = (0, 0, 2)


def add(p, d, L=None):
    q = tuple(p[i] + DIRECTIONS[d][i] for i in range(3))
    return q if L is None else tuple(v % L for v in q)


def channel_path(coupling, start, g0, dirs, L=None, sigma0=1):
    """[(site, channel, sigma), ...] for the site path start, start+e_{d0}, ... following the ports."""
    nodes = [(tuple(start), g0, sigma0)]
    site, g, sigma = tuple(start), g0, sigma0
    for d in dirs:
        w = coupling.weights[d][g]
        g = coupling.ports[d][g]
        site = add(site, d, L)
        sigma *= w
        nodes.append((site, g, sigma))
    return nodes


def expand_dirs(runs):
    """[[d, n], ...] -> [d]*n + ...  (run-length direction lists)."""
    out = []
    for d, n in runs:
        out += [int(d)] * int(n)
    return out


def guide_remainder(sigma):
    return 4 if sigma == 1 else 0


def guide_cells(nodes):
    return {(*s, g): (0, 0, guide_remainder(sigma)) for s, g, sigma in nodes}


def halo_map(coupling, nodes, L=None, closed=False):
    index = {(*s, g): i for i, (s, g, _) in enumerate(nodes)}
    n = len(nodes)
    out = []
    for i, (s, g, _) in enumerate(nodes):
        nbrs = set()
        for j in (i - 1, i + 1):
            if closed:
                nbrs.add(j % n)
            elif 0 <= j < n:
                nbrs.add(j)
        halo = []
        for d in range(6):
            rec = (*add(s, d, L), coupling.ports[d][g])
            j = index.get(rec)
            if j is not None and j in nbrs:
                continue
            halo.append((rec, coupling.weights[d][g], j))
        out.append(halo)
    return out


def _periodic_history(sigma, F, G, q0, period):
    start = -1
    k = (q0 - start) % period
    theta = 2 if sigma == 1 else 0
    H = 0
    for q in range(start, start + k):
        ell = sigma * G(q)
        if ell:
            if not ((ell == 1 and theta == 2) or (ell == -1 and theta == 0)):
                raise ValueError("inadmissible periodic packet")
            theta -= 2 * ell
    for q in range(0, max(0, start + k)):
        H += F(q)
    return theta, H


def packet_state(coupling, nodes, f, lead, L=None, closed=False):
    """Cells of an in-flight packet c_i(t) = f(t - i + lead) on ``nodes`` (complete guide + halo)."""
    f = tuple(f)
    n = len(nodes)
    period = n if closed else None

    def F(q):
        if period is not None:
            q %= period
            return f[q] if q < len(f) else 0
        return f[q] if 0 <= q < len(f) else 0

    def G(q):
        return F(q + 1) + F(q - 1)

    cells = {}
    hm = halo_map(coupling, nodes, L, closed)
    halo_theta = defaultdict(int)
    for i, (s, g, sigma) in enumerate(nodes):
        q0 = lead - i
        b = sigma * F(q0)
        a = sigma * F(q0 - 1)
        theta = 2 if sigma == 1 else 0
        if period is None:
            for gq in [G(q) for q in range(-len(f) - 3, q0)]:
                ell = sigma * gq
                if ell == 0:
                    continue
                if not ((ell == 1 and theta == 2) or (ell == -1 and theta == 0)):
                    raise ValueError(f"inadmissible packet history at node {i}")
                theta -= 2 * ell
            H = sum(F(q) for q in range(-len(f) - 3, q0))
        else:
            theta, H = _periodic_history(sigma, F, G, q0, period)
        cells[(*s, g)] = (a, b, 2 * theta)
        for rec, w, j in hm[i]:
            if j is None:
                halo_theta[rec] += w * sigma * H
    for rec, h in halo_theta.items():
        th = 1 + h
        if not 0 <= th <= 2:
            raise ValueError("halo history out of range")
        if th != 1:
            cells[rec] = (0, 0, 2 * th)
    return cells


def superpose(rest, *packets, background=VAC):
    """rest + sum(packet - rest), refusing overlapping packet deviations (r04)."""
    out = dict(rest)
    touched = {}
    for k_pk, pk in enumerate(packets):
        for k, v in pk.items():
            base = rest.get(k, background)
            dv = tuple(v[i] - base[i] for i in range(3))
            if dv == (0, 0, 0):
                continue
            if k in touched and touched[k] != k_pk:
                raise ValueError(f"packets overlap at {k}")
            touched[k] = k_pk
            cur = out.get(k, base)
            out[k] = tuple(cur[i] + dv[i] for i in range(3))
    return out
