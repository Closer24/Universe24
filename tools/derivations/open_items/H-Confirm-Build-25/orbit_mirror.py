"""The orbit's mirror read against the walked orbit (3dbfa2d10, 8bce04a58): the half turn H the table stops at, the table's length, and the mirror's pair at H + 1,000 and H + 10,000 beside the pair walked step by step from the seed, with their difference against X."""
import sys
sys.path.insert(0, "src")
sys.path.insert(0, ".")
from event_universe import readings
from event_universe.features import phase
from tests.laws import node_of

node = node_of("world_hole.json")
print("Gamma", node.gamma, "X", int(node.X))
readings.pair_angle(node, 1 << 20)
H = node.orbit_half
print("the half turn H", H, "the table's pairs", len(node.orbit))
print("the table's deepest cosine", min(c for c, _ in node.orbit), "against -X", -int(node.X))
walk_c, walk_s = node.orbit_lines and phase.seed(node.X, node.gamma)
deep = max(H + 10000, H + 1000)
reads = {}
c, s = phase.seed(node.X, node.gamma)
for n in range(1, deep + 1):
    c, s = phase.act(c, node.gamma, 1), phase.act(s, node.gamma, 1)
    if n in (H + 1000, H + 10000):
        reads[n] = (int(c[0]), int(s[0]))
for n in (H + 1000, H + 10000):
    m = readings.pair_angle(node, n)
    w = reads[n]
    print("count", n, "mirror", m, "walked", w, "apart", (m[0] - w[0], m[1] - w[1]), "of X", int(node.X))
