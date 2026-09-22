"""atom-level-v1, the release at a closure of the difference of two closures
(2026-09-22, the world key `atom_level`, absent by default; the body's
`level` declaration; docs/designs/atom_levels/LEVELS.md section 2 (b), the
virial form on the physics-rule reviewer's recommendation; the model
owner's word of record 973 of the log of 2026-09-20 through the Boss).
Under the key a body that declares `level` carries the action gained on
each axis since its last return, the count of its self-creations since it
and the level at its last release; at a return (the momentum's component on
the declared axis crossing zero in the declared sense) its level is
`floor(n_l x (the action gained) / (2 h d_l x (the count)))`, the first
return sets the last level and releases nothing, and a later return
releases the rise of the level as one row per declared direction of the
declared paid family, content h_q x (the rise), the row's phase turning that
many steps per interval of its age. The expected integers of
docs/TEST_EXPECTATIONS.md ("The atom's levels"), written down before the
first run:

(a) the key absent computes nothing: every registered world outside the
    three `atoms/hydrogen_r*_level.json` parses with `atom_level` false and
    the identity absent from its hypotheses; the gate world
    `detector/grouped_12_nodes` replays to the digests of `gate_set.json`
    byte for byte, its `run.json` without an `atom_level` key; the new
    store column `turn` is 0 on every row of a world without the key;
(b) the level on declared integers: with the action gained `j N h` over a
    count T the level is `floor(n_l N j / (2 d_l T))` (the rung-4 numbers
    of the generator, j = 4, T = 1490, [512, 1]: 43; j = 2, T = 212: 154;
    the ladder's `j / (2 T)` in phase steps of h d_l / (N n_l)), the
    remainder discarded as the band, and a body on the same closed loop
    (the same gain and count at every return) releases nothing;
(c) the return on the engine: the r = 3 level world run to its first
    return reads one `level` line with `last` null and `released` 0, its
    `level` the whole part of `512 x action / (2 h x count)` of the line's
    own `action` and `count`, no `light` row born, the electron's content
    1836 and the books balanced at every tick;
(d) the release on the engine: a rise of s released from the electron at
    its start births four rows of `light` of content s (one per in-plane
    heading), with the row's own rate s, the electron's content less by
    4 s and its momentum unchanged (the four labels cancel), the books
    balanced; three rows click on the +x, +y and -y faces of the r = 3
    world with content s within 40 intervals at the rows' pace and the -x
    row is taken at the proton's Node, and the phase difference between
    the +x face's click and the +y face's click of that release equals
    `s x (age_y - age_x) mod N` (the Planck identity `E = h_q s = h_q N f`
    read after a detector, LEVELS.md section 5 (d), R5);
(e) the refusals: `level` without the world key; `atom_level` of a type
    other than a boolean; a free family; a family without a phase circle;
    a fixed body; a body without `phase_by_momentum`; a pair or a return
    outside its range; and the three level worlds parse with the key, their
    hypotheses `bohr-v1`, `centred-step-v1`, `atom-level-v1`, the r = 12
    world the registered centred world plus the key, the declaration, the
    photon's family and its own model id, integer for integer.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import ATOM_LEVEL_RULE, BOHR_RULE, CENTRED_STEP_RULE
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "events"
ATOMS = EXAMPLES / "atoms"
GATE_SET = EXAMPLES / "gate_set.json"
LEVEL_WORLDS = ("hydrogen_r3_level.json", "hydrogen_r7_level.json", "hydrogen_r12_level.json")
N = 64
H = 5536242544  # the atoms series' action, h = 16 p_B(8)


def digests(folder: Path) -> dict[str, str]:
    """The gate set's three digests of a run folder (`test_centred_step.py`'s form)."""
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    return {
        "state_sha256": hashlib.sha256((folder / "state.json").read_bytes()).hexdigest(),
        "audit_sha256": hashlib.sha256(json.dumps(record.get("audit", [])).encode("utf-8")).hexdigest(),
        "events_sha256": hashlib.sha256((folder / "events.jsonl").read_bytes()).hexdigest(),
    }


def level_of(n_l: int, d_l: int, gained: int, count: int, action: int = H) -> int:
    """The level as the engine forms it (LEVELS.md section 2 (b))."""
    return (n_l * gained) // (2 * action * d_l * count)


def level_world(name: str = "hydrogen_r3_level.json") -> dict[str, object]:
    document = json.loads((ATOMS / name).read_text(encoding="utf-8"))
    assert isinstance(document, dict)
    return document


def loaded(name: str = "hydrogen_r3_level.json"):
    path = ATOMS / name
    return load_world(path.read_bytes(), base_dir=path.parent, root=EXAMPLES)


def expanded(name: str = "hydrogen_r3_level.json") -> dict[str, object]:
    """The shipped world as the loader expands it, its families inline (the
    definitions it references placed), for the parser's refusals."""
    document = json.loads(loaded(name).expanded_source)
    assert isinstance(document, dict)
    return document


def parse(document: dict[str, object]):
    return parse_nature_beam_world(document)


def the_electron(simulation: NatureBeamSimulation):
    return next(entry for entry in simulation.measured.values() if entry.level is not None)


# -- (a) ---------------------------------------------------------------------------


def test_the_key_absent_computes_nothing_and_the_gate_world_replays_byte_identical(tmp_path):
    """(a)."""
    checked = 0
    for path in sorted(EXAMPLES.rglob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(document, dict) or "format" in document or path.name in LEVEL_WORLDS:
            continue
        world = load_world(path.read_bytes(), base_dir=path.parent, root=EXAMPLES).world
        assert world.atom_level is False, path
        assert ATOM_LEVEL_RULE not in world.hypotheses, path
        assert all(entry.level is None for entry in world.measured), path
        checked += 1
    assert checked >= 100
    gate = json.loads(GATE_SET.read_text(encoding="utf-8"))
    entry = next(w for w in gate["worlds"] if w["path"] == "detector/grouped_12_nodes.json")
    path = EXAMPLES / entry["path"]
    source = path.read_bytes()
    world = load_world(source, base_dir=path.parent, root=EXAMPLES)
    out = tmp_path / "gate"
    out.mkdir()
    execute_nature_beam_run(world.world, source, out, "test", entry["cap"])
    assert digests(out) == entry["digests"]
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert "atom_level" not in record
    assert ATOM_LEVEL_RULE not in record["hypotheses"]
    simulation = NatureBeamSimulation(world.world)
    for _ in range(entry["cap"]):
        simulation.step()
    assert all(not store.turn.any() for store in simulation.stores)


# -- (b) ---------------------------------------------------------------------------


def test_the_level_on_declared_integers():
    """(b)."""
    assert level_of(512, 1, 4 * N * H, 1490) == 43
    assert level_of(512, 1, 2 * N * H, 212) == 154
    assert level_of(1, 1, 4 * N * H, 1490) == 0  # the dictionary's grain: below one step
    assert level_of(512, 1, 4 * N * H, 1490) == (512 * N * 4) // (2 * 1490)
    # A closed loop: the same gain and count at every return, the level the
    # same, the rise 0 (the rule of section 2 (b): s = L - L_rel when positive).
    last = None
    released = []
    for _ in range(5):
        level = level_of(512, 1, 4 * N * H, 1490)
        released.append(0 if last is None or level <= last else level - last)
        last = level if last is None or level > last else last
    assert released == [0, 0, 0, 0, 0]
    # A tightening: the levels 47, 44, 53, 55 of RUN_CENTRED's loops after a
    # first loop at 50 release 0, 0, 3, 2 (LEVELS.md section 5 (d), R5).
    last = 50
    found = []
    for level in (47, 44, 53, 55):
        rise = level - last if level > last else 0
        found.append(rise)
        if rise:
            last = level
    assert found == [0, 0, 3, 2]


# -- (c) ---------------------------------------------------------------------------


def test_the_first_return_on_the_engine_sets_the_level_and_releases_nothing():
    """(c)."""
    world = loaded().world
    events: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(world, observer=events.append)
    for _ in range(300):
        simulation.step()
        assert simulation.books()["balanced"]
    levels = [e for e in events if e["event"] == "level"]
    assert len(levels) == 1
    (line,) = levels
    assert line["last"] is None and line["released"] == 0
    assert line["level"] == level_of(512, 1, int(line["action"]), int(line["count"]))
    assert int(line["count"]) == int(line["tick"])  # every interval a self-creation, no crowd
    assert line["content"] == 1836
    assert not [e for e in events if e["event"] == "click" and e.get("family") == "light"]
    electron = the_electron(simulation)
    assert electron.level_last == line["level"]
    assert electron.level_count == simulation.tick - int(line["tick"])
    assert electron.held[electron.family] == 1836


# -- (d) ---------------------------------------------------------------------------


def test_the_release_births_the_rows_with_their_rate_and_the_faces_read_the_planck_identity():
    """(d)."""
    world = loaded().world
    events: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(world, observer=events.append)
    electron = the_electron(simulation)
    light = next(index for index, family in enumerate(world.families) if family.name == "light")
    rise = 3
    momentum_before = list(electron.momentum)
    simulation._level_release(electron, light, rise)
    store = simulation.stores[light]
    assert store.size == 4
    assert store.content.tolist() == [rise] * 4 and store.amount.tolist() == [1] * 4
    assert store.turn.tolist() == [rise] * 4 and store.age.tolist() == [0] * 4
    assert electron.held[electron.family] == 1836 - 4 * rise
    assert electron.momentum == momentum_before
    assert simulation.ledger.held_spent[electron.family] == 4 * rise
    assert simulation.ledger.content_released[light] == 4 * rise
    assert simulation.ledger.transit_released[light] == 4
    for _ in range(40):
        simulation.step()
        assert simulation.books()["balanced"]
    clicks = [e for e in events if e["event"] == "click" and e.get("family") == "light"]
    # The rows fly at the rows' pace (64 / 110 Links per interval on a
    # heading): the +x, +y and -y rows reach the faces (14 and 17 Links)
    # within 40 intervals; the -x row is measured at the proton's Node, 3
    # Links away (`at_proton`, a paid row taken).
    assert sorted(str(e["detector"]) for e in clicks) == ["at_proton", "face:+x", "face:+y", "face:-y"]
    assert all(e["content"] == rise for e in clicks)
    by_face = {str(e["detector"]): e for e in clicks}
    age = {
        face: int(by_face[face]["tick"]) for face in ("face:+x", "face:+y")
    }  # born at tick 0, one Link per interval
    phase_x, phase_y = int(by_face["face:+x"]["phase"]), int(by_face["face:+y"]["phase"])
    assert (phase_y - phase_x) % N == (rise * (age["face:+y"] - age["face:+x"])) % N
    assert age["face:+y"] > age["face:+x"]
    # A release that would take the body's whole content is refused loudly.
    with pytest.raises(ValueError, match="whole content"):
        simulation._level_release(electron, light, 1836 // 4)


# -- (e) ---------------------------------------------------------------------------


def test_the_refusals_and_the_three_worlds():
    """(e)."""
    base = expanded()
    without = copy.deepcopy(base)
    del without["atom_level"]
    with pytest.raises(ValueError, match="without the world key atom_level"):
        parse(without)
    typed = copy.deepcopy(base)
    typed["atom_level"] = 1
    with pytest.raises(ValueError, match="atom_level must be true or false"):
        parse(typed)

    def declaring(**changes: object) -> dict[str, object]:
        document = copy.deepcopy(base)
        electron = document["measured"][1]  # type: ignore[index]
        level = dict(electron["level"])
        level.update(changes)
        electron["level"] = level
        return document

    with pytest.raises(ValueError, match="free family"):
        parse(declaring(family="e"))
    unphased = copy.deepcopy(base)
    unphased["families"][2]["phase"] = False  # type: ignore[index]
    with pytest.raises(ValueError, match="without a phase circle"):
        parse(unphased)
    for pair in ([0, 1], [512], [512, 0], "512"):
        with pytest.raises(ValueError, match="pair"):
            parse(declaring(pair=pair))
    for turn in ([3, -1], [0, 0], [0, 2], [0]):
        with pytest.raises(ValueError, match="return"):
            parse(declaring(**{"return": turn}))
    fixed = copy.deepcopy(base)
    fixed["measured"][1]["fixed"] = True  # type: ignore[index]
    with pytest.raises(ValueError):
        parse(fixed)
    still = copy.deepcopy(base)
    still["measured"][1]["phase_by_momentum"] = False  # type: ignore[index]
    with pytest.raises(ValueError, match="phase_by_momentum"):
        parse(still)
    for name, radius in zip(LEVEL_WORLDS, (3, 7, 12), strict=True):
        world = loaded(name).world
        assert world.atom_level and world.centred_step
        assert world.hypotheses == [BOHR_RULE, CENTRED_STEP_RULE, ATOM_LEVEL_RULE]
        assert world.action == H
        electron = world.measured[1]
        assert electron.level is not None
        assert electron.level.pair == (512, 1) and (electron.level.axis, electron.level.sign) == (0, -1)
        assert world.families[electron.level.family].name == "light"
        side = world.shape[0]
        assert electron.position == (side // 2 + radius, side // 2, side // 2)
        assert electron.phase_by_momentum and not electron.fixed
    centred = json.loads((ATOMS / "hydrogen_r12_centred.json").read_text(encoding="utf-8"))
    level12 = level_world("hydrogen_r12_level.json")
    assert level12["model_id"] == "rays-atoms-hydrogen-r12-level-v1"
    assert level12["atom_level"] is True
    for key in centred:
        if key in ("model_id", "measured", "entities"):
            continue
        assert level12[key] == centred[key], key
    assert level12["measured"][0] == centred["measured"][0]  # type: ignore[index]
    electron_level = dict(level12["measured"][1])  # type: ignore[index, arg-type]
    assert electron_level.pop("level") == {"family": "light", "pair": [512, 1], "return": [0, -1]}
    assert electron_level == centred["measured"][1]  # type: ignore[index]
    assert [e["definition"] for e in level12["entities"]] == ["proton", "electron", "photon"]  # type: ignore[index]
    assert np.int64(H) * 2 * 7500 < 2**62
