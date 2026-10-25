"""Probe: why do Nodes turn on a board with no sea (the floor X_f against the vacuum's X)."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'toy'))
import numpy as np
from lean_full import Lean, load_world
universe, world = load_world(sys.argv[1])
b = Lean(universe, world)
m = b.row(10).lines[0]
print('X at vacuum Node (0,0,0):', int(m.now[0,0,0]), int(m.before[0,0,0]), 'floor X_f:', b.floor(), 'content there:', int(b.content()[0,0,0]))
b.step()
print('after 1 interval: X now/before at (0,0,0):', int(m.now[0,0,0]), int(m.before[0,0,0]), 'turned there:', bool(b.turned[0,0,0]), 'turns:', b.counts['turns'])
print('X at centre:', int(m.now[4,4,4]), int(m.before[4,4,4]), 'turned:', bool(b.turned[4,4,4]))
