"""One Node through a run: its volume line's three levels before and after the step, the turned count of the board, its light and its light share in quanta, printed at the named intervals (the diagnostic that found the two-cycle of the post-state swap).
Usage: python freeze_diag.py <world.json> <intervals> [mode] [x,y,z]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lean_full import Lean, load_world
universe, world = load_world(sys.argv[1]); n = int(sys.argv[2])
mode = sys.argv[3] if len(sys.argv) > 3 else 'current'
at = tuple(int(x) for x in sys.argv[4].split(',')) if len(sys.argv) > 4 else (0, 0, 0)
b = Lean(universe, world, link_birth={'current': 'current', 'link': True, 'node': False}[mode])
marks = {1, 5, 10, 25, 50, 100, 200, 300, 400, 500, 600} | set(range(max(1, n - 12), n + 1))
for t in range(n):
    vb, vn = int(b.vol.before[at]), int(b.vol.now[at])
    b.step()
    if b.interval in marks:
        print(b.interval, 'turned', int(b.turned.sum()), 'node', at, 'vol before/now (start)', vb, vn, '-> now/before after', int(b.vol.now[at]), int(b.vol.before[at]), 'light', int(b.light.now[at]), int(b.light.before[at]), 'light share quanta', int(b.share(b.light, b.rule((b.den, b.den), b.content(), b.link_factors()))[at]) // b.unit_light)
