"""The decoder reads the engine's own beats (Animate): on the stage 4 engine under random masks (the Mesh test's parted
layouts: teeth, rates and grips parted at every site and Mesh, one clock stopped), each Node-clock's rate lines are
written at its first beat and at each beat whose k differs from its last beat's, with the count the beat reached and
the dial after it, into a record of the schema 1.0 (the header, the rate lines in the schema's order, the end). The
record is read by src/tensor24/decoder, and the ticks to every beat are read back by clocks.ticks_to against the k the
engine put out; a Node-clock's lines with their first dropped, and a whole click at a site with no rate line, read not
read with the cause named. Run from anywhere: python -I engine_rates.py <worktree> <scratch folder>.
"""

import json
import sys
from pathlib import Path

sys.path[:0] = [sys.argv[1] + "/src", sys.argv[1]]

from tensor24.decoder import clocks, records  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tests.test_the_tensor24_mesh import T, parted  # noqa: E402

OUT = Path(sys.argv[2])


def run(seed):
    layout, s, rng = parted(seed)
    n = s.c.shape[1]
    lines, last, truth, rounds = [], [None] * n, [[] for _ in range(n)], 0
    while (s.c < T).any() and rounds < 60 * T:
        allowed = rng.integers(0, 2, size=s.c.shape).astype(object)
        s, out = step.tick(layout, s, allowed)
        rounds += 1
        for i in range(n):
            fire, k, count = int(out.fire[0, i]), int(out.k[0, i]), int(s.c[0, i])
            if fire:
                truth[i].append((count, k))
                if last[i] != k:
                    lines.append(
                        {
                            "kind": "rate",
                            "round": rounds,
                            "site": i,
                            "count": count,
                            "dial": int(s.ph[0, i]),
                            "k": k,
                        }
                    )
                    last[i] = k
    header = {
        "kind": "header",
        "record": "tensor24",
        "major": 1,
        "minor": 0,
        "runner": f"random masks, seed {seed}",
    }
    end = {"kind": "end", "rounds": rounds, "undone": 0, "exact": 1}
    path = OUT / f"rates_{seed}.jsonl"
    path.write_text("".join(json.dumps(x) + "\n" for x in [header, *lines, end]), encoding="utf-8")
    record, cause = records.read(str(path))
    if record is None:
        return {"not read": cause}
    held = clocks.stretches(record)
    asked = right = 0
    for i in range(n):
        ticks = 0
        for count, k in truth[i]:
            ticks += k
            asked += 1
            right += clocks.ticks_to(held.get(i, []), count) == ticks
    beaten = [i for i in range(n) if truth[i]]
    first = beaten[0]
    cut = (
        clocks.ticks_to(held[first][1:], truth[first][-1][0]),
        clocks.unread(held[first][1:], truth[first][-1][0]),
    )
    alone = clocks.ticks_to([], 1), clocks.unread([], 1)
    return {
        "rounds": rounds,
        "beats": asked,
        "rate lines": len(lines),
        "ticks read back right at every beat": f"{right} of {asked}",
        "a Node-clock's lines with the first dropped": cut,
        "a site with no rate line": alone,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for seed in (0, 1, 1 + 1):
        print(f"seed {seed}: {run(seed)}")


if __name__ == "__main__":
    main()
