"""Written by the Light for world (e) until the Clock's tools/pixel_mode.py lands; run from the repository root: PYTHONPATH=src python examples/events/experiments/rule/pixel_modes_by_hand.py <world.json> ... The mode files of world (e)'s pixels by the recipe of the Closer's line (13:54 Israel) until the Clock's tool: the giver's profile isqrt(c) at its Node over the whole board, the clock pair from Cheshbon's line (13:51), the twist 0, the light's wavelength 4; the taker content alone; the world's digest by the generator's function."""

import json
import math
import sys

sys.path.insert(0, "tools")
from pathlib import Path

from body_generator import input_digest

CLOCK = {3000: [90326, 65536], 4000: [103722, 65536], 2706: [87388, 65536], 5000: [114155, 65536]}
for path in map(Path, sys.argv[1:]):
    world = json.loads(path.read_text(encoding="utf-8"))
    shape = world["shape"]
    total = shape[0] * shape[1] * shape[2]
    bodies = []
    for body in world["measured"]:
        node, count = body["nodes"][0]["node"], int(body["nodes"][0]["count"])
        if "emitter" in body:
            profile = [0] * total
            profile[(node[0] * shape[1] + node[1]) * shape[2] + node[2]] = math.isqrt(count)
            bodies.append(
                {
                    "family": body["family"],
                    "pair": [2, 3],
                    "profile": profile,
                    "clock": CLOCK[count],
                    "twist": 0,
                    "wavelength": 4,
                    "wave_number": 0,
                    "amplitude_unit": math.isqrt(count),
                    "recipe": "by hand: isqrt(c) at the Node, Cheshbon's clock pair, until tools/pixel_mode.py",
                }
            )
        else:
            bodies.append(
                {
                    "family": body["family"],
                    "pair": [2, 3],
                    "mode": "none: no giving and no momentum, the body loads as content alone",
                }
            )
    mode = {
        "rest": {},
        "bodies": bodies,
        "world_digest": input_digest(json.loads(path.read_text(encoding="utf-8"))),
    }
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    print(path.with_suffix(".mode.json"), "written")
