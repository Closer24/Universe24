"""CANCELLED (the one stroke's commit 7; ALGEBRA.md 9.85 (5), 9.91 (10) 7; the model owner's
record 2102: marked and disconnected, not deleted): the given train is retired, every giving is
the window's; this suite is skipped whole, its text and its helpers kept as the record.
THE GIVEN TRAIN (ALGEBRA.md 9.17 (6a), 9.25 (11), 9.22 (7a) (iv); BUILD.md section 26 item
27): every giving is a travelling train, the character of one **K** over 8 periods under the
window across the transverse extents and the tapers along **K**, written on the body's Nodes
at both levels; the generator's integers (the profile, its norm on the vacuum), its checks
(the flux sign, the passage's one-way flux within 2 x 10^-3 of the norm, the transparency of a
coupled body, the placement one train's length from every face slab), the loader's checks in
integers (in `tests/test_emitter.py`, the refusals by name; in `tests/test_initial_state.py`,
the stamp moving with the profile), the engine's write and the passage read by a receiver
ahead, and the registered light clock in the one table's form. Every number here is the
engine's or the generator's on the line's small worlds (COMPUTATION, HOST); no pin.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import (
    body_node_indices,
    given_train_flux_sign,
    given_train_norm,
)
from event_universe.world_files import parse_nature_beam_world
from tests.worlds import NODE_CLOCK, emitter_world, layer_world, massive_generator

pytestmark = pytest.mark.skip(
    reason="CANCELLED at commit 7: the given train is retired, every giving is the window's "
    "(ALGEBRA.md 9.85 (5), 9.91 (10) 7; record 2102: marked, not deleted)"
)

ROOT = Path(__file__).resolve().parents[1]
LIGHT_CLOCK = ROOT / "examples/events/massive_record/light_clock.json"
AMPLITUDE = 1 << 16
TRAIN = 32
COS_OMEGA = 2.0 / 3.0  # light's vacuum at k = pi / 2: 3 cos omega = cos k + 2


def profile_of(document: dict, number: int = 0) -> dict:
    return document["measured"][number]["emitter"]["given"]


def test_the_generators_train_is_the_character_under_the_tapers_and_the_window():
    """THE INTEGER FORM (ALGEBRA.md 9.17 (6a)): on the emitter world's chain the train's 32
    integers are round(A e(i) cos(pi i / 2)) and round(A e(i) cos(pi i / 2 + omega)) with
    A = 2^16, omega = acos(2 / 3) (light's vacuum at the wavelength 4) and the tapers of
    tau = 8 at both ends: the flat middle reads 65536, 0, -65536, 0 at t = 0 and 43691,
    -48848, -43691, 48848 at t = -1, the first detector 630 (sin^2(pi / 32) of A) and the last
    0, the profile exactly the formula at every detector; the flux along +x positive and along
    -x negative (the loader's sign, `given_train_flux_sign`); the norm the conserved form of
    the record planted alone on the vacuum, bit for bit (`given_train_norm` against the
    engine's `conserved_form`). On a layer the window across a transverse extent the body
    does not span is the Hann window sin^2(pi (y + 1 / 2) / Y) (the edge rows 0.0955 of the
    middle on Y = 5), and across an extent the body spans on a periodic face the profile is
    UNIFORM (the extruded form of the one table): the layer world's rows equal."""
    document = emitter_world(stock=1)
    train = profile_of(document)
    now, before = train["now"], train["before"]
    assert len(now) == len(before) == TRAIN
    omega = math.acos(COS_OMEGA)

    def envelope(i: int) -> float:
        tau = TRAIN // 4
        if i < tau:
            return math.sin(math.pi * (i + 0.5) / (2 * tau)) ** 2
        if i >= TRAIN - tau:
            return envelope(TRAIN - 1 - i)
        return 1.0

    for i in range(TRAIN):
        assert now[i] == round(AMPLITUDE * envelope(i) * math.cos(math.pi * i / 2)), i
        assert before[i] == round(AMPLITUDE * envelope(i) * math.cos(math.pi * i / 2 + omega)), i
    assert now[8:12] == [65536, 0, -65536, 0] and before[8:12] == [43691, -48848, -43691, 48848]
    assert now[0] == 630 and now[TRAIN - 1] == 0
    extents = (TRAIN, 1, 1)
    assert given_train_flux_sign(now, before, extents, 0, 1) > 0
    assert given_train_flux_sign(now, before, extents, 0, -1) < 0
    # the norm on the vacuum against the engine's conserved form of the planted train
    vacuum = json.loads(json.dumps(document))
    vacuum["measured"] = []
    vacuum["detectors"] = []
    vacuum.pop("stamp", None)
    world = parse_nature_beam_world(vacuum)
    simulation = DetectorLawSimulation(world)
    shape = (int(world.shape[0]), 1, 1)
    nodes = body_node_indices(shape, (5, 0, 0), extents, world.kind_periodic(0))
    level_now = np.zeros(shape, dtype=np.int64).reshape(-1)
    level_before = np.zeros(shape, dtype=np.int64).reshape(-1)
    for index, a, b in zip(nodes, now, before, strict=True):
        level_now[index] = a
        level_before[index] = b
    live = simulation.planted_record(0, level_now.reshape(shape), level_before.reshape(shape))
    norm = given_train_norm(now, before, shape, (0, 0, 0), extents, (1, 1), world.kind_periodic(0))
    # the engine's form under the Node's own pace is the file's vacuum norm itself on the
    # vacuum (no content anywhere; the Node's terms weighted by 1 / Gamma; BUILD.md section
    # 26 item 36)
    assert norm == train["norm"] > 0 and Fraction(*simulation.conserved_form(live)) == norm
    # the window across y on a layer: Y = 5 not spanned, then Y = 9 spanned (uniform)
    layer = layer_world()
    layer["measured"][0]["extents"] = [TRAIN, 5, 1]
    layer["measured"][0]["position"] = [2, 2, 0]
    layer["measured"][0]["seed"] = 1 << 20
    layer["measured"][0].pop("clock", None)
    layer["measured"][0]["emitter"].pop("given", None)
    massive_generator().seed_on_the_mode(layer)
    windowed = profile_of(layer)["now"]
    rows = [windowed[y::5][:TRAIN] for y in range(5)]  # x-major: the 5 rows interleaved
    peak = max(abs(v) for v in rows[2])
    assert peak == AMPLITUDE
    edge = max(abs(v) for v in rows[0])
    assert rows[0] == rows[4] and rows[1] == rows[3]
    assert abs(edge / peak - math.sin(math.pi * 0.5 / 5) ** 2) < 1e-3
    spanned = profile_of(layer_world())["now"]
    assert all(spanned[i] == spanned[i - i % 9] for i in range(len(spanned)))


def test_the_passage_books_the_norm_and_a_short_train_does_not(capsys):
    """THE FLUX CHECK (ALGEBRA.md 9.25 (11) (a), the generator's `train_passage_flux`): the
    emitter world's train alone on the vacuum books its one-way flux through a plane 40
    Links ahead within 2 x 10^-3 of its norm (COMPUTATION; the mathematician's 0.9987 on his
    window), while a train of 3 periods (12 Nodes, the same formula) books above it: 1.0052
    read on the generator's window of six trains (`train_run` on the 3-period profile; the
    mathematician's 1.0285 on his longer window, the standing parts' sloshing growing),
    outside the tolerance and refused. The loader refuses periods below 8 by name before
    that (`tests/test_emitter.py`)."""
    generator = massive_generator()
    document = emitter_world(stock=1)
    train = profile_of(document)
    # the check board's engine books the plain flux, the wall times the current (BUILD.md
    # section 26 item 36); the file's norm is the plain vacuum form, the same units
    booked = generator.train_passage_flux(document, 0, train["now"], train["before"])
    ratio = booked / train["norm"]
    print(f"the emitter chain's train books {ratio:.5f} of its norm (HOST)")
    assert abs(ratio - 1.0) < 2e-3, ratio
    omega = math.acos(COS_OMEGA)
    short = 12
    tau = short // 4

    def envelope(i: int) -> float:
        if i < tau:
            return math.sin(math.pi * (i + 0.5) / (2 * tau)) ** 2
        if i >= short - tau:
            return envelope(short - 1 - i)
        return 1.0

    now = [round(AMPLITUDE * envelope(i) * math.cos(math.pi * i / 2)) for i in range(short)]
    before = [round(AMPLITUDE * envelope(i) * math.cos(math.pi * i / 2 + omega)) for i in range(short)]
    norm = given_train_norm(
        now, before, (80, 1, 1), (0, 0, 0), (short, 1, 1), (1, 1), (False, True, True)
    )
    booked = generator.train_run(
        document, "light", 0, 1, (short, 1, 1), (5, 0, 0), now, before, (512, 1)
    )  # the given clock, the emitter's (item 59)
    print(f"the 3-period train books {booked / (NODE_CLOCK**2 * norm):.4f} of its norm (HOST)")
    assert booked / norm > 1.002


def test_the_engine_writes_the_train_and_a_receiver_ahead_reads_its_passage():
    """THE WRITE AND THE PASSAGE: on the emitter world (the screen 33 Links ahead of the
    train's head) every given record is written as the train (in `tests/test_emitter.py`
    the levels bit for bit) and TRAVELS: the centroid of its levels' magnitude advances
    along +x at about the group pace 0.447 between the ages 10 and 30 (more than 6 Links);
    the screen books the passage and each record clicks there once, its pointer at the
    click at or above the rung (2 u + 1) T / (2 W) and at most 1.02 T (the passage books
    the norm, nothing more), the record deleted whole at it; the books balanced."""
    document = emitter_world(stock=2, ticks=600)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    screen = simulation.detector_names.index("screen")
    at_click: dict[int, tuple[int, int, int, int, int]] = {}
    original = simulation._ladder_click

    def spy(live, increments):
        pointer = live.pointers[screen]
        original(live, increments)
        if live.clicked and live.identity not in at_click:
            at_click[live.identity] = (pointer, live.u, live.norm, live.wheel, live.pace)

    simulation._ladder_click = spy  # type: ignore[method-assign]
    centroids: dict[int, dict[int, float]] = {}
    for _ in range(600):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        for live in simulation.records.values():
            if live.family != 0:
                continue
            weights = np.abs(live.now[:, 0, 0]).astype(np.float64)
            if weights.sum() > 0 and live.age in (10, 30):
                centroids.setdefault(live.identity, {})[live.age] = float(
                    (weights * np.arange(weights.size)).sum() / weights.sum()
                )
    gathers = [line for line in lines if line["event"] == "gather"]
    assert len(gathers) == 2 and all(g["chosen"][0][0] == "screen" for g in gathers)
    for identity, seen in centroids.items():
        assert 30 in seen and seen[30] - seen[10] > 6.0, (identity, seen)
    for gather in gathers:
        pointer, u, norm, wheel, pace = at_click[gather["record"]]
        # the plain flux against the norm's rational norm / pace (item 36)
        assert 2 * wheel * pace * pointer >= (2 * u + 1) * norm
        assert pointer * pace * 100 <= 102 * norm
        assert gather["record"] not in simulation.records


def test_the_light_clock_in_the_tables_form_and_the_generators_checks(capsys):
    """THE LIGHT CLOCK (ALGEBRA.md 9.22 (8), its row; the one table of 9.30; the module
    docstring of the detector-law generator): the registered file carries the board
    [760, 3, 3] with x open and the face slabs 32 deep, N = 1024 and the emitter's given clock
    [512, 1] (the families file's light declares none; item 59), A [800, 801] of the extents [32, 3, 3] at [600, 632) with its train along +x
    uniform across y and z, its stock 64 and its `receiver` at_well, the set at_well bound
    to A without positions, the mirror of light's kind with the gap [1, 2] over [4, 3, 3] at
    [690, 694); it loads and constructs. The generator's readings on it (HOST): the passage
    books the norm within 2 x 10^-3 (1.0002 read); the transparency reading of 9.22 (7a) (iv)
    is HISTORY with the coupling (the model owner's decision (2) of record 1962). The
    placement rule (9.25 (11) (b)): A moved to [10, 42), nine Links from the low slab's
    front, is refused by the generator naming the emitter and the slab; a set nearer than
    one train's length to the high slab likewise."""
    document = json.loads(LIGHT_CLOCK.read_text(encoding="utf-8"))
    assert document["shape"] == [760, 3, 3] and document["face_depth"] == 32
    # the families file names the world's families; light's clock is the emitter's (item 59)
    assert document["N"] == 1024 and document["universe"] == "examples/events/families.json"
    a = document["measured"][0]
    assert a["extents"] == [32, 3, 3] and a["position"] == [600, 0, 0] and a["pair"] == [800, 801]
    # the stock as the given family's content held at the body (item 47): one own quantum
    assert a["amount"] == 1 and a["held"] == {"charge": 64} and a["receiver"] == "at_well"
    assert a["family"] == "matter" and a["kind"] == [800, 809]  # the body's rest pair (9.91 (7))
    assert a["emitter"]["train"] == {"direction": [1, 0, 0], "periods": 8}
    assert a["emitter"]["clock"] == [512, 1]
    train = profile_of(document)
    assert len(train["now"]) == 288 and all(
        train["now"][i] == train["now"][i - i % 9] for i in range(288)
    )
    mirror = document["measured"][1]
    assert mirror["family"] == "charge" and mirror["pair"] == [1, 2]  # light's kind, the charge's
    assert mirror["extents"] == [4, 3, 3] and mirror["position"] == [690, 0, 0]
    assert document["detectors"] == [{"name": "at_well", "block": 0}]
    world = parse_nature_beam_world(document)
    DetectorLawSimulation(world)
    generator = massive_generator()
    booked = generator.train_passage_flux(document, 0, train["now"], train["before"])
    ratio = booked / train["norm"]  # the plain flux in the norm's own units (item 36)
    assert abs(ratio - 1.0) < 2e-3
    print(f"the light clock (HOST): the passage {ratio:.4f} of the norm")
    near = json.loads(json.dumps(document))
    near["measured"][0]["position"] = [10, 0, 0]
    with pytest.raises(ValueError, match=r"the emitter measured\[0\] stands .* from the low face slab"):
        generator.placement_check(near)
    close = json.loads(json.dumps(document))
    close["detectors"].append({"name": "late", "positions": [[720, 0, 0], [720, 1, 0], [720, 2, 0]]})
    with pytest.raises(ValueError, match=r"the receiver 'late' stands .* from the high face slab"):
        generator.placement_check(close)
