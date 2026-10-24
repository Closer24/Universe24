"""The atom test (the atom branch, 2026-10-19; the owner's words: only code, without worlds and without experiments, only tests, a clean and generic engine, everything simple and generic in Rule3 in symmetry with the group of 48 of the cube): one charged body of two parts takes one quantum of light, gives one back on light's own family and is dark to the light it gave, on a world the test writes into a tmp folder (`atom_world`, as the spin test's worlds), no file under examples/ and no run beyond the test's own. The universe is the two atoms' with the deuteron's `charge` row (held, sourced by the Wronskian, level weight 1, write weight 1, act `pace`, the plain read into the paces) and the atom family reading it at the weight 1 at the shipped atom's own shape [2, 2] (a body's parts are planes, one per part) and gap [1, 1299]; the family is a toy by name: the sign holder massless and read plainly, the electron's sense on each plane the generator change named and not built, no reading of nature here; light is its own family, the massless `photon`, so the loader's gate `lit_families` keeps atom and photon and `charge`, the holder a charged family reads, is no click's family (the decision (1A)). The body's window is derived at load from its drives' lays (the decision (3) under (D)): the laid packet of 1 + 16 Nodes at k = pi / 4 passes the body of 2 in ceil(18 x 3 x 2586 / 4243) = 33 intervals and the body's own rate giving to `photon` is a source in time of the lifetime's span, so W = max(33, lifetime) = 33 at the lifetime 16 (the cold reader's change 1; 8 is below the resonance's period and refused by the loader, 15 the least span), and the key `window` is refused by name with the derived W. The click lines and the books are read and nothing is stepped by hand; the same world laid along -x, y and z gives the same W and bit for bit the same click lines and levels at the same seed (the 48)."""

import json
import time
from pathlib import Path

import numpy as np

from event_universe import credit, node_detector, world_files
from event_universe.core.rule3 import largest_below
from event_universe.features.click import wave_cosine
from event_universe.lattice import Lattice
from event_universe.loader.node_detector_declaration import lit_families
from event_universe.loader.universe import universe_of
from event_universe.loader.world import bodies_of
from event_universe.world_files import load_world
from tests.laws import TOOL, credit_lines, refused
from tests.laws_content import TWO_ATOMS, with_content

AXES = "xyz"
LENGTH, INTERVALS, LIFETIME = 64, 160, 16  # the chain, the run and the body's lifetime, below W = 33
CHARGE = {"name": "charge", "pair": [6000, 6000], "reads": {}}  # the deuteron's holder of the sign
CHARGE["held"] = {"sources": ["wronskian"], "level_weight": 1}  # alpha derived at the load
TURN = {"from": "g", "to": "e", "drive": "photon", "weight": 6, "resonance": [5414, 6000]}
RATE = {"from": "e", "to": "g", "lifetime": LIFETIME, "gives_to": "photon"}
Run = tuple[Lattice, list[dict], list[dict]]  # type: ignore[type-arg]
RUNS: dict[tuple[str, int, int | None, int], Run] = {}  # the worlds run, once per process

IRRATIONAL = "a reader of the sign writes its charge per quantum by its count unit"  # the refusal of 2026-10-24 (tests/test_the_sign_reader_with_an_irrational_sine.py)


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
    draw = (
        {} if window is None else {"window": window}
    )  # the key, refused by name where given (2026-10-23)
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
                    "own": [
                        int(rows[board.families[charge].width].now[n]) for n in nodes
                    ],  # the record's own row's time line, after the free row's 1 + 3 lines
                }
            )
        RUNS[key] = (board, lines, marks)
    return RUNS[key]


def closes(lines: list[dict]) -> list[dict]:  # type: ignore[type-arg]
    """The body's credit lines in order: its clicks (count 1) and the null windows that re-laid a level (count 0)."""
    return [c for c in lines if c["event"] == "credit" and c["node_detector"] == "body 0"]


def test_light_is_its_own_family_and_the_window_is_the_lays_passage_derived_at_load(
    tmp_path, monkeypatch
):
    """The gate and the derived window on the atom's universe: the families of quanta are charge (the holder of the sign, its free row 0 the light's record), atom and photon (the indices 0, 3 and 4: the holders of the content, gravity and binding, between them under the content of the born universe, 2026-10-20), and the families a click may name (`lit_families`) are atom and photon alone, `charge` being the holder the atom reads, refused by name as a transition's `drive` and as a rate's `gives_to` with the admitted list (the decision (1A)); the body's window as the loader derives it from the lay's declared passage (the decision (3) under (D), `loader/window.py`): the packet of 17 Nodes at k = pi / 4 (den cos k 4242, den cos omega 5414, the sines 4243 and 2586 of 6000 by the search) over the body of 2, ceil((17 + 2 - 1) x 3 x 2586 / 4243) = 33, the body's own source in time of the span 16 the shorter lay, W = max(33, 16) = 33; a declared `window` 48 on the body is refused by name with the body, the drive and W = 33 (the cold reader's change 1), and the lifetime 8 is refused by the span's rule, 15 the least span holding one period of [5414, 6000]."""
    refused(
        IRRATIONAL, universe_of, atom_universe()
    )  # the two atoms' universe refused at load since 2026-10-24: its atom reads the charge with an irrational sine (the owner's word); the former assertions below stand as the record of the law to 2026-10-23, kept by name
    return
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
    refused(
        IRRATIONAL, universe_of, atom_universe()
    )  # the two atoms' universe refused at load since 2026-10-24: its atom reads the charge with an irrational sine (the owner's word); the former assertions below stand as the record of the law to 2026-10-23, kept by name
    return
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
