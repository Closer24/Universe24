"""The window is derived and never declared (the owner's decision of 2026-10-23: "derive and replace the declared ones; the window shall not be declared"; ALGEBRA.md, The click writes on the lattice, C2 and (5), the regions' one window; src/event_universe/loader/window.py, loader/draw.py): (1) the loader refuses the key `window` by name on a body's node_detector and on the world's draw at the end of the load, the derived number and its cause named (the parse carries the key for that refusal alone); (2) a body whose drive has no end has its own beat for its window, one period of its transition's resonance pair in whole intervals by Chebyshev's recurrence (`period_of`), 15 on Universe24's instrument at [902, 1000], and the clicks world's absorber, whose drive is a laid packet with an end, keeps the passage rule's 32 beside its beat's 15; (3) the world's draw window is the longest passage of every lay with an end over the declared regions, 149 on the clicks chain (the electron over the target) and 30 on the Bell chain; (4) the two rules meet on one body: the clicks absorber on its closed chain reads the passage, and on the chain made a ring, where the packets fill no end, its beat; (5) a small world with the instrument body clicks at the derived cadence, the credits at the windows' closes."""

import json
from pathlib import Path

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.loader import window
from event_universe.loader.draw import body_draw_of, draw_of
from event_universe.loader.world import World, parse_world
from tests.laws import EVENTS, refused
from tests.laws_read import load_shipped, redeclared

CLICKS, BELL = EVENTS / "clicks" / "clicks_chain.json", EVENTS / "bell" / "bell_a_b.json"
UNIVERSE = EVENTS / "universe24" / "universe24.json"


def parsed(path: Path, edit=None) -> World:  # type: ignore[no-untyped-def]
    """The shipped world at `path` parsed from its document with `edit` applied, the mode file beside it read; no interval stepped."""
    document = json.loads(path.read_text(encoding="utf-8"))
    files, digest = world_files.world_files(document), world_files.input_digest(document)
    redeclared(document)
    beside = path.with_suffix(".mode.json")
    if beside.is_file():
        files[beside.name] = json.loads(beside.read_text(encoding="utf-8"))
    if edit is not None:
        edit(document)
    return parse_world(document, files, digest)


def test_a_declared_window_is_refused_by_name_on_a_body_and_on_the_world():
    """(1) The key `window` refused by name with the rule that derives it: on a body's node_detector (the body's own beat or the lays' passage) and on the world's draw (the region's passage), at the parse of the key and at the parse of the shipped worlds given the key again."""
    assert body_draw_of({"window": 12}, "b").window == draw_of({"window": 12}, "draw", True).window == 12
    assert draw_of({}, "draw", True).window is None and body_draw_of({}, "b").window is None

    def body(document):  # type: ignore[no-untyped-def]
        document["bodies"][0]["node_detector"]["window"] = 12

    def world(document):  # type: ignore[no-untyped-def]
        document["draw"]["window"] = 12

    assert "W = 32" in str(refused("declares the window 12", parsed, CLICKS, body))
    assert "W = 149" in str(refused("declares the window 12", parsed, CLICKS, world))
    assert "own beat" in str(
        refused(
            "declares the window 12",
            parsed,
            UNIVERSE,
            lambda d: d["bodies"][4]["node_detector"].update(window=12),
        )
    )


def test_the_body_window_is_its_own_beat_where_the_drive_has_no_end():
    """(2) Universe24's instrument body at the resonance [902, 1000] in the standing uniform light of a board periodic on three axes, no passage end: its window the beat's period, 15 intervals, `period_of` (the first count n with sin(n Omega) back at or above 0 after a negative turn, 2 pi / Omega = 14.08); the clicks world's absorber at [5414, 6000] has the same beat, 15, and its drive, a laid packet with an end, gives the passage rule's 32."""
    assert window.period_of((902, 1000)) == window.period_of((5414, 6000)) == 15
    universe = parsed(UNIVERSE)
    instrument = next(b for b in universe.bodies if b.detector is not None)
    assert universe.draw is None and instrument.detector.draw.window == 15
    assert instrument.detector.transitions[0].resonance == (902, 1000)
    clicks = parsed(CLICKS)
    absorber = clicks.bodies[0]
    assert absorber.detector.transitions[0].resonance == (5414, 6000)
    assert absorber.detector.draw.window == 32


def test_the_regions_window_is_the_longest_passage_over_the_declared_regions():
    """(3) The world's draw window: on the clicks chain the electron packet's passage over the target of 21 Nodes, 149 (the photon 68, the neutron 122; the screen's 54, 92, 102 shorter), the former declared 12; on the Bell chain the pair's packets of 1 + 12 Nodes at k = pi / 4 over a side of 4 Nodes, 30, the former declared 100; each the longest of `packet_passage` over the declared regions."""
    for path, expected in ((CLICKS, 149), (BELL, 30)):
        world = parsed(path)
        passages = [
            window.packet_passage(
                p, world.families, tuple(dict.fromkeys(r.positions)), world.shape, world.periodic
            )
            for r in world.node_detectors
            if r.declared and r.positions
            for p in world.packets
        ]
        assert world.draw is not None and world.draw.window == max(passages) == expected  # type: ignore[arg-type]


def test_the_two_rules_meet_on_one_body():
    """(4) The clicks world's absorber: on its closed chain every photon packet has an end and the window is their passage over the body, 32 = ceil((17 + 1 - 1) / v_g) at k = pi / 4, above its beat; with the chain made a ring and one photon packet laid over the whole ring, a drive with no end, the same body's window is its own beat, 15, the passage rule standing wherever a passage can be read."""
    chain = parsed(CLICKS)
    assert chain.bodies[0].detector.draw.window == 32 > window.period_of((5414, 6000))

    def ring(document):  # type: ignore[no-untyped-def]
        document["boundary"]["x"] = "periodic"
        document["packets"][0]["top"]["x"] = [0, document["shape"][0] - 1]  # the photon fills the ring
        document["packets"][0]["edge"]["x"] = 0
        document["node_detectors"] = []
        document.pop("draw", None)

    ringed = parsed(CLICKS, ring)
    assert ringed.bodies[0].detector.draw.window == 15


def test_a_small_world_with_the_instrument_body_clicks_at_the_derived_cadence(tmp_path):
    """(5) Universe24 cut to 30 intervals: the first instrument's (body 4, at [902, 1000]) windows close at 15 and 30, the derived cadence, and every credit line of the body falls at a close with the window [close - 14, close]; the former file's cadence of 12 closed at 12 and 24."""
    document = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    document["intervals"] = 30
    (world := tmp_path / "universe24.json").write_text(json.dumps(document), encoding="utf-8")
    mode = json.loads(UNIVERSE.with_suffix(".mode.json").read_text(encoding="utf-8"))
    mode["world_digest"] = world_files.input_digest(document)
    world.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_shipped(world), lines.append)
    for _ in range(30):
        board.step()
    credits = [c for c in lines if c.get("event") == "credit" and c.get("node_detector") == "body 4"]
    assert credits and all(
        c["interval"] % 15 == 0 and c["window"] == [c["interval"] - 14, c["interval"]] for c in credits
    )
    assert all(c["interval"] in (15, 30) for c in credits) and not any(
        c["interval"] in (12, 24) for c in credits
    )
