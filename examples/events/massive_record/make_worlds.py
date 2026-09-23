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
  beat on a wide mode); at rest and pushed to k = 3 over the ramp 1500 and the hold
  8000: PIN worlds (layer), the pin the mode's period and the one formula at the
  exact cone.

Run from the repository root:

    PYTHONPATH=src python examples/events/massive_record/make_worlds.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PERIODIC = {"x": "periodic", "y": "periodic", "z": "periodic"}
CHAIN = {"x": "open", "y": "periodic", "z": "periodic"}
FACES_OPEN = {"x": "open"}
AGE_BOUND = 1 << 20
MOMENTUM_K3 = 64
MOMENTUM_K4 = 48
BLOCK_KEYS = (
    "coupling",
    "wheel",
    "seed",
    "absorbing",
    "cavity",
    "ramp",
    "start",
    "margin",
    "emits",
    "held",
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
) -> dict:
    """One world file: light's family with its clock, the massive kind `matter` with
    its pair (and its faces where the chain's are open), the blocks as measured
    events with `side`, the lamp and the probes of the index worlds."""
    matter: dict = {"name": "matter", "quantum": 1, "pair": pair}
    if faces is not None:
        matter["faces"] = faces
    measured: list[dict] = []
    if lamp is not None:
        measured.append(lamp)
    for block in blocks:
        entry: dict = {
            "position": block["position"],
            "family": "matter",
            "amount": 1,
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
        "directions": [],
        "families": [light or {"name": "light", "quantum": 1, "phase_per_link": [77, 25]}, matter],
        "measured": measured,
        "detectors": [],
    }
    if probes is not None:
        document["probes"] = probes
    if mode_axis is not None:
        document["mode_axis"] = mode_axis
    return document


def lamp_at(x: int, train: int) -> dict:
    """A lamp of light at a Node of the chain, its train of `train` periods on +x."""
    return {
        "position": [x, 0, 0],
        "family": "light",
        "amount": 1,
        "phase": 0,
        "momentum": [0, 0, 0],
        "fixed": True,
        "directions": [[1, 0, 0]],
        "lamp": {"rate": [1, 1], "wheel": [2531, 4096], "directions": [[1, 0, 0]], "train": train},
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
            [block],
            1850,
            light=index_light,
            faces={"x": "open"},
            lamp=lamp_at(600, 64),
            probes=[[1100, 0, 0]],
        )
    out["index_reference"] = world(
        "index-reference",
        "CONTROL",
        [1400, 1, 1],
        CHAIN,
        [7, 8],
        [],
        1850,
        light=index_light,
        faces={"x": "open"},
        lamp=lamp_at(600, 64),
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
                lamp=lamp_at(300, 200),
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
                [moving_block(x, [sign * momentum, 0, 0], start=2600)],
                4400,
                light={"name": "light", "quantum": 1, "phase_per_link": MOVING_CLOCKS["omega"]},
                faces=FACES_OPEN,
                lamp=lamp_at(300, 200),
                probes=[[1500, 0, 0]],
                mode_axis="x",
            )
    # (v-m, the longer chain) the receding case the design's pin from behind is read on
    # (`massive_moving_index.out`, "the receding case on a longer chain"): n = 4000, the
    # source at 300, the probe at 2500, the block from x = 1500 moving away from interval
    # 2600, the window [5000, 6000]; the rest world at omega' away at x = 2100 and the
    # references at omega and at omega' away on the same chain.
    for label in ("omega", "k3_away", "k4_away"):
        light_clock = {"name": "light", "quantum": 1, "phase_per_link": MOVING_CLOCKS[label]}
        for name, blocks in (
            (f"index_moving_long_rest_{label}", [moving_block(2100, [0, 0, 0])]),
            (f"index_moving_long_reference_{label}", []),
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
                lamp=lamp_at(300, 200),
                probes=[[2500, 0, 0]],
            )
    for k, momentum in ((3, MOMENTUM_K3), (4, MOMENTUM_K4)):
        name = f"index_moving_long_k{k}_away"
        out[name] = world(
            name.replace("_", "-"),
            "PREDICTION",
            [4000, 1, 1],
            CHAIN,
            [156, 157],
            [moving_block(1500, [momentum, 0, 0], start=2600)],
            6000,
            light={"name": "light", "quantum": 1, "phase_per_link": MOVING_CLOCKS["omega"]},
            faces=FACES_OPEN,
            lamp=lamp_at(300, 200),
            probes=[[2500, 0, 0]],
            mode_axis="x",
        )
    # (i-L), (ii-L): the layer pin world of section 11 item 7 (mu = 0.15, s = 14, g = mu^2 / 4:
    # the kind [3200, 3236], the well [3200, 3227]) on a periodic 200 x 200 x 1 layer (the pin
    # margin s + 4 extents = 159 < 200), the seed the BOUND MODE'S INTEGER PROFILE at 2^20 over
    # the whole layer (the generator computes the module's mode and writes the integers into
    # the world file; the engine reads integers; the load-time check prints the deviation): at
    # rest 3500 intervals, and pushed to k = 3 over the ramp 1500 and the hold 8000.
    block = {"position": [93, 93, 0], "side": 14, "pair": [3200, 3227], "margin": "pin"}
    rest = world("layer-pin-rest-14", "PIN", [200, 200, 1], PERIODIC, [3200, 3236], [block], 3500)
    profile = mode_profile(rest, 0)
    rest["measured"][0]["seed"] = profile
    out["layer_pin_rest_14"] = rest
    moving = world(
        "layer-pin-k3-14",
        "PIN",
        [200, 200, 1],
        PERIODIC,
        [3200, 3236],
        [dict(block, momentum=[MOMENTUM_K3, 0, 0], ramp=1500)],
        9500,
        mode_axis="x",
    )
    moving["measured"][0]["seed"] = profile
    out["layer_pin_k3_14"] = moving
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
