"""The check worlds of the massive record kind (`massive-record-v1`; the chief
physicist's design docs/designs/detector_law/MASSIVE_RECORD.md section 11, the
build's plan docs/designs/detector_law/BUILD.md section 5), written by this
script from the design's declarations, each a CONTROL, a PIN or a PREDICTION
world named so in its file; every pin is written by `pins.py` into
`expectations.json` before its world runs and never moved after it.

The pairs (BUILD.md section 5): at mu = 0.15 the medium D_out = 1 + mu^2 / 2 =
809 / 800 is the kind `[800, 809]`; the well at full depth g = mu^2 is D_in = 1,
the pair `[800, 800]`; at half depth g = mu^2 / 2 the kind is written
`[1600, 1618]` and the well `[1600, 1609]`. The drive: the wall 3 Q S M = 192
at Q = 64, width 1, amount 1, so the momentum 64 on an axis is one Link every
three intervals (k = 3, beta_c = 1 / sqrt 3, gamma_m = sqrt(3 / 2)) and 48 is
k = 4. The massive kind's faces are periodic by default (the medium
continuous) with the margin rule of section 11 item 4 checked at load; the
chains' light faces are open on x (light's row zero beyond the ends), as the
design's chain scripts have them (the index script's window before the ends'
reflections reach the probe; on the moving-index chains a face's reflection
reaches the probe inside the long chain's window, named in the readings; a
trial with light's faces periodic, the script's np.roll, moved the rest
readings away from the script's numbers by the wrapped wave and was not kept).

- (i-a) `rest_20.json`, (i-b) `rest_28.json`: one block at rest on a periodic
  48^3 board, 3000 intervals: CONTROL worlds (the block's own clock against
  section 4's threshold table; the extent and the margin printed at load).
- (ii-a) `moving_20.json`, (ii-b) `moving_28.json`: the same blocks pushed to
  k = 3 on a periodic 64^3 board over a ramp of 1500 intervals and a hold of
  8000: PREDICTION worlds (the one formula of section 8 per world on its own
  box, `massive_moving_pins.py`: 0.7831 and 0.8048), with the pump's two
  GAMEBOARD readings (light's energy drift, the mode k = 2 pi / 3 on x).
- (iii-a) `cavity_24.json`: the rest cavity of form (I), side 24, the kind's
  own pair, on 48^3: a CONTROL (the separable form's omega 0.19503);
  (iii-b) `cavity_24_moving.json`: the cavity pushed to k = 3 on 64^3: the
  CONTROL of the medium's clock (1 / gamma_m^2).
- (v) `index_50.json`, `index_20.json`, `index_10.json` and
  `index_reference.json`: the index block at rest on a chain of 1400 (the
  kind `[7, 8]`; a block of side 12 at x = 900 with seed 0, a CAVITY with the
  kind's own pair, the design script's oscillator held at 0 outside its
  cells; G `[1, 1]` and g 1 / 50, 1 / 20, 1 / 10; the light clock `[153, 100]` on N = 64, omega
  0.150214; a lamp at x = 600, a probe at x = 1100): CONTROL of the coupling
  (the closed form n^2 = 1 + G g / (omega_0^2 - omega^2)).
- (v-m) `index_moving_k3_toward.json`, `index_moving_k3_away.json` and the
  same at k = 4: the moving index on the design's chain of 2200 (the source
  at 300, the probe at 1500, s = 24, the kind `[156, 157]`, the well
  `[314, 315]`, g `[1, 200]`, G `[1, 1]`, light at omega 0.035, the block
  stepping from interval 2600 toward the source from x = 1300 or away from
  x = 700): PREDICTION worlds of the model as built (the same-Node ratios of
  `massive_moving_index.out`), never Fizeau's; beside them the block at
  rest at x = 1100 read at omega and at the block-frame frequencies of each
  K (`index_moving_rest_*.json`) with a reference without the block at each
  clock (`index_moving_reference_*.json`), from which the covariant
  expectation is formed on the engine's own chain as the script forms it;
  and the design's receding case on the longer chain, where its pin from
  behind is read (`index_moving_long_*.json`: n = 4000, the source at 300,
  the probe at 2500, the block from x = 1500 from interval 2600, the window
  [5000, 6000]; the rest world at omega' away at x = 2100).

- (i-L) `layer_pin_rest_14.json`, (ii-L) `layer_pin_k3_14.json`: the layer pin world
  of MASSIVE_RECORD.md section 11 item 7 (mu = 0.15, s = 14, g = mu^2 / 4 on a
  periodic 200 x 200 x 1 layer, `margin` "pin"), the seed the bound mode's integer
  profile at 2^20 over the whole layer (the generator's integers in the file, the
  same at both levels: the reader of record is the clicks, which a flat seed makes
  beat on a wide mode); at rest and pushed to k = 3 over the ramp 10000 and the hold
  8000 (the ticks 18500: the ramp declared by the well's relaxation time, ten times
  1 / (omega_0 - omega_b) = 1027 intervals, DECLARATIONS.md section 8): PIN worlds
  (layer), the pin the mode's period and the one formula at the exact cone.

- The launch list's worlds (RUN_LIST.md on `detector-law-design`, the declarations
  DECLARATIONS.md sections 4, 10 and 11; the Boss's order of 2026-09-23 23:40Z item
  (c): every world generated from its declaration, no number of the builder's own):
  (4b) `redshift_k3.json` and `redshift_control.json` (NOT WRITTEN: refused at load by
  MUST 3 with the declared g = [1, 50000], see `launch_list_worlds`; section 4, the second draft:
  the chain of 2200, the emitter A of side 12, the well [314, 315] in [156, 157],
  the flat seed 2^20, `emits` light with G [1, 1] and g [1, 50000], W = 64, A at
  x = 700 pushed to k = 3 on -x over the ramp 1500, the control A at rest at x = 1300;
  the light detector B a receiver body at x = 1900, 9500 intervals; the stock A holds
  of light one unit per interval of the run, an inert bound on the births); the deep
  well in motion `deep_well_k3_40.json` and `deep_well_rest_40.json` (a 128^2 layer,
  s = 40 at full depth [800, 800] in [800, 809], the flat seed, the ramp 1500 and the
  hold 8000; the block centred, the rest world's 3500 intervals the series' rest
  length, as the layer pin's rest world keeps 3500 on main); (v-m) the long chains REGENERATED on section 11's geometry (the chain of
  4000, the source at 800, the probe at 2400, the block from x = 1500 stepping away
  from interval 3000, the window [3800, 5400]); and `EXPLORATORY_light_clock_60.json`
  (NOT WRITTEN, refused by MUST 3 as 4b's; section 10 read by PROBES only: the chain of 673, A at [600, 612) at full depth,
  g [1, 50000], the open face at 672 the mirror, the probes at x = 612 and 613 and
  2000 intervals; the pinned file `light_clock_60.json` waits on the physicist's
  line for the face detector, since a receiver body at x = 612 on a chain takes the
  whole line and nothing returns from the mirror through it).

Run from the repository root:

    PYTHONPATH=src python examples/events/massive_record/make_worlds.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from event_universe.events.world import BLOCK_SEED

HERE = Path(__file__).resolve().parent
PERIODIC = {"x": "periodic", "y": "periodic", "z": "periodic"}
CHAIN = {"x": "open", "y": "periodic", "z": "periodic"}
FACES_OPEN = {"x": "open"}
AGE_BOUND = 1 << 20
AMPLITUDE_BOUND = 1 << 32
MOMENTUM_K3 = 64
MOMENTUM_K4 = 48
# The layer pin world's push (DECLARATIONS.md section 8): the ramp ten relaxation times of
# the well (1027 intervals), the hold 8000 after it, the ticks 18500 (500 more, the hold
# read over [10200, 18200] by RUN_LIST.md).
LAYER_RAMP = 12000  # ten relaxation times of the well by the margin module's own omega_b on the 200^2 layer (1164.6 intervals; the design script's 1027 the estimate), the model owner's word of 2026-09-24, 16:48Z: the body's conditions checked at load
LAYER_HOLD = 8000
BLOCK_KEYS = (
    "coupling",
    "seed",
    "cavity",
    "ramp",
    "start",
    "margin",
    "held",
    # the emitter as a clicking body (ALGEBRA.md 9.17; BUILD.md section 26)
    "emitter",
    "receiver",
)


def world(
    name: str,
    kind: str,
    shape: list[int],
    boundary: dict[str, str],
    pair: list[int],
    blocks: list[dict],
    ticks: int,
    light: dict | None = None,
    faces: dict[str, str] | None = None,
    lamp: dict | None = None,
    probes: list[list[int]] | None = None,
    mode_axis: str | None = None,
    seed_profile: bool = True,
) -> dict:
    """One world file: light's family with its clock, the massive kind `matter` with
    its pair (and its faces where the chain's are open), the blocks as measured
    events with `side`, the lamp and the probes of the index worlds; every bound body's
    seed on its mode (`seed_on_the_mode`) unless `seed_profile` is off, for a caller that
    completes the document first (the detector-law generator's emitters) and calls it then."""
    matter: dict = {"name": "matter", "quantum": 1, "pair": pair}
    if faces is not None:
        matter["faces"] = faces
    families = [light or {"name": "light", "quantum": 1, "phase_per_link": [77, 25]}, matter]
    if any(block.get("family") == "source" for block in blocks):
        # the emitter bodies' own family (`emitter_at`): the kind SOURCE_KIND
        families.append({"name": "source", "quantum": 1, "pair": list(SOURCE_KIND)})
    measured: list[dict] = []
    if lamp is not None:
        measured.append(lamp)
    for block in blocks:
        entry: dict = {
            "position": block["position"],
            "family": block.get("family", "matter"),
            "amount": block.get("amount", 1),
            "phase": 0,
            "momentum": block.get("momentum", [0, 0, 0]),
            "fixed": True,
            "side": block["side"],
            "pair": block["pair"],
        }
        for key in BLOCK_KEYS:
            if key in block:
                entry[key] = block[key]
        measured.append(entry)
    document: dict = {
        "law": "beam",
        "model_id": f"beam-massive-record-{name}-v1",
        "shape": shape,
        "boundary": boundary,
        "ticks": ticks,
        "age_bound": AGE_BOUND,
        "K": 1073741824,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "clock_stamp": True,
        "detector_law": True,
        "massive_record": True,
        # the amplitude bound A every row stays below (DECLARATIONS.md section
        # 15 M1-10: 2^32 in every massive world; MUST 3 at that A, the rows
        # asserted below it at run time)
        "amplitude_bound": AMPLITUDE_BOUND,
        "directions": [],
        "families": families,
        "measured": measured,
        "detectors": [],
    }
    if probes is not None:
        document["probes"] = probes
    if mode_axis is not None:
        document["mode_axis"] = mode_axis
    if seed_profile:
        seed_on_the_mode(document)
    return document


def seed_on_the_mode(document: dict) -> None:
    """Every bound body's seed as the bound mode's integer profile over the whole board at
    the declared amplitude (the model owner's word of 2026-09-24, 16:48Z, through the Boss:
    the body's algebraic conditions exact in the initial state, the whole board carrying the
    mode's values; the engine's `check_body_conditions` refuses a body whose initial state
    differs from it on any Node): a block of the massive kind with a lowered pair (a well),
    a nonzero scalar seed (the loader's default 2^20 where none is declared) and no cavity,
    of ANY massive family (the emitter bodies of the light worlds and the M1 rows' source
    family included, ALGEBRA.md 9.17),
    gets `seed` the profile of `mode_profile` at that scalar, its `margin` made explicit
    (the loader admits a profile with `margin` declared; "pin" is the loader's default). A
    silent block (seed 0), a barrier (a raised pair) and a cavity keep their keys."""
    kinds = {family["name"]: family["pair"] for family in document["families"] if "pair" in family}
    for number, entry in enumerate(document["measured"]):
        if "side" not in entry or entry.get("family") not in kinds or entry.get("cavity"):
            continue
        kind = kinds[entry["family"]]
        pair = entry["pair"]
        if pair[0] * kind[1] <= pair[1] * kind[0]:
            continue
        scalar = entry.get("seed", BLOCK_SEED)
        if not isinstance(scalar, int) or scalar == 0:
            continue
        entry.setdefault("margin", "pin")
        entry["seed"] = mode_profile(document, number, amplitude=scalar)
    for number, entry in enumerate(document["measured"]):
        if "emitter" in entry:
            excite_on_the_mode(document, number)


def excite_on_the_mode(document: dict, number: int) -> None:
    """The emitter body `number`'s integers of ALGEBRA.md 9.17 (5) item 1 in the flux's
    units of 9.19 (3), written into the world file by the generator (a HOST computation; the
    loader recomputes and refuses a mismatch): `period` P, the nearest integer to 2 pi /
    omega_b of the body's mode (the margin module's own omega_b), `norm` T, the one-way
    inward flux into the body's centre cell that the seeded mode books over P intervals
    advanced alone by the engine (exact integers), and `born` [now, before], the born
    pair's two integers on every cell (9.17 (6); the table is the generator's, not the
    engine's)."""
    from event_universe.diagnostics.massive_record_margin import (
        block_margin,
        excitation_norm,
        period_of,
    )
    from event_universe.events.detector_law import UNIT
    from event_universe.events.world import parse_nature_beam_world

    entry = document["measured"][number]
    emitter = entry["emitter"]
    emitter.pop("period", None)
    emitter.pop("norm", None)
    emitter.pop("born", None)
    world = parse_nature_beam_world(document)
    period = period_of(block_margin(world, number))
    emitter["period"] = period
    emitter["norm"] = excitation_norm(world, number, period)
    # the born pair (ALGEBRA.md 9.17 (6); no table in the engine): the
    # character half a step either side of its zero, the step the born
    # clock's advance n / d of the circle's N per interval: now = round(A sin(pi
    # n / (d N))), before = -now, A the amplitude unit (a HOST computation
    # written into the file; 9.17 (6)'s whole step floor(n / d) is 0 for a
    # clock below one step per interval, the index rows' [3565, 10000], and
    # wrote no motion: the finding of BUILD.md section 26 item 17)
    born_family = next(f for f in document["families"] if f["name"] == emitter["family"])
    numerator, denominator = born_family["phase_per_link"]
    steps = int(document.get("N", 64))
    level = int(round(UNIT * math.sin(math.pi * numerator / (denominator * steps))))
    emitter["born"] = [level, -level]


SOURCE_KIND = [7, 8]  # the emitter bodies' own family `source` (omega_0 = 0.505; no clock)
SOURCE_WELL = [
    801,
    700,
]  # its one-cell well, rich (700 remainder values, ALGEBRA.md 9.19 (4a)): bound on a chain (2 cos omega_b = 1.90) and on a layer (1.75)


def emitter_at(x: int, stock: int = 1, pair: list[int] | None = None) -> dict:
    """An EMITTER BODY of light at a Node of the chain (ALGEBRA.md 9.17 (4); BUILD.md section
    26): a well of the massive kind of side 1 seeded on its mode (`seed_on_the_mode`), its
    stock `stock` excitations, each clicking at its own rung and writing its photon once;
    the lamp's train of periods retired (a one-cell birth is broadband; the line emitter's
    travelling character is owed, LAB_TOOLS.md A.1). The body is of the family `source` (the
    kind SOURCE_KIND, added to the world by `world`), its well SOURCE_WELL unless given; the
    residue and the wheel are the law's (ALGEBRA.md 9.22 (4): the remainder at the birth
    cell, W = 700 on SOURCE_WELL), the cadence about (2 u + 1) P / (2 W) intervals for the
    residue u, P the mode's period (COMPUTATION, BUILD.md section 26); a well too deep for
    its board is a runaway, refused at the margin rule."""
    return {
        "position": [x, 0, 0],
        "family": "source",
        "side": 1,
        "pair": list(pair or SOURCE_WELL),
        "seed": 100,
        "amount": stock,
        "margin": "control",
        "emitter": {"family": "light"},
    }


def rest_block(side: int, corner: int, pair: list[int], **extra: object) -> dict:
    block: dict = {"position": [corner, corner, corner], "side": side, "pair": pair, "margin": "control"}
    block.update(extra)
    return block


# The light clocks of the moving-index worlds, `phase_per_link` [a, b] the phase steps of
# the circle of N = 64 per interval, omega = 2 pi (a / b) / 64: the design's omega = 0.035
# and the block-frame frequencies gamma_m omega (1 +- beta) at K = 3 (beta = 1 / sqrt 3,
# gamma_m = sqrt(3 / 2): 0.06762 toward, 0.01812 away) and at K = 4 (beta = sqrt 3 / 4,
# gamma_m = 4 / sqrt 13: 0.05565 toward, 0.02202 away).
MOVING_CLOCKS = {
    "omega": [3565, 10000],
    "k3_toward": [6888, 10000],
    "k3_away": [1846, 10000],
    "k4_toward": [5669, 10000],
    "k4_away": [2243, 10000],
}


def moving_block(x: int, momentum: list[int], start: int | None = None) -> dict:
    """The moving-index world's block: s = 24 cells of the well [314, 315] on the kind
    [156, 157], seed 0, g 1 / 200 with G 1, its drive from `start`."""
    block: dict = {
        "position": [x, 0, 0],
        "side": 24,
        "pair": [314, 315],
        "seed": 0,
        "coupling": {"G": [1, 1], "g": [1, 200]},
        "momentum": momentum,
        "margin": "control",
    }
    if start is not None:
        block["start"] = start
    return block


def worlds() -> dict[str, dict]:
    out: dict[str, dict] = {}
    # (i) one block at rest, 48^3, CONTROL
    out["rest_20"] = world(
        "rest-20", "CONTROL", [48, 48, 48], PERIODIC, [800, 809], [rest_block(20, 14, [800, 800])], 3000
    )
    out["rest_28"] = world(
        "rest-28",
        "CONTROL",
        [48, 48, 48],
        PERIODIC,
        [1600, 1618],
        [rest_block(28, 10, [1600, 1609])],
        3000,
    )
    # (ii) the blocks pushed to k = 3 on 64^3, PREDICTION
    for name, side, corner, kind_pair, well in (
        ("moving_20", 20, 22, [800, 809], [800, 800]),
        ("moving_28", 28, 18, [1600, 1618], [1600, 1609]),
    ):
        out[name] = world(
            name.replace("_", "-"),
            "PREDICTION",
            [64, 64, 64],
            PERIODIC,
            kind_pair,
            [rest_block(side, corner, well, momentum=[MOMENTUM_K3, 0, 0], ramp=1500)],
            9500,
            mode_axis="x",
        )
    # (iii) the cavity of form (I), CONTROL
    out["cavity_24"] = world(
        "cavity-24",
        "CONTROL",
        [48, 48, 48],
        PERIODIC,
        [800, 809],
        [rest_block(24, 12, [800, 809], cavity=True)],
        3000,
    )
    out["cavity_24_moving"] = world(
        "cavity-24-moving",
        "CONTROL",
        [64, 64, 64],
        PERIODIC,
        [800, 809],
        [rest_block(24, 20, [800, 809], cavity=True, momentum=[MOMENTUM_K3, 0, 0], ramp=1500)],
        9500,
        mode_axis="x",
    )
    # (v) the index block at rest on a chain, CONTROL of the coupling
    index_light = {"name": "light", "quantum": 1, "phase_per_link": [153, 100]}
    for name, g in (("index_50", [1, 50]), ("index_20", [1, 20]), ("index_10", [1, 10])):
        # the design script's oscillator: the massive row held at 0 outside the
        # cells (`massive_dielectric_index.py`), a CAVITY with the kind's own pair
        block = {
            "position": [900, 0, 0],
            "side": 12,
            "pair": [7, 8],
            "seed": 0,
            "cavity": True,
            "coupling": {"G": [1, 1], "g": g},
            "margin": "control",
        }
        out[name] = world(
            name.replace("_", "-"),
            "CONTROL",
            [1400, 1, 1],
            CHAIN,
            [7, 8],
            [emitter_at(600), block],
            1850,
            light=index_light,
            faces={"x": "open"},
            lamp=None,
            probes=[[1100, 0, 0]],
        )
    out["index_reference"] = world(
        "index-reference",
        "CONTROL",
        [1400, 1, 1],
        CHAIN,
        [7, 8],
        [emitter_at(600)],
        1850,
        light=index_light,
        faces={"x": "open"},
        lamp=None,
        probes=[[1100, 0, 0]],
    )
    # (v-m) the moving index, PREDICTION: the block at rest at x = 1100 read at light's
    # omega and at the two block-frame frequencies omega' = gamma_m omega (1 +- beta) of
    # each K (the covariant expectation formed from the engine's own rest readings, as
    # the design's script forms it), each with its reference without the block; then the
    # block stepping from interval 2600 toward the source (from x = 1300) or away (from
    # x = 700) at K = 3 and K = 4, read at omega against the reference at omega.
    for label, clock in MOVING_CLOCKS.items():
        light_clock = {"name": "light", "quantum": 1, "phase_per_link": clock}
        for name, blocks in (
            (f"index_moving_rest_{label}", [moving_block(1100, [0, 0, 0])]),
            (f"index_moving_reference_{label}", []),
        ):
            out[name] = world(
                name.replace("_", "-"),
                "PREDICTION",
                [2200, 1, 1],
                CHAIN,
                [156, 157],
                blocks,
                4400,
                light=light_clock,
                faces=FACES_OPEN,
                lamp=None,
                probes=[[1500, 0, 0]],
            )
    for k, momentum in ((3, MOMENTUM_K3), (4, MOMENTUM_K4)):
        for direction, x, sign in (("toward", 1300, -1), ("away", 700, 1)):
            name = f"index_moving_k{k}_{direction}"
            out[name] = world(
                name.replace("_", "-"),
                "PREDICTION",
                [2200, 1, 1],
                CHAIN,
                [156, 157],
                [emitter_at(300), moving_block(x, [sign * momentum, 0, 0], start=2600)],
                4400,
                light={"name": "light", "quantum": 1, "phase_per_link": MOVING_CLOCKS["omega"]},
                faces=FACES_OPEN,
                lamp=None,
                probes=[[1500, 0, 0]],
                mode_axis="x",
            )
    # (v-m, the longer chain) the receding case the design's pin from behind is read on,
    # REGENERATED on the declared geometry of DECLARATIONS.md section 11 (2026-09-24,
    # 00:30Z; the first window sat inside the train's own arrival and was withdrawn):
    # n = 4000, the source at 800, the probe at 2400, the block from x = 1500 moving away
    # from interval 3000, the window [3800, 5400] (the front at the probe at 2770, the
    # reflection from x = 0 at 5543); the rest world at omega' away at x = 2100 and the
    # references at omega and at omega' away on the same chain, as before.
    for label in ("omega", "k3_away", "k4_away"):
        light_clock = {"name": "light", "quantum": 1, "phase_per_link": MOVING_CLOCKS[label]}
        for name, blocks in (
            (f"index_moving_long_rest_{label}", [emitter_at(800), moving_block(2100, [0, 0, 0])]),
            (f"index_moving_long_reference_{label}", [emitter_at(800)]),
        ):
            if label == "omega" and "rest" in name:
                continue
            out[name] = world(
                name.replace("_", "-"),
                "PREDICTION",
                [4000, 1, 1],
                CHAIN,
                [156, 157],
                blocks,
                6000,
                light=light_clock,
                faces=FACES_OPEN,
                lamp=None,
                probes=[[2400, 0, 0]],
            )
    for k, momentum in ((3, MOMENTUM_K3), (4, MOMENTUM_K4)):
        name = f"index_moving_long_k{k}_away"
        out[name] = world(
            name.replace("_", "-"),
            "PREDICTION",
            [4000, 1, 1],
            CHAIN,
            [156, 157],
            [emitter_at(800), moving_block(1500, [momentum, 0, 0], start=3000)],
            6000,
            light={"name": "light", "quantum": 1, "phase_per_link": MOVING_CLOCKS["omega"]},
            faces=FACES_OPEN,
            lamp=None,
            probes=[[2400, 0, 0]],
            mode_axis="x",
        )
    # (i-L), (ii-L): the layer pin world of section 11 item 7 (mu = 0.15, s = 14, g = mu^2 / 4:
    # the kind [3200, 3236], the well [3200, 3227]) on a periodic 200 x 200 x 1 layer (the pin
    # margin s + 4 extents = 159 < 200), the seed the BOUND MODE'S INTEGER PROFILE at 2^20 over
    # the whole layer (the generator computes the module's mode and writes the integers into
    # the world file; the engine reads integers; the load-time check prints the deviation): at
    # rest and pushed to k = 3 over the ramp 12000 (ten relaxation times of the well by the
    # margin module's own number, DECLARATIONS.md section 8) and the hold 8000, the ticks
    # 20500 in both (M1-8: the same hold window); the seed on the mode by `seed_on_the_mode`.
    block = {"position": [93, 93, 0], "side": 14, "pair": [3200, 3227], "margin": "pin"}
    rest = world(
        "layer-pin-rest-14",
        "PIN",
        [200, 200, 1],
        PERIODIC,
        [3200, 3236],
        [block],
        LAYER_RAMP + LAYER_HOLD + 500,
    )
    out["layer_pin_rest_14"] = rest
    moving = world(
        "layer-pin-k3-14",
        "PIN",
        [200, 200, 1],
        PERIODIC,
        [3200, 3236],
        [dict(block, momentum=[MOMENTUM_K3, 0, 0], ramp=LAYER_RAMP)],
        LAYER_RAMP + LAYER_HOLD + 500,
        mode_axis="x",
    )
    out["layer_pin_k3_14"] = moving
    out.update(launch_list_worlds())
    return out


def receiver_at(x: int, name: str) -> tuple[list[dict], dict]:
    """A DETECTOR on the light record on the chain: the cube of side 3 of receiver bodies
    at [x, x + 2] (record 1899: one region, its click the detector's) and its detector set;
    the rung's wheel is the record's own (ALGEBRA.md 9.22 (4))."""
    bodies = [
        {
            "position": [x + offset, 0, 0],
            "family": "light",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "directions": [[-1, 0, 0]],
        }
        for offset in range(3)
    ]
    return bodies, {"name": name, "positions": [body["position"] for body in bodies]}


def emitter(position: list[int], side: int, pair: list[int], ticks: int, **extra: object) -> dict:
    """An EMITTER block of the launch list (DECLARATIONS.md sections 4 and 10): the well at
    the cells, the seed 50 x 2^20, the coupling G [1, 50] and g [1, 1000] (section 15
    M1-1) for its response to light, W = 64; SINCE ALGEBRA.md 9.17 its emission is by its
    excited records' clicks (`emitter`: light on the wheel [1, 64], the stock 64
    excitations), no `emits`, no `own_grace`, no source term. `ticks` is the world's."""
    _ = ticks
    block: dict = {
        "position": position,
        "side": side,
        "pair": pair,
        "seed": 50 << 20,
        "coupling": {"G": [1, 50], "g": [1, 1000]},
        "amount": 64,
        "emitter": {"family": "light"},
        "margin": "pin",
    }
    block.update(extra)
    return block


def launch_list_worlds(include_refused: bool = False) -> dict[str, dict]:
    """The launch list's worlds (RUN_LIST.md; DECLARATIONS.md sections 4, 10 and 11).
    The emitters' worlds (4b and the light clock) are written only with
    `include_refused`: their declared coupling g = [1, 50000] is REFUSED at load by
    Reviewer 3's MUST 3 (the load bound of the pair with its g_d at the amplitude bound
    A = 2^40: num x 6 x A x g_d + 3 x den x g_d x (A + 1) below 2^63 admits g_d up to
    about 4450 on [314, 315] and 1750 on [800, 800]); a world that does not load is not
    an example (the gate parses every example), so the conflict of the declaration with
    the bound is the physicist's and Reviewer 3's to settle (BUILD.md section 12)."""
    out: dict[str, dict] = {}
    # (4b) the redshift of the moving lamp, section 4 (the second draft): the chain of 2200,
    # light's faces open, the massive kind's faces open on x; A at x = 700 pushed to k = 3 on
    # -x (receding from B) over the ramp 1500, the hold 8000; the control A at rest at x = 1300;
    # B the light detector at x = 1900, a probe at the free Node it faces (GAMEBOARD).
    emitters: list[tuple[str, int, dict]] = (
        [
            ("redshift_k3", 700, {"momentum": [-MOMENTUM_K3, 0, 0], "ramp": 1500}),
            ("redshift_control", 1300, {}),
        ]
        if include_refused
        else []
    )
    for name, x, extra in emitters:
        bodies, detector = receiver_at(1900, "B")
        document = world(
            name.replace("_", "-"),
            "PIN" if extra else "CONTROL",
            [2200, 1, 1],
            CHAIN,
            [156, 157],
            [emitter([x, 0, 0], 12, [314, 315], 9500, **extra)],
            9500,
            faces=FACES_OPEN,
            probes=[[1899, 0, 0]],
        )
        document["measured"].extend(bodies)
        document["detectors"] = [detector]
        out[name] = document
    # the deep well in motion (the cavity row's CONTROL): a 128^2 layer, s = 40 at full depth
    # in the kind [800, 809], the flat seed, the block centred; pushed to k = 3 over the ramp
    # 1500 and the hold 8000, and at rest.
    deep = {
        "position": [44, 44, 0],
        "side": 40,
        "pair": [800, 800],
        "seed": 1 << 20,
        "margin": "control",
    }
    out["deep_well_rest_40"] = world(
        "deep-well-rest-40", "CONTROL", [128, 128, 1], PERIODIC, [800, 809], [deep], 3500
    )
    out["deep_well_k3_40"] = world(
        "deep-well-k3-40",
        "CONTROL",
        [128, 128, 1],
        PERIODIC,
        [800, 809],
        [dict(deep, momentum=[MOMENTUM_K3, 0, 0], ramp=1500)],
        9500,
        mode_axis="x",
    )
    # the light clock of two bodies, section 10, as an EXPLORATORY world read by probes: the
    # chain of 673 with light's faces open (the zero face at x = 672 the mirror B, sixty
    # Links from A's face at 612), A the emitter of side 12 at [600, 612) at full depth, the
    # probes at x = 612 (A's face, the declared detector's Node) and 613; 2000 intervals (the
    # window before the far end's return). The pinned file waits on the physicist's line
    # for the face detector (a receiver body on a chain takes the whole line).
    if include_refused:
        out["EXPLORATORY_light_clock_60"] = world(
            "exploratory-light-clock-60",
            "EXPLORATORY",
            [673, 1, 1],
            CHAIN,
            [800, 809],
            [emitter([600, 0, 0], 12, [800, 801], 2000)],
            2000,
            probes=[[612, 0, 0], [613, 0, 0]],
        )
    return out


def mode_profile(document: dict, number: int, amplitude: int = 1 << 20) -> list[int]:
    """The bound mode's integer profile of a block over the whole board (the margin module's
    Lanczos vector at load, rounded at the amplitude), the pin worlds' seed of MASSIVE_RECORD.md
    section 11 item 7: a HOST computation of the generator, written into the world file so that
    the run's record follows from the file and the engine alone."""
    from event_universe.diagnostics.massive_record_margin import bound_mode
    from event_universe.events.world import parse_nature_beam_world

    mode = bound_mode(parse_nature_beam_world(document), number)
    return [int(value) for value in np.rint(mode * amplitude).astype(np.int64).ravel()]


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(path.name)


if __name__ == "__main__":
    main()
