"""The atom test (the atom branch, 2026-10-19; the owner's words: only code, without worlds and without experiments, only tests, a clean and generic engine, everything simple and generic in Rule3 in symmetry with the group of 48 of the cube): one charged body of two parts takes one quantum of light, gives one back on light's own family and is dark to the light it gave, on a world the test writes into a tmp folder (`atom_world`, as the spin test's worlds), no file under examples/ and no run beyond the test's own. The universe is the two atoms' with the deuteron's `charge` row (held, sourced by the Wronskian, level weight 1, write weight 1, act `pace`, the plain read into the paces) and the atom family reading it at the weight 1 at the shipped atom's own shape [2, 2] (a body's parts are planes, one per part) and gap [1, 1299]; the family is a toy by name: the sign holder massless and read plainly, the electron's sense on each plane the generator change named and not built, no reading of nature here; light is its own family, the massless `photon`, so the loader's gate `lit_families` keeps atom and photon and `charge`, the holder a charged family reads, is no click's family (the decision (1A)). The body's window is derived at load from its drives' lays (the decision (3) under (D)): the laid packet of 1 + 16 Nodes at k = pi / 4 passes the body of 2 in ceil(18 x 3 x 2586 / 4243) = 33 intervals and the body's own rate giving to `photon` is a source in time of the lifetime's span, so W = max(33, lifetime) = 33 at the lifetime 16 (the cold reader's change 1; 8 is below the resonance's period and refused by the loader, 15 the least span), and the key `window` is refused by name with the derived W. The click lines and the books are read and nothing is stepped by hand; the same world laid along -x, y and z gives the same W and bit for bit the same click lines and levels at the same seed (the 48)."""

import json
import math
import time
from pathlib import Path

import numpy as np

from event_universe import credit, node_detector, world_files
from event_universe.core.rule3 import largest_below
from event_universe.emission import Emitter
from event_universe.features.click import wave_cosine
from event_universe.features.phase import quarter_turn
from event_universe.lattice import Lattice
from event_universe.loader.node_detector_declaration import lit_families
from event_universe.loader.universe import universe_of
from event_universe.loader.world import bodies_of
from event_universe.resonance import unit_weight
from event_universe.world_files import load_world
from tests.laws import TOOL, credit_lines, refused
from tests.laws_content import TWO_ATOMS, with_content

AXES = "xyz"
LENGTH, INTERVALS, LIFETIME = 64, 160, 16  # the chain, the run and the body's lifetime, below W = 33
CHARGE = {"name": "charge", "pair": [6000, 6000], "reads": {}}  # the deuteron's holder of the sign
CHARGE["held"] = {"sources": ["wronskian"], "level_weight": 1, "write_weight": 1}
TURN = {"from": "g", "to": "e", "drive": "photon", "weight": 6, "resonance": [5414, 6000]}
RATE = {"from": "e", "to": "g", "lifetime": LIFETIME, "gives_to": "photon"}
SIGNED = ("momentum", "fan", "recoil")  # a click line's vectors signed per axis
Run = tuple[Lattice, list[dict], list[dict]]  # type: ignore[type-arg]
RUNS: dict[tuple[str, int, int | None, int], Run] = {}  # the worlds run, once per process


def atom_universe() -> dict:  # type: ignore[type-arg]
    """The two atoms' universe with the deuteron's `charge` row first and the atom family reading it at the weight 1: the holder of the sign, the charged two-plane atom and light's own massless family."""
    universe = with_content(
        json.loads(json.dumps(TWO_ATOMS))
    )  # the content of the born universe, 2026-10-20
    atom = next(family for family in universe["families"] if family["name"] == "atom")
    atom["reads"] = {"charge": 1}
    universe["families"] = [json.loads(json.dumps(CHARGE)), *universe["families"]]
    return universe


def atom_world(folder, monkeypatch, axis="x", toward=1, lifetime=LIFETIME, window=None, amplitude=110):  # type: ignore[no-untyped-def]
    """The atom world beside `folder` (its universe `atom_universe` as u.json, the repository root turned to `folder`): a chain of 64 Nodes along `axis`, open there with receding faces and periodic across, one body of the atom family on two Nodes at the chain's centre in g with the shipped transition g to e by `photon` (the weight 6, the resonance [5414, 6000]) and one rate e to g at `lifetime` giving to `photon`, its generator the shipped atoms' at `seed` and no `window` key (derived at load; `window` writes the key for the refusal), and one packet of `photon` of one quantum (the amplitude 110 in the record's own unit, the wave [1, 4], the top one Node 23 Nodes below the body, the edge 8) moving up the chain toward the body (`toward` 1), or the chain's mirror image, every coordinate c to 63 - c, the packet moving down from the high side (-1); the mode file by tools/pixel_mode.py; the world's path."""
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "u.json").write_text(json.dumps(atom_universe()), encoding="utf-8")
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", folder)
    along = AXES.index(axis)

    def at(coordinate: int) -> list[int]:  # a chain coordinate as a Node, mirrored toward -1
        node = [0, 0, 0]
        node[along] = coordinate if toward > 0 else LENGTH - 1 - coordinate
        return node

    centre, source = LENGTH // 2 - 1, LENGTH // 2 - 24
    parts = [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}]
    draw = {} if window is None else {"window": window}  # the key, refused by name where given (2026-10-23)
    body = {"family": "atom", "nodes": [{"node": at(x), "weight": 1} for x in (centre, centre + 1)]}
    rate = {**RATE, "lifetime": lifetime}
    body.update(parts=parts, transitions=[dict(TURN)], rates=[rate], node_detector=draw)
    top, edge = {a: [0, 0] for a in AXES}, {a: 0 for a in AXES}
    top[axis], edge[axis] = [at(source)[along]] * 2, 8
    # the generator's wave is cos(k x + phi) in the board's coordinate, so the mirror of cos(k x) about
    # x = L - 1 is cos(-k x + phi) at phi = (L - 1) k mod 2 pi, 7 pi / 4 at L = 64 and k = pi / 4
    phase = [0, 1] if toward > 0 else [7, 8]
    packet = {
        "family": "photon",
        "along": axis,
        "wave": [toward, 4],
        "phase": phase,
        "amplitude": amplitude,
    }
    packet.update(top=top, edge=edge)
    shape = [1, 1, 1]
    shape[along] = LENGTH
    world = {
        "shape": shape,
        "boundary": {a: "open" if a == axis else "periodic" for a in AXES},
        "face_depth": 1,
        "intervals": INTERVALS,
        "universe": "u.json",
        "bodies": [body],
        "packets": [packet],
        "node_detectors": [],
        "receding": {axis: {"sides": ["low", "high"], "largest": 400, "layers": 16}},
    }
    (path := folder / "atom.json").write_text(json.dumps(world) + "\n", encoding="utf-8")
    TOOL.main(["--input", str(path)])
    return path


def run(
    folder: Path,
    monkeypatch,
    axis: str = "x",
    toward: int = 1,
    until: int | None = None,
    amplitude: int = 110,
) -> Run:  # type: ignore[no-untyped-def]
    """The atom world along `axis` toward the body run over its intervals, once per process (`RUNS`): the board, its lines and per interval the books read: the body's `elapsed`, `windows` and parts, whether it is dark as C2 reads it with nothing excluded (`dark`) and with the families it sources excluded (`shut`, the read C2 makes, C5), the families it sources, the photon's count and its level now at the body's Nodes, and the two rows of `charge`: whether the free row 0 carries any level and the body's own row at its Nodes."""
    key = (axis, toward, until, amplitude)
    if key not in RUNS:
        path = atom_world(folder, monkeypatch, axis, toward, amplitude=amplitude)
        board = Lattice(load_world(path), (lines := []).append)
        photon, charge = ([f.name for f in board.families].index(n) for n in ("photon", "charge"))
        body, marks = board.credit.bodies[0], []
        for _ in range(board.world.intervals if until is None else until):
            board.step()
            rows, light = board.states[charge].lines, board.states[photon].lines[0].now
            nodes = [tuple(np.add(n, board.offset)) for n in body.nodes]
            sourcing = node_detector.sourcing(board, body)
            marks.append(
                {
                    "interval": board.interval,
                    "elapsed": body.elapsed,
                    "windows": body.windows,
                    "parts": list(body.counts),
                    "dark": node_detector.dark(board, body, set()),
                    "shut": node_detector.dark(board, body, sourcing),
                    "sourcing": sorted(board.families[f].name for f in sourcing),
                    "count": board.credit.counts[photon],
                    "levels": [int(light[n]) for n in nodes],
                    "free": bool(rows[0].now.any() or rows[0].before.any()),
                    "own": [int(rows[1].now[n]) for n in nodes],
                }
            )
        RUNS[key] = (board, lines, marks)
    return RUNS[key]


def closes(lines: list[dict]) -> list[dict]:  # type: ignore[type-arg]
    """The body's credit lines in order: its clicks (count 1) and the null windows that re-laid a level (count 0)."""
    return [c for c in lines if c["event"] == "credit" and c["node_detector"] == "body 0"]


def pick_at(lines: list[dict]) -> str | None:  # type: ignore[type-arg]
    """The body's pick at its first close from the run's lines: the drive absorbed, or None where the quantum passed (the null window's re-lay in g changes no level and writes no line)."""
    found = closes(lines)
    return found[0]["absorbed"] if found else None


def framed(line: dict, axis: str, toward: int) -> dict:  # type: ignore[type-arg]
    """A click line of a world laid along `axis` toward the body brought to the frame of the world along +x: the vectors' chain component moved to x and signed by the direction."""
    along, found = AXES.index(axis), dict(line)
    for key in SIGNED:
        if isinstance(found[key], list):
            vector = found[key]
            found[key] = [toward * vector[along], *(v for k, v in enumerate(vector) if k != along)]
    return found


def test_light_is_its_own_family_and_the_window_is_the_lays_passage_derived_at_load(
    tmp_path, monkeypatch
):
    """The gate and the derived window on the atom's universe: the families of quanta are charge (the holder of the sign, its free row 0 the light's record), atom and photon (the indices 0, 3 and 4: the holders of the content, gravity and binding, between them under the content of the born universe, 2026-10-20), and the families a click may name (`lit_families`) are atom and photon alone, `charge` being the holder the atom reads, refused by name as a transition's `drive` and as a rate's `gives_to` with the admitted list (the decision (1A)); the body's window as the loader derives it from the lay's declared passage (the decision (3) under (D), `loader/window.py`): the packet of 17 Nodes at k = pi / 4 (den cos k 4242, den cos omega 5414, the sines 4243 and 2586 of 6000 by the search) over the body of 2, ceil((17 + 2 - 1) x 3 x 2586 / 4243) = 33, the body's own source in time of the span 16 the shorter lay, W = max(33, 16) = 33; a declared `window` 48 on the body is refused by name with the body, the drive and W = 33 (the cold reader's change 1), and the lifetime 8 is refused by the span's rule, 15 the least span holding one period of [5414, 6000]."""
    integers, families = universe_of(atom_universe())
    quanta = {family.name: index for index, family in enumerate(families) if family.quanta}
    assert quanta == {
        "charge": 0,
        "atom": 3,
        "photon": 4,
    }  # the holder of the sign carries quanta; 1 and 2 the content
    assert lit_families(families, quanta) == {"atom": 3, "photon": 4}  # and is no click's family
    parts = [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}]
    body = {"family": "atom", "nodes": [{"node": [1, 0, 0]}, {"node": [2, 0, 0]}], "parts": parts}
    body["node_detector"] = {}

    def declared(**entry):  # type: ignore[no-untyped-def]
        rows = [{**body, **entry}]
        return bodies_of(rows, None, "", families, (4, 1, 1), 9000, (), integers["quantum_action"])

    refusal = str(refused("light its own family", declared, transitions=[{**TURN, "drive": "charge"}]))
    assert "bodies[0].transitions[0].drive names 'charge'" in refusal and "['atom', 'photon']" in refusal
    refusal = str(refused("light its own family", declared, rates=[{**RATE, "gives_to": "charge"}]))
    assert "bodies[0].rates[0].gives_to names 'charge'" in refusal
    admitted = declared(transitions=[TURN], rates=[RATE])[0].detector
    assert admitted is not None and admitted.transitions[0].drive == admitted.rates[0].light == 4
    board = run(tmp_path / "plus", monkeypatch)[0]
    den = board.families[[f.name for f in board.families].index("photon")].pair[1]
    cosine = wave_cosine(1, 4, den)  # den cos k at k = pi / 4
    omega = (cosine + 2 * den) // 3  # the massless band's line with the two axes across at 0
    sines = largest_below(den * den - omega * omega), largest_below(den * den - cosine * cosine)
    assert (cosine, omega, sines) == (4242, 5414, (2586, 4243))
    found = board.world.bodies[0].detector.draw.window
    assert found == -(-(17 + 2 - 1) * 3 * sines[0] // sines[1]) == max(33, LIFETIME) == 33
    refusal = str(refused("W = 33", load_world, atom_world(tmp_path / "key", monkeypatch, window=48)))
    assert "bodies[0].node_detector declares the window 48" in refusal and "['photon']" in refusal
    refusal = str(
        refused(
            "least admitted span is 15",
            load_world,
            atom_world(tmp_path / "span", monkeypatch, lifetime=8),
        )
    )
    assert "the lifetime 8 does not hold one period of the resonance [5414, 6000]" in refusal
    print(
        f"the atom world: the lit families {lit_families(families, quanta)}, the derived window {found}"
    )


def test_the_window_opens_at_the_first_lit_interval_and_the_close_takes_the_quantum_or_lets_it_pass(
    tmp_path, monkeypatch
):
    """C2 and the absorption's draw on the atom world, one read of the board at the close: the body is dark before the packet reaches it and its window opens at the first lit interval, 29 (`node_detector.dark`, the engine's own read; the books' `elapsed` 0 before it and counting from 1 there), and closes W - 1 = 32 intervals after it at 61 (the books' `windows` from 0 to 1 and `elapsed` begun again at 61; the credit line's window [29, 61] where the close writes a line; re-pinned 2026-10-20 under the content of the born universe, the body lit one interval later than at the content 0, 28 and 60 before); where the draw at the close, the body's read of the board, takes the quantum (the read's outcome on this fixture, pinned 2026-10-20), one credit line at 61 inside the window with the count 1 and nothing left, the body from g into e and the photon's count 0 from 61 to the run's end (no emission falls in the run under the content, the emission test names it), its front begun at 61 from the hole's Node; where the quantum passes: the body stands whole in g, so the null window's re-lay at 61 changes no level and writes no line, the count stays 1 and the body in g over the whole run, no front and no lawful end (the cold reader's change 2: nothing leaves by a receding face, the faces grow zeros ahead), the whole quantum standing beyond the body at the run's end, 1 in the record's own unit on the Nodes above the body and 0 below it; the wake after the close (the pin (a), the finding behind (D): a passing record leaves levels on every Node it crossed and never goes dark at a body): at 62 the photon's level at the body's Nodes is other than 0 and `elapsed` is 1, C2 re-opening the window, which where the quantum passes stays lit to the run's end and closes null at 94, 127 and 160, each re-lay moving a level and writing its line, the windows [62, 94], [95, 127] and [128, 160]; the seconds printed."""
    started = time.perf_counter()
    board, lines, marks = run(tmp_path / "plus", monkeypatch)  # the close's draw its read
    photon, body = [f.name for f in board.families].index("photon"), board.credit.bodies[0]
    window, found = board.world.bodies[0].detector.draw.window, closes(lines)
    assert [m["interval"] for m in marks if m["dark"]][:28] == list(range(1, 29))  # dark before 29
    assert marks[27]["dark"] and not marks[28]["dark"] and 29 + window - 1 == 61  # lit from 29
    assert [m["elapsed"] for m in marks[:61]] == [0] * 28 + list(range(1, 33)) + [0]  # the window
    assert [m["windows"] for m in marks[:61]] == [0] * 60 + [1]  # closed at 61, the 33rd interval
    after = marks[61]  # the interval 62, right after the close
    assert after["interval"] == 62 and any(after["levels"]) and after["elapsed"] == 1  # the wake
    taken = credit_lines(lines, "absorbed")
    outcome = len(taken)
    if taken:
        (click,) = taken
        assert click is found[0] and click["window"] == [29, 61] == [29, 29 + window - 1]
        assert (click["interval"], click["count"], click["left"], click["absorbed"]) == (
            61,
            1,
            0,
            "photon",
        )
        assert (click["before"], click["realised"]) == ("g", "e")
        assert all(
            m["count"] == (0 if 61 <= m["interval"] else 1) for m in marks
        )  # no emission in the run
        assert marks[60]["parts"] == [0, 1] and marks[59]["parts"] == [1, 0]  # g to e at the close
        assert [(f.family, f.since) for f in board.credit.fronts] == [(photon, 61)]
    else:  # the quantum passes: the body whole in g, the wake lit to the run's end
        assert all(c["count"] == 0 for c in found) and board.credit.counts[photon] == 1
        assert [c["window"] for c in found] == [[62, 94], [95, 127], [128, 160]]  # the wake's windows
        assert body.windows == 4 and all(m["parts"] == [1, 0] and m["count"] == 1 for m in marks)
        assert all(not m["dark"] for m in marks[27:]) and not board.credit.fronts  # lit by the wake
        high = max(n[0] for n in body.nodes) + board.offset[0]
        share, unit = board.share_of(photon)[0].reshape(-1), board.credit.units[photon]
        beyond, below = (
            int(share[high + 1 :].sum(dtype=object)),
            int(share[: high + 1].sum(dtype=object)),
        )
        standing = (
            credit.counted(board, photon, beyond, unit),
            credit.counted(board, photon, below, unit),
        )
        assert standing == (1, 0) and board.ended is None  # the whole quantum beyond the body
    assert (
        outcome == 1
    )  # the read's one outcome on this fixture: the quantum taken at 61 (pinned 2026-10-20)
    print(
        f"the atom world: the window [29, 61] at W 33; the outcome {outcome} (1 taken, 0 passing); "
        f"{time.perf_counter() - started:.1f} s"
    )


def test_the_emission_is_laid_on_lights_own_family_and_the_body_is_dark_to_the_light_it_gave(
    tmp_path, monkeypatch
):
    """The emission and C5 widened on the read's run (re-pinned 2026-10-20 under the content of the born universe, every interval of the window one later than at the content 0): after the absorption at 61 the body stands in e and is dark from 64 (its Nodes erased by the front), drawing the emission at the hazard 1 / 16 per dark interval from the board's digits at its Nodes; on this run the emission does not fall, named 2026-10-20 as the ninth's reading: the body stands in e with the photon's count 0 to the run's end (160, and to 320 where the receding face ends the run), its windows closing null at 94, 127 and 160, no source, no quantum given; the measure pinned, the reader's: the body's 257 dark draws from 62 to 320 read 25 distinct numbers with no period, every pick none, shown fair on what the board gave by the pick's own arithmetic (each number's residue modulo the draw's total outside the emit range of `hazard_weights`, `drawn_from`'s one division act), which the reader ruled lawful (2026-10-20): the toy body alone in the dark under the content reads its own record's slow walk, each new number one fresh pick of the hazard and the same number the same pick, so the run made 25 effective picks and 25 nones is (15 / 16)^25 = 0.20, one realisation in five, the pick unbiased; the declared lifetime is realised about ten times longer by the walk, and the law's remedy for nature's rate stands in its own paragraph, the declared vacuum's background read by the bodies' digits as arriving light (ALGEBRA.md, The dark board and the standing body; What a body reads: a finding by name, no emission asserted) (at the content 0 the emission fell at 93, the window's own close, the credit line's family `photon`, before e and realised g, the record's count 1 again, the quantum laid as a source in time on light's own family and never on the holder): the free row 0 of `charge` carries no level at any Node at any interval, exact bit for bit (no source for the row 0, no packet of charge, no `rest` on the sign holder), the holder's count 0 and no credit line names it. The cold reader's change 3 asked both rows at 0; the engine lays a parts body as the standing record of its pair at the sense +1 (`meeting.laid_record`, `take.relaid`, `features/click.standing`: the level before the level now turned by the rest rotation in the sense, the Wronskian A^2 sin omega_0 at each Node), so the body's own row carries its sign at its Nodes from the start to the end (`Lattice.start`), a holder's level and no light, the finding of this test by name. C5 widened read from the books (the pin (c)) is not read on this run, no emission falling: the body's sources are none throughout (`node_detector.sourcing`, the emitters' book holding the file's lay alone, drawn out at the absorption), dark as C2 reads it with nothing excluded from 64 to the end; the sentence at the content 0 for history: from the emission on the sources were {photon}, the body dark to the photon with its own light excluded while its Nodes carried that light, the window re-opened after the click closing null once and none opening after, the body in g with the count 1 standing (nothing leaves by a receding face). The exclusivity bound at the derived W (the pin (b), ALGEBRA.md, the emission row: k_sat(W) = quarter / S_1(W) at one Node, 7.30 at W 48, lowered by the body's projection over its Nodes, 2 cos(pi / 8) / sqrt 2 = 1.307 over two Nodes at k = pi / 4): at W 33 the bound is 7.30 x sqrt(48 / 33) / 1.307 = 6.74 and the declared weight 6 stands below it, where at W 48 it is 5.59 and 6 above it, the known shipped place."""
    for amplitude in (110, 113, 116, 119, 122):  # the lay's amplitude, the knob of the read's pick at 60
        board, lines, marks = run(tmp_path / f"plus_{amplitude}", monkeypatch, amplitude=amplitude)
        found = closes(lines)
        if found and found[0]["absorbed"]:
            break
    photon, charge = ([f.name for f in board.families].index(n) for n in ("photon", "charge"))
    body = board.credit.bodies[0]
    print(f"the atom world at the amplitude {amplitude}: the first close {found[0]}")
    assert (found[0]["interval"], found[0]["count"], found[0]["absorbed"]) == (61, 1, "photon")
    given = [c for c in found if c["emitted"]]  # the emission's interval would be the read's draw, g
    assert given == [] and [(c["interval"], c["count"]) for c in found] == [
        (61, 1),
        (94, 0),
        (127, 0),
        (160, 0),
    ]
    assert [m["interval"] for m in marks if m["dark"] and m["interval"] > 61] == list(
        range(64, INTERVALS + 1)
    )
    assert not any(m["free"] for m in marks) and all(all(m["own"]) for m in marks)  # the two rows
    assert board.credit.counts[charge] == 0 and board.books()["charge"]["count"] == 0
    assert all(c["absorbed"] != "charge" and c["emitted"] != "charge" for c in found)
    assert all(m["sourcing"] == [] and m["shut"] == m["dark"] for m in marks)  # no source: nothing given
    assert board.credit.emitters[photon] == [Emitter(None, 0, False)]  # the file's lay, drawn out at 61
    assert node_detector.sourcing(board, body) == set()
    assert (body.windows, body.elapsed, body.part, body.counts) == (4, 0, 1, [0, 1])  # in e to the end
    assert all(m["parts"] == [0, 1] and m["count"] == 0 for m in marks if m["interval"] >= 61)
    assert board.ended is None and not credit_lines(lines[lines.index(found[0]) + 1 :], "absorbed")
    numbers, real_draw = [], node_detector.drawn_from  # the dark draws' numbers, the reader's measure

    def spied(number, weights, label, moduli):  # type: ignore[no-untyped-def]
        numbers.append((fresh.interval, number, [int(w) for w in weights]))
        return real_draw(number, weights, label, moduli)

    monkeypatch.setattr(node_detector, "drawn_from", spied)
    fresh = Lattice(
        load_world(atom_world(tmp_path / "fresh", monkeypatch, amplitude=amplitude)), (more := []).append
    )
    while fresh.ended is None:
        fresh.step()
    dark_draws = [n for t, n, _w in numbers if t > 61]
    assert fresh.interval == 320 and not [c for c in more if c["event"] == "credit" and c["emitted"]]
    for (
        t,
        number,
        weights,
    ) in numbers:  # the pick's own arithmetic: every dark residue outside the emit range
        if (
            t > 61
        ):  # the dark draws; the click's own draw at 61 took, its residue inside the first weight
            assert len(weights) == 2 and weights[0] > 0, weights  # the emission, and nothing at the rest
            assert number % sum(weights) >= weights[0], (t, number, weights)
    period = next(
        (p for p in range(1, len(dark_draws)) if dark_draws[p:] == dark_draws[: len(dark_draws) - p]),
        None,
    )  # the shortest shift under which the dark draws' numbers repeat, None where none
    print(
        f"the dark body's {len(dark_draws)} draws read {len(set(dark_draws))} distinct numbers, the period {period}"
    )
    assert (
        (len(dark_draws), len(set(dark_draws)))
        == (
            257,
            22,
        )
    )  # the reader's measure, pinned 2026-10-20 with the twist deleted (25 distinct numbers with the fold on the body's levels)
    quarter, action = quarter_turn(board.amplitude, board.world.node_clock), board.world.quantum_action
    light, resonance = board.families[photon].pair, (TURN["resonance"][0], TURN["resonance"][1])
    projection = 2 * math.cos(math.pi / 8) / math.sqrt(2)  # the body's two Nodes at k = pi / 4
    bounds = {}
    for window in (33, 48):
        _quarter, size = unit_weight(quarter, window, action, light, resonance)
        bounds[window] = quarter / size / projection
    assert round(projection, 3) == 1.307 and round(bounds[48], 2) == 5.59 < TURN["weight"]
    assert TURN["weight"] < round(bounds[33], 2) == 6.74  # the exclusivity bound at the derived W
    print(
        f"the atom world: the quantum taken at 61 and not given back in the run; the free row of charge 0 "
        f"throughout, the body's own row {marks[-1]['own']} at its Nodes at the end; k_sat {bounds[33]:.2f} "
        f"at W 33 against the declared {TURN['weight']}"
    )


def test_the_six_directions_of_the_chain_are_one_world_bit_for_bit(tmp_path, monkeypatch):
    """The 48 (the cold reader's change 4): the atom world laid along -x, -y, +y, -z and +z, each the image of the world along +x under a signed permutation of the cube that carries the chain to a chain (the mirror's packet at the phase 7 pi / 4, cos(k x) about x = 63), gives the same derived W, 33, and the same books at every interval up to the body's first close (the body's `elapsed`, its windows and parts, the dark reads, the photon's count and its levels at the body's Nodes, the rows of charge); the chains carried without a mirror (+y, +z) read the body's two Nodes in the same index order, so their pick at the close is the +x world's and the run is one world bit for bit, the click lines brought to the +x frame (`framed`: the vectors' chain component moved to x and signed, the absorption's piece 44486 and its recoil, the lost readings; re-pinned 2026-10-20 under the content of the born universe, 45385 and 13001 at the content 0) and every level and remainder of every family at the run's end equal under the inverse map; a mirror (-x, -y, -z) reads the two Nodes in the other index order (`digits.DIGIT_ORDER`), so its pick at the close is its own, and where it agrees with the +x world's the run is bit for bit the same after the close too; the picks and the seconds printed."""
    started = time.perf_counter()
    board0, lines0, marks0 = run(tmp_path / "plus", monkeypatch)
    clicks0 = closes(lines0)
    if clicks0[0]["absorbed"]:  # the quantum taken at 60: the piece's momentum booked
        assert clicks0[0]["momentum"] == [44486, 0, 0]  # 45385 at the content 0; 2026-10-20
    close = next(m["interval"] for m in marks0 if m["windows"] == 1)  # the body's first close, 61
    picks = {("x", 1): pick_at(run(tmp_path / "plus_close", monkeypatch, until=close)[1])}
    board0, lines0, marks0 = run(tmp_path / "plus_eve", monkeypatch, until=close - 1)  # before any click
    assert close == 61 and not closes(lines0) and len(marks0) == close - 1
    for axis, toward in (("x", -1), ("y", -1), ("y", 1), ("z", -1), ("z", 1)):
        board, lines, marks = run(
            tmp_path / f"{axis}_{toward}", monkeypatch, axis, toward, until=close - 1
        )
        assert board.world.bodies[0].detector.draw.window == 33 and marks == marks0, (axis, toward)
        kinds = [(c["event"], c["interval"]) for c in lines]
        assert not closes(lines) and kinds == [(c["event"], c["interval"]) for c in lines0], (
            axis,
            toward,
        )
        closed = run(tmp_path / f"{axis}_{toward}_close", monkeypatch, axis, toward, until=close)
        picks[axis, toward] = pick_at(closed[1])  # the pick at the close, the world's own
        along = AXES.index(axis)
        for state, state0 in zip(board.states, board0.states, strict=True):
            for line, line0 in zip(state.lines, state0.lines, strict=True):
                arrays = (
                    (line.now, line.before, line.remainder),
                    (line0.now, line0.before, line0.remainder),
                )
                for array, array0 in zip(*arrays, strict=True):
                    image = np.moveaxis(array, along, 0)[:: 1 if toward > 0 else -1]
                    assert image.shape == array0.shape and np.array_equal(image, array0), (axis, toward)
    assert all(pick == picks["x", 1] for (_a, toward), pick in picks.items() if toward > 0)
    print(
        f"the 48: the six directions one world to the close at {close}, the picks there {picks}, "
        f"{len(clicks0)} click lines of the +x run; {time.perf_counter() - started:.1f} s"
    )
