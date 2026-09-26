"""The reading of row (3) of ALGEBRA.md 9.59, the bending on today's law, from the one
command's outputs of the dark body's two worlds (`../dark_body/dark.json`, `bright.json`;
9.54 (4)), every number labelled; no pin, no verdict (9.59 (6)): the row's own pins in
`../dark_body/expectations.json` are not read here.

DETECTOR: per world the clicks of the emitter's records (identities 0 x 2^32 + n) at the
screen's cubes, their count, the centroid of the cubes' centre y less the beam's line
(toward the body positive) with its standard error, the clicks at the body's set and the
body's own records' clicks (bright). COMPUTATION: set beside, the closed form of 9.59 (3)
for this geometry, 2 U_b L with U_b = c_b / (2 Gamma) at the beam's closest distance b from
the body's centre and L the screen's distance beyond the body, c_b read from the declared
content as the static field of the row's generator (`../dark_body/make_worlds.py::
static_field`, a Laplace solve, COMPUTATION), and the ray through that field
(`ray_bend`).

    PYTHONPATH=src python examples/events/toward_nature/read_bending.py <out dir> [--bending]
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DARK = HERE.parent / "dark_body"


def load_generator():
    spec = importlib.util.spec_from_file_location("dark_body_make_worlds", DARK / "make_worlds.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["dark_body_make_worlds"] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def screen_reading(path: Path, beam_y: int, side: int) -> None:
    out = json.loads(path.read_text(encoding="utf-8"))
    clicks = out.get("clicks", [])
    emitter = [c for c in clicks if (c.get("record", 0) >> 32) == 0]
    body = [c for c in clicks if (c.get("record", 0) >> 32) != 0]
    screen = [c for c in emitter if str(c["detector"]).startswith("screen_")]
    ys = [int(str(c["detector"]).split("_")[1]) + side // 2 - beam_y for c in screen]
    print(
        f"DETECTOR {path.name}: verdict {out.get('verdict')}, {len(clicks)} clicks in all; the emitter's records {len(emitter)} (at the screen {len(screen)}), the body's records {len(body)}"
    )
    per = {}
    for c in emitter:
        per[c["detector"]] = per.get(c["detector"], 0) + 1
    print(f"  the emitter's records per set: {dict(sorted(per.items()))}")
    if ys:
        mean = sum(ys) / len(ys)
        rms = math.sqrt(sum((y - mean) ** 2 for y in ys) / len(ys))
        print(
            f"  centroid of the emitter's clicks over the screen less the beam's line (toward the body positive): {mean:.2f} Links, rms {rms:.2f}, standard error {rms / math.sqrt(len(ys)):.2f}, {len(ys)} clicks"
        )
    if body:
        per_body = {}
        for c in body:
            per_body[c["detector"]] = per_body.get(c["detector"], 0) + 1
        print(f"  the body's own records per set: {dict(sorted(per_body.items()))}")


def bending_generator():
    spec = importlib.util.spec_from_file_location("toward_nature_make_worlds", HERE / "make_worlds.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["toward_nature_make_worlds"] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.bending_generator()


def main(folder: Path, names: tuple[str, ...] = ("dark", "bright")) -> None:
    generator = bending_generator() if names == ("bending",) else load_generator()
    print(
        f"== ROW (3) THE BENDING ON TODAY'S LAW (ALGEBRA.md 9.59 (3)): {'row (3) world' if names == ('bending',) else 'the dark body two worlds (9.54 (4)) as they stand'}"
    )
    side = generator.DETECTOR_SIDE
    for name in names:
        path = folder / f"{name}.output.json"
        if path.exists():
            screen_reading(path, generator.BEAM_Y, side)
        else:
            print(f"{name}: no output")
    gamma = generator.NODE_CLOCK if hasattr(generator, "NODE_CLOCK") else None
    body_centre_y = generator.BODY_CORNER[1] + generator.BODY_EXTENTS[1] // 2
    body_centre_x = generator.BODY_CORNER[0] + generator.BODY_EXTENTS[0] // 2
    b = body_centre_y - generator.BEAM_Y
    length = generator.SCREEN_X - body_centre_x
    field = generator.static_field()
    c_b = float(field[body_centre_x, generator.BEAM_Y])
    print(
        f"COMPUTATION the geometry: b = {b} Links from the body's centre to the beam, L = {length} Links from the body's centre to the screen, the level on the beam's line under the body c_b = {c_b:.1f} (the static field of the declared content, a Laplace solve), Gamma = {gamma}"
    )
    if gamma:
        u_b = c_b / (2 * gamma)
        print(
            f"COMPUTATION set beside: 2 U_b L = {2 * u_b * length:.2f} Links (today's law, 9.59 (3)); the Einstein form's 4 U_b L = {4 * u_b * length:.2f}; the ray through the static field {generator.ray_bend(field):.2f} (the row's generator)"
        )
    print("  a direction, not a pin: the row's pins are not read (9.59 (6))")


if __name__ == "__main__":
    main(Path(sys.argv[1]), ("bending",) if "--bending" in sys.argv[2:] else ("dark", "bright"))
