"""centred-step-v1, the body's step at half the wall (2026-09-22, the world
key `centred_step`, absent by default; docs/designs/atom_give/CENTRED_STEP.md;
the cause it answers docs/designs/atom_give/CAUSE.md section 2 (v); the
model owner's word through the Boss, record 953 of the log of 2026-09-20).
Under the key the count of a body's step is the NEAREST whole number of its
accumulator in units of the wall, `(abs(drive) + wall // 2) // wall` with
the sign, the whole wall subtracted, on both drives (`core.integer.by_drive`
and `by_line`, `centred`); every other count keeps the whole part. The
expected integers of docs/TEST_EXPECTATIONS.md ("The centred step"), written
down before the first run:

(a) the key absent computes nothing: every registered world outside
    `atoms/hydrogen_r12_centred.json` and the three level worlds
    `atoms/hydrogen_r*_level.json` (atom-level-v1, which declare the
    centred step too) parses with `centred_step` false and
    the identity absent from its hypotheses; the gate world
    `detector/grouped_12_nodes` replays to the digests of `gate_set.json`
    byte for byte, its `run.json` without a `centred_step` key; `by_drive`
    and `by_line` without the flag are the primitives as they were (the
    first fire of a constant rate 6000 against 10096 at n = 2, the 21st at
    n = 36);
(b) `by_drive` centred on declared integers: from an empty accumulator at
    a constant rate 6000 against the denominator 10096 (Q x 64 + 6000, the
    wall of a body of content 64 at width 1) the total count after n
    self-creations is `(6000 n + 5048) // 10096` (the first fire at n = 1,
    the 21st at n = 35) and the accumulator after n is `6000 n - total x
    10096`, in [-5048, 5048); a rate 25000 above the denominator with the
    cap 1 fires one count per self-creation and carries the rest; a
    reversal at n = 10 (6000 for 10, then -6000) fires -1 where the
    accumulated motion first passes -5048 on the other side (the count's
    sign the accumulator's), and the accumulator after 20 is 0;
(c) `by_line` centred on one axis gives the same integers as `by_drive`
    centred against the same wall (the rate 384000 against W = 922144 over
    60 self-creations), the furthest-over axis stepping at half the wall
    and the whole wall subtracted, an idle axis at rate 0 never stepping;
(d) the deciding world on the engine (the box world of `test_drive_b.py`
    without `drive_b`: a body of content 64 at (20, 20, 20) of an open 41^3
    box, p = (6000, 0, 0), width 1): under the key the steps fall at the
    self-creations where `(6000 n + 5048) // 10096` rises (the first at
    tick 1) and the click on face:+x at tick 35 (the 21st fire), against
    tick 36 without the key; `run.json` carries `centred_step: true` and
    the hypotheses `centred-step-v1`; under `drive_b` and the key together
    the steps are the host's replay of `by_line(..., centred=True)`
    integer for integer over 60 intervals, the click at the 21st fire;
(e) the refusals: `centred_step` of a type other than a boolean; and the
    atoms world `hydrogen_r12_centred.json` parses with the key, its
    hypotheses `bohr-v1` then `centred-step-v1`, its electron and proton
    the registered world's integer for integer.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from event_universe.core.integer import by_drive, by_line
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import BOHR_RULE, CENTRED_STEP_RULE, DRIVE_B_RULE, LABEL_SCALE
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "events"
ATOMS = EXAMPLES / "atoms"
GATE_SET = EXAMPLES / "gate_set.json"
Q = LABEL_SCALE
RATE, DENOMINATOR = 6000, Q * 64 + 6000  # 10096: the wall of a body of content 64 at width 1


def box_world(
    momentum: list[int], *, key: bool, drive_b: bool = False, ticks: int = 200
) -> dict[str, object]:
    """`test_drive_b.py`'s deciding world: one free body of no release at the
    centre of an open 41^3 cube, the faces the detectors."""
    document: dict[str, object] = {
        "law": "beam",
        "model_id": "centred-step-box",
        "shape": [41, 41, 41],
        "boundary": "open",
        "ticks": ticks,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1 << 20],
        "suspension": 0,
        "width": 1,
        "families": [{"name": "probe", "quantum": 0, "charge": 0, "phase": False}],
        "measured": [
            {"position": [20, 20, 20], "family": "probe", "amount": 64, "momentum": list(momentum)}
        ],
    }
    if key:
        document["centred_step"] = True
    if drive_b:
        document["drive_b"] = True
    return document


def run_in_process(document: dict[str, object], ticks: int):
    events: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(document), observer=events.append)
    for _ in range(ticks):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    return events, simulation


def digests(folder: Path) -> dict[str, str]:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    return {
        "state_sha256": hashlib.sha256((folder / "state.json").read_bytes()).hexdigest(),
        "audit_sha256": hashlib.sha256(json.dumps(record.get("audit", [])).encode("utf-8")).hexdigest(),
        "events_sha256": hashlib.sha256((folder / "events.jsonl").read_bytes()).hexdigest(),
    }


def expected_fires(n_max: int) -> list[int]:
    """The self-creations at which the centred total `(6000 n + 5048) // 10096` rises."""
    found, last = [], 0
    for n in range(1, n_max + 1):
        total = (RATE * n + DENOMINATOR // 2) // DENOMINATOR
        if total > last:
            found.append(n)
            last = total
    return found


# -- (a) ---------------------------------------------------------------------------


def test_the_key_absent_computes_nothing_and_the_gate_world_replays_byte_identical(tmp_path):
    """(a)."""
    checked = 0
    for path in sorted(EXAMPLES.rglob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        if (
            not isinstance(document, dict)
            or "format" in document
            or path.name == "hydrogen_r12_centred.json"
            or path.name.endswith("_level.json")
        ):
            continue
        world = load_world(path.read_bytes(), base_dir=path.parent, root=EXAMPLES).world
        assert world.centred_step is False, path
        assert CENTRED_STEP_RULE not in world.hypotheses, path
        checked += 1
    assert checked >= 100
    gate = json.loads(GATE_SET.read_text(encoding="utf-8"))
    entry = next(w for w in gate["worlds"] if w["path"] == "detector/grouped_12_nodes.json")
    path = EXAMPLES / entry["path"]
    source = path.read_bytes()
    loaded = load_world(source, base_dir=path.parent, root=EXAMPLES)
    out = tmp_path / "gate"
    out.mkdir()
    execute_nature_beam_run(loaded.world, source, out, "test", entry["cap"])
    assert digests(out) == entry["digests"]
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert "centred_step" not in record
    assert CENTRED_STEP_RULE not in record["hypotheses"]
    # The primitives without the flag are what they were: the whole part.
    drive, fires = 0, []
    for n in range(1, 37):
        count, drive = by_drive(drive, RATE, DENOMINATOR, at_most=1)
        if count:
            fires.append(n)
    assert fires[0] == 2 and fires[20] == 36 and len(fires) == 21
    assert by_line([0], [RATE], DENOMINATOR) == (None, 0, [RATE])


# -- (b) ---------------------------------------------------------------------------


def test_by_drive_centred_counts_the_nearest_whole_number():
    """(b)."""
    drive, total = 0, 0
    fires = []
    for n in range(1, 201):
        count, drive = by_drive(drive, RATE, DENOMINATOR, at_most=1, centred=True)
        total += count
        assert count in (0, 1)
        assert total == (RATE * n + DENOMINATOR // 2) // DENOMINATOR, n
        assert drive == RATE * n - total * DENOMINATOR, n
        assert -(DENOMINATOR - DENOMINATOR // 2) <= drive < DENOMINATOR // 2, n
        if count:
            fires.append(n)
    assert fires[:3] == [1, 3, 5] and fires[20] == 35
    assert fires == expected_fires(200)
    # A rate above the denominator with the cap: one count per self-creation, the rest carried.
    drive = 0
    for n in range(1, 6):
        count, drive = by_drive(drive, 25000, DENOMINATOR, at_most=1, centred=True)
        assert count == 1
        assert drive == 25000 * n - n * DENOMINATOR
    count, drive = by_drive(0, 25000, DENOMINATOR, centred=True)
    assert count == (25000 + DENOMINATOR // 2) // DENOMINATOR == 2 and drive == 25000 - 2 * DENOMINATOR
    # The reversal: 6000 for ten self-creations, then -6000; the count reverses where the
    # accumulated motion first passes the half line on the other side.
    drive, total, reversed_at = 0, 0, None
    for n in range(1, 21):
        rate = RATE if n <= 10 else -RATE
        count, drive = by_drive(drive, rate, DENOMINATOR, at_most=1, centred=True)
        total += count
        motion = RATE * min(n, 10) - RATE * max(n - 10, 0)
        assert total == (abs(motion) + DENOMINATOR // 2) // DENOMINATOR * (1 if motion >= 0 else -1), n
        if count < 0 and reversed_at is None:
            reversed_at = n
    assert reversed_at is not None and total == 0 and drive == 0


# -- (c) ---------------------------------------------------------------------------


def test_by_line_centred_on_one_axis_is_by_drive_centred():
    """(c)."""
    wall, rate = 922144, 6000 * Q
    drives, drive = [0, 0, 0], 0
    for n in range(1, 61):
        axis, sign, drives = by_line(drives, [rate, 0, 0], wall, centred=True)
        count, drive = by_drive(drive, rate, wall, at_most=1, centred=True)
        assert (axis, sign) == ((0, 1) if count else (None, 0)), n
        assert drives == [drive, 0, 0], n
        assert -(wall - wall // 2) <= drives[0] < wall // 2, n
    # The threshold is half the wall: an accumulator at wall // 2 carries, one below does not.
    assert by_line([wall // 2 - 1 - 10, 0, 0], [10, 0, 0], wall, centred=True)[0] is None
    assert by_line([wall // 2 - 10, 0, 0], [10, 0, 0], wall, centred=True)[:2] == (0, 1)
    assert by_line([wall // 2 - 10, 0, 0], [10, 0, 0], wall)[0] is None


# -- (d) ---------------------------------------------------------------------------


def test_the_deciding_world_steps_at_the_nearest_whole_number_and_clicks_a_tick_earlier():
    """(d)."""
    events, simulation = run_in_process(box_world([6000, 0, 0], key=True, ticks=40), 40)
    assert simulation.world.centred_step is True
    assert CENTRED_STEP_RULE in simulation.hypotheses
    ticks = [e["tick"] for e in events if e["event"] == "step"]
    fires = expected_fires(40)
    assert ticks == fires[:20] and ticks[0] == 1
    clicks = [e for e in events if e["event"] == "click"]
    assert clicks and clicks[0]["tick"] == fires[20] == 35
    control, _ = run_in_process(box_world([6000, 0, 0], key=False, ticks=40), 40)
    assert [e for e in control if e["event"] == "click"][0]["tick"] == 36
    # Under `drive_b` and the key together: the host's replay of `by_line` centred.
    events, simulation = run_in_process(box_world([6000, 0, 0], key=True, drive_b=True, ticks=60), 60)
    assert DRIVE_B_RULE in simulation.hypotheses and CENTRED_STEP_RULE in simulation.hypotheses
    wall = Q * Q * 64 + 6000 * 110
    drives, expected = [0, 0, 0], []
    for n in range(1, 61):
        axis, _sign, drives = by_line(drives, [6000 * Q, 0, 0], wall, centred=True)
        if axis is not None:
            expected.append(n)
    ticks = [e["tick"] for e in events if e["event"] == "step"]
    assert ticks == expected[:20]
    assert [e for e in events if e["event"] == "click"][0]["tick"] == expected[20]


def test_the_record_carries_the_key_only_under_it(tmp_path):
    """(d), the record."""
    document = box_world([6000, 0, 0], key=True, ticks=40)
    source = json.dumps(document).encode("utf-8")
    loaded = load_world(source, base_dir=tmp_path, root=tmp_path)
    out = tmp_path / "run"
    out.mkdir()
    execute_nature_beam_run(loaded.world, source, out, "test", 40)
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert record["centred_step"] is True
    assert CENTRED_STEP_RULE in record["hypotheses"]


# -- (e) ---------------------------------------------------------------------------


def test_the_refusal_and_the_atoms_world():
    """(e)."""
    document = box_world([6000, 0, 0], key=True)
    document["centred_step"] = 1
    with pytest.raises(ValueError, match="centred_step must be true or false"):
        parse_nature_beam_world(document)
    path = ATOMS / "hydrogen_r12_centred.json"
    world = load_world(path.read_bytes(), base_dir=path.parent, root=EXAMPLES).world
    assert world.centred_step is True
    assert world.hypotheses[:2] == [BOHR_RULE, CENTRED_STEP_RULE]
    registered = json.loads((ATOMS / "hydrogen_r12.json").read_text(encoding="utf-8"))
    declared = json.loads(path.read_text(encoding="utf-8"))
    assert declared.pop("centred_step") is True
    assert declared.pop("model_id") == "rays-atoms-hydrogen-r12-centred-step-v1"
    registered.pop("model_id")
    assert declared == registered
