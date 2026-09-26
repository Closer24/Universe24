"""Write the two worlds of the dark body row (ALGEBRA.md 9.54 (4); the model owner's word of
2026-09-25 through the Boss, record 2015: "yes" to building it now, run only after he says the
engine is stable; BUILD.md section 26 item 39) and their expectations, declared blind from the
algebra before any run.

THE ROW: a beam of given light passes a body of content M standing 45 Links beside its line
and reaches a screen far ahead. THE DARK BODY (9.54 (2)): a block of the family `dark` (the
matter kind [800, 809] in the well [800, 801], its own record on its mode) with the charge 0,
no emitter (it gives nothing) and no detector set (it takes nothing): its content M is held
at its Nodes, the family of clicks reads it, every record's pace bends toward it, and nothing
of it is ever a click. THE BRIGHT CONTROL: the same M in a body of the light clock's family
`matter` at the same place, with an emitter of light (its own giving clicks) and a detector set
bound to its Nodes (its taking clicks, the shadow it casts on the beam). Both worlds are one
layer, 400 x 200 x 1, the beam along x at y = 100, x closed (mirrors), y open (a zero face
with the receiver slab), the Node clock 10^6 and the Node's own pace (item 36).

THE EXPECTATIONS (`expectations.json`; the pins are declared here from the algebra, blind, and
read only when the model owner says the engine is stable): (i) DARK, DETECTOR: every one of
the emitter's given records reaches the screen (the far count equals the stock), no click at
the dark body (it is on no set), no light from it (no giving line of its number); (ii) BRIGHT,
DETECTOR: the far count of the emitter's records falls short of the stock by the body's taking
clicks (the shadow), and the body's own giving lines exist; (iii) THE BEND, DETECTOR: the
centroid of the emitter's records' clicks over the screen's cubes moves toward the body's
side by the same amount in both worlds within one cube (3 Links), and by the ray equation's
number computed here (COMPUTATION: the discrete Coulomb field of the held M, 9.41 (3), solved
static on this board with the faces at 0, and the ray of the given clock [512, 1] traced
through it by 9.29's equations under the Node's own pace, 9.50 (13)) within 30 percent, the
packet's average of the gradient falling short of the ray's (9.29's table, the packet 15
percent under the ray); (iv) GAMEBOARD, diagnostics beside: the family of clicks' level at
the same distance from the two bodies equal within the rounding, the family of charge flat
around both (every family's charge 0).

Every number in the file is a COMPUTATION or a declaration; nothing here is a measurement."""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

SHAPE = [400, 200, 1]
BEAM_Y = 100  # the beam's line
BODY_CORNER = [184, 143, 0]  # the body's lower corner: its centre (200, 145), 45 Links beside the line
BODY_EXTENTS = [32, 5, 1]  # the train's length along x (a bright body's emitter needs it), 5 across
BODY_CONTENT = 4812  # M, the quanta held at every Node of the body: below Gamma = 10^4 (the load's guard), the static level on the beam's line under it 2000, U_b = 0.1 (100000 at Gamma 10^6 HISTORY)
EMITTER_CORNER = [5, 98, 0]  # the train's 32 Nodes along x, 5 wide across the beam
EMITTER_EXTENTS = [32, 5, 1]
STOCK = 30  # the emitter's given records, one per giving click
# the bright body's stock of light beside its own content (ALGEBRA.md 9.51 (8); BUILD.md
# section 26 item 47): the givings the run's ticks allow (83 read on the control) with room;
# its own quanta BODY_CONTENT - BRIGHT_STOCK, so the level at its Nodes stays BODY_CONTENT
BRIGHT_STOCK = 128
SCREEN_X = 380  # the screen's column, cubes of side 3 from y = 40 to 160
SCREEN_YS = range(40, 160)
TICKS = 2400  # the last giving near 30 x P / 2 intervals, the flight 340 Links at 0.447
NODE_CLOCK = 10_000  # Gamma = 10^4 (ALGEBRA.md 9.57 (2), 9.61 (3); item 44)
MATTER = [800, 809]
WELL = [800, 801]  # the emitter's well, the light clock's
BODY_WELL = WELL  # the body's well the emitter's: 32 by 5 binds its mode in [800, 801]
SEED = 1 << 18  # below the amplitude bound 2^20 (9.61 (3))
GIVEN_CLOCK = [512, 1]
READS = [
    {"family": "clicks", "weight": 1},
    {"family": "charge", "weight": 1, "by": "sign"},
]  # every reading family's `reads` (BUILD.md section 26 item 51): the content plainly, the charge by its own sign
DETECTOR_SIDE = 3


def load_generator(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def cube(document: dict, name: str, corner: list[int]) -> str:
    """One detector cube of side 3 of receiver bodies of light (record 1899), read as `name`."""
    positions = [
        [corner[0] + dx, corner[1] + dy, 0] for dx in range(DETECTOR_SIDE) for dy in range(DETECTOR_SIDE)
    ]
    for position in positions:
        document["measured"].append(
            {
                "position": position,
                "family": "light",
                "amount": 1,
                "momentum": [0, 0, 0],
                "held": {},
            }
        )
    document["detectors"].append({"name": name, "positions": positions})
    return name


def block(
    corner: list[int],
    extents: list[int],
    family: str,
    amount: int,
    emitter: dict | None,
    well: list[int] = WELL,
    stock: int | None = None,
) -> dict:
    entry: dict = {
        "position": list(corner),
        "family": family,
        "amount": amount,
        "momentum": [0, 0, 0],
        "held": {},
        "ramp": 0,
        "start": 0,
        "extents": list(extents),
        "pair": list(well),
        "seed": SEED,
        "margin": "control",
    }
    if emitter is not None:
        # the stock as the given family's content held at the body (ALGEBRA.md
        # 9.51 (8); BUILD.md section 26 item 47): without `stock`, one own quantum
        # and `amount` givings; with it, `stock` givings beside amount - stock own
        # quanta (the level at the Nodes `amount`, the bright body's field)
        entry["emitter"] = emitter
        entry["amount"] = 1 if stock is None else amount - stock
        entry["held"] = {emitter["family"]: amount if stock is None else stock}
        assert entry["amount"] >= 1
    return entry


def world(dark: bool) -> dict:
    """The dark world (True) or the bright control (False)."""
    document: dict = {
        "law": "beam",
        "model_id": "beam-dark-body-v1" if dark else "beam-dark-body-bright-control-v1",
        "shape": list(SHAPE),
        "boundary": {"x": "closed", "y": "open", "z": "periodic"},
        "face_depth": 1,
        "ticks": TICKS,
        "K": 1073741824,
        "N": 1024,
        "release": [1, 128],
        "width": 1,
        "clock_stamp": True,
        "detector_law": True,
        "massive_record": True,
        "body_record": False,
        "point_emitter": False,
        "engine": "examples/events/engine_start.json",
        "amplitude_bound": 1 << 20,  # the integers of 9.61 (3) (item 44)
        "node_clock": NODE_CLOCK,
        "families": [
            {
                "name": "light",
                "quantum": 1,
                "pair": [1, 1],
                "phase_per_link": list(GIVEN_CLOCK),
                "charge": 0,
                "reads": [dict(read) for read in READS],
            },
            {
                "name": "matter",
                "quantum": 1,
                "pair": list(MATTER),
                "charge": 0,
                "reads": [dict(read) for read in READS],
            },
            {
                "name": "dark",
                "quantum": 1,
                "pair": list(MATTER),
                "charge": 0,
                "reads": [dict(read) for read in READS],
            },
            {
                "name": "clicks",
                "quantum": 1,
                "pair": [1, 1],
                "charge": 0,
                "held": "content",
                "reads": [],
            },
            {"name": "charge", "quantum": 1, "pair": [1, 1], "charge": 0, "held": "sign", "reads": []},
        ],
        "measured": [],
        "detectors": [],
    }
    screen_names = [f"screen_{y}" for y in range(SCREEN_YS.start, SCREEN_YS.stop, DETECTOR_SIDE)]
    ladder = screen_names if dark else ["at_body", *screen_names]
    document["measured"].append(
        block(
            EMITTER_CORNER,
            EMITTER_EXTENTS,
            "matter",
            STOCK,
            {
                "family": "light",
                "receiver": ladder,
                "train": {"direction": [1, 0, 0], "periods": 8},
            },
        )
    )
    if dark:
        document["measured"].append(
            block(BODY_CORNER, BODY_EXTENTS, "dark", BODY_CONTENT, None, BODY_WELL)
        )
    else:
        document["measured"].append(
            block(
                BODY_CORNER,
                BODY_EXTENTS,
                "matter",
                BODY_CONTENT,
                {
                    "family": "light",
                    "receiver": screen_names,
                    "train": {"direction": [1, 0, 0], "periods": 8},
                },
                BODY_WELL,
                stock=BRIGHT_STOCK,
            )
        )
        document["detectors"].append({"name": "at_body", "block": 1})
    for y in range(SCREEN_YS.start, SCREEN_YS.stop, DETECTOR_SIDE):
        cube(document, f"screen_{y}", [SCREEN_X, y, 0])
    massive = load_generator(
        ROOT / "examples/events/massive_record/make_worlds.py", "massive_record_make_worlds"
    )
    massive.seed_on_the_mode(document)
    return document


def static_field() -> np.ndarray:
    """THE DISCRETE COULOMB FIELD (ALGEBRA.md 9.41 (3); COMPUTATION): the family of clicks'
    static level on this layer with the body's Nodes held at M and the faces at 0 (the zero
    faces of every family), the plain step's fixed point: at every free Node four times the
    level is the sum of its four neighbours (the folded axis reads the Node itself twice)."""
    from scipy.sparse import lil_matrix
    from scipy.sparse.linalg import spsolve

    nx, ny = SHAPE[0], SHAPE[1]
    held = np.zeros((nx, ny), dtype=bool)
    held[
        BODY_CORNER[0] : BODY_CORNER[0] + BODY_EXTENTS[0],
        BODY_CORNER[1] : BODY_CORNER[1] + BODY_EXTENTS[1],
    ] = True
    index = -np.ones((nx, ny), dtype=np.int64)
    free = np.nonzero(~held)
    index[free] = np.arange(free[0].size)
    n = free[0].size
    matrix = lil_matrix((n, n))
    rhs = np.zeros(n)
    for row, (x, y) in enumerate(zip(free[0].tolist(), free[1].tolist(), strict=True)):
        matrix[row, row] = 4.0
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            xx, yy = x + dx, y + dy
            if not (0 <= xx < nx and 0 <= yy < ny):
                continue  # a zero face beyond the board
            if held[xx, yy]:
                rhs[row] += BODY_CONTENT
            else:
                matrix[row, index[xx, yy]] = -1.0
    solution = spsolve(matrix.tocsr(), rhs)
    field = np.full((nx, ny), float(BODY_CONTENT))
    field[free] = solution
    return field


def ray_bend(field: np.ndarray) -> float:
    """THE RAY (ALGEBRA.md 9.29's equations under the Node's own pace, 9.50 (13); COMPUTATION):
    a ray of the given clock k = (pi / 2, 0) from the train's head at the beam's line, dx / dt
    = p sin k_x / (3 Gamma sin omega'), dy / dt = p sin k_y / (3 Gamma sin omega'), d k_y / dt
    = (1 - cos omega_k) / (Gamma sin omega') x dc / dy, with cos omega' = 1 - (p / Gamma)(1 -
    cos omega_k), p = Gamma - c the pace at the ray's place, c the static field read there
    (bilinear); its transverse shift in Links when it reaches the screen's column."""
    gamma = float(NODE_CLOCK)
    kx, ky = math.pi / 2, 0.0
    x, y = float(EMITTER_CORNER[0] + EMITTER_EXTENTS[0]), float(BEAM_Y)
    dt = 0.25

    def read(px: float, py: float) -> tuple[float, float]:
        ix, iy = int(math.floor(px)), int(math.floor(py))
        fx, fy = px - ix, py - iy
        ix = min(max(ix, 0), SHAPE[0] - 2)
        iy = min(max(iy, 0), SHAPE[1] - 2)
        c00, c10, c01, c11 = field[ix, iy], field[ix + 1, iy], field[ix, iy + 1], field[ix + 1, iy + 1]
        value = (1 - fx) * (1 - fy) * c00 + fx * (1 - fy) * c10 + (1 - fx) * fy * c01 + fx * fy * c11
        slope_y = (1 - fx) * (c01 - c00) + fx * (c11 - c10)
        return value, slope_y

    while x < SCREEN_X:
        c, slope = read(x, y)
        cos_k = (math.cos(kx) + math.cos(ky) + 1.0) / 3.0
        pace = gamma - c
        cos_w = 1.0 - (pace / gamma) * (1.0 - cos_k)
        sin_w = math.sqrt(max(1.0 - cos_w * cos_w, 1e-12))
        x += dt * pace * math.sin(kx) / (3.0 * gamma * sin_w)
        y += dt * pace * math.sin(ky) / (3.0 * gamma * sin_w)
        ky += dt * (1.0 - cos_k) / (gamma * sin_w) * slope
    return y - BEAM_Y


def expectations(bend: float) -> dict:
    band = 0.3
    return {
        "row": "the dark body (ALGEBRA.md 9.54 (4); BUILD.md section 26 item 39)",
        "declared": "before any run, from the algebra; read only when the model owner says the engine is stable",
        "pins": {
            "dark_far_count_equals_stock": {
                "kind": "DETECTOR",
                "value": STOCK,
                "reading": "the clicks of the emitter's records (their identities 0 x 2^32 + n) at the screen's cubes",
            },
            "dark_no_click_at_the_body": {
                "kind": "DETECTOR",
                "value": 0,
                "reading": "no set on the dark body: no line names it",
            },
            "dark_no_light_from_the_body": {
                "kind": "DETECTOR",
                "value": 0,
                "reading": "no giving line of measured 1 in the dark world",
            },
            "bright_far_count_below_stock": {
                "kind": "DETECTOR",
                "value": STOCK,
                "reading": "the emitter's records' clicks at the screen fewer than the stock, the rest at at_body (the shadow)",
            },
            "bright_body_gives": {
                "kind": "DETECTOR",
                "value": 1,
                "reading": "at least one giving line of measured 1",
            },
            "bend_links": {
                "kind": "DETECTOR",
                "value": bend,
                "band": [bend * (1 - band), bend * (1 + band)],
                "reading": "the centroid of the emitter's records' clicks over the screen's cubes, in y, less the beam's line (toward the body positive), the same in both worlds within one cube (3 Links)",
                "computed": "the ray of the given clock through the static Coulomb field of the held M (9.41 (3), 9.29, 9.50 (13))",
            },
        },
        "diagnostics": {
            "clicks_level_equal_around_both": "GAMEBOARD: the family of clicks' level 10 Links beside each body's centre, dark against bright, within the rounding",
            "charge_flat": "GAMEBOARD: the family of charge 0 everywhere in both worlds (every family's charge 0)",
        },
    }


def main() -> None:
    for name, dark in (("dark", True), ("bright", False)):
        document = world(dark)
        (HERE / f"{name}.json").write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(name, flush=True)
    bend = ray_bend(static_field())
    (HERE / "expectations.json").write_text(
        json.dumps(expectations(bend), indent=1) + "\n", encoding="utf-8"
    )
    print(f"the ray's bend {bend:.2f} Links (COMPUTATION)")


if __name__ == "__main__":
    main()
