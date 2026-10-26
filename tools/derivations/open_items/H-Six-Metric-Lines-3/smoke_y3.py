import sys, os, time
sys.set_int_max_str_digits(0)
from tests.laws import node_of, run_back_exact, state_of
name, n, back = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
t0 = time.time()
node = node_of(name)
for _ in range(n - back):
    node.step()
kept = []
for _ in range(back):
    kept.append(state_of(node)); node.step()
h = node.state_hash()
exact = sum(state_of(node) == kept[back - 1 - k] for k in range(back) if not node.step_back())
print(name, n, "hash", h[:16], "births", node.counts["births"], "credits", node.counts["body_clicks"], "turns", node.counts["turns"], "run back", exact, "of", back, "census", node.census(), "s", round(time.time() - t0, 1))
