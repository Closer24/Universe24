"""The window derived from the record's declared passage (the atom branch claude/atom-events, (3), 2026-10-19; the owner's decision with the cold reader's five changes; ALGEBRA.md, The click writes on the lattice, C2; `loader/window.py`): a body's window is the longest passage over it of its drives' lays with an end, every lay of the family on the board, derived at load from the declaration alone, the same along every axis and in either direction (the group of 48 of the cube), the key refused by name where derived and required where a lay has no end or none is laid; and C5 widened to the emitters' book (`node_detector.sourcing`): a body dark to the light it gave while its given quanta stand. The worlds are the shipped files loaded and never stepped and the tests' own small worlds; no folder is run."""

import json
from pathlib import Path

import pytest

from event_universe import node_detector, world_files
from event_universe.core.rule3 import largest_below
from event_universe.emission import Emitter
from event_universe.features.click import wave_cosine
from event_universe.lattice import Lattice
from event_universe.loader import window
from event_universe.loader.draw import Draw
from event_universe.loader.world import World, parse_world
from tests.laws import EVENTS, ROOT, refused, world_beside
from tests.laws_content import RESONANT, ZENO_ATOM, content_world, emit_and_take_world, opened, ring_of
from tests.laws_read import redeclared

CHAIN = EVENTS / "chain"
# the deleted two-photons world's declaration and its universe, inlined 2026-10-20 (the loader's derived window reads
# the files alone, no interval stepped): two drives, one lay without an end
TWO_PHOTONS = {
    "shape": [96, 1, 1],
    "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
    "face_depth": 1,
    "intervals": 170,
    "universe": "examples/events/anticoincidence/two_atoms_two_records.json",
    "bodies": [
        {
            "family": "atom",
            "nodes": [{"node": [23, 0, 0], "weight": 1}, {"node": [24, 0, 0], "weight": 1}],
            "parts": [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}],
            "transitions": [
                {"from": "g", "to": "e", "drive": "photon", "weight": 6, "resonance": [5414, 6000]},
                {"from": "g", "to": "e", "drive": "photon_b", "weight": 6, "resonance": [5414, 6000]},
            ],
            "rates": [],
            "node_detector": {},
        },
        {
            "family": "atom",
            "nodes": [{"node": [71, 0, 0], "weight": 1}, {"node": [72, 0, 0], "weight": 1}],
            "parts": [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}],
            "transitions": [
                {"from": "g", "to": "e", "drive": "photon", "weight": 6, "resonance": [5414, 6000]},
                {"from": "g", "to": "e", "drive": "photon_b", "weight": 6, "resonance": [5414, 6000]},
            ],
            "rates": [],
            "node_detector": {},
        },
    ],
    "packets": [
        {
            "family": "photon",
            "along": "x",
            "wave": [1, 4],
            "phase": [0, 1],
            "amplitude": 110,
            "top": {"x": [48, 48], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": 8, "y": 0, "z": 0},
        },
        {
            "family": "photon_b",
            "along": "x",
            "wave": [-1, 4],
            "phase": [0, 1],
            "amplitude": 110,
            "top": {"x": [47, 47], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": 8, "y": 0, "z": 0},
        },
    ],
    "node_detectors": [],
    "receding": {"x": {"sides": ["low", "high"], "largest": 400, "layers": 16}},
}
TWO_PHOTONS_MODE = {
    "world_digest": "f8826ef1ec30537e8c4af9c498395b136e6722b60e8277c649857fde5c65c72b",
    "bodies": [],
    "packets": [
        {
            "family": "photon",
            "pair": [6000, 6000],
            "amplitude": 110,
            "count": 1,
            "moving": {
                "now": {
                    "at": [41, 43, 44, 45, 47, 48, 49, 51, 52, 53, 55],
                    "values": [3, -24, -55, -54, 75, 110, 75, -54, -55, -24, 3],
                },
                "before": {
                    "at": [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56],
                    "values": [2, 3, -11, -43, -60, -29, 43, 103, 98, 34, -36, -61, -39, -8, 4, 1, -1],
                },
            },
        },
        {
            "family": "photon_b",
            "pair": [6000, 6000],
            "amplitude": 106,
            "count": 1,
            "moving": {
                "now": {
                    "at": [40, 41, 43, 44, 45, 47, 48, 49, 51, 52, 53],
                    "values": [4, 11, -39, -76, -66, 78, 106, 66, -39, -34, -11],
                },
                "before": {
                    "at": [41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55],
                    "values": [8, 10, -14, -58, -80, -43, 37, 99, 95, 37, -22, -41, -24, -5, 1],
                },
            },
        },
    ],
}
TWO_RECORDS = {
    "integers": {"node_clock": 6000, "quantum_action": 32768, "width": 63, "link_unit": 16},
    "families": [
        {"name": "atom", "pair": [1, 1299], "dimension": [2, 2], "reads": {}},
        {"name": "photon", "pair": [6000, 6000], "dimension": 1, "reads": {}},
        {"name": "photon_b", "pair": [6000, 6000], "dimension": 1, "reads": {}},
    ],
}
THREE = sorted(json.loads((CHAIN / "design.json").read_text(encoding="utf-8"))["worlds"])


def declared(path: Path, window: int | None = None, edit=None) -> World:  # type: ignore[no-untyped-def]
    """The shipped world at `path` parsed as a document with every body's `window` key removed, or set to `window`, and `edit` applied to the document, the mode file beside the path read against the file's own digest, so that the lays stand as the generator wrote them; no interval stepped."""
    document = json.loads(path.read_text(encoding="utf-8"))
    files, digest = world_files.world_files(document), world_files.input_digest(document)
    redeclared(document)  # the read's shape, the digest the shipped mode file's
    beside = path.with_suffix(".mode.json")
    if beside.is_file():
        files[beside.name] = json.loads(beside.read_text(encoding="utf-8"))
    for body in document["bodies"]:
        draw = body.get("node_detector", {})
        draw.pop("window", None)
        if window is not None:
            draw["window"] = window
    if edit is not None:
        edit(document)
    return parse_world(document, files, digest)


def windows(world: World) -> list[int]:
    """Every body's window as the loader left it, in the world's order."""
    return [
        b.detector.draw.window
        for b in world.bodies
        if b.detector is not None and isinstance(b.detector.draw, Draw)
    ]


def passages(world: World, number: int) -> list[int | None]:
    """The passages over the body `number` of every lay of the world, the packets and then every body's rates, as `loader/window.windowed` gathers them."""
    nodes, rates = world.bodies[number].nodes, []
    for body in world.bodies:
        rates += list(body.detector.rates) if body.detector is not None else []
    found: list[int | None] = [
        window.packet_passage(p, world.families, nodes, world.shape, world.periodic)
        for p in world.packets
    ]
    for rate in rates:
        light = world.families[rate.light]
        found.append(
            window.rate_passage(rate, light, nodes, world.shape, world.periodic, world.quantum_action)
        )
    return found


def test_the_shipped_lays_passages_are_derived_at_load_and_one_along_every_axis_and_direction():
    """The derived W of the shipped declarations loaded as files with their bodies' `window` keys removed, no interval stepped (the rule (D)): one_photon and two_photons 33, the laid packet of 1 + 16 Nodes at k = pi / 4 over a body of 2 (den cos k 4242 and den sin k 4243 by the search, den cos omega 5414 and den sin omega 2586 the unit's, ceil(18 x 3 x 2586 / 4243) = 33; the bodies declare no rate, so the packet is their one lay); the chain's six worlds 48 each, the lays over a body the laid packet 35 (L 17 over 3 Nodes) and the two bodies' emitted trains 48, the span tau, the longest the window, one number for the packet along -x, +x, -y, +y, -z and +z over the same body (the 48, the pace by |sin k|); chain_detuned 116 in the loader's integers (the packet of 48 + 16 Nodes at k = pi / 8 over 3: den cos k 5541, den sin k 2301, den cos omega 5847, den sin omega 1346; 116 in the reals too), its body's own train 48 beside it; packet_emission 758, its own emitted train of 312 slices at the width 4 and the lifetime 48 (`features/click.envelope` on the one-line root, the length the loader holds the board to) at k_x from the band with the transverse mode cos(pi / 5) on two axes (2 den cos k_x 4588, den cos k_perp 4853, den cos omega 4000 the resonance's), v_g = 5544 / (3 x 4472) = 0.413 and ceil(313 x 3 x 4472 / 5544) = 758, where the e-folding of the train alone (48 slices) would read 119."""
    den = 6000
    cosine = wave_cosine(1, 4, den)
    omega = (cosine + 2 * den) // 3  # the massless band's line with the two axes across at 0
    sines = largest_below(den * den - omega * omega), largest_below(den * den - cosine * cosine)
    assert (cosine, omega, sines) == (4242, 5414, (2586, 4243))
    assert (
        -(-18 * 3 * sines[0] // sines[1]) == 33
    )  # ceil((L + b - 1) / v_g), v_g = sin k / (3 sin omega)
    for name in (
        THREE
    ):  # re-pinned 2026-10-20: the chain's three worlds along the axes, the toy atom worlds deleted
        world = declared(CHAIN / f"{name}.json")
        assert windows(world) == [48, 48] and passages(world, 0) == [35, 48, 48], name  # the longest 48
        assert [r.lifetime for b in world.bodies if b.detector for r in b.detector.rates] == [48, 48]
    for name in sorted(
        json.loads((EVENTS / "chain" / "design.json").read_text(encoding="utf-8"))["worlds"]
    ):
        world = declared(EVENTS / "chain" / f"{name}.json")
        assert windows(world) == [48, 48] and passages(world, 0) == [35, 48, 48], name  # the longest 48
        assert [r.lifetime for b in world.bodies if b.detector for r in b.detector.rates] == [48, 48]
    emitted = declared(EVENTS / "packet_emission" / "packet_emission.json")
    assert windows(emitted) == [758] and passages(emitted, 0) == [758]
    assert (wave_cosine(1, 5, den), largest_below(den * den - 4000 * 4000)) == (4853, 4472)
    print(
        f"the derived windows: the chain's three (the lays {passages(world, 0)}), packet_emission {windows(emitted)}"
    )


def test_the_key_is_refused_by_name_where_derived_and_required_where_a_lay_has_no_end(tmp_path):
    """The refusals and the kept keys: a declared window on a body whose drives' lays all have an end is refused by name with the body, the drives and the derived W (one_photon's declaration with its key, W = 33; the resonance world with its ring opened, W = 48 = tau, the source in time's own duration, the emitter's own train counted for itself and read by the taker); a lay with no end keeps the declared key and its absence is refused by name with the body and the drive: the Zeno pulse filling the periodic box (zeno_1's 48 as shipped and set again), the resonance ring's source in time (48 and 96), the ion's two drives filling its box (1); mixed drives, one laid with an end and one without (two_photons on a ring with `photon_b`'s top the whole ring), the same, declared."""
    chain, resonant = CHAIN / "chain_x_minus.json", EVENTS / "resonance" / "resonant.json"
    refusal = str(
        refused("W = 48", declared, chain, 96)
    )  # re-pinned 2026-10-20 from one_photon's W = 33
    assert "bodies[0].node_detector declares the window 96" in refusal and "['photon']" in refusal

    def opened(document):  # type: ignore[no-untyped-def]
        document["boundary"]["x"], document["face_depth"] = "open", 1

    assert windows(declared(resonant, None, opened)) == [48, 48]  # the span tau, both bodies
    assert "W = 48" in str(refused("declares the window 96", declared, resonant, 96, opened))

    def shipped(path):  # type: ignore[no-untyped-def]
        copied = world_beside(tmp_path / path.stem, path, lambda w: None)  # the read's shape
        try:
            return world_files.load_world(copied)
        finally:
            world_files.REPOSITORY_ROOT = ROOT  # the shipped files read at their paths after

    assert windows(shipped(resonant)) == [48, 96]

    def ring(document):  # type: ignore[no-untyped-def]
        document["boundary"]["x"] = "periodic"
        del document["face_depth"], document["receding"]
        document["packets"][1]["top"]["x"] = [0, document["shape"][0] - 1]  # photon_b fills the ring

    (universe := tmp_path / "two_records.json").write_text(json.dumps(TWO_RECORDS), encoding="utf-8")
    document = {**TWO_PHOTONS, "universe": str(universe)}
    (two := tmp_path / "two_photons.json").write_text(json.dumps(document), encoding="utf-8")
    mode = {**TWO_PHOTONS_MODE, "world_digest": world_files.input_digest(document)}
    two.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    assert windows(declared(two, 48, ring)) == [48, 48]  # mixed drives: the declared key stands
    assert passages(declared(two, 48, ring), 0) == [33, None]
    refused("declares no window", declared, two, None, ring)


def test_an_emitter_is_dark_to_the_light_it_gave_while_its_quanta_stand_where_the_lay_has_an_end(
    tmp_path,
):
    """C5's reach where the lay has an end (the cold reader's change (a) with the reader's fix of 2026-10-19; `node_detector.sourcing`, `Rate.ended`, `emission.Emitter.outstanding`): the resonance world opened (x open with receding faces, the ring cut, the run 200): body 0's rate lays the pulse as a source in time on an open guide, a lay with an end (`Rate.ended` True; the window of both bodies derived, 48 = tau), so from its emission on body 0 is dark to the pulse while its given quantum stands in the record, through the source's span and after it, its Nodes carrying its own train and wake (lit by the board, dark to its own light: no window opens or closes on it after), until body 1 takes the quantum, the piece's source body 0 drawn (`twist.drawn_emitter`), the count 0 and body 0 lit again by what stands at its Nodes, or the run ends with the quantum standing; a read of the books and of the lay's end, symmetric under the 48 by construction. Re-pinned 2026-10-20 under the content of the born universe (the reader's ruling: the sentence needs only the emission): the universe with the holders of the content, the box opened along x as the content's sink; body 0's first close at 48 reads no emission (e standing: under the content the emission is drawn within the span by the digits, not at the window's close as in the exact dark), the emission falls at 83, the window open at the emission closes null at 96 and none after, the body's windows 2; body 1's closes at 146 and 194 take nothing and the run ends with the quantum standing in the books, the light leaving by the faces: no take falls in the run."""

    def receding(document):  # type: ignore[no-untyped-def]
        opened(document)  # the box opened along x as the content's sink, the windows derived
        document["intervals"] = 200
        document["receding"] = {"x": {"sides": ["low", "high"], "largest": 400, "layers": 16}}

    path = content_world(tmp_path, "resonant", RESONANT, ZENO_ATOM, receding)
    board = Lattice(world_files.load_world(path), (lines := []).append)
    pulse = [f.name for f in board.families].index("pulse")
    giver, taker = board.credit.bodies
    assert [r.ended for r in giver.declared.rates] == [True] and giver.declared.draw.window == 48
    while not any(c["event"] == "credit" and c["emitted"] == "pulse" for c in lines):
        board.step()
    given = board.interval
    assert node_detector.sourcing(board, giver) == {pulse}
    assert board.credit.emitters[pulse] == [Emitter(0, 1, False)]
    while board.credit.sources:
        board.step()
    assert board.interval == given + 47  # the span's 48 lays
    dark_to_its_own = []
    while board.credit.counts[pulse] > 0 and board.interval < board.world.intervals:
        own = node_detector.sourcing(board, giver)
        dark_to_its_own.append(own == {pulse} and node_detector.dark(board, giver, own))
        board.step()
    assert all(dark_to_its_own) and len(dark_to_its_own) > 40  # widened: its quantum stands, no window
    assert (giver.windows, giver.elapsed) == (2, 0)  # the null close at 48 and the emission's window
    taken = [c for c in lines if c["event"] == "credit" and c["absorbed"] == "pulse"]
    closes = [(c["interval"], c["node_detector"], c["emitted"]) for c in lines if c["event"] == "credit"]
    assert closes == [
        (48, "body 0", None),
        (83, "body 0", "pulse"),
        (96, "body 0", None),
        (146, "body 1", None),
        (194, "body 1", None),
    ]
    assert taken == [] and board.credit.counts[pulse] == 1  # no take falls in the run (2026-10-20)
    print(
        f"C5 where the lay has an end: body 0 gave at {given}, its source spent at {given + 47}, dark to its own "
        f"light over {len(dark_to_its_own)} intervals after it; taken {[c['interval'] for c in taken]}"
    )


def test_an_emitter_on_a_periodic_board_is_dark_to_its_source_alone_and_released_at_the_spans_end(
    tmp_path, monkeypatch
):
    """C5's reach where the lay has no end (the reader's fix of 2026-10-19: a periodic board, the quantum circulating as in a cavity, the first line as on main): on the emit-and-take world (`tests.laws_content`, a periodic chain of 48) body 0's rate lays the pulse on the ring, a lay with no end (`Rate.ended` False), so body 0 is dark to the pulse while its source has intervals left and released at the span's end, lit by its own circulating train, closing a null window on it and keeping its P through the re-lay; body 1 takes with the piece's source body 0, the count 0: the readings of the periodic worlds stand as on main. History, kept by name (the reader's ruling of 2026-10-20): the sentence is the periodic board's and is not read under the content of the born universe, where the periodic chain is refused at the start by name, the held sums' rest needing a sink (asserted here on the ring re-declared from the content fixture, `ring_of`, whose loader still marks the rate's lay as one with no end); its pins stand as history: body 1's take at 353 with the piece's source body 0 and body 0's null window on its own train at 143 under the eighth commit of the read (2026-10-20), 169 and 156 before it."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    ring = world_files.load_world(
        ring_of(emit_and_take_world(tmp_path, list(range(6)), list(range(12, 18))))
    )
    assert [r.ended for r in ring.bodies[0].detector.rates] == [False]  # the lay has no end on the ring
    with pytest.raises(ValueError, match="the sum's rest needs a sink"):
        Lattice(ring)
