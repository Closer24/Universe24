"""P9, the fitted train on the head (R3, click.list_of) and what a fitted hand costs.

Read: every fitting the head lays, by the fitted hands' train (the light set into light, SL-S3, among them);
each train's fitted hand's own wind at one Node-clock on zero gears (unspring.fitted_windings_of, the due a
fitting books) in light windings, so that the threshold E = mc^2 can be read off it; and the sizes R3's replacement
would draw by (the couplings), as min(spring, 1) (the head's coupling_of) and as the spring itself (R4's word).

argv: the head's worktree, the world file, the ticks.
"""
import sys
WT = sys.argv[1]
sys.path[:0] = [WT + '/src', WT]
from collections import Counter
from tests.laws import world_of
from event_universe import readings
from event_universe.clock import Clock
from event_universe.meshes import coupling_of, factors
from event_universe.unspring import fitted_windings_of

calibre, piece = world_of(sys.argv[2])
clock = Clock(calibre, piece)
hands_ = clock.hands()
light = hands_.index(clock.unsprung())
w_light = clock.windings[light]
print(sys.argv[2], "at the setting: each train's fitted hand at one Node-clock, its own wind in light windings")
for k, h in enumerate(hands_):
    g = readings.gearing(clock, h.ratio, readings.load(clock), factors(clock))
    own = {}
    at = (1, 1, 1)
    w_minus, w_plus = fitted_windings_of(clock, k, at, (2, 1, 1), g, own)
    print(f"  hand {k}: spring {h.spring}, coupling {coupling_of(h)}, its winding {clock.windings[k]} "
          f"= {clock.windings[k] * 10 ** 6 // w_light} millionths of a light winding; a fitted hand's wind "
          f"{w_minus} = {w_minus * 10 ** 6 // w_light} millionths of a light winding")
for _ in range(int(sys.argv[3])):
    clock.tick()
by = Counter(e["line_pair"] for e in clock.log if e["event"] == "birth" and "takes" not in e)
unspr = Counter(e["taken_row"] for e in clock.log if e["event"] == "birth" and "takes" in e)
print(f"  {sys.argv[3]} ticks: fittings by the fitted train {dict(by)} (the light is hand {light}); unspringings by the "
      f"unwound train {dict(unspr)}")
springs = [h.spring for h in hands_]
total = sum(springs)
print("  R3 by sizes: the odds as the spring itself (R4), in billionths:",
      {k: s * 10 ** 9 // total for k, s in enumerate(springs)})
