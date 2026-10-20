"""The helpers of the law's tests: a module loaded by its path (a tool; the generator, the back-in-time gate and the runner loaded once for every test), and the generator's bodies of ALGEBRA.md #the-generator laid on a chain of the universe the tests run on (`UNIVERSE`); the chain is the shortest that holds the body of 50 quanta (about eleven Nodes about its centre) and the end node_detectors with their regions apart, since the lay's cost is the start's relaxation over the chain's length squared, and every bound the tests put on the chain is per Node, the same on any length."""

import importlib.util
import json
import math
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe import credit, growth, node, readings, share, world_files
from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients
from event_universe.lattice import Lattice
from event_universe.loader.derived import FamilyRule, Row, quanta_records
from event_universe.loader.keys import Node
from event_universe.loader.universe import universe_of
from event_universe.loader.world import World
from event_universe.records import Record
from event_universe.world_files import input_digest, load_world
from tests.laws_read import redeclared, redeclared_file

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "examples" / "events"
UNIVERSE = EVENTS / "rule.json"  # the rule's own universe: Gamma 6000, T = 32768, the law's rows
CHAIN, QUANTA = (
    24,
    6,
)  # the shortest chain (x open) holding the body apart from the end node_detectors; the
# smallest body the generator lays on it in seconds (a test runs under 30 seconds, the owner's word)
CHARGED = {"name": "charged", "pair": [4000, 6000], "dimension": 2}  # matter's pair as a plane
# the band's top as a resonance pair, cos Omega = 0; a region declares no quantum of its own
TOP = [0, 6000]
CHARGED["reads"] = {"gravity": 1, "binding": 1, "charge": 1}  # every holder, the sign's among them


def real_rows(*rows: tuple[str, tuple[int, int], int, int | None]) -> list[Row]:
    """Rows of real lines as the loader reads them (loader.derived.Row), each (name, pair, lines, level weight): one part, no plane, sourced by the form where it is held at the write weight 1, acting on the pace, and every row reading every held row among them at the weight 1 (the tests' declaration)."""
    held = tuple((name, 1) for name, _pair, _lines, weight in rows if weight is not None)
    return [Row(n, p, k, 1, False, False, False, w, w and 1, 0, held) for n, p, k, w in rows]


def vacuum_content(world: World, family: FamilyRule) -> int:
    """The content a record of `family` reads where nothing is laid: the declared rests of the holders its declaration names, each at its read weight (ALGEBRA.md, The vacuum content, item 22; the generator's `vacuum_of`), 60 on the shipped universes with a gravity row and 0 on the atom worlds'."""
    return sum(world.families[read.family].rest * read.weight for read in family.reads)


def band_of(pair, gamma: int, content: int, unit: int, *cosines):  # type: ignore[no-untyped-def]
    """cos omega(q) in the test's floats from the line's own read at `content` (the law's (h), **L** the line's own read: 2 w cos omega(q) = S + SUM over the six Ports of R_ij cos q_a), Rule3's coefficients at the composed paces of the content with no tension; `cosines` the cos q_a of the three axes, numbers or arrays; (num / den) SUM_a cos q_a / 3 at the content 0."""
    reads, self_coefficient, wall = coefficients(
        *pair, gamma, *paces.node_paces(gamma, content), None, unit
    )
    arrived = sum(int(read) * cosines[port // 2] for port, read in enumerate(reads))
    return (int(self_coefficient) + arrived) / (2 * int(wall))


def load_file(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    sys.modules[name] = module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def refused(match: str, call, *args, **keys):
    with pytest.raises(ValueError, match=match) as refusal:
        call(*args, **keys)
    return refusal.value


def design_beside(folder: Path, stem: str, **keys: object) -> Path:
    """The folder's design file with the generator's keys for one world (`worlds[stem]`: `quanta`, `senses`, `pixels`, the inputs the generator reads from the design file beside the world and never from the command line; the owner's decision C2, #1793 comment 5982379080), the other worlds' entries kept."""
    path = folder / "design.json"
    design = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"worlds": {}}
    design["worlds"][stem] = {**design["worlds"].get(stem, {}), **keys}
    path.write_text(json.dumps(design), encoding="utf-8")
    return path


TOOLS = ("pixel_mode", "back_in_time", "run_inputs")  # the generator, the back-in-time gate, the runner
TOOL, BACK, RUN = (load_file(name, ROOT / "tools" / f"{name}.py") for name in TOOLS)
GATE = load_file("bell_gate", ROOT / "tools" / "bell_gate.py")  # the Bell and GHZ gates' reader
RECORD = load_file("look_record", ROOT / "tools" / "look" / "record.py")  # the look's reader


def universe_beside(tmp_path, drop=(), charged=False, **pairs):  # type: ignore[no-untyped-def]
    """The tests' universe copied beside a world as u.json (the families `drop` names left out, of every family's reads too, a family's pair replaced where `pairs` names it, the charged matter row, matter's pair as a plane, added where `charged`)."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    universe["families"] = [family for family in universe["families"] if family["name"] not in drop]
    universe["families"] += [json.loads(json.dumps(CHARGED))] if charged else []
    for family in universe["families"]:
        family["pair"] = pairs.get(family["name"], family["pair"])
        family["reads"] = {name: w for name, w in family["reads"].items() if name not in drop}
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")


def chain_body_world(folder, tool, quanta=QUANTA, at=(), senses=(), taker=False, mode=True, chain=CHAIN):  # type: ignore[no-untyped-def]
    """A chain of `chain` Nodes (x open) with a body of matter declared with `quanta` on each Node of `at` (the chain's centre where empty; the last read by the node_detector `taker` where asked), or, where `senses` gives the body a sense, a body of the charged family (matter's pair as a plane) rotating in that sense, one quantum of count 1 (the law's count per charged record, the loader's gate; ALGEBRA.md, No record reads its own write of the sign), laid by the generator as the one-Node record of its quantum (the design file's `pixels` and `senses` beside the chain, `design_beside`) where the matter body is laid at its fixed point: the bodies' Nodes with their counts and the mode file beside them; the node_detectors `left` and `right`, two Nodes each at the chain's two ends (never one Node), report the light's inflow there."""
    at = at or (chain // 2,)  # the chain's centre where no Node is named
    families = [CHARGED["name"] if i < len(senses) and senses[i] else "matter" for i in range(len(at))]
    universe_beside(folder, charged=CHARGED["name"] in families)
    charged = [f == CHARGED["name"] for f in families]  # one quantum per charged record, the law's count
    nodes = [[dict(node=[x, 0, 0], count=1 if c else quanta)] for x, c in zip(at, charged, strict=True)]
    bodies = [dict(family=f, nodes=n) for f, n in zip(families, nodes, strict=True)]
    ends = [{"name": "left", "positions": [[0, 0, 0], [1, 0, 0]]}]
    ends += [{"name": "right", "positions": [[chain - 2, 0, 0], [chain - 1, 0, 0]]}]
    node_detectors = ends + ([{"name": "taker", "block": len(at) - 1}] if taker else [])
    world = dict(
        shape=[chain, 1, 1], node_detectors=node_detectors, bodies=bodies, intervals=400, face_depth=1
    )
    world.update(boundary=dict(x="open", y="periodic", z="periodic"), universe="u.json")
    (path := folder / "chain.json").write_text(json.dumps(world), encoding="utf-8")
    pixels = [n for n, c in enumerate(charged) if c]  # the charged body a one-Node record
    design_beside(folder, path.stem, senses=list(senses), pixels=pixels)  # the design's keys beside
    if mode:  # the charged body laid by the design's `pixels` in its sense, matter at its fixed point
        tool.main(["--input", str(path)])
    return path


SLIT = dict(
    shape=[24, 9, 1], boundary=dict(x="open", y="open", z="periodic"), face_depth=1, intervals=24
)
SLIT.update(universe="u.json", bodies=[], node_detectors=[])
SLIT["faces"] = [{"axis": "x", "at": 12, "gaps": [{"y": [4, 4], "z": [0, 0]}]}]
PACKET = {"family": "charge", "along": "x", "wave": [1, 4], "phase": [0, 1], "amplitude": 1328}
PACKET.update(top={"x": [5, 5], "y": [0, 8], "z": [0, 0]}, edge={"x": 4, "y": 0, "z": 0})


def packet_world(folder: Path, tool, lifetime: int = 8, width: int = 3, intervals: int = 60) -> Path:  # type: ignore[no-untyped-def]
    """The open board's packet world cut small: the shipped packet emission's giver over two Nodes of a 160 by 5 by 5 board with one emission at `lifetime` and `width`, its window derived from its own train's passage (the lay's 69 slices at the lifetime 8 and the width 3: 194 intervals, `loader/window.py`; in the exact dark the giver gives at that close, `meeting.emission_fell`), the giver's detector declared with no key (its draw the click's read of the board), no world draw, its mode file written by the generator."""
    world = json.loads((EVENTS / "packet_emission" / "packet_emission.json").read_text(encoding="utf-8"))
    giver = world["bodies"][0]
    rate = {**giver["rates"][0], "width": width, "lifetime": lifetime}
    nodes = [{"node": [80, 2, 2], "weight": 1}, {"node": [81, 2, 2], "weight": 1}]
    small = {**world, "shape": [160, 5, 5], "intervals": intervals, "node_detectors": []}
    reader = {k: v for k, v in giver["node_detector"].items() if k != "window"}  # the window derived
    small["bodies"] = [{**giver, "nodes": nodes, "rates": [rate], "node_detector": reader}]
    del small["draw"]
    redeclared(small)  # the read's shape: no engine start file, no generator
    (path := folder / "small.json").write_text(json.dumps(small) + "\n", encoding="utf-8")
    tool.main(["--input", str(path)])
    return path


def ion_universe_beside(folder: Path) -> None:
    """The shelved ion's universe copied beside a world as u.json: four families, no holder of the content, so a periodic box needs no sink."""
    (folder / "u.json").write_bytes((EVENTS / "shelved_ion" / "mercury_ion.json").read_bytes())


def ion_world(folder: Path, tool, intervals: int = 23, amplitude: int = 600, body: bool = True) -> Path:  # type: ignore[no-untyped-def]
    """The ion-like world on a periodic box of 8 by 6 by 5 (one odd extent, so that the staggered mode (-1)^(x + y + z + t), the band's top, is no exact mode of the board): the three-part ion over two Nodes with its transition at [2, 3] from the strong drive and its emission to the fluorescence at the lifetime 8, the drive a plane wave along x at `amplitude`, the counter the plane x = 0 with the world's draw at the window 18, every draw the click's read of the board; the telegraph's shape, its mode file written by the generator; without the ion (`body` False) the drive and the counter alone as beam_alone.json, the twin of the undepleted beam."""
    ion_universe_beside(folder)
    shape = (8, 6, 5)
    at, beside = [3, 3, 2], [4, 3, 2]
    parts = [{"part": k, "name": n, "count": int(k == 0)} for k, n in enumerate("SPD")]
    draw = {"window": 1}
    nodes = [{"node": at, "weight": 1}, {"node": beside, "weight": 1}]
    record = {"family": "ion", "nodes": nodes, "parts": parts, "node_detector": draw}
    record["transitions"] = [
        {"from": "S", "to": "P", "drive": "strong_drive", "weight": 1, "resonance": [2, 3]}
    ]
    record["rates"] = [{"from": "P", "to": "S", "lifetime": 8, "gives_to": "fluorescence"}]
    drive = {
        "family": "strong_drive",
        "along": "x",
        "wave": [1, 2],
        "phase": [0, 1],
        "amplitude": amplitude,
    }
    top = {axis: [0, extent - 1] for axis, extent in zip("xyz", shape, strict=True)}
    drive.update(top=top, edge={"x": 0, "y": 0, "z": 0})
    plane = [[0, y, z] for y in range(shape[1]) for z in range(shape[2])]
    world = dict(
        shape=list(shape), boundary=dict(x="periodic", y="periodic", z="periodic"), intervals=intervals
    )
    world.update(universe="u.json", bodies=[record] if body else [], packets=[drive])
    world.update(node_detectors=[{"name": "counter", "positions": plane}], draw={"window": 18})
    (path := folder / ("ion_like.json" if body else "beam_alone.json")).write_text(json.dumps(world))
    tool.main(["--input", str(path)])
    return path


def slit_world(folder: Path, tool, name: str = "slit", **changes: object) -> Path:  # type: ignore[no-untyped-def]
    universe_beside(folder)
    path = folder / f"{name}.json"
    path.write_text(json.dumps({**SLIT, "packets": [PACKET], **changes}), encoding="utf-8")
    tool.main(["--input", str(path)])
    return path


def pulsed_world(folder: Path, monkeypatch) -> Path:  # type: ignore[no-untyped-def]
    """The minimal pulsed world (ALGEBRA.md, The pulsed gate): the shipped pulsed universe beside `folder` as u.json and the repository root turned to `folder`, the Zeno body over two adjacent Nodes of a periodic 3 by 3 by 3 box with the drive's two turns and the probe's transition of g into itself, no drive laid, the probe laid whole by the count at its Node at the intervals 3 and 7, no node_detectors; the world's path."""
    (folder / "u.json").write_bytes((EVENTS / "zeno_pulsed" / "pulsed_atom.json").read_bytes())
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", folder)
    draw: dict[str, object] = {}  # a body with a probe: its node_detector declares no key
    parts = [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}]
    ways, drive = (("g", "e"), ("e", "g")), {"drive": "pulse", "weight": 1, "resonance": [2, 3]}
    turns, probe = [{"from": a, "to": b, **drive} for a, b in ways], {"from": "g", "to": "g"}
    region = [{"node": [1, 1, 1], "weight": 1}, {"node": [2, 1, 1], "weight": 1}]  # two adjacent Nodes
    record = {"family": "atom", "nodes": region, "parts": parts, "rates": [], "node_detector": draw}
    record["transitions"] = [*turns, {**probe, "drive": "probe"}]
    lays = [{"family": "probe", "whole": [1, 1, 1], "count": 1, "interval": t} for t in (3, 7)]
    world = dict(shape=[3, 3, 3], boundary=dict(x="periodic", y="periodic", z="periodic"), intervals=9)
    world.update(universe="u.json", bodies=[record], packets=lays, node_detectors=[])
    (path := folder / "w.json").write_text(json.dumps(world), encoding="utf-8")
    return path


def click_key(line: dict[str, object]) -> str:
    """A click line's key as tools/meeting_trials.py counts the kinds: the reader, the part realised and the family taken or given."""
    return f"{line['node_detector']} {line['realised']} by {line['absorbed'] or line['emitted']}"


def credit_lines(lines: list[dict[str, object]], key: str) -> list[dict[str, object]]:
    """The NodeDetectors' click lines with `key` set: the credit lines labelled NODEDETECTOR whose `key` is not None."""
    return [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR" and c[key]]


def own_lines(board: Lattice, index: int) -> list[Record]:
    """A family's record lines as the engine reads them: every record's lines, light the sum of its rows."""
    return [line for r in quanta_records(board.families, index) for line in board.lines_of(index, r)]


def shares_of(board: Lattice, index: int, read, pairs) -> np.ndarray:  # type: ignore[no-untyped-def]
    """The share form per Node of a family's lines at the paces of its `read`, in Python's integers."""
    gamma, unit = board.world.node_clock, board.unit
    found = share.family_share(board.families[index], pairs, board.wrap, gamma, *read, unit)
    return found.astype(object)


def booked(board: Lattice, monkeypatch, *indexes: int) -> list[tuple[int, Fraction]]:  # type: ignore[no-untyped-def]
    """One step of the lattice with the booking identity per act on the families `indexes` (ALGEBRA.md S.6; the advisor's lines, #1563 comments 5954101082 and 5963391333): the share's change over the step is the currents at the pair the step started from with the paces' anisotropy term and Rule3's remainder term, within the division act's floors, plus the face term per face presented at the step, (next - before) R_face (value - arrival) over 2 p_i^2 G^2 (the hole over its two intervals, each shell of the front), the identity on the stepped levels before the lays; the lays (the absorption's and the emission's parts, the emitted quantum, the null window's re-lay) change the share form at the written Nodes and their six neighbours alone, exact; per family the paces' own change of the books' total and the slack."""
    growth.grow(board)  # the receding faces read first, as the step reads them
    gamma, unit, begun, shape = board.world.node_clock, board.unit, {}, board.shape
    for index in indexes:
        read = board.read(index)
        pace = np.asarray(paces.link_pace_of(gamma, read[0])).astype(object)
        flow = [np.asarray(current, dtype=object) for current in board.currents()[index]]
        factors = [np.asarray(q).astype(object) - unit * unit for q in read[1]]
        skew = [q * c for q, c in zip(factors, flow, strict=True)]
        terms = sum(Fraction(int(n), unit * unit) for found in skew for n in found.ravel())
        reads = node.rule_of(board.families[index], gamma, *read, unit)[0]
        squares, net = np.broadcast_to(pace * pace, shape), int(sum(c.sum() for c in flow))
        begun[index] = (read, own_lines(board, index), net, terms, squares, reads)
    stepped, counted = {}, credit.counted_windows

    def kept(b: Lattice) -> bool:  # the lines after the held write, before the NodeDetectors' acts
        stepped.update({i: own_lines(b, i) for i in indexes})
        return counted(b)

    with monkeypatch.context() as swap:
        swap.setattr(credit, "counted_windows", kept), board.step()
    found = []
    for index in indexes:
        read, records, net, terms, squares, reads = begun[index]
        moved, fixed = own_lines(board, index), int(shares_of(board, index, read, stepped[index]).sum())
        for was, now in zip(records, stepped[index], strict=True):  # Rule3's remainder term per line
            step = (now.now.astype(object) - was.before.astype(object)).ravel()  # next - before
            carried = (now.remainder.astype(object) - was.remainder.astype(object)).ravel()  # r' - r
            pairs = zip(step * carried, squares.ravel(), strict=True)
            terms += sum(Fraction(-int(n), 2 * int(d) * unit * unit) for n, d in pairs)
        for face in [f for f in board.credit.faces.get(board.interval, []) if f.family == index]:
            here, fill = (
                tuple(np.add(face.at, board.offset)),
                board.families[index].rest * (face.line == 0),
            )
            arrivals = readings.ports(records[face.line].now, board.wrap, fill)  # the face term per Port
            reach = [
                int(np.asarray(reads[p])[here]) if np.ndim(reads[p]) else int(reads[p])
                for p in face.ports
            ]
            step = int(stepped[index][face.line].now[here]) - int(records[face.line].before[here])
            wall = 2 * int(squares[here]) * unit * unit
            wiped = sum(
                r * (face.value - int(arrivals[p][here])) for r, p in zip(reach, face.ports, strict=True)
            )
            terms += Fraction(step * wiped, wall)
        floors = len(records) * records[0].now.size  # the division act's floor, under one unit per Node
        start = int(shares_of(board, index, read, records).sum())
        assert abs(Fraction(fixed - start - net) - terms) < floors, (index, fixed - start - net, terms)
        delta = shares_of(board, index, read, moved) - shares_of(board, index, read, stepped[index])
        laid = np.zeros(shape, dtype=bool)
        for a, b in zip(stepped[index], moved, strict=True):  # the Nodes a lay wrote
            laid |= (a.now != b.now) | (a.before != b.before) | (a.remainder != b.remainder)
        ports = readings.ports(laid.astype(np.int64), board.wrap)
        near = laid | np.logical_or.reduce([p != 0 for p in ports])
        assert not delta[~near].any() and fixed + int(delta[near].sum()) == int(delta.sum()) + fixed
        found.append((board.total_share(index)[0] - fixed - int(delta.sum()), abs(terms) + floors))  # type: ignore[operator]
    return found


# the builders the parts' tests share (tests/test_part_*.py; the shape of tests/: a helper imported by two files
# lives here): the turning universe's charged record by hand, the Coulomb chain, the one photon's board, a shipped
# world edited beside tmp_path, the emit-and-take world and the fold's floor
TURNING_FILE = EVENTS / "turning.json"
TURNING_INTEGERS, TURNING = universe_of(json.loads(TURNING_FILE.read_text(encoding="utf-8")))
TURNING_T, TURNING_PAIR = TURNING_INTEGERS["quantum_action"], (4000, 6000)
CHARGE = [family.name for family in TURNING].index("charge")
RULE_WALL = coefficients(*TURNING[CHARGE].pair, 6000, 6000, 6000, None, 16)[2]  # w = 6 den Gamma^2 G^2
SINE = 4472  # isqrt(6000^2 - 4000^2): the matter pair's sin omega_0 times den
COULOMB_CHAIN, COULOMB_AT, EMIT_RUN = 400, 280, 200
GRAVITY = {
    "name": "gravity",
    "pair": [6000, 6000],
    "reads": {"gravity": 1},
    "held": {"sources": ["form"], "level_weight": 1000, "write_weight": 1, "rest": 60, "act": "pace"},
}
COULOMB_UNIVERSE = {
    "integers": {"node_clock": 6000, "quantum_action": 36000, "width": 63, "link_unit": 16},
    "families": [
        {
            "name": "charge",
            "pair": [6000, 6000],
            "reads": {},
            "held": {
                "sources": ["wronskian"],
                "level_weight": 100,
                "write_weight": 400,
                "act": "rotation",
            },
        },
        {"name": "charged", "pair": list(TURNING_PAIR), "reads": {"charge": 1}, "dimension": 2},
    ],
}  # the energy line: E_h T num = 100 x 36,000 x 4,000 = k_w Gamma den = 400 x 6,000 x 6,000


def sign_world(tmp_path, name, shape, boundary, intervals, centre, profile):  # type: ignore[no-untyped-def]
    """A world on turning.json's universe with one charged record by hand at the count 1 (the count-1 gate: the profile scaled to one quantum, 2 SUM L^2 sin omega_0 = T, as test_the_node lays it): the level now (L, 0) over `profile` and the level before the band's rest rotation in the sense +1, (L cos omega_0, L sin omega_0)."""
    (tmp_path / "u.json").write_bytes(TURNING_FILE.read_bytes())
    values = [int(v) for v in np.asarray(profile).ravel()]
    scale = math.isqrt(
        TURNING_T * TURNING_PAIR[1] * 1000 * 1000 // (2 * SINE * sum(v * v for v in values))
    )  # one quantum
    levels = [v * scale // 1000 for v in values]  # 2 SUM L^2 sin omega_0 = T, the law's one quantum
    moving = dict(now=levels, before=[v * TURNING_PAIR[0] // TURNING_PAIR[1] for v in levels])
    moving.update(im_now=[0] * len(levels), im_before=[v * SINE // TURNING_PAIR[1] for v in levels])
    body = {"family": "charged", "nodes": [{"node": list(centre), "count": 1}]}
    world = dict(shape=list(shape), boundary=boundary, face_depth=1, intervals=intervals)
    world.update(universe="u.json", node_detectors=[], bodies=[body])
    (path := tmp_path / f"{name}.json").write_text(json.dumps(world), encoding="utf-8")
    mode = {"family": "charged", "pair": list(TURNING_PAIR), "moving": moving}
    beside = {"world_digest": input_digest(world), "bodies": [mode]}
    path.with_suffix(".mode.json").write_text(json.dumps(beside), encoding="utf-8")
    return path


def imaged(a: np.ndarray, axes: tuple[int, ...], signs: tuple[int, ...]) -> np.ndarray:
    return np.transpose(a, axes)[tuple(slice(None, None, s) for s in signs)]


def coulomb_world(
    tmp_path, shape=(COULOMB_CHAIN, 1, 1), boundary=None, intervals=3000, centre=(COULOMB_AT, 0, 0)
):  # type: ignore[no-untyped-def]
    """The Coulomb world: the sign holder alone with a plane record [4000, 6000] reading it (no holder of the content: the vacuum's paces, as the hands' chain), the body a one-quantum profile at the centre (the count-1 gate), the chain x open, y and z periodic of size 1 (the hands' chain of 400)."""
    (tmp_path / "u.json").write_text(json.dumps(COULOMB_UNIVERSE), encoding="utf-8")
    profile = np.zeros(shape, dtype=np.int64)
    profile[centre] = 1
    values = [int(v) for v in profile.ravel()]
    scale = math.isqrt(36000 * TURNING_PAIR[1] * 1000 * 1000 // (2 * SINE * sum(v * v for v in values)))
    levels = [v * scale // 1000 for v in values]
    moving = dict(now=levels, before=[v * TURNING_PAIR[0] // TURNING_PAIR[1] for v in levels])
    moving.update(
        im_now=[0] * len(levels), im_before=[0] * len(levels)
    )  # W = 0: nothing sources the holder at the start (the massless fixed point on 400 Nodes is slow), the record laid by hand after
    body = {"family": "charged", "nodes": [{"node": list(centre), "count": 1}]}
    boundary = boundary or dict(x="open", y="periodic", z="periodic")
    world = dict(shape=list(shape), boundary=boundary, face_depth=1, intervals=intervals)
    world.update(universe="u.json", node_detectors=[], bodies=[body])
    (path := tmp_path / "coulomb.json").write_text(json.dumps(world), encoding="utf-8")
    mode = {"family": "charged", "pair": list(TURNING_PAIR), "moving": moving}
    beside = {"world_digest": input_digest(world), "bodies": [mode]}
    path.with_suffix(".mode.json").write_text(json.dumps(beside), encoding="utf-8")
    return path


def one_photon_board(tmp_path, draw: bool = True):  # type: ignore[no-untyped-def]
    """The anticoincidence world's one photon (examples/events/anticoincidence/one_photon.json) copied beside tmp_path with its universe and its mode file at the copy's digest (`world_beside`), its output kept; without `draw` the bodies' node_detector keys are dropped (the twin that books nothing)."""
    source = EVENTS / "anticoincidence" / "one_photon.json"

    def twin(world):  # type: ignore[no-untyped-def]
        for body in world["bodies"]:  # the parts alone: no draw, no transition, no rate
            body.pop("node_detector"), body.pop("transitions"), body.pop("rates")

    path = world_beside(tmp_path, source, (lambda world: None) if draw else twin)
    return Lattice(load_world(path), (lines := []).append), lines


def world_beside(tmp_path, source, edit):  # type: ignore[no-untyped-def]
    """A shipped world copied under tmp_path at its repository paths with its universe and its mode file at the edited world's digest, the document in the read's shape first (`redeclared`) and `edit` applied after; the repository root moved there."""
    world = redeclared(json.loads(source.read_text(encoding="utf-8")))
    edit(world)
    folder = tmp_path / source.parent.relative_to(EVENTS.parents[1])
    folder.mkdir(parents=True, exist_ok=True)
    (folder / source.name).write_text(json.dumps(world), encoding="utf-8")
    target = tmp_path / world["universe"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((EVENTS.parents[1] / world["universe"]).read_bytes())
    mode = json.loads(source.with_suffix(".mode.json").read_text(encoding="utf-8"))
    mode["world_digest"] = input_digest(world)
    (folder / source.with_suffix(".mode.json").name).write_text(json.dumps(mode), encoding="utf-8")
    world_files.REPOSITORY_ROOT = tmp_path
    return folder / source.name


def emit_and_take_world(tmp_path, emitter_nodes, taker_nodes, window=61):  # type: ignore[no-untyped-def]
    """The resonance world rewritten beside tmp_path: body 0 the emitter on `emitter_nodes` (excited, [2, 3], lifetime 48, its window `window`, 61 by default: in the exact dark its emission falls at its window's close, `meeting.emission_fell`), body 1 the taker on `taker_nodes` (ground, window 48), 200 intervals on the periodic chain of 48."""

    def edit(world):  # type: ignore[no-untyped-def]
        world["intervals"] = EMIT_RUN
        world["bodies"][0]["nodes"] = [{"node": [x, 0, 0], "weight": 1} for x in emitter_nodes]
        world["bodies"][1]["nodes"] = [{"node": [x, 0, 0], "weight": 1} for x in taker_nodes]
        world["bodies"][0]["node_detector"]["window"] = window
        world["bodies"][1]["node_detector"]["window"] = 48

    return world_beside(tmp_path, EVENTS / "resonance" / "resonant.json", edit)


def levels_floor(board: Lattice, index: int, at: np.ndarray) -> int:
    """The floor of a fold's roundings in T's unit (Part F, test 5's floor; the two hands' lines of 2026-10-09): one level unit per rounding at each Node of `at`, meeting the neighbour's level on two Links, 2 SUM over the family's lines and the Nodes of (|now| + |before|), plus one for the reading's own rounding half up."""
    lines = own_lines(board, index)
    levels = sum(
        int(np.abs(r.now.astype(object))[at].sum()) + int(np.abs(r.before.astype(object))[at].sum())
        for r in lines
    )
    return 2 * levels + 1


ORACLE = load_file(
    "step_oracle", ROOT / "tools" / "step_oracle.py"
)  # the step's oracle: the law's first form with the 2.0.0 step around it
arrivals_rule3 = (
    ORACLE.arrivals_rule3
)  # the first form of Rule3, written in the tool and in no file of src/


def flux_world(tmp_path, shape, boundary, intervals=4, level_weight=1):  # type: ignore[no-untyped-def]
    """The rule's universe with the charged plane and gravity carrying the flux's odd lines, on a board."""
    universe_beside(tmp_path, charged=True)
    rows = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    gravity = next(row for row in rows["families"] if row["name"] == "gravity")["held"]
    gravity["sources"], gravity["level_weight"] = ["form", "tensions", "flux"], level_weight
    (tmp_path / "u.json").write_text(json.dumps(rows), encoding="utf-8")
    world = dict(shape=list(shape), boundary=boundary, face_depth=1, intervals=intervals)
    world.update(universe="u.json", bodies=[], node_detectors=[])
    (path := tmp_path / "flux.json").write_text(json.dumps(world), encoding="utf-8")
    return path


def packet(board: Lattice, axis: int, wave: tuple[int, int], size: int, at: int) -> None:
    """A plane-wave packet of the charged family laid by hand, moving along `axis` with the wave number 2 pi wave[0] / wave[1] per Link under a raised-cosine envelope over `size` Nodes from `at`, its level before the wave advanced by the band's own rotation at the vacuum's content, z_before = z_now e^(i omega), the record of positive Wronskian moving toward +a."""
    index = [f.name for f in board.families].index(CHARGED["name"])
    family, gamma = board.families[index], board.world.node_clock
    k = 2 * np.pi * wave[0] / wave[1]
    content = vacuum_content(board.world, family)
    omega = np.arccos(band_of(family.pair, gamma, content, board.unit, np.cos(k), 1.0, 1.0))
    x = np.indices(board.shape)[axis]
    inside = (x >= at) & (x < at + size)  # a raised-cosine window: a locally plane wave
    envelope = 600 * inside * np.sin(np.pi * (x - at + 1) / (size + 1)) ** 2
    phase = k * x
    lines = [
        Record(
            np.rint(envelope * np.cos(phase)).astype(board.kind),
            np.rint(envelope * np.cos(phase + omega)).astype(board.kind),
            board.states[index].lines[0].remainder,
        ),
        Record(
            np.rint(envelope * np.sin(phase)).astype(board.kind),
            np.rint(envelope * np.sin(phase + omega)).astype(board.kind),
            board.states[index].lines[1].remainder,
        ),
    ]
    board.states[index].lines = lines


def d4_bound(board: Lattice, index: int, nodes: Sequence[Node]) -> list[int]:
    """D4's bound on a body's lattice momentum change at a re-lay, per axis, in T's unit (the click's plan, section D4; the chain folder's lay_bounds.py reads the same): one level's change per line and Node at most, so over the Links along the axis with an end at a body Node (a Link to the Node itself across a folded axis is no Link) and over the record's lines, |now_i| + |before_i| + |now_j| + |before_j| + 2; times num in the current's unit."""
    lines = own_lines(board, index)
    placed = [tuple(int(v) for v in np.add(node, board.offset)) for node in nodes]
    found = []
    for axis in range(3):
        links = set()
        for here in placed:
            for step in (-1, 1):
                there = list(here)
                there[axis] += step
                if board.wrap[axis]:
                    there[axis] %= board.shape[axis]
                elif not 0 <= there[axis] < board.shape[axis]:
                    continue
                if tuple(there) != here:
                    links.add(frozenset((here, tuple(there))))
        total = 0
        for link in links:
            for at in link:
                total += sum(abs(int(r.now[at])) + abs(int(r.before[at])) for r in lines)
            total += 2 * len(lines)
        found.append(total)
    return found


def drift_bound(board: Lattice, index: int) -> int:
    """The hands' bound on the integers' drift of P_x per step in T's unit, 2 SUM_i |now_(i+1) - now_(i-1)| over the chain's axis (Part F, test (a); D1, the floors in integers)."""
    chain = board.shape[0]
    found = 0
    for r in own_lines(board, index):
        now = r.now.reshape(-1).astype(object)
        found += int(sum(abs(now[(i + 1) % chain] - now[(i - 1) % chain]) for i in range(chain)))
    return 2 * found


LINE_KEYS = ("now", "before", "remainder")  # a record's three arrays


def family(board: Lattice, name: str) -> int:
    return [f.name for f in board.families].index(name)


def arrays(board: Lattice) -> list[np.ndarray]:
    """Every array of the state: the lines, the write remainders and the phase pairs."""
    found = [getattr(r, k).copy() for s in board.states for r in s.lines for k in LINE_KEYS]
    found += [r.copy() for s in board.states for r in s.write_remainders]
    found += [
        getattr(r, k).copy() for s in board.states for rows in s.phases for r in rows for k in LINE_KEYS
    ]
    return found


def linear_sum(wall: int, line: Record) -> int:
    """The linear sum of one line over the board, L = SUM over the Nodes of [w (now - before) + r], w the family's wall 6 den Gamma^2 G^2 (the flux form of Rule3: w (next - 2 now + before) + r' - r = SUM over the Ports of R_ij (arrival - now) - D now, so the Link terms pair off on a closed board read at one rate and L moves by the mass term alone, zero for light); a lattice reading, no level written."""
    now, before = line.now.astype(object), line.before.astype(object)
    return int((wall * (now - before) + line.remainder.astype(object)).sum())


def linear_exchange(reads: Sequence[Any], line: Record, wrap: Wrap) -> int:
    """The change of a line's linear sum over one interval by its exchange with the board's faces, a family of light (num = den, so D = 0, at any content): -SUM over the Ports of R_ij times the Node's number over every Node whose Port arrives from beyond a face (the fill 0 there), 0 on a periodic axis; with the step's own six reads R_ij, the expected change of L where no other act writes the line, so that a jump beyond it names a level written outside Rule3's line."""
    beyond = readings.ports(np.zeros_like(line.now), wrap, 1)
    now = line.now.astype(object)
    found = 0
    for read, mask in zip(reads, beyond, strict=True):
        where = np.asarray(mask, dtype=bool)
        found += int(
            (np.broadcast_to(np.asarray(read, dtype=object), now.shape)[where] * now[where]).sum()
        )
    return -found


def weighted_linear_sum(wall: int, line: Record, weights: Any) -> int:
    """The linear sum weighted by the Node's rate, L'' = SUM over the Nodes of weight_i x [w (now - before) + r] with weight_i = scale div p_i^2, scale the least common multiple of the distinct p_i^2 on the board, so that every weight is a whole number (the caller's, no division here): R_ij / p_i^2 = 2 num Q_ij G^2 is the same at a Link's two ends whatever their rates, so the weighted Link terms of the flux form pair off on a closed board at any fixed content profile and L'' of light is kept exactly where L moves by the pairing term; a lattice reading."""
    now, before = line.now.astype(object), line.before.astype(object)
    scaled = np.broadcast_to(np.asarray(weights, dtype=object), now.shape)
    return int(((wall * (now - before) + line.remainder.astype(object)) * scaled).sum())


def gate_worlds(build, folder, keys=None):  # type: ignore[no-untyped-def]
    """A gate's folder built from its design beside tmp_path and its worlds run, every one LAWFUL with its parts lines equal across the parts, its credit lines at the window's close and the back-in-time gate MATCH over 4 intervals; `keys` the settings run (every world without): with them each world's own reading (`bell_gate.one_world`) by its setting, without them the folder's reading against the blind (`bell_gate.reading`: the combination, the correlations and the marginals the blind's); with the expectation."""
    build.main(["--design", str(build.HERE / "design.json"), "--folder", str(folder)])
    expected = json.loads((folder / "expectation.json").read_text(encoding="utf-8"))
    worlds = {}
    for key in keys or expected["runs"]:
        name = expected["runs"][key]
        redeclared_file(folder / f"{name}.json")  # the builder's world in the read's shape
        TOOL.main(["--input", str(folder / f"{name}.json")])
        assert RUN.run_input(str(folder / f"{name}.json"), str(folder))["verdict"] == "LAWFUL"
        lines = json.loads((folder / f"{name}.output.json").read_text(encoding="utf-8"))["lines"]
        parts = [line for line in lines if line["event"] == "parts"]
        equal = all(len({*map(tuple, p["levels"])}) == 1 and p["label"] == "NODEDETECTOR" for p in parts)
        credits = [line for line in lines if line["event"] == "credit"]
        assert parts and equal and credits and all(c["interval"] == c["window"][1] for c in credits)
        board = Lattice(load_world(folder / f"{name}.json"))
        assert BACK.verdict(board, 4)["verdict"] == "MATCH"  # exact before the click, the gate per step
        worlds[key] = GATE.one_world(folder / f"{name}.json", lines, expected)
    if keys:
        return worlds, expected
    outputs = [folder / f"{name}.output.json" for name in expected["runs"].values()]
    read, name = GATE.reading(folder / "expectation.json", outputs), expected["combination"]["name"]
    assert read[name] == expected["blind"][name]
    assert read["correlation"] == expected["blind"]["correlation"]
    assert read["marginals"] == expected["blind"]["marginals"]
    return read, expected
