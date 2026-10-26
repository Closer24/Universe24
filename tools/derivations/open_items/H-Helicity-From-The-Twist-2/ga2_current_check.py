"""The ga2 450 check of the Node line's current against the close's: the world stepped to the start of the named interval through run.py (no direct import of node or interval), then at the named Links the gap-0 ROW's current (close.meet's flow, links.row_current over re and im) against the gap-0 LINE's (run.node_lines' current, the re line alone). Usage: python ga2_current_check.py <world.json> <interval> <x,y,z,axis> ..."""
import sys

from event_universe.core.ports import port_of
from event_universe.links import link_current, row_current
from event_universe.run import Node, load_world

universe, world = load_world(sys.argv[1])
node = Node(universe, world)
until = int(sys.argv[2])
for _ in range(until - 1):
    node.step()
print("interval ended", node.interval, "(the state at the start of", until, ")")
em = node.emitter()
for spec in sys.argv[3:]:
    x, y, z, axis = (int(v) for v in spec.split(","))
    at = (x, y, z)
    row = int(row_current(em.lines, port_of(axis, 0))[at])
    line = int(link_current(em.lines[0], port_of(axis, 0))[at])
    im = int(link_current(em.lines[1], port_of(axis, 0))[at])
    print({"at": at, "axis": axis, "row current (re + im, the close's flow)": row, "re line's current (the Node line's)": line, "im line's current": im, "im levels now, before at the Node": [int(em.lines[1].now[at]), int(em.lines[1].before[at])]})
