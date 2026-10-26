"""The intervals to frame from the record's integers: 1, the first top of the mean X (the first local maximum), the first bottom after it (local minimum), the end; and the rising/falling/rest counts of X against the interval before, at each."""
import json, sys
from pathlib import Path
out, name = Path(sys.argv[1]), sys.argv[2]
r = json.loads((out / f"{name}.json").read_text(encoding="utf-8"))
X = [[int(x) for x in l["X"]] for l in r["nodes"]]
mean = [sum(x) for x in X]  # the sum stands for the mean, the count constant
n = len(mean)
top = next((k for k in range(1, n - 1) if mean[k] >= mean[k - 1] and mean[k] > mean[k + 1]), None)
bottom = next((k for k in range(top + 1, n - 1) if mean[k] <= mean[k - 1] and mean[k] < mean[k + 1]), None) if top is not None else None
picks = [1] + [k + 1 for k in (top, bottom) if k is not None] + [n]
print("intervals", " ".join(map(str, picks)))
for i in picks:
    now, before = X[i - 1], X[max(i - 2, 0)]
    up = sum(a > b for a, b in zip(now, before)); down = sum(a < b for a, b in zip(now, before))
    print(f"interval {i}: sum X {mean[i-1]}; rising {up} falling {down} at rest {len(now) - up - down}")
