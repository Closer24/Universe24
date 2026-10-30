"""N2's second text, the probe machinery: term 5 (the metric's push from the matter's four-vector) on the engine's
own pieces (tensor24, installed editable in the worktree's venv), in the head's r-form and in the first-order p-form.

Clock: a board of Node-clocks, each gear stepped once a round by Rule3's carry; the matter's strides push the metric
family's slots, and the metric's 00 slot is every other row's teeth.
Algebra: whole numbers only: Python ints in numpy object arrays, +, * and Rule3's carry; the varied lays come from an
integer recurrence, no random module.
Board: rows 0-2 a T1 family, 3-4 an E family, 5 an A1 family (the matter); 6-15 the metric family's ten slots in the
square's basis (6: 00; 7-9: 0x 0y 0z; 10-12: xx yy zz; 13-15: yz zx xy, each by its third axis). Reading planes: 0 the
value, 1-3 the centred difference along x, y, z, 4 the pull, 5 the stride into the now (sigma_b), 6 the stride out of
it (sigma_a); then the unit.
Clicks: n/a: the probes read the board from outside.

Built on the first text's n2_lib.py (tools/derivations/open_items/derive/boss/n2), with the clock's read and the
grips' read made general, the drift undone to any depth of acyclic reads, the product form of the 00 slot, the
metric's own rows as a source family, and the cube's 24 turns in both forms.
"""

import numpy as np

from tensor24.algebra.carry import carry, flip
from tensor24.engine import contract, mesh, step
from tensor24.engine.state import Gearing, Layout, Plan, Read, State
from tensor24.main import made
from tensor24.runner import load as loading
from tensor24.runner.board import board

KINDS, TABLES, SQUARE = made(loading.star(3))
LABELS = [n.upper() for n in KINDS._fields]
TURNS = [g for g in range(KINDS.t1.shape[0]) if (KINDS.t1[g] != 0).any()]  # the 24 among the 216 candidates


def table(kind):
    """C[K x K -> A1] from the engine's own tables, derived from the star."""
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


# the time reversal on the four-vector: the stride turns, the differences do not; a slot of the square is odd where
# exactly one of its two indices turns: 00 even, each 0i odd, every ii and jk even
TURNED = [1, 0, 0, 0]
PAIRS = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (2, 2), (3, 3), (2, 3), (3, 1), (1, 2)]
ODD = [TURNED[m] + TURNED[n] - (TURNED[m] * TURNED[n] + TURNED[m] * TURNED[n]) for m, n in PAIRS]
ROW_ODD = [0] * len(MATTER) + ODD  # 1 where a row is odd under the reversal
EVEN = np.array([1 - o for o in ROW_ODD], dtype=object).reshape(-1, 1)  # 1 even, 0 odd, per row


def leg_parity(index):
    """A reading's parity under the reversal: a stride plane is odd, a 0i row's reading is odd, the unit even."""
    if index == UNIT:
        return 0
    plane, row = divmod(index, ROWS)
    stride = 1 if plane in (SB, SA) else 0
    return (stride + ROW_ODD[row]) % 2


def term_parity_ok(term):
    """Whether a term's legs and its target have one parity: the reversal's condition on a monomial."""
    f, s, t, _, g = term
    return (leg_parity(f) + leg_parity(s) + leg_parity(t)) % 2 == ROW_ODD[g]


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


def engine_plan(plan):
    """The same plan on the engine's own readings (five planes, then the unit), for step.tick."""
    return plan._replace(
        **{
            f: np.where(getattr(plan, f) == UNIT, 5 * ROWS, getattr(plan, f)).astype(np.intp)
            for f in ("first", "second", "third")
        }
    )


def pairs(c, rows):
    return [
        (rows[i], rows[j], int(c[i, j])) for i in range(len(rows)) for j in range(len(rows)) if c[i, j]
    ]


def eye_family(rows):
    """A set of rows read through the identity table, each row a scalar of its own."""
    return (rows, np.eye(len(rows), dtype=object))


def spring(k, rows_c):
    """V = (k/2) x C x per family: each component pushed by -k (C x)_x."""
    out = []
    for rows, c in rows_c:
        out += [(at(VALUE, y), UNIT, UNIT, -k * cxy, x) for x, y, cxy in pairs(c, rows)]
    return out


def notch(k, rows=METRIC):
    """A spring on each metric slot toward 0: a stand-in for term 9 that keeps a probe's metric bounded, named so."""
    return [(at(VALUE, m), UNIT, UNIT, -k, m) for m in rows]


def potential(kv, families=FAMILIES):
    """The 2 eta V part of term 5: 2V = kv x C x on the 00 slot with eta_00 = -1 and on each ii slot with +1."""
    out = []
    for rows, c in families:
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


def rate_part(st, before=SB, after=SA, families=FAMILIES, slot00=True, slot0i=True):
    """The stride parts of S = sum C (v_b (x) v_b + v_a (x) v_a): 00 by sigma_b sigma_b + sigma_a sigma_a, each 0i by
    (sigma_b + sigma_a) times the gradient at the now slot."""
    out = []
    for rows, c in families:
        for x, y, cxy in pairs(c, rows):
            if slot00:
                out += [
                    (at(before, x), at(before, y), UNIT, st * cxy, S00),
                    (at(after, x), at(after, y), UNIT, st * cxy, S00),
                ]
            if slot0i:
                for i in range(3):
                    out += [
                        (at(before, x), at(GRAD + i, y), UNIT, st * cxy, S0I[i]),
                        (at(after, x), at(GRAD + i, y), UNIT, st * cxy, S0I[i]),
                    ]
    return out


def product_rate_part(st, families=FAMILIES):
    """The product form of the 00 slot, 2 sigma_b sigma_a, with the 0i slots as in rate_part."""
    out = []
    for rows, c in families:
        for x, y, cxy in pairs(c, rows):
            out += [(at(SB, x), at(SA, y), UNIT, st * cxy, S00)] * 2
    return out + rate_part(st, families=families, slot00=False)


def layout(
    shape,
    rest_m,
    rest_g,
    grip,
    drive_m,
    drive_g,
    clock="others",
    grip_rows=SII,
    rest_rows=None,
):
    """The engine's records: teeth at rest per row (rest_rows overrides them row by row), the clocks' read of the 00
    slot ('every' row as the loader lays it, 'others' every row but the 00 row, 'none', or a list of (read row,
    target row) pairs at the factor 1), the grips reading one row per axis at both ends of each Mesh (grip_rows, or
    None for no read)."""
    nb = board(shape)
    spokes, meshes = loading.geometry(nb, 3)
    n = nb.shape[1]
    rest = np.array([rest_m] * len(MATTER) + [rest_g] * len(METRIC), dtype=object).reshape(-1, 1)
    if rest_rows is not None:
        for row, value in rest_rows.items():
            rest[row, 0] = value
    ones = np.ones((ROWS, 1), dtype=object)
    drive = np.array([drive_m] * len(MATTER) + [drive_g] * len(METRIC), dtype=object).reshape(-1, 1)
    gearing = Gearing(rest, ones, ones.copy(), drive)
    if isinstance(clock, str):
        targets = {"every": list(range(ROWS)), "others": [r for r in range(ROWS) if r != S00], "none": []}[
            clock
        ]
        pairs_ = [(S00, t) for t in targets]
    else:
        pairs_ = list(clock)
    clk = Read(
        np.array([f for f, _ in pairs_], dtype=np.intp),
        np.array([1] * len(pairs_), dtype=object),
        np.array([t for _, t in pairs_], dtype=np.intp),
    )
    if grip_rows is None:
        held = Read(np.zeros(0, dtype=np.intp), np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))
    else:
        held = Read(
            np.array([grip_rows[s // 2] for s in range(6)], dtype=np.intp),
            np.array([1] * 6, dtype=object),
            np.arange(6, dtype=np.intp),
        )
    grips = np.full((1, 3 * n), grip, dtype=object)
    return Layout(nb, spokes, meshes, grips, gearing, terms([]), clk, held)


def readings(layout_, a, sb, sa):
    """The flat readings: the value, the centred differences, the pull, both strides, and the unit."""
    force = mesh.pull(layout_, a)
    grad = np.tensordot(layout_.spokes, mesh.seen(a, layout_.nb), axes=(0, 1))
    flat = np.concatenate((a[None], grad, force[None], sb[None], sa[None])).reshape(-1, a.shape[-1])
    return force, np.concatenate((flat, np.ones_like(a[:1], dtype=object)))


# ------------------------------------------------------------------------ the head's r-form, staged (candidate (i))


def tick_head(layout_, s, now_plan, rate_plan):
    """One round in the head's form, staged: pass 1 gives every row its stride out of the now (sigma_a = q) from the
    now slot's sources; pass 2 adds the terms that read the matter's strides at both slots."""
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
    (-b, -a, r, r_d); parity=False is the head's mirror on every row."""
    a, b, r, rd = s
    g = layout_.gearing
    e = EVEN if parity else 1 + 0 * EVEN
    tau = e + e - 1
    wb = step.weight(g, layout_.clock, b)
    return State(tau * b, tau * a, r + e * (flip(r, wb) - r), rd + e * (flip(rd, g.drive) - rd))


# ------------------------------------------------------------------------ the first-order p-form (candidate (iii))


def tick_first(layout_, s, now_plan, rate_plan):
    """One round in the first-order form: each gear's rate in its own slot p (p = W (a - b) + r at a standing clock).
    Pass 1 the now slot's sources, pass 2 the terms that read the strides sigma_b = p div W and sigma_a = p1 div W at
    the now slot's teeth; then p+ = p + s (F + T_k q_d) and the drift a+ = a + p+ div W."""
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


def undrift(layout_, a1, p, depth=1):
    """The drift undone: a from a+ = a + p div W(a), by depth + 1 carries, exact where the clock's reads are acyclic
    of that depth (a row reading no row comes back at the first carry, a row reading only such rows at the second)."""
    g = layout_.gearing
    a = a1
    for _ in range(depth + 1):
        q, _ = carry(p, step.weight(g, layout_.clock, a), 0)
        a = a1 - q
    return a, step.weight(g, layout_.clock, a)


def mirror_first(layout_, s, parity=True, depth=1):
    """R = R_P o D^-1: the drift undone, then an even row's rate flipped in the now slot's teeth and its drive's tooth
    in T_d, an odd row's count negated."""
    a1, p, z, rd = s
    g = layout_.gearing
    e = EVEN if parity else 1 + 0 * EVEN
    tau = e + e - 1
    a, w = undrift(layout_, a1, p, depth)
    return State(tau * a, p + e * (flip(p, w) - p), z, rd + e * (flip(rd, g.drive) - rd))


def run(tick, mirror, layout_, s, n, now_plan, rate_plan, parity=True, watch=None, depth=1):
    """n rounds forth, then n rounds back by the mirrored tick; the first round back that departs, if any, with the
    rows departing there."""
    states = [s]
    for _ in range(n):
        if watch:
            watch(states[-1])
        states.append(tick(layout_, states[-1], now_plan, rate_plan))
    t = states[-1]
    kw = {"depth": depth} if mirror is mirror_first else {}
    for k in range(n):
        t = mirror(layout_, tick(layout_, mirror(layout_, t, parity, **kw), now_plan, rate_plan), parity, **kw)
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


def metric_source(L_, s_, now_plan, rate_plan, first=False):
    """J on every row before the drive, for a state in the r-form or the p-form: pass 1's strides out, then pass 2."""
    g = L_.gearing
    if first:
        a, p, _, rd = s_
        w = step.weight(g, L_.clock, a)
        sb, _ = carry(p, w, 0)
    else:
        a, b, r, rd = s_
        w = step.weight(g, L_.clock, a)
        sb = a - b
    force, flat = readings(L_, a, sb, 0 * a)
    j1 = contract.contract(now_plan, flat, a)
    q1d, _ = step.drive(j1, g.drive, rd)
    if first:
        sa, _ = carry(p + step.driven(g, force, q1d), w, 0)
    else:
        a1, _, _ = step.gear(a, b, r, w, step.driven(g, force, q1d))
        sa = a1 - a
    _, flat = readings(L_, a, sb, sa)
    return j1 + contract.contract(rate_plan, flat, a)


# ------------------------------------------------------------------------------ an integer carry sequence


class Carry:
    """Varied whole numbers by an integer recurrence (a 64-bit linear congruence through Rule3's carry): no random."""

    def __init__(self, seed):
        self.x = seed

    def draw(self, low, high, shape):
        """Whole numbers in [low, high) in the given shape."""
        out = np.empty(shape, dtype=object)
        for i in np.ndindex(*shape):
            _, self.x = carry(self.x * 6364136223846793005 + 1442695040888963407, 1 << 64, 0)
            top, _ = carry(self.x, 1 << 24, 0)
            _, v = carry(top, high - low, 0)
            out[i] = low + int(v)
        return out


def lay(seq, layout_, matter=(20, 3), metric=(100, 10), first=False, metric_rows=None):
    """A varied lay: matter counts in +-matter[0] with strides in +-matter[1], metric slots likewise (or only the rows
    in metric_rows, the other slots at 0); every fine tooth within its teeth at the before slot and every drive's
    tooth within T_d. first=True gives the same lay in the first-order form, p = W(b)(a - b) + r."""
    n = layout_.nb.shape[1]
    cm, sm = matter
    cg, sg = metric
    a = np.concatenate(
        (seq.draw(-cm, cm + 1, (len(MATTER), n)), seq.draw(-cg, cg + 1, (len(METRIC), n)))
    )
    stride = np.concatenate(
        (seq.draw(-sm, sm + 1, (len(MATTER), n)), seq.draw(-sg, sg + 1, (len(METRIC), n)))
    )
    if metric_rows is not None:
        for m in METRIC:
            if m not in metric_rows:
                a[m] = 0
                stride[m] = 0
    b = a - stride
    wb = step.weight(layout_.gearing, layout_.clock, b)
    _, r = carry(seq.draw(0, 1 << 40, (ROWS, n)), wb, 0)
    _, rd = carry(seq.draw(0, 1 << 40, (ROWS, n)), layout_.gearing.drive, 0)
    if first:
        return State(a, wb * (a - b) + r, 0 * a, rd)
    return State(a, b, r, rd)


def to_first(layout_, s):
    """A state of the r-form carried to the p-form at the same teeth: p = W(b) (a - b) + r."""
    a, b, r, rd = s
    wb = step.weight(layout_.gearing, layout_.clock, b)
    return State(a, wb * (a - b) + r, 0 * a, rd)


# ------------------------------------------------------------------------------ the cube's 24 turns


def turn_rows(g):
    """The turn g on the 16 rows: T1 rows by the turn, A1 fixed, the metric's ten slots by the square's signed
    permutation; the E rows are left in place (they stand at 0 in every run that uses this, as E has no whole basis)."""
    p = np.zeros((ROWS, ROWS), dtype=object)
    t1 = np.array(KINDS.t1[g], dtype=object)
    for i, x in enumerate(T1ROWS):
        for j, y in enumerate(T1ROWS):
            p[x, y] = t1[i, j]
    for x in EROWS + A1ROWS:
        p[x, x] = 1
    sq = np.array(SQUARE[g], dtype=object)
    for i, x in enumerate(METRIC):
        for j, y in enumerate(METRIC):
            p[x, y] = sq[i, j]
    return p


def turn_sites(g, shape):
    """Each site's index after the turn: the coordinates x to m x, each wrapped by Rule3's carry (a cube)."""
    side = shape[0]
    xyz = np.indices(shape).reshape(len(shape), -1)
    moved = np.array(KINDS.t1[g], dtype=np.intp) @ xyz
    _, wrapped = carry(moved, side, 0)
    return np.ravel_multi_index(tuple(wrapped), shape)


def signs(p):
    """The two halves of a signed permutation: its + entries and its - entries, each a 0 or 1 matrix."""
    plus, _ = carry(p * p + p, 1 + 1, 0)
    return plus, p * p - plus


def moved(xs, site):
    out = []
    for x in xs:
        y = np.empty_like(x)
        y[:, site] = x
        out.append(y)
    return out


def turned_head(s, p, site, w, wd):
    """The r-form's state turned: rows by p, sites moved, each tooth of a row whose sign p flips taken to w - 1 - r
    (the drive's in its teeth wd)."""
    plus, minus = signs(p)
    r = plus @ s.r + minus @ flip(s.r, w)
    rd = plus @ s.rd + minus @ flip(s.rd, wd)
    return State(*moved((p @ s.a, p @ s.b, r, rd), site))


def turned_first(s, p, site, w, wd):
    """The p-form's state turned: rows by p, sites moved, the rate p of a row whose sign the turn flips taken to
    w - 1 - p in the now slot's teeth w (the carry's sign law on the dividend), the drive's tooth to wd - 1 - r_d."""
    plus, minus = signs(p)
    rate = plus @ s.b + minus @ flip(s.b, w)
    rd = plus @ s.rd + minus @ flip(s.rd, wd)
    return State(*moved((p @ s.a, rate, s.r, rd), site))


def sign_free(p):
    return not bool((p < 0).any())
