"""I_verify v4: do draft I's head patches (i4_head.py) change only the two lines named?

The patch functions are taken verbatim from i4_head.py (the source between its '# ---- the patches' marker and
'def new_clock') and exec'd here. The head runs UNPATCHED; at every call of meshes_of, skewed and Clock.reverse the
patched function is also called on the same inputs and the outputs are compared field by field:
  meshes_of : factor, pawl, cosine, sine identical; odd differs only by s (f - 1) o_y (so only where f = -1)
  skewed    : every field identical but the skew's sine part, which must be e_x times the head's
  reverse   : every train's written gears identical, except a coupled hand's twelve gear: now, before negated and
              its fine tooth mirrored once (acts.mirror(., ., 1)) against the head's
Run: venv314/bin/python -I v4_patch_equiv.py <world> <ticks>
"""
import sys
from pathlib import Path

S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src']
import numpy as np  # noqa: E402
from event_universe import hands, readings  # noqa: E402,F401
from event_universe import tick as T  # noqa: E402
from event_universe.assembly.piece import read_piece  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.core import acts  # noqa: E402
from event_universe.core.acts import mid  # noqa: E402,F401
from event_universe.core.spokes import AXES, SPOKE_SIDES, SPOKES, across  # noqa: E402,F401
from event_universe.meshes import Mesh, coupling_of, mesh_teeth, odd_sum  # noqa: E402,F401
from event_universe.regulation import rest_rate_of  # noqa: E402,F401
from event_universe.trains import HAND, Gear  # noqa: E402,F401

world, ticks = sys.argv[1], int(sys.argv[2])
DYN = sys.argv[3] if len(sys.argv) > 3 else 'head'
assert DYN in ('head', 'fix12')
src = Path(S + '/derive/I/i4_head.py').read_text()
start = src.index('# ---------------------------------------------------------------- the patches')
stop = src.index('T.Tick.standard_rate = standard_rate')
ns = dict(globals())
ns['EPS'] = {}
exec(compile(src[start:stop], 'i4_patches', 'exec'), ns)
meshes_of_fix, skewed_fix, reverse_fix, std_rate_rec = ns['meshes_of_fix'], ns['skewed_fix'], ns['reverse_fix'], ns['standard_rate']
EPS = ns['EPS']

orig_meshes_of, orig_skewed, orig_reverse = T.meshes_of, T.skewed, Clock.reverse
ns['orig_standard_rate'] = T.Tick.standard_rate
T.Tick.standard_rate = std_rate_rec          # records e = 1 - 2 b only; returns what the head's returns (None)
C = dict(mesh_calls=0, mesh_bad=0, odd_sites=0, odd_changed=0, odd_changed_at_f1=0,
         skew_calls=0, skew_bad=0, skew_changed=0, skew_changed_at_e1=0,
         rev_calls=0, rev_trains=0, rev_bad=0, rev_changed_hands=0, rev_other_changed=0)


def arr(x):
    return np.asarray(x, dtype=object)


def eq(a, b):
    return np.array_equal(arr(a) * np.ones(1, dtype=object), arr(b) * np.ones(1, dtype=object))


def meshes_of_shadow(factors, pawl_signs, offset_pairs, odd):
    h = orig_meshes_of(factors, pawl_signs, offset_pairs, odd)
    f = meshes_of_fix(factors, pawl_signs, offset_pairs, odd)
    C['mesh_calls'] += 1
    for spoke, (axis, side) in enumerate(SPOKE_SIDES):
        a, b = h[spoke], f[spoke]
        same = all(x is y for x, y in ((a.factor, b.factor), (a.pawl, b.pawl), (a.cosine, b.cosine), (a.sine, b.sine)))
        same = same and a.skew == b.skew
        want = arr(a.odd) + side * (arr(pawl_signs[spoke]) - 1) * arr(across(odd[axis], spoke))
        C['mesh_bad'] += int(not same or not eq(b.odd, want))
        d = arr(b.odd) != arr(a.odd)
        fp = arr(pawl_signs[spoke]) * np.ones(np.shape(d), dtype=object)
        C['odd_sites'] += int(np.size(d))
        C['odd_changed'] += int(np.sum(d))
        C['odd_changed_at_f1'] += int(np.sum(d & (fp == 1)))
    return f if DYN == 'fix12' else h


def skewed_shadow(meshes_, rest_rate, flow_gears, full_rate):
    h = orig_skewed(meshes_, rest_rate, flow_gears, full_rate)
    f = skewed_fix(meshes_, rest_rate, flow_gears, full_rate)
    C['skew_calls'] += 1
    e = EPS['e']
    for a, b in zip(h, f, strict=True):
        same = all(x is y for x, y in ((a.factor, b.factor), (a.pawl, b.pawl), (a.cosine, b.cosine), (a.sine, b.sine), (a.odd, b.odd)))
        same = same and a.skew[0] == b.skew[0] and eq(b.skew[1], arr(e) * arr(a.skew[1]))
        C['skew_bad'] += int(not same)
        d = (arr(b.skew[1]) * np.ones(np.shape(e), dtype=object)) != (arr(a.skew[1]) * np.ones(np.shape(e), dtype=object))
        C['skew_changed'] += int(np.sum(d))
        C['skew_changed_at_e1'] += int(np.sum(d & (arr(e) == 1)))
    return f if DYN == 'fix12' else h


def reverse_shadow(self, top, held):
    captured = []
    head_written = []
    real_restore = self.restore
    if DYN == 'head':
        self.restore = lambda train, gears, top_: captured.append(('fix', [g for g in gears]))
        try:
            reverse_fix(self, top, held)
        finally:
            del self.restore
        self.restore = lambda train, gears, top_: (head_written.append(('head', [g for g in gears])), real_restore(train, gears, top_))
        try:
            orig_reverse(self, top, held)
        finally:
            del self.restore
    else:
        self.restore = lambda train, gears, top_: head_written.append(('head', [g for g in gears]))
        try:
            orig_reverse(self, top, held)
        finally:
            del self.restore
        self.restore = lambda train, gears, top_: (captured.append(('fix', [g for g in gears])), real_restore(train, gears, top_))
        try:
            reverse_fix(self, top, held)
        finally:
            del self.restore
    C['rev_calls'] += 1
    t = np.asarray(top, dtype=bool)
    for r, (_k1, gf), (_k2, gh) in zip(self.trains_, captured, head_written, strict=True):
        C['rev_trains'] += 1
        hand_c1 = r.size == HAND and r.ratio is not None and coupling_of(r) == 1
        for gi, (a, b) in enumerate(zip(gh, gf, strict=True)):
            fields_h = [arr(a.now)[t], arr(a.before)[t], (arr(a.fine) * np.ones(t.shape, dtype=object))[t]]
            fields_f = [arr(b.now)[t], arr(b.before)[t], (arr(b.fine) * np.ones(t.shape, dtype=object))[t]]
            same_meta = eq(a.teeth, b.teeth) and ((a.dfine is None and b.dfine is None) or eq(a.dfine, b.dfine))
            if hand_c1 and gi == 1:
                w = (arr(a.teeth) * np.ones(t.shape, dtype=object))[t]
                ok = (np.array_equal(fields_f[0], -fields_h[0]) and np.array_equal(fields_f[1], -fields_h[1])
                      and np.array_equal(fields_f[2], acts.mirror(fields_h[2], w, 1)) and same_meta)
                C['rev_bad'] += int(not ok)
                C['rev_changed_hands'] += int(t.sum())
            else:
                ok = all(np.array_equal(x, y) for x, y in zip(fields_h, fields_f)) and same_meta
                C['rev_bad'] += int(not ok)
                C['rev_other_changed'] += int(not ok)


T.meshes_of, T.skewed, Clock.reverse = meshes_of_shadow, skewed_shadow, reverse_shadow
calibre, piece = read_piece(Path(S + '/t24/tests/worlds/' + world))
clk = Clock(calibre, piece)
for _ in range(ticks):
    clk.tick()
print(f"V4 {world}, {ticks} ticks on the {DYN} dynamics, the other side run in shadow:")
print(f"  meshes_of: {C['mesh_calls']} calls; {C['mesh_bad']} spoke readings off the one-line change; the odd sum"
      f" changed at {C['odd_changed']} of {C['odd_sites']} spoke-sites, of them at f = +1: {C['odd_changed_at_f1']}")
print(f"  skewed: {C['skew_calls']} calls; {C['skew_bad']} spoke readings off the one-line change; the skew changed at"
      f" {C['skew_changed']} spoke-sites, of them at e = +1: {C['skew_changed_at_e1']}")
print(f"  reverse: {C['rev_calls']} turnovers; {C['rev_trains']} trains compared; {C['rev_bad']} gears off the one-line"
      f" change; coupled hands' twelve gears changed at {C['rev_changed_hands']} turned Node-clocks; other gears changed:"
      f" {C['rev_other_changed']}")
print(f"  turnovers counted by the head: {clk.counts['turns']}")
