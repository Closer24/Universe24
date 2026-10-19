"""The window derived from the record's declared passage (the atom branch claude/atom-events, (3), 2026-10-19; the owner's decision with the cold reader's five changes; ALGEBRA.md, The click writes on the lattice, C2; `loader/window.py`): a body's window is the longest passage over it of its drives' lays with an end, every lay of the family on the board, derived at load from the declaration alone, the same along every axis and in either direction (the group of 48 of the cube), the key refused by name where derived and required where a lay has no end or none is laid; and C5 widened to the emitters' book (`node_detector.sourcing`): a body dark to the light it gave while its given quanta stand. The worlds are the shipped files loaded and never stepped and the tests' own small worlds; no folder is run."""

import json
from pathlib import Path

from event_universe import node_detector, world_files
from event_universe.core.rule3 import largest_below
from event_universe.emission import Emitter
from event_universe.features.click import wave_cosine
from event_universe.lattice import Lattice
from event_universe.loader import window
from event_universe.loader.draw import Draw
from event_universe.loader.world import World, parse_world
from tests.laws import EVENTS, emit_and_take_world, refused

CHAIN, ANTICOINCIDENCE = EVENTS / "chain", EVENTS / "anticoincidence"
SIX = sorted(json.loads((CHAIN / "design.json").read_text(encoding="utf-8"))["worlds"])


def declared(path: Path, window: int | None = None, edit=None) -> World:  # type: ignore[no-untyped-def]
    """The shipped world at `path` parsed as a document with every body's `window` key removed, or set to `window`, and `edit` applied to the document, the mode file beside the path read against the file's own digest, so that the lays stand as the generator wrote them; no interval stepped."""
    document = json.loads(path.read_text(encoding="utf-8"))
    files, digest = world_files.world_files(document), world_files.input_digest(document)
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
    for name in ("one_photon", "two_photons"):
        world = declared(ANTICOINCIDENCE / f"{name}.json")
        assert windows(world) == [33, 33] and passages(world, 0)[:1] == [33]
        assert all(not body.detector.rates for body in world.bodies if body.detector is not None)
    for name in SIX:
        world = declared(CHAIN / f"{name}.json")
        assert windows(world) == [48, 48] and passages(world, 0) == [35, 48, 48], name  # the longest 48
        assert [r.lifetime for b in world.bodies if b.detector for r in b.detector.rates] == [48, 48]
    detuned = declared(CHAIN / "chain_detuned.json")
    assert windows(detuned) == [116] and passages(detuned, 0) == [116, 48]
    emitted = declared(EVENTS / "packet_emission" / "packet_emission.json")
    assert windows(emitted) == [758] and passages(emitted, 0) == [758]
    assert (wave_cosine(1, 5, den), largest_below(den * den - 4000 * 4000)) == (4853, 4472)
    print(
        f"the derived windows: one_photon {windows(declared(ANTICOINCIDENCE / 'one_photon.json'))}, the chain's six "
        f"{[windows(declared(CHAIN / f'{n}.json')) for n in SIX]} (the lays {passages(world, 0)}), chain_detuned "
        f"{windows(detuned)} (the lays {passages(detuned, 0)}), packet_emission {windows(emitted)}"
    )


def test_the_key_is_refused_by_name_where_derived_and_required_where_a_lay_has_no_end(tmp_path):
    """The refusals and the kept keys: a declared window on a body whose drives' lays all have an end is refused by name with the body, the drives and the derived W (one_photon's declaration with its key, W = 33; the resonance world with its ring opened, W = 48 = tau, the source in time's own duration, the emitter's own train counted for itself and read by the taker); a lay with no end keeps the declared key and its absence is refused by name with the body and the drive: the Zeno pulse filling the periodic box (zeno_1's 48 as shipped and set again), the resonance ring's source in time (48 and 96), the ion's two drives filling its box (1); mixed drives, one laid with an end and one without (two_photons on a ring with `photon_b`'s top the whole ring), the same, declared."""
    one, resonant = ANTICOINCIDENCE / "one_photon.json", EVENTS / "resonance" / "resonant.json"
    refusal = str(refused("W = 33", declared, one, 48))
    assert "bodies[0].node_detector declares the window 48" in refusal and "['photon']" in refusal

    def opened(document):  # type: ignore[no-untyped-def]
        document["boundary"]["x"], document["face_depth"] = "open", 1

    assert windows(declared(resonant, None, opened)) == [48, 48]  # the span tau, both bodies
    assert "W = 48" in str(refused("declares the window 96", declared, resonant, 96, opened))
    zeno = EVENTS / "zeno" / "zeno_1.json"
    assert windows(world_files.load_world(zeno)) == [48] and windows(declared(zeno, 48)) == [48]
    refusal = str(refused("declares no window", declared, zeno))
    assert "bodies[0].node_detector" in refusal and "['pulse']" in refusal and "no end" in refusal
    assert windows(world_files.load_world(resonant)) == [48, 96]
    assert windows(world_files.load_world(EVENTS / "shelved_ion" / "shelved_ion.json")) == [1]

    def ring(document):  # type: ignore[no-untyped-def]
        document["boundary"]["x"] = "periodic"
        del document["face_depth"], document["receding"]
        document["packets"][1]["top"]["x"] = [0, document["shape"][0] - 1]  # photon_b fills the ring

    two = ANTICOINCIDENCE / "two_photons.json"
    assert windows(declared(two, 48, ring)) == [48, 48]  # mixed drives: the declared key stands
    assert passages(declared(two, 48, ring), 0) == [33, None]
    refused("declares no window", declared, two, None, ring)


def test_an_emitter_is_dark_to_the_family_of_its_own_given_quanta_while_they_stand(
    tmp_path, monkeypatch
):
    """C5 widened to the emitters' book (the cold reader's change (a), 2026-10-19; `node_detector.sourcing`, `emission.Emitter.outstanding`): on the emit-and-take world (`tests.laws`, a periodic chain of 48) body 0 gives one quantum of the pulse as a source in time at 61 and is dark to the pulse from the lay on, through the source's span (to 108) and after it while its given quantum stands in the record, its Nodes carrying its own train (lit by the board, dark to its own light: no window opens, none closes), where the narrower line, dark to the source while it had intervals left, read the body's own train from 109 and closed a null window on it (the self-lit window; chain_detuned's body took its own quantum back at 215, seed 25, a finding by name); body 1 takes at 169 on both lines, the piece's source body 0 drawn (`twist.drawn_emitter`), the count 0, and body 0 is lit again by what stands at its Nodes; a read of the books and no geometry, symmetric under the 48 by construction."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = emit_and_take_world(tmp_path, list(range(6)), list(range(12, 18)), window=48)
    board = Lattice(world_files.load_world(path), (lines := []).append)
    pulse = [f.name for f in board.families].index("pulse")
    giver = board.credit.bodies[0]
    while not any(c["event"] == "credit" and c["emitted"] == "pulse" for c in lines):
        board.step()
    given = board.interval
    assert node_detector.sourcing(board, giver) == {pulse}
    assert board.credit.emitters[pulse] == [Emitter(0, 1, False)]
    while board.credit.sources:
        board.step()
    assert board.interval == given + 47  # the span's 48 lays
    assert node_detector.sourcing(board, giver) == {pulse}  # widened: its given quantum stands
    assert not node_detector.dark(board, giver, set())  # its Nodes carry its own train
    assert node_detector.dark(
        board, giver, node_detector.sourcing(board, giver)
    )  # dark to its own light
    while board.credit.counts[pulse] > 0:
        board.step()
    taken = [c for c in lines if c["event"] == "credit" and c["absorbed"] == "pulse"]
    assert [(c["node_detector"], c["source"]) for c in taken] == [("body 1", "body 0")]
    assert (giver.windows, giver.elapsed) == (0, 0)  # no window on its own light, through the take
    assert board.credit.emitters[pulse] == [Emitter(0, 0, False)]
    assert node_detector.sourcing(board, giver) == set() and not node_detector.dark(board, giver, set())
    print(
        f"C5 widened: body 0 gave at {given}, its source spent at {given + 47}, dark to its own light until "
        f"body 1 took at {taken[0]['interval']} and lit again by what stands at its Nodes"
    )
