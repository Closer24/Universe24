"""Exact symmetries of Rule3 as data maps (THEORY S3, S5, S6, S7); nothing here evolves a state.

* ``J``:  (a, b, r) -> (-a, -b, j(r)), j(r) = 4 - r (r even) or 6 - r (r odd); swaps C1 <-> C2, q -> -q.
* ``JR``: (a, b, r) -> (-b, -a, r), the time reversal: F^-1 = JR o F o JR (S6). A preparation that
  reaches a target T after N updates is S0 = JR(F^N(JR(T))) ("Big Bang built backwards").
* ``C``:  channel g -> z*g (z = 14), the 360-degree relabelling (S5).
* Gauges (S7; r16 coupling_variants_v1 "Per-site tensors are not supported"): with a J-fixed
  background (r = 2, 3), J on the channels with chi_A2(g) = -1 maps the triple (sx, sy, sz) to
  (sx, -sy, -sz) on every L (``character``), and J on the odd sites x+y+z maps it to (-sx, -sy, -sz)
  on even L or before any wrap (``staggered``). Class B = {+++, +--, -++, ---} and class F =
  {++-, +-+, -+-, --+} are the two gauge classes; a block moves between triples of one class as data.
"""
from __future__ import annotations

from universe24 import Channel, State
from universe24.core.group_2o import group

GR = group()
Z = GR.central


def _perm_sign(R):
    perm = [next(j for j in range(3) if R[i][j]) for i in range(3)]
    s = 1
    for i in range(3):
        for j in range(i + 1, 3):
            if perm[i] > perm[j]:
                s = -s
    return s


#: The A2 character of the binary octahedral group, chi_A2(g) = sign of the axis permutation of R(g).
CHI_A2 = tuple(_perm_sign(GR.rotations[g]) for g in range(48))
CLASS_B = {(1, 1, 1), (1, -1, -1), (-1, 1, 1), (-1, -1, -1)}
CLASS_F = {(1, 1, -1), (1, -1, 1), (-1, 1, -1), (-1, -1, 1)}


def jr_r(r):
    return 4 - r if r % 2 == 0 else 6 - r


def J(t):
    return (-t[0], -t[1], jr_r(t[2]))


def JR(t):
    return (-t[1], -t[0], t[2])


def gauge_class(signs):
    s = tuple(signs)
    return "B" if s in CLASS_B else "F" if s in CLASS_F else None


def gauged_signs(signs, character=False, staggered=False):
    sx, sy, sz = signs
    if character:
        sy, sz = -sy, -sz
    if staggered:
        sx, sy, sz = -sx, -sy, -sz
    return (sx, sy, sz)


def gauge_for(src, dst):
    """(character, staggered) taking triple ``src`` to ``dst`` inside one class, or None."""
    for ch in (False, True):
        for st in (False, True):
            if gauged_signs(src, ch, st) == tuple(dst):
                return ch, st
    return None


def flipped(world_address, character, staggered):
    x, y, z, g = world_address
    f = False
    if character and CHI_A2[g] == -1:
        f = not f
    if staggered and (x + y + z) % 2:
        f = not f
    return f


def gauge_cells(cells, character, staggered, background=(0, 0, 2)):
    """Apply the gauge to world-coordinate cells {(x,y,z,g): (a,b,r)}; background must be J-fixed."""
    if J(tuple(background)) != tuple(background):
        raise ValueError("gauge transport needs a J-fixed background (r = 2 or 3)")
    out = {}
    for k, v in cells.items():
        w = J(v) if flipped(k, character, staggered) else tuple(v)
        out[k] = w
    return out


def gauge_state(state, character, staggered):
    bg = (state.background.a, state.background.b, state.background.r)
    cells = gauge_cells({k: (v.a, v.b, v.r) for k, v in state.cells.items()}, character, staggered, bg)
    return State(state.cube, state.background, {k: Channel(*v) for k, v in cells.items() if v != bg})


def time_reverse_state(state):
    """JR applied to every channel of a complete state (the background (0,0,r) is JR-fixed)."""
    bg = state.background
    if (bg.a, bg.b) != (0, 0):
        raise ValueError("JR needs a stationary background")
    return State(state.cube, bg, {k: Channel(*JR((v.a, v.b, v.r))) for k, v in state.cells.items()})


def c_image_state(state):
    mul = GR.multiplication
    return State(state.cube, state.background, {(*k[:3], mul[Z][k[3]]): v for k, v in state.cells.items()})
