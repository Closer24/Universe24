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
from fractions import Fraction
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
# THE ONE FAMILIES FILE (ALGEBRA.md 9.83 (2), 9.85 (3); BUILD.md section 26 item 59): the
# universe's families as laws and the universe's integers, one canonical copy; every world of
# this generator is built with the file's entries and written with the file's path
UNIVERSE_FILE = "examples/events/universe.json"  # the universe file (record 2128 (3))
MASSIVE_GIVEN_CLOCK = [77, 25]  # this generator's light clock (the pair form on N = 64)
# THE THREE FAMILIES (ALGEBRA.md 9.86 (2), 9.91 (7); the one stroke, commit 1): gravity (the
# held content, the Node clock), the charge (the held sign; light is its wave, so a light
# record, a mirror of light's kind and a stock of light are the charge family's), and matter
# (one family, every body with its own rest pair `kind`)
MATTER_FAMILY_NAME = "matter"
WAVE_FAMILY_NAME = "charge"
# THE LIGHT EMITTER'S MOMENT (ALGEBRA.md 9.82 (3) (d), 9.82 (4); the one stroke, commit 4):
# the given light is written into the charge family's component along the body's moment
# mu; every shipped light row gives along z, the axis with no Port in its worlds (folded
# or the body's whole periodic extent), so its bookings are the scalar light's bit for bit
LIGHT_MOMENT = [0, 0, 1]


def families_entries() -> tuple[list[dict], dict[str, int]]:
    """The universe file's entries in the loader's list form and the universe's integers."""
    from event_universe.world_files import families_file_entries

    entries, integers = families_file_entries(UNIVERSE_FILE)
    return [dict(entry) for entry in entries], dict(integers)


def universe_integer(document: dict, key: str) -> int:
    """One of the universe's integers as the world reads it: the world's own key on an inline
    list, the universe file's under the path (Q, `momentum_unit`, ALGEBRA.md 9.96 (1))."""
    if isinstance(document["universe"], str):
        return int(families_entries()[1][key])
    return int(document[key])


def bind_universe_file(document: dict) -> dict:
    """The world as written: the universe file's path in place of the list (the world's key
    `universe`, record 2128 (3)), the universe's integers the file's alone (the world's copies
    removed), the stamp over the file."""
    document["universe"] = UNIVERSE_FILE
    document.pop("node_clock", None)
    document.pop("amplitude_bound", None)
    document.pop("momentum_unit", None)
    document.pop("twist_table", None)
    return stamped(document)


def families_of(document: dict) -> list[dict]:
    """The world's families in the loader's list form: the list as written, or the families
    file's entries when the world names the file (ALGEBRA.md 9.85 (3); item 59)."""
    families = document["universe"]
    if isinstance(families, str):
        from event_universe.world_files import families_file_entries

        return [dict(entry) for entry in families_file_entries(families)[0]]
    return list(families)


def pair_on_body(document: dict, family: str) -> bool:
    """Whether the family declares no pair of its own, every body and record of it declaring
    theirs (`pair` "body"; ALGEBRA.md 9.85 (3), 9.91 (7))."""
    entry = next(item for item in families_of(document) if item["name"] == family)
    return entry.get("pair") == "body"


def kind_of(document: dict, entry: dict) -> list[int]:
    """A body's rest pair (its kind): its family's declared pair, or its own `kind` on a family
    whose pair is the body's; [1, 1] for a family declaring none (light's kind)."""
    if pair_on_body(document, entry["family"]):
        return [int(entry["kind"][0]), int(entry["kind"][1])]
    family = next(item for item in families_of(document) if item["name"] == entry["family"])
    pair = family.get("pair", [1, 1])
    return [int(pair[0]), int(pair[1])]


FAMILIES_INTEGERS = families_entries()[1]
# Gamma = 10^4 (ALGEBRA.md 9.57 (2), 9.61 (3); item 44; the eighteen's 10^6 under
# the first-order rule HISTORY); the families file's integer
NODE_CLOCK = FAMILIES_INTEGERS["node_clock"]
MOMENTUM_SPEED_THIRD = 64
MOMENTUM_SPEED_QUARTER = 48
# The layer pin world's push (DECLARATIONS.md section 8): the ramp ten relaxation times of
# the well (1027 intervals), the hold 8000 after it, the ticks 18500 (500 more, the hold
# read over [10200, 18200] by RUN_LIST.md).
LAYER_RAMP = 12000  # ten relaxation times of the well by the margin module's own omega_b on the 200^2 layer (1164.6 intervals; the design script's 1027 the estimate), the model owner's word of 2026-09-24, 16:48Z: the body's conditions checked at load
LAYER_HOLD = 8000
BLOCK_KEYS = (
    "seed",
    # the stock as the given family's content held at the body (ALGEBRA.md
    # 9.51 (8); item 47): the body's `stocks` (record 2128 (1))
    "stocks",
    "ramp",
    "start",
    "margin",
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
    given_clock: list[int] | None = None,
    probes: list[list[int]] | None = None,
    mode_axis: str | None = None,
    seed_profile: bool = True,
) -> dict:
    """One world file: the families file's three families, the bodies of matter with the
    world's kind `pair` as their rest pair `kind` (its faces the world's `boundary`, one
    border for every family), the blocks as measured events with `side` or `extents`, the
    probes; every bound body's seed on its mode (`seed_on_the_mode`) unless `seed_profile` is
    off, for a caller that completes the document first (the detector-law generator's
    emitters) and calls it then."""
    # THE ONE FAMILIES FILE (item 59; the three entries of ALGEBRA.md 9.91 (7), commit 1):
    # every family of the universe in every world, the file's entries; a body of matter
    # declares its rest pair `kind`; the light record's clock the emitter's (`clock` on
    # every emitter, ALGEBRA.md 9.85 (3))
    families, integers = families_entries()
    clock = list(MASSIVE_GIVEN_CLOCK if given_clock is None else given_clock)
    from event_universe.generator_numbers import body_twist, emitter_twist

    measured: list[dict] = []
    for block in blocks:
        # EVERY KEY THE DETECTOR LAW READS, WRITTEN (the model owner's record 2089;
        # BUILD.md section 26 item 57): the momentum, the held quanta, the drive's
        # ramp and start and the margin kind on every measured event; the ray
        # law's `phase`, `fixed` and `directions` no longer written (never read)
        family = block.get("family", MATTER_FAMILY_NAME)
        entry: dict = {
            "position": block["position"],
            "family": family,
            "amount": block.get("amount", 1),
            "momentum": block.get("momentum", [0, 0, 0]),
            "stocks": {},  # the body's stocks of other families' quanta (record 2128 (1))
            "ramp": 0,
            "start": 0,
        }
        if "seed" in block:
            entry["margin"] = "pin"  # a well's margin kind (record 2037), declared on every well
        if "side" in block:
            entry["side"] = block["side"]
        else:
            entry["extents"] = block["extents"]  # a box (BUILD.md section 26 item 23)
        entry["pair"] = block["pair"]
        if any(item["name"] == family and item.get("pair") == "body" for item in families):
            entry["kind"] = list(block.get("kind", pair))  # the body's rest pair (9.91 (7))
        # the body's numbers the holds read (ALGEBRA.md 9.91 (3), (7); commit 2), no default
        entry["q"] = block.get("q", 0)  # the body's signed number (record 2128 (1))
        entry["spin"] = list(block.get("spin", [0, 0, 0]))
        entry["moment"] = list(block.get("moment", [0, 0, 0]))
        for key in BLOCK_KEYS:
            if key in block:
                entry[key] = block[key]
        # THE TWIST "OWN" (ALGEBRA.md 9.96 (2) (a); item 73): the kind's rest rotation here,
        # the mode's rotation once the body is seeded (`declare_twists` at every stamp)
        entry["twist"] = block.get("twist", body_twist(block.get("clock"), entry.get("kind", pair)))
        if "emitter" in entry:
            entry["emitter"].setdefault("clock", list(clock))
            entry["emitter"].setdefault(
                "twist", emitter_twist(entry["emitter"].get("pair"), block.get("clock"))
            )
        # A TOOL IS APPARATUS HELD IN PLACE (ALGEBRA.md 9.104 (6) (b); the Boss's record
        # 2157): every resting body of a shipped world declares `fixed: true` (the feed, when
        # it lands, acts on a body without the word alone); a body with a momentum is free
        if all(int(component) == 0 for component in entry["momentum"]):
            entry["fixed"] = True
        measured.append(entry)
    document: dict = {
        "shape": shape,
        "boundary": boundary,
        "ticks": ticks,
        "age_bound": AGE_BOUND,
        "K": 1073741824,
        "N": 64,
        "release": [1, 128],
        # the drive wall's width S (3 Q S M; ALGEBRA.md 9.52 (4)), declared (record 2089)
        "width": 1,
        "clock_stamp": True,
        "massive_record": True,
        "body_record": False,
        # THE ENGINE START FILE (record 2089; BUILD.md section 26 item 57): the one
        # canonical copy, referenced by its repository path
        "engine": "examples/events/engine_start.json",
        # the amplitude bound A every row stays below (BUILD.md section 26 item
        # 31; the ceiling 2^28 retired, ALGEBRA.md 9.83 (2) (a); the rows
        # asserted below A at run time)
        "amplitude_bound": integers["amplitude_bound"],
        # the Node clock Gamma (ALGEBRA.md 9.35 (3); item 31): (e, f) = (Gamma,
        # Gamma + M) at every Node, M the content held there; required, no default
        "node_clock": integers["node_clock"],
        # the momentum's unit Q (ALGEBRA.md 9.96 (1)): every body's wall W = 3 Q M
        "momentum_unit": integers["momentum_unit"],
        # the twist table (ALGEBRA.md 9.96 (2) (c)): the file's, on the inline document
        # while the build runs the engine
        "twist_table": integers["twist_table"],
        # the families' roles stand on the families (`held`, `reads`; the family
        # genericity, BUILD.md section 26 item 51); the list during the build, the
        # file's path as written (`bind_universe_file`; the world's key `universe`, record 2128)
        "universe": families,
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
    # the loader requires the window's weight on every emitter (commit 7): the mode and the
    # rung are read at the weight 1 where none is declared yet; the row's generator chooses
    # the weight after the seeding (`point_weight`, `finish_windows`), a test declares its own
    for entry in document["measured"]:
        if "emitter" in entry:
            entry["emitter"].setdefault("weight", 1)
    for number, entry in enumerate(document["measured"]):
        if "side" not in entry and "extents" not in entry:
            continue
        kind = kind_of(document, entry)
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
        if any(component != 0 for component in entry.get("momentum", [0, 0, 0])):
            # the moving body's Node's proper pairs (ALGEBRA.md 9.63 (3); item 46)
            entry["proper_clock"] = proper_clock(document, number)
    for number, entry in enumerate(document["measured"]):
        if "emitter" in entry:
            # THE WINDOW IS THE ONE GIVING (ALGEBRA.md 9.85 (5), 9.71 (1); commit 7): the
            # rung alone (the weight is set after the seeding by `point_weight`: the mode is
            # computed first); the given train's `given_train` is CANCELLED, called nowhere
            emitter_rung(document, number)
    placement_check(document)
    stamped(document)


def stamped(document: dict) -> dict:
    """THE INPUT STAMP (record 1886; ALGEBRA.md 9.22 (7) (i)) rewritten for the document's
    integers as they stand: the hash of the whole file under `stamp` (no law identifier,
    ALGEBRA.md 9.90 (1)); written before every parse of a document under construction and last of
    all, so that the file carries the stamp of what it holds."""
    from event_universe.world_files import input_stamp

    declare_twists(document)
    document["stamp"] = input_stamp(document)
    return document


def declare_twists(document: dict) -> None:
    """THE TWIST "OWN" DECLARED (ALGEBRA.md 9.96 (2) (a); BUILD.md section 26 item 73): on
    every body (a block) round(2^16 omega_0) of its mode's rotation (`clock`) or of its
    kind's rest rotation, and on every emitter the given record's (the emitter's own `pair`
    on a body giving its own family, else the body's rotation where the window writes it);
    the generator's HOST number, an integer the loader reads under `twist`, no default."""
    from event_universe.generator_numbers import body_twist, emitter_twist

    for entry in document["measured"]:
        if "side" in entry or "extents" in entry:
            entry["twist"] = body_twist(entry.get("clock"), kind_of(document, entry))
        if "emitter" in entry:
            emitter = entry["emitter"]
            emitter["twist"] = emitter_twist(emitter.get("pair"), entry.get("clock"))


GIVEN_AMPLITUDE = 1 << 16  # the given train's amplitude A (ALGEBRA.md 9.17 (6a))
TRAIN_FLUX_TOLERANCE = 2  # per thousand: the train's one-way flux 40 Links ahead within 2 x 10^-3 of T
TRAIN_FLUX_DISTANCE = 40  # Links ahead of the train's head, the plane the generator's checks read


def emitter_rung(document: dict, number: int):  # type: ignore[no-untyped-def]
    """The emitter's rung as the file declares it (ALGEBRA.md 9.17 (7) (e) and (f); 9.44 (5)
    (c)): `period` P, the nearest integer to 2 pi over the body's mode's rotation, and `norm`
    T, one period's action of the excited record (`excitation_norm`), the generator's integers
    under the input stamp, written on the emitter of measured[`number`] (the train emitter's
    by `given_train`, the point emitter's on their own, ALGEBRA.md 9.71 (1); item 50). Returns
    the world parsed with them."""
    from event_universe.diagnostics.massive_record_margin import (
        block_margin,
        excitation_action,
        excitation_norm,
        period_of,
    )
    from event_universe.world_files import parse_nature_beam_world

    emitter = document["measured"][number]["emitter"]
    for key in ("period", "norm", "norm_denominator"):
        emitter.pop(key, None)
    world = parse_nature_beam_world(stamped(document))
    period = period_of(block_margin(world, number))
    emitter["period"] = period
    emitter["norm"] = excitation_norm(world, number, period)
    # THE WINDOW'S T (9.71 (1) (d); item 50): the action's exact rational
    action = excitation_action(world, number, period)
    assert action.numerator == emitter["norm"]
    emitter["norm_denominator"] = int(action.denominator)
    return parse_nature_beam_world(stamped(document))


def given_train(document: dict, number: int) -> None:
    """CANCELLED (commit 7; record 2102: marked, disconnected, not deleted): the given train
    is retired, every giving is the window's (ALGEBRA.md 9.85 (5), 9.71 (1)); called nowhere.
    THE GIVEN TRAIN (ALGEBRA.md 9.17 (6a); BUILD.md section 26 item 27): the emitter body
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
    the mode's as before (`excitation_norm`). THE BOOSTED NORM (ALGEBRA.md 9.74 (3), 9.75 (1);
    BUILD.md section 26 item 56): a moving body's train at its own boosted clock (item 49),
    written at the rest amplitude A, ALREADY carries the quantum's energy in the board's frame,
    D T_rest forward and T_rest / D backward, D = sqrt((1 + beta) / (1 - beta)), beta = v / c_l
    (`doppler_factor`): the form is quadratic in the wave number as in the amplitude (the
    energy of a wave A^2 k^2 L; k by D and the length by 1 / D), so no amplitude factor enters
    (the reading asked in 9.75 (1): the long-wave pair's ratio 1.577 against D = 1.596,
    COMPUTATION on the files' integers). `rest_norm`, the same train's norm at the family's
    own clock, is written beside `norm` (the ladder's threshold); the ratio norm / rest_norm
    is checked against D (1 / D backward) within 3 percent, else refused."""
    from event_universe.events.world import (
        given_train_flux_sign,
        given_train_norm,
    )

    entry = document["measured"][number]
    emitter = entry["emitter"]
    emitter.pop("given", None)
    world = emitter_rung(document, number)
    definition = world.measured[number].block
    assert definition is not None and definition.emitter is not None
    train = definition.emitter.train
    if train is None:
        raise ValueError(
            f"measured[{number}].emitter declares no `train` (the direction and the periods): "
            "every giving is a travelling train (ALGEBRA.md 9.17 (6a)); nothing written"
        )
    num, den = int(definition.emitter.pair[0]), int(definition.emitter.pair[1])
    p, q = train.clock
    steps = int(world.phase_steps)
    extents = tuple(int(v) for v in definition.extents)
    shape = (int(world.shape[0]), int(world.shape[1]), int(world.shape[2]))
    wrap = world.kind_periodic(definition.emitter.family)
    axis, sign = train.axis, train.sign
    k = 2.0 * math.pi * p / (2.0 * steps * q)
    omega = math.acos((num / den) * (math.cos(k) + 2.0) / 3.0)
    spanned = tuple(extents[a] == shape[a] and wrap[a] for a in range(3))
    # THE BOOSTED NORM (9.74 (3), 9.75 (1); item 56): the rest train (the
    # family's clock, the same amplitude and periods) written beside a boosted
    # train for its norm; the boosted rows' norm is read against D T_rest
    expected = 1.0
    rest_norm: int | None = None
    if train.boosted:
        # the rest clock is the given record's clock, the family's own or the
        # emitter's declared `clock` (ALGEBRA.md 9.85 (3); item 59)
        rest_clock = [int(definition.emitter.clock[0]), int(definition.emitter.clock[1])]
        entry = world.measured[number]
        wall = 3 * int(world.momentum_unit) * sum(int(value) for value in entry.held)
        momentum = int(entry.momentum[axis])
        if momentum == 0:
            raise ValueError(
                f"measured[{number}]: the train's own clock along {['x', 'y', 'z'][axis]} on a body "
                "with no momentum along it (ALGEBRA.md 9.62 (4)); nothing written"
            )
        forward = sign * momentum > 0
        doppler = doppler_factor(rest_clock, steps, [num, den], Fraction(abs(momentum), wall))
        expected = doppler if forward else 1.0 / doppler
        rest_wavelength = (2 * steps * rest_clock[1]) // rest_clock[0]
        rest_extents = list(extents)
        rest_extents[axis] = train.periods * rest_wavelength
        rest_k = 2.0 * math.pi * rest_clock[0] / (2.0 * steps * rest_clock[1])
        rest_omega = math.acos((num / den) * (math.cos(rest_k) + 2.0) / 3.0)
        rest_now, rest_before = train_rows(
            tuple(rest_extents), axis, sign, rest_k, rest_omega, float(GIVEN_AMPLITUDE), spanned
        )
        rest_shape = tuple(max(shape[a], rest_extents[a]) for a in range(3))
        rest_norm = given_train_norm(
            rest_now, rest_before, rest_shape, (0, 0, 0), tuple(rest_extents), (num, den), wrap
        )
    now, before = train_rows(extents, axis, sign, k, omega, float(GIVEN_AMPLITUDE), spanned)
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
    if rest_norm is not None:
        ratio = norm / rest_norm
        if not 0.97 * expected <= ratio <= 1.03 * expected:
            raise ValueError(
                f"measured[{number}]: the boosted train's norm {norm} over the rest train's "
                f"{rest_norm} is {ratio:.4f}, not the Doppler factor {expected:.4f} within 3 percent "
                "(ALGEBRA.md 9.74 (3), 9.75 (1)); nothing written"
            )
        emitter["given"]["rest_norm"] = rest_norm


def train_rows(
    extents: tuple[int, ...],
    axis: int,
    sign: int,
    k: float,
    omega: float,
    amplitude: float,
    spanned: tuple[bool, ...],
) -> tuple[list[int], list[int]]:
    """CANCELLED (commit 7): the given train's helper, disconnected, not deleted.
    The train's two levels over a box (`given_train`): the character of **K** under the
    Hann window across the transverse extents and the tapers over a quarter of the length at
    each end, at the amplitude, x-major (HOST, the generator's floats rounded once)."""
    length = extents[axis]
    taper = length // 4

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
                scaled = amplitude * shape_factor
                now.append(int(round(scaled * math.cos(k * along))))
                before.append(int(round(scaled * math.cos(k * along + omega))))
    return now, before


def doppler_factor(
    given_clock: list[int], phase_steps: int, given_pair: list[int], pace: Fraction
) -> float:
    """CANCELLED (commit 7): the given train's helper, disconnected, not deleted.
    D = sqrt((1 + beta) / (1 - beta)), beta = v / c_l, the Doppler factor of a light train
    given along the motion (ALGEBRA.md 9.74 (3), 9.75 (1)): the boosted norm D T_rest forward
    and T_rest / D backward; c_l the given family's group pace at the rest clock's k
    (`group_pace`). HOST, the generator's float; the file carries integers."""
    p, q = int(given_clock[0]), int(given_clock[1])
    k = 2.0 * math.pi * p / (2.0 * phase_steps * q)
    speed = group_pace((int(given_pair[0]), int(given_pair[1])), k)
    beta = float(pace) / speed
    if not 0 < beta < 1:
        raise ValueError(
            f"the body's pace {float(pace):.4f} is not between 0 and the given family's pace "
            f"{speed:.4f} at k = {k:.4f}: no boost (ALGEBRA.md 9.62 (4))"
        )
    return math.sqrt((1.0 + beta) / (1.0 - beta))


def names_of(document: dict) -> dict[str, int]:
    return {family["name"]: index for index, family in enumerate(families_of(document))}


def group_pace(pair: tuple[int, int], k: float) -> float:
    """The group velocity of the dispersion 3 cos omega = (num / den) (cos k + 2) along
    **K** (a HOST number for the checks' windows): d omega / d k = (num / den) sin k /
    (3 sin omega)."""
    num, den = pair
    cos_omega = (num / den) * (math.cos(k) + 2.0) / 3.0
    return (num / den) * math.sin(k) / (3.0 * math.sqrt(1.0 - cos_omega * cos_omega))


def doppler_clock(
    given_clock: list[int], phase_steps: int, given_pair: list[int], pace: Fraction, forward: bool
) -> tuple[list[int], int]:
    """CANCELLED (commit 7): the given train's helper, disconnected, not deleted.
    DOPPLER (ALGEBRA.md 9.62 (4), adopted by the model owner, record 2042; BUILD.md section
    26 item 49): the given rows of a moving body carry its motion in the given family's
    representation. For a train given along the motion (`forward`) or against it, the wave
    number k = 2 pi p / (2 N q) of the given family's clock is boosted to k' = k gamma (1 +- v /
    c_l), v the body's pace (Links per interval, the momentum over the drive's wall) and c_l the
    given family's group pace at k (`group_pace`), gamma = 1 / sqrt(1 - (v / c_l)^2); the
    train's wavelength is the whole number nearest 2 pi / k' (the loader's rule: a whole
    wavelength, the body's extent n of them), and the pair returned is [2 N / g, lambda' / g]
    with g their gcd, so that 2 N q' / p' = lambda' exactly. Returns (the pair, the wavelength).
    HOST, the generator's floats as `given_train` solves its clock; the engine reads the pair."""
    p, q = int(given_clock[0]), int(given_clock[1])
    k = 2.0 * math.pi * p / (2.0 * phase_steps * q)
    speed = group_pace((int(given_pair[0]), int(given_pair[1])), k)
    v = float(pace)
    if not 0 < v < speed:
        raise ValueError(
            f"the body's pace {v:.4f} is not between 0 and the given family's pace {speed:.4f} at "
            f"k = {k:.4f}: no boost (ALGEBRA.md 9.62 (4))"
        )
    gamma = 1.0 / math.sqrt(1.0 - (v / speed) ** 2)
    boosted = k * gamma * (1.0 + v / speed if forward else 1.0 - v / speed)
    wavelength = max(2, round(2.0 * math.pi / boosted))
    g = math.gcd(2 * phase_steps, wavelength)
    return [2 * phase_steps // g, wavelength // g], wavelength


def point_window(document: dict, number: int, weight: int, limit: int) -> int | None:
    """HOST: the first window's length of the emitter measured[`number`] at the weight
    `weight` on the document as it stands, run up to `limit` intervals; None when no window
    closed by then."""

    window, _ = window_reading(document, number, weight, limit)
    return window


def window_reading(document: dict, number: int, weight: int, limit: int) -> tuple[int | None, bool]:
    """HOST: the first window's length at the weight, or None; and whether the run was refused
    for a row above the world's amplitude bound (a body of several Nodes writing at all its
    Nodes piles the given row up inside itself; the weight is then too high)."""
    from event_universe.events.detector_law import DetectorLawSimulation
    from event_universe.world_files import parse_nature_beam_world

    trial = json.loads(json.dumps(document))
    trial["measured"][number]["emitter"]["weight"] = weight
    trial["ticks"] = limit
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(stamped(trial)), observer=lines.append)
    for _ in range(limit):
        try:
            simulation.step()
        except RuntimeError as error:
            if "amplitude bound" in str(error):
                return None, True
            raise
        for line in lines:
            if line.get("event") == "giving" and line.get("measured") == number:
                return int(line["window"]), False
        lines.clear()
    return None, False


def point_weight(document: dict, number: int, periods: int, start: int = 1) -> int:
    """THE EMITTER'S WEIGHT (ALGEBRA.md 9.71 (1), 9.85 (5); BUILD.md section 26 item 50): the
    integer g at which the window of measured[`number`] is nearest `periods` periods of the
    body's rotation (the window's length falls about as 1 / g^2, the outward norm growing as
    the square of the written amplitude): the window at g = `start` read first, the estimate
    g* = start sqrt(n_start / target) and its neighbours read, the nearest taken; written as
    the emitter's `weight`. HOST, a trial run of the generator; the engine reads the integer.
    SINCE COMMIT 7 every emitter's weight is chosen here (the window the one giving); a
    light clock's window is aimed shorter than its arm's round trip (9.85 (5) (a))."""
    emitter = document["measured"][number]["emitter"]
    target = periods * int(emitter["period"])
    # the window at g = 1 runs about 32 periods (the point chain's 1124 intervals at P = 35);
    # where a weight's window does not close within the limit (a moving body at g = 1: the
    # write chases the hop) the start weight is doubled, up to six times
    limit = max(12 * target, 64 * int(emitter["period"]))
    readings: dict[int, int] = {}
    over: set[int] = set()  # the weights whose rows rise above the world's amplitude bound

    def read(weight: int) -> int | None:
        window, exceeded = window_reading(document, number, weight, limit * weight * weight)
        if exceeded:
            over.add(weight)
        elif window is not None:
            readings[weight] = window
        return window

    first = None
    for _ in range(7):
        first = read(start)
        if first is not None or start in over:
            break
        start *= 2
    while start > 1 and start in over:  # the start weight itself too high: halved until it fits
        start //= 2
        first = read(start)
    if first is None:
        raise ValueError(
            f"measured[{number}]: the emitter's window did not close within {limit} intervals at "
            f"the weights tried up to {start}, or its rows rose above the bound; nothing written"
        )
    guess = max(1, round(start * math.sqrt(first / target)))
    for weight in sorted({guess, guess + 1, max(1, guess - 1)}):
        if weight not in readings and weight not in over and all(weight < w for w in over):
            read(weight)
    best = min(readings, key=lambda w: (abs(readings[w] - target), w))
    emitter["weight"] = best
    emitter["window_read"] = readings[best]  # HOST: the trial's window at the chosen weight
    return best


def giving_ticks(document: dict, number: int, extra: int) -> int:
    """HOST: a run's length covering every giving of the emitter measured[`number`]: its stock
    times (the window read at its weight plus two periods of its rotation, the rung's wait)
    plus `extra` intervals (the flights declared by the row's generator)."""
    entry = document["measured"][number]
    emitter = entry["emitter"]
    stock = int(entry["stock"]) if "stock" in entry else int(entry["stocks"][emitter["family"]])
    return stock * (int(emitter["window_read"]) + 2 * int(emitter["period"])) + extra


def train_run(
    document: dict,
    family: str,
    axis: int,
    sign: int,
    train_extents: tuple[int, int, int],
    transverse_corner: tuple[int, int, int],
    now: list[int],
    before: list[int],
    clock: tuple[int, int],
    pair: tuple[int, int] | None = None,
) -> int:
    """CANCELLED (commit 7): the given train's helper, disconnected, not deleted.
    THE GENERATOR'S RUN OF A TRAIN (HOST; ALGEBRA.md 9.25 (11) (a)): the train's two
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
    from event_universe.events.world import body_node_indices
    from event_universe.world_files import parse_nature_beam_world

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
    family_entry = families_of(document)[given]
    declared = family_entry.get("pair", [1, 1]) if pair is None else list(pair)
    if declared == "body":
        raise ValueError(
            f"the family {family!r} declares no pair; the train's pair is the emitter's (ALGEBRA.md "
            "9.85 (3)); nothing written"
        )
    pair = (int(declared[0]), int(declared[1]))
    p, q = clock  # the given record's clock, the emitter's (ALGEBRA.md 9.85 (3); item 59)
    k = 2.0 * math.pi * p / (2.0 * int(document["N"]) * q)
    window = math.ceil((TRAIN_FLUX_DISTANCE + 6 * length) / group_pace(pair, k))
    booked = 0
    for _ in range(window):
        simulation._advance(live)
        booked += simulation.inward_flux(live, plane)
    return booked


def given_clock_of(document: dict, number: int) -> tuple[int, int]:
    """THE GIVEN CLOCK of measured[`number`]'s emitter (ALGEBRA.md 9.85 (3); item 59): the
    emitter's declared `clock` [p, q], else the given family's own (`phase_per_link` on an
    inline families list)."""
    emitter = document["measured"][number]["emitter"]
    if "clock" in emitter:
        return int(emitter["clock"][0]), int(emitter["clock"][1])
    family_entry = families_of(document)[names_of(document)[emitter["family"]]]
    if "phase_per_link" not in family_entry:
        raise ValueError(
            f"measured[{number}].emitter declares no `clock` and the given family "
            f"{emitter['family']!r} declares none (ALGEBRA.md 9.85 (3)); nothing written"
        )
    return int(family_entry["phase_per_link"][0]), int(family_entry["phase_per_link"][1])


def train_passage_flux(document: dict, number: int, now: list[int], before: list[int]) -> int:
    """CANCELLED (commit 7): the given train's helper, disconnected, not deleted.
    THE FLUX CHECK'S READING (ALGEBRA.md 9.25 (11) (a)): the train alone on the vacuum,
    the plane TRAIN_FLUX_DISTANCE Links ahead of its head (`train_run`)."""
    entry = document["measured"][number]
    direction = entry["emitter"]["train"]["direction"]
    axis = next(index for index, v in enumerate(direction) if v != 0)
    sign = 1 if direction[axis] > 0 else -1
    corner = (int(entry["position"][0]), int(entry["position"][1]), int(entry["position"][2]))
    clock = given_clock_of(document, number)
    given_pair = entry["emitter"].get("pair")
    return train_run(
        document,
        entry["emitter"]["family"],
        axis,
        sign,
        block_extents_of(entry),
        corner,
        now,
        before,
        clock,
        pair=None if given_pair is None else (int(given_pair[0]), int(given_pair[1])),
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
    from event_universe.events.world import body_node_indices, mode_residual
    from event_universe.world_files import parse_nature_beam_world

    world = parse_nature_beam_world(stamped(document))
    flat, clock, _ = iterated_mode(world, number, amplitude)
    entry = world.measured[number]
    block = entry.block
    assert block is not None
    kind = block.kind  # the body's rest pair (ALGEBRA.md 9.91 (7); commit 1)
    shape = (int(world.shape[0]), int(world.shape[1]), int(world.shape[2]))
    wrap = world.kind_periodic(entry.family)
    corner = (int(entry.position[0]), int(entry.position[1]), int(entry.position[2]))
    count = shape[0] * shape[1] * shape[2]
    num, den = [kind[0]] * count, [kind[1]] * count
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


def mode_dispersion(document: dict, number: int, axis: int) -> tuple[Fraction, Fraction]:
    """THE MODE'S OWN DISPERSION ALONG AN AXIS (ALGEBRA.md 9.63 (3), 9.46 (7) (b), 9.24 (2)):
    the bound mode's profile p times the character of K along `axis` rotates at 2 cos omega_K
    = 2 cos omega_b - (1 - cos K) X, with X = SUM_i num_i p_i (p_{i+e} + p_{i-e}) / (3 SUM_i
    den_i p_i^2) the profile's own quotient on the axis's two reads (the operator's quotient
    as `iterated_mode` reads the clock, every Node weighing in; the reads wrap on a periodic
    axis and are zero beyond a face). Returns (2 cos omega_b, X) as exact rationals, 2 cos
    omega_b the entry's clock a / b. On a plane wave X = 2 num / (3 den) and the line is the
    free dispersion 3 cos omega = (num / den)(cos K + 2) of 9.24 (2) exactly. HOST, the
    generator's own reading of its integers."""
    import numpy as np

    entry = document["measured"][number]
    shape = [int(extent) for extent in document["shape"]]
    profile = np.array(entry["seed"], dtype=object).reshape(shape)
    kind = kind_of(document, entry)
    num = np.full(shape, int(kind[0]), dtype=object)
    den = np.full(shape, int(kind[1]), dtype=object)
    corner = [int(component) for component in entry["position"]]
    extents = [int(entry["side"])] * 3 if "side" in entry else [int(v) for v in entry["extents"]]
    wrap = tuple(document["boundary"][name] == "periodic" for name in ("x", "y", "z"))
    for index in range(3):
        if wrap[index]:
            continue
        if corner[index] < 0 or corner[index] + extents[index] > shape[index]:
            raise ValueError(f"measured[{number}] leaves the board on an open axis; nothing written")
    on_body = np.zeros(shape, dtype=bool)
    for x in range(extents[0]):
        for y in range(extents[1]):
            for z in range(extents[2]):
                on_body[
                    (corner[0] + x) % shape[0], (corner[1] + y) % shape[1], (corner[2] + z) % shape[2]
                ] = True
    num[on_body] = int(entry["pair"][0])
    den[on_body] = int(entry["pair"][1])
    reads = np.zeros(shape, dtype=object)
    for side in (1, -1):
        shifted = np.roll(profile, side, axis=axis)
        if not wrap[axis]:
            edge = [slice(None)] * 3
            edge[axis] = slice(0, 1) if side == 1 else slice(shape[axis] - 1, shape[axis])
            shifted[tuple(edge)] = 0
        reads = reads + shifted
    quotient = Fraction(int(np.sum(num * profile * reads)), 3 * int(np.sum(den * profile * profile)))
    a, b = entry["clock"]
    return Fraction(int(a), int(b)), quotient


def moving_rotation(two_cos_rest: float, quotient: float, pace: float) -> tuple[float, float]:
    """The moving mode at the pace v = `pace` Links per interval on the dispersion 2 cos
    omega_K = 2 cos omega_b - (1 - cos K) X: the wavenumber K at which the group pace X sin
    K / (2 sin omega_K) equals v (bisection on [0, pi], the host's floats as `given_train`
    solves its clock) and the rotation of the rows at the moving centre per interval,
    omega_K - K v (ALGEBRA.md 9.63 (3), 9.24 (2)); on the plane wave of [800, 809] at v = 1 /
    3 the algebra's own K = 0.18556 and (omega_K - K v) / omega_b = 0.81457 (COMPUTATION)."""

    def omega_at(k: float) -> float:
        return math.acos((two_cos_rest - (1.0 - math.cos(k)) * quotient) / 2.0)

    low, high = 0.0, math.pi
    for _ in range(200):
        middle = 0.5 * (low + high)
        group = quotient * math.sin(middle) / (2.0 * math.sin(omega_at(middle)))
        if group < pace:
            low = middle
        else:
            high = middle
    wavenumber = 0.5 * (low + high)
    return wavenumber, omega_at(wavenumber) - wavenumber * pace


def proper_clock(document: dict, number: int) -> list[list[int]]:
    """THE PROPER PAIRS OF A MOVING BODY ON ONE NODE (ALGEBRA.md 9.63 (3); BUILD.md section 26 item 46; the
    mathematician's ruling on Nature24's finding that the body's Node's clock did not slow in motion):
    for a block with the momentum P on one axis, the pair [num_m, b] for every whole part m of
    the momentum from 0 to |P| (the ramp's P t // ramp, then P; the engine's `_momentum_now`),
    b the clock's denominator and num_m = round(b 2 cos(omega_K - K v)) with v = m / W the hop
    rate (W = 3 Q S M, the drive's wall) and (K, omega_K - K v) from `moving_rotation` on the
    mode's own dispersion (`mode_dispersion`): the rotation of the moving mode's rows at its
    moving centre per interval, which the body's Node rotates at between hops; at m = 0 the clock
    itself. The cube carries the dilation in its rows by the rule; the body's Node carries it in
    this declared pair, the seam of the host form (9.46). HOST, the generator's; the engine
    reads the integers alone."""
    entry = document["measured"][number]
    momentum = [int(component) for component in entry.get("momentum", [0, 0, 0])]
    axes = [axis for axis in range(3) if momentum[axis] != 0]
    if len(axes) != 1:
        raise ValueError(
            f"measured[{number}]: the proper pair is read along one axis of motion; the momentum "
            f"{momentum} lies on {len(axes)} (ALGEBRA.md 9.63 (3)); nothing written"
        )
    two_cos_rest, quotient = mode_dispersion(document, number, axes[0])
    a, b = (int(value) for value in entry["clock"])
    # the body's wall W = 3 Q M on its whole content, its own quanta and what it holds
    # (ALGEBRA.md 9.96 (1); Q the universe's `momentum_unit`)
    content = int(entry.get("amount", 1)) + sum(int(value) for value in entry.get("stocks", {}).values())
    wall = 3 * universe_integer(document, "momentum_unit") * content
    table = [[a, b]]
    for whole in range(1, abs(momentum[axes[0]]) + 1):
        _, rotation = moving_rotation(float(two_cos_rest), float(quotient), whole / wall)
        table.append([round(b * 2.0 * math.cos(rotation)), b])
    return table


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(bind_universe_file(document), indent=1) + "\n", encoding="utf-8")
        print(path.name)


if __name__ == "__main__":
    main()
