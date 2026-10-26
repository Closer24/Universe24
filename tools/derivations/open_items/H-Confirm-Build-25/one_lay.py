"""Two letters at one Node: the raised cosine's weights at the three half widths (the one Node's crest 4) and a child's levels as gram.moving's one lay (the now pair (sense A, 0), the before pair (0, sense B) along the unit vector)."""
import sys
sys.path.insert(0, "src")
sys.path.insert(0, ".")
from event_universe import gram, merger, seed
from tests.laws import node_of
for h in (1, 2, 3):
    print("half width", h, "weights", seed.raised_cosine(h))
try:
    seed.raised_cosine(4)
except ValueError as e:
    print("width 4 refused:", e)
node = node_of("world_hole.json")
for r in (1, 4):
    row = node.rows_[r]
    for sense in (-1, 1):
        got = merger.child_levels(row, sense, node.A, node.B)
        vector = [1] + [0] * (len(row.lines) - 1)
        lines = gram.moving(row.shape, 1, vector, (sense * node.A, 0), (0, sense * node.B), 1, sense)
        same = got == tuple(int(x) for line in lines for x in (line.now, line.before))
        print("row", r, "shape", row.shape, "sense", sense, "levels", got[:6], "of", len(got), "one lay", same)
print("A", node.A, "B", node.B, "A B", node.A * node.B, "T div 2", node.T // 2)
