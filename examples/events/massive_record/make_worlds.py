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
k = 4. ONE BORDER FOR EVERY FAMILY (BUILD.md section 26 item 28): every family
reads the world's `boundary` (the massive kind's own periodic faces of the
first builds, the family key `faces`, HISTORY, refused by name at load), with
the margin rule of section 11 item 4 checked at load; a chain open on x is
open on x for light and for matter alike (a zero face beyond the ends, the
receiver slab of `face_depth` there). Every well declares its `seed` (no
loader default, item 28: SEED_AMPLITUDE here).

- (i-a) `boxed_clock_side_20_at_rest.json`, (i-b) `boxed_clock_side_28_at_rest.json`: one block at rest on a periodic
  48^3 board, 3000 intervals: CONTROL worlds (the block's own clock against
  section 4's threshold table; the extent and the margin printed at load).
- `boxed_clock_side_20_moving.json` and `boxed_clock_side_28_moving.json` (the boxed clocks of sides 20 and 28 in motion): the same blocks pushed to
  k = 3 on a periodic 64^3 board over a ramp of 1500 intervals and a hold of
  8000: PREDICTION worlds (the one formula of section 8 per world on its own
  box, `massive_moving_pins.py`: 0.7831 and 0.8048), with the pump's two
  GAMEBOARD readings (light's energy drift, the mode k = 2 pi / 3 on x).
- CANCELLED WITH THE CAVITY (BUILD.md section 26 item 28; the cavity of form
  (I), a record held by mirror faces of its own, is refused by name at load):
  `cavity_24.json` (the rest cavity, side 24, the kind's own pair, on 48^3) and
  `cavity_24_moving.json` (the cavity pushed to k = 3 on 64^3), moved as
  written to `docs/designs/detector_law/held_worlds/` (HISTORY, their pins in
  `expectations.json` never moved), their builders retired here.
- HELD UNDER THE GIVEN TRAIN (ALGEBRA.md 9.17 (6a); BUILD.md section 26 item 27; their
  files in `docs/designs/detector_law/held_worlds/` as written with the one-Node giving,
  HISTORY, not loaded by the gate; their builders retired here, to be rebuilt from the
  table of ALGEBRA.md 9.22 (8) in its form, the cleanup's item 7): the index at rest
  (`medium_index_at_rest_50`, `medium_index_at_rest_20`, `medium_index_at_rest_10`,
  `medium_index_reference`: the index block at rest on a chain of 1400, a cavity of the
  kind [7, 8] with G [1, 1] and g 1 / 50, 1 / 20, 1 / 10, the light clock [153, 100] on
  N = 64, an emitter body at x = 600, a probe at x = 1100; the closed form n^2 = 1 + G g /
  (omega_0^2 - omega^2)) and the index in motion (`receding_index_short_*`, `receding_index_*`
  at one third and one quarter of a Link per interval, toward and away, with their rest
  and reference worlds: the moving index on the chains of 2200 and 4000, the well
  [314, 315] of side 24 on the kind [156, 157], g [1, 200], G [1, 1], light at omega
  0.035 and at the block-frame frequencies of each speed; the table's rows 31 and 33 to 37
  restate them on a medium whose mode lies above the train's omega, OPEN there).

- (i-L) `muon_moving_clock_at_rest_14.json`, (ii-L) `muon_moving_clock_speed_third_14.json`: the layer pin world
  of MASSIVE_RECORD.md section 11 item 7 (mu = 0.15, s = 14, g = mu^2 / 4 on a
  periodic 200 x 200 x 1 layer, `margin` "pin"), the seed the bound mode's integer
  profile at 2^20 over the whole layer (the generator's integers in the file, the
  same at both levels: the reader of record is the clicks, which a flat seed makes
  beat on a wide mode); at rest and pushed to k = 3 over the ramp 10000 and the hold
  8000 (the ticks 18500: the ramp declared by the well's relaxation time, ten times
  1 / (omega_0 - omega_b) = 1027 intervals, DECLARATIONS.md section 8): PIN worlds
  (layer), the pin the mode's period and the one formula at the exact cone.

- The deep well's clock, `deep_well_clock_at_rest_40.json` and
  `deep_well_clock_speed_third_40.json` (the launch list's group M2: a 128^2 layer, s = 40 at
  full depth [800, 800] in [800, 809], the seed on the mode, the block centred; at rest
  3500 intervals, the series' rest length; pushed to k = 3 over the ramp 1500 and the hold
  8000, 9500 intervals). The launch list's emitter worlds of this generator (the redshift's
  first draft on the chain of 2200 and the exploratory light clock, never written: refused
  by the load bound with their declared g) are retired with the held rows above.

Run from the repository root:

    PYTHONPATH=src python examples/events/massive_record/make_worlds.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
PERIODIC = {"x": "periodic", "y": "periodic", "z": "periodic"}
CHAIN = {"x": "open", "y": "periodic", "z": "periodic"}
# the declared amplitude of every well of this generator's worlds (its own
# record at interval 0, the iterated mode's peak): no loader default (BUILD.md
# section 26 item 28)
SEED_AMPLITUDE = (
    1 << 18
)  # below the amplitude bound A = 2^20 of the weak-field rule's integers (ALGEBRA.md 9.61 (3); item 44)
AGE_BOUND = 1 << 20
# the amplitude bound A of every row: the ceiling 2^28 under the Node clock (the
# model owner's decision (5) of record 1962; BUILD.md section 26 item 31)
AMPLITUDE_BOUND = (
    1 << 20
)  # the integers of ALGEBRA.md 9.57 (2) and 9.61 (3) under the weak-field rule (item 44; 2^28 under the first-order rule HISTORY)
# THE NODE CLOCK (ALGEBRA.md 9.35 (3); item 31): Gamma, declared per world like
# the pairs, the clock pair (e, f) = (Gamma, Gamma + M) at every Node with M the
# content held there; the eighteen declare 10^6 (a clock body of 64 quanta slows
# by 6 x 10^-5, a well of one quantum by 10^-6, the mathematician's reading: no
# pin of the eighteen moves beyond its band)
NODE_CLOCK = 10_000  # Gamma = 10^4 (ALGEBRA.md 9.57 (2), 9.61 (3); item 44; the eighteen's 10^6 under the first-order rule HISTORY)
# THE FAMILY OF CLICKS (the model owner's record 1982; ALGEBRA.md 9.45; BUILD.md
# section 26 item 32): the fourth family, whose level at a Node is the Node
# clock; its pair [1, 1] (light's kind, the default), its unit the quantum, no
# clock of its own; declared in every world and named by `clock_family`
CLOCK_FAMILY_NAME = "clicks"
CLOCK_FAMILY = {"name": CLOCK_FAMILY_NAME, "quantum": 1, "charge": 0}
# THE FAMILY OF CHARGE (ALGEBRA.md 9.48; BUILD.md section 26 item 35): the fifth family,
# its level the signed charge held at every body's Nodes; Lambda its weight in the clock;
# every registered family's charge is 0, so the field stays 0 and no row moves
CHARGE_FAMILY_NAME = "charge"
CHARGE_FAMILY = {"name": CHARGE_FAMILY_NAME, "quantum": 1, "charge": 0}
CHARGE_STRENGTH = 1
MOMENTUM_SPEED_THIRD = 64
MOMENTUM_SPEED_QUARTER = 48
# The layer pin world's push (DECLARATIONS.md section 8): the ramp ten relaxation times of
# the well (1027 intervals), the hold 8000 after it, the ticks 18500 (500 more, the hold
# read over [10200, 18200] by RUN_LIST.md).
LAYER_RAMP = 12000  # ten relaxation times of the well by the margin module's own omega_b on the 200^2 layer (1164.6 intervals; the design script's 1027 the estimate), the model owner's word of 2026-09-24, 16:48Z: the body's conditions checked at load
LAYER_HOLD = 8000
BLOCK_KEYS = (
    "seed",
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
    probes: list[list[int]] | None = None,
    mode_axis: str | None = None,
    seed_profile: bool = True,
) -> dict:
    """One world file: light's family with its clock, the massive kind `matter` with
    its pair (its faces the world's `boundary`, one border for every family), the blocks as measured
    events with `side` or `extents`, the probes; every bound body's
    seed on its mode (`seed_on_the_mode`) unless `seed_profile` is off, for a caller that
    completes the document first (the detector-law generator's emitters) and calls it then."""
    matter: dict = {"name": "matter", "quantum": 1, "pair": pair}
    families = [light or {"name": "light", "quantum": 1, "phase_per_link": [77, 25]}, matter]
    if any(block.get("family") == "source" for block in blocks):
        # the emitter bodies' own family (`emitter_at`): the kind SOURCE_KIND
        families.append({"name": "source", "quantum": 1, "pair": list(SOURCE_KIND)})
    families.append(dict(CLOCK_FAMILY))  # the family of clicks, the Node clock (item 32)
    for family in families:
        # the sign on the quantum (ALGEBRA.md 9.48 (1)): 0 on every registered family
        family.setdefault("charge", 0)
    families.append(dict(CHARGE_FAMILY))  # the family of charge (item 35)
    measured: list[dict] = []
    for block in blocks:
        entry: dict = {
            "position": block["position"],
            "family": block.get("family", "matter"),
            "amount": block.get("amount", 1),
            "phase": 0,
            "momentum": block.get("momentum", [0, 0, 0]),
            "fixed": True,
        }
        if "side" in block:
            entry["side"] = block["side"]
        else:
            entry["extents"] = block["extents"]  # a box (BUILD.md section 26 item 23)
        entry["pair"] = block["pair"]
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
        # the amplitude bound A every row stays below (2^28, the ceiling under
        # the Node clock, BUILD.md section 26 item 31; DECLARATIONS.md section
        # 15 M1-10's 2^32 HISTORY; the rows asserted below it at run time)
        "amplitude_bound": AMPLITUDE_BOUND,
        # the Node clock Gamma (ALGEBRA.md 9.35 (3); item 31): (e, f) = (Gamma,
        # Gamma + M) at every Node, M the content held there; required, no default
        "node_clock": NODE_CLOCK,
        # the family of clicks by name: its level at a Node is the Node clock
        # (Gamma, Gamma + c), held at every body's Nodes at the content (9.45)
        "clock_family": CLOCK_FAMILY_NAME,
        # the family of charge by name and Lambda, its weight in the clock (9.48)
        "charge_family": CHARGE_FAMILY_NAME,
        "charge_strength": CHARGE_STRENGTH,
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
    a nonzero scalar seed (declared on every well, no loader default: BUILD.md section 26 item 28),
    of ANY massive family (the emitter bodies of the light worlds and the M1 rows' source
    family included, ALGEBRA.md 9.17),
    gets `seed` the profile of `mode_profile` at that scalar, its `margin` made explicit
    (the loader admits a profile with `margin` declared; "pin" is the loader's default). A
    silent block (seed 0) and a barrier (a raised pair) keep their keys."""
    kinds = {family["name"]: family["pair"] for family in document["families"] if "pair" in family}
    for number, entry in enumerate(document["measured"]):
        if ("side" not in entry and "extents" not in entry) or entry.get("family") not in kinds:
            continue
        kind = kinds[entry["family"]]
        pair = entry["pair"]
        if pair[0] * kind[1] <= pair[1] * kind[0]:
            continue
        if "seed" not in entry:
            raise ValueError(
                f"measured[{number}] declares no seed: every well declares its own record's "
                "amplitude (no default, BUILD.md section 26 item 28); nothing written"
            )
        scalar = entry["seed"]
        if not isinstance(scalar, int) or scalar == 0:
            continue
        entry.setdefault("margin", "pin")
        entry["seed"] = mode_profile(document, number, amplitude=scalar)
    for number, entry in enumerate(document["measured"]):
        if "emitter" in entry:
            given_train(document, number)
    placement_check(document)
    stamped(document)


def stamped(document: dict) -> dict:
    """THE INPUT STAMP (record 1886; ALGEBRA.md 9.22 (7) (i)) rewritten for the document's
    integers as they stand: the law identifier and the hash of every profile, clock and
    given pair; written before every parse of a document under construction and last of
    all, so that the file carries the stamp of what it holds."""
    from event_universe.events.world import input_stamp

    document["input"] = input_stamp(document)
    return document


GIVEN_AMPLITUDE = 1 << 16  # the given train's amplitude A (ALGEBRA.md 9.17 (6a))
TRAIN_FLUX_TOLERANCE = 2  # per thousand: the train's one-way flux 40 Links ahead within 2 x 10^-3 of T
TRAIN_FLUX_DISTANCE = 40  # Links ahead of the train's head, the plane the generator's checks read


def given_train(document: dict, number: int) -> None:
    """THE GIVEN TRAIN (ALGEBRA.md 9.17 (6a); BUILD.md section 26 item 27): the emitter body
    `number`'s `given` profile, the character of one **K** over its declared periods under the
    window across the transverse extents and the tapers along **K**, written on the body's
    Nodes at both levels (t = 0 and t = -1), the generator's integers at the amplitude
    A = 2^16: now = round(A e(i) h(y) h(z) cos(k i)), before = round(A e h h cos(k i + omega)),
    i the Node's index along the train's way from its tail, k = 2 pi p / (2 N q) from the
    given family's clock [p, q] on the world's N, 3 cos omega = (num / den) (cos k + 2) on the
    given family's vacuum pair; h the Hann window sin^2(pi (y + 1 / 2) / Y) across a transverse
    extent Y, and 1 across an axis the body spans on a periodic face (a chain, and the
    extruded axes of the one table's boards, where the seed is uniform across the added
    axes); e the taper over tau = X / 4 Nodes at each end (sin^2(pi (i + 1 / 2) / (2 tau))
    for i < tau, 1 between, mirrored at the tail). THE NORM T the conserved form of the two
    levels on the vacuum (`given_train_norm`, the one copy the loader checks). THE FLUX CHECK
    (HOST, the generator, 9.25 (11) (a)): the train alone on the given family's vacuum,
    advanced by the engine's rule, books its one-way flux through a plane one Node deep 40
    Links ahead of its head; the sum over the passage must be T within 2 x 10^-3, else the
    profile is refused (3 periods 1.0285 and growing; 8 periods 0.9987; 16 periods 0.9997).
    THE TRANSPARENCY (9.22 (7a) (iv)): every body coupled to the given family (a body its
    record must enter to be read: the emitter itself where its light returns, another well,
    a medium) passes the train run through it alone on the vacuum with 0.99 of T booked 40
    Links beyond, refused below. The emitter's `period` and `norm` (the excited record's) are
    the mode's as before (`excitation_norm`)."""
    from event_universe.diagnostics.massive_record_margin import (
        block_margin,
        excitation_norm,
        period_of,
    )
    from event_universe.events.world import (
        given_train_flux_sign,
        given_train_norm,
        parse_nature_beam_world,
    )

    entry = document["measured"][number]
    emitter = entry["emitter"]
    for key in ("period", "norm", "given"):
        emitter.pop(key, None)
    world = parse_nature_beam_world(stamped(document))
    period = period_of(block_margin(world, number))
    emitter["period"] = period
    emitter["norm"] = excitation_norm(world, number, period)
    definition = world.measured[number].block
    assert definition is not None and definition.emitter is not None
    train = definition.emitter.train
    if train is None:
        raise ValueError(
            f"measured[{number}].emitter declares no `train` (the direction and the periods): "
            "every giving is a travelling train (ALGEBRA.md 9.17 (6a)); nothing written"
        )
    given_family = world.families[definition.emitter.family]
    num, den = int(given_family.pair[0]), int(given_family.pair[1])
    p, q = train.clock
    steps = int(world.phase_steps)
    extents = tuple(int(v) for v in definition.extents)
    shape = (int(world.shape[0]), int(world.shape[1]), int(world.shape[2]))
    wrap = world.kind_periodic(definition.emitter.family)
    axis, sign = train.axis, train.sign
    length = extents[axis]
    taper = length // 4
    k = 2.0 * math.pi * p / (2.0 * steps * q)
    omega = math.acos((num / den) * (math.cos(k) + 2.0) / 3.0)
    spanned = tuple(extents[a] == shape[a] and wrap[a] for a in range(3))

    def envelope(i: int) -> float:
        if i < taper:
            return math.sin(math.pi * (i + 0.5) / (2.0 * taper)) ** 2
        if i >= length - taper:
            return envelope(length - 1 - i)
        return 1.0

    def window(index: int, extent: int, uniform: bool) -> float:
        if extent <= 1 or uniform:
            return 1.0
        return math.sin(math.pi * (index + 0.5) / extent) ** 2

    now: list[int] = []
    before: list[int] = []
    for x in range(extents[0]):
        for y in range(extents[1]):
            for z in range(extents[2]):
                position = (x, y, z)
                along = position[axis] if sign > 0 else length - 1 - position[axis]
                shape_factor = envelope(along)
                for other in range(3):
                    if other != axis:
                        shape_factor *= window(position[other], extents[other], spanned[other])
                amplitude = GIVEN_AMPLITUDE * shape_factor
                now.append(int(round(amplitude * math.cos(k * along))))
                before.append(int(round(amplitude * math.cos(k * along + omega))))
    if given_train_flux_sign(now, before, extents, axis, sign) <= 0:
        raise ValueError(
            f"measured[{number}]: the train's flux along its way is not positive; nothing written"
        )
    norm = given_train_norm(now, before, shape, (0, 0, 0), extents, (num, den), wrap)
    # the check board's engine books the plain flux, the wall times the current,
    # unweighted (ALGEBRA.md 9.50 (13); BUILD.md section 26 item 36); the file's norm
    # is the plain vacuum form (the loader's check), so the passage is read against
    # the norm itself (Gamma squared times it under form (B) of item 34, HISTORY)
    gamma = int(document["node_clock"])
    booked = train_passage_flux(document, number, now, before)
    scaled = norm
    if (
        not scaled * (1000 - TRAIN_FLUX_TOLERANCE)
        <= booked * 1000
        <= scaled * (1000 + TRAIN_FLUX_TOLERANCE)
    ):
        raise ValueError(
            f"measured[{number}]: the train of {train.periods} periods books {booked} of its norm "
            f"{norm} (the Node clock {gamma}) through a plane {TRAIN_FLUX_DISTANCE} Links ahead "
            f"({booked / scaled:.4f}): not a passage within 2 x 10^-3 (ALGEBRA.md 9.25 (11)); "
            "nothing written"
        )
    emitter["given"] = {"now": now, "before": before, "norm": norm}


def names_of(document: dict) -> dict[str, int]:
    return {family["name"]: index for index, family in enumerate(document["families"])}


def group_pace(pair: tuple[int, int], k: float) -> float:
    """The group velocity of the dispersion 3 cos omega = (num / den) (cos k + 2) along
    **K** (a HOST number for the checks' windows): d omega / d k = (num / den) sin k /
    (3 sin omega)."""
    num, den = pair
    cos_omega = (num / den) * (math.cos(k) + 2.0) / 3.0
    return (num / den) * math.sin(k) / (3.0 * math.sqrt(1.0 - cos_omega * cos_omega))


def train_run(
    document: dict,
    family: str,
    axis: int,
    sign: int,
    train_extents: tuple[int, int, int],
    transverse_corner: tuple[int, int, int],
    now: list[int],
    before: list[int],
) -> int:
    """THE GENERATOR'S RUN OF A TRAIN (HOST; ALGEBRA.md 9.25 (11) (a)): the train's two
    levels planted on the given family's VACUUM of the world's families, on a check board of
    the world's transverse shape and faces whose axis along **K** is open and long (a back
    margin of one train's length behind the tail, the train, the plane one Node deep
    TRAIN_FLUX_DISTANCE Links beyond the train's head, and a far margin of twelve trains'
    lengths, so that the far face's reflection returns after the window); the train advanced
    by the engine's rule for the window (TRAIN_FLUX_DISTANCE + six trains' lengths) / v_g
    intervals, v_g the dispersion's group pace along **K** (a narrow train's oblique parts
    pass more slowly: an 8-wide train on a layer books 0.9972 of its norm in a window of
    three trains and 1.0000 in six, COMPUTATION); the one-way inward flux into the plane
    summed over the window is returned. The transparency reading of 9.22 (7a) (iv) (a body
    placed at the train's head) is HISTORY with the coupling (the model owner's decision
    (2) of record 1962)."""
    import numpy as np

    from event_universe.events.detector_law import DetectorLawSimulation
    from event_universe.events.world import body_node_indices, parse_nature_beam_world

    length = train_extents[axis]
    far = 12 * length + TRAIN_FLUX_DISTANCE
    total = length + length + TRAIN_FLUX_DISTANCE + far
    shape = [int(v) for v in document["shape"]]
    shape[axis] = total

    def at(t: int) -> int:
        return t if sign > 0 else total - 1 - t

    train_low = length
    plane_t = train_low + length + TRAIN_FLUX_DISTANCE - 1
    check = json.loads(json.dumps(document))
    check["shape"] = shape
    check["boundary"] = dict(document["boundary"])
    check["boundary"]["xyz"[axis]] = "open"
    check["face_depth"] = 1  # the check board's receiver slab one Node deep at its open ends
    check.pop("probes", None)
    check["detectors"] = []
    check["measured"] = []
    check["ticks"] = 1
    stamped(check)
    world = parse_nature_beam_world(check)
    simulation = DetectorLawSimulation(world)
    given = names_of(document)[family]
    board = (int(shape[0]), int(shape[1]), int(shape[2]))
    corner = list(transverse_corner)
    corner[axis] = min(at(train_low), at(train_low + length - 1))
    nodes = body_node_indices(
        board, (corner[0], corner[1], corner[2]), train_extents, world.kind_periodic(given)
    )
    level_now = np.zeros(board, dtype=np.int64).reshape(-1)
    level_before = np.zeros(board, dtype=np.int64).reshape(-1)
    for index, a, b in zip(nodes, now, before, strict=True):
        level_now[index] = a
        level_before[index] = b
    live = simulation.planted_record(given, level_now.reshape(board), level_before.reshape(board))
    plane = np.zeros(board, dtype=bool)
    index_slice: list[object] = [slice(None)] * 3
    index_slice[axis] = at(plane_t)
    plane[tuple(index_slice)] = True
    family_entry = document["families"][given]
    pair = (int(family_entry.get("pair", [1, 1])[0]), int(family_entry.get("pair", [1, 1])[1]))
    p, q = (int(v) for v in family_entry["phase_per_link"])
    k = 2.0 * math.pi * p / (2.0 * int(document["N"]) * q)
    window = math.ceil((TRAIN_FLUX_DISTANCE + 6 * length) / group_pace(pair, k))
    booked = 0
    for _ in range(window):
        simulation._advance(live)
        booked += simulation.inward_flux(live, plane)
    return booked


def train_passage_flux(document: dict, number: int, now: list[int], before: list[int]) -> int:
    """THE FLUX CHECK'S READING (ALGEBRA.md 9.25 (11) (a)): the train alone on the vacuum,
    the plane TRAIN_FLUX_DISTANCE Links ahead of its head (`train_run`)."""
    entry = document["measured"][number]
    direction = entry["emitter"]["train"]["direction"]
    axis = next(index for index, v in enumerate(direction) if v != 0)
    sign = 1 if direction[axis] > 0 else -1
    corner = (int(entry["position"][0]), int(entry["position"][1]), int(entry["position"][2]))
    return train_run(
        document, entry["emitter"]["family"], axis, sign, block_extents_of(entry), corner, now, before
    )


def block_extents_of(entry: dict) -> tuple[int, int, int]:
    if "extents" in entry:
        return (int(entry["extents"][0]), int(entry["extents"][1]), int(entry["extents"][2]))
    side = int(entry["side"])
    return (side, side, side)


def placement_check(document: dict) -> None:
    """THE PLACEMENT RULE (ALGEBRA.md 9.25 (11) (b)): every emitter's tail and every
    receiver stands at least one train's length from every face slab's front (the slab
    returns what it books); refused naming the tool and the slab. The face slabs are the
    `face_depth` Nodes nearest every open border of the world's `boundary` (declared on
    every open board, no default; 0 on a board with no open face)."""
    shape = [int(v) for v in document["shape"]]
    depth = int(document["face_depth"]) if "face_depth" in document else 0
    lengths = []
    tools: list[tuple[str, tuple[int, int, int], tuple[int, int, int]]] = []
    for number, entry in enumerate(document["measured"]):
        if "emitter" in entry and "train" in entry["emitter"]:
            extents = block_extents_of(entry)
            direction = entry["emitter"]["train"]["direction"]
            axis = next(index for index, v in enumerate(direction) if v != 0)
            lengths.append(extents[axis])
            corner = (int(entry["position"][0]), int(entry["position"][1]), int(entry["position"][2]))
            tools.append((f"the emitter measured[{number}]", corner, extents))
    if not lengths:
        return
    train_length = max(lengths)
    for detector in document.get("detectors", []):
        if "positions" in detector:
            xs = [int(p[0]) for p in detector["positions"]]
            ys = [int(p[1]) for p in detector["positions"]]
            zs = [int(p[2]) for p in detector["positions"]]
            corner = (min(xs), min(ys), min(zs))
            extents = (max(xs) - min(xs) + 1, max(ys) - min(ys) + 1, max(zs) - min(zs) + 1)
        elif "block" in detector:
            entry = document["measured"][int(detector["block"])]
            corner = (int(entry["position"][0]), int(entry["position"][1]), int(entry["position"][2]))
            extents = block_extents_of(entry)
        else:
            continue
        tools.append((f"the receiver {detector['name']!r}", corner, extents))
    boundary = document["boundary"]
    for axis, name in enumerate("xyz"):
        if boundary.get(name, "periodic") != "open":
            continue
        for label, corner, extents in tools:
            low_gap = corner[axis] - depth
            high_gap = shape[axis] - depth - (corner[axis] + extents[axis])
            for gap, where in ((low_gap, "low"), (high_gap, "high")):
                if gap < train_length:
                    raise ValueError(
                        f"{label} stands {gap} Links from the {where} face slab's front on the axis "
                        f"{name} (the slab {depth} deep), nearer than one train's length "
                        f"{train_length} (ALGEBRA.md 9.25 (11) (b)); nothing written"
                    )


SOURCE_KIND = [7, 8]  # the emitter bodies' own family `source` (omega_0 = 0.505; no clock)
SOURCE_WELL = [
    801,
    700,
]  # its one-Node well, rich (700 remainder values, ALGEBRA.md 9.19 (4a)): bound on a chain (2 cos omega_b = 1.90) and on a layer (1.75)


def rest_block(side: int, corner: int, pair: list[int], **extra: object) -> dict:
    block: dict = {
        "position": [corner, corner, corner],
        "side": side,
        "pair": pair,
        "margin": "control",
        "seed": SEED_AMPLITUDE,
    }
    block.update(extra)
    return block


def worlds() -> dict[str, dict]:
    out: dict[str, dict] = {}
    # (i) one block at rest, 48^3, CONTROL
    out["boxed_clock_side_20_at_rest"] = world(
        "boxed-clock-side-20-at-rest",
        "CONTROL",
        [48, 48, 48],
        PERIODIC,
        [800, 809],
        [rest_block(20, 14, [800, 800])],
        3000,
    )
    out["boxed_clock_side_28_at_rest"] = world(
        "boxed-clock-side-28-at-rest",
        "CONTROL",
        [48, 48, 48],
        PERIODIC,
        [1600, 1618],
        [rest_block(28, 10, [1600, 1609])],
        3000,
    )
    # (ii) the blocks pushed to k = 3 on 64^3, PREDICTION
    for name, side, corner, kind_pair, well in (
        ("boxed_clock_side_20_moving", 20, 22, [800, 809], [800, 800]),
        ("boxed_clock_side_28_moving", 28, 18, [1600, 1618], [1600, 1609]),
    ):
        out[name] = world(
            name.replace("_", "-"),
            "PREDICTION",
            [64, 64, 64],
            PERIODIC,
            kind_pair,
            [rest_block(side, corner, well, momentum=[MOMENTUM_SPEED_THIRD, 0, 0], ramp=1500)],
            9500,
            mode_axis="x",
        )
    # (iii) the cavity of form (I): CANCELLED, its two worlds held as written (the
    # module docstring; BUILD.md section 26 item 28)
    # the index rows at rest and in motion: HELD under the given train (the module docstring)
    # (i-L), (ii-L): the layer pin world of section 11 item 7 (mu = 0.15, s = 14, g = mu^2 / 4:
    # the kind [3200, 3236], the well [3200, 3227]) on a periodic 200 x 200 x 1 layer (the pin
    # margin s + 4 extents = 159 < 200), the seed the BOUND MODE'S INTEGER PROFILE at 2^20 over
    # the whole layer (the generator computes the module's mode and writes the integers into
    # the world file; the engine reads integers; the load-time check prints the deviation): at
    # rest and pushed to k = 3 over the ramp 12000 (ten relaxation times of the well by the
    # margin module's own number, DECLARATIONS.md section 8) and the hold 8000, the ticks
    # 20500 in both (M1-8: the same hold window); the seed on the mode by `seed_on_the_mode`.
    block = {
        "position": [93, 93, 0],
        "side": 14,
        "pair": [3200, 3227],
        "margin": "pin",
        "seed": SEED_AMPLITUDE,
    }
    rest = world(
        "muon-moving-clock-at-rest-14",
        "PIN",
        [200, 200, 1],
        PERIODIC,
        [3200, 3236],
        [block],
        LAYER_RAMP + LAYER_HOLD + 500,
    )
    out["muon_moving_clock_at_rest_14"] = rest
    moving = world(
        "muon-moving-clock-speed-third-14",
        "PIN",
        [200, 200, 1],
        PERIODIC,
        [3200, 3236],
        [dict(block, momentum=[MOMENTUM_SPEED_THIRD, 0, 0], ramp=LAYER_RAMP)],
        LAYER_RAMP + LAYER_HOLD + 500,
        mode_axis="x",
    )
    out["muon_moving_clock_speed_third_14"] = moving
    out.update(launch_list_worlds())
    return out


def launch_list_worlds() -> dict[str, dict]:
    """The launch list's worlds of this generator (RUN_LIST.md): the deep well's clock at
    rest and in motion (the module docstring); its emitter worlds retired with the held
    rows."""
    out: dict[str, dict] = {}
    deep = {
        "position": [44, 44, 0],
        "side": 40,
        "pair": [800, 800],
        "seed": SEED_AMPLITUDE,
        "margin": "control",
    }
    out["deep_well_clock_at_rest_40"] = world(
        "deep-well-clock-at-rest-40", "CONTROL", [128, 128, 1], PERIODIC, [800, 809], [deep], 3500
    )
    out["deep_well_clock_speed_third_40"] = world(
        "deep-well-clock-speed-third-40",
        "CONTROL",
        [128, 128, 1],
        PERIODIC,
        [800, 809],
        [dict(deep, momentum=[MOMENTUM_SPEED_THIRD, 0, 0], ramp=1500)],
        9500,
        mode_axis="x",
    )
    return out


def mode_profile(document: dict, number: int, amplitude: int) -> list[int]:
    """The bound mode's integer profile of a block over the whole board, THE GENERATOR AS THE
    BOARD'S OWN OPERATOR ITERATED IN INTEGERS WITH THE STOP (the model owner's word of
    2026-09-25, 04:10Z, closing record 1898; the margin module's `iterated_mode`: the operator
    iterated from the Nodes' indicator, the clock read from the growth at the peak Node, the
    stop the first iteration at which the scaled profile passes the loader's own residual
    bound), the pin worlds' seed of MASSIVE_RECORD.md section 11 item 7: a HOST computation of
    the generator, reproducible bit for bit, written into the world file so that the run's
    record follows from the file and the engine alone. SINCE record 1886 (ALGEBRA.md 9.22 (7))
    the entry also receives the mode's `clock` [a, b] (2 cos omega as a rational, b at least
    twice the amplitude), and the profile is checked here once more against the loader's
    residual bound before it is written: a profile that fails is a generator fault, raised,
    never written."""
    from event_universe.diagnostics.massive_record_margin import iterated_mode
    from event_universe.events.world import body_node_indices, mode_residual, parse_nature_beam_world

    world = parse_nature_beam_world(stamped(document))
    flat, clock, _ = iterated_mode(world, number, amplitude)
    entry = world.measured[number]
    block = entry.block
    assert block is not None
    family = world.families[entry.family]
    shape = (int(world.shape[0]), int(world.shape[1]), int(world.shape[2]))
    wrap = world.kind_periodic(entry.family)
    corner = (int(entry.position[0]), int(entry.position[1]), int(entry.position[2]))
    count = shape[0] * shape[1] * shape[2]
    num, den = [family.pair[0]] * count, [family.pair[1]] * count
    for index in body_node_indices(shape, corner, block.extents, wrap):
        num[index], den[index] = block.pair[0], block.pair[1]
    residual, bound, node = mode_residual(flat, num, den, clock, shape, wrap)
    if residual > bound:
        raise ValueError(
            f"the generator's mode for measured[{number}] fails the loader's residual bound at "
            f"Node {list(node)}: {residual} above {bound} (the clock {list(clock)}, the amplitude "
            f"{amplitude}); nothing written"
        )
    document["measured"][number]["clock"] = list(clock)
    return flat


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(path.name)


if __name__ == "__main__":
    main()
