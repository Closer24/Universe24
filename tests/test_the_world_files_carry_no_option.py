"""The world files carry no option (the owner's word of 2026-10-23: "In the world file, is it not better to run the same as the Node? Nature is one, not several options"): the one world's file declares no `boundary`, the torus being the board, and loads as the torus with its mode file's digest; a side's setting is one key, `basis`, the former second key `axis` refused by name with the sentence naming `basis`, and the singlet's shipped worlds load with their half-angle pairs under it."""

import json

from event_universe.loader.world import node_detectors_of
from event_universe.world_files import input_digest
from tests.laws import EVENTS, refused
from tests.laws_read import load_shipped

ONE_WORLD = EVENTS / "universe24" / "universe24.json"
SINGLET = EVENTS / "bell_singlet" / "singlet_a_b.json"


def test_the_one_world_declares_no_boundary_and_a_side_declares_one_setting_key():
    # (1) the one world: no `boundary` in its file, the torus at load, the mode file standing by its digest
    document = json.loads(ONE_WORLD.read_text(encoding="utf-8"))
    assert "boundary" not in document and list(document) == [
        "shape",
        "intervals",
        "universe",
        "bodies",
        "node_detectors",
    ]
    mode = json.loads(ONE_WORLD.with_suffix(".mode.json").read_text(encoding="utf-8"))
    assert mode["world_digest"] == input_digest(document)
    torus = load_shipped(ONE_WORLD)
    assert torus.periodic == (True, True, True) and torus.open_axes == (False, False, False)
    assert torus.face_depth == 0 and torus.receding == () and torus.beyond == ()
    # (2) the singlet's sides: the half-angle pairs under `basis`, the kind read from the two-plane record
    sides = load_shipped(SINGLET).node_detectors
    assert [(s.name, s.basis, s.axis, s.plane) for s in sides if s.declared] == [
        ("left", (1, 0), (1, 0), True),
        ("right", (12, 5), (12, 5), True),
    ]
    # (3) the key `axis` refused by name with the sentence naming `basis`, on the shipped row re-keyed
    row = json.loads(SINGLET.read_text(encoding="utf-8"))["node_detectors"][0]
    wrong = {**{key: value for key, value in row.items() if key != "basis"}, "axis": row["basis"]}
    found = refused(
        "node_detectors\\[0\\] holds the key 'axis'", node_detectors_of, [wrong], (33, 1, 1), 0, (), ()
    )
    sentence = str(found)
    assert "a side's setting is one key, `basis`" in sentence
    assert "nature is one, not several options" in sentence
    assert "write the pair under `basis`" in sentence
