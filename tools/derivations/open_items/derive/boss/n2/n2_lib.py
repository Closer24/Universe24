"""N2 probe machinery: term 5 (the metric's push from the matter's four-vector) on the head's engine pieces.

Whole numbers only: Python ints in numpy object arrays, +, *, and Rule3's carry. The engine is imported from a
read-only `git archive` snapshot of head ed745f7cc, its src passed as the first argument.

Rows: a T1 family (0, 1, 2), an E family (3, 4), an A1 family (5): the matter; the metric family's ten slots in the
square's basis (6: 00; 7-9: 0x 0y 0z; 10-12: xx yy zz; 13-15: yz zx xy, each by its third axis).
Reading planes: 0 the value, 1-3 the centred difference along x, y, z, 4 the pull, 5 the stride into the now (sigma_b),
6 the stride out of it (sigma_a); then the unit.
"""

import sys

sys.path.insert(0, sys.argv[1])  # the src of tensor24-review at ed745f7cc, as a read-only snapshot

import numpy as np  # noqa: E402

from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import contract, mesh, step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.main import made  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.board import board  # noqa: E402

KINDS, TABLES, SQUARE = made(loading.star(3))
LABELS = [n.upper() for n in KINDS._fields]


def table(kind):
    """C[K x K -> A1] from the head's own tables, derived from the star."""
    k, a1 = LABELS.index(kind), LABELS.index("A1")
    return TABLES[(k, k, a1)][0]


T1ROWS, EROWS, A1ROWS = [0, 1, 2], [3, 4], [5]
FAMILIES = [(T1ROWS, table("T1")), (EROWS, table("E")), (A1ROWS, table("A1"))]
MATTER = T1ROWS + EROWS + A1ROWS
S00, S0I, SII, SJK = 6, [7, 8, 9], [10, 11, 12], [13, 14, 15]
METRIC = [S00, *S0I, *SII, *SJK]
ROWS, PLANES = 16, 7
UNIT = PLANES * ROWS
VALUE, GRAD, FORCE, SB, SA = 0, 1, 4, 5, 6


def at(plane, row):
    return plane * ROWS + row


# the time reversal on the four-vector: the stride turns, the differences do not (1 marks the turned index); a slot of
# the square is odd where exactly one of its two indices turns, o_m + o_n - 2 o_m o_n, the 2 the slot's two indices:
# 00 even, each 0i odd, every ii and jk even (the same construction as kinds.square, on the reversal)
TURNED = [1, 0, 0, 0]
PAIRS = [
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 1),
    (2, 2),
    (3, 3),
    (2, 3),
    (3, 1),
    (1, 2),
]  # the square's slot order
ODD = [TURNED[m] + TURNED[n] - (TURNED[m] * TURNED[n] + TURNED[m] * TURNED[n]) for m, n in PAIRS]
EVEN = np.array([1] * len(MATTER) + [1 - o for o in ODD], dtype=object).reshape(
    -1, 1
)  # 1 even, 0 odd, per row


def terms(rows):
    """A Plan from (first, second, third, factor, target) tuples."""
    if not rows:
        none = np.zeros(0, dtype=np.intp)
        return Plan(none, none, none, none.astype(object), none)
    f, s, t, c, g = zip(*rows, strict=True)
    ix = lambda x: np.array(x, dtype=np.intp)  # noqa: E731
    return Plan(ix(f), ix(s), ix(t), np.array(c, dtype=object), ix(g))


def join(*plans):
    return Plan(*(np.concatenate(xs) for xs in zip(*plans, strict=True)))


def pairs(c, rows):
    return [
        (rows[i], rows[j], int(c[i, j])) for i in range(len(rows)) for j in range(len(rows)) if c[i, j]
    ]


def spring(k, rows_c):
    """V = (k/2) x C x per family: each component pushed by -k (C x)_x (the gear's spring, a term of one reading)."""
    out = []
    for rows, c in rows_c:
        out += [(at(VALUE, y), UNIT, UNIT, -k * cxy, x) for x, y, cxy in pairs(c, rows)]
    return out


def notch(k):
    """A spring on each metric slot toward 0 (a stand-in for term 9 that keeps the probe's metric bounded)."""
    return [(at(VALUE, m), UNIT, UNIT, -k, m) for m in METRIC]


def potential(kv):
    """The 2 eta V part of term 5: 2V = kv x C x on the 00 slot with eta_00 = -1 and on each ii slot with +1."""
    out = []
    for rows, c in FAMILIES:
        for x, y, cxy in pairs(c, rows):
            out.append((at(VALUE, x), at(VALUE, y), UNIT, -kv * cxy, S00))
            out += [(at(VALUE, x), at(VALUE, y), UNIT, kv * cxy, s) for s in SII]
    return out


def gradient_part(st, families=FAMILIES):
    """S_ij = sum C (v_b,i v_b,j + v_a,i v_a,j): both slots read the gradient at the now slot, two terms each."""
    out = []
    for rows, c in families:
        for x, y, cxy in pairs(c, rows):
            for i in range(3):
                out += [(at(GRAD + i, x), at(GRAD + i, y), UNIT, st * cxy, SII[i])] * 2
            for k in range(3):
                i, j = (k + 1) % 3, (k + 2) % 3
                out += [(at(GRAD + i, x), at(GRAD + j, y), UNIT, st * cxy, SJK[k])] * 2
    return out


def rate_part(st, before=SB, after=SA):
    """The stride parts of S = sum C (v_b (x) v_b + v_a (x) v_a): 00 by sigma_b sigma_b + sigma_a sigma_a, each 0i by
    (sigma_b + sigma_a) times the gradient at the now slot (the centred stride a+ - b)."""
    out = []
    for rows, c in FAMILIES:
        for x, y, cxy in pairs(c, rows):
            out += [
                (at(before, x), at(before, y), UNIT, st * cxy, S00),
                (at(after, x), at(after, y), UNIT, st * cxy, S00),
            ]
            for i in range(3):
                out += [
                    (at(before, x), at(GRAD + i, y), UNIT, st * cxy, S0I[i]),
                    (at(after, x), at(GRAD + i, y), UNIT, st * cxy, S0I[i]),
                ]
    return out


def metric_gradient_selfpush(st):
    """The metric's own four-vector, its gradient part only (read at the now slot), identity form on the ten slots."""
    eye = np.eye(len(METRIC), dtype=object)
    return gradient_part(st, [(METRIC, eye)])


def layout(shape, rest_m, rest_g, grip, drive_m, drive_g, clock="every", grips_read=True):
    """The head's records: teeth at rest per row, the clocks' read of the 00 slot ('every' row as the loader lays it,
    'others' every row but the 00 row, 'none'), the grips reading each axis's ii slot at both ends of its Mesh."""
    nb = board(shape)
    spokes, meshes = loading.geometry(nb, 3)
    n = nb.shape[1]
    rest = np.array([rest_m] * len(MATTER) + [rest_g] * len(METRIC), dtype=object).reshape(-1, 1)
    ones = np.ones((ROWS, 1), dtype=object)
    drive = np.array([drive_m] * len(MATTER) + [drive_g] * len(METRIC), dtype=object).reshape(-1, 1)
    gearing = Gearing(rest, ones, ones.copy(), drive)
    targets = {"every": list(range(ROWS)), "others": [r for r in range(ROWS) if r != S00], "none": []}[
        clock
    ]
    clk = Read(
        np.array([S00] * len(targets), dtype=np.intp),
        np.array([1] * len(targets), dtype=object),
        np.array(targets, dtype=np.intp),
    )
    held = (
        Read(
            np.array([SII[s // 2] for s in range(6)], dtype=np.intp),
            np.array([1] * 6, dtype=object),
            np.arange(6, dtype=np.intp),
        )
        if grips_read
        else Read(np.zeros(0, dtype=np.intp), np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))
    )
    grips = np.full((1, 3 * n), grip, dtype=object)
    return Layout(nb, spokes, meshes, grips, gearing, terms([]), clk, held)


def readings(layout_, a, sb, sa):
    """The flat readings: the value, the centred differences, the pull, both strides, and the unit."""
    force = mesh.pull(layout_, a)
    grad = np.tensordot(layout_.spokes, mesh.seen(a, layout_.nb), axes=(0, 1))
    flat = np.concatenate((a[None], grad, force[None], sb[None], sa[None])).reshape(-1, a.shape[-1])
    return force, np.concatenate((flat, np.ones_like(a[:1], dtype=object)))


# ---------------------------------------------------------------- the head's (second-order) form, candidates (i), (ii)


def tick_head(layout_, s, now_plan, rate_plan):
    """One round in the head's form, staged: pass 1 gives every row its stride out of the now (sigma_a = q) from the
    now slot's sources; pass 2 adds the terms that read the matter's strides at both slots. The plan never reads a
    row's own stride, nor a pass-2 row's: only the matter's rows step before the metric reads them."""
    a, b, r, rd = s
    g = layout_.gearing
    w = step.weight(g, layout_.clock, a)
    zero = 0 * a
    force, flat = readings(layout_, a, a - b, zero)
    j1 = contract.contract(now_plan, flat, a)
    q1d, _ = step.drive(j1, g.drive, rd)
    a1, _, _ = step.gear(a, b, r, w, step.driven(g, force, q1d))
    _, flat = readings(layout_, a, a - b, a1 - a)
    j = j1 + contract.contract(rate_plan, flat, a)
    qd, rd1 = step.drive(j, g.drive, rd)
    a2, b2, r2 = step.gear(a, b, r, w, step.driven(g, force, qd))
    return State(a2, b2, r2, rd1)


def mirror_head(layout_, s, parity=True):
    """The head's mirror, each row by its parity: an even row (b, a, flip(r, W(b)), flip(r_d, T_d)), an odd row
    (-b, -a, r, r_d); parity=False is the head's mirror on every row (all even)."""
    a, b, r, rd = s
    g = layout_.gearing
    e = EVEN if parity else 1 + 0 * EVEN
    tau = e + e - 1
    wb = step.weight(g, layout_.clock, b)
    return State(tau * b, tau * a, r + e * (flip(r, wb) - r), rd + e * (flip(rd, g.drive) - rd))


# ---------------------------------------------------------------------- the first-order form, candidate (iii)


def tick_first(layout_, s, now_plan, rate_plan):
    """One round in the first-order form: each gear's rate in its own slot, p (the momentum in teeth, p = W(a-b) + r
    at a standing clock). Kick: pass 1 the now slot's sources, pass 2 adds the terms that read the matter's strides
    at both slots, sigma_b = p div W and sigma_a = p1 div W at the now slot's teeth. Drift: a+ = a + p+ div W."""
    a, p, z, rd = s
    g = layout_.gearing
    w = step.weight(g, layout_.clock, a)
    sb, _ = carry(p, w, 0)
    force, flat = readings(layout_, a, sb, 0 * a)
    j1 = contract.contract(now_plan, flat, a)
    q1d, _ = step.drive(j1, g.drive, rd)
    sa, _ = carry(p + step.driven(g, force, q1d), w, 0)
    _, flat = readings(layout_, a, sb, sa)
    j = j1 + contract.contract(rate_plan, flat, a)
    qd, rd1 = step.drive(j, g.drive, rd)
    p1 = p + step.driven(g, force, qd)
    q, _ = carry(p1, w, 0)
    return State(a + q, p1, z, rd1)


def mirror_first(layout_, s, parity=True):
    """The first-order form's mirror R = R_P o D^-1: the drift undone (the 00 row's teeth read no count, so a first
    carry recovers it and the second every row), then an even row's rate flipped in the now slot's teeth and its
    drive's tooth in T_d, an odd row's count negated."""
    a1, p, z, rd = s
    g = layout_.gearing
    e = EVEN if parity else 1 + 0 * EVEN
    tau = e + e - 1
    q0, _ = carry(p, step.weight(g, layout_.clock, a1), 0)
    w = step.weight(
        g, layout_.clock, a1 - q0
    )  # the clock reads the 00 row alone, and its own teeth stand at rest
    q, _ = carry(p, w, 0)
    a = a1 - q
    return State(tau * a, p + e * (flip(p, w) - p), z, rd + e * (flip(rd, g.drive) - rd))


def run(tick, mirror, layout_, s, n, now_plan, rate_plan, parity=True, watch=None):
    """n rounds forth, then n rounds back by the mirrored tick; the first round back that departs, if any."""
    states = [s]
    for _ in range(n):
        if watch:
            watch(states[-1])
        states.append(tick(layout_, states[-1], now_plan, rate_plan))
    t = states[-1]
    for k in range(n):
        t = mirror(layout_, tick(layout_, mirror(layout_, t, parity), now_plan, rate_plan), parity)
        want = states[n - 1 - k]
        if not all(np.array_equal(x, y) for x, y in zip(t, want, strict=True)):
            diff = [i for i, (x, y) in enumerate(zip(t, want, strict=True)) if not np.array_equal(x, y)]
            rows = sorted({int(r) for i in diff for r in np.argwhere(t[i] != want[i])[:, 0]})
            return states, k + 1, rows
    return states, None, []


def same(xs, ys):
    return all(
        np.array_equal(x, y) and all(type(v) is int for v in np.asarray(x).flat)
        for x, y in zip(xs, ys, strict=True)
    )


# ------------------------------------------------------------------------------ an integer carry sequence


class Carry:
    """Varied whole numbers by an integer carry sequence (Knuth's 64-bit LCG through Rule3's carry): no random."""

    def __init__(self, seed):
        self.x = seed

    def draw(self, low, high, shape):
        out = np.empty(shape, dtype=object)
        for i in np.ndindex(*shape):
            _, self.x = carry(self.x * 6364136223846793005 + 1442695040888963407, 1 << 64, 0)
            top, _ = carry(self.x, 1 << 24, 0)
            _, v = carry(top, high - low, 0)
            out[i] = low + int(v)
        return out


def lay(seq, layout_, matter=(20, 3), metric=(100, 10), first=False):
    """A varied lay: matter counts in +-matter[0] with strides in +-matter[1], metric slots likewise; every fine tooth
    within its teeth at the before slot and every drive's tooth within T_d. first=True gives the same lay in the
    first-order form, p = W(b)(a - b) + r."""
    n = layout_.nb.shape[1]
    cm, sm = matter
    cg, sg = metric
    a = np.concatenate(
        (seq.draw(-cm, cm + 1, (len(MATTER), n)), seq.draw(-cg, cg + 1, (len(METRIC), n)))
    )
    stride = np.concatenate(
        (seq.draw(-sm, sm + 1, (len(MATTER), n)), seq.draw(-sg, sg + 1, (len(METRIC), n)))
    )
    b = a - stride
    wb = step.weight(layout_.gearing, layout_.clock, b)
    _, r = carry(seq.draw(0, 1 << 40, (ROWS, n)), wb, 0)
    _, rd = carry(seq.draw(0, 1 << 40, (ROWS, n)), layout_.gearing.drive, 0)
    if first:
        return State(a, wb * (a - b) + r, 0 * a, rd)
    return State(a, b, r, rd)
