"""The two one-Node tests of the black hole on the lean toy (the owner's word of 2026-10-25: a Node at the horizon is never read and never clicks; after a turn everything returns bit for bit). The board is the world file's (a sea of light, no hole); one Node is fed by the test's hand before the run, as the engine's one-Node tests feed a line from outside, and the fed state is the run's seed.
(i) The horizon: the Node's x axis line of the volume row fed to 2 Gamma, so the tension of its two x Links (the mean of the two ends' parts) stands at Gamma and their factor is 0: the Node holds on that axis (the x arrivals enter no line), it is read by no Link close and births nothing; the content fed to the frozen level (the pace 0): the Node is not read and never clicks though its light holds whole quanta; the axis line fed back below Gamma: the Links re-couple; the run back exact through all of it.
(ii) The turn: the Node's volume time line fed a bump with before = now above its neighbours, so X0 = X1 > X2 at the first interval and the Node turns alone: every line at the Node is its pre-state exchanged and complemented, the exchange applied twice is the identity, the run back returns the fed state bit for bit; the same at the horizon's Node.
Usage: python one_node_test.py <world_node.json> [intervals]"""
import sys, os, copy, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from lean_full import Lean, load_world
from event_universe.features import volume as volform

universe, world = load_world(sys.argv[1]); n = int(sys.argv[2]) if len(sys.argv) > 2 else int(world['intervals'])
p = tuple(x // 2 for x in world['shape'])  # the fed Node, the cube's centre


def volume_at(b, level): return int(np.asarray(volform.volume_of(b.gamma, np.array([level], dtype=object)), dtype=object).reshape(-1)[0])
def state(b): return hashlib.sha256(b.state_bytes() + str(b.interval).encode()).hexdigest()
def run_back_exact(b, n):
    hashes = []
    for _ in range(n): hashes.append(state(b)); b.step()
    exact = 0
    for k in range(n): b.step_back(); exact += (state(b) == hashes[n - 1 - k])
    return exact
def log_at(b, at): return [e for e in b.log if tuple(e['node']) == at]
def ports_of(b, at): return [tuple((at[a] + (side if a == axis else 0)) % b.cube for a in range(3)) for axis, side in ((0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1))]


out = {}
# (i) the horizon
b = Lean(universe, world)
b.vol_axes[0].now[p] = 2 * b.gamma; b.vol_axes[0].before[p] = 2 * b.gamma  # the x axis part at 2 Gamma: the tension of both x Links (2 Gamma + 0 + 1) div 2 = Gamma
b.light.now[p] = 4 * int(b.light.now[p])  # the light at the Node far above two quanta, so a meeting would be read were the Node read
factors = b.link_factors()
out['horizon: factors at the Node per Port (+x, -x, +y, -y, +z, -z)'] = [int(f[p]) for f in factors]
out['horizon: factors at the +x neighbour'] = [int(f[ports_of(b, p)[0]]) for f in factors]
fed = copy.deepcopy(b)
for _ in range(n): b.step()
births_p = [e for e in log_at(b, p) if e['event'] in ('birth', 'credit')]
out['horizon: clicks at the Node in %d intervals' % n] = len(births_p)
out['horizon: clicks on the board'] = b.counts['births'] + b.counts['body_clicks']
out['horizon: the Node named in the log as an end of a refused or born Link'] = sum(1 for e in b.log if e['event'] == 'birth' and (tuple(e['minus']) == p or tuple(e['plus']) == p))
out['horizon: x Link factors at the Node after the run'] = [int(f[p]) for f in b.link_factors()[:2]]
b2 = copy.deepcopy(fed); out['horizon: run back exact of %d' % n] = run_back_exact(b2, n)
# the frozen content: the Node's volume at the clock's zero (pace 0): not read, never clicks
c = Lean(universe, world)
from event_universe.core import paces
pace_at = lambda level: int(np.asarray(paces.link_pace_of(c.gamma, np.array([level], dtype=object)), dtype=object).reshape(-1)[0])
clock_at = lambda level: int(np.asarray(paces.clock_of(c.gamma, np.array([level], dtype=object)), dtype=object).reshape(-1)[0])
frozen_level = next(level for level in range(1, 100000) if pace_at(level) == 0)
out['frozen: the first content at the Link pace 0, and the clock there'] = [frozen_level, clock_at(frozen_level)]
c.vol.now[p] = volume_at(c, frozen_level); c.vol.before[p] = c.vol.now[p]; c.light.now[p] = 4 * int(c.light.now[p])
fed_c = copy.deepcopy(c)
for _ in range(n): c.step()
out['frozen: clicks at the Node in %d intervals, clicks on the board' % n] = [len([e for e in log_at(c, p) if e['event'] in ('birth', 'credit')]), c.counts['births'] + c.counts['body_clicks']]
out['frozen: the Node an end of a born Link'] = sum(1 for e in c.log if e['event'] == 'birth' and (tuple(e['minus']) == p or tuple(e['plus']) == p))
out['frozen: content at the Node start/end'] = [frozen_level, int(c.content()[p])]
out['frozen: run back exact of %d' % n] = run_back_exact(copy.deepcopy(fed_c), n)
# the re-coupling: the axis line fed back below the wall at the fed state (2 Gamma - 2: the tension Gamma - 1), then to the sea's 0
d = copy.deepcopy(fed)
def factor_at(tension): d.vol_axes[0].now[p] = 2 * tension; return int(d.link_factors()[0][p])
coupled = next(t for t in range(b.gamma, -1, -1) if factor_at(t) > 0)  # the largest tension at which the Link still couples
out['re-coupling: the factor at the tensions Gamma, Gamma - 1, the largest coupled tension, 0'] = {b.gamma: factor_at(b.gamma), b.gamma - 1: factor_at(b.gamma - 1), coupled: factor_at(coupled), coupled + 1: factor_at(coupled + 1), 0: factor_at(0)}
recoupled = None
e = copy.deepcopy(fed)
for k in range(n):
    e.step()
    if recoupled is None and int(e.link_factors()[0][p]) > 0: recoupled = e.interval
out['horizon: the interval at which the +x Link re-coupled of itself (the axis line relaxing by Rule3)'] = recoupled
out['horizon: light credits and births on the board, the Node apart'] = [b.counts['births'], b.counts['body_clicks'], b.counts['refused_orientation'], b.counts['refused_lay'], b.counts['refused_stop']]
# (ii) the turn, on the plain sea (the world's seed with the hole and the plus-one struck), so that no other Node turns
sea_world = dict(world, seed=[lay for lay in world['seed'] if 'sea' in lay]); sea_world['seed'] = [{'row': lay['row'], 'sea': lay['sea']} for lay in sea_world['seed']]
t = Lean(universe, sea_world)
bump = volume_at(t, 40)  # the volume at the content 40 above the sea's Gamma
t.vol.now[p] = bump; t.vol.before[p] = bump
fed_t = copy.deepcopy(t)
held = [[l.copy() for l in row] for row in t.rows()]
t.step()
out['turn: turned Nodes at the first interval'] = [tuple(int(x) for x in q) for q in zip(*np.nonzero(t.turned))]
flat_h = [l for row in held for l in row]; flat_t = t.all_lines(); im = t.is_im()
exchanged = all(int(lt.now[p]) == (-1 if i else 1) * int(lh.before[p]) and int(lt.before[p]) == (-1 if i else 1) * int(lh.now[p]) and int(lt.rem[p]) == (int(lh.rem[p]) if i else lt.wall - 1 - int(lh.rem[p])) and (lt.wr is None or int(lt.wr[p]) == lt.wwall - 1 - int(lh.wr[p])) for lt, lh, i in zip(flat_t, flat_h, im))
out['turn: every line at the Node is the pre-state exchanged and complemented'] = exchanged
twice = copy.deepcopy(t); top = t.turned
before_twice = twice.state_bytes(); twice.exchange(top, [[l.copy() for l in row] for row in twice.rows()]); twice.exchange(top, [[l.copy() for l in row] for row in twice.rows()])
out['turn: the exchange applied twice is the identity'] = twice.state_bytes() == before_twice
out['turn: run back exact of %d' % n] = run_back_exact(copy.deepcopy(fed_t), n)
# the turn at the horizon's Node
h = copy.deepcopy(fed_t); h.vol_axes[0].now[p] = 2 * h.gamma; h.vol_axes[0].before[p] = 2 * h.gamma
fed_h = copy.deepcopy(h); h.step()
out['turn at the horizon: turned Nodes at the first interval'] = [tuple(int(x) for x in q) for q in zip(*np.nonzero(h.turned))]
out['turn at the horizon: run back exact of %d' % n] = run_back_exact(copy.deepcopy(fed_h), n)
for k, v in out.items(): print(k, ':', v)
