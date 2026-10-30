"""The sign of each channel's table as the build makes it: the first nonzero entry of C[i, k -> m], positive or negative.
usage: python -I signs.py <a worktree of tensor24-review>"""
import sys

sys.path[:0] = [sys.argv[1] + "/src"]
from tensor24.main import made  # noqa: E402

held, c = made((3, 3, 3))
labels = tuple(name.upper() for name in held._fields)
negative, positive = [], 0
for (i, k, m), table in sorted(c.items()):
    if table.any():
        first = next(x for x in table.flat if x)
        if first > 0:
            positive += 1
        else:
            negative.append(f"{labels[i]} x {labels[k]} -> {labels[m]}")
print(f"channels {positive + len(negative)}; first nonzero entry positive on {positive}, negative on {len(negative)}")
print("negative:", ", ".join(negative))
