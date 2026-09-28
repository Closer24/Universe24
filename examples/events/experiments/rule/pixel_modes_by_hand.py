"""The mode files of world (e)'s pixels by Cheshbon's recipe of the bound state (2026-09-28, 14:12 Israel; the Moving Clock's `tools/pixel_mode.py` writes the same when it lands): a pixel of the count c with the clock pair [a, den] of 2 cos omega_b carries the level b = isqrt(c T den div (2 den - a)) at its Node (the count through the form D = now^2 - next before at rest) and the tail b t^(|dx| + |dy| + |dz|) rounded at every Node until it falls under 1, t = e^(-kappa) as a pair over 2^16, both time levels equal (the standing phase); the taker content alone where it gives nothing. The pairs per count are Cheshbon's lines: under the conformal term (the edge 2,706) and under the engine of today (the level once, the edge 4,136). Run from the repository root: PYTHONPATH=src python examples/events/experiments/rule/pixel_modes_by_hand.py [--today] <world.json> ..."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from body_generator import input_digest  # noqa: E402

DEN = 65536  # den of the clock pair [a, den] and of the tail's pair [t, 65536]
# per count: [a, t] with 2 cos omega_b = a / DEN and e^(-kappa) = t / DEN (Cheshbon, 13:51 and 14:12 Israel)
WITH_THE_TERM = {
    2706: (87388, 64160),
    3000: (90326, 41943),
    4000: (103722, 23724),
    5000: (114155, 18415),
}
TODAY = {
    5000: (93270, 34734),
    6000: (102490, 24904),
    7000: (110576, 19661),
}  # 2 cos of 0.778, 0.674, 0.564; t 0.53, 0.38, 0.30


def profile_of(shape: list[int], node: list[int], count: int, a: int, t: int) -> list[int]:
    """The bound state's integer profile over the whole board, x-major: b at the Node, b t^d rounded at the distance d (the sum of the axes' distances) while it stays at least 1."""
    b = math.isqrt(count * DEN // (2 * DEN - a))  # T = 1, the unit of the rule's universe
    levels = [0] * (shape[0] * shape[1] * shape[2])
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                d = abs(x - node[0]) + abs(y - node[1]) + abs(z - node[2])
                level = (b * t**d + DEN**d // 2) // DEN**d if d else b
                if level >= 1:
                    levels[(x * shape[1] + y) * shape[2] + z] = level
    return levels


def main(argv: list[str]) -> int:
    today = "--today" in argv
    table = TODAY if today else WITH_THE_TERM
    for path in (Path(p) for p in argv if not p.startswith("--")):
        world = json.loads(path.read_text(encoding="utf-8"))
        shape = world["shape"]
        pair = list(world.get("pair", [8000, 12000]))
        bodies = []
        for body in world["measured"]:
            node, count = body["nodes"][0]["node"], int(body["nodes"][0]["count"])
            if "emitter" not in body:
                bodies.append(
                    {
                        "family": body["family"],
                        "pair": pair,
                        "mode": "none: no giving and no momentum, the body loads as content alone",
                    }
                )
                continue
            a, t = table[count]
            profile = profile_of(shape, node, count, a, t)
            bodies.append(
                {
                    "family": body["family"],
                    "pair": pair,
                    "profile": profile,
                    "clock": [a, DEN],
                    "moving": {"now": profile, "before": list(profile)},
                    "twist": 0,
                    "wavelength": 4,
                    "wave_number": 0,
                    "recipe": f"the bound state by Cheshbon's line: b = isqrt(c T den div (2 den - a)) at the Node, the tail b t^d, {'the engine of today' if today else 'under the conformal term'}",
                }
            )
        mode = {
            "rest": {},
            "bodies": bodies,
            "world_digest": input_digest(json.loads(path.read_text(encoding="utf-8"))),
        }
        path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
        print(path.with_suffix(".mode.json"), "written")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
