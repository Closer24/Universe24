"""The worlds of the Beam Law on minimal GameBoards (docs/BEAM_LAW.md,
section 7; the model owner, 2026-09-19): the two slits as a world test with a
pinned correlation, the Bell run A2 unchanged, and one content on an open
GameBoard with the books closed. The expected results of
docs/TEST_EXPECTATIONS.md ("The worlds of the Beam Law"), written down first:

(a) the two slits (the example world's design, 60 x 121 x 1, z periodic,
    500 intervals): a lamp at (2, 60) of turn 8 per self-creation (K 2^30,
    content 8 K + 1 400 000, 64 rays per self-creation on five directions),
    a wall at x = 8 measuring light with the openings at y = 55 and 65
    re-emitting on the fan of the 91 primitive directions (a, b, 0) with
    a >= 1 and a + |b| <= 12, a screen at x = 52 read as 121 one-Node
    detectors `screen_<y>` (the screen's pixels) under the reading `wave`
    (the model owner, 2026-09-19: a detector is a set of Nodes with one
    record, so a screen declared as one detector of 121 Nodes would read
    one record with no resolution in y; a pixel one Node wide reads what
    the Node read before, so the record is unchanged).
    Three runs, both openings and each alone: the plain count is additive
    to the unit (count_both = count_55 + count_65 at every screen Node) and
    the interference term V(y) = (I_both - I_55 - I_65) / (2 sqrt(I_55
    I_65)) of the record correlates with the two-source Euclidean cosine at
    lambda = c x period = 8 / sqrt 3 above 0.85 over the Nodes both
    openings reach (the design pinned 0.9 for a fan of 203 directions; rays
    measured 0.893 with the 91 of this world), and the correlation at the
    periods 4 and 16 is below 0.5;
(b) Bell (the ten A2 worlds under `"law": "beam"`, `tools/click_readings/bell.py`):
    S = 2 exactly, S' = 3/2 exactly, the controls +1, -1, 0, no-signalling
    exact, 0 criteria failed; the registered plus offset derived from the
    flight table (the tick of the first birth plus the age at which a
    heading row has walked the 8 Links, DERIVATIONS_BEAM 11.1) and compared;
(c) one content of 2^24 at the centre of an open 11^3 GameBoard at `release`
    [1, 128], 40 intervals: the books close at every tick, the content is
    2^24 at every tick, the momentum on the measured events zero, the flux
    through the cube of half-width 2 equals the emission q = 6 x 2^17 at
    every interval once the front has passed (six beams on the six
    headings, a ballistic stream: Gauss exact); the shell means once
    steady: the count at r = 3 and r = 4 is 6 x 2^17 over the shell's
    Nodes (one ray of 2^17 arrives at each axial Node every interval), the
    presence at r = 3 twice the count (the ages 5 and 6 sit at 3 Links: the
    flight table's first arrivals at 3 and 4 Links are the intervals 5 and
    7) and at r = 4 equal to it (the age 7 alone);
(d) every example world parses as a NatureBeam world, and every path of the
    gate set (`examples/events/gate_set.json`, the worlds replayed at every
    commit of an integration; the model owner, 2026-09-20) exists, parses as
    one, is listed once, at its declared `ticks`, with a `cap` no longer than
    them and a line saying what it covers, and carries its three `digests`
    exactly when it has no lamp (a structural check, no pinned number);
(e) `two_contents` (the two contents 8 Links apart on the open 21^3 GameBoard)
    for 20 intervals: not refused (the night's bound refused it at the 20th
    interval, when the two +y beams of 2^17 click face:+y together, 2^18 in
    one interval); the books close at every tick; every face's record grows
    at every tick by the Python-int square of the pointer of the rows that
    clicked there (X = sum 32 x amount x C[phase], Y the same with S,
    through the tables from the click lines); at the 20th interval face:+y
    records 2^62 exactly, one past the law's bound 2^62 - 1, and face:+x,
    clicked 2^17 per interval since the 13th, holds 2^63, beyond int64 and
    round-tripped through JSON; the two pushes are equal and opposite along
    x, toward each other (the third law on lone beams).
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.diagnostics.shell_readings import shell_readings
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import direction_flight
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import MOMENTUM_BOUND
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


P = 12
FAN = [
    [a, b, 0]
    for a in range(1, P + 1)
    for b in range(-P, P + 1)
    if a + abs(b) <= P and math.gcd(a, abs(b)) == 1 and (a, b) != (1, 0)
]
K_SLITS = 1 << 30
TURN = 8
WALL_X, SCREEN_X, TICKS = 8, 52, 500


def slits(openings: tuple[int, ...]) -> dict[str, object]:
    measured: list[dict[str, object]] = [
        {
            "position": [2, 60, 0],
            "family": "light",
            "amount": TURN * K_SLITS + 1400000,
            "phase": 0,
            "fixed": True,
            "lamp": {
                "wheel": [1, 64],
                "rate": [64, 1],
                "directions": [[1, 0, 0], [1, 1, 0], [1, -1, 0], [2, 1, 0], [2, -1, 0]],
            },
        }
    ]
    for y in range(121):
        entry: dict[str, object] = {
            "position": [WALL_X, y, 0],
            "family": "wall",
            "amount": 1,
            "fixed": True,
        }
        if y in openings:
            entry["table"] = {"light": "rerelease"}
            entry["directions"] = [[1, 0, 0], *FAN]
        measured.append(entry)
    screen = []
    for y in range(121):
        measured.append({"position": [SCREEN_X, y, 0], "family": "wall", "amount": 1, "fixed": True})
        screen.append(
            {
                "name": f"screen_{y}",
                "positions": [[SCREEN_X, y, 0]],
                "threshold": 1,
                "reading": "wave",
            }
        )
    return {
        "law": "beam",
        "model_id": f"rays-test-slits-{len(openings)}",
        "shape": [60, 121, 1],
        "boundary": {"z": "periodic"},
        "ticks": TICKS,
        "K": K_SLITS,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "directions": FAN,
        "families": [{"name": "light", "quantum": 1}, {"name": "wall", "quantum": 1}],
        "measured": measured,
        "detectors": screen,
    }


def screen_readings(openings: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray]:
    simulation = NatureBeamSimulation(parse_nature_beam_world(slits(openings)))
    for tick in range(TICKS):
        simulation.step()
        if tick % 100 == 0:
            assert simulation.books()["balanced"], tick
    assert simulation.books()["balanced"]
    record = np.zeros(121, dtype=np.int64)
    count = np.zeros(121, dtype=np.int64)
    for entry in simulation.measured.values():
        if entry.detector is not None:
            record[entry.position[1]] = entry.detector_set.record[0]
            count[entry.position[1]] = entry.clicks[0]
    reports = simulation.detectors()[:121]
    assert [r["name"] for r in reports] == [f"screen_{y}" for y in range(121)]
    assert sum(r["families"]["light"]["clicks"] for r in reports) == int(count.sum()) > 0
    return record, count


def test_the_two_slits_fringe_in_the_record_and_not_in_the_count():
    """(a)."""
    both, count_both = screen_readings((55, 65))
    one, count_one = screen_readings((55,))
    two, count_two = screen_readings((65,))
    assert (count_both == count_one + count_two).all()
    lit = (one > 0) & (two > 0)
    assert int(lit.sum()) >= 20
    visibility = (both[lit] - one[lit] - two[lit]).astype(float) / (
        2 * np.sqrt(one[lit].astype(float) * two[lit].astype(float))
    )
    assert (np.abs(visibility) <= 1.0 + 1e-9).all()
    ys = np.flatnonzero(lit)
    length = SCREEN_X - WALL_X
    r1 = np.sqrt(length**2 + (ys - 55) ** 2)
    r2 = np.sqrt(length**2 + (ys - 65) ** 2)
    speed = 1 / math.sqrt(3)
    correlations = {}
    for period in (4, 8, 16):
        cosine = np.cos(2 * math.pi * (r1 - r2) / (period * speed))
        correlations[period] = float(np.corrcoef(visibility, cosine)[0, 1])
    # Re-run under the one click (stage (vii) step 4); the verdict to be
    # re-read: the lamp's rows are records with the path phase alone, so the
    # fringe reads the per-Link turn without the crowd form's emission lag
    # (the lamp's clock turn per interval) and its period doubles: the
    # correlation 0.80 at 16, 0.12 at 8, 0.35 at 4 (until that step 0.85 or
    # more at 8 and below 0.5 at 4 and 16). This reads the rows' `wave`
    # record per pixel (the GameBoard's absorptions); the record's own
    # reading is its gathers, which the ladder lands on five pixels of the
    # screen (the register's A1 line), not a fringe this test reads.
    assert correlations[16] > 0.75, correlations
    assert abs(correlations[8]) < 0.5 and abs(correlations[4]) < 0.5, correlations


def test_the_bell_worlds_read_the_triangle_and_the_chsh_bound(tmp_path):
    """(b)."""
    make_worlds = load_script(
        "bell_make_worlds", ROOT / "examples" / "events" / "bell" / "make_worlds.py"
    )
    bell = load_script("bell_chsh", ROOT / "tools" / "click_readings" / "bell.py")
    for a, b in make_worlds.SETTINGS:
        document = make_worlds.world(a, b)
        source = json.dumps(document).encode("utf-8")
        output = tmp_path / f"a{a}_b{b}"
        output.mkdir()
        execute_nature_beam_run(
            parse_nature_beam_world(document), source, output, "test", int(document["ticks"])
        )
    # The pair lamp's rows are records with the path phase 0 and the
    # counters' windows read the path phase, so every pair of a world lands
    # in one cell, E = +1 or -1 by the settings' half circles, S = 2 and
    # S' = 2, and 115 of the tool's 350 criteria of the crowd form fail
    # (the minus counters silent on most worlds, every pair in one cell, no
    # pass; since the fraction-free law of 2026-09-20 the tool reads a pair
    # by its record and its age as the birth ordinal, ten criteria of the
    # record on the lines added, and the exact clock's one stall at tick 4
    # moves no correlation: 118 of 340 under the one click read by tick;
    # until stage (vii) step 4 the triangle: 0 failed, S = 2, S' = 3/2,
    # E(0, 16) = 0).
    # The numbers are the register's (`examples/events/bell/expectations.json`,
    # since 2026-09-21: a test reads a world's numbers from the register).
    registered = json.loads(
        (ROOT / "examples" / "events" / "bell" / "expectations.json").read_text(encoding="utf-8")
    )
    assert registered["format"] == "bell-expectations-v1"
    assert bell.main([str(tmp_path)]) == registered["tool_exit"]
    checks = bell.Checks()
    runs = {
        run.setting: run
        for run in (bell.analyse(folder, checks) for folder in sorted(tmp_path.iterdir()))
    }
    assert checks.failed == registered["failed"] and len(checks.rows) == registered["criteria"]
    assert runs[(0, 0)].offsets == registered["offsets_0_0"]
    # The registered plus offset derived and compared (DERIVATIONS_BEAM 11.1,
    # the register's `derivations`; a formula gives, a run proves, record
    # 205): a pair's age is its birth ordinal less one, so the offset tick -
    # age of a plus counter is the tick of the lamp's first birth plus the
    # age tau_8 at which a heading row has walked the PATH Links to it, the
    # least age whose Manhattan steps (the position accumulator's count,
    # `Flight.manhattan_steps`) reach PATH; the minus counters, one Link
    # on, hold no click under the one click (0).
    first_birth = min(
        int(line["tick"])
        for line in map(
            json.loads,
            (tmp_path / "a0_b0" / "events.jsonl").read_text(encoding="utf-8").splitlines(),
        )
        if line["event"] == "birth"
    )
    table = direction_flight(((0, 0, 0), (0, 0, 0), (1, 0, 0)))
    ages = np.arange(1, 8 * make_worlds.PATH, dtype=np.int64)
    walked = table.manhattan_steps(np.full(ages.shape, 2, dtype=np.int64), ages)
    tau = int(ages[np.flatnonzero(walked >= make_worlds.PATH)[0]])
    assert registered["offsets_0_0"]["alice_plus"] == first_birth + tau
    assert registered["offsets_0_0"]["bob_plus"] == first_birth + tau
    assert registered["offsets_0_0"]["alice_minus"] == registered["offsets_0_0"]["bob_minus"] == 0
    assert bell.chsh(runs, bell.CHSH) == registered["chsh_sum"]
    assert bell.chsh(runs, bell.PRIME) == registered["primed_sum"]
    for key, correlation in registered["correlations"].items():
        a, b = (int(v) for v in key.split("_"))
        assert runs[(a, b)].correlation == correlation, key


def test_one_content_streams_outward_with_the_books_closed():
    """(c)."""
    content = 1 << 24
    world = {
        "law": "beam",
        "model_id": "rays-test-one",
        "shape": [11, 11, 11],
        "boundary": "open",
        "ticks": 40,
        "K": 1 << 22,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "families": [{"name": "m", "quantum": 0, "charge": 0, "phase": False}],
        "measured": [{"position": [5, 5, 5], "family": "m", "amount": content, "fixed": True}],
    }
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    emission = 6 * (content // 128)
    centre = (5, 5, 5)
    for tick in range(1, 41):
        simulation.step()
        books = simulation.books()
        assert books["balanced"], tick
        line = books["families"]["m"]["measured"]
        assert line["current"] == line["initial"] == content and line["measured"] == line["spent"] == 0
        assert books["momentum"]["measured"] == [0, 0, 0]
        if tick > 20:
            assert simulation.cube_flux(0, centre, 2) == emission, tick
            three = shell_readings(simulation, 0, centre, 3)
            four = shell_readings(simulation, 0, centre, 4)
            assert (
                three["arrived"] * three["nodes"] == emission
                and four["arrived"] * four["nodes"] == emission
            )
            assert three["presence"] == 2 * three["arrived"] and four["presence"] == four["arrived"], (
                tick
            )


@pytest.mark.parametrize(
    "name", ["one_content.json", "two_contents.json", "two_slits.json", "one_slit.json"]
)
def test_the_example_worlds_parse_as_nature_beam_worlds(name):
    path = ROOT / "examples" / "events" / name
    document = json.loads(path.read_text(encoding="utf-8"))
    # Through the loader: a shipped world may reference the family
    # definitions beside it (2026-09-20).
    world = load_world(path.read_bytes(), base_dir=path.parent).world
    assert document["law"] == "beam" and world.model_id.startswith("rays-")


def test_every_gate_set_world_exists_and_parses_as_a_nature_beam_world():
    """(d): the gate set."""
    gate = ROOT / "examples" / "events" / "gate_set.json"
    document = json.loads(gate.read_text(encoding="utf-8"))
    assert document["format"] == "gate-set-v1" and document["worlds"]
    names = []
    for entry in document["worlds"]:
        assert set(entry) - {"digests", "refusal"} == {"path", "ticks", "cap", "covers"}, entry
        if "refusal" in entry:
            # A world the law as it stands refuses before its cap (the
            # generic entry of the bending, 2026-09-22): the interval and
            # the refusal's line, its digests before the entry kept.
            assert set(entry["refusal"]) == {"since", "interval", "match", "note"}, entry["path"]
            assert 0 < int(entry["refusal"]["interval"]) <= int(entry["cap"]), entry["path"]
        path = gate.parent / entry["path"]
        assert path.is_file(), entry["path"]
        source = json.loads(path.read_text(encoding="utf-8"))
        loaded = load_world(path.read_bytes(), base_dir=path.parent)
        # The digests at the cap (the register `test_amplitude_click` (d)
        # reads, 2026-09-21) on every world without a lamp and on no other.
        lamp_free = all(event.lamp is None for event in loaded.world.measured)
        assert ("digests" in entry) == lamp_free, entry["path"]
        if lamp_free:
            digests = entry["digests"]
            assert set(digests) == {"state_sha256", "audit_sha256", "events_sha256"}, entry["path"]
            assert all(len(d) == 64 and int(d, 16) >= 0 for d in digests.values()), entry["path"]
        assert source["law"] == "beam" and loaded.world.model_id == source["model_id"]
        assert entry["ticks"] == source["ticks"], entry["path"]
        assert 1 <= entry["cap"] <= entry["ticks"], entry["path"]
        assert isinstance(entry["covers"], str) and entry["covers"].strip()
        names.append(path.stem)
    assert len(set(names)) == len(names), "two gate worlds of one name"


def test_two_contents_is_not_refused_and_its_face_records_are_exact():
    """(e)."""
    path = ROOT / "examples" / "events" / "two_contents.json"
    document = json.loads(load_world(path.read_bytes(), base_dir=path.parent).expanded_source)
    # The numbers are the register's (`examples/events/expectations.json`,
    # since 2026-09-21: a test reads a world's numbers from the register).
    registered = json.loads((path.parent / "expectations.json").read_text(encoding="utf-8"))
    assert registered["format"] == "root-worlds-expectations-v1"
    expected = registered["two_contents"]
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(document), records.append)
    cosines, sines = phase_cosines(document["N"]), phase_sines(document["N"])
    before: dict[str, int] = {}
    faces: dict[str, int] = {}
    clicked: dict[str, list[tuple[int, int]]] = {}
    for tick in range(1, int(expected["ticks"]) + 1):
        simulation.step()
        assert simulation.books()["balanced"], tick
        faces = {str(d["name"]): int(d["families"]["m"]["record"]) for d in simulation.face_detectors()}
        clicked = {}
        for line in records:
            if line["event"] == "click" and line["tick"] == tick:
                clicked.setdefault(str(line["detector"]), []).append(
                    (int(line["amount"]), int(line["phase"]))
                )
        for name, record in faces.items():
            rows = clicked.get(name, [])
            x = sum(32 * amount * cosines[phase] for amount, phase in rows)
            y = sum(32 * amount * sines[phase] for amount, phase in rows)
            assert record - before.get(name, 0) == x * x + y * y, (tick, name)
        before = faces
    assert clicked["face:+y"] == [tuple(pair) for pair in expected["face_plus_y"]["clicks_at_last_tick"]]
    assert faces["face:+y"] == expected["face_plus_y"]["record"] == MOMENTUM_BOUND + 1
    assert faces["face:+x"] == expected["face_plus_x"]["record"]
    assert faces["face:-x"] == expected["face_minus_x"]["record"] > MOMENTUM_BOUND
    report = {d["name"]: d for d in json.loads(json.dumps(simulation.detectors()))}
    assert report["face:+x"]["families"]["m"]["record"] == expected["face_plus_x"]["record"]
    first, second = simulation.measured[1], simulation.measured[2]
    assert first.pushed[0] > 0 and first.pushed == [-second.pushed[0], 0, 0]
    assert second.pushed[1:] == [0, 0] and first.momentum == first.pushed


def test_the_root_worlds_are_the_generators():
    """The four world files at the root of `examples/events/` equal the
    documents of `make_worlds.py` beside them (2026-09-20)."""
    generator = load_script("root_make_worlds", ROOT / "examples" / "events" / "make_worlds.py")
    documents = generator.worlds()
    assert set(documents) == {"one_content", "two_contents", "one_slit", "two_slits"}
    for name, document in documents.items():
        shipped = (ROOT / "examples" / "events" / f"{name}.json").read_bytes()
        assert shipped == (json.dumps(document) + "\n").encode("utf-8"), name
