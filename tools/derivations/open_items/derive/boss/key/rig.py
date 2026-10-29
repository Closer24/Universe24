"""Shared rig for the key probes: tensor24-review's committed act (the clean copy at 7b), driven from universe dicts.

Nothing under src/ is changed or patched; every world is built through load.load and main.layout, as run.run builds it,
and ticked by step.tick with every due beat firing.  Readings are taken from the act's own arrays:

  the count      the time gear's row (the great clock's load c at every Node-clock), its board mean the course;
  J              the time gear's source, step.sources' own contraction (rho + 3p through the plan);
  forms          the leapfrog's own conserved quadratic form of each gear row, H = (1/2)(W/s)(a - b)^2 + (1/2) a.K b,
                 K the act's force operator (the grip's Meshes and the spring D as ruled at the state's counts);
                 for fixed W, s and K the act's step keeps H exactly up to its carries (the rounding of a+).
  Q              a hand's swept area SUM Im(conj(a) b) = SUM (re_now im_before - im_now re_before), a whole number.
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

SRC = str(Path(__file__).resolve().parents[6] / "src")  # the worktree's committed act
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import numpy as np  # noqa: E402

from tensor24 import main as tensor24  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import load  # noqa: E402

DEN = 15162856759112389  # examples/tensor24/universe.json's den
GAMMA = 1000
KEY = 36000

_MADE: dict = {}


def made(shape):
    shape = tuple(shape)
    if shape not in _MADE:
        _MADE[shape] = tensor24.made(shape)
    return _MADE[shape]


def integers(key=KEY, den=DEN, gamma=GAMMA):
    return {"den": den, "full_rate": gamma, "key": key, "trace": 6, "width": 128}


def teeth(den=DEN, gamma=GAMMA):
    """T = 6 den Gamma^2 G^2, as load.geared makes it."""
    g = load.mesh_unit(gamma)
    return 6 * den * gamma * gamma * g * g


def light(part=1):
    return {"name": "light", "kinds": ["A1"], "part": part, "pinion": DEN}


def matter(div=50, part=1):
    return {"name": "matter", "kinds": ["A1"], "part": part, "pinion": DEN - DEN // div}


def built(trains, laid, shape, ints, drive_home=True, tooth_home=True):
    """Layout and state; laid maps (train, component, site) -> (now, before), every other gear 0.  Every fine tooth is
    laid at its home (W div 2) so the carries round half up from the start; with drive_home the time gear's drive
    tooth starts at T_d div 2 (the same symmetric rounding), else at the load's 0."""
    universe = {"version": 1, "integers": ints, "trains": trains, "couplings": []}
    sites = int(np.prod(shape))
    kinds, tables = made(shape)
    labels = tuple(n.upper() for n in kinds._fields)
    dims = tuple(k.shape[-1] for k in kinds)
    held, found = load.trains_of(trains, labels, dims)
    assert not found, found
    big_t = teeth(ints["den"], ints["full_rate"])
    gears = []
    for t_index, tr in enumerate(held):
        w = (
            big_t if t_index == len(trains) else 2 * big_t
        )  # the time gear stands on T; a file train on 2 T at count 0
        for comp in range(tr.rows()):
            for site in range(sites):
                now, before = laid.get((t_index, comp, site), (0, 0))
                gears.append([t_index, comp, site, now, before, w // 2 if tooth_home else 0])
    setting = {"version": 1, "ticks": 0, "gears": gears}
    loaded, found = load.load(universe, setting, sites, kinds, tables)
    assert loaded is not None, found
    layout = tensor24.layout(universe, list(shape), loaded)
    s = tensor24.ENGINE.state(*loaded.state)
    bad = load.promises(s.r, layout.gearing.w, layout.rate, layout.gamma)
    assert not bad, bad[:3]
    if drive_home:
        rd = s.rd.copy()
        row = layout.ruler.row
        rd[row, :] = int(layout.gearing.drive[row, 0]) // 2
        s = s._replace(rd=rd)
    return layout, s


def tick(layout, s):
    allowed = np.ones((1, s.c.shape[1]), dtype=object)
    s, out = step.tick(layout, s, allowed)
    assert all(int(k) == 1 for k in out.k[0].tolist()), "a Node-clock did not tick"
    return s


def count(layout, s):
    """The board's mean count, exact."""
    row = layout.ruler.row
    return Fraction(int(s.a[row].sum()), s.a.shape[1])


def source(layout, s):
    """The time gear's J at every site, from the act's own sources."""
    _, j = step.sources(layout, s)
    return j[layout.ruler.row]


def forms(layout, s):
    """Each gear row's 2H = (W/s)(a - b)^2 + a.K b summed over the board, as exact Fractions, at the state's own counts
    (W, s and the spring as step.ruled gives them for this state's before and now counts)."""
    laid = step.ruled(layout.gearing, layout.ruler, s.b, s.a, s.a)
    a, b = s.a, s.b
    nb = layout.nb
    grip = int(layout.grip[0, 0])
    rows = a.shape[0]
    out = []
    for g in range(rows):
        ag, bg = a[g], b[g]
        w = np.broadcast_to(laid.w[g], ag.shape)
        st = int(np.broadcast_to(laid.stretch[g], ag.shape)[0])
        sp = np.broadcast_to(laid.spring[g], ag.shape)
        d = ag - bg
        kin = Fraction(int((w * d * d).sum()), st)
        pot = 0
        for k in (0, 2, 4):  # each Mesh once: the +x, +y and +z Spokes
            pot += grip * int(((ag[nb[k]] - ag) * (bg[nb[k]] - bg)).sum())
        pot += int((sp * ag * bg).sum())
        out.append(kin + pot)
    return out  # 2H per row


def swept(s, row_re, row_im):
    """A hand's swept area SUM Im(conj(a) b) over the board: re_now im_before - im_now re_before, a whole number."""
    a, b = s.a, s.b
    return int((a[row_re] * b[row_im] - a[row_im] * b[row_re]).sum())


def ruler_ell(layout, c):
    """The ruler's mean log-slope from count 0 to count c: ln(Y(c) / Y(0)) / c, Y the ruler's own integers recovered
    from its square table (Y^2)."""
    sq = layout.ruler.square
    y0 = math.isqrt(int(sq[0]))
    yc = math.isqrt(int(sq[int(c)]))
    return math.log(yc / y0) / c


def standing(shape, amp, wave=(1, 0, -1, 0)):
    """A standing wave along the fastest axis (z in runner/board.py: site = (x sy + y) sz + z), at rest (b = a)."""
    sx, sy, sz = shape
    out = {}
    for site in range(sx * sy * sz):
        v = amp * wave[site % sz]
        if v:
            out[(0, 0, site)] = (v, v)
    return out


def uniform(shape, amp):
    out = {}
    for site in range(int(np.prod(shape))):
        out[(0, 0, site)] = (amp, amp)
    return out
